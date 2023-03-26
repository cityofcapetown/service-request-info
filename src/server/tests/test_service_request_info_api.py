# coding: utf-8

from fastapi.testclient import TestClient


from coct_sr_info_server.models.service_request_schema import ServiceRequestSchema  # noqa: F401
from coct_sr_info_server.models.service_request_stats_schema import ServiceRequestStatsSchema  # noqa: F401


def test_v1_service_request_stats_get(client: TestClient):
    """Test case for v1_service_request_stats_get

    Get statistical information on service requests for a given area and type
    """
    params = [("area", 'Simon's Town'),     ("type_identifier", 'type_identifier_example')]
    headers = {
    }
    response = client.request(
        "GET",
        "/v1/service-request/stats/",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_v1_service_request_status_get(client: TestClient):
    """Test case for v1_service_request_status_get

    Get the status of a particular service request
    """
    params = [("service_request_no", '987654567')]
    headers = {
    }
    response = client.request(
        "GET",
        "/v1/service-request/status/",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

