import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS NÂNG CẤP (GOM TẤT CẢ VÀO 1 KHUNG) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e6ed; }
    
    /* Container chính */
    .nba-card {
        background: linear-gradient(135deg, rgba(30, 33, 45, 0.9), rgba(15, 18, 26, 0.95));
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 45px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6);
        margin-top: 20px;
        position: relative; /* Quan trọng để định vị biểu đồ */
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .player-name {
        color: #ffffff; font-size: 60px; font-weight: 900; 
        line-height: 1.1; text-transform: uppercase; letter-spacing: -2px;
        margin: 0; padding: 0;
    }
    .id-tag { 
        background: #00d4ff1a; color: #00d4ff; padding: 4px 12px; 
        border-radius: 5px; font-size: 14px; font-weight: bold;
        display: inline-block; margin: 10px 0 30px 0;
    }
    
    .stats-row { display: flex; gap: 60px; margin-bottom: 35px; }
    .stat-item { border-left: 4px solid #ffcc00; padding-left: 20px; }
    .stat-l { color: #8899a6; font-size: 12px; text-transform: uppercase; letter-spacing: 2px; }
    .stat-v { color: #ffffff; font-size: 35px; font-weight: 900; }

    .info-grid { display: grid; grid-template-columns: 140px 1fr; gap: 12px; font-size: 15px; max-width: 500px; }
    .info-l { color: #5c6c7a; font-weight: 600; text-transform: uppercase; }
    .info-v { color: #00ff88; font-weight: 700; }

    /* Lớp phủ giả lập để chừa chỗ cho biểu đồ bên phải */
    .content-wrapper { max-width: 60%; }

    /* Fix lỗi hiển thị Streamlit */
    [data-testid="stVerticalBlock"] > div:has(div.nba-card) { overflow: visible !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ BIỂU ĐỒ (GIỮ NGUYÊN) ---
def draw_kpi_rings(total, kill_val, kill_target, dead_val, dead_target):
    k_pct = (kill_val / kill_target * 100) if kill_target > 0 else 0
    d_pct = (dead_val / dead_target * 100) if dead_target > 0 else 0
    fig = go.Figure()
    fig.add_trace(go.Pie(hole=0.82, values=[total, max(0, 100-total)], marker=dict(colors=['#ffcc00', 'rgba(255,255,255,0.05)']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))
    fig.add_trace(go.Pie(hole=0.72, values=[k_pct, max(0, 100-k_pct)], marker=dict(colors=['#00d4ff', 'transparent']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))
    fig.add_trace(go.Pie(hole=0.62, values=[d_pct, max(0, 100-d_pct)], marker=dict(colors=['#ffffff', 'transparent']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=450,
        annotations=[dict(text=f"<span style='color:#8899a6;font-size:16px'>KPI</span><br><b style='color:white;font-size:48px'>{total}%</b>", x=0.5, y=0.5, showarrow=False)]
    )
    return fig

# --- 4. TẢI DỮ LIỆU (GIỮ NGUYÊN LOGIC) ---
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
    names = sorted(df['Tên_2'].unique())
    sel = st.selectbox("🔍 TRA CỨU CHIẾN BINH:", ["--- Chọn tên ---"] + names)
    
    if sel != "--- Chọn tên ---":
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # Tạo khung bao quanh trước
        card_placeholder = st.container()
        
        with card_placeholder:
            # Render HTML phần nội dung bên trái
            st.markdown(f"""
                <div class="nba-card">
                    <div class="content-wrapper">
                        <div class="player-name">{sel}</div>
                        <div class="id-tag">#{d['ID']} | {d['Liên Minh_2']}</div>
                        
                        <div class="stats-row">
                            <div class="stat-item">
                                <span class="stat-l">SỨC MẠNH</span>
                                <span class="stat-v">{int(d['Sức Mạnh_2']):,}</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-l">TỔNG KILL</span>
                                <span class="stat-v">{int(d['Tổng Tiêu Diệt_2']):,}</span>
                            </div>
                        </div>
                        
                        <div class="info-grid">
                            <span class="info-l">MỤC TIÊU KILL:</span><span class="info-v" style="color:white">{int(d['GK']):, }</span>
                            <span class="info-l">MỤC TIÊU DEAD:</span><span class="info-v" style="color:white">{int(d['GD']):, }</span>
                            <span class="info-l">TRẠNG THÁI:</span><span class="info-v">COMMAND CENTER ACTIVE</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Đưa biểu đồ lên đè vào khung bằng columns và margin-top âm
            c1, c2 = st.columns([1, 1])
            with c2:
                # Kỹ thuật margin-top âm cực lớn để kéo biểu đồ vào trong Card
                st.markdown('<div style="margin-top: -460px; position: relative; z-index: 99;">', unsafe_allow_html=True)
                fig = draw_kpi_rings(d['KPI'], d['KI'], d['GK'], d['DI'], d['GD'])
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)

        # 6. DƯỚI CARD LÀ CÁC THÔNG SỐ PHỤ
        st.write(f"📊 **Kill tăng:** {int(d['KI']):,} / {int(d['GK']):,}")
        st.progress(max(0.0, min(float(d['KI']) / d['GK'], 1.0)) if d['GK'] > 0 else 0.0)
        
        st.write(f"📊 **Dead tăng:** {int(d['DI']):,} / {int(d['GD']):,}")
        st.progress(max(0.0, min(float(d['DI']) / d['GD'], 1.0)) if d['GD'] > 0 else 0.0)
