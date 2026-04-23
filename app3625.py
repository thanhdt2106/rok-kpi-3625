import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="ROK KPI SYSTEM", layout="wide")

# --- 2. CSS TỐI GIẢN (Chỉ dùng để chỉnh màu và bo góc ô vuông) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    /* Khung xanh chính bao bọc toàn bộ */
    .main-card {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #3eb5e5;
        margin-bottom: 20px;
    }
    /* Các ô vuông thông số nền mờ */
    .stat-box {
        background: rgba(0, 0, 0, 0.4);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: left;
    }
    .label-text { color: #b0d4e3; font-size: 12px; text-transform: uppercase; }
    .value-text { color: white; font-size: 22px; font-weight: bold; display: block; margin-top: 5px; }
    
    /* Khung mờ chứa KPI */
    .kpi-container {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 12px;
        padding: 15px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ BIỂU ĐỒ (Đảm bảo không xung đột) ---
def create_kpi_chart(percent, color, title):
    fig = go.Figure(go.Pie(
        hole=0.7, values=[percent, max(0, 100-percent)],
        marker=dict(colors=[color, "#222"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        title={'text': title, 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': {'color': 'white', 'size': 14}},
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=30, b=10, l=10, r=10), height=180,
        annotations=[dict(text=f"{percent}%", x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=20))]
    )
    return fig

# --- 4. XỬ LÝ DỮ LIỆU (Fix lỗi Merge và ID) ---
@st.cache_data(ttl=60)
def get_data():
    try:
        sid = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
        u1 = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=731741617'
        u2 = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=371969335'
        
        df1 = pd.read_csv(u1)
        df2 = pd.read_csv(u2)
        
        # Ép kiểu ID về String để tránh lỗi float64 vs str
        for df in [df1, df2]:
            df['ID'] = df['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        
        df = pd.merge(df1, df2, on='ID', suffixes=('_1', '_2'))
        
        # Tính toán KPI
        def calculate_kpi(row):
            pow_val = row.get('Sức Mạnh_2', 0)
            # Tier mục tiêu
            target_k = 300e6 if pow_val >= 45e6 else 220e6 if pow_val >= 35e6 else 130e6 if pow_val >= 25e6 else 80e6
            target_d = 400e3 if pow_val >= 30e6 else 200e3
            
            kill_inc = max(0, row.get('Tổng Tiêu Diệt_2', 0) - row.get('Tổng Tiêu Diệt_1', 0))
            dead_inc = max(0, row.get('Điểm Chết_2', 0) - row.get('Điểm Chết_1', 0))
            
            pk = round((kill_inc / target_k * 100), 1) if target_k > 0 else 0
            pd_val = round((dead_inc / target_d * 100), 1) if target_d > 0 else 0
            return pd.Series([pk, pd_val, round((pk + pd_val)/2, 1)])

        df[['PK', 'PD', 'PT']] = df.apply(calculate_kpi, axis=1)
        return df
    except Exception as e:
        st.error(f"Lỗi dữ liệu: {e}")
        return None

df = get_data()

# --- 5. GIAO DIỆN HIỂN THỊ ---
if df is not None:
    names = sorted(df['Tên_2'].dropna().unique())
    selected = st.selectbox("🔍 CHỌN THỐNG ĐỐC:", ["---"] + names)
    
    if selected != "---":
        d = df[df['Tên_2'] == selected].iloc[0]
        
        # KHUNG XANH CHÍNH
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        
        # 1. Header: Tên và ID
        st.markdown(f"""
            <div style="margin-bottom: 20px;">
                <div style="color: #b0d4e3; font-size: 14px;">Thống đốc(ID: {d['ID']})</div>
                <div style="color: white; font-size: 36px; font-weight: 800; text-transform: uppercase;">{selected}</div>
                <div style="color: #ffd700; font-weight: bold;">Liên minh: [{d['Liên Minh_2']}]</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 2. Lưới ô vuông thông số (Dùng st.columns của Streamlit để tránh lỗi hiển thị)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="stat-box"><span class="label-text">Điểm Tiêu Diệt</span><span class="value-text">{int(d["Tổng Tiêu Diệt_2"]):,}</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-box"><span class="label-text">Sức Mạnh</span><span class="value-text">{int(d["Sức Mạnh_2"]):,}</span></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="stat-box"><span class="label-text">Điểm Chiến Công</span><span class="value-text">0</span></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="stat-box"><span class="label-text">Chiến Công Cao Nhất</span><span class="value-text">---</span></div>', unsafe_allow_html=True)
            
        # 3. Khu vực KPI (Vòng tròn) - Nằm trong khung mờ bên trong khung xanh
        st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1:
            st.plotly_chart(create_kpi_chart(d['PK'], "#00ffff", "KPI TIÊU DIỆT"), use_container_width=True, config={'displayModeBar': False})
        with k2:
            st.plotly_chart(create_kpi_chart(d['PD'], "#ff4b4b", "KPI ĐIỂM CHẾT"), use_container_width=True, config={'displayModeBar': False})
        with k3:
            st.plotly_chart(create_kpi_chart(d['PT'], "#ffd700", "TỔNG KPI KVK"), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # Đóng main-card
