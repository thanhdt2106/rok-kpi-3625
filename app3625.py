import streamlit as st
import pandas as pd  # Đã sửa lại lỗi import pd ở đây
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS: ĐẨY CAO, CĂN GIỮA Ô & TIÊU ĐỀ VÀNG ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    
    /* ĐẨY SÁT LÊN TRÊN & CĂN GIỮA */
    .main .block-container {
        max-width: 1250px !important;
        padding-top: 0.1rem !important; /* Đẩy sát kịch trần */
        margin: auto !important;
    }

    /* LOGO CĂN GIỮA */
    .logo-container { display: flex; justify-content: center; width: 100%; margin-bottom: 10px; }
    .logo-img { width: 280px; filter: drop-shadow(0 0 10px rgba(0,212,255,0.3)); }

    /* BẢNG DỮ LIỆU: CĂN GIỮA Ô & MÀU VÀNG */
    .table-wrapper { 
        background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; 
        border-radius: 12px; padding: 15px; margin: 10px auto; 
    }
    .elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
    
    /* Tiêu đề bảng căn giữa */
    .elite-table thead th { 
        background: rgba(0, 212, 255, 0.1); color: #00d4ff; 
        text-align: center; padding: 12px; font-size: 13px; 
        border-bottom: 3px solid #00d4ff;
    }

    /* Nội dung ô căn giữa & màu vàng các cột ID, Power, Kill, Dead */
    .elite-table td { 
        padding: 12px 8px; font-size: 14px; color: #e0e6ed; 
        border-bottom: 1px solid #1a2a3a; text-align: center; 
    }
    .val-gold { color: #ffd700 !important; font-weight: bold; }
    
    .rank-badge { 
        background: linear-gradient(135deg, #ffd700, #b8860b); color: #000; 
        padding: 3px 8px; border-radius: 4px; font-weight: 900;
    }
    
    .kpi-bar-container { width: 80px; background: #1a2a3a; height: 6px; border-radius: 3px; display: inline-block; margin-right: 5px; }
    .kpi-bar-fill { height: 100%; border-radius: 3px; background: linear-gradient(90deg, #00d4ff, #00ffcc); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="color: #00d4ff; font-weight: bold; font-size: 18px; text-align: center; margin-bottom: 20px;">🛡️ COMMAND CENTER</div>', unsafe_allow_html=True)
    lang = st.radio("Language", ["VN", "EN"], horizontal=True)
    
    texts = {
        "VN": {
            "menu": ["📊 Bảng KPI", "👤 Tài khoản"],
            "search": "👤 Tìm kiếm thành viên...",
            "headers": ['Hạng', 'Thành viên', 'ID', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']
        },
        "EN": {
            "menu": ["📊 KPI Leaderboard", "👤 Profile"],
            "search": "👤 Search member...",
            "headers": ['Rank', 'Member', 'ID', 'Power', 'Total Kill', 'Dead Pt', 'Kill +', 'Dead +', 'KPI %']
        }
    }
    t = texts[lang]
    menu = st.radio("Menu", t["menu"])

# --- 4. DATA LOGIC (FIX LỖI MERGE ID & FLOAT) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        
        # Chuyển ID về chuỗi để không bị lỗi merge float/str
        dt['ID'] = dt['ID'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        ds['ID'] = ds['ID'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        
        df = pd.merge(dt.drop_duplicates('ID'), ds.drop_duplicates('ID'), on='ID', suffixes=('_1', '_2'))
        
        # Xử lý số liệu
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
        def calc_kpi(r):
            p = r['Sức Mạnh_2']
            target_k = 300e6 if p >= 45e6 else 200e6
            target_d = 400e3 if p >= 30e6 else 200e3
            pk = round((r['KI'] / target_k * 100), 1) if target_k > 0 else 0
            pdv = round((r['DI'] / target_d * 100), 1) if target_d > 0 else 0
            return pd.Series([pk, pdv, round((pk + pdv) / 2, 1)])
            
        df[['KPI_K', 'KPI_D', 'KPI_T']] = df.apply(calc_kpi, axis=1)
        df['Rank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)
        return df
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu: {e}")
        return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    # Logo
    st.markdown('<div class="logo-container"><img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true" class="logo-img"></div>', unsafe_allow_html=True)
    
    # Thanh tìm kiếm
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        sel = st.selectbox("", sorted(df['Tên_2'].dropna().unique()), index=None, placeholder=t["search"], label_visibility="collapsed")
    
    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        # TRẢ VỀ FORM PROFILE GỐC CỦA BẠN (image_16d9c2.png)
        html_card = f"""
        <div style="position: relative; width: 100%; max-width: 900px; margin: 45px auto 10px; font-family: 'Segoe UI', sans-serif;">
            <div style="position: absolute; top: -40px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 10px; padding: 8px 30px; z-index: 10; text-align: center; box-shadow: 0 0 15px rgba(0, 212, 255, 0.4);">
                <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true" style="width: 30px;">
                    <div style="color: #ffffff; font-size: 22px; font-weight: bold;">{sel}</div>
                </div>
                <div style="font-size: 10px; color: #00d4ff; opacity: 0.8;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
            </div>
            <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 12px; padding: 60px 20px 20px 20px;">
                <div style="display: flex; justify-content: space-around; align-items: center; border: 1px solid rgba(0, 212, 255, 0.1); padding: 30px; border-radius: 10px;">
                    <div style="text-align: center;"><div style="color:#00ffff; font-size: 20px; font-weight:bold;">{d['KPI_K']}%</div><div style="font-size:10px; color:#00ffff; margin-top:5px;">KILL KPI</div></div>
                    <div style="text-align: center;"><div style="color:#ffd700; font-size:36px; font-weight:bold; text-shadow: 0 0 15px rgba(255,215,0,0.5);">{d['KPI_T']}%</div><div style="font-size:11px; color:#ffd700; font-weight:bold; margin-top:5px;">TOTAL KPI</div></div>
                    <div style="text-align: center;"><div style="color:#ff4b4b; font-size: 20px; font-weight:bold;">{d['KPI_D']}%</div><div style="font-size:10px; color:#ff4b4b; margin-top:5px;">DEAD KPI</div></div>
                </div>
            </div>
        </div>
        """
        components.html(html_card, height=300)

    # --- BẢNG DỮ LIỆU ---
    df_sorted = df.sort_values(by='Rank')
    rows_list = []
    for _, r in df_sorted.iterrows():
        rows_list.append(f"""
        <tr>
            <td><span class="rank-badge">#{int(r['Rank'])}</span></td>
            <td style="text-align:left"><b style="color:#fff">{r['Tên_2']}</b></td>
            <td class="val-gold">{r['ID']}</td>
            <td class="val-gold">{int(r['Sức Mạnh_2']):,}</td>
            <td class="val-gold">{int(r['Tổng Tiêu Diệt_2']):,}</td>
            <td class="val-gold">{int(r['Điểm Chết_2']):,}</td>
            <td style="color:#00ffcc">+{int(r['KI']):,}</td>
            <td style="color:#ff4b4b">+{int(r['DI']):,}</td>
            <td>
                <div class="kpi-bar-container"><div class="kpi-bar-fill" style="width:{min(r['KPI_T'], 100)}%"></div></div>
                <span style="color:#ffd700; font-weight:bold">{r['KPI_T']}%</span>
            </td>
        </tr>""")

    table_html = f"""
    <div class="table-wrapper">
        <table class="elite-table">
            <thead><tr>{"".join([f"<th>{h}</th>" for h in t["headers"]])}</tr></thead>
            <tbody>{"".join(rows_list)}</tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center; color: #8b949e; font-size: 11px; padding: 15px;">🛡️ Admin Louis | v10.9 | Kingdom 3625</div>', unsafe_allow_html=True)
