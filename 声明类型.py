from typing import Annotated

from fastapi import FastAPI, Query

import uvicorn

app = FastAPI()


@app.get("/user/")
async def get_q(name: Annotated[str | None, Query(min_length=3)] = None):
    return {"name": name}


if __name__ == "__main__":
    uvicorn.run(app, port=8888)
