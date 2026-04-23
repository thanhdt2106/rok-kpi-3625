import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# Link các ảnh
LOGO_MAIN = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true"
LOGO_PROFILE = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true"

# --- 2. SIÊU CSS (Tối ưu vị trí các thành phần) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .block-container { padding-top: 0.5rem !important; max-width: 98% !important; }
    header { visibility: hidden; height: 0px !important; }

    /* Logo & Slogan giữa màn hình */
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .logo-img { 
        width: 250px; 
        filter: drop-shadow(0px 0px 10px rgba(0, 212, 255, 0.4));
    }
    .slogan {
        color: #00d4ff;
        font-size: 16px;
        font-weight: bold;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Đưa phần chọn ngôn ngữ lên góc phải màn hình */
    .lang-wrapper {
        display: flex;
        justify-content: flex-end;
        padding-right: 20px;
        margin-bottom: -30px;
    }

    /* Thanh tìm kiếm sát bảng bên trái */
    div[data-testid="stSelectbox"] {
        max-width: 350px !important;
        margin-bottom: 10px;
    }

    [data-testid="stDataFrame"] { 
        background: #0d1b2a; 
        border-radius: 10px; 
        border: 1px solid #00d4ff; 
    }

    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: rgba(5, 10, 14, 0.95); color: #8b949e;
        padding: 8px; font-size: 12px; text-align: center;
        border-top: 1px solid #1a2a3a; z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ĐIỀU KHIỂN NGÔN NGỮ (Góc phải) ---
st.markdown('<div class="lang-wrapper">', unsafe_allow_html=True)
lang = st.radio("", ["VN", "EN"], horizontal=True, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. DỮ LIỆU ---
texts = {
    "VN": {
        "search": "👤 Tìm kiếm thành viên...",
        "pow": "SỨC MẠNH", "tk": "TỔNG TIÊU DIỆT", "td": "ĐIỂM CHẾT", "rank": "HẠNG",
        "slogan": "Chào mừng đến trang web quản lý KPI 3625",
        "cols": ['Tên', 'ID', 'Liên minh', 'Hạng', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']
    },
    "EN": {
        "search": "👤 Search member name...",
        "pow": "POWER", "tk": "TOTAL KILL", "td": "TOTAL DEAD", "rank": "RANK",
        "slogan": "Welcome to the 3625 KPI Management Website",
        "cols": ['Name', 'ID', 'Alliance', 'Rank', 'Power', 'Total Kill', 'Total Dead', 'Kill Inc', 'Dead Inc', 'KPI %']
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
    except: return None

df = load_data()

# --- 5. GIAO DIỆN CHÍNH ---
if df is not None:
    # Logo & Slogan
    st.markdown(f"""
        <div class="logo-container">
            <img src="{LOGO_MAIN}" class="logo-img">
            <div class="slogan">{L['slogan']}</div>
        </div>
    """, unsafe_allow_html=True)

    # Thanh tìm kiếm
    sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder=L['search'], label_visibility="collapsed")

    # Hiển thị Card Profile
    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        html_card = f"""
        <div style="position: relative; width: 100%; margin: 60px auto 10px; font-family: 'Segoe UI', sans-serif;">
            <div style="position: absolute; top: -50px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 12px 40px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; box-shadow: 0 8px 25px rgba(0,0,0,0.8); min-width: 450px;">
                <div style="color: #00d4ff; font-size: 11px; font-weight: 900; letter-spacing: 2px; margin-bottom: 5px;">PROFILE MEMBER</div>
                <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
                    <img src="{LOGO_PROFILE}" style="width: 50px; height: 50px; object-fit: contain;">
                    <div style="color: #ffffff; font-size: 28px; font-weight: bold; text-shadow: 0 0 10px #00d4ff;">{sel}</div>
                </div>
                <div style="font-size: 13px; margin-top: 8px; color: #fff;">
                    <b>ID:</b> {d['ID']} | <b>ALLIANCE:</b> {d['Liên Minh_2']}
                </div>
            </div>
            <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 85px 20px 20px 20px;">
                <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 25px;">
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3.5px solid #00d4ff;">
                        <div style="font-size: 10px; color: #8b949e;">{L['pow']}</div>
                        <div style="font-size: 22px; font-weight: 900;">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3.5px solid #00ffcc;">
                        <div style="font-size: 10px; color: #8b949e;">{L['tk']}</div>
                        <div style="font-size: 22px; font-weight: 900;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3.5px solid #ff4b4b;">
                        <div style="font-size: 10px; color: #ff4b4b;">{L['td']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 0.6; text-align: center; border-bottom: 3.5px solid #ffd700;">
                        <div style="font-size: 10px; color: #ffd700;">{L['rank']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #ffd700;">#{d['KillRank']}</div>
                    </div>
                </div>
                <div style="background: #1a2a3a; border-radius: 15px; padding: 25px; display: flex; justify-content: space-around; align-items: center;">
                    <div style="text-align: center;"><div style="font-size: 24px; color: #ffd700; font-weight: 900;">{d['KPI_T']}%</div><div style="font-size: 12px; color: #8b949e;">TOTAL KPI</div></div>
                </div>
            </div>
        </div>
        """
        components.html(html_card, height=480)

    # Bảng số liệu chính
    display_df = df[['Tên_2', 'ID', 'Liên Minh_2', 'KillRank', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'KI', 'DI', 'KPI_T']].copy()
    display_df.columns = L['cols']
    
    # Định dạng số có dấu phẩy cho dễ đọc
    for col in L['cols'][4:9]:
        display_df[col] = display_df[col].apply(lambda x: f"{int(x):,}")
    display_df[L['cols'][9]] = display_df[L['cols'][9]].apply(lambda x: f"{x}%")

    st.dataframe(display_df.sort_values(by=L['cols'][3]), use_container_width=True, hide_index=True, height=600)

    st.markdown(f'<div class="footer">🛡️ Discord: <b>louiss.nee</b> | Zalo: <b>0.3.7.3.2.7.4.6.0.0</b></div>', unsafe_allow_html=True)
else:
    st.error("⚠️ Không thể tải dữ liệu. Vui lòng kiểm tra lại Google Sheet.")
