import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional

def read_excel_with_merged_cells(file_path: str, sheet_name: str = 0) -> pd.DataFrame:
    """
    读取包含合并单元格的Excel表格，提取多层表头结构并整理数据
    
    参数:
        file_path: Excel文件路径
        sheet_name: 工作表名称或索引
    
    返回:
        规范化的DataFrame，包含多层列索引
    """
    # 读取Excel文件，第一次读取获取顶层表头
    df_top_header = pd.read_excel(file_path, sheet_name=sheet_name, header=None, nrows=1)
    
    # 第二次读取获取底层表头
    df_bottom_header = pd.read_excel(file_path, sheet_name=sheet_name, header=None, nrows=1, skiprows=1)
    
    # 第三次读取获取实际数据
    df_data = pd.read_excel(file_path, sheet_name=sheet_name, header=None, skiprows=2)
    
    # 处理合并单元格的顶层表头
    top_header = df_top_header.iloc[0].tolist()
    filled_top_header = fill_merged_cells(top_header)
    
    # 处理合并单元格的底层表头
    bottom_header = df_bottom_header.iloc[0].tolist()
    filled_bottom_header = fill_merged_cells(bottom_header)
    
    # 设置多层列索引
    df_data.columns = pd.MultiIndex.from_arrays([filled_top_header, filled_bottom_header])
    
    # 假设第一列是行业类型，设置为索引
    if not df_data.empty:
        df_data.set_index(df_data.columns[0], inplace=True)
        df_data.index.name = '行业类型'
    
    return df_data

def fill_merged_cells(header_list: List[Any]) -> List[Any]:
    """填充合并单元格导致的None值"""
    filled = []
    last_value = None
    for value in header_list:
        if pd.notna(value):
            last_value = value
        filled.append(last_value)
    return filled

def analyze_header_structure(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    分析表头结构，确定每年包含的列数
    
    参数:
        df: 带有多层列索引的DataFrame
    
    返回:
        年份与对应列名列表的映射
    """
    if df.columns.nlevels < 2:
        raise ValueError("DataFrame需要至少两层列索引")
    #TO FIX
    year_columns = {}
    for year, gender in df.columns:
        if year not in year_columns:
            year_columns[year] = []
        year_columns[year].append(gender)
    
    return year_columns

def restructure_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    将多层列索引的数据重构为长格式，便于分析
    
    参数:
        df: 带有多层列索引的原始DataFrame
    
    返回:
        重构后的长格式DataFrame
    """
    #TO FIX
    # 重置索引，将行业类型转为列
    df_melted = df.reset_index()
    
    # 将DataFrame从宽格式转换为长格式
    df_long = pd.melt(
        df_melted, 
        id_vars=['行业类型'],
        var_name=['年份', '性别'],
        value_name='数据值'
    )
    
    return df_long

def process_excel_file(file_path: str, sheet_name: str = 0) -> pd.DataFrame:
    """
    处理Excel文件的主函数，整合数据读取和处理流程
    
    参数:
        file_path: Excel文件路径
        sheet_name: 工作表名称或索引
    
    返回:
        处理完成的长格式DataFrame
    """
    # 读取数据
    df = read_excel_with_merged_cells(file_path, sheet_name)
    
    # 分析表头结构
    header_structure = analyze_header_structure(df)
    print(f"检测到的年份结构: {header_structure}")
    
    # 重构数据
    df_processed = restructure_data(df)
    
    return df_processed

# if __name__ == "__main__":
#     # 使用示例
#     file_path = "your_excel_file.xlsx"  # 替换为实际文件路径
#     try:
#         processed_data = process_excel_file(file_path)
#         print("数据处理完成，结构示例:")
#         print(processed_data.head())
        
#         # 保存处理后的数据
#         processed_data.to_csv("processed_data.csv", index=False)
#         print("数据已保存至 processed_data.csv")
#     except Exception as e:
#         print(f"处理过程中发生错误: {e}")    