import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. TỐI ƯU CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    
    /* Ép nội dung lên sát trên cùng */
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 5rem !important; 
        padding-left: 2rem !important; 
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    header { visibility: hidden; height: 0px !important; }
    
    /* Căn chỉnh tiêu đề chính */
    .main-header-container {
        text-align: center;
        margin-bottom: 10px;
    }
    .main-title {
        color: #00d4ff;
        font-size: 32px !important;
        font-weight: bold;
        text-shadow: 0px 0px 15px rgba(0,212,255,0.6);
        margin-bottom: 0px;
    }

    /* Đường kẻ chia phần sáng loáng */
    .hr-line {
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(0, 212, 255, 0), rgba(0, 212, 255, 0.75), rgba(0, 212, 255, 0));
        margin: 20px 0;
    }

    /* Footer cố định bên dưới */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(10, 20, 30, 0.95);
        color: #8b949e;
        text-align: center;
        padding: 10px;
        font-size: 13px;
        border-top: 1px solid #1a2a3a;
        z-index: 100;
    }
    .footer b { color: #00d4ff; }

    /* Fix Selectbox ẩn label */
    div[data-testid="stSelectbox"] label { display: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. QUẢN LÝ NGÔN NGỮ ---
texts = {
    "VN": {
        "header": "🛡️ HỆ THỐNG QUẢN TRỊ 3625", 
        "placeholder": "👤 Điền tên của bạn để tìm kiếm 🔍",
        "pow": "SỨC MẠNH", "tk": "TỔNG TIÊU DIỆT", "td": "ĐIỂM CHẾT", "rank": "HẠNG",
        "cols": ['Tên', 'ID', 'Liên minh', 'Hạng', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']
    },
    "EN": {
        "header": "🛡️ COMMAND CENTER 3625", 
        "placeholder": "👤 Search member name 🔍",
        "pow": "POWER", "tk": "TOTAL KILL", "td": "TOTAL DEAD", "rank": "RANK",
        "cols": ['Name', 'ID', 'Alliance', 'Rank', 'Power', 'Total Kill', 'Total Dead', 'Kill Inc', 'Dead Inc', 'KPI %']
    }
}

# --- 4. TẢI DỮ LIỆU ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        df = pd.merge(dt.drop_duplicates('ID'), ds.drop_duplicates('ID'), on='ID', suffixes=('_1', '_2'))
        # Xử lý ID và Tên
        df['ID'] = df['ID'].astype(str).str.replace('.0', '', regex=False)
        df['Tên_2'] = df['Tên_2'].fillna('Unknown').astype(str)
        # Tính toán KPI (giữ nguyên logic cũ của Louis)
        df['KI'] = pd.to_numeric(df['Tổng Tiêu Diệt_2'], errors='coerce').fillna(0) - pd.to_numeric(df['Tổng Tiêu Diệt_1'], errors='coerce').fillna(0)
        df['DI'] = pd.to_numeric(df['Điểm Chết_2'], errors='coerce').fillna(0) - pd.to_numeric(df['Điểm Chết_1'], errors='coerce').fillna(0)
        df['KillRank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').fillna(0).astype(int)
        df['KPI_T'] = 0.0 # Placeholder cho logic KPI thực tế
        return df
    except: return None

df = load_data()

# --- 5. BỐ CỤC HEADER ---
# Nút chuyển ngôn ngữ nằm góc trên bên phải
_, col_lang = st.columns([6, 1])
with col_lang:
    lang = st.radio("LANG:", ["VN", "EN"], horizontal=True, label_visibility="collapsed")
L = texts[lang]

# 1. Tiêu đề hệ thống nằm trên cùng
st.markdown(f"""
    <div class='main-header-container'>
        <p class='main-title'>{L['header']}</p>
    </div>
""", unsafe_allow_html=True)

# 2. Thanh tìm kiếm nằm ngay dưới tiêu đề
col_left, col_mid, col_right = st.columns([1.5, 3, 1.5])
with col_mid:
    sel = st.selectbox("", sorted(df['Tên_2'].unique()) if df is not None else [], index=None, placeholder=L["placeholder"])

# 3. Đường kẻ chia phần (Header Line)
st.markdown("<div class='hr-line'></div>", unsafe_allow_html=True)

# --- 6. HIỂN THỊ NỘI DUNG ---
if df is not None:
    if sel:
        # Hiển thị Profile Member (Giữ thiết kế Card đẹp mắt của Louis)
        d = df[df['Tên_2'] == sel].iloc[0]
        html_card = f"""
        <div style="position: relative; width: 100%; margin: 50px auto 10px; font-family: 'Segoe UI', sans-serif;">
            <div style="position: absolute; top: -45px; left: 50%; transform: translateX(-50%); 
                        background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; 
                        padding: 10px 70px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700;">
                <div style="color: #00d4ff; font-size: 13px; font-weight: 900;">PROFILE MEMBER</div>
                <div style="color: #ffffff; font-size: 28px; font-weight: bold;">{sel}</div>
                <div style="color: #8b949e; font-size: 11px;">ID: {d['ID']}</div>
            </div>
            <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 70px 20px 20px 20px;">
                <div style="display: flex; justify-content: space-around; text-align: center;">
                    <div><div style="color:#8b949e; font-size:10px;">{L['pow']}</div><div style="font-size:20px; font-weight:900;">{int(d['Sức Mạnh_2']):,}</div></div>
                    <div><div style="color:#8b949e; font-size:10px;">{L['tk']}</div><div style="font-size:20px; font-weight:900;">{int(d['Tổng Tiêu Diệt_2']):,}</div></div>
                    <div><div style="color:#ff4b4b; font-size:10px;">{L['td']}</div><div style="font-size:20px; font-weight:900; color:#ff4b4b;">{int(d['Điểm Chết_2']):,}</div></div>
                </div>
            </div>
        </div>
        """
        components.html(html_card, height=300)
    
    # Bảng dữ liệu chính
    st.dataframe(df[['Tên_2', 'ID', 'Liên Minh_2', 'KillRank', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'KPI_T']], 
                 use_container_width=True, hide_index=True, height=500)

# --- 7. FOOTER LIÊN HỆ ---
st.markdown(f"""
    <div class='footer'>
        🛡️ Liên hệ hỗ trợ: Discord: <b>louiss.nee</b> | Zalo: <b>0.3.7.3.2.7.4.6.0.0</b>
    </div>
""", unsafe_allow_html=True)
