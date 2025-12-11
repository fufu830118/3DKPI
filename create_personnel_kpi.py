import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 讀取已有精簡分類的報修資料
df = pd.read_csv(r'c:\Users\f2302\Desktop\報修分析\報修明細數據_精簡分類.csv')

# 處理人員名稱 (移除空白)
df['實際維修人員'] = df['實際維修人員'].str.strip()

# 統計每個人員在各類別的案件數
# Pivot table: Index=人員, Columns=類別, Values=案件數
pivot_df = df.pivot_table(index='實際維修人員', columns='精簡類別', aggfunc='size', fill_value=0)

# 準備繪圖資料
personnel = pivot_df.index.tolist()
categories = pivot_df.columns.tolist()
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

fig = go.Figure()

# 建立 3D 柱狀圖
# X軸: 人員 (i)
# Y軸: 類別 (j)
# Z軸: 數量

bar_width = 0.4  # 柱子寬度
bar_depth = 0.4  # 柱子深度 (Y軸方向)

for j, cat in enumerate(categories):
    # 為每個類別建立一組柱子
    x_vals = []
    y_vals = []
    z_vals = []
    
    # 收集該類別下所有人員的數據
    counts = pivot_df[cat].tolist()
    
    # 為了效能，我們用一個 Mesh3d 物件畫出該類別的所有柱子 (或者分開畫也可以，分開畫比較好做 hover info)
    # 這裡選擇分開畫每個柱子以便顯示詳細資訊，或者依類別分組
    
    color = google_colors[j % len(google_colors)]
    
    for i, person in enumerate(personnel):
        count = counts[i]
        if count == 0:
            continue
            
        x0, x1 = i - bar_width/2, i + bar_width/2
        y0, y1 = j - bar_depth/2, j + bar_depth/2
        z0, z1 = 0, count
        
        # 定義立方體頂點
        vertices_x = [x0, x1, x1, x0, x0, x1, x1, x0]
        vertices_y = [y0, y0, y1, y1, y0, y0, y1, y1]
        vertices_z = [z0, z0, z0, z0, z1, z1, z1, z1]
        
        # 定義面 (修正為正確的封閉立方體索引)
        # 0:000, 1:100, 2:110, 3:010
        # 4:001, 5:101, 6:111, 7:011
        
        # Bottom: 0-2-1, 0-3-2
        # Top: 4-5-6, 4-6-7
        # Front: 0-1-5, 0-5-4
        # Right: 1-2-6, 1-6-5
        # Back: 2-3-7, 2-7-6
        # Left: 0-4-7, 0-7-3
        
        i_faces = [0, 0, 4, 4, 0, 0, 1, 1, 2, 2, 0, 0]
        j_faces = [2, 3, 5, 6, 1, 5, 2, 6, 3, 7, 4, 7]
        k_faces = [1, 2, 6, 7, 5, 4, 6, 5, 7, 6, 7, 3]
        
        # 繪製實體方塊 (Mesh3d)
        fig.add_trace(go.Mesh3d(
            x=vertices_x,
            y=vertices_y,
            z=vertices_z,
            i=i_faces,
            j=j_faces,
            k=k_faces,
            color=color,
            opacity=1.0,  # 改為不透明
            name=cat,
            showlegend=False,
            flatshading=True,
            hoverinfo='text',
            text=f"人員: {person}<br>類別: {cat}<br>案件數: {count}",
            lighting=dict(ambient=0.7, diffuse=0.8, specular=0.1, roughness=0.1) # 調整光影讓平面更明顯
        ))

        # 繪製邊框線條 (Scatter3d) 讓方塊更有立體感
        # 定義線條路徑: 底面框 -> 頂面框 -> 垂直稜線
        lines_x = [x0, x1, x1, x0, x0, None, x0, x1, x1, x0, x0, None, x0, x0, None, x1, x1, None, x1, x1, None, x0, x0]
        lines_y = [y0, y0, y1, y1, y0, None, y0, y0, y1, y1, y0, None, y0, y0, None, y0, y0, None, y1, y1, None, y1, y1]
        lines_z = [z0, z0, z0, z0, z0, None, z1, z1, z1, z1, z1, None, z0, z1, None, z0, z1, None, z0, z1, None, z0, z1]
        
        fig.add_trace(go.Scatter3d(
            x=lines_x, y=lines_y, z=lines_z,
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))

# 手動添加圖例 (Dummy traces)
for j, cat in enumerate(categories):
    fig.add_trace(go.Scatter3d(
        x=[None], y=[None], z=[None],
        mode='markers',
        marker=dict(size=10, color=google_colors[j % len(google_colors)]),
        name=cat
    ))

# 計算每個人員的總案件數，用於排序或標註
total_counts = pivot_df.sum(axis=1)
max_count = total_counts.max()

# 更新佈局
fig.update_layout(
    title=dict(
        text='<b>👨‍🔧 維修人員 KPI 分析 (案件分類統計)</b>',
        font=dict(size=32, family='Microsoft JhengHei', color='#202124'),
        x=0.5
    ),
    scene=dict(
        xaxis=dict(
            title=dict(text='維修人員', font=dict(size=18)),
            tickmode='array',
            tickvals=list(range(len(personnel))),
            ticktext=personnel,
            tickfont=dict(size=14, family='Microsoft JhengHei', weight='bold'),
            gridcolor='#E0E0E0'
        ),
        yaxis=dict(
            title=dict(text='精簡類別', font=dict(size=18)),
            tickmode='array',
            tickvals=list(range(len(categories))),
            ticktext=categories,
            tickfont=dict(size=14, family='Microsoft JhengHei', weight='bold'),
            gridcolor='#E0E0E0'
        ),
        zaxis=dict(
            title=dict(text='案件數量', font=dict(size=18)),
            tickfont=dict(size=14),
            gridcolor='#E0E0E0'
        ),
        camera=dict(
            eye=dict(x=2.0, y=-2.0, z=1.0) # 調整視角以便看清 X 和 Y
        ),
        bgcolor='#FAFAFA',
        aspectmode='manual',
        aspectratio=dict(x=2, y=1.5, z=1)
    ),
    paper_bgcolor='white',
    margin=dict(l=20, r=20, t=80, b=20),
    legend=dict(
        title=dict(text='<b>精簡類別</b>', font=dict(size=16)),
        font=dict(size=14, family='Microsoft JhengHei'),
        bgcolor='rgba(255,255,255,0.9)',
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=0.05
    )
)

output_path = r'c:\Users\f2302\Desktop\報修分析\人員KPI分析_3D圖表.html'
fig.write_html(output_path)
print(f"✅ 人員 KPI 3D 圖表已儲存至: {output_path}")

# 輸出簡單統計
print("\n=== 人員案件統計 ===")
print(total_counts.sort_values(ascending=False))
