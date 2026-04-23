import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS TỔNG THỂ ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .stSelectbox { max-width: 500px; margin: 0 auto; }
    .main-header {
        color: #00d4ff; text-align: center; font-size: 35px;
        font-weight: bold; padding: 20px; text-transform: uppercase;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. QUẢN LÝ NGÔN NGỮ ---
col_t, col_l = st.columns([4, 1]) 
with col_l:
    lang = st.radio("LANG:", ["VN", "EN"], horizontal=True, label_visibility="collapsed")

texts = {
    "VN": {
        "header": "🛡️ COMMAND CENTER 3625", "search": "🔍 TRA CỨU CHIẾN BINH:",
        "select": "--- Chọn tên ---", "pow": "POWER", "tk": "TỔNG KILL", 
        "td": "TOTAL DEAD", "rank": "RANK", "target": "Target",
        "cols": ['Tên', 'ID', 'Liên minh', 'Sức mạnh', 'Tổng Kill', 'Kill tăng (+)', 'Dead tăng (+)', 'KPI (%)']
    },
    "EN": {
        "header": "🛡️ COMMAND CENTER 3625", "search": "🔍 WARRIOR LOOKUP:",
        "select": "--- Select name ---", "pow": "POWER", "tk": "TOTAL KILL", 
        "td": "TOTAL DEAD", "rank": "RANK", "target": "Target",
        "cols": ['Name', 'ID', 'Alliance', 'Power', 'Total Kill', 'Kill Inc (+)', 'Dead Inc (+)', 'KPI (%)']
    }
}
L = texts[lang]

# --- 4. TẢI DỮ LIỆU ---
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
            gk = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 220e6 if p >= 35e6 else 200e6
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = max(0.0, float(r['KI']) / gk) if gk > 0 else 0.0
            pdv = max(0.0, float(r['DI']) / gd) if gd > 0 else 0.0
            return pd.Series([round(pk * 100, 1), round(pdv * 100, 1), round(((pk + pdv) / 2) * 100, 1), f"{gk/1e6:,.0f}M", f"{gd/1e3:,.0f}K"])
            
        df[['KPI_K', 'KPI_D', 'KPI_T', 'T_K', 'T_D']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    st.markdown(f'<div class="main-header">{L["header"]}</div>', unsafe_allow_html=True)
    
    _, col_search, _ = st.columns([1, 2, 1])
    with col_search:
        sel = st.selectbox(L["search"], [L["select"]] + sorted(df['Tên_2'].unique()), label_visibility="collapsed")
    
    if sel != L["select"]:
        d = df[df['Tên_2'] == sel].iloc[0]
        _, col_mid, _ = st.columns([1, 5, 1])
        
        with col_mid:
            html_card = f"""
            <div style="position: relative; width: 100%; max-width: 1000px; margin: 60px auto 20px; font-family: 'Segoe UI', sans-serif;">
                
                <div style="position: absolute; top: -50px; left: 50%; transform: translateX(-50%); 
                            background: #1a2a3a; border: 2px solid #00d4ff; border-radius: 15px; 
                            padding: 10px 40px; z-index: 10; box-shadow: 0 10px 30px rgba(0,0,0,0.8); min-width: 320px; text-align: center;">
                    <div style="color: #00d4ff; font-size: 18px; font-weight: 900; letter-spacing: 2px;">PROFILE MEMBER</div>
                    <div style="color: #ffffff; font-size: 24px; font-weight: bold; margin: 2px 0;">{sel}</div>
                    <div style="color: #8b949e; font-size: 11px;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                </div>

                <div style="background: rgba(13, 25, 47, 0.95); border: 2px solid #00d4ff; border-radius: 15px; padding: 60px 25px 25px 25px;">
                    
                    <div style="display: flex; justify-content: space-between; align-items: stretch; gap: 15px; margin-bottom: 25px;">
                        <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center;">
                            <div style="font-size: 11px; color: #8b949e; font-weight: bold;">{L['pow']}</div>
                            <div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                        </div>
                        <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center;">
                            <div style="font-size: 11px; color: #8b949e; font-weight: bold;">{L['tk']}</div>
                            <div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                        </div>
                        <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center;">
                            <div style="font-size: 11px; color: #ff4b4b; font-weight: bold;">{L['td']}</div>
                            <div style="font-size: 20px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                        </div>
                        <div style="background: #ffd700; border-radius: 10px; padding: 15px; width: 120px; text-align: center; display: flex; flex-direction: column; justify-content: center;">
                            <div style="font-size: 10px; color: #000; font-weight: 900;">RANK</div>
                            <div style="font-size: 22px; font-weight: 900; color: #000;">#{d['KillRank']}</div>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1.2fr 1fr; gap: 20px; background: rgba(0, 212, 255, 0.05); padding: 25px; border-radius: 15px; align-items: center;">
                        <div style="text-align: center;">
                            <div style="position: relative; width: 70px; height: 70px; margin: 0 auto;">
                                <svg viewBox="0 0 36 36" style="width: 70px; height: 70px; transform: rotate(-90deg);">
                                    <circle cx="18" cy="18" r="16" fill="none" stroke="#222" stroke-width="3"></circle>
                                    <circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" 
                                            stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round"></circle>
                                </svg>
                                <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:13px; font-weight:bold; color: white;">{d['KPI_K']}%</div>
                            </div>
                            <div style="font-size: 11px; color: #00ffff; font-weight: bold; margin-top: 8px;">KPI KILL</div>
                            <div style="font-size: 10px; color: #8b949e;">{L['target']}: {d['T_K']}</div>
                        </div>

                        <div style="text-align: center;">
                            <div style="position: relative; width: 100px; height: 100px; margin: 0 auto;">
                                <svg viewBox="0 0 36 36" style="width: 100px; height: 100px; transform: rotate(-90deg);">
                                    <circle cx="18" cy="18" r="16" fill="none" stroke="#222" stroke-width="2.5"></circle>
                                    <circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3.5" 
                                            stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round"></circle>
                                </svg>
                                <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:18px; font-weight:900; color: #ffd700;">{d['KPI_T']}%</div>
                            </div>
                            <div style="font-size: 13px; color: #ffd700; font-weight: bold; margin-top: 5px; letter-spacing: 1px;">TOTAL KPI</div>
                        </div>

                        <div style="text-align: center;">
                            <div style="position: relative; width: 70px; height: 70px; margin: 0 auto;">
                                <svg viewBox="0 0 36 36" style="width: 70px; height: 70px; transform: rotate(-90deg);">
                                    <circle cx="18" cy="18" r="16" fill="none" stroke="#222" stroke-width="3"></circle>
                                    <circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" 
                                            stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round"></circle>
                                </svg>
                                <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:13px; font-weight:bold; color: white;">{d['KPI_D']}%</div>
                            </div>
                            <div style="font-size: 11px; color: #ff4b4b; font-weight: bold; margin-top: 8px;">KPI DEAD</div>
                            <div style="font-size: 10px; color: #8b949e;">{L['target']}: {d['T_D']}</div>
                        </div>
                    </div>
                </div>
            </div>
            """
            components.html(html_card, height=520)

    st.divider()
    st.dataframe(df[['Tên_2', 'ID', 'Sức Mạnh_2', 'KPI_T']].sort_values(by='KPI_T', ascending=False), use_container_width=True)
