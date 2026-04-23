import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS NÂNG CẤP (LAYOUT ĐỒNG NHẤT) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e6ed; }
    
    /* Khung card tổng hợp */
    .nba-profile-card {
        background: linear-gradient(135deg, rgba(35, 38, 50, 0.95), rgba(15, 18, 26, 0.98));
        border-radius: 25px;
        padding: 40px;
        border: 1px solid rgba(0, 212, 255, 0.3);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7);
        display: grid;
        grid-template-columns: 1.5fr 1fr; /* Chia đôi khung: Trái thông tin, Phải biểu đồ */
        gap: 20px;
        align-items: center;
        position: relative;
    }

    .player-name {
        color: #ffffff; font-size: 55px; font-weight: 900; 
        line-height: 1; text-transform: uppercase; letter-spacing: -2px;
        margin-bottom: 5px;
    }
    .id-sub { 
        color: #00d4ff; font-weight: bold; background: rgba(0, 212, 255, 0.1);
        padding: 5px 15px; border-radius: 8px; display: inline-block; margin-bottom: 30px;
    }
    
    .main-stats { display: flex; gap: 50px; margin-bottom: 30px; }
    .stat-node { border-left: 4px solid #ffcc00; padding-left: 15px; }
    .stat-label { color: #8899a6; font-size: 12px; text-transform: uppercase; }
    .stat-val { color: #ffffff; font-size: 32px; font-weight: 800; }

    .detail-list { font-size: 15px; color: #ccd6f6; }
    .detail-item { margin-bottom: 8px; }
    .detail-bold { color: #00ff88; font-weight: bold; margin-right: 10px; }

    /* Container cho biểu đồ bên trong khung */
    .chart-box { display: flex; justify-content: center; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ BIỂU ĐỒ (NEON STYLE) ---
def draw_kpi_rings(total, kill_val, kill_target, dead_val, dead_target):
    k_pct = (kill_val / kill_target * 100) if kill_target > 0 else 0
    d_pct = (dead_val / dead_target * 100) if dead_target > 0 else 0
    fig = go.Figure()
    # Vòng KPI Tổng
    fig.add_trace(go.Pie(hole=0.8, values=[total, max(0, 100-total)], marker=dict(colors=['#ffcc00', 'rgba(255,255,255,0.05)']), showlegend=False, hoverinfo='skip'))
    # Vòng Kill & Dead (Nhỏ dần vào trong)
    fig.add_trace(go.Pie(hole=0.7, values=[k_pct, max(0, 100-k_pct)], marker=dict(colors=['#00d4ff', 'transparent']), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Pie(hole=0.6, values=[d_pct, max(0, 100-d_pct)], marker=dict(colors=['#ffffff', 'transparent']), showlegend=False, hoverinfo='skip'))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=380,
        annotations=[dict(text=f"<b style='color:white;font-size:40px'>{total}%</b>", x=0.5, y=0.5, showarrow=False)]
    )
    return fig

# --- 4. TẢI DỮ LIỆU (KHÔNG ĐỔI) ---
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

# --- 5. HIỂN THỊ ---
if df is not None:
    sel = st.selectbox("🔍 TRA CỨU CHIẾN BINH:", ["--- Chọn tên ---"] + sorted(df['Tên_2'].unique()))
    
    if sel != "--- Chọn tên ---":
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # SỬ DỤNG MỘT CONTAINER DUY NHẤT ĐỂ ĐẢM BẢO BIỂU ĐỒ NẰM TRONG KHUNG
        with st.container():
            # Mở khung Card
            st.markdown(f"""
                <div class="nba-profile-card">
                    <div>
                        <div class="player-name">{sel}</div>
                        <div class="id-sub">#{d['ID']} | {d['Liên Minh_2']}</div>
                        
                        <div class="main-stats">
                            <div class="stat-node">
                                <span class="stat-label">SỨC MẠNH</span><br>
                                <span class="stat-val">{int(d['Sức Mạnh_2']):,}</span>
                            </div>
                            <div class="stat-node">
                                <span class="stat-label">TỔNG KILL</span><br>
                                <span class="stat-val">{int(d['Tổng Tiêu Diệt_2']):,}</span>
                            </div>
                        </div>
                        
                        <div class="detail-list">
                            <div class="detail-item"><span class="detail-bold">MỤC TIÊU KILL:</span> {int(d['GK']):,}</div>
                            <div class="detail-item"><span class="detail-bold">MỤC TIÊU DEAD:</span> {int(d['GD']):,}</div>
                            <div class="detail-item"><span class="detail-bold">TRẠNG THÁI:</span> <span style="color:#00ff88">ONLINE COMMAND</span></div>
                        </div>
                    </div>
                    <div id="chart-holder">
            """, unsafe_allow_html=True)
            
            # Chèn biểu đồ Plotly vào cột bên phải của Grid
            fig = draw_kpi_rings(d['KPI'], d['KI'], d['GK'], d['DI'], d['GD'])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # Đóng khung Card
            st.markdown("</div></div>", unsafe_allow_html=True)

        # Thanh tiến độ phụ bên dưới
        st.write(f"📊 **Tiến độ Kill:** {int(d['KI']):,} / {int(d['GK']):,}")
        st.progress(max(0.0, min(float(d['KI']) / d['GK'], 1.0)) if d['GK'] > 0 else 0.0)
        st.write(f"📊 **Tiến độ Dead:** {int(d['DI']):,} / {int(d['GD']):,}")
        st.progress(max(0.0, min(float(d['DI']) / d['GD'], 1.0)) if d['GD'] > 0 else 0.0)
