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
        "select": "--- Chọn tên ---", "pow": "SỨC MẠNH", "tk": "TỔNG KILL", 
        "td": "ĐIỂM CHẾT", "rank": "HẠNG", "target": "Mục tiêu",
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

# --- 4. XỬ LÝ DỮ LIỆU ---
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
            # Cấu hình mốc KPI
            gk = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 220e6 if p >= 35e6 else 200e6
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = max(0.0, float(r['KI']) / gk) if gk > 0 else 0.0
            pdv = max(0.0, float(r['DI']) / gd) if gd > 0 else 0.0
            return pd.Series([
                round(pk * 100, 1), 
                round(pdv * 100, 1), 
                round(((pk + pdv) / 2) * 100, 1),
                f"{gk/1e6:,.0f}M", 
                f"{gd/1e3:,.0f}K"
            ])
            
        df[['KPI_K', 'KPI_D', 'KPI_T', 'T_K', 'T_D']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    st.markdown(f'<div class="main-header">{L["header"]}</div>', unsafe_allow_html=True)
    
    _, col_search, _ = st.columns([1, 2, 1])
    with col_search:
        names = sorted(df['Tên_2'].unique())
        sel = st.selectbox(L["search"], [L["select"]] + names, label_visibility="collapsed")
    
    if sel != L["select"]:
        d = df[df['Tên_2'] == sel].iloc[0]
        _, col_mid, _ = st.columns([1, 2, 1])
        
        with col_mid:
            html_card = f"""
            <div style="background: linear-gradient(180deg, #0d253f 0%, #06111d 100%); 
                        border: 2px solid #00d4ff; border-radius: 20px; padding: 25px; 
                        font-family: 'Segoe UI', sans-serif; color: white; 
                        box-shadow: 0 15px 40px rgba(0,0,0,0.8); text-align: center;">
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <div style="text-align: left;">
                        <div style="font-size: 30px; font-weight: 900; color: #00d4ff; text-transform: uppercase;">{sel}</div>
                        <div style="font-size: 13px; color: #8899a6;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                    </div>
                    <div style="background: #ffd700; color: #000; padding: 8px 15px; border-radius: 10px; font-weight: 900; font-size: 18px;">
                        #{d['KillRank']}
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 20px;">
                    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; border: 1px solid rgba(0,212,255,0.1);">
                        <div style="color: #bbe1fa; font-size: 10px; font-weight: bold;">{L['pow']}</div>
                        <div style="font-size: 16px; font-weight: bold;">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; border: 1px solid rgba(0,212,255,0.1);">
                        <div style="color: #ffd700; font-size: 10px; font-weight: bold;">{L['tk']}</div>
                        <div style="font-size: 16px; font-weight: bold; color: #ffd700;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; border: 1px solid rgba(0,212,255,0.1);">
                        <div style="color: #ff4b4b; font-size: 10px; font-weight: bold;">{L['td']}</div>
                        <div style="font-size: 16px; font-weight: bold; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                    </div>
                </div>

                <div style="display: flex; justify-content: space-around; align-items: flex-end; background: rgba(0,212,255,0.03); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05);">
                    <div style="text-align: center;">
                        <svg width="70" height="70" viewBox="0 0 36 36">
                            <circle cx="18" cy="18" r="16" fill="none" stroke="#222" stroke-width="3"></circle>
                            <circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" 
                                    stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"></circle>
                            <text x="18" y="20.5" text-anchor="middle" font-size="8" font-weight="bold" fill="white">{d['KPI_K']}%</text>
                        </svg>
                        <div style="font-size: 10px; color: #00ffff; font-weight: bold; margin-top: 5px;">KPI KILL</div>
                        <div style="font-size: 9px; color: #8899a6;">{L['target']}: {d['T_K']}</div>
                    </div>

                    <div style="text-align: center;">
                        <svg width="90" height="90" viewBox="0 0 36 36">
                            <circle cx="18" cy="18" r="16" fill="none" stroke="#222" stroke-width="2"></circle>
                            <circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" 
                                    stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"></circle>
                            <text x="18" y="21" text-anchor="middle" font-size="9" font-weight="900" fill="#ffd700">{d['KPI_T']}%</text>
                        </svg>
                        <div style="font-size: 12px; color: #ffd700; font-weight: bold; margin-top: 5px;">TOTAL KPI</div>
                    </div>

                    <div style="text-align: center;">
                        <svg width="70" height="70" viewBox="0 0 36 36">
                            <circle cx="18" cy="18" r="16" fill="none" stroke="#222" stroke-width="3"></circle>
                            <circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" 
                                    stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"></circle>
                            <text x="18" y="20.5" text-anchor="middle" font-size="8" font-weight="bold" fill="white">{d['KPI_D']}%</text>
                        </svg>
                        <div style="font-size: 10px; color: #ff4b4b; font-weight: bold; margin-top: 5px;">KPI DEAD</div>
                        <div style="font-size: 9px; color: #8899a6;">{L['target']}: {d['T_D']}</div>
                    </div>
                </div>
            </div>
            """
            components.html(html_card, height=450)

    st.divider()
    v_df = df[['Tên_2', 'ID', 'Liên Minh_2', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'KI', 'DI', 'KPI_T']].sort_values(by='Tổng Tiêu Diệt_2', ascending=False)
    v_df.columns = L["cols"]
    st.dataframe(v_df.style.format({L["cols"][3]: '{:,.0f}', L["cols"][4]: '{:,.0f}', L["cols"][5]: '{:,.0f}', L["cols"][6]: '{:,.0f}', L["cols"][7]: '{:.1f}%'}), use_container_width=True, height=350)
