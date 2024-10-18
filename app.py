import os
import pandas as pd

def process_csv_file(file_path):
    try:
        # 读取 CSV 文件
        data = pd.read_csv(file_path, delimiter=';')
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def convert_to_sankey_format(data):
    # 用来存储最终的 Source, Target, Value 结果
    sankey_data = []

    # 1. 对每个用户的访问记录按 Visitor ID 分组
    grouped = data.groupby('Visitor ID')

    # 2. 对每个用户的事件顺序（Event position）排序，生成 Source -> Target
    for visitor_id, group in grouped:
        # 按 Event position 对单个用户的记录排序
        group = group.sort_values('Event position')

        # 获取页面列表
        pages = group['Page - with levels'].tolist()

        # 3. 生成 Source -> Target
        for i in range(len(pages) - 1):
            source = pages[i]
            target = pages[i + 1]
            # 增加到 sankey_data 中
            sankey_data.append((source, target))

    # 4. 统计每个 Source -> Target 对的次数
    sankey_df = pd.DataFrame(sankey_data, columns=['Source', 'Target'])
    sankey_df['Value'] = 1
    sankey_df = sankey_df.groupby(['Source', 'Target']).sum().reset_index()

    return sankey_df

# 设置 CSV 文件路径
file_path = "data\myexport_20241017150020.csv"  # 将 "your_file.csv" 替换为你实际的文件名

# 加载单个 CSV 文件
data = process_csv_file(file_path)

# 检查是否成功加载数据
if data is not None:
    # 转换为适合桑基图的数据格式
    sankey_df = convert_to_sankey_format(data)
    
    output_excel_file = 'sankey_diagram_data.xlsx'
    sankey_df.to_excel(output_excel_file, index=False)

    print(f"Sankey data saved to {output_excel_file}")
    
    # 打印处理后的桑基图数据
    print(f"Processed data for Sankey diagram:\n{sankey_df.head()}")

