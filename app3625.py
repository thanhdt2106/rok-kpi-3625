import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS CUSTOM (BAO GỒM CẢ PHẦN ĐIỀU CHỈNH RADIO & NỀN TỐI) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    
    /* Radio button ngôn ngữ góc phải */
    div[data-testid="stRadio"] > label { font-weight: bold; color: #00d4ff; }
    
    /* Tiêu đề chính */
    .main-header {
        color: #00d4ff; text-align: center; font-size: 32px;
        font-weight: bold; padding: 15px;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    /* Dataframe style */
    [data-testid="stDataFrame"] { background-color: #161b22; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. QUẢN LÝ NGÔN NGỮ ---
col_t, col_l = st.columns([4, 1]) 
with col_l:
    lang = st.radio("LANG:", ["VN", "EN"], horizontal=True, label_visibility="collapsed")

texts = {
    "VN": {
        "header": "🛡️ HỆ THỐNG QUẢN LÝ KPI",
        "search": "🔍 TRA CỨU CHIẾN BINH:",
        "select": "--- Chọn tên ---",
        "all": "LIÊN MINH", "pow": "SỨC MẠNH", "tk": "TỔNG KILL", "td": "TỔNG DEAD",
        "kt": "MỤC TIÊU KILL", "dt": "MỤC TIÊU DEAD",
        "table": "📋 BẢNG THỐNG KÊ TỔNG HỢP",
        "cols": ['Tên', 'ID', 'Liên minh', 'Sức mạnh', 'Tổng Kill', 'Kill tăng (+)', 'Dead tăng (+)', 'KPI (%)']
    },
    "EN": {
        "header": "🛡️ KPI MANAGEMENT SYSTEM",
        "search": "🔍 WARRIOR LOOKUP:",
        "select": "--- Select name ---",
        "all": "ALLIANCE", "pow": "POWER", "tk": "TOTAL KILL", "td": "TOTAL DEAD",
        "kt": "TARGET KILL", "dt": "TARGET DEAD",
        "table": "📋 SUMMARY STATISTICS TABLE",
        "cols": ['Name', 'ID', 'Alliance', 'Power', 'Total Kill', 'Kill Inc (+)', 'Dead Inc (+)', 'KPI (%)']
    }
}
L = texts[lang]

# --- 4. XỬ LÝ DỮ LIỆU TỪ GOOGLE SHEETS ---
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
        
        num_cols = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in num_cols:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
            
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']

        def get_metrics(r):
            p = r['Sức Mạnh_2']
            if p < 15e6: gk = 80e6
            elif p < 20e6: gk = 100e6
            elif p < 25e6: gk = 130e6
            elif p < 30e6: gk = 170e6
            elif p < 35e6: gk = 200e6
            elif p < 40e6: gk = 220e6
            elif p < 45e6: gk = 250e6
            else: gk = 300e6
            
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = max(0.0, float(r['KI']) / gk) if gk > 0 else 0.0
            pdv = max(0.0, float(r['DI']) / gd) if gd > 0 else 0.0
            return pd.Series([round(((pk + pdv) / 2) * 100, 1), gk, gd])
        
        df[['KPI', 'GK', 'GD']] = df.apply(get_metrics, axis=1)
        return df
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu: {e}")
        return None

df = load_data()

# --- 5. HIỂN THỊ GIAO DIỆN ---
if df is not None:
    st.markdown(f'<div class="main-header">{L["header"]}</div>', unsafe_allow_html=True)
    
    names = sorted(df['Tên_2'].unique())
    sel = st.selectbox(L["search"], [L["select"]] + names)
    
    if sel != L["select"]:
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # Tạo chuỗi HTML cho Frame Nổi Xanh Đậm
        html_card = f"""
        <div class="floating-card">
            <style>
                .floating-card {{
                    background: linear-gradient(145deg, #0a3d62, #062c43);
                    border: 2px solid #3282b8;
                    border-radius: 15px;
                    padding: 25px;
                    color: white;
                    box-shadow: 0 15px 35px rgba(0,0,0,0.6);
                    font-family: sans-serif;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 15px;
                    margin-top: 20px;
                }}
                .stat-box {{
                    background: rgba(0, 0, 0, 0.3);
                    padding: 12px;
                    border-radius: 10px;
                    border: 1px solid rgba(255,255,255,0.1);
                    text-align: center;
                }}
                .s-label {{ color: #bbe1fa; font-size: 10px; text-transform: uppercase; font-weight: bold; }}
                .s-value {{ display: block; font-size: 18px; font-weight: bold; margin-top: 5px; }}
                .target {{ color: #00d4ff; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 10px; padding-top: 5px; }}
            </style>

            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h2 style="margin:0; color:#00d4ff;">👤 {sel}</h2>
                    <p style="margin:5px 0; color:#8899a6; font-size:13px;">ID: {d['ID']} | {d['Liên Minh_2']}</p>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 32px; font-weight: bold; color: #00d4ff;">{d['KPI']}%</span>
                    <br><span style="font-size: 10px; color: #bbe1fa;">TOTAL PERFORMANCE</span>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-box">
                    <span class="s-label">{L['pow']}</span>
                    <span class="s-value">{int(d['Sức Mạnh_2']):,}</span>
                </div>
                <div class="stat-card stat-box">
                    <span class="s-label">{L['tk']}</span>
                    <span class="s-value">{int(d['Tổng Tiêu Diệt_2']):,}</span>
                </div>
                <div class="stat-box">
                    <span class="s-label">{L['td']}</span>
                    <span class="s-value">{int(d['Điểm Chết_2']):,}</span>
                </div>
                <div class="stat-box">
                    <span class="s-label">RANK</span>
                    <span class="s-value" style="color:#ffd700">S-RANK</span>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
                <div class="stat-box target">
                    <span class="s-label">{L['kt']}</span>
                    <span class="s-value">{int(d['GK']):,}</span>
                </div>
                <div class="stat-box target">
                    <span class="s-label">{L['dt']}</span>
                    <span class="s-value">{int(d['GD']):,}</span>
                </div>
            </div>
        </div>
        """
        components.html(html_card, height=350)

        # Thanh tiến độ Streamlit nguyên bản bên dưới Frame
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.caption(f"🔥 {L['cols'][5]}: {int(d['KI']):,}")
            st.progress(max(0.0, min(float(d['KI']) / d['GK'], 1.0)) if d['GK'] > 0 else 0.0)
        with col_p2:
            st.caption(f"💀 {L['cols'][6]}: {int(d['DI']):,}")
            st.progress(max(0.0, min(float(d['DI']) / d['GD'], 1.0)) if d['GD'] > 0 else 0.0)

    # --- 6. BẢNG TỔNG HỢP ---
    st.divider()
    st.subheader(L["table"])
    v_df = df[['Tên_2', 'ID', 'Liên Minh_2', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'KI', 'DI', 'KPI']].copy()
    v_df.columns = L["cols"]
    
    # Định dạng bảng
    st.dataframe(v_df.style.format({
        L["cols"][3]: '{:,.0f}', L["cols"][4]: '{:,.0f}', 
        L["cols"][5]: '{:,.0f}', L["cols"][6]: '{:,.0f}', L["cols"][7]: '{:.1f}%'
    }), use_container_width=True, height=500)
