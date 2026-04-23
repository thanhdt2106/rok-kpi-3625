import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="ROK KPI SYSTEM", layout="wide")

# --- 2. CSS FIX GIAO DIỆN ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    .rok-card {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #3eb5e5;
        color: white;
    }
    .main-row { display: flex; justify-content: space-between; align-items: start; }
    .left-box { flex: 1; }
    .right-box { 
        flex: 1; 
        display: grid; 
        grid-template-columns: 1fr 1fr; 
        gap: 15px; 
        background: rgba(0,0,0,0.25); 
        padding: 15px; 
        border-radius: 6px;
    }
    .p-id { font-size: 14px; color: #b0d4e3; opacity: 0.9; }
    .p-name { font-size: 30px; font-weight: 800; margin: 5px 0; text-transform: uppercase; }
    .label-nba { color: #b0d4e3; font-size: 12px; text-transform: uppercase; }
    .value-nba { font-size: 22px; font-weight: 700; color: white; display: block; }
    
    /* Style cho 3 ô KPI */
    .kpi-container {
        background: #1a1c23;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #333;
    }
    .kpi-title { font-size: 13px; font-weight: bold; color: #888; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM BIỂU ĐỒ KPI ---
def create_gauge(pct, color):
    try:
        val = float(pct)
    except:
        val = 0.0
    fig = go.Figure(go.Pie(
        hole=0.7, values=[val, max(0, 100-val)],
        marker=dict(colors=[color, "#222"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=5, r=5), height=140,
        annotations=[dict(text=f"{val}%", x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=18))]
    )
    return fig

# --- 4. DATA LOGIC ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        df_t = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        df_s = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        df_t['ID'] = df_t['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df_s['ID'] = df_s['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df = pd.merge(df_t, df_s, on='ID', suffixes=('_1', '_2'))
        
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        def calc(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            gd = 400e3 if p >= 30e6 else 200e3
            ki = r['Tổng Tiêu Diệt_2'] - r['Tổng Tiêu Diệt_1']
            di = r['Điểm Chết_2'] - r['Điểm Chết_1']
            kp = round((ki / gk * 100), 1) if gk > 0 else 0
            dp = round((di / gd * 100), 1) if gd > 0 else 0
            return pd.Series([round((kp + dp) / 2, 1), kp, dp])
        
        df[['KPI_T', 'KPI_K', 'KPI_D']] = df.apply(calc, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    names = sorted(df['Tên_2'].dropna().unique())
    sel_name = st.selectbox("🔍 TRA CỨU CHIẾN BINH:", ["---"] + names)
    
    if sel_name != "---":
        d = df[df['Tên_2'] == sel_name].iloc[0]
        
        # Phần Hồ sơ xanh
        st.markdown(f"""
            <div class="rok-card">
                <div class="main-row">
                    <div class="left-box">
                        <div class="p-id">Thống đốc(ID: {d['ID']})</div>
                        <div class="p-name">{sel_name}</div>
                        <div style="margin-top:10px;">Liên minh: <b>[{d['Liên Minh_2']}]</b></div>
                    </div>
                    <div class="right-box">
                        <div><span class="label-nba">Điểm Tiêu Diệt</span><span class="value-nba">{int(d['Tổng Tiêu Diệt_2']):,}</span></div>
                        <div><span class="label-nba">Sức mạnh</span><span class="value-nba">{int(d['Sức Mạnh_2']):,}</span></div>
                        <div><span class="label-nba">Điểm Chiến Công</span><span class="value-nba">0</span></div>
                        <div><span class="label-nba">Chiến công cao nhất</span><span class="value-nba">---</span></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Phần 3 vòng tròn KPI (Dùng st.columns để tránh lỗi render HTML)
        st.write("### TIẾN ĐỘ KVK")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="kpi-container"><div class="kpi-title">KPI TIÊU DIỆT</div>', unsafe_allow_html=True)
            st.plotly_chart(create_gauge(d['KPI_K'], "#00ffff"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="kpi-container"><div class="kpi-title">KPI ĐIỂM CHẾT</div>', unsafe_allow_html=True)
            st.plotly_chart(create_gauge(d['KPI_D'], "#ff4b4b"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="kpi-container"><div class="kpi-title">TỔNG KPI</div>', unsafe_allow_html=True)
            st.plotly_chart(create_gauge(d['KPI_T'], "#ffd700"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
