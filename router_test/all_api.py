from fastapi import FastAPI
from student import router as student_router
from user import router as user_router
import uvicorn

app = FastAPI()

app.include_router(student_router, prefix="/student", tags=["student"])
app.include_router(user_router, prefix="/user", tags=["user"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
