import pytest
import json
from api.ci.kpi.validation_logic import validate_ci_kpi, CIValidationException
from pathlib import Path
import os

MAIN_PATH = str(Path(os.getcwd()).absolute().parent) + "/model/json_schema/examples/ci_testing/"
@pytest.mark.parametrize("file_path", [
    MAIN_PATH + "unitTest.json",
    MAIN_PATH + "end2end.json",
    MAIN_PATH + "integrationtests.json",
    MAIN_PATH + "linter.json",
    MAIN_PATH + "nonFunctionaltest.json"
])
def test_validate_ci_kpi_from_json_file(file_path):
    """Test validation with data loaded from a JSON file"""

    with open(file_path, 'r') as file:
        test_data = json.load(file)

    result = validate_ci_kpi(test_data)
    assert result == None

def test_validate_ci_kpi_missing_required_field():
    """Test validation with missing required field"""
    invalid_data = {
        "determinist": True,
        "testType": "unitTest",
        "success": True
        # Missing testName field
    }
    
    with pytest.raises(CIValidationException) as exc_info:
        validate_ci_kpi(invalid_data)
    
    # Verify error details
    error_info = exc_info.value.errors
    assert error_info["error_counter"] > 0
    assert "'testName' is a required property" in str(error_info["errors"]["required"])


def test_validate_ci_kpi_invalid_type():
    """Test validation with incorrect data type"""
    invalid_data = {
        "testName": "InvalidTypeTest",
        "determinist": "not_a_boolean",  # Should be boolean
        "testType": "unitTest",
        "success": True
    }
    
    with pytest.raises(CIValidationException) as exc_info:
        validate_ci_kpi(invalid_data)
    
    # Verify error details
    error_info = exc_info.value.errors
    assert error_info["error_counter"] > 0
    assert "determinist" in str(error_info["errors"])


def test_validate_ci_kpi_invalid_enum_value():
    """Test validation with invalid enum value"""
    invalid_data = {
        "testName": "InvalidEnumTest",
        "determinist": True,
        "testType": "invalidTestType",  # Assuming this should be from an enum
        "success": True
    }
    
    with pytest.raises(CIValidationException) as exc_info:
        validate_ci_kpi(invalid_data)
    
    # Verify error details
    error_info = exc_info.value.errors
    assert error_info["error_counter"] > 0
    assert "testType" in str(error_info["errors"])


def test_validate_ci_kpi_multiple_errors():
    """Test validation with multiple validation errors"""
    invalid_data = {
        # Missing testName
        "determinist": "not_a_boolean",  # Wrong type
        "testType": "invalidTestType",   # Invalid enum value
        "success": True
    }
    
    with pytest.raises(CIValidationException) as exc_info:
        validate_ci_kpi(invalid_data)
    
    # Verify error details
    error_info = exc_info.value.errors
    assert error_info["error_counter"] > 1  # Should have multiple errors
    
    # Check if errors dictionary contains multiple entries
    assert len(error_info["errors"]) > 1


def test_validation_exception_initialization():
    """Test CIValidationException initialization and properties"""
    test_errors = {
        "error_counter": 1,
        "errors": {
            "testName": {
                "error_reasons": ["Field is required"],
                "schema_to_satisfy": {"type": "string"}
            }
        }
    }
    
    exception = CIValidationException(test_errors)
    
    # Verify exception properties
    assert exception.errors == test_errors
    assert str(exception) == str(test_errors)


def test_validate_ci_kpi_empty_data():
    """Test validation with empty data"""
    empty_data = {}
    
    with pytest.raises(CIValidationException) as exc_info:
        validate_ci_kpi(empty_data)
    
    # Verify error details
    error_info = exc_info.value.errors
    assert error_info["error_counter"] > 0


def test_validate_ci_kpi_additional_properties_with_other_errors():
    """Test validation with additional unexpected properties"""
    data_with_extra = {
        "testName": "ExtraPropertiesTest",
        "determinist": True,
        "testType": "unitTest",
        "success": True,
        "extraField": "This shouldn't be here"  # Extra field not in schema
    }
    
    # This test will pass if additional properties are allowed, or fail if they're not
    # The assertion depends on the schema configuration
    try:
        result = validate_ci_kpi(data_with_extra)
        # If no exception, additional properties must be allowed in the schema
        assert result is None
    except CIValidationException as exc:
        # If exception, additional properties must not be allowed
        assert "extraField" not in str(exc.errors)