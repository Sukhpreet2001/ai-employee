from fastapi import FastAPI
from app.routes import analysis, reports

app = FastAPI()

# Include routes from analysis and reports
app.include_router(analysis.router)
app.include_router(reports.router)

# Serve the static files (if needed)
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Employee system!"}



