import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="ROK KPI SYSTEM", layout="wide")

# --- 2. CSS STYLE (MÔ PHỎNG HUY HIỆU ROK) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; color: #e0e6ed; }
    
    /* Khung Profile Thống đốc */
    .governor-card {
        background: linear-gradient(180deg, #1a202c 0%, #0d1117 100%);
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #30363d;
        margin-bottom: 25px;
    }

    /* Container cho 3 huy hiệu */
    .badge-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-top: 10px;
    }

    /* Từng ô huy hiệu */
    .badge-item {
        background: radial-gradient(circle, #1c212e 0%, #0b0f19 100%);
        border-radius: 15px;
        padding: 15px;
        border: 2px solid #2d333b;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    /* Hiệu ứng phát sáng cho từng loại huy hiệu */
    .glow-gold { border-color: #ffd700; box-shadow: 0 0 15px rgba(255, 215, 0, 0.2); }
    .glow-cyan { border-color: #00d4ff; box-shadow: 0 0 15px rgba(0, 212, 255, 0.2); }
    .glow-red { border-color: #ff4b4b; box-shadow: 0 0 15px rgba(255, 75, 75, 0.2); }

    .badge-label {
        font-size: 13px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ VÒNG TRÒN KPI ---
def draw_kpi_circle(pct, color):
    # Đảm bảo giá trị hiển thị vòng tròn không vượt quá 100% để tránh lỗi vẽ
    display_val = min(max(float(pct), 0.0), 100.0)
    
    fig = go.Figure(go.Pie(
        hole=0.7,
        values=[display_val, 100 - display_val],
        marker=dict(colors=[color, "#1a1f26"]),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=5, b=5, l=5, r=5),
        height=150,
        annotations=[dict(
            text=f"<b style='color:{color}; font-size:22px'>{pct}%</b>",
            x=0.5, y=0.5, showarrow=False
        )]
    )
    return fig

# --- 4. DATA LOGIC (FIX LỖI TRUY XUẤT) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        df = pd.merge(dt, ds, on='ID', suffixes=('_1', '_2'))
        
        # Chuyển đổi dữ liệu số an toàn
        for col in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
        def calculate_kpi(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 220e6 if p >= 35e6 else 170e6 if p >= 30e6 else 130e6 if p >= 25e6 else 100e6 if p >= 20e6 else 80e6
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            k_pct = round((r['KI'] / gk * 100), 1) if gk > 0 else 0
            d_pct = round((r['DI'] / gd * 100), 1) if gd > 0 else 0
            total = round((k_pct + d_pct) / 2, 1)
            return pd.Series([total, k_pct, d_pct, gk, gd])
        
        df[['KPI_Total', 'KPI_K', 'KPI_D', 'GK', 'GD']] = df.apply(calculate_kpi, axis=1)
        return df
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu: {e}")
        return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    sel_name = st.selectbox("🔍 TÌM KIẾM THỐNG ĐỐC:", ["---"] + sorted(df['Tên_2'].unique()))
    
    if sel_name != "---":
        d = df[df['Tên_2'] == sel_name].iloc[0]
        
        # Header Profile
        st.markdown(f"""
            <div class="governor-card">
                <div style="font-size: 32px; font-weight: 900; color: #fff;">{sel_name}</div>
                <div style="color: #00d4ff; font-size: 14px; margin-bottom: 15px;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                <div style="display: flex; gap: 30px;">
                    <div><small style="color:#6a737d">SỨC MẠNH</small><br><b>{int(d['Sức Mạnh_2']):,}</b></div>
                    <div><small style="color:#6a737d">TỔNG TIÊU DIỆT</small><br><b>{int(d['Tổng Tiêu Diệt_2']):,}</b></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Layout 3 ô huy hiệu
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown('<div class="badge-item glow-cyan"><span class="badge-label" style="color:#00d4ff">⚔️ KPI KILL</span>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi_circle(d['KPI_K'], "#00d4ff"), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<small>Target: {int(d["GK"]):,}</small></div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div class="badge-item glow-red"><span class="badge-label" style="color:#ff4b4b">💀 KPI DEAD</span>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi_circle(d['KPI_D'], "#ff4b4b"), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<small>Target: {int(d["GD"]):,}</small></div>', unsafe_allow_html=True)
            
        with c3:
            st.markdown('<div class="badge-item glow-gold"><span class="badge-label" style="color:#ffd700">🏆 TOTAL KPI</span>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi_circle(d['KPI_Total'], "#ffd700"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('<small>Xếp hạng: COMMANDER</small></div>', unsafe_allow_html=True)
