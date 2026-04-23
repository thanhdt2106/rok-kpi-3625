import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH HỆ THỐNG ---
st.set_page_config(page_title="ROK KPI SYSTEM", layout="wide")

# CSS: Tối ưu khung xanh lấp đầy màn hình và ô vuông nền mờ
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    .main-card {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 12px;
        padding: 25px;
        border: 2px solid #3eb5e5;
        width: 100%;
    }
    .stats-grid {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-top: 20px;
    }
    .stat-box {
        flex: 1;
        background: rgba(0, 0, 0, 0.3);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    .label { color: #b0d4e3; font-size: 12px; text-transform: uppercase; font-weight: bold; }
    .value { color: white; font-size: 20px; font-weight: 800; display: block; margin-top: 5px; }
    
    /* Khung KPI mờ lấp đầy phía dưới */
    .kpi-section {
        background: rgba(0, 0, 0, 0.15);
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀM VẼ BIỂU ĐỒ (ỔN ĐỊNH TUYỆT ĐỐI) ---
def draw_chart(val, color, title):
    try:
        v = float(val)
    except:
        v = 0.0
    fig = go.Figure(go.Pie(
        hole=0.7, values=[v, max(0, 100-v)],
        marker=dict(colors=[color, "rgba(255,255,255,0.05)"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        title={'text': title, 'y':0.95, 'x':0.5, 'xanchor': 'center', 'font': {'color': 'white', 'size': 14}},
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=40, b=0, l=0, r=0), height=180,
        annotations=[dict(text=f"{v}%", x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=20, bordercolor='white'))]
    )
    return fig

# --- 3. XỬ LÝ DỮ LIỆU (CHỐNG LỖI MERGE & SO SÁNH) ---
@st.cache_data(ttl=60)
def get_clean_data():
    try:
        sid = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
        u1 = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=731741617'
        u2 = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=371969335'
        
        df1 = pd.read_csv(u1)
        df2 = pd.read_csv(u2)
        
        # Ép kiểu ID về String và dọn dẹp để không lỗi merge
        df1['ID'] = df1['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df2['ID'] = df2['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        
        df = pd.merge(df1, df2, on='ID', suffixes=('_1', '_2'))
        
        # Ép kiểu số cho toàn bộ cột tính toán để không bị lỗi '>='
        cols = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in cols:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        def run_calc(r):
            p = r['Sức Mạnh_2']
            tk = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            td = 400e3 if p >= 30e6 else 200e3
            ki = max(0, r['Tổng Tiêu Diệt_2'] - r['Tổng Tiêu Diệt_1'])
            di = max(0, r['Điểm Chết_2'] - r['Điểm Chết_1'])
            pk = round((ki/tk*100), 1) if tk > 0 else 0
            pd_v = round((di/td*100), 1) if td > 0 else 0
            return pd.Series([pk, pd_v, round((pk+pd_v)/2, 1)])

        df[['PKILL', 'PDEAD', 'PTOTAL']] = df.apply(run_calc, axis=1)
        return df
    except Exception as e:
        st.error(f"Lỗi nạp dữ liệu: {e}")
        return None

df = get_clean_data()

# --- 4. HIỂN THỊ ---
if df is not None:
    names = sorted(df['Tên_2'].dropna().astype(str).unique())
    sel = st.selectbox("🔍 TÌM KIẾM CHIẾN BINH:", ["---"] + names)
    
    if sel != "---":
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # TOÀN BỘ NẰM TRONG KHUNG XANH
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        
        # Header: Tên & ID
        st.markdown(f"""
            <div style="margin-bottom: 20px;">
                <h1 style="color:white; margin:0; text-transform:uppercase; font-size:40px;">{sel}</h1>
                <p style="color:#b0d4e3; margin:0;">ID Thống đốc: <b>{d['ID']}</b> | Liên minh: <b>[{d['Liên Minh_2']}]</b></p>
            </div>
        """, unsafe_allow_html=True)
        
        # Các ô thông số (Tự động giãn cách lấp đầy chiều ngang)
        st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
        
        # Chúng ta dùng columns của Streamlit để nhét các box HTML vào cho chuẩn vị trí
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="stat-box"><span class="label">Tiêu diệt</span><span class="value">{int(d["Tổng Tiêu Diệt_2"]):,}</span></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="stat-box"><span class="label">Sức mạnh</span><span class="value">{int(d["Sức Mạnh_2"]):,}</span></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="stat-box"><span class="label">Điểm Chết</span><span class="value">{int(d["Điểm Chết_2"]):, }</span></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="stat-box"><span class="label">Xếp hạng</span><span class="value">S-RANK</span></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Khu vực 3 vòng tròn KPI
        st.markdown('<div class="kpi-section">', unsafe_allow_html=True)
        st.markdown('<p style="color:white; font-weight:bold; margin-bottom:10px; text-align:center;">TIẾN ĐỘ KVK</p>', unsafe_allow_html=True)
        
        k1, k2, k3 = st.columns(3)
        with k1: st.plotly_chart(draw_chart(d['PKILL'], "#00ffff", "KPI KILL"), use_container_width=True, config={'displayModeBar': False})
        with k2: st.plotly_chart(draw_chart(d['PDEAD'], "#ff4b4b", "KPI DEAD"), use_container_width=True, config={'displayModeBar': False})
        with k3: st.plotly_chart(draw_chart(d['PTOTAL'], "#ffd700", "TOTAL KPI"), use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # Đóng main-card
