import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# 讀取已有精簡分類的報修資料
df = pd.read_csv(r'c:\Users\f2302\Desktop\報修分析\報修明細數據_精簡分類.csv')

# 人員職責對照表（含 emoji 與配色）
personnel_info = {
    '陳世霖': {'emoji': '🔧', 'title': '實體損壞、水電問題', 'details': '漏水、水管、馬桶、燈具、門壞、電視硬體、家具', 'priority': 1, 'color': '#EA4335'}, # Red
    '彭柏翔': {'emoji': '⚙️', 'title': '電力、空調、環控', 'details': '插座、冷氣、風管、環控偵測器', 'priority': 2, 'color': '#4285F4'}, # Blue
    '蘇昱融': {'emoji': '🚨', 'title': '警報、門禁軟體', 'details': '警報、門禁錯誤、監控軟體、中興保全', 'priority': 3, 'color': '#E91E63'}, # Pink
    '鄭易佳': {'emoji': '🧽', 'title': '清潔與衛生', 'details': '髒污、異味、垃圾、衛生紙、咖啡機', 'priority': 4, 'color': '#34A853'}, # Green
    '秦婉蓉': {'emoji': '🧷', 'title': '行政用品、HDMI', 'details': '文具、名片、HDMI線、訪客報到機', 'priority': 5, 'color': '#FBBC05'}, # Yellow
    '吳昭穎': {'emoji': '🖨️', 'title': '事務機設備', 'details': '影印機、印表機、掃描器、卡紙', 'priority': 6, 'color': '#8E24AA'}, # Purple
    '陳德儀': {'emoji': '🚗', 'title': '差勤、停車、標示', 'details': '停車位、標示貼紙、桶裝水', 'priority': 7, 'color': '#FF6D01'}, # Orange
    '林雅雯': {'emoji': '✈️', 'title': '國外差旅', 'details': '國外差旅、交通車', 'priority': 8, 'color': '#00ACC1'}, # Cyan
    '梁時豪': {'emoji': '♻️', 'title': '行政權限、廢棄物', 'details': '文件銷毀、權限管理', 'priority': 9, 'color': '#607D8B'}, # Blue Grey
    '曾誌偉': {'emoji': '🧪', 'title': '化學品、保全管理', 'details': '化學品、承攬商、保全', 'priority': 10, 'color': '#795548'}, # Brown
    '鄭志峯': {'emoji': '🔨', 'title': '一般維修', 'details': '一般維修支援', 'priority': 11, 'color': '#9E9E9E'}  # Grey
}

# 資料處理
df['實際維修人員'] = df['實際維修人員'].str.strip()
pivot_df = df.pivot_table(index='實際維修人員', columns='精簡類別', aggfunc='size', fill_value=0)

personnel = pivot_df.index.tolist()
categories = pivot_df.columns.tolist()

# Google 品牌色系
google_colors = ['#4285F4', '#EA4335', '#FBBC05', '#34A853', '#FF6D01', '#46BDC6', '#7B1FA2', '#E91E63']

fig = go.Figure()

bar_width = 0.5
bar_depth = 0.5

# 構建 3D 圖表
for j, cat in enumerate(categories):
    counts = pivot_df[cat].tolist()
    # 根據類別分配顏色
    color = google_colors[j % len(google_colors)]
    
    for i, person in enumerate(personnel):
        count = counts[i]
        if count == 0:
            continue
            
        # 取得人員對應顏色 (若要依人員改色可在此調整，目前依類別著色)
        
        x0, x1 = i - bar_width/2, i + bar_width/2
        y0, y1 = j - bar_depth/2, j + bar_depth/2
        z0, z1 = 0, count
        
        # 定義立方體頂點
        vertices_x = [x0, x1, x1, x0, x0, x1, x1, x0]
        vertices_y = [y0, y0, y1, y1, y0, y0, y1, y1]
        vertices_z = [z0, z0, z0, z0, z1, z1, z1, z1]
        
        # 定義面 (正確索引)
        i_faces = [0, 0, 4, 4, 0, 0, 1, 1, 2, 2, 0, 0]
        j_faces = [2, 3, 5, 6, 1, 5, 2, 6, 3, 7, 4, 7]
        k_faces = [1, 2, 6, 7, 5, 4, 6, 5, 7, 6, 7, 3]
        
        person_info = personnel_info.get(person, {'emoji': '👤'})
        
        hover_template = f"""
<b>{person_info['emoji']} {person}</b>
<br>📂 類別: {cat}
<br>📊 數量: <b>{count}</b>
<br><i style="font-size:10px; color:#ddd;">點擊查看詳情</i>
        """
        
        fig.add_trace(go.Mesh3d(
            x=vertices_x, y=vertices_y, z=vertices_z,
            i=i_faces, j=j_faces, k=k_faces,
            color=color,
            opacity=1.0, # 實體
            name=cat,
            showlegend=False,
            flatshading=True, # 關閉光影 (平面化)
            lighting=dict(ambient=1.0, diffuse=0.0, specular=0.0, roughness=1.0, fresnel=0.0),
            hoverinfo='text',
            hovertext=hover_template.strip()
        ))
        
        # 邊框線條
        lines_x = [x0, x1, x1, x0, x0, None, x0, x1, x1, x0, x0, None, x0, x0, None, x1, x1, None, x1, x1, None, x0, x0]
        lines_y = [y0, y0, y1, y1, y0, None, y0, y0, y1, y1, y0, None, y0, y0, None, y0, y0, None, y1, y1, None, y1, y1]
        lines_z = [z0, z0, z0, z0, z0, None, z1, z1, z1, z1, z1, None, z0, z1, None, z0, z1, None, z0, z1, None, z0, z1]
        
        fig.add_trace(go.Scatter3d(
            x=lines_x, y=lines_y, z=lines_z,
            mode='lines',
            line=dict(color='black', width=3),
            showlegend=False,
            hoverinfo='skip'
        ))

# 圖例 Dummy
for j, cat in enumerate(categories):
    fig.add_trace(go.Scatter3d(
        x=[None], y=[None], z=[None],
        mode='markers',
        marker=dict(size=10, color=google_colors[j % len(google_colors)]),
        name=cat
    ))

# 佈局設定
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0), # 滿版
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    scene=dict(
        xaxis=dict(
            title=dict(text='維修人員', font=dict(size=16, color='#5F6368')),
            tickmode='array',
            tickvals=list(range(len(personnel))),
            ticktext=[f"{personnel_info.get(p, {}).get('emoji', '')} {p}" for p in personnel],
            tickfont=dict(size=12, color='#3C4043'),
            backgroundcolor='#F8F9FA',
            gridcolor='#E8EAED',
            showbackground=True,
        ),
        yaxis=dict(
            title=dict(text='問題類別', font=dict(size=16, color='#5F6368')),
            tickmode='array',
            tickvals=list(range(len(categories))),
            ticktext=categories,
            tickfont=dict(size=12, color='#3C4043'),
            backgroundcolor='#F8F9FA',
            gridcolor='#E8EAED',
            showbackground=True,
        ),
        zaxis=dict(
            title=dict(text='案件數', font=dict(size=16, color='#5F6368')),
            tickfont=dict(size=12, color='#3C4043'),
            backgroundcolor='#F8F9FA',
            gridcolor='#E8EAED',
            showbackground=True,
        ),
        camera=dict(
            eye=dict(x=1.4, y=-1.4, z=0.6),
            center=dict(x=0, y=0, z=-0.2)
        ),
        aspectmode='manual',
        aspectratio=dict(x=2, y=1.2, z=0.8)
    ),
    legend=dict(
        yanchor="top",
        y=0.95,
        xanchor="right",
        x=0.95,
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#E8EAED",
        borderwidth=1,
        font=dict(size=13, color='#3C4043')
    )
)

# 產生圖表 HTML div
plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn', config={'displayModeBar': True, 'responsive': True})

# 計算統計數據
total_cases = df.shape[0]
total_people = len(personnel)
sorted_personnel = sorted(
    [(p, personnel_info.get(p, {})) for p in personnel],
    key=lambda x: x[1].get('priority', 999)
)
total_counts = df['實際維修人員'].value_counts()
max_count = total_counts.max() if not total_counts.empty else 1

# 建立完整 HTML
html_content = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Style KPI Analysis Dashboard</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
    <!-- Plotly.js -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        :root {{
            --google-blue: #4285F4;
            --google-red: #EA4335;
            --google-yellow: #FBBC05;
            --google-green: #34A853;
            --bg-color: #F8F9FA;
            --text-primary: #202124;
            --text-secondary: #5F6368;
            --card-shadow: 0 4px 12px rgba(0,0,0,0.1);
            --sidebar-width: 320px;
        }}
        
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Google Sans', 'Noto Sans TC', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            overflow: hidden; /* 防止雙卷軸 */
            height: 100vh;
            display: flex;
        }}

        /* 側邊欄懸浮卡片設計 */
        #sidebar {{
            width: var(--sidebar-width);
            height: 94vh;
            margin: 3vh 0 3vh 20px;
            background: #FFFFFF;
            border-radius: 16px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.08);
            display: flex;
            flex-direction: column;
            z-index: 100;
            position: relative;
            border: 1px solid rgba(0,0,0,0.05);
        }}
        
        #sidebar-header {{
            padding: 24px 24px 16px 24px;
            border-bottom: 1px solid #F1F3F4;
        }}
        
        h1 {{
            font-size: 20px;
            font-weight: 500;
            margin: 0 0 12px 0;
            color: var(--text-primary);
            letter-spacing: -0.5px;
        }}
        
        .badge-container {{
            display: flex;
            gap: 8px;
        }}
        
        .badge {{
            background: #F1F3F4;
            color: var(--text-secondary);
            padding: 4px 12px;
            border-radius: 50px;
            font-size: 12px;
            font-weight: 600;
        }}

        #personnel-list {{
            flex: 1;
            overflow-y: auto;
            padding: 16px 20px;
        }}
        
        /* 隱藏卷軸但保留功能 */
        #personnel-list::-webkit-scrollbar {{
            width: 6px;
        }}
        #personnel-list::-webkit-scrollbar-thumb {{
            background-color: #DADCE0;
            border-radius: 3px;
        }}

        .person-card {{
            background: #FFFFFF;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 1px 2px rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
            border-left: 0; /* 移除舊的 border */
        }}
        
        .person-card:hover {{
            box-shadow: 0 4px 8px 3px rgba(60,64,67,0.15);
            transform: translateY(-1px);
        }}
        
        .person-card.active {{
            background: #F8F9FA;
            box-shadow: inset 0 0 0 2px var(--google-blue);
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }}
        
        .name-group {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        
        .emoji-icon {{ 
            font-size: 20px; 
            margin-bottom: 4px;
        }}
        
        .name {{ 
            font-weight: 500; 
            font-size: 16px; 
            color: var(--text-primary);
        }}
        
        .count-badge {{ 
            background: #F1F3F4;
            color: var(--text-primary);
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 700;
        }}
        
        .role-pill {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            background: #F8F9FA; /* Default fallback */
        }}
        
        .details {{
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: 16px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .progress-container {{
            width: 100%;
            height: 4px;
            background-color: #F1F3F4;
            border-radius: 2px;
            overflow: hidden;
        }}
        
        .progress-bar {{
            height: 100%;
            border-radius: 2px;
            transition: width 0.5s ease-out;
        }}

        /* 主畫面圖表區 */
        #main-content {{
            flex: 1;
            height: 100vh;
            position: relative;
            overflow: hidden;
        }}
        
        /* 確保 Plotly 圖表填滿容器 */
        .plotly-graph-div, #main-content > div {{
            width: 100% !important;
            height: 100% !important;
        }}
        
        /* 浮水印/標題 */
        .chart-overlay-title {{
            position: absolute;
            bottom: 30px; /* 改到底部 */
            right: 30px;
            text-align: right;
            pointer-events: none;
            z-index: 10;
        }}
        
        .chart-overlay-title h2 {{
            margin: 0;
            font-size: 32px;
            font-weight: 400;
            color: var(--text-primary);
        }}
        
        .chart-overlay-title p {{
            margin: 8px 0 0 0;
            color: var(--text-secondary);
        }}

    </style>
</head>
<body>

    <aside id="sidebar">
        <header id="sidebar-header">
            <h1>維修人員配置</h1>
            <div class="badge-container">
                <div class="badge">總案件: {total_cases}</div>
                <div class="badge">人員: {total_people}</div>
            </div>
        </header>
        
        <div id="personnel-list">
"""

# 生成人員卡片
for person, info in sorted_personnel:
    count = total_counts.get(person, 0)
    if count == 0: continue
    
    color = info.get('color', '#9E9E9E')
    percent = (count / max_count) * 100
    
    html_content += f"""
            <div class="person-card" onclick="focusPerson('{person}')">
                <div class="card-header">
                    <div class="name-group">
                        <span class="emoji-icon">{info['emoji']}</span>
                        <span class="name">{person}</span>
                    </div>
                    <span class="count-badge">{count}</span>
                </div>
                
                <div class="role-pill" style="color: {color}; border: 1px solid {color}33; background: {color}11;">
                    {info['title']}
                </div>
                
                <div class="details">{info['details']}</div>
                
                <div class="progress-container">
                    <div class="progress-bar" style="width: {percent}%; background-color: {color};"></div>
                </div>
            </div>
    """

html_content += f"""
        </div>
    </aside>

    <main id="main-content">
        <div class="chart-overlay-title">
            <h2>KPI Analytics</h2>
            <p>維修數據 3D 可視化分析</p>
        </div>
        {plot_div}
    </main>

    <script>
        // 簡單互動邏輯
        function focusPerson(name) {{
            // 點擊卡片時的高亮效果
            document.querySelectorAll('.person-card').forEach(card => card.classList.remove('active'));
            event.currentTarget.classList.add('active');
            
            // 這裡未來可以加入控制 Plotly Camera 的邏輯
            console.log("Focus on:", name);
        }}
    </script>

</body>
</html>
"""

output_path = r'c:\Users\f2302\Desktop\報修分析\index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✨ 全新 Google 風格儀表板已生成: {output_path}")
