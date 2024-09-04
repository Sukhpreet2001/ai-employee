# tests/test_analysis_engine.py

import unittest
import pandas as pd
from app.services.analysis_engine import AnalysisEngine

class TestAnalysisEngine(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10, 20, 30, 40, 50],
            'target': [5, 10, 15, 20, 25]
        })
        self.analysis_engine = AnalysisEngine(self.data)

    def test_descriptive_statistics(self):
        result = self.analysis_engine.descriptive_statistics()
        self.assertIn('mean', result)
        self.assertIn('median', result)
        self.assertIn('mode', result)
        self.assertIn('variance', result)
        self.assertIn('standard_deviation', result)

    def test_linear_regression(self):
        result = self.analysis_engine.linear_regression(target_column='target')
        self.assertIn('coefficients', result)
        self.assertIn('intercept', result)
        self.assertIn('r_squared', result)

    def test_k_means_clustering(self):
        result = self.analysis_engine.k_means_clustering(num_clusters=2)
        self.assertIn('cluster_labels', result)
        self.assertIn('cluster_centers', result)

if __name__ == '__main__':
    unittest.main()
