import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="ROK PROFILE SYSTEM", layout="wide")

# --- 2. CSS ĐẶC CHẾ THEO HỒ SƠ ROK ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    
    /* Khung nền xanh hồ sơ */
    .rok-card {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 5px;
        padding: 25px;
        border: 1px solid #3eb5e5;
        color: white;
        font-family: sans-serif;
    }

    /* Bố cục phần trên: Tên & Chỉ số */
    .header-row { display: flex; justify-content: space-between; align-items: flex-start; }
    .name-section { flex: 1.5; }
    .stats-section { flex: 2; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

    .p-id { font-size: 14px; color: #b0d4e3; margin-bottom: 2px; }
    .p-name { font-size: 32px; font-weight: 800; background: rgba(0,0,0,0.2); padding: 5px 15px; border-radius: 4px; display: inline-block; margin-bottom: 10px; }
    .p-alliance { font-size: 16px; color: #ffffff; margin-top: 5px; }

    .stat-item { display: flex; flex-direction: column; }
    .stat-label { color: #b0d4e3; font-size: 13px; margin-bottom: 2px; }
    .stat-value { font-size: 24px; font-weight: 700; color: #ffffff; }

    /* Khung 3 ô KPI phía dưới */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        margin-top: 30px;
        gap: 15px;
    }
    .kpi-box {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 15px;
        flex: 1;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .kpi-label { font-size: 12px; font-weight: bold; color: #e0e0e0; margin-bottom: 10px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ VÒNG TRÒN KPI ---
def draw_kpi(pct, color):
    val = min(max(float(pct), 0.0), 100.0)
    fig = go.Figure(go.Pie(
        hole=0.75, values=[val, 100 - val],
        marker=dict(colors=[color, "rgba(255,255,255,0.1)"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=140,
        annotations=[dict(text=f"<b style='color:white; font-size:18px'>{pct}%</b>", x=0.5, y=0.5, showarrow=False)]
    )
    return fig

# --- 4. XỬ LÝ DỮ LIỆU (SỬA LỖI MERGE ID) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        df_t = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        df_s = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        for d in [df_t, df_s]:
            d['ID'] = d['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df = pd.merge(df_t, df_s, on='ID', suffixes=('_1', '_2'))
        
        # Chuyển đổi số
        cols = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in cols: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        def calc(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            gd = 400e3 if p >= 30e6 else 200e3
            ki = r['Tổng Tiêu Diệt_2'] - r['Tổng Tiêu Diệt_1']
            di = r['Điểm Chết_2'] - r['Điểm Chết_1']
            kp = round((ki / gk * 100), 1) if gk > 0 else 0
            dp = round((di / gd * 100), 1) if gd > 0 else 0
            return pd.Series([round((kp+dp)/2, 1), kp, dp, gk, gd])
        
        df[['KPI_T', 'KPI_K', 'KPI_D', 'GK', 'GD']] = df.apply(calc, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    names = sorted(df['Tên_2'].dropna().unique())
    sel_name = st.selectbox("🔍 CHỌN THỐNG ĐỐC:", ["---"] + names)
    
    if sel_name != "---":
        d = df[df['Tên_2'] == sel_name].iloc[0]
        
        # Toàn bộ Profile ROK
        st.markdown(f"""
            <div class="rok-card">
                <div class="header-row">
                    <div class="name-section">
                        <div class="p-id">Thống đốc(ID: {d['ID']})</div>
                        <div class="p-name">{sel_name}</div>
                        <div class="p-alliance">Liên minh<br><b>[{d['Liên Minh_2']}]</b></div>
                    </div>
                    
                    <div class="stats-section">
                        <div class="stat-item">
                            <span class="stat-label">Điểm Tiêu Diệt</span>
                            <span class="stat-value">{int(d['Tổng Tiêu Diệt_2']):,}</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-label">Sức mạnh</span>
                            <span class="stat-value">{int(d['Sức Mạnh_2']):,}</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-label">Điểm Chiến Công</span>
                            <span class="stat-value">0</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-label">Chiến công cao nhất</span>
                            <span class="stat-value">---</span>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 3 Vòng tròn KPI phía dưới
        st.write("") # Tạo khoảng cách nhẹ
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="kpi-box"><div class="kpi-label">KPI Tiêu Diệt</div>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi(d['KPI_K'], "#00ffff"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="kpi-box"><div class="kpi-label">KPI Điểm Chết</div>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi(d['KPI_D'], "#ff4b4b"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="kpi-box"><div class="kpi-label">Tổng KPI KvK</div>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi(d['KPI_T'], "#ffd700"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
