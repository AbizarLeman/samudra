from typing import Dict

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from samudra.conf.server.cors_policy import ALLOWED_ORIGINS
from samudra.server.setup import check_tables
from server import lemmas

SLEEP_TIME: int = 10

app = FastAPI()

app.include_router(lemmas.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root() -> Dict[str, str]:
    return {"details": "Successfully connected!"}


if __name__ == '__main__':
    check_tables(create_tables=True)
    uvicorn.run("serve:app", port=8000, reload=True)