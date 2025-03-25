from pydantic import BaseModel, Field, computed_field
from json import dumps, load
from pathlib import Path

CI_KPI_PATH = str(Path(__file__).absolute().parent) + "/json_schema/ci_testing.json"

with open(CI_KPI_PATH) as f:
    CI_KPI_JSON_SCHEMA = load(f)

class AuxBaseModel(BaseModel):
    def json(self):
        return dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def jsonfy(cls, item: dict):
        item["_id"] = str(item["_id"])
        return item
