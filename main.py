from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
import uvicorn



async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


# 全局依赖：所有路由都需要通过 token 校验
app = FastAPI(dependencies=[Depends(verify_token)])


@app.get("/items/")
async def read_items():
    return JSONResponse(content={"items": []}, status_code=200)
    #return [{"item": "Foo"}]


@app.get("/users/")
async def read_users():
    return [{"user": "Bar"}]


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
