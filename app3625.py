import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. GIAO DIỆN (CSS TÁI TẠO PROFILE NBA - FIX LỖI RENDER) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e6ed; }
    
    /* Container chính cho Profile Card */
    .profile-container {
        background: #1a1c23;
        border-radius: 15px;
        padding: 35px;
        border: 1px solid #2d2f36;
        margin-bottom: 20px;
    }

    /* Tên người chơi lớn */
    .player-name-large {
        color: #ffffff; font-size: 50px; font-weight: 800; 
        line-height: 1; text-transform: uppercase; letter-spacing: 2px;
        margin-bottom: 5px;
    }
    .id-sub-text { color: #8899a6; font-size: 16px; margin-bottom: 30px; font-family: monospace; }
    
    /* Hàng chỉ số chính */
    .main-stats-row { display: flex; gap: 50px; margin-bottom: 25px; border-bottom: 1px solid #333; padding-bottom: 20px; }
    .stat-block { display: flex; flex-direction: column; }
    .label-nba { color: #8899a6; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .value-nba { color: #ffffff; font-size: 26px; font-weight: bold; }

    /* Lưới chỉ số chi tiết */
    .detail-grid { display: grid; grid-template-columns: 130px 1fr; gap: 10px; font-size: 14px; }
    .detail-label { color: #8899a6; font-weight: bold; }
    .detail-val { color: #ffffff; }

    /* Tiêu đề bảng */
    .main-header {
        color: #00d4ff; text-align: center; font-size: 32px;
        font-weight: bold; padding: 15px;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. QUẢN LÝ NGÔN NGỮ ---
col_t, col_l = st.columns([4, 1]) 
with col_l:
    lang = st.radio("LANG:", ["VN", "EN"], horizontal=True, label_visibility="collapsed")

texts = {
    "VN": {
        "header": "🛡️ HỆ THỐNG QUẢN LÝ KPI", "search": "🔍 TRA CỨU CHIẾN BINH:", "select": "--- Chọn tên ---",
        "all": "Liên minh", "pow": "Sức mạnh", "tk": "Tổng Kill", "td": "Tổng Dead",
        "kt": "Mục tiêu Kill", "dt": "Mục tiêu Dead", "ki": "Kill tăng", "di": "Dead tăng",
        "table": "📋 BẢNG THỐNG KÊ TỔNG HỢP",
        "cols": ['Tên', 'ID', 'Liên minh', 'Sức mạnh', 'Tổng Kill', 'Kill tăng (+)', 'Dead tăng (+)', 'KPI (%)']
    },
    "EN": {
        "header": "🛡️ KPI MANAGEMENT SYSTEM", "search": "🔍 WARRIOR LOOKUP:", "select": "--- Select name ---",
        "all": "Alliance", "pow": "Power", "tk": "Total Kill", "td": "Total Dead",
        "kt": "Target Kill", "dt": "Target Dead", "ki": "Kill inc", "di": "Dead inc",
        "table": "📋 SUMMARY STATISTICS TABLE",
        "cols": ['Name', 'ID', 'Alliance', 'Power', 'Total Kill', 'Kill Inc (+)', 'Dead Inc (+)', 'KPI (%)']
    }
}
L = texts[lang]

# --- 4. HÀM VẼ VÒNG TRÒN KPI 3 LỚP (GIỮ NGUYÊN LOGIC) ---
def draw_kpi_rings(total, kill_val, kill_target, dead_val, dead_target):
    k_pct = (kill_val / kill_target * 100) if kill_target > 0 else 0
    d_pct = (dead_val / dead_target * 100) if dead_target > 0 else 0
    
    fig = go.Figure()
    # Vòng KPI Tổng
    fig.add_trace(go.Pie(hole=0.85, values=[total, max(0, 100-total)], marker=dict(colors=['#ffcc00', '#222']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))
    # Vòng Kill
    fig.add_trace(go.Pie(hole=0.75, values=[k_pct, max(0, 100-k_pct)], marker=dict(colors=['#00d4ff', 'transparent']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))
    # Vòng Dead
    fig.add_trace(go.Pie(hole=0.65, values=[d_pct, max(0, 100-d_pct)], marker=dict(colors=['#ffffff', 'transparent']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=400,
        annotations=[dict(text=f"{total}%", x=0.5, y=0.5, font_size=35, font_color="white", showarrow=False)]
    )
    return fig

# --- 5. XỬ LÝ DỮ LIỆU (GIỮ NGUYÊN 100% GỐC) ---
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
            if p < 15e6: gk = 80e6
            elif p < 20e6: gk = 100e6
            elif p < 25e6: gk = 130e6
            elif p < 30e6: gk = 170e6
            elif p < 35e6: gk = 200e6
            elif p < 40e6: gk = 220e6
            elif p < 45e6: gk = 250e6
            else: gk = 300e6
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = max(0.0, min(float(r['KI']) / gk, 1.0)) if gk > 0 else 0.0
            pdv = max(0.0, min(float(r['DI']) / gd, 1.0)) if gd > 0 else 0.0
            return pd.Series([round(((pk + pdv) / 2) * 100, 1), gk, gd])
        
        df[['KPI', 'GK', 'GD']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 6. HIỂN THỊ ---
if df is not None:
    st.markdown(f'<div class="main-header">{L["header"]}</div>', unsafe_allow_html=True)
    names = sorted(df['Tên_2'].unique())
    sel = st.selectbox(L["search"], [L["select"]] + names)
    
    if sel != L["select"]:
        d = df[df['Tên_2'] == sel].iloc[0]
        
        col1, col2 = st.columns([1.6, 1])
        with col1:
            # FIX: SỬ DỤNG f-string VÀ unsafe_allow_html ĐÚNG CÁCH
            profile_html = f"""
                <div class="profile-container">
                    <div class="player-name-large">{sel}</div>
                    <div class="id-sub-text">#{d['ID']} | {d['Liên Minh_2']}</div>
                    
                    <div class="main-stats-row">
                        <div class="stat-block">
                            <span class="label-nba">{L['pow']}</span>
                            <span class="value-nba">{int(d['Sức Mạnh_2']):,}</span>
                        </div>
                        <div class="stat-block">
                            <span class="label-nba">{L['tk']}</span>
                            <span class="value-nba">{int(d['Tổng Tiêu Diệt_2']):,}</span>
                        </div>
                    </div>
                    
                    <div class="detail-grid">
                        <span class="detail-label">{L['kt']}:</span><span class="detail-val">{int(d['GK']):,}</span>
                        <span class="detail-label">{L['dt']}:</span><span class="detail-val">{int(d['GD']):,}</span>
                        <span class="detail-label">Status:</span><span class="detail-val">Active Command Center</span>
                    </div>
                </div>
            """
            st.markdown(profile_html, unsafe_allow_html=True)
            
            # Progress bars phụ bên dưới Card
            st.write(f"📊 {L['ki']}: {int(d['KI']):,}")
            st.progress(max(0.0, min(float(d['KI']) / d['GK'], 1.0)) if d['GK'] > 0 else 0.0)
            st.write(f"📊 {L['di']}: {int(d['DI']):,}")
            st.progress(max(0.0, min(float(d['DI']) / d['GD'], 1.0)) if d['GD'] > 0 else 0.0)

        with col2:
            fig = draw_kpi_rings(d['KPI'], d['KI'], d['GK'], d['DI'], d['GD'])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 7. BẢNG TỔNG HỢP (GIỮ NGUYÊN)
    st.divider()
    st.subheader(L["table"])
    v_df = df[['Tên_2', 'ID', 'Liên Minh_2', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'KI', 'DI', 'KPI']].copy()
    v_df.columns = L["cols"]
    st.dataframe(v_df.style.format({
        L["cols"][3]: '{:,.0f}', L["cols"][4]: '{:,.0f}', 
        L["cols"][5]: '{:,.0f}', L["cols"][6]: '{:,.0f}', L["cols"][7]: '{:.1f}%'
    }), use_container_width=True, height=450)
