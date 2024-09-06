import unittest
import pandas as pd
import os
from app.services.report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10, 20, 30, 40, 50]
        })
        self.output_file = 'test_report.pdf'  # Ensure the file extension is correct
        self.report_generator = ReportGenerator(self.data)

    def test_report_generation(self):
        self.report_generator.create_report(self.output_file)
        self.assertTrue(os.path.exists(self.output_file), "Report file does not exist.")

        # Additional validation can be added here if needed

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

if __name__ == '__main__':
    unittest.main()

