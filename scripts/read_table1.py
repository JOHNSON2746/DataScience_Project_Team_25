import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
from code.reader.abs_excel_reader import extract_feature_tables

def main():
    file_path = 'abs_raw_data/Table 1 - Jobs and employment income by sex, age, business characteristics and geography, 2017-18 to 2021-22.xlsx'
    # To do: Modularize later
    feature_rows = "code/reader/feature_rows.json"
    table_name = "Table 1.1"
    tables = extract_feature_tables(file_path, feature_rows, table_name)
    for feature, df in tables.items():
        filename = f"{feature}_gender.csv"
        df.to_csv(f"data/transformed/{filename}", index=False)
        print(f"{feature} 已保存为 {filename}")

if __name__ == "__main__":
    main()
