from fastapi import FastAPI
from dotenv import load_dotenv
import os

# ✅ load environment variables at app startup
load_dotenv()

app = FastAPI(title="AITCAL Infra API")

from app.company.auth.routes_auth import router as auth_router
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
