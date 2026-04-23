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

# --- 2. SIÊU CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .block-container { padding-top: 0rem !important; max-width: 98% !important; }
    header { visibility: hidden; height: 0px !important; }

    .logo-container { display: flex; justify-content: center; margin-top: -20px; margin-bottom: 10px; }
    .logo-img { width: 280px; filter: drop-shadow(0px 0px 10px rgba(0, 212, 255, 0.4)); }

    /* Sidebar Style */
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    .sidebar-header { color: #00d4ff; font-weight: bold; font-size: 18px; text-align: center; margin-bottom: 20px; }

    /* Bảng dữ liệu */
    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 20px; }
    .elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
    .elite-table thead th { 
        background: rgba(0, 212, 255, 0.1); color: #00d4ff; text-align: left; 
        padding: 15px; font-size: 16px; border-bottom: 3px solid #00d4ff; 
    }
    .elite-table td { padding: 14px 15px; font-size: 16px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; }
    
    .rank-badge { background: #ffd700; color: #000; padding: 4px 10px; border-radius: 6px; font-weight: 900; font-size: 14px; }
    .kpi-bar-container { width: 100px; background: #1a2a3a; height: 8px; border-radius: 4px; display: inline-block; vertical-align: middle; margin-right: 10px; }
    .kpi-bar-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #00d4ff, #00ffcc); }

    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: rgba(5, 10, 14, 0.95); color: #8b949e; padding: 10px; font-size: 13px; text-align: center; border-top: 1px solid #1a2a3a; z-index: 999; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (THANH MENU BÊN TRÁI) ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">🛡️ COMMAND CENTER</div>', unsafe_allow_html=True)
    
    # Mục chọn ngôn ngữ
    st.write("**NGÔN NGỮ / LANGUAGE**")
    lang = st.radio("Chon ngon ngu", ["VN", "EN"], horizontal=True, label_visibility="collapsed")
    
    st.divider()
    
    # Menu chính - ĐÃ THÊM CÁC MỤC MỚI
    st.write("**MENU QUẢN LÝ**")
    menu = st.radio("Chon menu", [
        "📊 Bảng KPI", 
        "👤 Tài khoản", 
        "⚠️ Tài khoản thiếu KPI",
        "🏔️ Top 15 Đèo 4",
        "🌋 Top 15 Đèo 7",
        "👑 Top 15 Kingland",
        "⚙️ Quản lý KPI"
    ], label_visibility="collapsed")
    
    st.divider()
    st.info("Phiên bản v10.9 - Admin Louis")

# --- 4. DỮ LIỆU (Giữ nguyên cấu trúc của bạn) ---
texts = {
    "VN": {
        "search": "👤 Tìm kiếm thành viên...", "pow": "SỨC MẠNH", "tk": "TỔNG TIÊU DIỆT", "td": "ĐIỂM CHẾT",
        "cols": ['Hạng', 'Thành viên', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']
    },
    "EN": {
        "search": "👤 Search member name...", "pow": "POWER", "tk": "TOTAL KILL", "td": "TOTAL DEAD",
        "cols": ['Rank', 'Member', 'Power', 'Total Kill', 'Total Dead', 'Kill Inc', 'Dead Inc', 'KPI %']
    }
}
L = texts[lang]

SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        for d in [dt, ds]:
            d['ID'] = d['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
            d['Tên'] = d['Tên'].fillna('Unknown').astype(str).str.strip()
        df = pd.merge(dt.drop_duplicates('ID'), ds.drop_duplicates('ID'), on='ID', suffixes=('_1', '_2'))
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        df['KillRank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)
        
        def get_metrics(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 200e6
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = max(0.0, float(r['KI']) / gk) if gk > 0 else 0.0
            pdv = max(0.0, float(r['DI']) / gd) if gd > 0 else 0.0
            return pd.Series([round(pk * 100, 1), round(pdv * 100, 1), round(((pk + pdv) / 2) * 100, 1)])
            
        df[['KPI_K', 'KPI_D', 'KPI_T']] = df.apply(get_metrics, axis=1)
        return df
    except:
        return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    st.markdown(f'<div class="logo-container"><img src="{LOGO_MAIN}" class="logo-img"></div>', unsafe_allow_html=True)

    # 5.1 XỬ LÝ MENU BẢNG KPI TỔNG
    if menu == "📊 Bảng KPI":
        # (Giữ nguyên code hiển thị Selectbox và Card Profile/Table của bạn)
        sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder=L['search'], label_visibility="collapsed")
        # ... [Phần render Card và Table giữ nguyên như cũ] ...
        st.info("Đang hiển thị Bảng KPI Tổng")

    # 5.2 XỬ LÝ TÀI KHOẢN THIẾU KPI (MỚI)
    elif menu == "⚠️ Tài khoản thiếu KPI":
        st.subheader("⚠️ Danh sách tài khoản chưa đạt KPI")
        st.write("Dữ liệu đang được lọc...")
        # Ở đây sau này Louis chỉ cần lọc df[df['KPI_T'] < mốc] rồi hiện bảng là xong.

    # 5.3 XỬ LÝ CÁC MỤC TOP 15 (MỚI)
    elif "Top 15" in menu:
        st.subheader(f"🏆 {menu}")
        st.write("Bảng vinh danh 15 chiến binh xuất sắc nhất.")
        # Louis sẽ lọc df.nlargest(15, 'Cột_Điểm_Tương_Ứng') tại đây.

    # 5.4 CÁC MỤC CÒN LẠI
    elif menu == "👤 Tài khoản":
        st.subheader("👤 Thông tin cá nhân")
        st.write("Vui lòng chọn thành viên ở Bảng KPI để xem chi tiết.")

    elif menu == "⚙️ Quản lý KPI":
        st.subheader("⚙️ Hệ thống quản trị")
        st.write("Dành riêng cho Admin Louis.")

    st.markdown(f'<div class="footer">🛡️ Discord: louiss.nee | Zalo: 0.3.7.3.2.7.4.6.0.0</div>', unsafe_allow_html=True)
else:
    st.error("Lỗi kết nối dữ liệu Google Sheets.")
