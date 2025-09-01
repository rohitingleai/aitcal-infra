from fastapi import FastAPI
from app.company.auth.routes_auth import router as auth_router

app = FastAPI(title="AITCAL Infra API")

# include routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])