import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="ROK KPI SYSTEM", layout="wide")

# --- 2. CSS STYLE (MÔ PHỎNG HUY HIỆU ROK) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; color: #e0e6ed; }
    .governor-card {
        background: linear-gradient(180deg, #1a202c 0%, #0d1117 100%);
        border-radius: 10px; padding: 20px; border: 1px solid #30363d; margin-bottom: 25px;
    }
    .badge-item {
        background: radial-gradient(circle, #1c212e 0%, #0b0f19 100%);
        border-radius: 15px; padding: 15px; border: 2px solid #2d333b;
        text-align: center; position: relative;
    }
    .glow-gold { border-color: #ffd700; box-shadow: 0 0 15px rgba(255, 215, 0, 0.2); }
    .glow-cyan { border-color: #00d4ff; box-shadow: 0 0 15px rgba(0, 212, 255, 0.2); }
    .glow-red { border-color: #ff4b4b; box-shadow: 0 0 15px rgba(255, 75, 75, 0.2); }
    .badge-label { font-size: 13px; font-weight: 800; text-transform: uppercase; margin-bottom: 5px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ VÒNG TRÒN KPI ---
def draw_kpi_circle(pct, color):
    # Đảm bảo giá trị là float và không lỗi vòng quay
    try:
        val = float(pct)
    except:
        val = 0.0
    display_val = min(max(val, 0.0), 100.0)
    
    fig = go.Figure(go.Pie(
        hole=0.7, values=[display_val, 100 - display_val],
        marker=dict(colors=[color, "#1a1f26"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=5, b=5, l=5, r=5), height=150,
        annotations=[dict(text=f"<b style='color:{color}; font-size:20px'>{val}%</b>", x=0.5, y=0.5, showarrow=False)]
    )
    return fig

# --- 4. DATA LOGIC (SỬA LỖI MERGE ID) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        # Tải dữ liệu
        df_t = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        df_s = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        
        # --- FIX LỖI: Đồng nhất kiểu dữ liệu ID thành chuỗi (String) ---
        for df_tmp in [df_t, df_s]:
            if 'ID' in df_tmp.columns:
                df_tmp['ID'] = df_tmp['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()

        # Merge sau khi đã ép kiểu ID
        df = pd.merge(df_t, df_s, on='ID', suffixes=('_1', '_2'))
        
        # Chuyển đổi các cột số
        cols_to_fix = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in cols_to_fix:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

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
        st.error(f"Lỗi hệ thống: {e}")
        return None

df = load_data()

# --- 5. HIỂN THỊ GIAO DIỆN ---
if df is not None:
    # Ô chọn tên thống đốc
    names = sorted(df['Tên_2'].dropna().unique())
    sel_name = st.selectbox("🔍 TRA CỨU THỐNG ĐỐC:", ["---"] + names)
    
    if sel_name != "---":
        d = df[df['Tên_2'] == sel_name].iloc[0]
        
        # Thẻ thông tin cá nhân
        st.markdown(f"""
            <div class="governor-card">
                <div style="font-size: 35px; font-weight: 900; color: #fff;">{sel_name}</div>
                <div style="color: #00d4ff; font-size: 15px; margin-bottom: 15px;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                <div style="display: flex; gap: 40px;">
                    <div><small style="color:#6a737d">SỨC MẠNH</small><br><b style="font-size:22px">{int(d['Sức Mạnh_2']):,}</b></div>
                    <div><small style="color:#6a737d">TỔNG KILL</small><br><b style="font-size:22px">{int(d['Tổng Tiêu Diệt_2']):,}</b></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 3 Ô Huy hiệu KPI (Theo yêu cầu khoanh đỏ)
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown('<div class="badge-item glow-cyan"><span class="badge-label" style="color:#00d4ff">⚔️ KPI KILL</span>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi_circle(d['KPI_K'], "#00d4ff"), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<p style="margin:0;font-size:12px;color:#889">Mục tiêu: {int(d["GK"]):,}</p></div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div class="badge-item glow-red"><span class="badge-label" style="color:#ff4b4b">💀 KPI DEAD</span>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi_circle(d['KPI_D'], "#ff4b4b"), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<p style="margin:0;font-size:12px;color:#889">Mục tiêu: {int(d["GD"]):,}</p></div>', unsafe_allow_html=True)
            
        with c3:
            st.markdown('<div class="badge-item glow-gold"><span class="badge-label" style="color:#ffd700">🏆 TOTAL KPI</span>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi_circle(d['KPI_Total'], "#ffd700"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('<p style="margin:0;font-size:12px;color:#ffd700">Xếp hạng: S-RANK</p></div>', unsafe_allow_html=True)
