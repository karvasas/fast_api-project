import importlib
import os
from contextlib import suppress

from fastapi import FastAPI, Request, Response, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.router import router
from core.exceptions import BaseAppException
from core.response import Error

BEARER_JWT_KEY = HTTPBearer(scheme_name="JWT", auto_error=False)


async def _build_swagger_jwt(
        _: HTTPAuthorizationCredentials | None = Security(BEARER_JWT_KEY)
):
    # Функция нужна, чтобы сделать JWT-авторизацию в сваггере с текущей auth реализацией
    return


async def log_request(
        request: Request,
        response: Response
):
    _msg = f"Request: [{request.method}] -> {request.url} < {request.headers} << {request.path_params}"
    with suppress(Exception):
        _msg += f" <<< {await request.json()}"
    print(_msg)

    try:
        yield
    except BaseAppException as e:
        resp_err = Error(name=str(e), extra_info=e.err_info())

        print(
            f"Response: [{request.method}] -> {request.url} >>> "
            f"BaseAppException {e.status_code=} {resp_err}"
        )

        raise
    except Exception as e:
        print(f"InternalServerError {e}")
        raise


app = FastAPI(
    dependencies=[
        Depends(_build_swagger_jwt),
        Depends(log_request)
    ]
)

for obj in os.scandir("app"):
    if obj.is_dir():
        if os.path.isfile(f"app/{obj.name}/router.py"):
            r = importlib.import_module(f"app.{obj.name}.router")
        app.include_router(r.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
