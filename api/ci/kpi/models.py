from model.base_model import AuxBaseModel
from typing import Union
import json

CI_KPI_RELATIVE_PATH = "././model/json_schema/ci_testing.json"


class CI_KPI(AuxBaseModel):
    startDate: int
    endDate: int
    project: str
    commitId: str
    branch: str
    testName: str
    determinist: bool
    testType: str
    success: bool
    context: dict
    result: Union[bool, dict, str, int]


with open(CI_KPI_RELATIVE_PATH) as f:
    CI_KPI_JSON_SCHEMA = json.load(f)
