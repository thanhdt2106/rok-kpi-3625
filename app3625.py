import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="ROK PROFILE SYSTEM", layout="wide")

# --- 2. CSS CHUẨN GIAO DIỆN HỒ SƠ ROK ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    
    /* Khung nền xanh hồ sơ */
    .rok-card {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 4px;
        padding: 20px;
        border: 1px solid #3eb5e5;
        color: white;
        margin-bottom: 20px;
    }

    /* Bố cục chia 2 phần: Trái (Tên/ID) - Phải (Chỉ số) */
    .main-layout { display: flex; justify-content: space-between; }
    .left-info { flex: 1; }
    .right-stats { 
        flex: 1.5; 
        display: grid; 
        grid-template-columns: 1fr 1fr; 
        gap: 15px;
        background: rgba(0, 0, 0, 0.3);
        padding: 15px;
        border-radius: 8px;
    }

    .p-id { font-size: 13px; color: #b0d4e3; }
    .p-name { font-size: 28px; font-weight: 800; background: rgba(0,0,0,0.4); padding: 5px 12px; border-radius: 3px; display: inline-block; margin: 5px 0; }
    .p-alliance { font-size: 15px; color: #ffffff; margin-top: 10px; }

    .stat-item { display: flex; flex-direction: column; }
    .stat-label { color: #b0d4e3; font-size: 12px; text-transform: uppercase; }
    .stat-value { font-size: 20px; font-weight: 700; color: #ffffff; }

    /* Khung KPI */
    .kpi-wrapper { text-align: center; background: #262730; padding: 15px; border-radius: 10px; border: 1px solid #444; }
    .kpi-title { font-size: 12px; font-weight: bold; margin-bottom: 10px; color: #aaa; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ VÒNG TRÒN KPI ---
def draw_kpi(pct, color):
    val = min(max(float(pct), 0.0), 100.0)
    fig = go.Figure(go.Pie(
        hole=0.75, values=[val, 100 - val],
        marker=dict(colors=[color, "#333"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=130,
        annotations=[dict(text=f"<b style='color:white; font-size:16px'>{pct}%</b>", x=0.5, y=0.5, showarrow=False)]
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
        for d_df in [df_t, df_s]:
            d_df['ID'] = d_df['ID'].astype(str).str.replace('.0', '', regex=False).strip()
        df = pd.merge(df_t, df_s, on='ID', suffixes=('_1', '_2'))
        
        cols = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in cols: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        def calc_kpi(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            gd = 400e3 if p >= 30e6 else 200e3
            ki, di = r['Tổng Tiêu Diệt_2'] - r['Tổng Tiêu Diệt_1'], r['Điểm Chết_2'] - r['Điểm Chết_1']
            kp, dp = round((ki/gk*100),1) if gk>0 else 0, round((di/gd*100),1) if gd>0 else 0
            return pd.Series([round((kp+dp)/2, 1), kp, dp])
        
        df[['KPI_T', 'KPI_K', 'KPI_D']] = df.apply(calc_kpi, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ GIAO DIỆN ---
if df is not None:
    names = sorted(df['Tên_2'].dropna().unique())
    sel_name = st.selectbox("🔍 CHỌN THỐNG ĐỐC:", ["---"] + names)
    
    if sel_name != "---":
        d = df[df['Tên_2'] == sel_name].iloc[0]
        
        # PHẦN 1: HỒ SƠ CHÍNH (Tên trái - Chỉ số phải)
        st.markdown(f"""
            <div class="rok-card">
                <div class="main-layout">
                    <div class="left-info">
                        <div class="p-id">Thống đốc(ID: {d['ID']})</div>
                        <div class="p-name">{sel_name}</div>
                        <div class="p-alliance">Liên minh: <br><b>[{d['Liên Minh_2']}]</b></div>
                    </div>
                    <div class="right-stats">
                        <div class="stat-item"><span class="stat-label">Điểm Tiêu Diệt</span><span class="stat-value">{int(d['Tổng Tiêu Diệt_2']):,}</span></div>
                        <div class="stat-item"><span class="stat-label">Sức mạnh</span><span class="stat-value">{int(d['Sức Mạnh_2']):,}</span></div>
                        <div class="stat-item"><span class="stat-label">Điểm Chiến Công</span><span class="stat-value">0</span></div>
                        <div class="stat-item"><span class="stat-label">Chiến công cao nhất</span><span class="stat-value">---</span></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # PHẦN 2: 3 VÒNG TRÒN KPI PHÍA DƯỚI
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="kpi-wrapper"><div class="kpi-title">KPI TIÊU DIỆT</div>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi(d['KPI_K'], "#00ffff"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="kpi-wrapper"><div class="kpi-title">KPI ĐIỂM CHẾT</div>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi(d['KPI_D'], "#ff4b4b"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="kpi-wrapper"><div class="kpi-title">TỔNG KPI KVK</div>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi(d['KPI_T'], "#ffd700"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
