from db.db_driver import database, ObjectId
from .models import CI_KPI
import jsonata
import json

ci_kpi_collection = database.ci_kpi


async def list_ci_kpi(query: dict, projection: dict = None, jsonata_query: str = ""):
    """
    Query to return the set of ci KPIs
    :param query: dict
    :param projection: dict
    :param jsonata_query: string
    :return: list of projects
    """
    result = []
    status_code = 200
    if projection:
        async for document in ci_kpi_collection.find(query, projection):
            result.append(CI_KPI.jsonfy(document))
    else:
        async for document in ci_kpi_collection.find(query):
            result.append(CI_KPI.jsonfy(document))
    if jsonata_query:
        try:
            result = jsonata.Context(bigint_patch=True)(jsonata_query, result)
        except Exception as ex:
            status_code = 400
            reason = str(ex)
            if reason[0] == "{":
                reason = json.loads(reason).get("message")
            result = {"errorType": "JSONata query", "reason": reason}
    return result, status_code


async def insert_ci_kpi(item: CI_KPI):
    """
    Insert ci kpi
    :param item: CI_KPI
    :return:
    """
    result = await ci_kpi_collection.insert_one(item.dict())
    return {"_id": str(result.inserted_id)}


async def delete_ci_kpi(ci_kpi_id: str):
    """
    Delete a ci kpi
    :param ci_kpi_id: id of the ci_kpi to delete
    :return: success or not found
    """
    result = await ci_kpi_collection.delete_one({"_id": ObjectId(ci_kpi_id)})
    response = {"status": "success"}
    status_code = 200
    if result.deleted_count != 1:
        response = {"status": "not found"}
        status_code = 404
    return response, status_code
