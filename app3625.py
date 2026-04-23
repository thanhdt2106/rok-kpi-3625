import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="ROK PROFILE KVK", layout="wide")

# --- 2. CSS TẠO Ô VUÔNG NỀN MỜ VÀ LAYOUT ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    
    /* Khung xanh bao quanh toàn bộ */
    .main-container {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 12px;
        padding: 25px;
        border: 1px solid #3eb5e5;
    }

    .p-name { font-size: 32px; font-weight: 800; color: white; margin-bottom: 5px; }
    .p-sub { font-size: 14px; color: #b0d4e3; margin-bottom: 20px; }

    /* Ô vuông nền mờ cho thông số */
    .stat-box {
        background: rgba(0, 0, 0, 0.3);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 10px;
        height: 80px;
    }
    .stat-label { color: #b0d4e3; font-size: 11px; text-transform: uppercase; display: block; }
    .stat-val { color: white; font-size: 20px; font-weight: 700; margin-top: 5px; display: block; }

    /* Khung nền mờ cho phần KPI */
    .kpi-area {
        background: rgba(0, 0, 0, 0.2);
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
    }
    .kpi-title { font-size: 12px; font-weight: bold; color: white; margin-bottom: 10px; text-align: center; }
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
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=120,
        annotations=[dict(text=f"<b style='color:white; font-size:16px'>{pct}%</b>", x=0.5, y=0.5, showarrow=False)]
    )
    return fig

# --- 4. XỬ LÝ DỮ LIỆU ---
@st.cache_data(ttl=30)
def load_data():
    try:
        sid = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
        u1, u2 = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=731741617', f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=371969335'
        df1, df2 = pd.read_csv(u1), pd.read_csv(u2)
        df1['ID'] = df1['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df2['ID'] = df2['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df = pd.merge(df1, df2, on='ID', suffixes=('_1', '_2'))
        
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

# --- 5. HIỂN THỊ GIAO DIỆN ---
if df is not None:
    names = sorted(df['Tên_2'].dropna().unique())
    sel_name = st.selectbox("🔍 TRA CỨU THỐNG ĐỐC:", ["---"] + names)
    
    if sel_name != "---":
        d = df[df['Tên_2'] == sel_name].iloc[0]
        
        # Mở khung xanh chính
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # Tiêu đề
        st.markdown(f'<div class="p-name">{sel_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="p-sub">Thống đốc(ID: {d["ID"]}) | Liên minh: [{d["Liên Minh_2"]}]</div>', unsafe_allow_html=True)
        
        # Lưới thông số (Mỗi ô 1 div mờ riêng)
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown(f'<div class="stat-box"><span class="stat-label">Điểm Tiêu Diệt</span><span class="stat-val">{int(d["Tổng Tiêu Diệt_2"]):,}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stat-box"><span class="stat-label">Sức Mạnh</span><span class="stat-val">{int(d["Sức Mạnh_2"]):, }</span></div>', unsafe_allow_html=True)
        with col_right:
            st.markdown(f'<div class="stat-box"><span class="stat-label">Điểm Chiến Công</span><span class="stat-val">0</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stat-box"><span class="stat-label">Chiến Công Cao Nhất</span><span class="stat-val">---</span></div>', unsafe_allow_html=True)
        
        # Phần KPI nằm trong khung mờ phía dưới (Vẫn nằm trong khung xanh)
        st.markdown('<div class="kpi-area"><div class="kpi-title">TIẾN ĐỘ KPI KVK</div>', unsafe_allow_html=True)
        k_col1, k_col2, k_col3 = st.columns(3)
        with k_col1:
            st.plotly_chart(draw_kpi(d['KPI_K'], "#00ffff"), use_container_width=True, config={'displayModeBar': False})
        with k_col2:
            st.plotly_chart(draw_kpi(d['KPI_D'], "#ff4b4b"), use_container_width=True, config={'displayModeBar': False})
        with k_col3:
            st.plotly_chart(draw_kpi(d['KPI_T'], "#ffd700"), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True) # Đóng kpi-area
        
        st.markdown('</div>', unsafe_allow_html=True) # Đóng main-container
