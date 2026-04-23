import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# Link ảnh Logo
LOGO_URL = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true"

# --- 2. SIÊU CSS (Chỉnh Header và Profile Card) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .block-container { padding-top: 1rem !important; max-width: 100% !important; }
    header { visibility: hidden; height: 0px !important; }
    
    /* Header chính */
    .header-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    .logo-main { width: 120px; filter: drop-shadow(0px 0px 10px rgba(0, 212, 255, 0.5)); }
    .main-title {
        color: #00d4ff; font-size: 32px !important; font-weight: bold;
        text-shadow: 0px 0px 15px rgba(0,212,255,0.6); margin: 5px 0;
    }

    .hr-line {
        border: 0; height: 1px;
        background-image: linear-gradient(to right, rgba(0, 212, 255, 0), rgba(0, 212, 255, 0.75), rgba(0, 212, 255, 0));
        margin: 15px 0;
    }

    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: rgba(5, 10, 14, 0.9); color: #8b949e;
        padding: 10px; font-size: 13px; text-align: center;
        border-top: 1px solid #1a2a3a; z-index: 999;
    }
    [data-testid="stDataFrame"] { background: #1a2a3a; border-radius: 10px; border: 1px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. QUẢN LÝ NGÔN NGỮ ---
texts = {
    "VN": {
        "header": "HỆ THỐNG QUẢN TRỊ 3625", 
        "placeholder": "👤 Điền tên của bạn để tìm kiếm 🔍",
        "pow": "SỨC MẠNH", "tk": "TỔNG TIÊU DIỆT", "td": "ĐIỂM CHẾT", "rank": "HẠNG",
        "cols": ['Tên', 'ID', 'Liên minh', 'Hạng', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']
    },
    "EN": {
        "header": "COMMAND CENTER 3625", 
        "placeholder": "👤 Enter member name to search 🔍",
        "pow": "POWER", "tk": "TOTAL KILL", "td": "TOTAL DEAD", "rank": "RANK",
        "cols": ['Name', 'ID', 'Alliance', 'Rank', 'Power', 'Total Kill', 'Total Dead', 'Kill Inc', 'Dead Inc', 'KPI %']
    }
}

# --- 4. GIỮ NGUYÊN BẮT DỮ LIỆU TỪ DATA (GOOGLE SHEETS) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = 'https://docs.google.com/spreadsheets/d/' + SHEET_ID + '/export?format=csv&gid=731741617'
URL_S = 'https://docs.google.com/spreadsheets/d/' + SHEET_ID + '/export?format=csv&gid=371969335'

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
            return pd.Series([round(pk * 100, 1), round(pdv * 100, 1), round(((pk + pdv) / 2) * 100, 1), gk, gd])
            
        df[['KPI_K', 'KPI_D', 'KPI_T', 'Target_K', 'Target_D']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    _, col_lang = st.columns([6, 1])
    with col_lang:
        lang = st.radio("LANG:", ["VN", "EN"], horizontal=True, label_visibility="collapsed")
    L = texts[lang]

    # Header chính (Logo to lên trên)
    st.markdown(f"""
        <div class="header-wrapper">
            <img src="{LOGO_URL}" class="logo-main">
            <p class="main-title">{L['header']}</p>
        </div>
    """, unsafe_allow_html=True)

    col_l, col_search, col_r = st.columns([1.5, 3, 1.5])
    with col_search:
        sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder=L["placeholder"])

    st.markdown("<div class='hr-line'></div>", unsafe_allow_html=True)

    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        tk_str = f"{int(d['Target_K']/1e6)}M" if d['Target_K'] >= 1e6 else f"{int(d['Target_K']/1e3)}K"
        td_str = f"{int(d['Target_D']/1e3)}K"

        # Phần Profile Card với Ava nhỏ nằm bên trái tên (ngang hàng chữ)
        html_card = f"""
        <div style="position: relative; width: 100%; margin: 60px auto 10px; font-family: 'Segoe UI', sans-serif;">
            <div style="position: absolute; top: -50px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 12px 40px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; box-shadow: 0 8px 25px rgba(0,0,0,0.8); min-width: 450px;">
                <div style="color: #00d4ff; font-size: 11px; font-weight: 900; letter-spacing: 2px; margin-bottom: 5px;">PROFILE MEMBER</div>
                <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
                    <img src="{LOGO_URL}" style="width: 45px; height: 45px; border-radius: 5px; border: 1px solid #00d4ff;">
                    <div style="color: #ffffff; font-size: 28px; font-weight: bold; text-shadow: 0 0 10px #00d4ff;">{sel}</div>
                </div>
                <div style="font-size: 13px; margin-top: 8px;">
                    <b style="color: #ffd700;">ID:</b> <span style="color: #fff;">{d['ID']}</span> | 
                    <b style="color: #00ffcc;">ALLIANCE:</b> <span style="color: #fff;">{d['Liên Minh_2']}</span>
                </div>
            </div>
            
            <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 85px 20px 20px 20px;">
                <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 25px;">
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3.5px solid #00d4ff;">
                        <div style="font-size: 10px; color: #8b949e; font-weight: bold;">{L['pow']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3.5px solid #00ffcc;">
                        <div style="font-size: 10px; color: #8b949e; font-weight: bold;">{L['tk']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3.5px solid #ff4b4b;">
                        <div style="font-size: 10px; color: #ff4b4b; font-weight: bold;">{L['td']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 0.6; text-align: center; border-bottom: 3.5px solid #ffd700;">
                        <div style="font-size: 10px; color: #ffd700; font-weight: bold;">{L['rank']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #ffd700;">#{d['KillRank']}</div>
                    </div>
                </div>

                <div style="background: #1a2a3a; border-radius: 15px; padding: 30px; border-bottom: 5px solid #ffd700; display: flex; justify-content: space-around; align-items: center;">
                    <div style="text-align: center;">
                        <div style="position: relative; width: 90px; height: 90px; margin: 0 auto;">
                            <svg viewBox="0 0 36 36" style="width: 90px; height: 90px; transform: rotate(-90deg);">
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="4"></circle>
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3.5" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round"></circle>
                            </svg>
                            <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:16px; font-weight:bold; color: #00ffff;">{d['KPI_K']}%</div>
                        </div>
                        <div style="font-size: 11px; color: #00ffff; font-weight: bold; margin-top: 10px;">KPI KILL</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="position: relative; width: 130px; height: 130px; margin: 0 auto;">
                            <svg viewBox="0 0 36 36" style="width: 130px; height: 130px; transform: rotate(-90deg);">
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="4"></circle>
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="4" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round"></circle>
                            </svg>
                            <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:24px; font-weight:900; color:#ffd700;">{d['KPI_T']}%</div>
                        </div>
                        <div style="font-size: 15px; color: #ffd700; font-weight: bold; margin-top: 10px;">TOTAL KPI</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="position: relative; width: 90px; height: 90px; margin: 0 auto;">
                            <svg viewBox="0 0 36 36" style="width: 90px; height: 90px; transform: rotate(-90deg);">
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="4"></circle>
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3.5" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round"></circle>
                            </svg>
                            <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:16px; font-weight:bold; color: #ff4b4b;">{d['KPI_D']}%</div>
                        </div>
                        <div style="font-size: 11px; color: #ff4b4b; font-weight: bold; margin-top: 10px;">KPI DEAD</div>
                    </div>
                </div>
            </div>
        </div>
        """
        components.html(html_card, height=580)

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    display_df = df[['Tên_2', 'ID', 'Liên Minh_2', 'KillRank', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'KI', 'DI', 'KPI_T']].copy()
    display_df.columns = L['cols']
    for col in L['cols'][4:9]:
        display_df[col] = display_df[col].apply(lambda x: f"{int(x):,}")
    display_df[L['cols'][9]] = display_df[L['cols'][9]].apply(lambda x: f"{x}%")

    st.dataframe(display_df.sort_values(by=L['cols'][3]), use_container_width=True, hide_index=True, height=600)

    st.markdown(f"""
        <div class="footer">
            🛡️ Discord: <b>louiss.nee</b> | Zalo: <b>0.3.7.3.2.7.4.6.0.0</b>
        </div>
        """, unsafe_allow_html=True)
else:
    st.error("⚠️ Không thể kết nối với dữ liệu Google Sheets.")
