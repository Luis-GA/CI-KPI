import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import json
from bson import ObjectId

from api.ci.kpi.db_queries import list_ci_kpi, insert_ci_kpi, delete_ci_kpi
from api.ci.kpi.models import CI_KPI


@pytest.fixture
def sample_ci_kpi_data():
    return {
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


@pytest.fixture
def sample_ci_kpi_model(sample_ci_kpi_data):
    return CI_KPI(**sample_ci_kpi_data)


@pytest.mark.asyncio
@patch('api.ci.kpi.db_queries.ci_kpi_collection')
async def test_list_ci_kpi_basic(mock_collection, sample_ci_kpi_data):
    """Test basic listing of CI KPIs without projection or JSONata"""
    # Setup mock
    mock_cursor = AsyncMock()
    mock_cursor.__aiter__.return_value = [
        {"_id": ObjectId("60d21b4667d0d8992e610c85"), **sample_ci_kpi_data},
        {"_id": ObjectId("60d21b4667d0d8992e610c86"), **sample_ci_kpi_data}
    ]
    mock_collection.find.return_value = mock_cursor
    
    # Execute function
    result, status_code = await list_ci_kpi({})
    
    # Assertions
    assert status_code == 200
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)
    assert all("_id" in item for item in result)
    mock_collection.find.assert_called_once_with({})


@pytest.mark.asyncio
@patch('api.ci.kpi.db_queries.ci_kpi_collection')
async def test_list_ci_kpi_with_projection(mock_collection, sample_ci_kpi_data):
    """Test listing CI KPIs with projection"""
    # Setup mock
    mock_cursor = AsyncMock()
    mock_cursor.__aiter__.return_value = [
        {"_id": ObjectId("60d21b4667d0d8992e610c85"), "testName": "SampleTest"},
        {"_id": ObjectId("60d21b4667d0d8992e610c86"), "testName": "SampleTest2"}
    ]
    mock_collection.find.return_value = mock_cursor
    
    # Execute function
    projection = {"testName": 1}
    result, status_code = await list_ci_kpi({}, projection)
    
    # Assertions
    assert status_code == 200
    assert len(result) == 2
    assert all("testName" in item for item in result)
    mock_collection.find.assert_called_once_with({}, projection)


@pytest.mark.asyncio
@patch('api.ci.kpi.db_queries.ci_kpi_collection')
@patch('api.ci.kpi.db_queries.jsonata.Context')
async def test_list_ci_kpi_with_jsonata(mock_jsonata_context, mock_collection, sample_ci_kpi_data):
    """Test listing CI KPIs with JSONata query"""
    # Setup mocks
    mock_cursor = AsyncMock()
    mock_cursor.__aiter__.return_value = [
        {"_id": ObjectId("60d21b4667d0d8992e610c85"), **sample_ci_kpi_data},
        {"_id": ObjectId("60d21b4667d0d8992e610c86"), **sample_ci_kpi_data}
    ]
    mock_collection.find.return_value = mock_cursor
    
    mock_context_instance = MagicMock()
    mock_context_instance.return_value = [{"testName": "SampleTest"}]
    mock_jsonata_context.return_value = mock_context_instance
    
    # Execute function
    jsonata_query = "$[testType='unitTest']"
    result, status_code = await list_ci_kpi({}, None, jsonata_query)
    
    # Assertions
    assert status_code == 200
    assert result == [{"testName": "SampleTest"}]
    mock_collection.find.assert_called_once_with({})
    mock_jsonata_context.assert_called_once_with(bigint_patch=True)
    mock_context_instance.assert_called_once()


@pytest.mark.asyncio
@patch('api.ci.kpi.db_queries.ci_kpi_collection')
@patch('api.ci.kpi.db_queries.jsonata.Context')
async def test_list_ci_kpi_with_jsonata_error(mock_jsonata_context, mock_collection, sample_ci_kpi_data):
    """Test listing CI KPIs with invalid JSONata query"""
    # Setup mocks
    mock_cursor = AsyncMock()
    mock_cursor.__aiter__.return_value = [
        {"_id": ObjectId("60d21b4667d0d8992e610c85"), **sample_ci_kpi_data}
    ]
    mock_collection.find.return_value = mock_cursor
    
    mock_context_instance = MagicMock()
    mock_context_instance.side_effect = Exception('{"message": "Invalid JSONata query"}')
    mock_jsonata_context.return_value = mock_context_instance
    
    # Execute function
    jsonata_query = "$[invalid query]"
    result, status_code = await list_ci_kpi({}, None, jsonata_query)
    
    # Assertions
    assert status_code == 400
    assert "errorType" in result
    assert result["errorType"] == "JSONata query"
    assert "reason" in result
    assert result["reason"] == "Invalid JSONata query"


@pytest.mark.asyncio
@patch('api.ci.kpi.db_queries.ci_kpi_collection')
async def test_insert_ci_kpi(mock_collection, sample_ci_kpi_model):
    """Test inserting a CI KPI"""
    # Setup mock
    mock_result = MagicMock()
    mock_result.inserted_id = ObjectId("60d21b4667d0d8992e610c85")
    mock_collection.insert_one.return_value = AsyncMock(return_value=mock_result)()
    
    # Execute function
    result = await insert_ci_kpi(sample_ci_kpi_model)
    
    # Assertions
    assert "_id" in result
    assert result["_id"] == "60d21b4667d0d8992e610c85"
    mock_collection.insert_one.assert_called_once_with(sample_ci_kpi_model.dict())


@pytest.mark.asyncio
@patch('api.ci.kpi.db_queries.ci_kpi_collection')
async def test_delete_ci_kpi_success(mock_collection):
    """Test successful deletion of a CI KPI"""
    # Setup mock
    mock_result = MagicMock()
    mock_result.deleted_count = 1
    mock_collection.delete_one.return_value = AsyncMock(return_value=mock_result)()

    # Execute function
    result, status_code = await delete_ci_kpi("60d21b4667d0d8992e610c85")
    
    # Assertions
    assert status_code == 200
    assert result["status"] == "success"
    mock_collection.delete_one.assert_called_once_with({"_id": ObjectId("60d21b4667d0d8992e610c85")})


@pytest.mark.asyncio
@patch('api.ci.kpi.db_queries.ci_kpi_collection')
async def test_delete_ci_kpi_not_found(mock_collection):
    """Test deletion of a non-existent CI KPI"""
    # Setup mock
    mock_result = MagicMock()
    mock_result.deleted_count = 0
    mock_collection.delete_one.return_value = AsyncMock(return_value=mock_result)()
    
    # Execute function
    result, status_code = await delete_ci_kpi("60d21b4667d0d8992e610c85")
    
    # Assertions
    assert status_code == 404
    assert result["status"] == "not found"
    mock_collection.delete_one.assert_called_once_with({"_id": ObjectId("60d21b4667d0d8992e610c85")})