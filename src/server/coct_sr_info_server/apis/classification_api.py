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

from coct_sr_info_server.models.extra_models import TokenModel  # noqa: F401
from coct_sr_info_server.models.image_recognition_schema import ImageRecognitionSchema


router = APIRouter()


@router.post(
    "/dev/service-request/image_classification/",
    responses={
        200: {"model": List[ImageRecognitionSchema], "description": "OK"},
        500: {"description": "Something has gone wrong with our server"},
    },
    tags=["classification"],
    summary="Warning! Experimental endpoint for image classification",
    response_model_by_alias=True,
)
async def dev_service_request_image_classification_post(
    body: str = Body(None, description=""),
) -> List[ImageRecognitionSchema]:
    ...
