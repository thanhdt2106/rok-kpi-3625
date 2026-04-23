import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide")

# --- CSS INJECTION: BIẾN TOÀN BỘ APP THÀNH KHUNG XANH ---
st.markdown("""
    <style>
    /* Biến toàn bộ nền ứng dụng thành màu xanh đặc trưng */
    .stApp {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%) !important;
        color: white !important;
    }

    /* Tùy chỉnh tiêu đề và text */
    h1, h2, h3, p, span, label {
        color: white !important;
    }

    /* Các ô thông số (Stats) */
    .stat-container {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }
    .s-label { font-size: 11px; color: #b0d4e3; text-transform: uppercase; font-weight: bold; }
    .s-value { font-size: 22px; font-weight: 800; display: block; margin-top: 5px; }

    /* Fix lỗi hiển thị biểu đồ Plotly trên nền xanh */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM VẼ BIỂU ĐỒ (SỬA LỖI VALUEERROR GÂY SẬP APP) ---
def draw_kpi(pct, color, title):
    try:
        val = float(pct)
    except:
        val = 0.0
        
    fig = go.Figure(go.Pie(
        hole=0.7,
        values=[val, max(0, 100-val)],
        marker=dict(colors=[color, "rgba(255,255,255,0.1)"]),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        # Sửa lỗi VALUEERROR: Không dùng fontWeight, dùng thẻ <b> trong text
        title={'text': f"<b>{title}</b>", 'y':0.9, 'x':0.5, 'xanchor':'center', 'font':{'color':'white', 'size':14}},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=30, b=0, l=10, r=10),
        height=200,
        annotations=[dict(
            text=f"<b>{val}%</b>", 
            x=0.5, y=0.5, 
            showarrow=False, 
            font=dict(color='white', size=20)
        )]
    )
    return fig

# --- DỮ LIỆU GIẢ LẬP (Thay bằng df.iloc[0] của bạn) ---
d = {
    "Tên": "56 3IMAD",
    "ID": "154411253",
    "Liên Minh": "[[C/56]PRAETORIA]",
    "Tiêu Diệt": 3358382,
    "Sức Mạnh": 13212420,
    "KPI_K": 0.0,
    "KPI_D": 0.0,
    "KPI_T": 0.0
}

# --- HIỂN THỊ GIAO DIỆN ---
# Header
st.title(f"战士: {d['Tên']}")
st.write(f"ID: {d['ID']} | Liên minh: {d['Liên Minh']}")
st.markdown("---")

# Hàng 1: Các ô thông số lồng trong khung mờ
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="stat-container"><span class="s-label">TIÊU DIỆT</span><span class="s-value">{d["Tiêu Diệt"]:,}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-container"><span class="s-label">SỨC MẠNH</span><span class="s-value">{d["Sức Mạnh"]:,}</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="stat-container"><span class="s-label">ĐIỂM CHẾT</span><span class="s-value">0</span></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="stat-container"><span class="s-label">XẾP HẠNG</span><span class="s-value" style="color:#ffd700">S-RANK</span></div>', unsafe_allow_html=True)

st.write("### TIẾN ĐỘ KVK")

# Hàng 2: Biểu đồ KPI
k1, k2, k3 = st.columns(3)
with k1: st.plotly_chart(draw_kpi(d['KPI_K'], "#00ffff", "KPI KILL"), use_container_width=True)
with k2: st.plotly_chart(draw_kpi(d['KPI_D'], "#ff4b4b", "KPI DEAD"), use_container_width=True)
with k3: st.plotly_chart(draw_kpi(d['KPI_T'], "#ffd700", "TOTAL KPI"), use_container_width=True)
