# app/routes/analysis.py

from fastapi import APIRouter, UploadFile, File
from app.utils.file_handler import read_file
from app.services.data_processing import clean_data, preprocess_data

router = APIRouter()

@router.post("/process/")
async def process_file(file: UploadFile = File(...)):
    # Read the file
    df = read_file(file.file)

    # Clean the data
    df_cleaned = clean_data(df)

    # Preprocess the data
    df_preprocessed = preprocess_data(df_cleaned)

    return {"status": "success", "columns": df_preprocessed.columns.tolist()}

