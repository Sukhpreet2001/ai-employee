from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import analysis, reports

app = FastAPI()

# Serve static files (HTML, JS, CSS) from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routers
app.include_router(analysis.router, prefix="/analysis")
app.include_router(reports.router, prefix="/reports")

@app.get("/")
def read_root():
    return {"message": "Welcome to Workplete AI Employee"}



