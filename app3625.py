import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS ĐỂ CĂN GIỮA TOÀN BỘ ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    /* Căn giữa selectbox */
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
        "td": "TỔNG DEAD", "rank": "HẠNG", "cols": ['Tên', 'ID', 'Liên minh', 'Sức mạnh', 'Tổng Kill', 'Kill tăng (+)', 'Dead tăng (+)', 'KPI (%)']
    },
    "EN": {
        "header": "🛡️ COMMAND CENTER 3625", "search": "🔍 WARRIOR LOOKUP:",
        "select": "--- Select name ---", "pow": "POWER", "tk": "TOTAL KILL", 
        "td": "TOTAL DEAD", "rank": "RANK", "cols": ['Name', 'ID', 'Alliance', 'Power', 'Total Kill', 'Kill Inc (+)', 'Dead Inc (+)', 'KPI (%)']
    }
}
L = texts[lang]

# --- 4. TẢI DỮ LIỆU (Giữ nguyên logic của bạn) ---
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
            return pd.Series([round(pk * 100, 1), round(pdv * 100, 1), round(((pk + pdv) / 2) * 100, 1)])
        df[['KPI_K', 'KPI_D', 'KPI_T']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    st.markdown(f'<div class="main-header">{L["header"]}</div>', unsafe_allow_html=True)
    
    # Tạo layout căn giữa cho thanh tìm kiếm
    _, col_search, _ = st.columns([1, 2, 1])
    with col_search:
        names = sorted(df['Tên_2'].unique())
        sel = st.selectbox(L["search"], [L["select"]] + names, label_visibility="collapsed")
    
    if sel != L["select"]:
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # SỬ DỤNG COLUMNS ĐỂ ÉP KHUNG VÀO GIỮA
        _, col_mid, _ = st.columns([1, 1.5, 1])
        
        with col_mid:
            html_card = f"""
            <div style="background: linear-gradient(180deg, #0d253f 0%, #06111d 100%); 
                        border: 2px solid #00d4ff; border-radius: 20px; padding: 30px; 
                        font-family: 'Segoe UI', sans-serif; color: white; 
                        box-shadow: 0 15px 40px rgba(0,0,0,0.8); text-align: center;">
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                    <div style="text-align: left;">
                        <div style="font-size: 32px; font-weight: 900; color: #00d4ff; text-transform: uppercase;">{sel}</div>
                        <div style="font-size: 14px; color: #8899a6;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                    </div>
                    <div style="background: #ffd700; color: #000; padding: 10px 20px; border-radius: 12px; font-weight: 900; font-size: 20px;">
                        #{d['KillRank']}
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px;">
                    <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(0,212,255,0.1);">
                        <div style="color: #bbe1fa; font-size: 12px; font-weight: bold; margin-bottom: 5px;">{L['pow']}</div>
                        <div style="font-size: 24px; font-weight: bold;">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(0,212,255,0.1);">
                        <div style="color: #bbe1fa; font-size: 12px; font-weight: bold; margin-bottom: 5px;">{L['tk']}</div>
                        <div style="font-size: 24px; font-weight: bold; color: #ffd700;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; background: rgba(0,212,255,0.05); padding: 20px; border-radius: 15px;">
                    <div>
                        <div style="font-size: 11px; color: #00ffff; font-weight: bold;">KPI KILL</div>
                        <div style="font-size: 22px; font-weight: 900;">{d['KPI_K']}%</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #ff4b4b; font-weight: bold;">KPI DEAD</div>
                        <div style="font-size: 22px; font-weight: 900;">{d['KPI_D']}%</div>
                    </div>
                    <div style="border-left: 1px solid rgba(255,255,255,0.1);">
                        <div style="font-size: 11px; color: #ffd700; font-weight: bold;">TOTAL</div>
                        <div style="font-size: 28px; font-weight: 900; color: #ffd700;">{d['KPI_T']}%</div>
                    </div>
                </div>
            </div>
            """
            components.html(html_card, height=480)

    # Bảng dữ liệu phía dưới (Giữ nguyên để đối chiếu)
    st.divider()
    v_df = df[['Tên_2', 'ID', 'Liên Minh_2', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'KI', 'DI', 'KPI_T']].sort_values(by='Tổng Tiêu Diệt_2', ascending=False)
    v_df.columns = L["cols"]
    st.dataframe(v_df.style.format({L["cols"][3]: '{:,.0f}', L["cols"][4]: '{:,.0f}', L["cols"][5]: '{:,.0f}', L["cols"][6]: '{:,.0f}', L["cols"][7]: '{:.1f}%'}), use_container_width=True, height=350)
