import pandas as pd
import glob
import os
import sys

# 替换为你的Excel文件所在文件夹路径
# folder_path = r"C:\ExcelFiles\*.xlsx"
folder_path=r"d:\Users\Administrator\Desktop\美团财务对账\3月\*.xlsx"
file_paths = glob.glob(folder_path)

# 按文件名自然排序（区分数字顺序，如 1.xlsx < 2.xlsx < 10.xlsx)
file_paths.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]) 
                if os.path.basename(x).split('.')[0].isdigit() 
                else os.path.basename(x))

# 打印排序后的文件名，用于测试
# print(file_paths)
# sys.exit()

# 定义字典：key=工作表名，value=该sheet的所有数据列表
sheet_data_dict = {}
# 读取参数：强制文本格式，避免格式丢失
read_excel_kwargs = {"dtype": str, "engine": "openpyxl"}

# 遍历所有Excel文件
for file in file_paths:
    xl_file = pd.ExcelFile(file, engine="openpyxl")
    # 遍历当前文件的每个sheet
    for sheet_name in xl_file.sheet_names:
        df = pd.read_excel(file, sheet_name=sheet_name, **read_excel_kwargs)
        # 添加溯源列（可选，方便核对）
        df["来源文件"] = os.path.basename(file)
        
        # 按sheet名分类存储
        if sheet_name not in sheet_data_dict:
            sheet_data_dict[sheet_name] = []
        sheet_data_dict[sheet_name].append(df)

# 创建Excel写入器，用于分sheet保存
with pd.ExcelWriter("同名工作表分组合并.xlsx", engine="openpyxl") as writer:
    # 遍历每个sheet名，合并对应数据并写入
    for sheet_name, df_list in sheet_data_dict.items():
        combined_df = pd.concat(df_list, ignore_index=True)
        combined_df.to_excel(writer, sheet_name=sheet_name, index=False)

print("合并完成！每个同名工作表已单独汇总为新Excel的对应sheet")