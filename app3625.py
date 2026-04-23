import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. Cấu hình ---
st.set_page_config(page_title="ROK KPI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    .main-card { background: #135d88; border-radius: 10px; padding: 20px; border: 1px solid #3eb5e5; }
    .stat-box { background: rgba(0,0,0,0.3); padding: 10px; border-radius: 5px; border: 1px solid rgba(255,255,255,0.1); }
    .label { color: #b0d4e3; font-size: 0.8rem; }
    .value { color: white; font-size: 1.2rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Hàm vẽ biểu đồ ổn định ---
def create_chart(val, color, title):
    fig = go.Figure(go.Pie(
        hole=0.7, values=[val, max(0, 100-val)],
        marker=dict(colors=[color, "#222"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        title={'text': title, 'y':0.9, 'x':0.5, 'xanchor': 'center', 'font': {'color': 'white'}},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=30, b=0, l=0, r=0), height=150,
        annotations=[dict(text=str(val)+'%', x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=15))]
    )
    return fig

# --- 3. Xử lý dữ liệu (Chống lỗi so sánh) ---
@st.cache_data(ttl=60)
def load_data():
    try:
        sid = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
        df1 = pd.read_csv("https://docs.google.com/spreadsheets/d/{}/export?format=csv&gid=731741617".format(sid))
        df2 = pd.read_csv("https://docs.google.com/spreadsheets/d/{}/export?format=csv&gid=371969335".format(sid))
        
        # Làm sạch ID
        for d in [df1, df2]:
            d['ID'] = d['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        
        df = pd.merge(df1, df2, on='ID', suffixes=('_1', '_2'))
        
        # Ép kiểu số để tránh lỗi '>='
        num_cols = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in num_cols:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        def calc_kpi(r):
            p = r['Sức Mạnh_2']
            target_k = 300e6 if p >= 45e6 else 220e6 if p >= 35e6 else 130e6 if p >= 25e6 else 80e6
            target_d = 400e3 if p >= 30e6 else 200e3
            k_inc = max(0, r['Tổng Tiêu Diệt_2'] - r['Tổng Tiêu Diệt_1'])
            d_inc = max(0, r['Điểm Chết_2'] - r['Điểm Chết_1'])
            pk = round((k_inc/target_k*100), 1) if target_k > 0 else 0
            pd_v = round((d_inc/target_d*100), 1) if target_d > 0 else 0
            return pd.Series([pk, pd_v, round((pk+pd_v)/2, 1)])

        df[['PK', 'PD', 'PT']] = df.apply(calc_kpi, axis=1)
        return df
    except Exception as e:
        st.error("Lỗi: {}".format(e))
        return None

df = load_data()

# --- 4. Giao diện ---
if df is not None:
    sel = st.selectbox("CHỌN THỐNG ĐỐC:", ["---"] + sorted(df['Tên_2'].unique().tolist()))
    
    if sel != "---":
        row = df[df['Tên_2'] == sel].iloc[0]
        
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        
        # Header
        st.write("### {} (ID: {})".format(sel, row['ID']))
        st.write("Liên minh: **{}**".format(row['Liên Minh_2']))
        
        st.write("---")
        
        # Stats
        c1, c2, c3, c4 = st.columns(4)
        stats = [
            ("TIÊU DIỆT", row['Tổng Tiêu Diệt_2']),
            ("SỨC MẠNH", row['Sức Mạnh_2']),
            ("CHIẾN CÔNG", 0),
            ("HẠNG", "---")
        ]
        
        cols = [c1, c2, c3, c4]
        for i, col in enumerate(cols):
            with col:
                val_str = "{:,}".format(int(stats[i][1])) if isinstance(stats[i][1], (int, float)) else stats[i][1]
                st.markdown('<div class="stat-box"><div class="label">{}</div><div class="value">{}</div></div>'.format(stats[i][0], val_str), unsafe_allow_html=True)

        st.write("")
        
        # KPI Charts
        k1, k2, k3 = st.columns(3)
        with k1: st.plotly_chart(create_chart(row['PK'], "#00ffff", "KPI KILL"), use_container_width=True)
        with k2: st.plotly_chart(create_chart(row['PD'], "#ff4b4b", "KPI DEAD"), use_container_width=True)
        with k3: st.plotly_chart(create_chart(row['PT'], "#ffd700", "TOTAL KPI"), use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
