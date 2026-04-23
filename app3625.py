import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | ELITE COMMAND", layout="wide")

# Link các ảnh
LOGO_MAIN = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true" 
LOGO_PROFILE = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true"

# --- 2. SIÊU CSS (GIAO DIỆN ELITE) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .block-container { padding-top: 0.5rem !important; max-width: 98% !important; }
    header { visibility: hidden; height: 0px !important; }

    /* Sidebar thiết kế lại */
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    
    /* Logo & Slogan trung tâm */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 25px;
    }
    .logo-img { width: 220px; filter: drop-shadow(0px 0px 10px rgba(0, 212, 255, 0.4)); }
    .slogan {
        color: #00d4ff;
        font-size: 16px;
        font-weight: bold;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }

    /* Thanh tìm kiếm sát bảng */
    div[data-testid="stSelectbox"] {
        max-width: 350px !important;
        margin-bottom: -15px;
    }

    /* BẢNG ELITE HTML/CSS */
    .elite-table-container {
        background: rgba(13, 27, 42, 0.9);
        border: 1px solid #1e3a5a;
        border-radius: 12px;
        padding: 5px;
        margin-top: 10px;
    }
    table.elite-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Segoe UI', sans-serif;
    }
    .elite-table thead {
        background: linear-gradient(90deg, #162a3e 0%, #1c3d5a 100%);
        border-bottom: 2px solid #00d4ff;
    }
    .elite-table th {
        padding: 12px;
        text-align: left;
        font-size: 12px;
        color: #00d4ff;
        text-transform: uppercase;
    }
    .elite-table tr { border-bottom: 1px solid #1a2a3a; transition: 0.2s; }
    .elite-table tr:hover { background: rgba(0, 212, 255, 0.05); }
    .elite-table td { padding: 10px 12px; font-size: 14px; }
    
    .val-power { color: #ffffff; font-weight: bold; }
    .val-kill { color: #00ffcc; font-weight: bold; }
    .val-dead { color: #ff4b4b; font-weight: bold; }
    .badge-rank {
        background: #ffd700; color: #000;
        padding: 1px 6px; border-radius: 4px; font-weight: 900; font-size: 12px;
    }

    /* Thanh KPI năng lượng */
    .kpi-bar-bg {
        width: 80px; height: 6px;
        background: #1a2a3a; border-radius: 3px;
        display: inline-block; vertical-align: middle; margin-right: 8px;
    }
    .kpi-bar-fill {
        height: 100%; background: linear-gradient(90deg, #00d4ff, #00ffcc);
        box-shadow: 0 0 8px #00d4ff; border-radius: 3px;
    }

    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: rgba(5, 10, 14, 0.95); color: #8b949e;
        padding: 8px; font-size: 12px; text-align: center;
        border-top: 1px solid #1a2a3a; z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (TAB TRÁI) ---
with st.sidebar:
    st.markdown("<h3 style='color:#ffd700; text-align:center;'>DASHBOARD</h3>", unsafe_allow_html=True)
    lang = st.radio("LANGUAGE / NGÔN NGỮ", ["VN", "EN"], horizontal=True)
    st.divider()
    st.info("Hệ thống tự động cập nhật dữ liệu từ Google Sheets mỗi 30 giây.")

# --- 4. DATA LOGIC (GIỮ NGUYÊN TỪ BẢN CŨ) ---
texts = {
    "VN": {
        "search": "🔍 Tìm chiến binh...",
        "slogan": "Chào mừng đến trang web quản lý KPI 3625",
        "header_cols": ["HẠNG", "CHIẾN BINH", "SỨC MẠNH", "TỔNG KILL", "ĐIỂM CHẾT", "TRẠNG THÁI KPI"]
    },
    "EN": {
        "search": "🔍 Search warrior...",
        "slogan": "Welcome to 3625 KPI Command Center",
        "header_cols": ["RANK", "WARRIOR", "POWER", "TOTAL KILL", "DEAD POINTS", "KPI STATUS"]
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
        return df.sort_values(by='KillRank')
    except: return None

df = load_data()

# --- 5. HIỂN THỊ GIAO DIỆN ---
if df is not None:
    # Header trung tâm
    st.markdown(f"""
        <div class="header-container">
            <img src="{LOGO_MAIN}" class="logo-img">
            <div class="slogan">{L['slogan']}</div>
        </div>
    """, unsafe_allow_html=True)

    # Tìm kiếm bên trái
    sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder=L['search'], label_visibility="collapsed")

    # Hiển thị Profile Card (HTML từ bản cũ)
    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        html_card = f"""
        <div style="position: relative; width: 100%; margin: 60px auto 30px; font-family: 'Segoe UI', sans-serif;">
            <div style="position: absolute; top: -50px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 12px 40px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; min-width: 450px;">
                <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
                    <img src="{LOGO_PROFILE}" style="width: 50px; height: 50px;">
                    <div style="color: #ffffff; font-size: 28px; font-weight: bold;">{sel}</div>
                </div>
            </div>
            <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 60px 20px 20px 20px; text-align:center;">
                <h3 style="color:#ffd700;">KPI TOTAL: {d['KPI_T']}%</h3>
            </div>
        </div>
        """
        components.html(html_card, height=250)

    # BẢNG ELITE TÙY CHỈNH
    h = L['header_cols']
    table_html = f"""
    <div class="elite-table-container">
        <table class="elite-table">
            <thead>
                <tr>
                    <th>{h[0]}</th><th>{h[1]}</th><th>{h[2]}</th><th>{h[3]}</th><th>{h[4]}</th><th>{h[5]}</th>
                </tr>
            </thead>
            <tbody>
    """

    for _, r in df.iterrows():
        kpi = r['KPI_T']
        table_html += f"""
            <tr>
                <td><span class="badge-rank">#{int(r['KillRank'])}</span></td>
                <td><b>{r['Tên_2']}</b><br><small style="color:#8b949e">ID: {r['ID']}</small></td>
                <td class="val-power">{int(r['Sức Mạnh_2']):,}</td>
                <td class="val-kill">{int(r['Tổng Tiêu Diệt_2']):,}</td>
                <td class="val-dead">{int(r['Điểm Chết_2']):,}</td>
                <td>
                    <div class="kpi-bar-bg"><div class="kpi-bar-fill" style="width: {min(kpi, 100)}%;"></div></div>
                    <span style="color:#00ffcc; font-weight:bold;">{kpi}%</span>
                </td>
            </tr>
        """
    
    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

    # Footer
    st.markdown(f'<div class="footer">🛡️ Discord: <b>louiss.nee</b> | Zalo: <b>0.3.7.3.2.7.4.6.0.0</b></div>', unsafe_allow_html=True)
else:
    st.error("⚠️ Lỗi kết nối dữ liệu Google Sheets!")
