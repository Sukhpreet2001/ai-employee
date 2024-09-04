from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from app.utils.file_handler import read_file
from app.services.data_processing import clean_data, preprocess_data
from app.services.analysis_engine import AnalysisEngine
import io
from pydantic import BaseModel
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

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
    n_clusters: int
    feature_columns: str

@router.post("/descriptive_statistics/")
async def get_descriptive_statistics(file: UploadFile = File(...)):
    contents = await file.read()
    file_like_object = io.BytesIO(contents)
    df = read_file(file_like_object, file.filename)
    
    analysis_engine = AnalysisEngine(df)
    result = analysis_engine.descriptive_statistics()
    return {"descriptive_statistics": result}

@router.post("/linear_regression/")
async def linear_regression(
    file: UploadFile = File(...),
    x_column: str = Query(..., alias="x"),
    y_column: str = Query(..., alias="y")
):
    # Read the CSV file
    df = pd.read_csv(file.file)

    if x_column not in df.columns or y_column not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid column names.")

    # Encode categorical data if necessary
    if df[x_column].dtype == 'object':
        le = LabelEncoder()
        df[x_column] = le.fit_transform(df[x_column])
    
    if df[y_column].dtype == 'object':
        le = LabelEncoder()
        df[y_column] = le.fit_transform(df[y_column])

    # Extracting the x and y values
    X = df[[x_column]].values
    y = df[y_column].values

    # Perform linear regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Return the slope and intercept
    return {"slope": model.coef_[0], "intercept": model.intercept_}

@router.post("/k_means_clustering/")
async def perform_k_means_clustering(
    file: UploadFile = File(...),
    n_clusters: int = Query(..., alias="n_clusters"),
    feature_columns: str = Query(..., alias="feature_columns")
):
    contents = await file.read()
    file_like_object = io.BytesIO(contents)
    df = read_file(file_like_object, file.filename)

    if n_clusters < 1:
        raise HTTPException(status_code=400, detail="Number of clusters must be at least 1")

    feature_columns = feature_columns.split(",")
    
    # Assuming AnalysisEngine is set up to handle k-means clustering
    analysis_engine = AnalysisEngine(df)
    result = analysis_engine.k_means_clustering(n_clusters, feature_columns)
    return {"k_means_clustering": result}