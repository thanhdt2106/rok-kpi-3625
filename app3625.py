import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="FTD KPI | COMMAND CENTER", 
    layout="wide", 
    initial_sidebar_state="collapsed" # Mặc định đóng sidebar để dùng nút bấm
)

# Link các ảnh
LOGO_MAIN = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true"
LOGO_PROFILE = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true"

# --- 2. SIÊU CSS (Tùy chỉnh Nút và Sidebar) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .block-container { padding-top: 0rem !important; max-width: 98% !important; }
    header { visibility: hidden; height: 0px !important; }

    /* Custom Sidebar phía bên trái */
    [data-testid="stSidebar"] { 
        background-color: #0d1b2a !important; 
        border-right: 2px solid #00d4ff; 
        min-width: 300px !important;
    }
    
    .sidebar-header { 
        color: #00d4ff; font-weight: bold; font-size: 20px; 
        text-align: center; margin-bottom: 20px; padding: 10px;
        border-bottom: 1px solid #1e3a5a;
    }

    .logo-container { display: flex; justify-content: center; margin-top: -20px; margin-bottom: 10px; }
    .logo-img { width: 280px; filter: drop-shadow(0px 0px 10px rgba(0, 212, 255, 0.4)); }

    /* Bảng dữ liệu */
    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 20px; margin-top: 20px; }
    .elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
    .elite-table thead th { 
        background: rgba(0, 212, 255, 0.1); color: #00d4ff; text-align: left; 
        padding: 15px; font-size: 15px; border-bottom: 3px solid #00d4ff; 
    }
    .elite-table td { padding: 12px 15px; font-size: 15px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; }
    
    .rank-badge { background: #ffd700; color: #000; padding: 3px 8px; border-radius: 4px; font-weight: 900; }
    .kpi-bar-container { width: 80px; background: #1a2a3a; height: 6px; border-radius: 3px; display: inline-block; vertical-align: middle; }
    .kpi-bar-fill { height: 100%; border-radius: 3px; background: linear-gradient(90deg, #00d4ff, #00ffcc); }

    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: rgba(5, 10, 14, 0.95); color: #8b949e; padding: 10px; font-size: 13px; text-align: center; border-top: 1px solid #1a2a3a; z-index: 999; }
    
    /* Nút cài đặt góc trái dưới */
    .stActionButton { display: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DỮ LIỆU ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: str(x).strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: str(x).strip())
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

# --- 4. HỆ THỐNG MENU (SIDEBAR GIẤU KÍN) ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ CÀI ĐẶT HỆ THỐNG</div>', unsafe_allow_html=True)
    
    st.write("🌍 **NGÔN NGỮ**")
    lang = st.radio("Lang", ["VN", "EN"], horizontal=True, label_visibility="collapsed")
    
    st.divider()
    
    st.write("📊 **DỮ LIỆU TRA CỨU**")
    menu = st.selectbox("Chọn mục xem:", [
        "📊 Bảng KPI Tổng",
        "👤 Thông tin tài khoản",
        "⚠️ Tài khoản thiếu KPI",
        "🏔️ Top 15 Đèo 4",
        "🌋 Top 15 Đèo 7",
        "👑 Top 15 Kingland"
    ])
    
    st.divider()
    st.info(f"Admin: Louis\nPhiên bản v10.9")

# Thiết lập ngôn ngữ
texts = {
    "VN": {"search": "👤 Tìm kiếm...", "pow": "SỨC MẠNH", "tk": "TỔNG DIỆT", "td": "ĐIỂM CHẾT", "cols": ['Hạng', 'Thành viên', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']},
    "EN": {"search": "👤 Search...", "pow": "POWER", "tk": "TOTAL KILL", "td": "DEAD", "cols": ['Rank', 'Member', 'Power', 'Total Kill', 'Total Dead', 'Kill Inc', 'Dead Inc', 'KPI %']}
}
L = texts[lang]

# --- 5. HIỂN THỊ NỘI DUNG CHÍNH ---
if df is not None:
    st.markdown(f'<div class="logo-container"><img src="{LOGO_MAIN}" class="logo-img"></div>', unsafe_allow_html=True)

    # Xử lý Logic từng Menu
    display_df = df.copy()
    title_prefix = menu

    if menu == "⚠️ Tài khoản thiếu KPI":
        display_df = df[df['KPI_T'] < 50].sort_values(by='KPI_T') # Ví dụ dưới 50% là thiếu
    
    elif "Top 15" in menu:
        # Tạm thời lọc Top 15 theo KPI_T cao nhất, Louis có thể đổi cột lọc tại đây
        display_df = df.nlargest(15, 'KPI_T')
        
    # Giao diện tìm kiếm (Chỉ hiện ở bảng tổng và thông tin cá nhân)
    if menu in ["📊 Bảng KPI Tổng", "👤 Thông tin tài khoản"]:
        sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder=L['search'], label_visibility="collapsed")
        if sel and menu == "👤 Thông tin tài khoản":
            d = df[df['Tên_2'] == sel].iloc[0]
            # ... (Giữ nguyên logic Card Profile cũ của Louis tại đây)
            st.success(f"Đã chọn thành viên: {sel}")

    # Render Bảng dữ liệu chung cho tất cả mục
    st.subheader(f"📍 {menu}")
    
    df_sorted = display_df.sort_values(by='KillRank') if "Top" not in menu else display_df
    rows_list = []
    for _, r in df_sorted.iterrows():
        rows_list.append(f"""
        <tr>
            <td><span class="rank-badge">#{int(r['KillRank'])}</span></td>
            <td><b>{r['Tên_2']}</b><br><small style="color:#8b949e">ID: {r['ID']}</small></td>
            <td style="text-align:right">{int(r['Sức Mạnh_2']):,}</td>
            <td style="text-align:right; color:#00ffcc">{int(r['Tổng Tiêu Diệt_2']):,}</td>
            <td style="text-align:right; color:#ff4b4b">{int(r['Điểm Chết_2']):,}</td>
            <td style="text-align:right; color:#00d4ff">+{int(r['KI']):,}</td>
            <td style="text-align:right; color:#ff4b4b">+{int(r['DI']):,}</td>
            <td>
                <div class="kpi-bar-container"><div class="kpi-bar-fill" style="width:{min(r['KPI_T'], 100)}%"></div></div>
                <span style="color:#ffd700; font-weight:bold">{r['KPI_T']}%</span>
            </td>
        </tr>""")

    h = L['cols']
    table_html = f"""
    <div class="table-wrapper">
        <table class="elite-table">
            <thead><tr><th>{h[0]}</th><th>{h[1]}</th><th style="text-align:right">{h[2]}</th><th style="text-align:right">{h[3]}</th><th style="text-align:right">{h[4]}</th><th style="text-align:right">{h[5]}</th><th style="text-align:right">{h[6]}</th><th>{h[7]}</th></tr></thead>
            <tbody>{"".join(rows_list)}</tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown(f'<div class="footer">🛡️ Discord: louiss.nee | Zalo: 0.3.7.3.2.7.4.6.0.0</div>', unsafe_allow_html=True)
else:
    st.error("Lỗi kết nối dữ liệu Google Sheets.")
