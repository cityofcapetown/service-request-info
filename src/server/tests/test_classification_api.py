# coding: utf-8

from fastapi.testclient import TestClient


from coct_sr_info_server.models.image_recognition_schema import ImageRecognitionSchema  # noqa: F401


def test_dev_service_request_image_classification_post(client: TestClient):
    """Test case for dev_service_request_image_classification_post

    Warning! Experimental endpoint for image classification
    """
    body = '/path/to/file'

    headers = {
    }
    response = client.request(
        "POST",
        "/dev/service-request/image_classification/",
        headers=headers,
        json=body,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

