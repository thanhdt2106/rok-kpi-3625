import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="ROK PROFILE SYSTEM", layout="wide")

# --- 2. CSS ĐỂ GIỐNG Y CHANG GIAO DIỆN HỒ SƠ ROK ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    
    /* Khung chính màu xanh đặc trưng của ROK */
    .rok-profile-container {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 10px;
        padding: 20px;
        border: 2px solid #3eb5e5;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        color: white;
    }

    /* Phần Header: Tên và ID */
    .p-header { font-size: 32px; font-weight: 800; margin: 0; }
    .p-id { font-size: 14px; color: #e0e0e0; margin-bottom: 10px; }
    
    /* Bố cục cột chỉ số bên phải */
    .stat-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
    }
    .stat-label { color: #b0d4e3; font-size: 13px; text-transform: uppercase; }
    .stat-value { font-size: 22px; font-weight: 700; color: #ffffff; }

    /* Khung 3 vòng tròn KPI bên dưới */
    .kpi-section {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 8px;
        margin-top: 20px;
        padding: 15px;
        display: flex;
        justify-content: space-around;
    }
    
    .badge-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        width: 30%;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ VÒNG TRÒN KPI ---
def draw_kpi_circle(pct, color, label):
    val = min(max(float(pct), 0.0), 100.0)
    fig = go.Figure(go.Pie(
        hole=0.7, values=[val, 100 - val],
        marker=dict(colors=[color, "rgba(255,255,255,0.1)"]),
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
        df_t = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        df_s = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        
        # Đồng nhất ID để tránh lỗi float/str
        for df_tmp in [df_t, df_s]:
            df_tmp['ID'] = df_tmp['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()

        df = pd.merge(df_t, df_s, on='ID', suffixes=('_1', '_2'))
        
        # Tính toán các chỉ số
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
        def calculate_metrics(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            gd = 400e3 if p >= 30e6 else 200e3
            k_pct = round((r['KI'] / gk * 100), 1) if gk > 0 else 0
            d_pct = round((r['DI'] / gd * 100), 1) if gd > 0 else 0
            return pd.Series([round((k_pct + d_pct) / 2, 1), k_pct, d_pct, gk, gd])
        
        df[['KPI_Total', 'KPI_K', 'KPI_D', 'GK', 'GD']] = df.apply(calculate_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    sel_name = st.selectbox("🔍 CHỌN THỐNG ĐỐC:", ["---"] + sorted(df['Tên_2'].unique()))
    
    if sel_name != "---":
        d = df[df['Tên_2'] == sel_name].iloc[0]
        
        # Toàn bộ khung Profile ROK
        st.markdown(f"""
            <div class="rok-profile-container">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <div class="p-id">Thống đốc(ID: {d['ID']})</div>
                        <div class="p-header">{sel_name}</div>
                        <div style="margin-top:10px;">
                            <span style="color:#b0d4e3">Liên minh:</span><br>
                            <b>[{d['Liên Minh_2']}]</b>
                        </div>
                    </div>
                    <div style="flex: 1;" class="stat-grid">
                        <div>
                            <div class="stat-label">Điểm Tiêu Diệt</div>
                            <div class="stat-value">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                        </div>
                        <div>
                            <div class="stat-label">Sức mạnh</div>
                            <div class="stat-value">{int(d['Sức Mạnh_2']):,}</div>
                        </div>
                        <div>
                            <div class="stat-label">Điểm Chiến Công</div>
                            <div class="stat-value">0</div>
                        </div>
                        <div>
                            <div class="stat-label">Cao nhất</div>
                            <div class="stat-value">---</div>
                        </div>
                    </div>
                </div>
        """, unsafe_allow_html=True)
        
        # 3 Vòng tròn KPI thay thế vị trí huy hiệu
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="badge-card"><small>KPI TIÊU DIỆT</small>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi_circle(d['KPI_K'], "#00ffff", "Kill"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="badge-card"><small>KPI ĐIỂM CHẾT</small>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi_circle(d['KPI_D'], "#ff4b4b", "Dead"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="badge-card"><small>TỔNG KPI KVK</small>', unsafe_allow_html=True)
            st.plotly_chart(draw_kpi_circle(d['KPI_Total'], "#ffd700", "Total"), use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True) # Đóng khung chính
