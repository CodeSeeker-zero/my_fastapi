from fastapi import FastAPI
import uvicorn

app = FastAPI()


# 必须在 /users/{user_id} 之前定义
@app.get("/users/me")
async def read_user_me():
    """获取当前用户信息"""
    return {"user_id": "the current user"}


if __name__ == "__main__":
    uvicorn.run("111:app", port=8000, reload=True)
