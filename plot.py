import plotly.graph_objects as go
from app import sankey_df  # 从 app.py 导入 sankey_df

def generate_sankey_diagram(sankey_df, output_file='sankey_diagram.png'):
    # 获取唯一的节点列表
    all_nodes = list(set(sankey_df['Source']).union(set(sankey_df['Target'])))

    # 创建节点到索引的映射
    node_mapping = {node: i for i, node in enumerate(all_nodes)}

    # 将 Source 和 Target 转换为对应的索引值
    sankey_df['source_id'] = sankey_df['Source'].map(node_mapping)
    sankey_df['target_id'] = sankey_df['Target'].map(node_mapping)

    # 创建桑基图
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes
        ),
        link=dict(
            source=sankey_df['source_id'],
            target=sankey_df['target_id'],
            value=sankey_df['Value']
        )
    ))

    # 将图表保存为 PNG 图片
    fig.write_image(output_file)
    print(f"Sankey diagram saved to {output_file}")

# 保存桑基图为 PNG 文件
generate_sankey_diagram(sankey_df, 'sankey_diagram.png')
