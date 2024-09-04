# app/services/analysis_engine.py

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from scipy import stats
from fastapi import HTTPException
class AnalysisEngine:
    def __init__(self, data):
        """
        Initialize the AnalysisEngine with data.
        :param data: Pandas DataFrame containing the data to be analyzed.
        """
        self.data = data

    def descriptive_statistics(self):
      """
      Calculate and return descriptive statistics for numeric columns in the data.
      """
      # Select only numeric columns
      numeric_data = self.data.select_dtypes(include='number')
    
      if numeric_data.empty:
        raise ValueError("No numeric data available for statistical analysis.")
    
      return {
        "mean": numeric_data.mean().to_dict(),
        "median": numeric_data.median().to_dict(),
        "std_dev": numeric_data.std().to_dict(),
        "min": numeric_data.min().to_dict(),
        "max": numeric_data.max().to_dict(),
        "count": numeric_data.count().to_dict(),
      }


    def linear_regression(self, target_column):
        """
        Perform linear regression on the data.
        :param target_column: The column to be predicted (dependent variable).
        :return: Dictionary with coefficients, intercept, and R-squared value.
        """
        X = self.data.drop(columns=[target_column])
        y = self.data[target_column]

        model = LinearRegression()
        model.fit(X, y)

        regression_results = {
            "coefficients": dict(zip(X.columns, model.coef_)),
            "intercept": model.intercept_,
            "r_squared": model.score(X, y),
        }
        return regression_results

    def k_means_clustering(self, n_clusters, feature_columns):
    # Select only numeric columns
        df_features = self.data[feature_columns].select_dtypes(include=[float, int])
        
        # Check if all selected columns are numeric
        if df_features.empty or df_features.shape[1] != len(feature_columns):
            raise HTTPException(
                status_code=400, 
                detail="One or more selected feature columns are non-numeric."
            )
        
        # Perform K-Means clustering
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(df_features)
        self.data['Cluster'] = kmeans.labels_
        
        # Group by clusters and calculate the mean for numeric columns
        grouped_data = self.data.groupby('Cluster').mean().to_dict()
        
        # Include non-numeric columns in the results
        non_numeric_columns = self.data[feature_columns].select_dtypes(exclude=[float, int])
        if not non_numeric_columns.empty:
            non_numeric_modes = self.data.groupby('Cluster')[non_numeric_columns.columns].agg(lambda x: x.mode()[0])
            grouped_data.update(non_numeric_modes.to_dict())
        
        return grouped_data