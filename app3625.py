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

# --- 2. SIÊU CSS (Tạo hiệu ứng bảng trượt từ trái) ---
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

    /* Hiệu ứng Bảng trượt từ trái */
    .slide-in-panel {
        background: linear-gradient(135deg, rgba(13, 27, 42, 0.95), rgba(5, 10, 14, 0.98));
        border: 1px solid #00d4ff;
        border-left: 5px solid #00d4ff;
        border-radius: 0 15px 15px 0;
        padding: 20px;
        animation: slideIn 0.4s ease-out;
        box-shadow: 10px 0px 30px rgba(0, 212, 255, 0.2);
        max-width: 350px;
        margin-bottom: 25px;
    }

    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    .settings-title { color: #00d4ff; font-weight: 900; letter-spacing: 1px; border-bottom: 1px solid #1e3a5a; padding-bottom: 10px; margin-bottom: 15px; font-size: 14px; }
    .settings-item { padding: 10px 0; color: #e0e6ed; font-size: 14px; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; align-items: center; gap: 10px; }
    .settings-item:hover { color: #00d4ff; }

    /* Bảng dữ liệu */
    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 20px; }
    .elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
    .elite-table thead th { background: rgba(0, 212, 255, 0.1); color: #00d4ff; text-align: left; padding: 15px; font-size: 16px; border-bottom: 3px solid #00d4ff; }
    .elite-table td { padding: 14px 15px; font-size: 16px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; }
    
    .rank-badge { background: #ffd700; color: #000; padding: 4px 10px; border-radius: 6px; font-weight: 900; font-size: 14px; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: rgba(5, 10, 14, 0.95); color: #8b949e; padding: 10px; font-size: 13px; text-align: center; border-top: 1px solid #1a2a3a; z-index: 999; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Giữ nguyên) ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">🛡️ COMMAND CENTER</div>', unsafe_allow_html=True)
    lang = st.radio("Chon ngon ngu", ["VN", "EN"], horizontal=True, label_visibility="collapsed")
    st.divider()
    menu = st.radio("Chon menu", ["📊 Bảng KPI", "👤 Tài khoản", "⚙️ Quản lý KPI"], label_visibility="collapsed")
    st.divider()
    st.info("Phiên bản v10.9 - Admin Louis")

# --- 4. DỮ LIỆU ---
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
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        df['KillRank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)
        
        def get_m(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 200e6
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = max(0.0, float(r['KI']) / gk) if gk > 0 else 0.0
            pdv = max(0.0, float(r['DI']) / gd) if gd > 0 else 0.0
            return pd.Series([round(pk * 100, 1), round(pdv * 100, 1), round(((pk + pdv) / 2) * 100, 1)])
        df[['KPI_K', 'KPI_D', 'KPI_T']] = df.apply(get_m, axis=1)
        return df
    except: return None

df = load_data()
L = {"VN": {"search": "👤 Tìm kiếm thành viên...", "cols": ['Hạng', 'Thành viên', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']}, "EN": {"search": "👤 Search...", "cols": ['Rank', 'Member', 'Power', 'Total Kill', 'Total Dead', 'Kill Inc', 'Dead Inc', 'KPI %']}}[lang]

# --- 5. HIỂN THỊ ---
if df is not None:
    st.markdown(f'<div class="logo-container"><img src="{LOGO_MAIN}" class="logo-img"></div>', unsafe_allow_html=True)

    # NÚT CÀI ĐẶT GÓC TRÁI
    col_btn, col_empty = st.columns([0.05, 0.95])
    with col_btn:
        open_panel = st.checkbox("⚙️", help="Mở bảng thông tin")

    # KHI CLICK: ĐẨY BẢNG TỪ TRÁI RA
    if open_panel:
        st.markdown("""
            <div class="slide-in-panel">
                <div class="settings-title">🛡️ THÔNG TIN HỆ THỐNG</div>
                <div class="settings-item">⚠️ Tài khoản thiếu KPI</div>
                <div class="settings-item">🏔️ Top 15 Đèo 4</div>
                <div class="settings-item">🌋 Top 15 Đèo 7</div>
                <div class="settings-item">👑 Top 15 Kingland</div>
                <div class="settings-item">📅 Phiên bản: v10.9</div>
            </div>
        """, unsafe_allow_html=True)

    # NỘI DUNG CHÍNH (Bảng KPI)
    if menu == "📊 Bảng KPI":
        sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder=L['search'], label_visibility="collapsed")
        
        # Table Render
        df_sorted = df.sort_values(by='KillRank')
        rows = "".join([f"<tr><td><span class='rank-badge'>#{int(r['KillRank'])}</span></td><td><b>{r['Tên_2']}</b><br><small>ID: {r['ID']}</small></td><td style='text-align:right'>{int(r['Sức Mạnh_2']):,}</td><td style='text-align:right; color:#00ffcc'>{int(r['Tổng Tiêu Diệt_2']):,}</td><td style='text-align:right; color:#ff4b4b'>{int(r['Điểm Chết_2']):,}</td><td style='text-align:right; color:#00d4ff'>+{int(r['KI']):,}</td><td style='text-align:right; color:#ff4b4b'>+{int(r['DI']):,}</td><td><span style='color:#ffd700'>{r['KPI_T']}%</span></td></tr>" for _, r in df_sorted.iterrows()])
        
        st.markdown(f'<div class="table-wrapper"><table class="elite-table"><thead><tr><th>Hạng</th><th>Thành viên</th><th style="text-align:right">Sức mạnh</th><th style="text-align:right">Tổng Kill</th><th style="text-align:right">Điểm Chết</th><th style="text-align:right">Kill +</th><th style="text-align:right">Dead +</th><th>KPI %</th></tr></thead><tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="footer">🛡️ Discord: louiss.nee | Zalo: 0.3.7.3.2.7.4.6.0.0</div>', unsafe_allow_html=True)
else:
    st.error("Lỗi kết nối dữ liệu.")
