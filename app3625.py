import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="ROK PROFILE COMMAND CENTER", layout="wide")

# --- 2. ADVANCED ROK-STYLE CSS (FIX LỖI F-STRING VÀ BỐ CỤC TUYỆT ĐỐI) ---
# Tách CSS sang một khối markdown riêng để đảm bảo tính ổn định
st.markdown("""
    <style>
    /* Tổng thể nền tối */
    .stApp { background-color: #0d1117; color: white; }
    
    /* Container chính màu xanh hồ sơ ROK với viền sáng */
    .rok-profile-card {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 8px;
        padding: 30px;
        border: 2px solid #3eb5e5;
        box-shadow: 0 5px 20px rgba(0,0,0,0.7);
        font-family: 'sans-serif';
    }

    /* Vị trí Tên và ID (Góc trên bên trái) */
    .p-header { font-size: 38px; font-weight: 800; text-transform: uppercase; margin: 0; line-height: 1.1; }
    .p-id-label { font-size: 14px; color: #b0d4e3; margin-top: -5px; }

    /* Layout Liên minh, Nền văn minh... (Chia cột dưới Tên) */
    .p-sub-layout { display: flex; gap: 40px; margin-top: 10px; font-size: 15px; color: #ffffff; }
    .p-sub-label { color: #b0d4e3; font-weight: bold; margin-right: 8px; }

    /* Lưới các ô vuông thông số chính (Góc trên bên phải) */
    .p-stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; width: 100%; }
    .p-stat-item {
        background: rgba(0, 0, 0, 0.2);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stat-label-nba { color: #b0d4e3; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }
    .stat-value-nba { font-size: 26px; font-weight: 700; color: #ffffff; }

    /* Hàng chứa 3 vòng tròn KPI (Thay thế vị trí huy hiệu KvK) */
    .kpi-container {
        margin-top: 40px;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }
    .badge-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .badge-title { font-size: 12px; font-weight: 800; color: #e0e0e0; margin-bottom: 5px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ BIỂU ĐỒ (NEON STYLE CHUẨN KVK) ---
def create_neon_gauge(pct, color):
    try:
        val = float(pct)
    except:
        val = 0.0
    display_val = min(max(val, 0.0), 100.0)
    
    fig = go.Figure(go.Pie(
        hole=0.72, values=[display_val, max(0, 100-display_val)],
        marker=dict(colors=[color, "rgba(255,255,255,0.08)"]),
        showlegend=False, hoverinfo='skip'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=140,
        annotations=[dict(text=f"<b style='color:white; font-size:18px'>{pct}%</b>", x=0.5, y=0.5, showarrow=False)]
    )
    return fig

# --- 4. DATA LOGIC (ÉP KIỂU ĐỂ TRÁNH LỖI MERGE) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        # Ép ID về string để tránh lỗi merge
        dt['ID'] = dt['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        ds['ID'] = ds['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df = pd.merge(dt, ds, on='ID', suffixes=('_1', '_2'))
        
        # Chuyển đổi các cột số
        cols_to_fix = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in cols_to_fix:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
        def calculate_kpi(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            gd = 400e3 if p >= 30e6 else 200e3
            pk = round((r['KI'] / gk * 100), 1) if gk > 0 else 0
            pd_v = round((r['DI'] / gd * 100), 1) if gd > 0 else 0
            return pd.Series([round((pk + pd_v) / 2, 1), pk, pd_v, gk, gd])
        
        df[['KPI_Total', 'KPI_K', 'KPI_D', 'GK', 'GD']] = df.apply(calculate_kpi, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. GIAO DIỆN HIỂN THỊ ---
if df is not None:
    names = sorted(df['Tên_2'].dropna().unique())
    sel_name = st.selectbox("🔍 CHỌN THỐNG ĐỐC:", ["---"] + names)
    
    if sel_name != "---":
        d = df[df['Tên_2'] == sel_name].iloc[0]
        
        # PHẦN 1: BẮT ĐẦU CARD HỒ SƠ ROK
        # layout Flex để phân chia Tên (Trái) và Chỉ số (Phải)
        st.markdown(f'<div class="rok-profile-card">', unsafe_allow_html=True)
        
        # Tạo 2 cột chính trong header
        col_name, col_stats = st.columns([1.2, 1])
        
        # Cột Trái: Tên, ID, Liên minh
        with col_name:
            st.markdown(f"""
                <div class="p-header">{sel_name}</div>
                <div class="p-id-label">Thống đốc(ID: {d['ID']})</div>
                <div class="p-sub-layout">
                    <div><span class="p-sub-label">Liên minh:</span>[{d['Liên Minh_2']}]</div>
                    <div><span class="p-sub-label">Văn minh:</span>⚜️ Pháp</div>
                </div>
            """, unsafe_allow_html=True)
            
        # Cột Phải: Sức mạnh & Tiêu diệt (Lưới các ô vuông)
        with col_stats:
            st.markdown('<div class="p-stats-grid">', unsafe_allow_html=True)
            st.markdown(f'<div class="p-stat-item"><div class="stat-label-nba">Điểm Tiêu Diệt</div><div class="stat-value-nba">{int(d["Tổng Tiêu Diệt_2"]):,}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="p-stat-item"><div class="stat-label-nba">Sức mạnh</div><div class="stat-value-nba">{int(d["Sức Mạnh_2"]):,}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="p-stat-item"><div class="stat-label-nba">Điểm Chiến Công</div><div class="stat-value-nba">0</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="p-stat-item"><div class="stat-label-nba">Chiến công cao nhất</div><div class="stat-value-nba">---</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # PHẦN 2: 3 VÒNG TRÒN KPI (Thay thế vị trí huy hiệu KvK)
        st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
        
        c_k, c_d, c_t = st.columns(3)
        with c_k:
            st.markdown('<div class="badge-card"><div class="badge-title">KPI TIÊU DIỆT (⚔️)</div>', unsafe_allow_html=True)
            st.plotly_chart(create_neon_gauge(d['KPI_K'], "#00ffff"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with c_d:
            st.markdown('<div class="badge-card"><div class="badge-title">KPI ĐIỂM CHẾT (💀)</div>', unsafe_allow_html=True)
            st.plotly_chart(create_neon_gauge(d['KPI_D'], "#ff4b4b"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with c_t:
            st.markdown('<div class="badge-card"><div class="badge-title">TỔNG KPI (🏆)</div>', unsafe_allow_html=True)
            st.plotly_chart(create_neon_gauge(d['KPI_Total'], "#ffd700"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True) # Đóng toàn bộ card
