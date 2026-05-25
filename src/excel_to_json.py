import os
import pandas as pd
from data_loader import BASE_DIR

def extract_excel_sheets():
    """
    Reads the main Excel file AITacDong.xlsx and extracts all sheets to CSV files
    in the data/processed directory, resolving paths dynamically.
    """
    excel_file_path = os.path.join(BASE_DIR, 'data', 'raw', 'G7_AI_Impact_Data.xlsx')
    output_dir = os.path.join(BASE_DIR, 'data', 'processed')
    
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(excel_file_path):
        print(f"Error: Raw Excel file not found at {excel_file_path}")
        return
        
    print(f"Reading all sheets from Excel: '{excel_file_path}'")
    xls = pd.ExcelFile(excel_file_path)
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name)
        
        # Save sheet to CSV
        csv_name = 'Data_Permuted.csv' if sheet_name == 'DataHoanVI' else f'{sheet_name}.csv'
        csv_file_path = os.path.join(output_dir, csv_name)
        df.to_csv(csv_file_path, index=False)
        print(f"Successfully converted sheet '{sheet_name}' to CSV: '{csv_file_path}'")
        
        # Optionally, save as JSON too if sheet_name is criteria details
        if sheet_name == 'Criteria':
            json_file_path = os.path.join(BASE_DIR, 'data', 'raw', 'G7_AI_Impact_Criteria.json')
            # Save orient records for Gemini ingestion if needed
            df.to_json(json_file_path, orient='records', indent=4)
            print(f"Exported sheet '{sheet_name}' to JSON for model ingestion: '{json_file_path}'")

if __name__ == '__main__':
    extract_excel_sheets()
