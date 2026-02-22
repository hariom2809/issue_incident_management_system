from fastapi import FastAPI
from app.database.database import engine, Base
from app.models import *
from app.routes import auth, issues, audit, comments
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Issue & Incident Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(issues.router)
app.include_router(audit.router)
app.include_router(comments.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "Backend running"}
