import argparse
from rich.console import Console
import requests
import os
from app.nlp.nlp_utils import process_user_query, interpret_query

console = Console()
API_URL = "http://127.0.0.1:8000"  # Ensure this is the correct URL for your FastAPI app

def upload_file(file_path: str):
    if not os.path.exists(file_path):
        console.print(f"[bold red]Error:[/bold red] File {file_path} does not exist.")
        return None
    console.print(f"Uploading file: {file_path}")
    return file_path

def run_analysis(file_path, analysis_type, x_column=None, y_column=None, target_column=None, feature_columns=None):
    with open(file_path, 'rb') as file:
        files = {'file': file}
        if analysis_type == "linear_regression":
            response = requests.post(
                f"{API_URL}/analysis/linear_regression/",
                files=files,
                params={'x': x_column, 'y': y_column}
            )
        elif analysis_type == "decision_tree":
            response = requests.post(
                f"{API_URL}/analysis/decision_tree_regression/",
                files=files,
                params={'target_column': target_column, 'feature_columns': feature_columns}
            )
        elif analysis_type == "descriptive":
            response = requests.post(
                f"{API_URL}/analysis/descriptive_statistics/",
                files=files
            )
        if response.status_code == 200:
            console.print(f"Analysis result: {response.json()}")
        else:
            console.print(f"[bold red]Error:[/bold red] {response.text}")

def generate_report(file_path):
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(f"{API_URL}/analysis/generate_report/", files=files)
        if response.status_code == 200:
            report_id = response.json()['report_id']
            console.print(f"Report generated with ID: {report_id}")
        else:
            console.print(f"[bold red]Error:[/bold red] {response.text}")

def list_reports():
    response = requests.get(f"{API_URL}/reports/reports/")
    if response.status_code == 200:
        reports = response.json()['available_reports']
        console.print(f"Available reports: {reports}")
    else:
        console.print(f"[bold red]Error:[/bold red] {response.text}")

def download_report(report_id):
    response = requests.get(f"{API_URL}/download_report/{report_id}")
    if response.status_code == 200:
        with open(report_id, 'wb') as file:
            file.write(response.content)
        console.print(f"Report downloaded as {report_id}")
    else:
        console.print(f"[bold red]Error:[/bold red] {response.text}")

def process_command(query):
    tokens = process_user_query(query)
    action = interpret_query(tokens)
    return action

def main():
    parser = argparse.ArgumentParser(description="AI Employee CLI for data analysis and reporting.")
    parser.add_argument("command", help="The action to perform.")
    parser.add_argument("file", help="Path to the file for upload or analysis.", nargs='?')
    parser.add_argument("--type", choices=["descriptive", "linear_regression", "decision_tree"], help="Type of analysis to perform.")
    parser.add_argument("--x_column", help="Column name for x in linear regression.")
    parser.add_argument("--y_column", help="Column name for y in linear regression.")
    parser.add_argument("--target_column", help="Target column for decision tree regression.")
    parser.add_argument("--feature_columns", help="Comma-separated feature columns for decision tree regression.")
    parser.add_argument("--report_id", help="ID of the report to download.")
    
    args = parser.parse_args()

    # Use NLP to process the command if `command` is a query
    if args.command == "query":
        action = process_command(input("Enter your query: "))
        if action == "analysis":
            # Extract additional arguments if needed
            run_analysis(args.file, args.type, x_column=args.x_column, y_column=args.y_column, target_column=args.target_column, feature_columns=args.feature_columns)
        elif action == "generate_report":
            generate_report(args.file)
        elif action == "upload_file":
            upload_file(args.file)
        elif action == "unknown":
            console.print("[bold red]Error:[/bold red] Unknown command.")
    else:
        if args.command == "upload":
            upload_file(args.file)
        elif args.command == "analyze":
            if args.type and args.file:
                run_analysis(args.file, args.type, x_column=args.x_column, y_column=args.y_column, target_column=args.target_column, feature_columns=args.feature_columns)
            else:
                console.print("[bold red]Error:[/bold red] Analysis type and file path must be specified.")
        elif args.command == "report":
            if args.file:
                generate_report(args.file)
            else:
                console.print("[bold red]Error:[/bold red] File path must be specified.")
        elif args.command == "list":
            list_reports()
        elif args.command == "download":
            if args.report_id:
                download_report(args.report_id)
            else:
                console.print("[bold red]Error:[/bold red] Report ID must be specified.")

if __name__ == "__main__":
    main()
