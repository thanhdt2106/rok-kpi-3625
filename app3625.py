import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="ROK PROFILE SYSTEM", layout="wide")

# --- 2. CSS CHUẨN GIAO DIỆN HỒ SƠ ROK ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Khung xanh đặc trưng của ROK */
    .rok-container {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 12px;
        padding: 25px;
        border: 2px solid #3eb5e5;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6);
        color: white;
        font-family: 'sans-serif';
    }

    /* Bố cục Header */
    .p-label { color: #b0d4e3; font-size: 14px; margin-bottom: 2px; }
    .p-name { font-size: 36px; font-weight: 800; line-height: 1.1; margin-bottom: 5px; }
    .p-sub { font-size: 15px; font-weight: 600; margin-bottom: 15px; color: #ffffff; }

    /* Lưới chỉ số bên phải */
    .stat-box { display: flex; flex-direction: column; margin-bottom: 15px; }
    .stat-label { color: #b0d4e3; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }
    .stat-value { font-size: 24px; font-weight: 700; color: #ffffff; }

    /* Khung 3 ô vòng tròn KPI */
    .badge-area {
        background: rgba(0, 0, 0, 0.15);
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .badge-title { font-size: 11px; color: #e0e0e0; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ VÒNG TRÒN KPI ---
def draw_kpi_circle(pct, color):
    try:
        val = float(pct)
    except:
        val = 0.0
    display_val = min(max(val, 0.0), 100.0)
    
    fig = go.Figure(go.Pie(
        hole=0.72, values=[display_val, 100 - display_val],
        marker=dict(colors=[color, "rgba(255,255,255,0.08)"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=130,
        annotations=[dict(text=f"<b style='color:white; font-size:18px'>{val}%</b>", x=0.5, y=0.5, showarrow=False)]
    )
    return fig

# --- 4. DATA LOGIC (SỬA LỖI SORT & MERGE) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        df_t = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        df_s = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        
        # Đồng nhất ID
        for df_tmp in [df_t, df_s]:
            df_tmp['ID'] = df_tmp['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()

        df = pd.merge(df_t, df_s, on='ID', suffixes=('_1', '_2'))
        
        # Chuyển đổi số an toàn
        num_cols = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in num_cols:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
        def calc_kpi(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            gd = 400e3 if p >= 30e6 else 200e3
            kp = round((r['KI'] / gk * 100), 1) if gk > 0 else 0
            dp = round((r['DI'] / gd * 100), 1) if gd > 0 else 0
            return pd.Series([round((kp + dp) / 2, 1), kp, dp, gk, gd])
        
        df[['KPI_Total', 'KPI_K', 'KPI_D', 'GK', 'GD']] = df.apply(calc_kpi, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. GIAO DIỆN ---
if df is not None:
    # Fix lỗi sorted bằng cách dropna()
    names = sorted(df['Tên_2'].dropna().unique())
    sel_name = st.selectbox("🔍 TRA CỨU CHIẾN BINH:", ["---"] + names)
    
    if sel_name != "---":
        d = df[df['Tên_2'] == sel_name].iloc[0]
        
        st.markdown(f"""
            <div class="rok-container">
                <div style="display: flex; justify-content: space-between;">
                    <div style="flex: 1.2;">
                        <div class="p-label">Thống đốc(ID: {d['ID']})</div>
                        <div class="p-name">{sel_name}</div>
                        <div class="p-sub">Liên minh: [{d['Liên Minh_2']}]</div>
                        <div style="margin-top: 10px;">
                            <div class="p-label">Nền văn minh:</div>
                            <div style="font-weight:bold; font-size:18px;">🔱 Pháp</div>
                        </div>
                    </div>
                    
                    <div style="flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div class="stat-box">
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

                <div class="badge-area">
                    <div style="display: flex; justify-content: space-around; gap: 10px;">
                        <div style="text-align:center; flex:1;">
                            <div class="badge-title">KPI TIÊU DIỆT</div>
                            <div id="chart_k"></div>
                        </div>
                        <div style="text-align:center; flex:1;">
                            <div class="badge-title">KPI ĐIỂM CHẾT</div>
                            <div id="chart_d"></div>
                        </div>
                        <div style="text-align:center; flex:1;">
                            <div class="badge-title">TỔNG KPI KVK</div>
                            <div id="chart_t"></div>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Chèn biểu đồ vào đúng vị trí bằng columns của Streamlit để không bị lỗi layout
        kpi_cols = st.columns(3)
        with kpi_cols[0]: st.plotly_chart(draw_kpi_circle(d['KPI_K'], "#00ffff"), use_container_width=True, config={'displayModeBar': False})
        with kpi_cols[1]: st.plotly_chart(draw_kpi_circle(d['KPI_D'], "#ff4b4b"), use_container_width=True, config={'displayModeBar': False})
        with kpi_cols[2]: st.plotly_chart(draw_kpi_circle(d['KPI_Total'], "#ffd700"), use_container_width=True, config={'displayModeBar': False})
