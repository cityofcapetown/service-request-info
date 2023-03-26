import contextlib
import logging
import logging.config
import os
from typing import Any, Generator
import uuid

import boto3

from coct_sr_info_server.models.logger import LogConfig


def get_logger() -> logging.Logger:
    if LogConfig().LOGGER_NAME not in logging.root.manager.loggerDict:
        logging.config.dictConfig(LogConfig().dict())

    return logging.getLogger(LogConfig().LOGGER_NAME)


@contextlib.contextmanager
def request_context() -> Generator[str, Any, Any]:
    request_id = str(uuid.uuid4())
    logger = get_logger()

    try:
        # Setting the request ID in the logging formatter
        for handler in logger.handlers:
            handler.formatter.requestId = request_id

        yield request_id
    finally:
        # Clearing the logging formatter
        for handler in logger.handlers:
            handler.formatter.requestId = None


def get_s3_resource() -> boto3.resource:
    boto_session = boto3.session.Session(
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ['AWS_REGION']
    )
    return boto_session.resource('s3',
                                 endpoint_url=os.environ['AWS_S3_ENDPOINT'])
