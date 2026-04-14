from fastapi import FastAPI
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import dal_users
from router_users import router as users_router
from router_ml import router as ml_router

"""
Running Prediction App - Main Entry Point
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    dal_users.create_table_users()
    yield

app = FastAPI(title="Run-Predictor AI Engine", lifespan=lifespan)

app.include_router(users_router)
app.include_router(ml_router)

@app.get("/")
def main_page():
    return FileResponse("running.html")

@app.get("/management")
def management_page():
    return FileResponse("users.html")