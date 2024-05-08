from pydantic import BaseModel
from json import dumps


class AuxBaseModel(BaseModel):
    def json(self):
        return dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def dict(self):
        return dict(self)

    @classmethod
    def jsonfy(cls, item: dict):
        item["_id"] = str(item["_id"])
        return item
