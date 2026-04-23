import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH GIAO DIỆN CHUẨN ROK ---
st.set_page_config(page_title="ROK KPI CENTER", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0b1015; }
    /* Khung xanh bo tròn lấp đầy màn hình */
    .rok-container {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border: 2px solid #3eb5e5;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        color: white;
    }
    /* Lưới thông số lấp đầy khoảng trống */
    .stats-row {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-top: 20px;
    }
    .stat-card {
        flex: 1;
        background: rgba(0, 0, 0, 0.4);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
    }
    .label { color: #b0d4e3; font-size: 13px; font-weight: bold; text-transform: uppercase; }
    .value { font-size: 24px; font-weight: 800; display: block; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# --- 2. HÀM CHỐNG LỖI DỮ LIỆU ---
def safe_num(val):
    """Chuyển đổi an toàn sang số, nếu lỗi trả về 0 thay vì làm sập app"""
    try:
        return float(str(val).replace(',', '').strip())
    except:
        return 0.0

def draw_gauge(val, color, title):
    v = safe_num(val)
    fig = go.Figure(go.Pie(
        hole=0.7, values=[v, max(0, 100-v)],
        marker=dict(colors=[color, "rgba(255,255,255,0.1)"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        title={'text': title, 'y':0.9, 'x':0.5, 'xanchor':'center', 'font':{'color':'white','size':14}},
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=30, b=0, l=0, r=0), height=180,
        annotations=[dict(text=f"{v}%", x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=22))]
    )
    return fig

# --- 3. XỬ LÝ DỮ LIỆU ---
@st.cache_data(ttl=30)
def load_and_merge():
    try:
        sid = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
        u1 = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=731741617'
        u2 = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=371969335'
        
        df1 = pd.read_csv(u1)
        df2 = pd.read_csv(u2)
        
        # Ép kiểu ID về string để merge không lỗi
        df1['ID'] = df1['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df2['ID'] = df2['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        
        df = pd.merge(df1, df2, on='ID', suffixes=('_1', '_2'))
        
        # Tính toán KPI an toàn
        def calc(r):
            sm = safe_num(r['Sức Mạnh_2'])
            gk = 300e6 if sm >= 45e6 else 220e6 if sm >= 35e6 else 130e6 if sm >= 25e6 else 80e6
            gd = 400e3 if sm >= 30e6 else 200e3
            
            ki = max(0, safe_num(r['Tổng Tiêu Diệt_2']) - safe_num(r['Tổng Tiêu Diệt_1']))
            di = max(0, safe_num(r['Điểm Chết_2']) - safe_num(r['Điểm Chết_1']))
            
            pk = round((ki/gk*100), 1) if gk > 0 else 0
            pd_v = round((di/gd*100), 1) if gd > 0 else 0
            return pd.Series([pk, pd_v, round((pk+pd_v)/2, 1)])

        df[['PK', 'PD', 'PT']] = df.apply(calc, axis=1)
        return df
    except:
        return None

df = load_and_merge()

# --- 4. HIỂN THỊ ---
if df is not None:
    names = sorted(df['Tên_2'].dropna().astype(str).unique())
    sel = st.selectbox("🔍 CHỌN THỐNG ĐỐC:", ["---"] + names)
    
    if sel != "---":
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # TOÀN BỘ TRONG KHUNG XANH
        st.markdown('<div class="rok-container">', unsafe_allow_html=True)
        
        # Header
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h1 style="margin:0; font-size:45px; text-transform:uppercase;">{sel}</h1>
                    <p style="color:#b0d4e3; font-size:16px;">ID: {d['ID']} | Liên minh: [{d['Liên Minh_2']}]</p>
                </div>
                <div style="text-align:right;">
                    <span style="background:#f39c12; padding:5px 15px; border-radius:20px; font-weight:bold;">S-RANK</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Stats Row (Lấp đầy khung)
        st.markdown('<div class="stats-row">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="stat-card"><span class="label">Tiêu diệt</span><span class="value">{int(safe_num(d["Tổng Tiêu Diệt_2"])):,}</span></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="stat-card"><span class="label">Sức mạnh</span><span class="value">{int(safe_num(d["Sức Mạnh_2"])):,}</span></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="stat-card"><span class="label">Điểm chết</span><span class="value">{int(safe_num(d["Điểm Chết_2"])):,}</span></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="stat-card"><span class="label">Chiến công</span><span class="value">0</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # KPI Section (3 vòng tròn)
        st.markdown('<div style="margin-top:30px; background:rgba(0,0,0,0.2); padding:20px; border-radius:10px;">', unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.plotly_chart(draw_gauge(d['PK'], "#00ffff", "KPI KILL"), use_container_width=True, config={'displayModeBar': False})
        with k2: st.plotly_chart(draw_gauge(d['PD'], "#ff4b4b", "KPI DEAD"), use_container_width=True, config={'displayModeBar': False})
        with k3: st.plotly_chart(draw_gauge(d['PT'], "#ffd700", "TOTAL KPI"), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # Đóng rok-container
else:
    st.error("Không thể kết nối dữ liệu. Vui lòng kiểm tra Google Sheet.")
