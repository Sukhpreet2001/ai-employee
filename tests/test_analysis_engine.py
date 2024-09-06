import unittest
import pandas as pd
from app.services.analysis_engine import AnalysisEngine

class TestAnalysisEngine(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10, 20, 30, 40, 50],
            'target': [0, 1, 0, 1, 0]
        })
        self.analysis_engine = AnalysisEngine(self.data)

    def test_descriptive_statistics(self):
        result = self.analysis_engine.descriptive_statistics()
        self.assertIn('mean', result)
        self.assertIn('median', result)
        self.assertIn('std_dev', result)
        self.assertIn('min', result)
        self.assertIn('max', result)
        self.assertIn('count', result)

    def test_linear_regression(self):
        result = self.analysis_engine.linear_regression(target_column='target')
        self.assertIn('coefficients', result)
        self.assertIn('intercept', result)
        self.assertIn('r_squared', result)

    def test_decision_tree_regression(self):
        result = self.analysis_engine.decision_tree_regression(target_column='target', feature_columns=['feature1', 'feature2'])
        self.assertIn('feature_importance', result)
        self.assertIn('predictions', result)
        self.assertIn('r_squared', result)

    def test_invalid_data(self):
        empty_df = pd.DataFrame()
        analysis_engine = AnalysisEngine(empty_df)
        with self.assertRaises(ValueError):
            analysis_engine.descriptive_statistics()

if __name__ == '__main__':
    unittest.main()

