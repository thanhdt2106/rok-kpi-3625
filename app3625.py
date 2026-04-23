import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | SIDEBAR CENTER", layout="wide")

# --- 2. SIÊU CSS (TỐI ƯU SIDEBAR & BẢNG) ---
st.markdown("""
    <style>
    /* Tổng thể */
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    header { visibility: hidden; }
    
    /* TÙY CHỈNH SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #0d1b2a !important;
        border-right: 2px solid #00d4ff;
    }
    section[data-testid="stSidebar"] .stSelectbox label, 
    section[data-testid="stSidebar"] .stMarkdown {
        color: #00d4ff !important;
        font-weight: bold;
    }

    /* TIÊU ĐỀ TRÊN CÙNG TRANG CHÍNH */
    .main-title {
        text-align: center;
        font-size: 30px;
        font-weight: 900;
        color: #fff;
        text-shadow: 0 0 15px #00d4ff;
        margin-bottom: 30px;
        letter-spacing: 2px;
    }

    /* STYLE CHO BẢNG DỮ LIỆU */
    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 15px; }
    .elite-table { width: 100%; border-collapse: collapse; font-family: sans-serif; }
    .elite-table th { background: rgba(0, 212, 255, 0.1); color: #00d4ff; padding: 12px; border-bottom: 2px solid #00d4ff; text-align: center; }
    .elite-table td { padding: 10px; border-bottom: 1px solid #1a2a3a; text-align: center; color: #e0e6ed; }
    .rank-badge { background: linear-gradient(135deg, #ffd700, #b8860b); color: #000; padding: 3px 8px; border-radius: 4px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA LOGIC ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        for d in [dt, ds]:
            d['ID'] = d['ID'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        df = pd.merge(dt.drop_duplicates('ID'), ds.drop_duplicates('ID'), on='ID', suffixes=('_1', '_2'))
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
        def calc_kpi(r):
            p = r['Sức Mạnh_2']
            tk = 300e6 if p >= 45e6 else 200e6
            td = 400e3 if p >= 30e6 else 200e3
            pk = round((r['KI'] / tk * 100), 1) if tk > 0 else 0
            pdv = round((r['DI'] / td * 100), 1) if td > 0 else 0
            return pd.Series([pk, pdv, round((pk + pdv) / 2, 1)])
            
        df[['KPI_K', 'KPI_D', 'KPI_T']] = df.apply(calc_kpi, axis=1)
        df['Rank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)
        return df
    except: return None

df = load_data()

# --- 4. SIDEBAR - ĐƯA TẤT CẢ THÔNG TIN VÀO ĐÂY ---
if df is not None:
    with st.sidebar:
        st.image("https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true", width=80)
        st.markdown("### 🛡️ FTD 3625 SYSTEM")
        st.divider()

        # 1. Tìm kiếm
        sel = st.selectbox("👤 TÌM THÀNH VIÊN", sorted(df['Tên_2'].dropna().unique()), index=None, placeholder="Nhập tên...")

        # 2. Ngôn ngữ
        lang = st.radio("🌐 NGÔN NGỮ", ["VN", "EN"], horizontal=True)

        # 3. Nút Profile (Dạng Button lớn)
        if st.button("📊 XEM CHI TIẾT PROFILE", use_container_width=True):
            st.toast("Đã cập nhật Profile")

        st.divider()
        # 4. Cài đặt hệ thống (Thay vì Drawer, đưa trực tiếp các mục vào sidebar)
        st.markdown("⚙️ **CÀI ĐẶT HỆ THỐNG**")
        st.button("⚠️ Missing KPI Accounts", use_container_width=True)
        st.button("🏔️ Pass 4 Rankings", use_container_width=True)
        st.button("🌋 Pass 7 Rankings", use_container_width=True)
        st.button("👑 Kingland Stats", use_container_width=True)
        
        st.divider()
        st.markdown(f"**Admin:** Louis  \n**Version:** 12.2")

    # --- 5. HIỂN THỊ TRANG CHÍNH ---
    st.markdown('<div class="main-title">FIGHT TO DEAD 3625</div>', unsafe_allow_html=True)

    t = {
        "VN": {"headers": ['Hạng', 'Thành viên', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']},
        "EN": {"headers": ['Rank', 'Member', 'Power', 'Total Kill', 'Dead Pt', 'Kill +', 'Dead +', 'KPI %']}
    }[lang]

    # Hiển thị Card nếu chọn thành viên
    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        st.markdown(f"""
            <div style="background: rgba(0, 212, 255, 0.05); border: 1px solid #00d4ff; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                <h2 style="color:#00d4ff; margin:0;">{sel} <small style="color:#8b949e; font-size:14px;">(ID: {d['ID']})</small></h2>
                <div style="display: flex; gap: 30px; margin-top: 15px;">
                    <div><b>Rank:</b> #{int(d['Rank'])}</div>
                    <div><b>KPI Tổng:</b> <span style="color:#ffd700">{d['KPI_T']}%</span></div>
                    <div><b>Liên Minh:</b> {d['Liên Minh_2']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Bảng dữ liệu chính
    df_sorted = df.sort_values(by='Rank')
    rows = []
    for _, r in df_sorted.iterrows():
        rows.append(f"""
            <tr>
                <td><span class='rank-badge'>#{int(r['Rank'])}</span></td>
                <td><b>{r['Tên_2']}</b><br><small>ID: {r['ID']}</small></td>
                <td>{int(r['Sức Mạnh_2']):,}</td>
                <td style='color:#00ffcc'>{int(r['Tổng Tiêu Diệt_2']):,}</td>
                <td style='color:#ff4b4b'>{int(r['Điểm Chết_2']):,}</td>
                <td style='color:#00d4ff'>+{int(r['KI']):,}</td>
                <td style='color:#ff4b4b'>+{int(r['DI']):,}</td>
                <td style='color:#ffd700; font-weight:bold'>{r['KPI_T']}%</td>
            </tr>
        """)

    html_table = f"""
    <div class="table-wrapper">
        <table class="elite-table">
            <thead>
                <tr>{"".join([f"<th>{h}</th>" for h in t["headers"]])}</tr>
            </thead>
            <tbody>
                {"".join(rows)}
            </tbody>
        </table>
    </div>
    """
    st.markdown(html_table, unsafe_allow_html=True)

else:
    st.error("⚠️ Không thể tải dữ liệu. Hãy kiểm tra kết nối Google Sheets.")
