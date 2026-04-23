import streamlit as st
import streamlit.components.v1 as components

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide")

# --- DỮ LIỆU (Bạn có thể thay bằng df.iloc[0] của bạn) ---
data = {
    "name": "56 3IMAD",
    "id": "154411253",
    "alliance": "[[C/56]PRAETORIA]",
    "kills": "3,358,382",
    "power": "13,212,420",
    "dead": "0",
    "rank": "S-RANK",
    "kpi_kill": 0.0,
    "kpi_dead": 0.0,
    "total_kpi": 0.0
}

# --- CHUẨN BỊ HTML & CSS ---
# Chúng ta đưa toàn bộ giao diện vào một chuỗi HTML duy nhất để tránh bị Streamlit chia cắt
html_code = f"""
<div class="main-container">
    <style>
        .main-container {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(145deg, #0a3d62, #062c43);
            border: 2px solid #3282b8;
            border-radius: 15px;
            padding: 30px;
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin: 10px auto;
            max-width: 1100px;
        }}
        
        .header {{ margin-bottom: 25px; }}
        .header h1 {{ margin: 0; font-size: 32px; color: #fff; }}
        .header p {{ margin: 5px 0; color: #bbe1fa; font-size: 14px; }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
        }}

        .label {{ font-size: 11px; color: #bbe1fa; text-transform: uppercase; font-weight: bold; }}
        .value {{ display: block; font-size: 20px; font-weight: bold; margin-top: 5px; }}
        .rank {{ color: #ffd700; }}

        .kvk-title {{
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
            color: #bbe1fa;
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 20px;
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            text-align: center;
        }}

        .chart-item {{ position: relative; }}
        
        /* Hiệu ứng vòng tròn giả lập KPI */
        .circle-progress {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: conic-gradient(#00ffff {data['kpi_kill']}% 0, rgba(255,255,255,0.1) 0);
            margin: 10px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}
        .circle-progress::before {{
            content: "{data['kpi_kill']}%";
            position: absolute;
            width: 80px;
            height: 80px;
            background: #082d45;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }}
    </style>

    <div class="header">
        <h1>战士: {data['name']}</h1>
        <p>ID: {data['id']} | <span style="color:#ffd700">{data['alliance']}</span></p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <span class="label">Tiêu Diệt</span>
            <span class="value">{data['kills']}</span>
        </div>
        <div class="stat-card">
            <span class="label">Sức Mạnh</span>
            <span class="value">{data['power']}</span>
        </div>
        <div class="stat-card">
            <span class="label">Điểm Chết</span>
            <span class="value">{data['dead']}</span>
        </div>
        <div class="stat-card">
            <span class="label">Xếp Hạng</span>
            <span class="value rank">{data['rank']}</span>
        </div>
    </div>

    <div class="kvk-title">TIẾN ĐỘ CHIẾN DỊCH KVK</div>

    <div class="charts-grid">
        <div class="chart-item">
            <div class="label">KPI KILL</div>
            <div class="circle-progress"></div>
        </div>
        <div class="chart-item">
            <div class="label">KPI DEAD</div>
            <div class="circle-progress" style="background: conic-gradient(#ff4b4b {data['kpi_dead']}% 0, rgba(255,255,255,0.1) 0);"></div>
        </div>
        <div class="chart-item">
            <div class="label">TỔNG KPI</div>
            <div class="circle-progress" style="background: conic-gradient(#ffd700 {data['total_kpi']}% 0, rgba(255,255,255,0.1) 0);"></div>
        </div>
    </div>
</div>
"""

# --- HIỂN THỊ ---
# Dùng components.html để đảm bảo code không bao giờ bị vỡ lớp div
components.html(html_code, height=550, scrolling=False)
