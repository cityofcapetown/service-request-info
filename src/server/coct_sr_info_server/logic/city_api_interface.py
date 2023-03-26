import bz2
import datetime
import functools
import gzip
import json
import os
import typing
import zipfile

import coct_sr_api_client
from coct_sr_api_client.apis.tags import auth_group_api, config_group_api, service_request_group_api

from coct_sr_info_server.models.service_request_schema import ServiceRequestSchema
from coct_sr_info_server.logic import utils

SR_ATTR_CACHE_BUCKET = "service-request-info-api.sr-cache"


@functools.lru_cache(1)
def _get_sr_api_configuration(public_key_env_var: str = "COCT_SR_API_PUBLIC_KEY",
                              private_key_env_var: str = "COCT_SR_API_PRIVATE_KEY",
                              host="https://qaeservices1.capetown.gov.za/coct/api") -> coct_sr_api_client.Configuration:
    logger = utils.get_logger()

    configuration = coct_sr_api_client.Configuration(
        host=host
    )
    # Setting the service Identifier
    public_key = os.environ[public_key_env_var]
    configuration.api_key['serviceAuth'] = public_key.replace("-", "")

    with coct_sr_api_client.ApiClient(configuration) as api_client:
        auth_api_instance = auth_group_api.AuthGroupApi(api_client)
        logger.info("Logging into API")
        private_key = os.environ[private_key_env_var]
        login_response = auth_api_instance.zcur_guest_login_get({"cookie": private_key.replace("-", "")})

        # Copying out the auth cookie, and setting it
        # clunkier than I expected
        set_cookie = login_response.response.headers['set-cookie']
        sap_sso_cookie, *_ = set_cookie.split(";")
        configuration.api_key['cookieAuth'] = sap_sso_cookie

        logger.info("Logged into API")

        logger.info("Starting an API session")
        # Setting the API session
        session_response = auth_api_instance.zsreq_session_get()
        configuration.api_key['sessionAuth'] = session_response.body.session_id

    return configuration


@functools.lru_cache(1)
def _get_types_lookup(request_id: str):
    logger = utils.get_logger()
    logger.info("Getting SR types...")
    logger.debug(f"{request_id=}")

    configuration = _get_sr_api_configuration()
    with coct_sr_api_client.ApiClient(configuration) as api_client:
        config_api_instance = config_group_api.ConfigGroupApi(api_client)
        types_response = config_api_instance.zsreq_config_types_get()

    logger.info("...Got SR types")

    return types_response.body


@functools.lru_cache()
def _query_sr_attr_cache(sr_number: str, cache_key: str) -> typing.Dict:
    logger = utils.get_logger()
    s3 = utils.get_s3_resource()
    s3_key = f"sr-cache-{cache_key}.json.bz2"

    cache_data = {}
    try:
        s3_bucket = s3.Bucket(SR_ATTR_CACHE_BUCKET)
        s3_objects = list(s3_bucket.objects.filter(Prefix=s3_key, MaxKeys=1))

        if len(s3_objects) == 0:
            logger.info("Nothing in S3 attribute cache")
        else:
            logger.info("Something in S3 attribute cache!")
            s3_object, *_ = s3_objects
            s3_object_body = s3_object.get()['Body']
            with bz2.open(s3_object_body, 'r') as bz2_content:
                cache_data = json.load(bz2_content)
    except Exception as e:
        logger.warning(
            f'Error {e.__class__.__name__} retrieving cache object {s3_key} from bucket {SR_ATTR_CACHE_BUCKET}')
        logger.debug(f"Error: {e}")
    finally:
        return cache_data.get(sr_number, {})


def get_sr_status(request_id: str, sr_number: str) -> ServiceRequestSchema:
    logger = utils.get_logger()
    logger.debug(f"{sr_number=}")

    configuration = _get_sr_api_configuration()
    with coct_sr_api_client.ApiClient(configuration) as api_client:
        sr_api_instance = service_request_group_api.ServiceRequestGroupApi(api_client)
        logger.info("Fetching SR status...")
        sr_status_response = sr_api_instance.zsreq_sr_reference_no_get({"reference_no": sr_number})
        logger.info("...Fetched SR status...")

    sr_status = sr_status_response.body
    sr_status_dict = dict(
        sr_status=sr_status.status,
        message=sr_status.message,
        type=sr_status.type,
        subtype=sr_status.subtype,
    )

    date_created = datetime.datetime.strptime(sr_status['created_on'], "%d.%m.%Y %H:%M:%S")
    cache_dict = _query_sr_attr_cache(sr_number, date_created.strftime("%Y-%m-%d"))
    combined_dict = {
        **sr_status_dict,
        **cache_dict
    }

    logger.info("Forming response and returning")
    return ServiceRequestSchema(
        id=request_id,
        **combined_dict
    )
