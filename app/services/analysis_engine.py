import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression ,LogisticRegression
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

    def logistic_regression(self, target_column, feature_columns):
        """
        Perform logistic regression on the data.
        :param target_column: The column to be predicted (dependent variable).
        :param feature_columns: List of feature columns to be used for prediction.
        :return: Dictionary with coefficients, intercept, accuracy, and predicted probabilities.
        """
        X = self.data[feature_columns]
        y = self.data[target_column]

        # Handle non-numeric data if present
        if X.select_dtypes(include='object').any().any():
            X = pd.get_dummies(X)
        
        # Encode target if it's categorical
        if y.dtype == 'object':
            y = pd.factorize(y)[0]

        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)

        logistic_regression_results = {
            "coefficients": dict(zip(feature_columns, model.coef_[0])),
            "intercept": model.intercept_[0],
            "accuracy": model.score(X, y),
            "predicted_probabilities": model.predict_proba(X).tolist(),
            "predictions": model.predict(X).tolist(),
        }

        return logistic_regression_results