from fastapi import FastAPI

from starlette.responses import RedirectResponse

from api.ci.kpi import endpoints as ci_kpi_imports

app = FastAPI(
    title="CICD Observability  in Cloud Native",
    description="OpenAPI to manage the entire CICD Observability",
    summary="Server Management",
    version="0.0.1",
    contact={
        "name": "Luis Gómez Alonso",
        "url": "https://www.linkedin.com/in/luis-g%C3%B3mez-alonso-5a661088/",
        "email": "luis.gomez.alonso95@gmail.com",
    },
    license_info={
        "name": "GNU LESSER GENERAL PUBLIC LICENSE",
        "url": "https://www.gnu.org/licenses/lgpl-3.0.en.html",
    },
)

app.include_router(ci_kpi_imports.router)


@app.get("/", include_in_schema=False)
def redirect_to_openapi():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_check():
    return {"status": "Success"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
