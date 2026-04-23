import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. GIAO DIỆN (CSS CUSTOM - TONE XANH ĐEN CHUYÊN NGHIỆP) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e6ed; }
    
    .main-header {
        color: #00d4ff; text-align: center; font-size: 32px;
        font-weight: bold; padding: 15px;
        text-transform: uppercase; letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }

    .command-card {
        background: rgba(26, 28, 35, 0.8);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        border: 1px solid rgba(0, 212, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }

    .player-name {
        color: #ffffff; font-size: 40px; font-weight: 800; 
        line-height: 1; margin-bottom: 5px;
        text-transform: uppercase;
    }

    .id-tag { color: #00d4ff; font-family: monospace; font-size: 14px; margin-bottom: 20px; }
    .stat-label { color: #8899a6; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
    .stat-value { color: #ffffff; font-size: 20px; font-weight: bold; }
    
    [data-testid="stDataFrame"] { background-color: #161b22; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. QUẢN LÝ NGÔN NGỮ ---
col_t, col_l = st.columns([4, 1]) 
with col_l:
    lang = st.radio("LANG:", ["VN", "EN"], horizontal=True, label_visibility="collapsed")

texts = {
    "VN": {
        "header": "🛡️ HỆ THỐNG QUẢN LÝ KPI",
        "search": "🔍 TRA CỨU CHIẾN BINH:",
        "select": "--- Chọn tên ---",
        "all": "LIÊN MINH", "pow": "SỨC MẠNH", "tk": "TỔNG KILL", "td": "TỔNG DEAD",
        "kt": "MỤC TIÊU KILL", "dt": "MỤC TIÊU DEAD",
        "ki": "Kill tăng", "di": "Dead tăng",
        "table": "📋 BẢNG THỐNG KÊ TỔNG HỢP",
        "cols": ['Tên', 'ID', 'Liên minh', 'Sức mạnh', 'Tổng Kill', 'Kill tăng (+)', 'Dead tăng (+)', 'KPI (%)']
    },
    "EN": {
        "header": "🛡️ KPI MANAGEMENT SYSTEM",
        "search": "🔍 WARRIOR LOOKUP:",
        "select": "--- Select name ---",
        "all": "ALLIANCE", "pow": "POWER", "tk": "TOTAL KILL", "td": "TOTAL DEAD",
        "kt": "TARGET KILL", "dt": "TARGET DEAD",
        "ki": "Kill inc", "di": "Dead inc",
        "table": "📋 SUMMARY STATISTICS TABLE",
        "cols": ['Name', 'ID', 'Alliance', 'Power', 'Total Kill', 'Kill Inc (+)', 'Dead Inc (+)', 'KPI (%)']
    }
}
L = texts[lang]

# --- 4. HÀM VẼ VÒNG TRÒN KPI (RADIAL GAUGE) ---
def draw_kpi_circles(total, kill_pct, dead_pct):
    fig = go.Figure()
    # Vòng ngoài (Total) - Xanh Cyan
    fig.add_trace(go.Pie(hole=0.8, values=[total, max(0, 100-total)], marker=dict(colors=['#00d4ff', '#161b22']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))
    # Vòng giữa (Kill) - Vàng
    fig.add_trace(go.Pie(hole=0.7, values=[kill_pct, max(0, 100-kill_pct)], marker=dict(colors=['#fbbf24', 'transparent']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))
    # Vòng trong (Dead) - Đỏ
    fig.add_trace(go.Pie(hole=0.6, values=[dead_pct, max(0, 100-dead_pct)], marker=dict(colors=['#f87171', 'transparent']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=10, b=10, l=10, r=10),
        annotations=[dict(text=f"{total}%", x=0.5, y=0.5, font_size=35, font_color="#00d4ff", showarrow=False)]
    )
    return fig

# --- 5. XỬ LÝ DỮ LIỆU ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        for d in [dt, ds]:
            d['ID'] = d['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
            d['Tên'] = d['Tên'].fillna('Unknown').astype(str).str.strip()
        df = pd.merge(dt.drop_duplicates('ID'), ds.drop_duplicates('ID'), on='ID', suffixes=('_1', '_2'))
        
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(float)
            
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
        def get_metrics(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 200e6 if p >= 30e6 else 100e6
            gd = 400e3 if p >= 30e6 else 200e3
            pk = max(0.0, min(float(r['KI']) / gk, 1.0)) if gk > 0 else 0.0
            pdv = max(0.0, min(float(r['DI']) / gd, 1.0)) if gd > 0 else 0.0
            return pd.Series([round(((pk + pdv) / 2) * 100, 1), gk, gd, pk*100, pdv*100])
        
        df[['KPI', 'GK', 'GD', 'K_PCT', 'D_PCT']] = df.apply(get_metrics, axis=1)
        return df
    except Exception as e:
        st.error(f"Lỗi load dữ liệu: {e}")
        return None

df = load_data()

# --- 6. HIỂN THỊ ---
if df is not None:
    st.markdown(f'<div class="main-header">{L["header"]}</div>', unsafe_allow_html=True)
    
    names = sorted(df['Tên_2'].unique())
    sel = st.selectbox(L["search"], [L["select"]] + names)
    
    if sel != L["select"]:
        d = df[df['Tên_2'] == sel].iloc[0]
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown(f"""
                <div class="command-card">
                    <div class="player-name">{sel}</div>
                    <div class="id-tag">ID: {d['ID']} • {d['Liên Minh_2']}</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div><span class="stat-label">{L['pow']}</span><br><span class="stat-value">{int(d['Sức Mạnh_2']):,}</span></div>
                        <div><span class="stat-label">{L['tk']}</span><br><span class="stat-value">{int(d['Tổng Tiêu Diệt_2']):,}</span></div>
                        <div style="border-top:1px solid #333; padding-top:10px;"><span class="stat-label">{L['kt']}</span><br><span style="color:#fbbf24; font-weight:bold;">{int(d['GK']):,}</span></div>
                        <div style="border-top:1px solid #333; padding-top:10px;"><span class="stat-label">{L['dt']}</span><br><span style="color:#f87171; font-weight:bold;">{int(d['GD']):,}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Thanh tiến độ phụ
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                st.caption(f"🔥 {L['ki']}: {int(d['KI']):,}")
                st.progress(d['K_PCT']/100 if d['K_PCT'] < 100 else 1.0)
            with c_m2:
                st.caption(f"💀 {L['di']}: {int(d['DI']):,}")
                st.progress(d['D_PCT']/100 if d['D_PCT'] < 100 else 1.0)

        with col2:
            # Vẽ vòng tròn KPI từ hàm đã định nghĩa
            fig = draw_kpi_circles(d['KPI'], d['K_PCT'], d['D_PCT'])
            st.plotly_chart(fig, use_container_width=True)

    # Bảng tổng hợp
    st.divider()
    st.subheader(L["table"])
    v_df = df[['Tên_2', 'ID', 'Liên Minh_2', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'KI', 'DI', 'KPI']].copy()
    v_df.columns = L["cols"]
    st.dataframe(v_df.style.format({L["cols"][3]: '{:,.0f}', L["cols"][4]: '{:,.0f}', L["cols"][5]: '{:,.0f}', L["cols"][6]: '{:,.0f}', L["cols"][7]: '{:.1f}%'}), use_container_width=True, height=400)
else:
    st.warning("⚠️ Không thể kết nối với dữ liệu. Vui lòng kiểm tra lại Google Sheets.")
