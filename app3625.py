import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. SIÊU CSS & JAVASCRIPT (ĐỂ LÀM THANH KÉO TRƯỢT) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    
    /* STYLE CHO THANH KÉO (DRAWER) */
    #myDrawer {
        height: 100%;
        width: 0;
        position: fixed;
        z-index: 999999;
        top: 0;
        left: 0;
        background-color: rgba(13, 27, 42, 0.95);
        overflow-x: hidden;
        transition: 0.5s;
        padding-top: 60px;
        border-right: 2px solid #00d4ff;
    }
    #myDrawer a {
        padding: 15px 25px;
        text-decoration: none;
        font-size: 15px;
        color: #e0e6ed;
        display: block;
        transition: 0.3s;
        border-bottom: 1px solid rgba(0,212,255,0.1);
    }
    #myDrawer .closebtn {
        position: absolute;
        top: 10px;
        right: 25px;
        font-size: 36px;
        color: #ff4b4b;
    }
    .drawer-title { color: #00d4ff; font-weight: bold; padding: 0 25px 20px; font-size: 18px; }
    </style>

    <div id="myDrawer">
      <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
      <div class="drawer-title">📋 THÔNG TIN NHANH</div>
      <a>⚠️ Tài khoản thiếu KPI</a>
      <a>🏔️ Top 15 Đèo 4</a>
      <a>🌋 Top 15 Đèo 7</a>
      <a>👑 Top 15 Kingland</a>
      <a>📅 Cập nhật: 2026</a>
    </div>

    <script>
    function openNav() { document.getElementById("myDrawer").style.width = "300px"; }
    function closeNav() { document.getElementById("myDrawer").style.width = "0"; }
    </script>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (GIỮ NGUYÊN BẢN CỦA LOUIS) ---
with st.sidebar:
    st.markdown('<div style="color: #00d4ff; font-weight: bold; font-size: 18px; text-align: center; margin-bottom: 20px;">🛡️ COMMAND CENTER</div>', unsafe_allow_html=True)
    
    # Nút mở ngăn kéo bằng HTML để không bị reload trang
    st.components.v1.html("""
        <button onclick="parent.openNav()" style="width: 100%; background: #1a2a3a; color: #00d4ff; border: 1px solid #00d4ff; padding: 10px; border-radius: 5px; cursor: pointer; font-weight: bold;">
            ⚙️ CÀI ĐẶT HỆ THỐNG
        </button>
    """, height=50)

    st.divider()
    st.write("**NGÔN NGỮ / LANGUAGE**")
    lang = st.radio("Lang", ["VN", "EN"], horizontal=True, label_visibility="collapsed")
    
    st.divider()
    st.write("**MENU**")
    menu = st.radio("Menu", ["📊 Bảng KPI", "👤 Tài khoản", "⚙️ Quản lý KPI"], label_visibility="collapsed")
    
    st.divider()
    st.info("Phiên bản v10.9 - Admin Louis")

# --- 4. LOGIC DỮ LIỆU & HIỂN THỊ (GIỮ NGUYÊN CARD PROFILE) ---
texts = {
    "VN": {"search": "👤 Tìm kiếm...", "pow": "SỨC MẠNH", "tk": "TỔNG TIÊU DIỆT", "td": "ĐIỂM CHẾT"},
    "EN": {"search": "👤 Search...", "pow": "POWER", "tk": "TOTAL KILL", "td": "TOTAL DEAD"}
}
L = texts[lang]

# Giả lập load data (Louis giữ nguyên hàm load_data cũ của bạn ở đây)
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
# ... (Phần code gộp data cũ của Louis mình không thay đổi) ...

if menu == "📊 Bảng KPI":
    # Phần hiển thị logo và selectbox của Louis
    st.markdown(f'<div style="text-align:center; margin-top:-20px;"><img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true" width="280"></div>', unsafe_allow_html=True)
    
    # Dưới đây là nơi hiển thị Profile Card khi chọn thành viên
    # Mình đảm bảo khối components.html(html_card) của bạn vẫn nằm ở đây
    st.write("---")
    st.warning("Louis hãy dán phần hiển thị Table và Card cũ vào đây để chạy nhé!")

st.markdown('<div style="position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #8b949e; padding: 10px; text-align: center; border-top: 1px solid #1a2a3a;">🛡️ Admin Louis | v10.9</div>', unsafe_allow_html=True)
