import pandas as pd
import requests
import os

# Load the CSV file
file_path = 'Hybrid RAG with Azure Data Explorer/download/USA-20220101-AviationData.csv'  # Replace with the path to your CSV file
df = pd.read_csv(file_path)

# Ensure the 'docs' directory exists
os.makedirs('docs', exist_ok=True)

# Function to download a PDF for a given NtsbNo
def download_report(mkey):
    url = f"https://data.ntsb.gov/carol-repgen/api/Aviation/ReportMain/GenerateNewestReport/{mkey}/pdf"
    response = requests.get(url)
    
    if response.status_code == 200:
        file_name = os.path.join('Hybrid RAG with Azure Data Explorer/download/docs', f"{mkey}.pdf")
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_name}")
    else:
        print(f"Failed to download report for NtsbNo: {mkey}")

# Iterate over the NtsbNo column and download each report
for mkey in df['Mkey']:
    download_report(mkey)
