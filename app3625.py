import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS FIX LỖI HIỂN THỊ & GIAO DIỆN NỔI BẬT ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e6ed; }
    
    /* Khung bao toàn bộ Profile */
    .profile-card {
        background: linear-gradient(135deg, #1e212d 0%, #0f121a 100%);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid #00d4ff4d;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }

    .p-name { color: white; font-size: 50px; font-weight: 900; text-transform: uppercase; margin: 0; }
    .p-id { color: #00d4ff; background: #00d4ff1a; padding: 3px 10px; border-radius: 5px; font-size: 14px; display: inline-block; margin: 10px 0 25px 0; }
    
    .s-row { display: flex; gap: 40px; margin-bottom: 25px; }
    .s-item { border-left: 3px solid #ffcc00; padding-left: 15px; }
    .s-label { color: #8899a6; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
    .s-val { color: white; font-size: 28px; font-weight: 800; display: block; }

    .d-grid { font-size: 15px; line-height: 1.8; }
    .d-label { color: #5c6c7a; font-weight: bold; text-transform: uppercase; margin-right: 10px; }
    .d-val { color: #00ff88; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ BIỂU ĐỒ (NEON STYLE) ---
def draw_kpi_rings(total, kill_val, kill_target, dead_val, dead_target):
    k_pct = (kill_val / kill_target * 100) if kill_target > 0 else 0
    d_pct = (dead_val / dead_target * 100) if dead_target > 0 else 0
    fig = go.Figure()
    # Vòng KPI Tổng (Vàng)
    fig.add_trace(go.Pie(hole=0.8, values=[total, max(0, 100-total)], marker=dict(colors=['#ffcc00', '#222']), showlegend=False, hoverinfo='skip'))
    # Vòng Kill (Cyan)
    fig.add_trace(go.Pie(hole=0.7, values=[k_pct, max(0, 100-k_pct)], marker=dict(colors=['#00d4ff', 'transparent']), showlegend=False, hoverinfo='skip'))
    # Vòng Dead (Trắng)
    fig.add_trace(go.Pie(hole=0.6, values=[d_pct, max(0, 100-d_pct)], marker=dict(colors=['#ffffff', 'transparent']), showlegend=False, hoverinfo='skip'))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=350,
        annotations=[dict(text=f"<b style='color:white;font-size:35px'>{total}%</b>", x=0.5, y=0.5, showarrow=False)]
    )
    return fig

# --- 4. TẢI DỮ LIỆU ---
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

# --- 5. HIỂN THỊ CHÍNH ---
if df is not None:
    sel = st.selectbox("🔍 TRA CỨU CHIẾN BINH:", ["--- Chọn tên ---"] + sorted(df['Tên_2'].unique()))
    
    if sel != "--- Chọn tên ---":
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # Bắt đầu bao quanh bằng 1 thẻ div duy nhất cho toàn bộ Profile
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        
        # Chia 2 cột bên trong Card
        col_info, col_chart = st.columns([1.5, 1])
        
        with col_info:
            st.markdown(f"""
                <div class="p-name">{sel}</div>
                <div class="p-id">#{d['ID']} | {d['Liên Minh_2']}</div>
                <div class="s-row">
                    <div class="s-item"><span class="s-label">Sức Mạnh</span><span class="s-val">{int(d['Sức Mạnh_2']):,}</span></div>
                    <div class="s-item"><span class="s-label">Tổng Kill</span><span class="s-val">{int(d['Tổng Tiêu Diệt_2']):,}</span></div>
                </div>
                <div class="d-grid">
                    <span class="d-label">Mục tiêu Kill:</span><span class="d-val" style="color:white">{int(d['GK']):,}</span><br>
                    <span class="d-label">Mục tiêu Dead:</span><span class="d-val" style="color:white">{int(d['GD']):,}</span><br>
                    <span class="d-label">Trạng thái:</span><span class="d-val">ONLINE COMMAND</span>
                </div>
            """, unsafe_allow_html=True)
            
        with col_chart:
            # Vẽ biểu đồ trực tiếp vào cột bên phải
            fig = draw_kpi_rings(d['KPI'], d['KI'], d['GK'], d['DI'], d['GD'])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
        st.markdown('</div>', unsafe_allow_html=True) # Đóng profile-card

        # Thanh tiến độ phụ bên dưới Card
        st.write(f"📊 **Tiến độ Kill:** {int(d['KI']):,} / {int(d['GK']):,}")
        st.progress(max(0.0, min(float(d['KI']) / d['GK'], 1.0)) if d['GK'] > 0 else 0.0)
        st.write(f"📊 **Tiến độ Dead:** {int(d['DI']):,} / {int(d['GD']):,}")
        st.progress(max(0.0, min(float(d['DI']) / d['GD'], 1.0)) if d['GD'] > 0 else 0.0)
