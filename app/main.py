from fastapi import FastAPI
from app.routes import analysis, reports

app = FastAPI()

app.include_router(analysis.router, prefix="/analysis")
app.include_router(reports.router, prefix="/reports")

@app.get("/")
def read_root():
    return {"message": "Welcome to Workplete AI Employee"}
