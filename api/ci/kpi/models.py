from model.base_model import AuxBaseModel, Field, computed_field, CI_KPI_JSON_SCHEMA
from typing import Union

class ADDONS(AuxBaseModel):
    version: str
    name: str


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
    addons: list[ADDONS] = Field(default_factory=lambda: [])

    @computed_field
    @property
    def duration(self) -> int:
        return self.endDate - self.startDate
