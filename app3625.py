import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="ROK PROFILE PRO", layout="wide")

# --- 2. CSS TẠO Ô VUÔNG NỀN MỜ & ĐƯA KPI VÀO KHUNG XANH ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    
    /* Khung xanh chủ đạo */
    .rok-main-card {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #3eb5e5;
        color: white;
    }

    /* Bố cục header */
    .header-info { margin-bottom: 20px; }
    .p-id { font-size: 13px; color: #b0d4e3; }
    .p-name { font-size: 32px; font-weight: 800; text-transform: uppercase; margin: 5px 0; }
    .p-alliance { font-size: 16px; font-weight: bold; }

    /* Lưới các ô vuông nền mờ */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-bottom: 20px;
    }
    
    .stat-square {
        background: rgba(0, 0, 0, 0.25); /* Nền mờ riêng biệt */
        padding: 12px;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .s-label { color: #b0d4e3; font-size: 12px; text-transform: uppercase; display: block; margin-bottom: 4px; }
    .s-value { font-size: 20px; font-weight: 700; color: white; }

    /* Khung chứa KPI nằm trong nền xanh */
    .kpi-inner-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        background: rgba(0, 0, 0, 0.15);
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
    .kpi-title { font-size: 11px; font-weight: bold; color: #e0e0e0; margin-bottom: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ BIỂU ĐỒ TRONG SUỐT ---
def draw_kpi(pct, color):
    val = min(max(float(pct), 0.0), 100.0)
    fig = go.Figure(go.Pie(
        hole=0.75, values=[val, 100 - val],
        marker=dict(colors=[color, "rgba(255,255,255,0.1)"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0), height=110,
        annotations=[dict(text=f"<b style='color:white; font-size:15px'>{pct}%</b>", x=0.5, y=0.5, showarrow=False)]
    )
    return fig

# --- 4. DATA LOGIC (Giữ nguyên phần xử lý dữ liệu của bạn) ---
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
            ki, di = r['Tổng Tiêu Diệt_2'] - r['Tổng Tiêu Diệt_1'], r['Điểm Chết_2'] - r['Điểm Chết_1']
            kp, dp = round((ki/gk*100), 1) if gk > 0 else 0, round((di/gd*100), 1) if gd > 0 else 0
            return pd.Series([round((kp+dp)/2, 1), kp, dp])
        
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
        
        # Toàn bộ nội dung nằm trong 1 Card xanh duy nhất
        st.markdown(f"""
            <div class="rok-main-card">
                <div class="header-info">
                    <div class="p-id">Thống đốc(ID: {d['ID']})</div>
                    <div class="p-name">{sel_name}</div>
                    <div class="p-alliance">Liên minh: [{d['Liên Minh_2']}]</div>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-square"><span class="s-label">Điểm Tiêu Diệt</span><span class="s-value">{int(d['Tổng Tiêu Diệt_2']):,}</span></div>
                    <div class="stat-square"><span class="s-label">Sức Mạnh</span><span class="s-value">{int(d['Sức Mạnh_2']):,}</span></div>
                    <div class="stat-square"><span class="s-label">Điểm Chiến Công</span><span class="s-value">0</span></div>
                    <div class="stat-square"><span class="s-label">Chiến Công Cao Nhất</span><span class="s-value">---</span></div>
                </div>
                
                <div style="font-size: 12px; font-weight: bold; margin-bottom: 5px;">TIẾN ĐỘ KVK</div>
                <div class="kpi-inner-row">
                    <div><div class="kpi-title">KPI KILL</div><div id="k1"></div></div>
                    <div><div class="kpi-title">KPI DEAD</div><div id="k2"></div></div>
                    <div><div class="kpi-title">TỔNG KPI</div><div id="k3"></div></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Chèn biểu đồ vào trong khung xanh bằng columns lồng (visual trick)
        # Sử dụng container để đẩy biểu đồ lên trên Card
        st.markdown('<style> div[data-testid="stVerticalBlock"] > div:nth-child(5) {margin-top: -165px;}</style>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.plotly_chart(draw_kpi(d['KPI_K'], "#00ffff"), use_container_width=True, config={'displayModeBar': False})
        with c2: st.plotly_chart(draw_kpi(d['KPI_D'], "#ff4b4b"), use_container_width=True, config={'displayModeBar': False})
        with c3: st.plotly_chart(draw_kpi(d['KPI_T'], "#ffd700"), use_container_width=True, config={'displayModeBar': False})
