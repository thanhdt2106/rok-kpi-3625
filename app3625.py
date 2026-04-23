import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Cấu hình trang cơ bản
st.set_page_config(page_title="ROK KPI", layout="wide")

# CSS để có màu nền tối và khung viền đơn giản
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; color: white; }
    .kpi-card {
        background-color: #135d88;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #3eb5e5;
    }
    .box {
        background: rgba(0,0,0,0.3);
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Hàm vẽ biểu đồ (Dùng Try-Except để không bao giờ làm sập App)
def draw_kpi(value, color, title):
    try:
        val = float(value)
    except:
        val = 0.0
    fig = go.Figure(go.Pie(
        hole=0.7, values=[val, max(0, 100-val)],
        marker=dict(colors=[color, "#222"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        title={'text': title, 'x':0.5, 'font': {'color': 'white', 'size': 14}},
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=30, b=0, l=0, r=0), height=150,
        annotations=[dict(text=f"{val}%", x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=16))]
    )
    return fig

# 3. Tải và làm sạch dữ liệu (Sửa lỗi 'strip' và lỗi so sánh)
@st.cache_data(ttl=60)
def get_data():
    try:
        sid = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
        df1 = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=731741617')
        df2 = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=371969335')

        # Cách sửa lỗi 'Series' has no attribute 'strip': dùng .str.strip()
        df1['ID'] = df1['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df2['ID'] = df2['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()

        df = pd.merge(df1, df2, on='ID', suffixes=('_1', '_2'))

        # Ép kiểu số toàn bộ cột cần tính
        cols = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in cols:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        # Tính KPI
        def calc(r):
            p = r['Sức Mạnh_2']
            tk = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            td = 400e3 if p >= 30e6 else 200e3
            ki = max(0, r['Tổng Tiêu Diệt_2'] - r['Tổng Tiêu Diệt_1'])
            di = max(0, r['Điểm Chết_2'] - r['Điểm Chết_1'])
            pk = round((ki/tk*100), 1) if tk > 0 else 0
            pd_v = round((di/td*100), 1) if td > 0 else 0
            return pd.Series([pk, pd_v, round((pk+pd_v)/2, 1)])

        df[['K_KILL', 'K_DEAD', 'K_TOTAL']] = df.apply(calc, axis=1)
        return df
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu: {e}")
        return None

df = get_data()

# 4. Hiển thị giao diện
if df is not None:
    # Sửa lỗi 'sorted' bằng cách ép kiểu về string cho tên
    names = sorted(df['Tên_2'].dropna().astype(str).unique())
    sel = st.selectbox("🔍 TRA CỨU CHIẾN BINH:", ["---"] + names)

    if sel != "---":
        d = df[df['Tên_2'] == sel].iloc[0]

        # Khung chính
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        
        st.header(f"战士: {sel}")
        st.write(f"**ID:** {d['ID']} | **Liên minh:** {d['Liên Minh_2']}")
        
        st.divider()

        # Hàng chỉ số
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="box"><small>TIÊU DIỆT</small><br><b>{int(d["Tổng Tiêu Diệt_2"]):,}</b></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="box"><small>SỨC MẠNH</small><br><b>{int(d["Sức Mạnh_2"]):,}</b></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="box"><small>ĐIỂM CHẾT</small><br><b>{int(d["Điểm Chết_2"]):,}</b></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="box"><small>XẾP HẠNG</small><br><b>S-Rank</b></div>', unsafe_allow_html=True)

        st.write("")

        # Hàng biểu đồ
        k1, k2, k3 = st.columns(3)
        with k1: st.plotly_chart(draw_kpi(d['K_KILL'], "#00ffff", "KPI KILL"), use_container_width=True)
        with k2: st.plotly_chart(draw_kpi(d['K_DEAD'], "#ff4b4b", "KPI DEAD"), use_container_width=True)
        with k3: st.plotly_chart(draw_kpi(d['K_TOTAL'], "#ffd700", "TOTAL KPI"), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)
