import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="ROK KPI SYSTEM", layout="wide")

# --- 2. CSS CUSTOM (PHONG CÁCH HUY HIỆU ROK) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e6ed; }
    
    /* Khung Profile chính */
    .rok-card {
        background: linear-gradient(135deg, rgba(20, 25, 35, 0.9), rgba(10, 12, 18, 0.95));
        border-radius: 15px;
        padding: 30px;
        border: 1px solid #3d4455;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        margin-bottom: 20px;
    }

    /* Container chứa 3 huy hiệu */
    .badge-container {
        display: flex;
        justify-content: space-around;
        gap: 20px;
        margin-top: 20px;
    }

    /* Style cho từng ô huy hiệu */
    .badge-box {
        text-align: center;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 215, 0, 0.1);
        transition: 0.3s;
        width: 100%;
    }
    .badge-box:hover {
        background: rgba(255, 215, 0, 0.05);
        border-color: rgba(255, 215, 0, 0.4);
        transform: translateY(-5px);
    }

    .badge-title {
        color: #a8b2c1;
        font-size: 14px;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: block;
    }

    .player-header { font-size: 45px; font-weight: 900; color: #fff; margin: 0; }
    .player-id { color: #00d4ff; font-size: 16px; margin-bottom: 20px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ VÒNG TRÒN KPI (STYLE HUY HIỆU) ---
def draw_badge_chart(value, target, color_theme, label):
    # Tính toán %
    pct = round((value / target * 100), 1) if target > 0 else 0
    display_pct = min(pct, 100) # Chỉ hiển thị vòng quay tối đa 100%
    
    # Màu sắc dựa theo theme
    if color_theme == "gold": # Total KPI
        line_color = "#FFD700"
        glow_color = "rgba(255, 215, 0, 0.6)"
    elif color_theme == "cyan": # Kill KPI
        line_color = "#00D4FF"
        glow_color = "rgba(0, 212, 255, 0.6)"
    else: # Dead KPI (Red/Orange)
        line_color = "#FF4B4B"
        glow_color = "rgba(255, 75, 75, 0.6)"

    fig = go.Figure(go.Pie(
        hole=0.75,
        values=[display_pct, max(0, 100-display_pct)],
        marker=dict(colors=[line_color, "rgba(255,255,255,0.05)"]),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0),
        height=180,
        annotations=[
            # Phần trăm ở giữa
            dict(text=f"<b style='color:{line_color}; font-size:24px;'>{pct}%</b>", 
                 x=0.5, y=0.5, showarrow=False),
            # Label nhỏ ở dưới số %
            dict(text=f"<span style='color:#889; font-size:10px;'>{label}</span>", 
                 x=0.5, y=0.2, showarrow=False)
        ]
    )
    return fig

# --- 4. DATA LOGIC (GIỮ NGUYÊN) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        df = pd.merge(dt, ds, on='ID', suffixes=('_1', '_2'))
        
        # Tính toán KI, DI
        df['KI'] = pd.to_numeric(df['Tổng Tiêu Diệt_2'], errors='coerce').fillna(0) - pd.to_numeric(df['Tổng Tiêu Diệt_1'], errors='coerce').fillna(0)
        df['DI'] = pd.to_numeric(df['Điểm Chết_2'], errors='coerce').fillna(0) - pd.to_numeric(df['Điểm Chết_1'], errors='coerce').fillna(0)
        
        def get_targets(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 220e6 if p >= 35e6 else 170e6 if p >= 30e6 else 130e6 if p >= 25e6 else 100e6 if p >= 20e6 else 80e6
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            k_p = round((r['KI'] / gk * 100), 1) if gk > 0 else 0
            d_p = round((r['DI'] / gd * 100), 1) if gd > 0 else 0
            total = round((k_p + d_p) / 2, 1)
            return pd.Series([total, gk, gd])
        
        df[['KPI_Total', 'GK', 'GD']] = df.apply(get_targets, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. GIAO DIỆN HIỂN THỊ ---
if df is not None:
    st.title("🛡️ ROK GOVERNOR COMMAND CENTER")
    sel = st.selectbox("🔍 CHỌN THỐNG ĐỐC:", ["---"] + sorted(df['Tên_2'].unique()))
    
    if sel != "---":
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # 1. Khung Profile phía trên
        st.markdown(f"""
            <div class="rok-card">
                <span class="player-header">{sel}</span>
                <span class="player-id">ID: {d['ID']} | {d['Liên Minh_2']}</span>
                <div style="display: flex; gap: 40px;">
                    <div><small style="color:#889">SỨC MẠNH</small><br><b style="font-size:20px">{int(d['Sức Mạnh_2']):,}</b></div>
                    <div><small style="color:#889">TỔNG KILL</small><br><b style="font-size:20px">{int(d['Tổng Tiêu Diệt_2']):,}</b></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 2. Hàng 3 huy hiệu KPI (Thay thế 3 ô khoanh đỏ)
        badge_col1, badge_col2, badge_col3 = st.columns(3)
        
        with badge_col1:
            st.markdown('<div class="badge-box"><span class="badge-title">⚔️ KPI KILL</span>', unsafe_allow_html=True)
            st.plotly_chart(draw_badge_chart(d['KI'], d['GK'], "cyan", "Tiến độ"), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<small style="color:#5c6c7a">Mục tiêu: {int(d["GK"]):,}</small></div>', unsafe_allow_html=True)
            
        with badge_col2:
            st.markdown('<div class="badge-box"><span class="badge-title">💀 KPI DEAD</span>', unsafe_allow_html=True)
            st.plotly_chart(draw_badge_chart(d['DI'], d['GD'], "red", "Tiến độ"), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<small style="color:#5c6c7a">Mục tiêu: {int(d["GD"]):,}</small></div>', unsafe_allow_html=True)
            
        with badge_col3:
            st.markdown('<div class="badge-box" style="border-color: rgba(255, 215, 0, 0.3); background: rgba(255, 215, 0, 0.05);">'
                        '<span class="badge-title" style="color:#FFD700">🏆 TOTAL KPI</span>', unsafe_allow_html=True)
            st.plotly_chart(draw_badge_chart(d['KPI_Total'], 100, "gold", "Hoàn thành"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('<small style="color:#FFD700">Xếp hạng: S</small></div>', unsafe_allow_html=True)

        st.divider()
        st.dataframe(df[['Tên_2', 'ID', 'KI', 'DI', 'KPI_Total']].sort_values('KPI_Total', ascending=False), use_container_width=True)
