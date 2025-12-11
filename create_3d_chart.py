import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 讀取已有精簡分類的報修資料
df = pd.read_csv(r'c:\Users\f2302\Desktop\報修分析\報修明細數據_精簡分類.csv')

# 統計各精簡類別數量
category_counts = df['精簡類別'].value_counts().reset_index()
category_counts.columns = ['類別', '數量']

# Google 品牌色系
google_colors = [
    '#4285F4',  # 藍
    '#EA4335',  # 紅
    '#FBBC05',  # 黃
    '#34A853',  # 綠
    '#FF6D01',  # 橙
    '#46BDC6',  # 青
    '#7B1FA2',  # 紫
    '#E91E63',  # 粉
]

categories = category_counts['類別'].tolist()
values = category_counts['數量'].tolist()

# 建立 3D 柱狀圖 (使用 Mesh3d 繪製立體柱)
fig = go.Figure()

bar_width = 0.6
bar_depth = 0.6

for i, (cat, val) in enumerate(zip(categories, values)):
    x0, x1 = i - bar_width/2, i + bar_width/2
    y0, y1 = -bar_depth/2, bar_depth/2
    z0, z1 = 0, val
    
    # 定義立方體的 8 個頂點
    vertices_x = [x0, x1, x1, x0, x0, x1, x1, x0]
    vertices_y = [y0, y0, y1, y1, y0, y0, y1, y1]
    vertices_z = [z0, z0, z0, z0, z1, z1, z1, z1]
    
    # 定義立方體的 12 個三角面
    i_faces = [0, 0, 4, 4, 0, 0, 1, 1, 0, 0, 4, 4]
    j_faces = [1, 2, 5, 6, 1, 4, 2, 5, 3, 4, 7, 5]
    k_faces = [2, 3, 6, 7, 4, 5, 5, 6, 4, 7, 3, 7]
    
    fig.add_trace(go.Mesh3d(
        x=vertices_x,
        y=vertices_y,
        z=vertices_z,
        i=i_faces,
        j=j_faces,
        k=k_faces,
        color=google_colors[i % len(google_colors)],
        opacity=0.9,
        name=f'{cat} ({val}件)',
        showlegend=True,
        flatshading=True,
        lighting=dict(ambient=0.6, diffuse=0.8, specular=0.3),
        hoverinfo='name'
    ))

# 更新佈局
fig.update_layout(
    title=dict(
        text='<b>📊 報修案件精簡分類統計 (3D)</b>',
        font=dict(size=26, family='Microsoft JhengHei', color='#202124'),
        x=0.5
    ),
    scene=dict(
        xaxis=dict(
            title='類別',
            tickmode='array',
            tickvals=list(range(len(categories))),
            ticktext=categories,
            tickfont=dict(size=11, family='Microsoft JhengHei'),
            gridcolor='#E0E0E0'
        ),
        yaxis=dict(
            title='',
            showticklabels=False,
            showgrid=False
        ),
        zaxis=dict(
            title='案件數量',
            tickfont=dict(size=12),
            gridcolor='#E0E0E0'
        ),
        camera=dict(
            eye=dict(x=1.8, y=1.8, z=0.8)
        ),
        bgcolor='#FAFAFA',
        aspectmode='manual',
        aspectratio=dict(x=2, y=0.5, z=1)
    ),
    paper_bgcolor='white',
    margin=dict(l=20, r=20, t=80, b=20),
    legend=dict(
        title=dict(text='<b>精簡類別</b>', font=dict(size=14)),
        font=dict(size=12, family='Microsoft JhengHei'),
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='#E0E0E0',
        borderwidth=1
    )
)

# 儲存為 HTML
output_path = r'c:\Users\f2302\Desktop\報修分析\精簡分類3D統計圖.html'
fig.write_html(output_path)
print(f"✅ 3D 圖表已儲存至: {output_path}")

# 顯示統計
print("\n=== 精簡類別統計 ===")
for cat, val in zip(categories, values):
    print(f"  {cat}: {val} 件")
print(f"\n總計: {sum(values)} 件")
