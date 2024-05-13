from pydantic import BaseModel, Field, computed_field
from json import dumps


class AuxBaseModel(BaseModel):
    def json(self):
        return dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def jsonfy(cls, item: dict):
        item["_id"] = str(item["_id"])
        return item
