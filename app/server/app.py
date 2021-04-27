from fastapi import FastAPI
from app.server.route.student import router as StudentRouter
from app.server.kafka_io.kafka_conn import aioproducer

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")


@app.on_event("startup")
async def startup_event():
    await aioproducer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

