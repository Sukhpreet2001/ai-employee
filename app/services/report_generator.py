import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import os

class ReportGenerator:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def generate_visualizations(self):
        numeric_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
        categorical_columns = self.df.select_dtypes(include=['object']).columns
        figures = {}

        # Generate bar charts for numeric columns
        for col in numeric_columns:
            fig = px.bar(self.df, x=self.df.index, y=col, title=f'{col} Distribution')
            fig_path = f"generated_reports/{col}_visualization.png"
            fig.write_image(fig_path)
            figures[col] = fig_path

        # Generate pie charts for categorical columns
        for col in categorical_columns:
            fig = px.pie(self.df, names=col, title=f'{col} Distribution')
            fig_path = f"generated_reports/{col}_visualization.png"
            fig.write_image(fig_path)
            figures[col] = fig_path

        return figures

    def generate_pdf_with_visualizations(self, output_path: str, visualizations: dict):
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        # Add title
        c.setFont("Helvetica", 24)
        c.drawString(200, height - 50, "Report with Visualizations")

        # Add each visualization
        y_position = height - 100
        for col, img_path in visualizations.items():
            img = Image.open(img_path)
            c.drawImage(img_path, 100, y_position - img.height, width=400, height=300)
            y_position -= img.height + 50
            c.showPage()

        c.save()

    def create_report(self, output_pdf_path: str):
        visualizations = self.generate_visualizations()
        self.generate_pdf_with_visualizations(output_pdf_path, visualizations)

        # Clean up image files
        for img_path in visualizations.values():
            if os.path.exists(img_path):
                os.remove(img_path)
