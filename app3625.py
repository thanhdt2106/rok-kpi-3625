import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CONFIG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS ÉP THẲNG HÀNG 1 DÒNG ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    #MainMenu, header, footer, [data-testid="stSidebar"] { visibility: hidden; display: none; }

    .main .block-container {
        max-width: 98% !important;
        padding-top: 65px !important; 
    }

    /* THANH TASKBAR 1 DÒNG DUY NHẤT */
    .custom-header {
        position: fixed; top: 0; left: 0; width: 100%; height: 60px;
        background: rgba(13, 27, 42, 0.98);
        border-bottom: 2px solid #00d4ff;
        display: flex; align-items: center; padding: 0 20px; z-index: 999999;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }

    /* Style cho logo & text trái */
    .header-left { display: flex; align-items: center; gap: 8px; white-space: nowrap; }
    .header-logo { width: 30px; filter: drop-shadow(0 0 5px #00d4ff); }
    .header-title { font-weight: 900; font-size: 14px; color: #fff; text-shadow: 0 0 8px #00d4ff; }

    /* Fix Streamlit Columns để không bị lệch */
    div[data-testid="stHorizontalBlock"] { align-items: center !important; gap: 0.5rem !important; }
    
    /* Table & Card Style */
    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 15px; margin-top: 20px; }
    .elite-table { width: 100%; border-collapse: collapse; text-align: center; }
    .elite-table th { background: rgba(0, 212, 255, 0.1); color: #00d4ff; padding: 12px; border-bottom: 2px solid #00d4ff; font-size: 13px; }
    .elite-table td { padding: 10px; border-bottom: 1px solid #1a2a3a; font-size: 13px; }
    .rank-badge { background: linear-gradient(135deg, #ffd700, #b8860b); color: #000; padding: 3px 8px; border-radius: 4px; font-weight: 900; }

    /* Drawer */
    #myDrawer {
        height: 100%; width: 0; position: fixed; z-index: 1000001;
        top: 0; right: 0; background-color: rgba(13, 27, 42, 0.98);
        transition: 0.5s; padding-top: 60px; border-left: 2px solid #00d4ff;
    }
    #myDrawer a { padding: 15px 25px; text-decoration: none; font-size: 14px; color: #e0e6ed; display: block; border-bottom: 1px solid rgba(0,212,255,0.05); }
    </style>

    <div id="myDrawer">
      <a href="javascript:void(0)" style="font-size:30px; color:#ff4b4b" onclick="closeNav()">&times;</a>
      <div style="color: #00d4ff; font-weight: bold; padding: 0 25px 20px;">⚙️ SETTINGS</div>
      <a>⚠️ Missing KPI</a>
      <a>🏔️ Pass 4 Stats</a>
      <a>🌋 Pass 7 Stats</a>
    </div>

    <script>
    function openNav() { document.getElementById("myDrawer").style.width = "280px"; }
    function closeNav() { document.getElementById("myDrawer").style.width = "0"; }
    </script>
    """, unsafe_allow_html=True)

# --- 3. DATA LOADING ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        df = pd.merge(dt, ds, on='ID', suffixes=('_1', '_2'))
        # Logic tính toán rút gọn
        df['KI'] = pd.to_numeric(df['Tổng Tiêu Diệt_2'], errors='coerce').fillna(0) - pd.to_numeric(df['Tổng Tiêu Diệt_1'], errors='coerce').fillna(0)
        df['DI'] = pd.to_numeric(df['Điểm Chết_2'], errors='coerce').fillna(0) - pd.to_numeric(df['Điểm Chết_1'], errors='coerce').fillna(0)
        df['KPI_T'] = 0.0 # Giữ logic của bạn
        df['Rank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)
        return df
    except: return None

df = load_data()

# --- 4. TASKBAR CĂN CHỈNH THẲNG HÀNG ---
if df is not None:
    st.markdown('<div class="custom-header">', unsafe_allow_html=True)
    
    # Chia 3 khu vực trên cùng 1 hàng
    c1, c2, c3 = st.columns([1, 2, 1.2])

    with c1:
        st.markdown("""
            <div class="header-left">
                <img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true" class="header-logo">
                <span class="header-title">FIGHT TO DEAD 3625</span>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        sel = st.selectbox("", sorted(df['Tên_2'].dropna().unique()), index=None, placeholder="👤 Tìm kiếm thành viên...", label_visibility="collapsed")

    with c3:
        r_c1, r_c2, r_c3 = st.columns([1.2, 0.8, 0.8])
        with r_c1: lang = st.selectbox("", ["VN", "EN"], label_visibility="collapsed")
        with r_c2: st.button("👤", use_container_width=True)
        with r_c3:
            components.html("""<button onclick="parent.openNav()" style="background:transparent; border:1px solid #00d4ff; color:#00d4ff; width:100%; height:30px; border-radius:5px; cursor:pointer;">⚙️</button>""", height=35)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 5. HIỂN THỊ NỘI DUNG (TABLE & CARD) ---
    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        # Card profile rút gọn để khớp giao diện
        st.info(f"Đang xem Profile của: {sel} - ID: {d['ID']}")

    # Bảng dữ liệu
    st.markdown('<div class="table-wrapper">', unsafe_allow_html=True)
    st.dataframe(df[['Rank', 'Tên_2', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'KI', 'DI']], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error("Lỗi dữ liệu! Hãy tạo file requirements.txt trên GitHub để sửa lỗi Module.")
