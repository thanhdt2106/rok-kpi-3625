import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="ROK PROFILE KPI", layout="wide")

# CSS tạo nền xanh bao quanh toàn bộ nội dung giống Profile game
st.markdown("""
<style>
    .stApp { background-color: #0b1015; }
    
    /* Khung xanh chủ đạo bao quanh tất cả */
    .rok-profile-card {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border: 2px solid #3eb5e5;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        color: white;
        width: 100%;
    }

    /* Header: Tên và ID */
    .header-section { margin-bottom: 25px; }
    .governor-name { font-size: 42px; font-weight: 900; text-transform: uppercase; margin: 0; line-height: 1; }
    .governor-id { color: #b0d4e3; font-size: 16px; margin-top: 5px; opacity: 0.9; }

    /* Lưới thông số (Sức mạnh, Kill, Dead...) */
    .stats-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 30px;
    }
    .stat-box {
        flex: 1;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    .stat-label { color: #b0d4e3; font-size: 12px; font-weight: bold; text-transform: uppercase; display: block; }
    .stat-value { font-size: 22px; font-weight: 800; color: #ffffff; display: block; margin-top: 5px; }

    /* Khu vực biểu đồ KPI */
    .kpi-wrapper {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 15px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. HÀM HỖ TRỢ (CHỐNG LỖI) ---
def safe_n(val):
    try:
        return float(str(val).replace(',', '').strip())
    except:
        return 0.0

def draw_kpi_chart(val, color, title):
    v = safe_n(val)
    fig = go.Figure(go.Pie(
        hole=0.75, values=[v, max(0, 100-v)],
        marker=dict(colors=[color, "rgba(255,255,255,0.05)"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        title={'text': title, 'y':0.9, 'x':0.5, 'xanchor':'center', 'font':{'color':'white','size':14}},
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=40, b=10, l=10, r=10), height=200,
        annotations=[dict(text=f"{v}%", x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=24, fontWeight='bold'))]
    )
    return fig

# --- 3. XỬ LÝ DỮ LIỆU ---
@st.cache_data(ttl=60)
def load_data():
    try:
        sid = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
        u1 = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=731741617'
        u2 = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=371969335'
        
        df1 = pd.read_csv(u1)
        df2 = pd.read_csv(u2)
        
        df1['ID'] = df1['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df2['ID'] = df2['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        
        df = pd.merge(df1, df2, on='ID', suffixes=('_1', '_2'))
        
        def calc_kpi(r):
            p = safe_n(r['Sức Mạnh_2'])
            target_k = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            target_d = 400e3 if p >= 30e6 else 200e3
            
            k_val = max(0, safe_n(r['Tổng Tiêu Diệt_2']) - safe_n(r['Tổng Tiêu Diệt_1']))
            d_val = max(0, safe_n(r['Điểm Chết_2']) - safe_n(r['Điểm Chết_1']))
            
            pk = round((k_val/target_k*100), 1) if target_k > 0 else 0
            pd_v = round((d_val/target_d*100), 1) if target_d > 0 else 0
            return pd.Series([pk, pd_v, round((pk+pd_v)/2, 1)])

        df[['PKILL', 'PDEAD', 'PTOTAL']] = df.apply(calc_kpi, axis=1)
        return df
    except:
        return None

df = load_data()

# --- 4. HIỂN THỊ ---
if df is not None:
    # Ô tìm kiếm nằm ngoài khung xanh
    names = sorted(df['Tên_2'].dropna().astype(str).unique())
    sel = st.selectbox("🔍 TÌM KIẾM CHIẾN BINH:", ["---"] + names)
    
    if sel != "---":
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # MỞ KHUNG XANH BAO QUANH TẤT CẢ
        st.markdown('<div class="rok-profile-card">', unsafe_allow_html=True)
        
        # 1. Header (Tên & ID)
        st.markdown(f"""
            <div class="header-section">
                <p class="governor-name">{sel}</p>
                <p class="governor-id">ID Thống đốc: {d['ID']} | Liên minh: [{d['Liên Minh_2']}]</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 2. Stats Row (Dàn hàng ngang lấp đầy khung)
        st.markdown('<div class="stats-container">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="stat-box"><span class="stat-label">Tiêu diệt</span><span class="stat-value">{int(safe_n(d["Tổng Tiêu Diệt_2"])):,}</span></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="stat-box"><span class="stat-label">Sức mạnh</span><span class="stat-value">{int(safe_n(d["Sức Mạnh_2"])):,}</span></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="stat-box"><span class="stat-label">Điểm Chết</span><span class="stat-value">{int(safe_n(d["Điểm Chết_2"])):,}</span></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="stat-box"><span class="stat-label">Xếp hạng</span><span class="stat-value">S-RANK</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. KPI Section (3 biểu đồ)
        st.markdown('<div class="kpi-wrapper">', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; font-weight:bold; letter-spacing:2px; margin-bottom:15px; color:#b0d4e3;">TIẾN ĐỘ CHIẾN DỊCH KVK</p>', unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.plotly_chart(draw_kpi_chart(d['PKILL'], "#00ffff", "KPI KILL"), use_container_width=True, config={'displayModeBar': False})
        with k2: st.plotly_chart(draw_kpi_chart(d['PDEAD'], "#ff4b4b", "KPI DEAD"), use_container_width=True, config={'displayModeBar': False})
        with k3: st.plotly_chart(draw_kpi_chart(d['PTOTAL'], "#ffd700", "TOTAL KPI"), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # ĐÓNG KHUNG XANH
