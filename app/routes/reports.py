from fastapi import APIRouter , HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/reports/")
async def list_reports():
    report_dir = "generated_reports/"
    
    # Check if the directory exists
    if not os.path.exists(report_dir):
        return {"message": "No reports available."}

    # List all PDF files in the directory
    reports = [f for f in os.listdir(report_dir) if f.endswith('.pdf')]
    return {"available_reports": reports}
@router.get("/download_report/{report_id}")
async def download_report(report_id: str):
    report_path = f"generated_reports/{report_id}"
    
    # Check if the report exists
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not found.")
    
    return FileResponse(report_path, media_type='application/pdf', filename=report_id)
