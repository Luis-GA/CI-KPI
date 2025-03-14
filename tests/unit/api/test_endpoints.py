import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import json

from api.ci.kpi.endpoints import router
from api.ci.kpi.validation_logic import CIValidationException

# Create a test client using the router
client = TestClient(router)

# Sample test data
valid_ci_kpi = {
    "startDate": 1698087500,
    "endDate": 1698097500,
    "project": "repo/test",
    "commitId": "0de83a78334c64250b18b5191f6cbd6b97e77f84",
    "branch": "master",
    "testName": "helm lint",
    "determinist": True,
    "testType": "linter",
    "success": True,
    "result": True,
    "context": {
      "toolUsed": "helm",
      "toolVersion": "1.0.0",
      "environment": "circle-ci"
    }
  }


@pytest.mark.asyncio
@patch('api.ci.kpi.endpoints.list_ci_kpi')
async def test_get_ci_kpi_success(mock_list_ci_kpi):
    """Test successful retrieval of CI KPIs"""
    # Setup mock
    mock_response = [{"testName": "Test1"}, {"testName": "Test2"}]
    mock_list_ci_kpi.return_value = (mock_response, 200)
    
    # Execute request
    response = client.get("/ci_kpi")
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == mock_response
    mock_list_ci_kpi.assert_called_once()


@pytest.mark.asyncio
@patch('api.ci.kpi.endpoints.validate_ci_kpi')
@patch('api.ci.kpi.endpoints.insert_ci_kpi')
async def test_insert_ci_kpi_success(mock_insert_ci_kpi, mock_validate_ci_kpi):
    """Test successful insertion of a CI KPI"""
    # Setup mocks
    mock_validate_ci_kpi.return_value = None
    mock_insert_ci_kpi.return_value = {"id": "123", **valid_ci_kpi}
    
    # Execute request
    response = client.post("/ci_kpi", json=valid_ci_kpi)
    
    # Assertions
    assert response.status_code == 200
    assert "123" == response.json()['id']



@pytest.mark.asyncio
@patch('api.ci.kpi.endpoints.validate_ci_kpi')
async def test_insert_ci_kpi_validation_error(mock_validate_ci_kpi):
    """Test insertion with validation error"""
    # Setup mock to raise validation exception
    validation_errors = {
        "error_counter": 1,
        "errors": {
            "required": ["'testName' is a required property"]
        }
    }
    mock_validate_ci_kpi.side_effect = CIValidationException(validation_errors)
    
    # Execute request
    response = client.post("/ci_kpi", json=valid_ci_kpi)
    
    # Assertions
    assert response.status_code == 422
    assert response.json() == validation_errors


@pytest.mark.asyncio
@patch('api.ci.kpi.endpoints.validate_ci_kpi')
@patch('api.ci.kpi.endpoints.insert_ci_kpi')
async def test_insert_ci_kpi_general_error(mock_insert_ci_kpi, mock_validate_ci_kpi):
    """Test insertion with a general error"""
    # Setup mocks
    mock_validate_ci_kpi.return_value = None
    mock_insert_ci_kpi.side_effect = Exception("Database connection error")
    
    # Execute request
    response = client.post("/ci_kpi", json=valid_ci_kpi)
    
    # Assertions
    assert response.status_code == 400
    assert response.json() == {"error": "Database connection error"}


@pytest.mark.asyncio
@patch('api.ci.kpi.endpoints.delete_ci_kpi')
async def test_delete_ci_kpi_success(mock_delete_ci_kpi):
    """Test successful deletion of a CI KPI"""
    # Setup mock
    mock_delete_ci_kpi.return_value = ({"deleted": True}, 200)
    
    # Execute request
    response = client.delete("/ci_kpi/123")
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == {"deleted": True}
    mock_delete_ci_kpi.assert_called_once_with("123")


@pytest.mark.asyncio
@patch('api.ci.kpi.endpoints.delete_ci_kpi')
async def test_delete_ci_kpi_not_found(mock_delete_ci_kpi):
    """Test deletion of a non-existent CI KPI"""
    # Setup mock
    mock_delete_ci_kpi.return_value = ({"error": "CI KPI not found"}, 404)
    
    # Execute request
    response = client.delete("/ci_kpi/999")
    
    # Assertions
    assert response.status_code == 404
    assert response.json() == {"error": "CI KPI not found"}
    mock_delete_ci_kpi.assert_called_once_with("999")