from jsonschema.validators import Draft7Validator

from api.ci.kpi.models import CI_KPI_JSON_SCHEMA


class CIValidationException(Exception):
    errors = {}

    def __init__(self, errors):
        self.errors = errors
        super().__init__(self.errors)


def validate_ci_kpi(ci_kpi: dict):
    """
    Validates the ci KPI
    :param ci_kpi: dict of the ci_KPI
    :return: None in case of success, a dict in case of failure with all the errors descriptors
    """
    list_of_errors = {}
    error_counter = 0
    validator = Draft7Validator(CI_KPI_JSON_SCHEMA)
    response = None

    errors = list(validator.iter_errors(ci_kpi))
    if errors:
        for error in errors:
            error_counter += 1
            error_path = error.absolute_path[0] if error.absolute_path else error.schema_path[0]

            if not list_of_errors.get(error_path):
                list_of_errors[error_path] = {"error_reasons": [error.message], "schema_to_satisfy": error.schema}
            else:
                list_of_errors[error_path]["error_reasons"].append(error.message)

        raise CIValidationException({"error_counter": error_counter, "errors": list_of_errors})
    return response
