import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. GIAO DIỆN NÂNG CẤP (GLASSMORPHISM & LAYER EFFECT) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e6ed; }
    
    /* Khung Profile chính với hiệu ứng nổi */
    .nba-card {
        background: linear-gradient(135deg, rgba(30, 33, 45, 0.8), rgba(15, 18, 26, 0.9));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }

    /* Tên và ID nổi bật */
    .player-name {
        color: #ffffff; font-size: 55px; font-weight: 900; 
        line-height: 1; text-transform: uppercase; letter-spacing: -1px;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .id-tag { 
        display: inline-block;
        background: rgba(0, 212, 255, 0.1);
        color: #00d4ff; padding: 4px 12px; border-radius: 5px;
        font-size: 14px; font-weight: bold; margin-bottom: 35px;
    }
    
    /* Stats Row */
    .stats-container { display: flex; gap: 60px; margin-bottom: 40px; }
    .stat-box { border-left: 3px solid #00d4ff; padding-left: 20px; }
    .stat-label { color: #8899a6; font-size: 12px; text-transform: uppercase; letter-spacing: 2px; }
    .stat-value { color: #ffffff; font-size: 32px; font-weight: 800; display: block; }

    /* Detail Grid */
    .info-grid { display: grid; grid-template-columns: 140px 1fr; gap: 15px; font-size: 15px; }
    .info-label { color: #5c6c7a; font-weight: 600; text-transform: uppercase; }
    .info-val { color: #00d4ff; font-weight: 700; }

    /* Overlay Chart Position - Để biểu đồ nằm đè lên khung */
    .chart-overlay {
        position: absolute;
        right: -20px;
        top: 50%;
        transform: translateY(-50%);
        width: 450px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. QUẢN LÝ NGÔN NGỮ (GIỮ NGUYÊN) ---
col_t, col_l = st.columns([4, 1]) 
with col_l:
    lang = st.radio("LANG:", ["VN", "EN"], horizontal=True, label_visibility="collapsed")

texts = {
    "VN": {
        "header": "🛡️ COMMAND CENTER", "search": "🔍 TRA CỨU:", "select": "--- Chọn tên ---",
        "pow": "Sức mạnh", "tk": "Tổng Kill", "kt": "Mục tiêu Kill", "dt": "Mục tiêu Dead", 
        "ki": "Kill tăng", "di": "Dead tăng", "table": "📋 THỐNG KÊ CHI TIẾT"
    },
    "EN": {
        "header": "🛡️ COMMAND CENTER", "search": "🔍 SEARCH:", "select": "--- Select name ---",
        "pow": "Power", "tk": "Total Kill", "kt": "Target Kill", "dt": "Target Dead", 
        "ki": "Kill inc", "di": "Dead inc", "table": "📋 DETAILED STATISTICS"
    }
}
L = texts[lang]

# --- 4. VẼ BIỂU ĐỒ KPI (TỐI ƯU MÀU SẮC NỔI BẬT) ---
def draw_kpi_rings(total, kill_val, kill_target, dead_val, dead_target):
    k_pct = (kill_val / kill_target * 100) if kill_target > 0 else 0
    d_pct = (dead_val / dead_target * 100) if dead_target > 0 else 0
    
    fig = go.Figure()
    # Vòng KPI Tổng (Vàng Neon)
    fig.add_trace(go.Pie(hole=0.82, values=[total, max(0, 100-total)], marker=dict(colors=['#ffcc00', 'rgba(255,255,255,0.05)']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))
    # Vòng Kill (Xanh Cyan)
    fig.add_trace(go.Pie(hole=0.72, values=[k_pct, max(0, 100-k_pct)], marker=dict(colors=['#00d4ff', 'transparent']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))
    # Vòng Dead (Trắng bạc)
    fig.add_trace(go.Pie(hole=0.62, values=[d_pct, max(0, 100-d_pct)], marker=dict(colors=['#ffffff', 'transparent']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0), height=450,
        annotations=[dict(text=f"<span style='color:#8899a6;font-size:16px'>KPI</span><br><b style='color:white;font-size:45px'>{total}%</b>", x=0.5, y=0.5, showarrow=False)]
    )
    return fig

# --- 5. XỬ LÝ DỮ LIỆU (GIỮ NGUYÊN LOGIC CŨ) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        for d_tmp in [dt, ds]:
            d_tmp['ID'] = d_tmp['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
            d_tmp['Tên'] = d_tmp['Tên'].fillna('Unknown').astype(str).str.strip()
        df = pd.merge(dt.drop_duplicates('ID'), ds.drop_duplicates('ID'), on='ID', suffixes=('_1', '_2'))
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(float)
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
        def get_metrics(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 220e6 if p >= 35e6 else 170e6 if p >= 30e6 else 130e6 if p >= 25e6 else 100e6 if p >= 20e6 else 80e6
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = max(0.0, min(float(r['KI']) / gk, 1.0)) if gk > 0 else 0.0
            pdv = max(0.0, min(float(r['DI']) / gd, 1.0)) if gd > 0 else 0.0
            return pd.Series([round(((pk + pdv) / 2) * 100, 1), gk, gd])
        
        df[['KPI', 'GK', 'GD']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 6. HIỂN THỊ ---
if df is not None:
    names = sorted(df['Tên_2'].unique())
    sel = st.selectbox(L["search"], [L["select"]] + names)
    
    if sel != L["select"]:
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # Bắt đầu Card Profile
        st.markdown(f"""
            <div class="nba-card">
                <div class="player-name">{sel}</div>
                <div class="id-tag">#{d['ID']} | {d['Liên Minh_2']}</div>
                
                <div class="stats-container">
                    <div class="stat-box">
                        <span class="stat-label">{L['pow']}</span>
                        <span class="stat-value">{int(d['Sức Mạnh_2']):,}</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-label">{L['tk']}</span>
                        <span class="stat-value">{int(d['Tổng Tiêu Diệt_2']):,}</span>
                    </div>
                </div>
                
                <div class="info-grid">
                    <span class="info-label">{L['kt']}:</span><span class="info-val">{int(d['GK']):,}</span>
                    <span class="info-label">{L['dt']}:</span><span class="info-val">{int(d['GD']):,}</span>
                    <span class="info-label">Current Status:</span><span class="info-val" style="color:#00ff88">ONLINE COMMAND</span>
                </div>
                
                </div>
        """, unsafe_allow_html=True)
        
        # Sử dụng columns để đặt Plotly nằm đè lên Card thông qua căn chỉnh
        overlay_col1, overlay_col2 = st.columns([1, 1.2])
        with overlay_col2:
            st.markdown('<div style="margin-top: -500px;">', unsafe_allow_html=True) # Kéo biểu đồ lên trên Card
            fig = draw_kpi_rings(d['KPI'], d['KI'], d['GK'], d['DI'], d['GD'])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

    # 7. BẢNG DỮ LIỆU
    st.divider()
    st.subheader(L["table"])
    st.dataframe(df[['Tên_2', 'ID', 'Liên Minh_2', 'KI', 'DI', 'KPI']].rename(columns=lambda x: x.replace('_2','')), use_container_width=True)
