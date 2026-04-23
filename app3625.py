import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="ROK PROFILE PRO", layout="wide")

# --- 2. CSS NỀN XANH BAO QUANH TOÀN BỘ (SỬA LỖI HIỂN THỊ) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1015; }
    
    /* Khung xanh bao quanh tất cả giống Profile game */
    .main-container {
        background: linear-gradient(180deg, #1d82b5 0%, #135d88 100%);
        border-radius: 15px;
        padding: 25px;
        border: 2px solid #3eb5e5;
        color: white;
        width: 100%;
    }

    /* Tên và ID */
    .p-name { font-size: 38px; font-weight: 800; text-transform: uppercase; margin: 0; line-height: 1.2; }
    .p-id { font-size: 14px; color: #b0d4e3; margin-bottom: 20px; }

    /* Ô thông số nền mờ */
    .stat-box {
        background: rgba(0, 0, 0, 0.35);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-bottom: 10px;
    }
    .s-label { color: #b0d4e3; font-size: 12px; text-transform: uppercase; display: block; font-weight: bold; }
    .s-value { font-size: 24px; font-weight: 800; color: white; display: block; margin-top: 5px; }

    /* Khung chứa biểu đồ KPI */
    .kpi-section {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ BIỂU ĐỒ (ĐÃ SỬA LỖI VALUERROR) ---
def draw_kpi(pct, color, title):
    # Đảm bảo pct là số
    try:
        val = round(float(pct), 1)
    except:
        val = 0.0
    
    # Giới hạn giá trị từ 0-100 để biểu đồ không lỗi
    display_val = min(max(val, 0.0), 100.0)
    
    fig = go.Figure(go.Pie(
        hole=0.7, 
        values=[display_val, 100 - display_val],
        marker=dict(colors=[color, "rgba(255,255,255,0.05)"]),
        showlegend=False, 
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title={'text': title, 'y':0.95, 'x':0.5, 'xanchor':'center', 'font':{'color':'white','size':14}},
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, b=0, l=10, r=10), 
        height=180,
        # SỬA LỖI TẠI ĐÂY: Loại bỏ fontWeight và dùng thẻ <b>
        annotations=[dict(
            text=f"<b>{val}%</b>", 
            x=0.5, y=0.5, 
            showarrow=False, 
            font=dict(color='white', size=20)
        )]
    )
    return fig

# --- 4. DATA LOGIC (CHỐNG LỖI MERGE & ÉP KIỂU) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        df_t = pd.read_csv(URL_T)
        df_s = pd.read_csv(URL_S)
        
        # Dọn dẹp tên cột
        df_t.columns = df_t.columns.str.strip()
        df_s.columns = df_s.columns.str.strip()
        
        # Ép kiểu ID về chuỗi để không bao giờ lỗi Merge
        df_t['ID'] = df_t['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df_s['ID'] = df_s['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        
        df = pd.merge(df_t, df_s, on='ID', suffixes=('_1', '_2'))
        
        # Chuyển đổi dữ liệu số an toàn (loại bỏ dấu phẩy rác)
        num_cols = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in num_cols:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', ''), errors='coerce').fillna(0)

        def calculate_kpis(r):
            sm = r['Sức Mạnh_2']
            # Công thức KPI của bạn
            target_k = 300e6 if sm >= 45e6 else 220e6 if sm >= 35e6 else 130e6 if sm >= 25e6 else 80e6
            target_d = 400e3 if sm >= 30e6 else 200e3
            
            diff_k = max(0, r['Tổng Tiêu Diệt_2'] - r['Tổng Tiêu Diệt_1'])
            diff_d = max(0, r['Điểm Chết_2'] - r['Điểm Chết_1'])
            
            pk = round((diff_k / target_k * 100), 1) if target_k > 0 else 0
            pd_v = round((diff_d / target_d * 100), 1) if target_d > 0 else 0
            return pd.Series([round((pk + pd_v) / 2, 1), pk, pd_v])
        
        df[['KPI_T', 'KPI_K', 'KPI_D']] = df.apply(calculate_kpis, axis=1)
        return df
    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")
        return None

df = load_data()

# --- 5. GIAO DIỆN HIỂN THỊ ---
if df is not None:
    names = sorted(df['Tên_2'].dropna().unique())
    sel_name = st.selectbox("🔍 CHỌN THỐNG ĐỐC:", ["---"] + names)
    
    if sel_name != "---":
        d = df[df['Tên_2'] == sel_name].iloc[0]
        
        # --- BẮT ĐẦU KHUNG XANH BAO QUANH TOÀN BỘ ---
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # Header: Tên & ID
        st.markdown(f'<div class="p-name">{sel_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="p-id">ID: {d["ID"]} | Liên minh: [{d["Liên Minh_2"]}]</div>', unsafe_allow_html=True)
        
        # Hàng 1: Ô thông số (4 cột lấp đầy)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="stat-box"><span class="s-label">Tiêu Diệt</span><span class="s-value">{int(d["Tổng Tiêu Diệt_2"]):,}</span></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="stat-box"><span class="s-label">Sức Mạnh</span><span class="s-value">{int(d["Sức Mạnh_2"]):,}</span></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="stat-box"><span class="s-label">Điểm Chết</span><span class="s-value">{int(d["Điểm Chết_2"]):,}</span></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="stat-box"><span class="s-label">Xếp hạng</span><span class="s-value">S-RANK</span></div>', unsafe_allow_html=True)
        
        # Hàng 2: Biểu đồ KPI nằm trong khung mờ phía dưới (vẫn thuộc khung xanh)
        st.markdown('<div class="kpi-section">', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; font-size:12px; font-weight:bold; color:#b0d4e3; letter-spacing:1px;">KẾT QUẢ CHIẾN DỊCH KVK</p>', unsafe_allow_html=True)
        
        k1, k2, k3 = st.columns(3)
        with k1: st.plotly_chart(draw_kpi(d['KPI_K'], "#00ffff", "KPI KILL"), use_container_width=True, config={'displayModeBar': False})
        with k2: st.plotly_chart(draw_kpi(d['KPI_D'], "#ff4b4b", "KPI DEAD"), use_container_width=True, config={'displayModeBar': False})
        with k3: st.plotly_chart(draw_kpi(d['KPI_T'], "#ffd700", "TỔNG KPI"), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # --- KẾT THÚC KHUNG XANH ---
