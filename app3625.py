import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(layout="wide")

# --- 2. CSS CUSTOM: TẠO KHUNG VUÔNG CHÍNH GIỮA MÀN HÌNH ---
st.markdown("""
    <style>
    /* Nền chính tối sâu phía sau */
    .stApp {
        background-color: #0b1015 !important;
    }

    /* Tạo container căn giữa màn hình */
    [data-testid="stVerticalBlock"] > div:has(div.rok-profile-card) {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 50px 0;
    }

    /* Khung xanh đậm vuông vức, nổi bật */
    .rok-profile-card {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border: 2px solid #3eb5e5;
        border-radius: 15px;
        width: 80%;
        max-width: 900px; /* Độ rộng tối đa để giữ dáng vuông */
        padding: 30px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.7);
        font-family: sans-serif;
    }

    /* Header Profile */
    .p-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px; }
    .governor-name { font-size: 38px; font-weight: 800; text-transform: uppercase; margin: 0; line-height: 1; }
    .governor-id { color: #b0d4e3; font-size: 14px; margin-top: 5px; }
    .alliance-tag { color: #ffd700; font-weight: bold; font-size: 15px; }

    /* Xếp hạng góc phải */
    .rank-tag {
        background: #f39c12; color: #fff;
        padding: 5px 15px; border-radius: 20px;
        font-weight: bold; font-size: 14px;
    }

    /* Lưới thông số (Sức mạnh, Kill, Dead...) */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        margin-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 20px;
    }
    .stat-box {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }
    .s-label { color: #b0d4e3; font-size: 12px; font-weight: bold; text-transform: uppercase; }
    .s-value { font-size: 26px; font-weight: 800; color: #ffffff; }

    /* Khu vực chỉ số KPI % */
    .kpi-row {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
        background: rgba(0, 0, 0, 0.15);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .kpi-item { text-align: center; }
    .kpi-title { font-size: 11px; font-weight: bold; color: #e0e0e0; margin-bottom: 5px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM CHỐNG LỖI DỮ LIỆU ---
def safe_n(val):
    """Chuyển đổi dữ liệu sang số, nếu lỗi trả về 0 để app không bị sập"""
    try:
        return float(str(val).replace(',', '').strip())
    except:
        return 0.0

# --- 4. GIẢ LẬP DỮ LIỆU TỪ SHEET (Thay bằng df của bạn) ---
# Thống đốc Gấu As | ID: 205888413 | [B/56] Praetoria
d = {
    "Tên": "Gấu As",
    "ID": "205888413",
    "Liên Minh": "[B/56] Praetoria",
    "Sức Mạnh": 52119586,
    "Tiêu Diệt": 330648467,
    "Điểm Chết": 2324564,
    "KPI_K": 33.3,
    "KPI_D": 250.0,
    "KPI_Total": 141.7
}

# --- 5. HIỂN THỊ GIAO DIỆN CHUẨN Ô Profile VUÔNG ---
# Tiêu đề bên ngoài khung
st.write("## TRUNG TÂM CHỈ HUY KPI")
st.markdown("---")

# MỞ THẺ DIV KHUNG Profile
st.markdown('<div class="rok-profile-card">', unsafe_allow_html=True)

# Header: Tên & ID & Alliance & Rank
st.markdown(f"""
    <div class="p-header">
        <div>
            <h1 class="governor-name">战士: {d['Tên']}</h1>
            <p class="governor-id">ID: {d['ID']} | <span class="alliance-tag">{d['Liên Minh']}</span></p>
        </div>
        <div class="rank-tag">RANK 3</div>
    </div>
    """, unsafe_allow_html=True)

# Chia cột thông số chính
st.markdown(f"""
    <div class="stats-container">
        <div class="stat-box">
            <span class="s-label">POWER</span>
            <span class="s-value">{int(safe_n(d['Sức Mạnh'])):,}</span>
        </div>
        <div class="stat-box">
            <span class="s-label">TOTAL KILL (Points)</span>
            <span class="s-value">{int(safe_n(d['Tiêu Diệt'])):,}</span>
        </div>
        <div class="stat-box">
            <span class="s-label">TOTAL DEAD (Points)</span>
            <span class="s-value">{int(safe_n(d['Điểm Chết'])):,}</span>
        </div>
        <div class="stat-box">
            <span class="s-label">TIẾN ĐỘ CHIẾN DỊCH</span>
            <span class="s-value" style="color:#00ff88">S-RANK</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="margin-top:20px; color: #b0d4e3; text-align:center; font-weight:bold; font-size:12px;">HIỆU SUẤT KPI (%)</div>', unsafe_allow_html=True)

# Hàng chứa các con số KPI %
st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-item">
            <div class="kpi-title">KPI KILL</div>
            <div style="font-size:20px; font-weight:bold; color:white;">{safe_n(d['KPI_K']):.1f}%</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-title">KPI DEAD</div>
            <div style="font-size:20px; font-weight:bold; color:#ff4b4b;">{safe_n(d['KPI_D']):.1f}%</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-title">TOTAL KPI</div>
            <div style="font-size:24px; font-weight:bold; color:#ffd700;">{safe_n(d['KPI_Total']):.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ĐÓNG THẺ DIV KHUNG Profile
st.markdown('</div>', unsafe_allow_html=True)
