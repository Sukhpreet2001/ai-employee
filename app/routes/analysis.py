from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.utils.file_handler import read_file
from app.services.data_processing import clean_data, preprocess_data
from app.services.analysis_engine import AnalysisEngine
import io
from pydantic import BaseModel
import pandas as pd

router = APIRouter()

# Existing data processing endpoint
@router.post("/process/")
async def process_file(file: UploadFile = File(...)):
    # Read the file contents
    contents = await file.read()
    file_like_object = io.BytesIO(contents)

    # Read the file using the read_file function, passing the filename
    df = read_file(file_like_object, file.filename)

    # Clean the data
    df_cleaned = clean_data(df)

    # Preprocess the data
    df_preprocessed = preprocess_data(df_cleaned)

    return {"status": "success", "columns": df_preprocessed.columns.tolist()}

# Analysis Engine Endpoints

# Request models
class LinearRegressionRequest(BaseModel):
    target_column: str

class KMeansRequest(BaseModel):
    num_clusters: int

@router.post("/descriptive_statistics/")
async def get_descriptive_statistics(file: UploadFile = File(...)):
    contents = await file.read()
    file_like_object = io.BytesIO(contents)
    df = read_file(file_like_object, file.filename)
    
    analysis_engine = AnalysisEngine(df)
    result = analysis_engine.descriptive_statistics()
    return {"descriptive_statistics": result}

@router.post("/linear_regression/")
async def perform_linear_regression(file: UploadFile = File(...), request: LinearRegressionRequest = Depends()):
    contents = await file.read()
    file_like_object = io.BytesIO(contents)
    df = read_file(file_like_object, file.filename)
    
    if request.target_column not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid target column")

    analysis_engine = AnalysisEngine(df)
    result = analysis_engine.linear_regression(request.target_column)
    return {"linear_regression": result}

@router.post("/k_means_clustering/")
async def perform_k_means_clustering(file: UploadFile = File(...), request: KMeansRequest = Depends()):
    contents = await file.read()
    file_like_object = io.BytesIO(contents)
    df = read_file(file_like_object, file.filename)
    
    if request.num_clusters < 1:
        raise HTTPException(status_code=400, detail="Number of clusters must be at least 1")

    analysis_engine = AnalysisEngine(df)
    result = analysis_engine.k_means_clustering(request.num_clusters)
    return {"k_means_clustering": result}
