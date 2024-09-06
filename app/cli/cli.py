import argparse
from rich.console import Console
from rich.table import Table
from app.services.analysis_engine import AnalysisEngine
from app.services.data_processing import clean_data, preprocess_data
from app.services.report_generator import ReportGenerator
from app.utils.file_handler import read_file
from app.nlp.nlp_utils import process_user_query, interpret_query
import os
import pandas as pd

console = Console()

def upload_file(file_path: str):
    if not os.path.exists(file_path):
        console.print(f"[bold red]Error:[/bold red] File {file_path} does not exist.")
        return None

    file_name = os.path.basename(file_path)
    if not file_name:
        console.print("[bold red]Error:[/bold red] File name not provided or cannot be determined.")
        return None

    console.print(f"Uploading file: {file_path}")

    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        console.print(f"[bold red]Error reading file:[/bold red] {e}")
        return None

def run_analysis(df, analysis_type):
    analysis_engine = AnalysisEngine(df)
    
    if analysis_type == "descriptive":
        result = analysis_engine.descriptive_statistics()
        console.print("Descriptive Statistics:", style="bold blue")
        console.print(result)
    
    elif analysis_type == "linear_regression":
        x_column = input("Enter the name of the x column: ")
        y_column = input("Enter the name of the y column: ")
        result = analysis_engine.linear_regression(x_column, y_column)
        console.print("Linear Regression Results:", style="bold blue")
        console.print(result)
    
    elif analysis_type == "decision_tree":
        target_column = input("Enter the target column name: ")
        feature_columns = input("Enter the feature columns separated by commas: ").split(",")
        result = analysis_engine.decision_tree_regression(target_column, feature_columns)
        console.print("Decision Tree Regression Results:", style="bold blue")
        console.print(result)
    
    else:
        console.print(f"[bold red]Error:[/bold red] Unknown analysis type {analysis_type}")

def process_query(query):
    tokens = process_user_query(query)
    action = interpret_query(tokens)
    
    if action == "upload_file":
        file_path = input("Enter the file path to upload: ")
        df = upload_file(file_path)
        if df is not None:
            console.print("Data uploaded successfully.")
    elif action == "analysis":
        file_path = input("Enter the file path for analysis: ")
        df = upload_file(file_path)
        if df is not None:
            analysis_type = input("Enter the type of analysis (descriptive, linear_regression, decision_tree): ")
            run_analysis(df, analysis_type)
    elif action == "generate_report":
        file_path = input("Enter the file path for report generation: ")
        df = upload_file(file_path)
        if df is not None:
            report_path = input("Enter the path to save the report: ")
            report_generator = ReportGenerator(df)
            report_generator.create_report(report_path)
            console.print(f"Report generated and saved at {report_path}")
    else:
        console.print("[bold red]Error:[/bold red] Unknown query action.")

def main():
    parser = argparse.ArgumentParser(description="AI Employee CLI for data analysis and reporting.")
    parser.add_argument("command", choices=["upload", "analyze", "report"], help="The action to perform.")
    parser.add_argument("file", help="Path to the file for upload or analysis.")
    parser.add_argument("--type", choices=["descriptive", "linear_regression", "decision_tree"], help="Type of analysis to perform.")

    args = parser.parse_args()

    if args.command == "upload":
        df = upload_file(args.file)
        if df is not None:
            console.print("Data uploaded successfully.")
    elif args.command == "analyze":
        if args.type:
            df = upload_file(args.file)
            if df is not None:
                run_analysis(df, args.type)
        else:
            console.print("[bold red]Error:[/bold red] Analysis type must be specified with --type.")
    elif args.command == "report":
        df = upload_file(args.file)
        if df is not None:
            report_path = input("Enter the path to save the report: ")
            report_generator = ReportGenerator(df)
            report_generator.create_report(report_path)
            console.print(f"Report generated and saved at {report_path}")

if __name__ == "__main__":
    main()
