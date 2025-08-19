import pandas as pd
import json

# feature_rows = {
#     "Age group": 17,
#     "Industry": 19,
#     "Institutional sector": 5,
#     "Type of legal organisation": 3,
#     "Employment size": 4,
#     "Job duration": 4
# }

# with open("feature_rows.json", "w", encoding="utf-8") as f:
#     json.dump(feature_rows, f, ensure_ascii=False, indent=4)

def read_feature_rows(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def fill_gender(genders):
    return pd.Series(genders).fillna(method='ffill').tolist()

def extract_feature_tables(excel_path, feature_rows_path, sheet_name=0):
    feature_rows = read_feature_rows(feature_rows_path)
    df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
    genders = df.iloc[6, 2:].tolist()
    genders = fill_gender(genders)
    years = df.iloc[7, 2:].tolist()
    data_start_col = 2
    group_width = 5
    feature_start_row = 9
    feature_tables = {}

    for feature, row_count in feature_rows.items():
        feature_data = df.iloc[feature_start_row:feature_start_row+row_count, :]
        class_names = feature_data.iloc[:, 0].values.tolist()
        values = feature_data.iloc[:, data_start_col:].values
        records = []
        for i_class in range(row_count):
            class_name = class_names[i_class]
            noj = values[i_class, :15]
            mincome = values[i_class, 15:30]
            for idx in range(15):
                year = years[idx]
                gender = genders[idx]
                records.append({
                    'feature': class_name,
                    'year': year,
                    'gender': gender,
                    'number_of_jobs': noj[idx],
                    'median_income': mincome[idx]
                })
        feature_tables[feature] = pd.DataFrame(records)
        feature_start_row += row_count

    return feature_tables

# 用法示例
# To modify raw data path
# tables = extract_feature_tables("test_data/Table1_test.xlsx", "feature_rows.json", "Table 1.1")
# for feature, df in tables.items():
#     filename = f"{feature}_gender.csv"
#     df.to_csv(f"test_result/{filename}", index=False)
#     print(f"{feature} 已保存为 {filename}")