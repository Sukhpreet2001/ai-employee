from fastapi import APIRouter , HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/get_report/{report_name}")
def get_report(report_name: str):
    file_path = f"generated_reports/{report_name}"
    
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/pdf', filename=report_name)
    else:
        raise HTTPException(status_code=404, detail="Report not found")
