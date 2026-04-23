import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="ROK KPI SYSTEM", layout="wide")

# --- 2. CSS TỐI ƯU (Tách biệt hoàn toàn với Logic) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    .main-card {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 12px; padding: 20px; border: 1px solid #3eb5e5;
    }
    .stat-square {
        background: rgba(0, 0, 0, 0.4);
        padding: 15px; border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
    }
    .label { color: #b0d4e3; font-size: 11px; text-transform: uppercase; }
    .value { color: white; font-size: 20px; font-weight: bold; display: block; }
    .kpi-box { background: rgba(0, 0, 0, 0.2); border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ BIỂU ĐỒ (Không dùng HTML lồng) ---
def draw_chart(percent, color, label):
    fig = go.Figure(go.Pie(
        hole=0.7, values=[percent, max(0, 100-percent)],
        marker=dict(colors=[color, "#222"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        title={'text': label, 'y':0.9, 'x':0.5, 'xanchor':'center', 'font':{'color':'white', 'size':13}},
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=40, b=10, l=10, r=10), height=180,
        annotations=[dict(text=f"{percent}%", x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=18))]
    )
    return fig

# --- 4. XỬ LÝ DỮ LIỆU (ÉP KIỂU TRIỆT ĐỂ) ---
@st.cache_data(ttl=60)
def load_clean_data():
    try:
        sid = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
        df1 = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=731741617')
        df2 = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=371969335')
        
        # Ép ID về string và dọn dẹp
        df1['ID'] = df1['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df2['ID'] = df2['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        
        df = pd.merge(df1, df2, on='ID', suffixes=('_1', '_2'))
        
        # Ép các cột số về float để tránh lỗi so sánh '>='
        cols_to_fix = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in cols_to_fix:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        def calc(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            gd = 400e3 if p >= 30e6 else 200e3
            ki = max(0, r['Tổng Tiêu Diệt_2'] - r['Tổng Tiêu Diệt_1'])
            di = max(0, r['Điểm Chết_2'] - r['Điểm Chết_1'])
            pk = round((ki/gk*100), 1) if gk > 0 else 0
            pd_v = round((di/gd*100), 1) if gd > 0 else 0
            return pd.Series([pk, pd_v, round((pk+pd_v)/2, 1)])
        
        df[['KPI_K', 'KPI_D', 'KPI_T']] = df.apply(calc, axis=1)
        return df
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu: {e}")
        return None

df = load_clean_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    names = sorted(df['Tên_2'].dropna().astype(str).unique())
    sel = st.selectbox("🔍 TRA CỨU CHIẾN BINH:", ["---"] + names)
    
    if sel != "---":
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # Bắt đầu Card xanh
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        
        # Thông tin header
        st.markdown(f"""
            <div style="margin-bottom:15px">
                <p style="color:#b0d4e3; margin:0; font-size:13px">ID: {d['ID']}</p>
                <h1 style="color:white; margin:0; text-transform:uppercase">{sel}</h1>
                <p style="color:#ffd700; margin:0; font-weight:bold">[{d['Liên Minh_2']}]</p>
            </div>
        """, unsafe_allow_html=True)

        # Lưới ô vuông thông số (4 ô)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="stat-square"><span class="label">Tiêu Diệt</span><span class="value">{int(d["Tổng Tiêu Diệt_2"]):,}</span></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="stat-square"><span class="label">Sức Mạnh</span><span class="value">{int(d["Sức Mạnh_2"]):, }</span></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="stat-square"><span class="label">Chiến Công</span><span class="value">0</span></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="stat-square"><span class="label">Hạng</span><span class="value">---</span></div>', unsafe_allow_html=True)

        # Khu vực KPI (3 vòng tròn)
        st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.plotly_chart(draw_chart(d['KPI_K'], "#00ffff", "KPI KILL"), use_container_width=True, config={'displayModeBar': False})
        with k2: st.plotly_chart(draw_chart(d['KPI_D'], "#ff4b4b",
                                        
