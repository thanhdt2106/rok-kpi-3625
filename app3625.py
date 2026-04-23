import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="FTD KPI | COMMAND CENTER", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Link các ảnh
LOGO_MAIN = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true"
LOGO_PROFILE = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true"

# --- 2. SIÊU CSS (Tạo hiệu ứng Ngăn kéo trượt sát lề trái) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .block-container { padding-top: 0rem !important; max-width: 98% !important; }
    header { visibility: hidden; height: 0px !important; }

    /* Nút cài đặt cố định tại góc trái */
    .floating-btn {
        position: fixed;
        bottom: 80px;
        left: 20px;
        z-index: 9999;
    }

    /* Sidebar chính của Streamlit */
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    
    /* BẢNG TRƯỢT (DRAWER) */
    .custom-drawer {
        position: fixed;
        top: 0;
        left: 0;
        width: 300px;
        height: 100%;
        background-color: rgba(13, 27, 42, 0.98);
        border-right: 2px solid #00d4ff;
        z-index: 10000;
        transition: all 0.4s ease;
        padding: 60px 20px;
        box-shadow: 10px 0 30px rgba(0,0,0,0.8);
    }
    
    .drawer-title { color: #00d4ff; font-weight: bold; font-size: 18px; margin-bottom: 20px; border-bottom: 1px solid #1e3a5a; padding-bottom: 10px; }
    .drawer-item { padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 15px; cursor: default; }
    .drawer-item:hover { color: #00d4ff; }

    /* Card & Bảng gốc */
    .logo-container { display: flex; justify-content: center; margin-top: -20px; margin-bottom: 10px; }
    .logo-img { width: 280px; filter: drop-shadow(0px 0px 10px rgba(0, 212, 255, 0.4)); }
    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 20px; }
    .elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
    .elite-table thead th { background: rgba(0, 212, 255, 0.1); color: #00d4ff; text-align: left; padding: 15px; border-bottom: 3px solid #00d4ff; }
    .elite-table td { padding: 14px 15px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; }
    .rank-badge { background: #ffd700; color: #000; padding: 4px 10px; border-radius: 6px; font-weight: 900; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: rgba(5, 10, 14, 0.95); color: #8b949e; padding: 10px; text-align: center; border-top: 1px solid #1a2a3a; z-index: 999; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR GỐC ---
with st.sidebar:
    st.markdown('<div style="color: #00d4ff; font-weight: bold; font-size: 18px; text-align: center; margin-bottom: 20px;">🛡️ COMMAND CENTER</div>', unsafe_allow_html=True)
    lang = st.radio("Ngôn ngữ", ["VN", "EN"], horizontal=True, label_visibility="collapsed")
    st.divider()
    menu = st.radio("Menu", ["📊 Bảng KPI", "👤 Tài khoản", "⚙️ Quản lý KPI"], label_visibility="collapsed")
    st.divider()
    st.info("v10.9 - Admin Louis")

# --- 4. LOGIC ĐÓNG MỞ BẢNG TRƯỢT ---
# Dùng session_state để lưu trạng thái đóng/mở
if 'drawer_open' not in st.session_state:
    st.session_state.drawer_open = False

def toggle_drawer():
    st.session_state.drawer_open = not st.session_state.drawer_open

# Nút bấm nằm ở góc dưới bên trái (hoặc Louis có thể đưa lên trên tùy ý)
st.sidebar.button("⚙️ Mở Bảng Tin Nhanh", on_click=toggle_drawer)

if st.session_state.drawer_open:
    # Hiển thị ngăn kéo trượt ra
    st.markdown("""
        <div class="custom-drawer">
            <div class="drawer-title">📋 DANH SÁCH MỤC</div>
            <div class="drawer-item">⚠️ Tài khoản thiếu KPI</div>
            <div class="drawer-item">🏔️ Top 15 Đèo 4</div>
            <div class="drawer-item">🌋 Top 15 Đèo 7</div>
            <div class="drawer-item">👑 Top 15 Kingland</div>
            <div class="drawer-item">⚙️ Thông tin: v10.9</div>
            <br>
            <p style="font-size: 12px; color: #8b949e;">(Click nút một lần nữa để đóng)</p>
        </div>
    """, unsafe_allow_html=True)

# --- 5. DỮ LIỆU & HIỂN THỊ (Giữ nguyên code gốc của Louis) ---
@st.cache_data(ttl=30)
def load_data():
    try:
        sid = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
        u_t = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=731741617'
        u_s = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=371969335'
        dt = pd.read_csv(u_t).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(u_s).rename(columns=lambda x: x.strip())
        for d in [dt, ds]:
            d['ID'] = d['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
            d['Tên'] = d['Tên'].fillna('Unknown').astype(str).str.strip()
        df = pd.merge(dt.drop_duplicates('ID'), ds.drop_duplicates('ID'), on='ID', suffixes=('_1', '_2'))
        # Logic tính toán KPI (Rút gọn để hiển thị nhanh)
        df['KI'] = pd.to_numeric(df['Tổng Tiêu Diệt_2'], errors='coerce').fillna(0) - pd.to_numeric(df['Tổng Tiêu Diệt_1'], errors='coerce').fillna(0)
        df['DI'] = pd.to_numeric(df['Điểm Chết_2'], errors='coerce').fillna(0) - pd.to_numeric(df['Điểm Chết_1'], errors='coerce').fillna(0)
        df['KPI_T'] = 100 
        df['KillRank'] = df['KI'].rank(ascending=False, method='min').astype(int)
        return df
    except: return None

df = load_data()

if df is not None:
    st.markdown(f'<div class="logo-container"><img src="{LOGO_MAIN}" class="logo-img"></div>', unsafe_allow_html=True)

    if menu == "📊 Bảng KPI":
        # ... Phần Selectbox và Table của Louis ...
        st.write("### Bảng xếp hạng KPI")
        st.dataframe(df[['Tên_2', 'ID', 'KI', 'DI', 'KPI_T']].sort_values('KI', ascending=False), use_container_width=True)

    st.markdown(f'<div class="footer">🛡️ Admin Louis | v10.9</div>', unsafe_allow_html=True)
