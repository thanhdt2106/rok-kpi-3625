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

    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    
    .header-container { display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 25px; }
    .logo-img { width: 220px; filter: drop-shadow(0px 0px 10px rgba(0, 212, 255, 0.4)); }
    .slogan { color: #00d4ff; font-size: 16px; font-weight: bold; margin-top: 8px; text-transform: uppercase; letter-spacing: 1.5px; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5); }

    div[data-testid="stSelectbox"] { max-width: 350px !important; margin-bottom: -15px; }

    /* BẢNG ELITE */
    .elite-table-container { background: rgba(13, 27, 42, 0.9); border: 1px solid #1e3a5a; border-radius: 12px; padding: 5px; margin-top: 10px; overflow-x: auto; }
    table.elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; min-width: 1000px; }
    .elite-table thead { background: linear-gradient(90deg, #162a3e 0%, #1c3d5a 100%); border-bottom: 2px solid #00d4ff; }
    .elite-table th { padding: 12px; text-align: left; font-size: 11px; color: #00d4ff; text-transform: uppercase; }
    .elite-table tr { border-bottom: 1px solid #1a2a3a; transition: 0.2s; }
    .elite-table tr:hover { background: rgba(0, 212, 255, 0.08); }
    .elite-table td { padding: 12px; font-size: 14px; }
    
    .val-power { color: #ffffff; font-weight: bold; }
    .val-kill { color: #00ffcc; font-weight: bold; }
    .val-dead { color: #ff4b4b; font-weight: bold; }
    .badge-rank { background: #ffd700; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 900; font-size: 12px; }

    .kpi-bar-bg { width: 60px; height: 6px; background: #1a2a3a; border-radius: 3px; display: inline-block; vertical-align: middle; margin-right: 8px; }
    .kpi-bar-fill { height: 100%; background: linear-gradient(90deg, #00d4ff, #00ffcc); box-shadow: 0 0 8px #00d4ff; border-radius: 3px; }

    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: rgba(5, 10, 14, 0.95); color: #8b949e; padding: 8px; font-size: 12px; text-align: center; border-top: 1px solid #1a2a3a; z-index: 999; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h3 style='color:#ffd700; text-align:center;'>BẢNG ĐIỀU KHIỂN</h3>", unsafe_allow_html=True)
    lang = st.radio("NGÔN NGỮ", ["VN", "EN"], horizontal=True)
    st.divider()

# --- 4. DATA PROCESSING (SỬA LỖI TRUY XUẤT) ---
texts = {
    "VN": { "search": "🔍 Tìm chiến binh...", "slogan": "Hệ thống quản trị KPI 3625", "h": ["Hạng", "Chiến binh", "Sức mạnh", "Tổng Kill", "Điểm chết", "KPI Kill", "KPI Dead", "Tổng KPI"] },
    "EN": { "search": "🔍 Search warrior...", "slogan": "3625 KPI Command Center", "h": ["Rank", "Warrior", "Power", "Total Kill", "Dead Points", "KPI Kill", "KPI Dead", "Total KPI"] }
}
L = texts[lang]

SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_and_clean_data():
    try:
        # Load data
        dt = pd.read_csv(URL_T)
        ds = pd.read_csv(URL_S)
        
        # Chuẩn hóa tên cột ngay lập tức để tránh lỗi KeyError
        dt.columns = dt.columns.str.strip()
        ds.columns = ds.columns.str.strip()

        # Merge dữ liệu dựa trên ID
        df = pd.merge(dt, ds, on='ID', suffixes=('_1', '_2'))
        
        # Ép kiểu dữ liệu số an toàn (Loại bỏ dấu phẩy, khoảng trắng)
        cols_to_fix = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for col in cols_to_fix:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        # Tính toán KPI
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        df['Rank_Num'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)
        
        def calc_kpi(row):
            p = row['Sức Mạnh_2']
            target_k = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 200e6
            target_d = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            k_k = round(max(0.0, float(row['KI']) / target_k) * 100, 1) if target_k > 0 else 0.0
            k_d = round(max(0.0, float(row['DI']) / target_d) * 100, 1) if target_d > 0 else 0.0
            return pd.Series([k_k, k_d, round((k_k + k_d) / 2, 1)])
            
        df[['KPI_K', 'KPI_D', 'KPI_T']] = df.apply(calc_kpi, axis=1)
        return df.sort_values(by='Rank_Num')
    except Exception as e:
        st.error(f"Lỗi dữ liệu: {e}")
        return None

df = load_and_clean_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    st.markdown(f'<div class="header-container"><img src="{LOGO_MAIN}" class="logo-img"><div class="slogan">{L["slogan"]}</div></div>', unsafe_allow_html=True)

    # Search (Tìm kiếm theo Tên_2)
    names = sorted(df['Tên_2'].dropna().unique())
    sel = st.selectbox("", names, index=None, placeholder=L['search'], label_visibility="collapsed")

    # Bảng Elite
    h = L['h']
    rows_html = ""
    for _, r in df.iterrows():
        # Chuẩn bị dữ liệu hiển thị an toàn
        name = str(r['Tên_2'])
        uid = str(r['ID']).split('.')[0]
        power = f"{int(r['Sức Mạnh_2']):,}"
        tkill = f"{int(r['Tổng Tiêu Diệt_2']):,}"
        tdead = f"{int(r['Điểm Chết_2']):,}"
        k_k = f"{r['KPI_K']}%"
        k_d = f"{r['KPI_D']}%"
        k_t = f"{r['KPI_T']}%"
        rank = int(r['Rank_Num'])
        
        rows_html += f"""
            <tr>
                <td><span class="badge-rank">#{rank}</span></td>
                <td><b>{name}</b><br><small style="color:#8b949e">ID: {uid}</small></td>
                <td class="val-power">{power}</td>
                <td class="val-kill">{tkill}</td>
                <td class="val-dead">{tdead}</td>
                <td style="color:#00ffff">{k_k}</td>
                <td style="color:#ff4b4b">{k_d}</td>
                <td>
                    <div class="kpi-bar-bg"><div class="kpi-bar-fill" style="width: {min(float(r['KPI_T']), 100)}%;"></div></div>
                    <span style="color:#00ffcc; font-weight:bold;">{k_t}</span>
                </td>
            </tr>
        """

    full_table = f"""
    <div class="elite-table-container">
        <table class="elite-table">
            <thead><tr><th>{h[0]}</th><th>{h[1]}</th><th>{h[2]}</th><th>{h[3]}</th><th>{h[4]}</th><th>{h[5]}</th><th>{h[6]}</th><th>{h[7]}</th></tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """
    st.markdown(full_table, unsafe_allow_html=True)

    st.markdown(f'<div class="footer">🛡️ Discord: <b>louiss.nee</b> | Zalo: <b>0.3.7.3.2.7.4.6.0.0</b></div>', unsafe_allow_html=True)
