import pandas as pd
import plotly.graph_objects as go

# 讀取已有精簡分類的報修資料
df = pd.read_csv(r'c:\Users\f2302\Desktop\報修分析\報修明細數據_精簡分類.csv')

# 人員職責對照表（含 emoji）
personnel_info = {
    '陳世霖': {
        'emoji': '🔧',
        'title': '實體損壞、水電問題、硬體維修',
        'details': '漏水、水管、馬桶水電故障、燈具、門壞、自動門、電視硬體壞掉、家具壞、一般飲水機壞、監控硬體',
        'priority': 1,
        'color_base': '#FF6B35'  # 橙色系
    },
    '彭柏翔': {
        'emoji': '⚙️',
        'title': '電力、冷氣、空調、會議室機電、環控偵測器',
        'details': '插座沒電、充電沒反應、冷氣不冷、風管問題、環控偵測器異常',
        'priority': 2,
        'color_base': '#4285F4'  # 藍色系
    },
    '鄭易佳': {
        'emoji': '🧽',
        'title': '清潔與衛生、耗材補充',
        'details': '髒污、異味、垃圾滿了、衛生紙不足、冰箱髒、咖啡機需要清潔',
        'priority': 4,
        'color_base': '#34A853'  # 綠色系
    },
    '秦婉蓉': {
        'emoji': '🧷',
        'title': '行政用品、線材（HDMI）、訪客設備',
        'details': '文具、名片、HDMI線、訪客報到機、行政備品需求',
        'priority': 5,
        'color_base': '#FBBC05'  # 黃色系
    },
    '陳德儀': {
        'emoji': '🚗',
        'title': '國內差勤、停車、標示、桶裝水',
        'details': '停車位問題、標示貼紙、桶裝水更換（B3F/A3F）',
        'priority': 7,
        'color_base': '#EA4335'  # 紅色系
    },
    '林雅雯': {
        'emoji': '✈️',
        'title': '國外差旅、交通車',
        'details': '國外差旅安排、交通車調度',
        'priority': 8,
        'color_base': '#46BDC6'  # 青色系
    },
    '吳昭穎': {
        'emoji': '🖨️',
        'title': '事務機類設備',
        'details': '影印機、印表機、掃描器、卡紙、缺墨、置物櫃密碼、公文鐵櫃、人體工學椅',
        'priority': 6,
        'color_base': '#7B1FA2'  # 紫色系
    },
    '蘇昱融': {
        'emoji': '🚨',
        'title': '警報、門禁軟體、保全系統異常',
        'details': '警報跳出、門禁錯誤訊息、監控軟體錯誤、中興保全異常',
        'priority': 3,
        'color_base': '#E91E63'  # 粉色系
    },
    '梁時豪': {
        'emoji': '♻️',
        'title': '文件銷毀、行政權限、廢棄物',
        'details': '文件銷毀、行政權限管理、廢棄物處理',
        'priority': 9,
        'color_base': '#9E9E9E'  # 灰色系
    },
    '曾誌偉': {
        'emoji': '🧪',
        'title': '化學品、承攬商、保全人員管理',
        'details': '化學品管理、承攬商協調、保全人員管理',
        'priority': 10,
        'color_base': '#795548'  # 棕色系
    },
    '鄭志峯': {
        'emoji': '🔨',
        'title': '一般維修',
        'details': '一般維修工作',
        'priority': 11,
        'color_base': '#607D8B'  # 藍灰色系
    }
}

# 處理人員名稱
df['實際維修人員'] = df['實際維修人員'].str.strip()

# 統計每個人員在各類別的案件數
pivot_df = df.pivot_table(index='實際維修人員', columns='精簡類別', aggfunc='size', fill_value=0)

personnel = pivot_df.index.tolist()
categories = pivot_df.columns.tolist()

# Google 品牌色系（備用）
google_colors = ['#4285F4', '#EA4335', '#FBBC05', '#34A853', '#FF6D01', '#46BDC6', '#7B1FA2', '#E91E63']

fig = go.Figure()

bar_width = 0.4
bar_depth = 0.4

# 為每個類別建立柱子
for j, cat in enumerate(categories):
    counts = pivot_df[cat].tolist()
    color = google_colors[j % len(google_colors)]
    
    for i, person in enumerate(personnel):
        count = counts[i]
        if count == 0:
            continue
            
        # 取得人員資訊
        person_data = personnel_info.get(person, {
            'emoji': '👤',
            'title': '一般維修',
            'details': '',
            'color_base': color
        })
        
        x0, x1 = i - bar_width/2, i + bar_width/2
        y0, y1 = j - bar_depth/2, j + bar_depth/2
        z0, z1 = 0, count
        
        # 定義立方體頂點
        vertices_x = [x0, x1, x1, x0, x0, x1, x1, x0]
        vertices_y = [y0, y0, y1, y1, y0, y0, y1, y1]
        vertices_z = [z0, z0, z0, z0, z1, z1, z1, z1]
        
        # 定義面（正確的封閉立方體索引）
        i_faces = [0, 0, 4, 4, 0, 0, 1, 1, 2, 2, 0, 0]
        j_faces = [2, 3, 5, 6, 1, 5, 2, 6, 3, 7, 4, 7]
        k_faces = [1, 2, 6, 7, 5, 4, 6, 5, 7, 6, 7, 3]
        
        # 增強的 hover 資訊
        hover_text = f"""
<b>{person_data['emoji']} {person}</b><br>
<b>職責：</b>{person_data['title']}<br>
<b>類別：</b>{cat}<br>
<b>案件數：</b>{count} 件<br>
<i>{person_data['details'][:50]}...</i>
        """.strip()
        
        # 繪製實體方塊
        fig.add_trace(go.Mesh3d(
            x=vertices_x,
            y=vertices_y,
            z=vertices_z,
            i=i_faces,
            j=j_faces,
            k=k_faces,
            color=color,
            opacity=1.0,
            name=cat,
            showlegend=False,
            flatshading=True,
            hoverinfo='text',
            hovertext=hover_text,
            lighting=dict(ambient=0.7, diffuse=0.8, specular=0.1, roughness=0.1)
        ))
        
        # 繪製邊框線條
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

# 手動添加圖例
for j, cat in enumerate(categories):
    fig.add_trace(go.Scatter3d(
        x=[None], y=[None], z=[None],
        mode='markers',
        marker=dict(size=10, color=google_colors[j % len(google_colors)]),
        name=cat
    ))

# 計算統計資訊
total_counts = pivot_df.sum(axis=1).sort_values(ascending=False)

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
            ticktext=[f"{personnel_info.get(p, {}).get('emoji', '👤')} {p}" for p in personnel],
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
            eye=dict(x=2.0, y=-2.0, z=1.0)
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

# 生成 HTML（加入側邊欄）
# 取得圖表的 HTML div 字串 (不包含 html/body 標籤與 script)
plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')

# 插入自訂 CSS 和側邊欄
custom_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>維修人員 KPI 分析</title>
    <!-- Plotly.js CDN -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            margin: 0;
            font-family: 'Microsoft JhengHei', sans-serif;
            display: flex;
            background: #f5f5f5;
            height: 100vh;
            overflow: hidden;
        }}
        #sidebar {{
            width: 300px; /* 稍微縮小側邊欄 */
            min-width: 300px;
            background: white;
            padding: 20px;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
            overflow-y: auto;
            position: relative;
            z-index: 10;
        }}
        #chart-container {{
            flex: 1;
            height: 100%;
            position: relative;
            background: #f5f5f5;
        }}
        /* Plotly 容器調整 */
        .plotly-graph-div {{
            height: 100% !important;
            width: 100% !important;
        }}
        .person-card {{
            background: #fafafa;
            border-left: 4px solid;
            padding: 12px;
            margin-bottom: 12px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .person-card:hover {{
            background: #f0f0f0;
            transform: translateX(5px);
        }}
        .person-emoji {{
            font-size: 24px;
            margin-right: 8px;
        }}
        .person-name {{
            font-weight: bold;
            font-size: 16px;
            color: #202124;
        }}
        .person-title {{
            font-size: 13px;
            color: #5f6368;
            margin-top: 4px;
        }}
        .person-details {{
            font-size: 12px;
            color: #80868b;
            margin-top: 6px;
            line-height: 1.4;
        }}
        .priority-badge {{
            display: inline-block;
            background: #ea4335;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            margin-top: 6px;
            font-weight: bold;
        }}
        h2 {{
            color: #202124;
            margin-top: 0;
            font-size: 20px;
            margin-bottom: 15px;
        }}
        .stats {{
            background: #e8f0fe;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .stats-item {{
            font-size: 14px;
            margin: 4px 0;
            color: #1967d2;
        }}
    </style>
</head>
<body>
    <div id="sidebar">
        <h2>👥 人員職責分配</h2>
        <div class="stats">
            <div class="stats-item"><b>總案件數：</b>{df.shape[0]} 件</div>
            <div class="stats-item"><b>維修人員：</b>{len(personnel)} 人</div>
        </div>
"""

# 加入人員卡片（依優先順序排序）
sorted_personnel = sorted(
    [(p, personnel_info.get(p, {})) for p in personnel],
    key=lambda x: x[1].get('priority', 999)
)

for person, info in sorted_personnel:
    if person not in total_counts.index:
        continue
    count = total_counts[person]
    color = info.get('color_base', '#9E9E9E')
    custom_html += f"""
        <div class="person-card" style="border-left-color: {color};" onclick="highlightPerson('{person}')">
            <div>
                <span class="person-emoji">{info.get('emoji', '👤')}</span>
                <span class="person-name">{person}</span>
                <span style="float: right; color: {color}; font-weight: bold;">{count} 件</span>
            </div>
            <div class="person-title">{info.get('title', '')}</div>
            <div class="person-details">{info.get('details', '')}</div>
            <span class="priority-badge">優先順序 {info.get('priority', '-')}</span>
        </div>
    """

custom_html += f"""
    </div>
    <div id="chart-container">
        {plot_div}
    </div>

    <script>
        // 簡單的互動功能 (未來可擴充)
        function highlightPerson(name) {{
            console.log("Selected: " + name);
            // 這裡可以加入與 Plotly 圖表互動的邏輯
        }}
    </script>
</body>
</html>
"""

# 儲存檔案
output_path = r'c:\Users\f2302\Desktop\報修分析\人員KPI分析_增強版.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(custom_html)

print(f"✅ 增強版 KPI 圖表已儲存至: {output_path}")
print("\n=== 人員案件統計（依優先順序） ===")
for person, info in sorted_personnel:
    if person in total_counts.index:
        print(f"{info.get('emoji', '👤')} {person}: {total_counts[person]} 件 (優先順序 {info.get('priority', '-')})")
