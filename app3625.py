import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS TỐI GIẢN & CHUYÊN NGHIỆP ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    div[data-testid="stRadio"] > label { font-weight: bold; color: #00d4ff; }
    .main-header {
        color: #00d4ff; text-align: center; font-size: 28px;
        font-weight: bold; padding: 10px; text-transform: uppercase;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. QUẢN LÝ NGÔN NGỮ ---
col_t, col_l = st.columns([4, 1]) 
with col_l:
    lang = st.radio("LANG:", ["VN", "EN"], horizontal=True, label_visibility="collapsed")

texts = {
    "VN": {
        "header": "🛡️ HỆ THỐNG QUẢN LÝ KPI", "search": "🔍 TRA CỨU CHIẾN BINH:",
        "select": "--- Chọn tên ---", "pow": "SỨC MẠNH", "tk": "TỔNG KILL", 
        "td": "TỔNG DEAD", "rank": "HẠNG", "cols": ['Tên', 'ID', 'Liên minh', 'Sức mạnh', 'Tổng Kill', 'Kill tăng (+)', 'Dead tăng (+)', 'KPI (%)']
    },
    "EN": {
        "header": "🛡️ KPI MANAGEMENT SYSTEM", "search": "🔍 WARRIOR LOOKUP:",
        "select": "--- Select name ---", "pow": "POWER", "tk": "TOTAL KILL", 
        "td": "TOTAL DEAD", "rank": "RANK", "cols": ['Name', 'ID', 'Alliance', 'Power', 'Total Kill', 'Kill Inc (+)', 'Dead Inc (+)', 'KPI (%)']
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
        
        # Làm sạch dữ liệu số để tránh lỗi 'strip' hoặc 'ValueError'
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
            
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
        # TÍNH TOÁN THỨ HẠNG DỰA TRÊN TỔNG KILL
        df['KillRank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)

        def get_metrics(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 220e6 if p >= 35e6 else 200e3
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = max(0.0, float(r['KI']) / gk) if gk > 0 else 0.0
            pdv = max(0.0, float(r['DI']) / gd) if gd > 0 else 0.0
            return pd.Series([round(pk * 100, 1), round(pdv * 100, 1), round(((pk + pdv) / 2) * 100, 1)])
        
        df[['KPI_K', 'KPI_D', 'KPI_T']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    st.markdown(f'<div class="main-header">{L["header"]}</div>', unsafe_allow_html=True)
    names = sorted(df['Tên_2'].unique())
    sel = st.selectbox(L["search"], [L["select"]] + names)
    
    if sel != L["select"]:
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # HTML PROFILE COMPACT (GỌN GÀNG HƠN)
        html_card = f"""
        <div style="background: linear-gradient(135deg, #0a192f, #062c43); border: 1px solid #00d4ff; border-radius: 10px; padding: 15px; font-family: sans-serif; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(0,212,255,0.2); padding-bottom: 10px;">
                <div>
                    <span style="font-size: 20px; font-weight: bold; color: #00d4ff;">战士: {sel}</span>
                    <div style="font-size: 11px; color: #8899a6; margin-top: 3px;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                </div>
                <div style="text-align: right;">
                    <span style="background: #ffd700; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;">{L['rank']} {d['KillRank']}</span>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px; text-align: center;">
                <div style="background: rgba(0,0,0,0.2); padding: 8px; border-radius: 5px;">
                    <div style="color: #bbe1fa; font-size: 10px;">{L['pow']}</div>
                    <div style="font-size: 14px; font-weight: bold;">{int(d['Sức Mạnh_2']):,}</div>
                </div>
                <div style="background: rgba(0,0,0,0.2); padding: 8px; border-radius: 5px;">
                    <div style="color: #bbe1fa; font-size: 10px;">{L['tk']}</div>
                    <div style="font-size: 14px; font-weight: bold;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                </div>
                <div style="background: rgba(0,0,0,0.2); padding: 8px; border-radius: 5px;">
                    <div style="color: #bbe1fa; font-size: 10px;">{L['td']}</div>
                    <div style="font-size: 14px; font-weight: bold;">{int(d['Điểm Chết_2']):,}</div>
                </div>
            </div>

            <div style="display: flex; justify-content: space-around; margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
                <div style="text-align:center;">
                    <div style="font-size:9px; color:#00ffff;">KPI KILL</div>
                    <div style="font-size:16px; font-weight:bold;">{d['KPI_K']}%</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:9px; color:#ff4b4b;">KPI DEAD</div>
                    <div style="font-size:16px; font-weight:bold;">{d['KPI_D']}%</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:9px; color:#ffd700;">TOTAL</div>
                    <div style="font-size:16px; font-weight:bold; color:#ffd700;">{d['KPI_T']}%</div>
                </div>
            </div>
        </div>
        """
        components.html(html_card, height=220)

    st.divider()
    v_df = df[['Tên_2', 'ID', 'Liên Minh_2', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'KI', 'DI', 'KPI_T']].sort_values(by='Tổng Tiêu Diệt_2', ascending=False)
    v_df.columns = L["cols"]
    st.dataframe(v_df.style.format({L["cols"][3]: '{:,.0f}', L["cols"][4]: '{:,.0f}', L["cols"][5]: '{:,.0f}', L["cols"][6]: '{:,.0f}', L["cols"][7]: '{:.1f}%'}), use_container_width=True, height=400)
