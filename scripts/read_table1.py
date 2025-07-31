import argparse
from code.reader.abs_excel_reader import process_excel_file
import pandas as pd

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='处理包含合并单元格的Excel数据')
    parser.add_argument('input_file', help='Excel文件路径')
    parser.add_argument('-s', '--sheet', default=0, help='工作表名称或索引')
    parser.add_argument('-o', '--output', help='输出文件路径（CSV格式）')
    args = parser.parse_args()
    
    try:
        # # 初始化读取器并读取数据
        # reader = process_excel_file()
        # print(f"正在读取文件: {args.input_file}")
        # df = reader.read(
        #     file_path=args.input_file,
        #     sheet_name=args.sheet
        # )
        
        # # 转换数据格式
        # transformer = DataTransformer()
        # processed_df = transformer.to_long_format(df)
        
        # # 显示处理结果预览
        print("\n处理后的数据预览:")
        # print(processed_df.head())
        
        # # 保存结果（如果指定了输出路径）
        # if args.output:
        #     processed_df.to_csv(args.output, index=False)
        #     print(f"\n数据已保存至: {args.output}")
            
    except Exception as e:
        print(f"处理失败: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()