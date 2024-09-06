import argparse
from rich.console import Console
from rich.table import Table
from app.services.analysis_engine import AnalysisEngine
from app.services.data_processing import clean_data, preprocess_data
from app.services.report_generator import ReportGenerator
from app.utils.file_handler import read_file
import os
import io
import pandas as pd

console = Console()

def upload_file(file_path: str):
    # Ensure the file path is valid
    if not os.path.exists(file_path):
        console.print(f"[bold red]Error:[/bold red] File {file_path} does not exist.")
        return None

    file_name = os.path.basename(file_path)
    if not file_name:
        console.print("[bold red]Error:[/bold red] File name not provided or cannot be determined.")
        return None

    # Log file upload
    console.print(f"Uploading file: {file_path}")

    # Read the file into a dataframe
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        console.print(f"[bold red]Error reading file:[/bold red] {e}")
        return None

def run_analysis(df):
    # Example to run descriptive statistics
    analysis_engine = AnalysisEngine(df)
    result = analysis_engine.descriptive_statistics()
    console.print("Descriptive Statistics:", style="bold blue")
    console.print(result)

def generate_report(df, output_file: str):
    report_generator = ReportGenerator(df)
    report_generator.create_report(output_file)
    console.print(f"Report generated: {output_file}", style="bold green")

def main():
    parser = argparse.ArgumentParser(description="AI Employee CLI for data analysis and reporting.")
    parser.add_argument("command", choices=["upload", "analyze", "report"], help="The action to perform.")
    parser.add_argument("file", help="Path to the file for upload or analysis.")
    parser.add_argument("--output", help="Path for saving the report.")

    args = parser.parse_args()

    if args.command == "upload":
        df = upload_file(args.file)
        if df is not None:
            console.print("Data uploaded successfully.")
    elif args.command == "analyze":
        df = upload_file(args.file)
        if df is not None:
            run_analysis(df)
    elif args.command == "report":
        df = upload_file(args.file)
        if df is not None and args.output:
            generate_report(df, args.output)
        else:
            console.print("Please specify an output file for the report.", style="bold red")

if __name__ == "__main__":
    main()
