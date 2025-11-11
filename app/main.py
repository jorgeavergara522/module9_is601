from fastapi import FastAPI
from app.routers import user_routes
from app.database import init_db

app = FastAPI(title="Module 10 - Secure User API")

@app.on_event("startup")
def on_startup():
    init_db()

# include user routes
app.include_router(user_routes.router)
