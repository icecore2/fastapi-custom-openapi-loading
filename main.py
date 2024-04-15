import json
import logging
import os
import time
import uuid

import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()

logger = logging.getLogger(__name__)
logging.config.fileConfig(
    fname=os.path.join('.', 'logging.conf'),
    disable_existing_loggers=False
)
logger.info('API is starting up')
logger.debug(f"Routes loaded: {[getattr(x, 'path') for x in app.routes]}")


@app.get("{path}")
async def read_items(path, request):
    body = await request.get_json()
    return [{path: body}]


@app.middleware("http")
async def log_requests(request: Request, call_next):
    item = uuid.uuid4()

    logger.info(f"req_id={item} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    logger.info(f"req_id={item} completed_in={process_time:.2f}ms status_code={response.status_code}")

    return response


def custom_openapi():
    openapi_filename = 'openapi.json'
    openapi_path = os.path.join(os.path.dirname(__file__), 'static', openapi_filename)

    with open(openapi_path, "r") as openapi:
        return json.load(openapi)


app.openapi = custom_openapi

test_json = {
    "data": {
        "test_data": ["test_value", "test_value2", "test_value3"],
        "test_data2": "test_value2",
        "test_data3": "test_value3",
        "test_data4": "test_value4",
        "test_data5": "test_value5",
        "test_data6": "test_value6",
    }
}


def run():
    uvicorn.run(app, host="127.0.0.1")


if __name__ == '__main__':
    run()
