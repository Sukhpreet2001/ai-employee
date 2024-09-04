# app/services/analysis_engine.py

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from scipy import stats

class AnalysisEngine:
    def __init__(self, data):
        """
        Initialize the AnalysisEngine with data.
        :param data: Pandas DataFrame containing the data to be analyzed.
        """
        self.data = data

    def descriptive_statistics(self):
        """
        Perform descriptive statistics on the data.
        Returns a dictionary with mean, median, mode, variance, and standard deviation.
        """
        stats_dict = {
            "mean": self.data.mean().to_dict(),
            "median": self.data.median().to_dict(),
            "mode": self.data.mode().iloc[0].to_dict(),  # Taking the first mode in case of multiple modes
            "variance": self.data.var().to_dict(),
            "standard_deviation": self.data.std().to_dict(),
        }
        return stats_dict

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

    def k_means_clustering(self, num_clusters):
        """
        Perform K-Means clustering on the data.
        :param num_clusters: Number of clusters to form.
        :return: Dictionary with cluster labels and cluster centers.
        """
        kmeans = KMeans(n_clusters=num_clusters)
        kmeans.fit(self.data)

        clustering_results = {
            "cluster_labels": kmeans.labels_.tolist(),
            "cluster_centers": kmeans.cluster_centers_.tolist(),
        }
        return clustering_results


