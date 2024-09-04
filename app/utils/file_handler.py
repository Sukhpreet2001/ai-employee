import pandas as pd
import io

def read_file(file: io.BytesIO, file_name: str = None) -> pd.DataFrame:
    """Read a file-like object and return a pandas DataFrame."""
    
    # If file_name is provided, use it; otherwise, fallback to a default or raise an error
    if file_name:
        if file_name.endswith('.csv'):
            return pd.read_csv(file)
        elif file_name.endswith('.json'):
            return pd.read_json(file)
        elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            return pd.read_excel(file)
        else:
            raise ValueError(f"Unsupported file format: {file_name}")
    else:
        raise ValueError("File name not provided or cannot be determined.")

