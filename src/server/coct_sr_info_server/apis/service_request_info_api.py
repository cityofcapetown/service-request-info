# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from coct_sr_info_server.logic import utils, city_api_interface
from coct_sr_info_server.models.extra_models import TokenModel  # noqa: F401
from coct_sr_info_server.models.service_request_schema import ServiceRequestSchema
from coct_sr_info_server.models.service_request_stats_schema import ServiceRequestStatsSchema


router = APIRouter()


@router.get(
    "/v1/service-request/stats/",
    responses={
        200: {"model": List[ServiceRequestStatsSchema], "description": "OK"},
        400: {"description": "One of the input parameters don&#39;t make sense"},
        404: {"description": "Either that area or type doesn&#39;t appear to exist"},
        500: {"description": "Something has gone wrong with our server"},
        502: {"description": "We can&#39;t talk to a server we rely upon"},
        503: {"description": "We can&#39;t handle your request right now"},
    },
    tags=["service_request_info"],
    summary="Get statistical information on service requests for a given area and type",
    response_model_by_alias=True,
)
async def v1_service_request_stats_get(
    area: str = Query(None, description=""),
    type_identifier: str = Query(None, description=""),
) -> List[ServiceRequestStatsSchema]:
    ...


@router.get(
    "/v1/service-request/status/",
    responses={
        200: {"model": List[ServiceRequestSchema], "description": "OK"},
        400: {"description": "One of the input parameters don&#39;t make sense"},
        404: {"description": "This SR doesn&#39;t appear to exist"},
        500: {"description": "Something has gone wrong with our server"},
        502: {"description": "We can&#39;t talk to the City&#39;s SR API"},
        503: {"description": "We can&#39;t handle your request right now"},
    },
    tags=["service_request_info"],
    summary="Get the status of a particular service request",
    response_model_by_alias=True,
)
async def v1_service_request_status_get(
    service_request_no: str = Query(None, description="Unique identifier of service request"),
) -> List[ServiceRequestSchema]:
    logger = utils.get_logger()
    with utils.request_context() as request_id:
        logger.debug(f"{request_id=}")
        return [city_api_interface.get_sr_status(request_id, service_request_no)]
