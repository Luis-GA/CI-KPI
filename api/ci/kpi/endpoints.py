from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from json import loads as json_loads

from api.ci.kpi.models import CI_KPI
from .db_queries import delete_ci_kpi, list_ci_kpi, insert_ci_kpi
from .validation_logic import validate_ci_kpi, CIValidationException

router = APIRouter()


@router.get("/ci_kpi", tags=["CI_KPI"], summary="Retrieve the list of CI KPIs")
async def get_vc_ids(query: str = Query(default="{}",
                                        description="Query following the syntax of [MongoDB query spec](https://www.mongodb.com/docs/manual/tutorial/query-documents/)"),
                     projection: str = Query(default="{}",
                                             description="Projection of the response (to increase the performance) following the syntax of [MongoDB query spec](https://www.mongodb.com/docs/manual/tutorial/query-documents/)"),
                     JSONata: str = Query(default="",
                                          description="Query & transformation language. [JSONata spec](https://jsonata.org/) Version used: 1.8.6")
                     ):
    return JSONResponse(*await list_ci_kpi(json_loads(query), json_loads(projection), JSONata))


@router.post("/ci_kpi", tags=["CI_KPI"], summary="Upsert a new CI KPI")
async def insert_vc_id(ci_kpi: CI_KPI):
    status_code = 200
    response = None
    try:
        response = validate_ci_kpi(ci_kpi.dict())
        if not response:
            response = await insert_ci_kpi(ci_kpi)

    except CIValidationException as exc:
        response = exc.errors
        status_code = 422

    except Exception as exc:
        response = {"error": str(exc)}
        status_code = 400
    finally:
        return JSONResponse(response, status_code)


@router.delete("/ci_kpi/{ci_kpi_id}", tags=["CI_KPI"], summary="Delete a existing CI KPI")
async def delete_vc(ci_kpi_id: str):
    return JSONResponse(*await delete_ci_kpi(ci_kpi_id))
