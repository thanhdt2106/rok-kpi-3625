import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="ROK PROFILE PRO", layout="wide")

# --- 2. CSS NỀN XANH BAO QUANH TOÀN BỘ ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    
    /* Khung xanh bao quanh tất cả */
    .main-container {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #3eb5e5;
        color: white;
    }

    /* Tên và ID */
    .p-name { font-size: 35px; font-weight: 800; text-transform: uppercase; margin: 0; }
    .p-id { font-size: 14px; color: #b0d4e3; margin-bottom: 20px; }

    /* Ô thông số nền mờ */
    .stat-box {
        background: rgba(0, 0, 0, 0.3);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-bottom: 10px;
    }
    .s-label { color: #b0d4e3; font-size: 12px; text-transform: uppercase; display: block; }
    .s-value { font-size: 22px; font-weight: 700; color: white; display: block; }

    /* Khung biểu đồ */
    .kpi-box {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ BIỂU ĐỒ (Sửa lỗi hiển thị) ---
def draw_kpi(pct, color, title):
    val = min(max(float(pct), 0.0), 100.0)
    fig = go.Figure(go.Pie(
        hole=0.7, values=[val, 100 - val],
        marker=dict(colors=[color, "rgba(255,255,255,0.05)"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        title={'text': title, 'y':0.95, 'x':0.5, 'xanchor':'center', 'font':{'color':'white','size':14}},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=30, b=0, l=10, r=10), height=180,
        annotations=[dict(text=f"{pct}%", x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=18, fontWeight='bold'))]
    )
    return fig

# --- 4. DATA LOGIC ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        df_t = pd.read_csv(URL_T)
        df_s = pd.read_csv(URL_S)
        df_t.columns = df_t.columns.str.strip()
        df_s.columns = df_s.columns.str.strip()
        
        df_t['ID'] = df_t['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df_s['ID'] = df_s['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        
        df = pd.merge(df_t, df_s, on='ID', suffixes=('_1', '_2'))
        
        # Chuyển đổi số an toàn
        cols_to_fix = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in cols_to_fix:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', ''), errors='coerce').fillna(0)

        def calc(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            gd = 400e3 if p >= 30e6 else 200e3
            ki = max(0, r['Tổng Tiêu Diệt_2'] - r['Tổng Tiêu Diệt_1'])
            di = max(0, r['Điểm Chết_2'] - r['Điểm Chết_1'])
            kp = round((ki/gk*100), 1) if gk > 0 else 0
            dp = round((di/gd*100), 1) if gd > 0 else 0
            return pd.Series([round((kp+dp)/2, 1), kp, dp])
        
        df[['KPI_T', 'KPI_K', 'KPI_D']] = df.apply(calc, axis=1)
        return df
    except Exception as e:
        st.error(f"Lỗi nạp dữ liệu: {e}")
        return None

df = load_data()

# --- 5. HIỂN THỊ GIAO DIỆN ---
if df is not None:
    names = sorted(df['Tên_2'].dropna().unique())
    sel_name = st.selectbox("🔍 TRA CỨU CHIẾN BINH:", ["---"] + names)
    
    if sel_name != "---":
        d = df[df['Tên_2'] == sel_name].iloc[0]
        
        # BẮT ĐẦU KHUNG XANH BAO QUANH
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # Header: Tên & ID
        st.markdown(f'<p class="p-name">{sel_name}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="p-id">Thống đốc ID: {d["ID"]} | Liên minh: [{d["Liên Minh_2"]}]</p>', unsafe_allow_html=True)
        
        # Hàng 1: Các ô thông số (Sức mạnh, Kill...)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="stat-box"><span class="s-label">Tiêu Diệt</span><span class="s-value">{int(d["Tổng Tiêu Diệt_2"]):,}</span></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="stat-box"><span class="s-label">Sức Mạnh</span><span class="s-value">{int(d["Sức Mạnh_2"]):,}</span></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="stat-box"><span class="s-label">Điểm Chết</span><span class="s-value">{int(d["Điểm Chết_2"]):,}</span></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="stat-box"><span class="s-label">Xếp hạng</span><span class="s-value">S-RANK</span></div>', unsafe_allow_html=True)
        
        # Hàng 2: Khu vực Biểu đồ KPI
        st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; font-size:12px; font-weight:bold; color:#b0d4e3;">TIẾN ĐỘ CHIẾN DỊCH KVK</p>', unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.plotly_chart(draw_kpi(d['KPI_K'], "#00ffff", "KPI KILL"), use_container_width=True, config={'displayModeBar': False})
        with k2: st.plotly_chart(draw_kpi(d['KPI_D'], "#ff4b4b", "KPI DEAD"), use_container_width=True, config={'displayModeBar': False})
        with k3: st.plotly_chart(draw_kpi(d['KPI_T'], "#ffd700", "TỔNG KPI"), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # KẾT THÚC KHUNG XANH
