from fastapi import FastAPI
from database.database import engine, Base
from models import *
from routes import auth, issues, audit

app = FastAPI(title="Issue & Incident Management System")
app.include_router(auth.router)
app.include_router(issues.router)
app.include_router(audit.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "Backend running"}
