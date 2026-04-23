import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH HỆ THỐNG ---
st.set_page_config(page_title="ROK KPI SYSTEM", layout="wide")

# CSS tối giản, không lồng biến để tránh lỗi SyntaxError
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    .main-container {
        background: linear-gradient(180deg, #135d88 0%, #0b3d59 100%);
        border-radius: 15px; padding: 25px; border: 2px solid #3eb5e5;
    }
    .stat-card {
        background: rgba(0, 0, 0, 0.4);
        padding: 15px; border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    .label { color: #b0d4e3; font-size: 12px; font-weight: bold; }
    .value { color: white; font-size: 22px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀM VẼ BIỂU ĐỒ CHUẨN ---
def make_kpi_chart(pct, color, title):
    # Đảm bảo pct là số để tránh lỗi vẽ biểu đồ
    val = float(pct) if pct else 0.0
    fig = go.Figure(go.Pie(
        hole=0.7, values=[val, max(0, 100-val)],
        marker=dict(colors=[color, "#1a1a1a"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        title={'text': title, 'y':0.9, 'x':0.5, 'xanchor': 'center', 'font': {'color': 'white', 'size': 14}},
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=40, b=10, l=10, r=10), height=180,
        annotations=[dict(text=f"{val}%", x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=20))]
    )
    return fig

# --- 3. XỬ LÝ DỮ LIỆU (KHÔNG LỖI MERGE) ---
@st.cache_data(ttl=60)
def fetch_and_clean_data():
    try:
        sid = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
        u1 = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=731741617'
        u2 = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=371969335'
        
        df1 = pd.read_csv(u1)
        df2 = pd.read_csv(u2)
        
        # Ép ID về chuỗi để tránh lỗi merge float/str
        df1['ID'] = df1['ID'].astype(str).str.replace('.0', '', regex=False).strip()
        df2['ID'] = df2['ID'].astype(str).str.replace('.0', '', regex=False).strip()
        
        df = pd.merge(df1, df2, on='ID', suffixes=('_1', '_2'))
        
        # Ép các cột số về kiểu số để tránh lỗi so sánh >=
        for col in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        def get_kpi(r):
            p = r['Sức Mạnh_2']
            tk = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            td = 400e3 if p >= 30e6 else 200e3
            ki = max(0, r['Tổng Tiêu Diệt_2'] - r['Tổng Tiêu Diệt_1'])
            di = max(0, r['Điểm Chết_2'] - r['Điểm Chết_1'])
            pk = round((ki/tk*100), 1) if tk > 0 else 0
            pd_v = round((di/td*100), 1) if td > 0 else 0
            return pd.Series([pk, pd_v, round((pk+pd_v)/2, 1)])

        df[['K_K', 'K_D', 'K_T']] = df.apply(get_kpi, axis=1)
        return df
    except Exception as e:
        st.error(f"Lỗi hệ thống dữ liệu: {e}")
        return None

df = fetch_and_clean_data()

# --- 4. GIAO DIỆN CHÍNH ---
if df is not None:
    # Lấy danh sách tên, loại bỏ giá trị rỗng để tránh lỗi selectbox
    name_list = sorted([str(x) for x in df['Tên_2'].dropna().unique()])
    sel_name = st.selectbox("🔍 TÌM KIẾM THỐNG ĐỐC:", ["---"] + name_list)
    
    if sel_name != "---":
        d = df[df['Tên_2'] == sel_name].iloc[0]
        
        # Container chính màu xanh
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # Tiêu đề
        st.write(f"## {sel_name}")
        st.write(f"**ID:** {d['ID']} | **Liên minh:** [{d['Liên Minh_2']}]")
        st.write("---")
        
        # Hàng 1: Các ô vuông thông số (Dùng st.columns để không lỗi hiển thị)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="stat-card"><div class="label">TIÊU DIỆT</div><div class="value">{int(d["Tổng Tiêu Diệt_2"]):,}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-card"><div class="label">SỨC MẠNH</div><div class="value">{int(d["Sức Mạnh_2"]):,}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="stat-card"><div class="label">CHIẾN CÔNG</div><div class="value">0</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<div class="stat-card"><div class="label">HẠNG</div><div class="value">S-Rank</div></div>', unsafe_allow_html=True)
        
        st.write("") # Tạo khoảng cách
        
        # Hàng 2: Biểu đồ KPI
        st.markdown('<div style="background:rgba(0,0,0,0.2); padding:15px; border-radius:10px;">', unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.plotly_chart(make_kpi_chart(d['K_K'], "#00ffff", "KPI KILL"), use_container_width=True)
        with k2: st.plotly_chart(make_kpi_chart(d['K_D'], "#ff4b4b", "KPI DEAD"), use_container_width=True)
        with k3: st.plotly_chart(make_kpi_chart(d['K_T'], "#ffd700", "TOTAL KPI"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # Đóng container chính
