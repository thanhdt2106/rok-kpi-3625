import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide")

# --- CSS ĐỂ TẠO KHUNG XANH BAO PHỦ TOÀN BỘ ---
st.markdown("""
    <style>
    /* Nền tối cho app */
    .stApp { background-color: #0e1117; }

    /* Khung xanh chủ đạo bao quanh toàn bộ nội dung */
    .main-profile-container {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border: 2px solid #3eb5e5;
        border-radius: 15px;
        padding: 30px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }

    /* Header: Tên và ID */
    .profile-header { margin-bottom: 25px; }
    .governor-name { font-size: 40px; font-weight: 800; text-transform: uppercase; margin: 0; }
    .governor-id { font-size: 16px; color: #b0d4e3; }

    /* Ô thông số (Stats) */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-bottom: 25px;
    }
    .stat-card {
        background: rgba(0, 0, 0, 0.4);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    .stat-label { display: block; font-size: 11px; color: #b0d4e3; text-transform: uppercase; font-weight: bold; }
    .stat-value { display: block; font-size: 22px; font-weight: 800; margin-top: 5px; }

    /* Khu vực biểu đồ */
    .chart-section {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 12px;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM VẼ BIỂU ĐỒ (SỬA LỖI VALUEERROR) ---
def draw_kpi_chart(pct, color, label):
    try:
        val = float(pct)
    except:
        val = 0.0
    
    fig = go.Figure(go.Pie(
        hole=0.7,
        values=[val, max(0, 100-val)],
        marker=dict(colors=[color, "rgba(255,255,255,0.05)"]),
        showlegend=False,
        hoverinfo='skip'
    ))
    fig.update_layout(
        title={'text': f"<b>{label}</b>", 'y':0.9, 'x':0.5, 'xanchor':'center', 'font':{'color':'white', 'size':14}},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=30, b=0, l=10, r=10),
        height=180,
        annotations=[dict(text=f"<b>{val}%</b>", x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=18))]
    )
    return fig

# --- GIẢ LẬP DỮ LIỆU (Thay bằng df của bạn) ---
# Ở đây tôi dùng dữ liệu mẫu để bạn thấy khung hình
d = {
    "Tên": "22 MORPHEUS",
    "ID": "210247547",
    "Liên Minh": "[sis6] shared house 3956",
    "Sức Mạnh": 20095399,
    "Tiêu Diệt": 9216189,
    "Điểm Chết": 450123,
    "KPI_K": 45.5,
    "KPI_D": 80.0,
    "KPI_T": 62.7
}

# --- HIỂN THỊ GIAO DIỆN ---
st.title("Hệ thống quản lý KPI")

# Mở khung xanh bao phủ
st.markdown('<div class="main-profile-container">', unsafe_allow_html=True)

# Header
st.markdown(f"""
    <div class="profile-header">
        <div class="governor-name">⚔️ {d['Tên']}</div>
        <div class="governor-id">ID: {d['ID']} | Liên minh: {d['Liên Minh']}</div>
    </div>
    """, unsafe_allow_html=True)

# Grid thông số
st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card"><span class="stat-label">SỨC MẠNH</span><span class="stat-value">{d['Sức Mạnh']:,}</span></div>
        <div class="stat-card"><span class="stat-label">TỔNG KILL</span><span class="stat-value">{d['Tiêu Diệt']:,}</span></div>
        <div class="stat-card"><span class="stat-label">ĐIỂM CHẾT</span><span class="stat-value">{d['Điểm Chết']:,}</span></div>
        <div class="stat-card"><span class="stat-label">XẾP HẠNG</span><span class="stat-value" style="color:#ffd700">S-RANK</span></div>
    </div>
    """, unsafe_allow_html=True)

# Khu vực biểu đồ
st.markdown('<div class="chart-section">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.plotly_chart(draw_kpi_chart(d['KPI_K'], "#00ffff", "KPI KILL"), use_container_width=True)
with c2: st.plotly_chart(draw_kpi_chart(d['KPI_D'], "#ff4b4b", "KPI DEAD"), use_container_width=True)
with c3: st.plotly_chart(draw_kpi_chart(d['KPI_T'], "#ffd700", "TOTAL KPI"), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Đóng khung xanh
st.markdown('</div>', unsafe_allow_html=True)
