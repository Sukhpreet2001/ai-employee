# tests/test_data_processing.py

import pandas as pd
from app.services.data_processing import clean_data, preprocess_data

def test_clean_data():
    data = {'col1': [1, 2, 2, None], 'col2': [3, 4, 4, None]}
    df = pd.DataFrame(data)
    df_cleaned = clean_data(df)
    
    assert df_cleaned.shape == (2, 2)

def test_preprocess_data():
    data = {'col1': [1, 2, 3], 'col2': ['A', 'B', 'A']}
    df = pd.DataFrame(data)
    df_preprocessed = preprocess_data(df)
    
    assert 'col2_A' in df_preprocessed.columns
    assert 'col2_B' in df_preprocessed.columns

