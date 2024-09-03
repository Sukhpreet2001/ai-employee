# app/core/data_processing.py

import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the data by handling missing values, duplicates, etc."""
    df = df.drop_duplicates()
    df = df.dropna()  # You might want to handle NaNs differently depending on the context
    # Add more cleaning steps as required
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the data (e.g., feature scaling, encoding)."""
    # Example: Scaling numerical features
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
    
    # Example: Encoding categorical features
    categorical_cols = df.select_dtypes(include=['object']).columns
    df = pd.get_dummies(df, columns=categorical_cols)
    
    return df
