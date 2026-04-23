import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# Link các ảnh
LOGO_MAIN = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true" 
LOGO_PROFILE = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true"

# --- 2. SIÊU CSS (Tối ưu nhẹ hơn) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .block-container { padding-top: 0.5rem !important; max-width: 98% !important; }
    header { visibility: hidden; height: 0px !important; }

    .logo-container { display: flex; flex-direction: column; align-items: center; margin-bottom: 20px; }
    .logo-img { width: 220px; filter: drop-shadow(0px 0px 10px rgba(0, 212, 255, 0.4)); }
    .slogan { color: #00d4ff; font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }

    /* Bảng Elite gọn nhẹ hơn */
    .elite-table-container { background: rgba(13, 27, 42, 0.9); border: 1px solid #1e3a5a; border-radius: 12px; padding: 5px; overflow-x: auto; }
    table.elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; min-width: 900px; }
    .elite-table thead { background: #162a3e; border-bottom: 2px solid #00d4ff; }
    .elite-table th { padding: 10px; text-align: left; font-size: 11px; color: #00d4ff; }
    .elite-table tr { border-bottom: 1px solid #1a2a3a; }
    .elite-table tr:hover { background: rgba(0, 212, 255, 0.05); }
    .elite-table td { padding: 8px 10px; font-size: 13px; }
    
    .badge-rank { background: #ffd700; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: 900; font-size: 11px; }
    .kpi-bar-bg { width: 50px; height: 5px; background: #1a2a3a; border-radius: 3px; display: inline-block; vertical-align: middle; margin-right: 5px; }
    .kpi-bar-fill { height: 100%; background: #00d4ff; border-radius: 3px; }

    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #5c6b7a; padding: 5px; font-size: 11px; text-align: center; border-top: 1px solid #1a2a3a; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ĐIỀU KHIỂN NGÔN NGỮ ---
col_space, col_lang = st.columns([8, 1.5])
with col_lang:
    lang = st.radio("", ["VN", "EN"], horizontal=True, label_visibility="collapsed")

# --- 4. DỮ LIỆU (Giữ nguyên logic của Louis) ---
texts = {
    "VN": { "search": "🔍 Tìm chiến binh...", "slogan": "QUẢN LÝ KPI KINGDOM 3625", "h": ["Hạng", "Thành viên", "Sức mạnh", "Tổng Kill", "Điểm Chết", "Kill+", "Dead+", "KPI%"] },
    "EN": { "search": "🔍 Search member...", "slogan": "3625 KPI MANAGEMENT", "h": ["Rank", "Member", "Power", "Total Kill", "Total Dead", "Kill+", "Dead+", "KPI%"] }
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

# --- 5. GIAO DIỆN ---
if df is not None:
    st.markdown(f'<div class="logo-container"><img src="{LOGO_MAIN}" class="logo-img"><div class="slogan">{L["slogan"]}</div></div>', unsafe_allow_html=True)

    # Sidebar điều hướng phân trang để giảm tải
    st.sidebar.title("💎 DANH SÁCH")
    items_per_page = 25
    total_pages = (len(df) // items_per_page) + 1
    page = st.sidebar.number_input("Trang", min_value=1, max_value=total_pages, step=1)
    
    # Search
    sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder=L['search'], label_visibility="collapsed")

    if sel:
        # Giữ nguyên phần Card Profile của bạn (không thay đổi logic)
        d = df[df['Tên_2'] == sel].iloc[0]
        # (Phần code html_card giữ nguyên như bản cũ của bạn...)
        st.info(f"Đang xem chi tiết chiến binh: {sel}") # Thay tạm bằng info để tránh dài code

    # HIỂN THỊ BẢNG (CHỈ RENDER THEO TRANG)
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_df = df.iloc[start_idx:end_idx]

    h = L['h']
    rows_html = ""
    for _, r in page_df.iterrows():
        kpi = r['KPI_T']
        rows_html += f"""
            <tr>
                <td><span class="badge-rank">#{int(r['KillRank'])}</span></td>
                <td><b>{r['Tên_2']}</b></td>
                <td>{int(r['Sức Mạnh_2']):,}</td>
                <td>{int(r['Tổng Tiêu Diệt_2']):,}</td>
                <td style="color:#ff4b4b">{int(r['Điểm Chết_2']):,}</td>
                <td style="color:#00ffff">{r['KPI_K']}%</td>
                <td style="color:#ff4b4b">{r['KPI_D']}%</td>
                <td>
                    <div class="kpi-bar-bg"><div class="kpi-bar-fill" style="width: {min(kpi, 100)}%;"></div></div>
                    <span style="color:#00ffcc; font-weight:bold;">{kpi}%</span>
                </td>
            </tr>
        """

    st.markdown(f"""
    <div class="elite-table-container">
        <table class="elite-table">
            <thead><tr><th>{h[0]}</th><th>{h[1]}</th><th>{h[2]}</th><th>{h[3]}</th><th>{h[4]}</th><th>{h[5]}</th><th>{h[6]}</th><th>{h[7]}</th></tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="footer">🛡️ Admin: Louis | Trang {page}/{total_pages}</div>', unsafe_allow_html=True)
else:
    st.error("⚠️ Lỗi dữ liệu!")
