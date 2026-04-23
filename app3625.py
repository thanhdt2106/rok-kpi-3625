import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="FTD KPI | COMMAND CENTER", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. SIÊU CSS (FIX LỖI SEARCH & GỘP HEADER) ---
st.markdown("""
    <style>
    /* ẨN SIDEBAR & HEADER MẶC ĐỊNH */
    [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"] { display: none !important; width: 0px !important; }
    header { visibility: hidden; }

    .main .block-container {
        max-width: 100% !important;
        padding: 0.5rem 1.5rem !important;
        margin-left: 0px !important;
    }

    .stApp { background-color: #050a0e; color: #e0e6ed; }
    
    /* STYLE DÒNG CHỮ TRÁI */
    .header-left-container {
        display: flex;
        align-items: center;
        gap: 20px; /* Khoảng cách giữa chữ và nút gạt */
    }

    .header-left-text {
        color: #00d4ff;
        font-weight: 900;
        font-size: 20px;
        text-shadow: 0 0 10px #00d4ff;
        font-family: 'Segoe UI', sans-serif;
        white-space: nowrap;
    }

    /* FIX THANH TÌM KIẾM */
    div[data-testid="stSelectbox"] {
        width: 100% !important;
        max-width: 400px; /* Giới hạn độ rộng tìm kiếm để không bị loãng */
    }

    /* TABLE STYLE */
    .table-wrapper { 
        background: rgba(13, 27, 42, 0.6); 
        border: 1px solid #1e3a5a; 
        border-radius: 12px; 
        padding: 15px; 
        margin-top: 10px;
        overflow-x: auto;
    }
    .elite-table { width: 100%; border-collapse: collapse; min-width: 850px;}
    .elite-table thead th { 
        background: rgba(0, 212, 255, 0.1); color: #00d4ff; 
        text-align: center !important; 
        padding: 12px; font-size: 14px; border-bottom: 3px solid #00d4ff; 
    }
    .elite-table td { padding: 10px 15px; font-size: 14px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; }
    
    /* MOBILE RESPONSIVE */
    @media (max-width: 768px) {
        .header-left-container { flex-direction: column; align-items: flex-start; gap: 5px; }
        div[data-testid="stSelectbox"] { max-width: 100%; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA LOGIC (GIỮ NGUYÊN) ---
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
            target_k = 300e6 if p >= 45e6 else 200e6
            target_d = 400e3 if p >= 30e6 else 200e3
            pk = round((r['KI'] / target_k * 100), 1) if target_k > 0 else 0
            pdv = round((r['DI'] / target_d * 100), 1) if target_d > 0 else 0
            return pd.Series([pk, pdv, round((pk + pdv) / 2, 1), target_k, target_d])
            
        df[['KPI_K', 'KPI_D', 'KPI_T', 'T_K', 'T_D']] = df.apply(calc_kpi, axis=1)
        df['Rank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)
        return df
    except: return None

df = load_data()

# --- 4. HEADER LAYOUT MỚI ---
if df is not None:
    # Chia 2 cột: Cột trái chứa (Text + Lang), Cột phải chứa (Search)
    col1, col2 = st.columns([1, 1])

    with col1:
        # Tạo một hàng ngang cho Text và Toggle
        sub_col_text, sub_col_toggle = st.columns([2, 1])
        with sub_col_text:
            st.markdown('<div class="header-left-text">FIGHT TO DEAD 3625</div>', unsafe_allow_html=True)
        with sub_col_toggle:
            is_en = st.toggle("EN", value=False, label_visibility="collapsed")
            lang = "EN" if is_en else "VN"

    with col2:
        sel = st.selectbox("", sorted(df['Tên_2'].dropna().unique()), index=None, placeholder="🔍 Tìm tên thành viên...", label_visibility="collapsed")

    t = {
        "VN": {"rank": "HẠNG", "pow": "SỨC MẠNH", "kill": "TỔNG KILL", "dead": "ĐIỂM CHẾT", "headers": ['Hạng', 'Thành viên', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']},
        "EN": {"rank": "RANK", "pow": "POWER", "kill": "TOTAL KILL", "dead": "DEAD PT", "headers": ['Rank', 'Member', 'Power', 'Total Kill', 'Dead Pt', 'Kill +', 'Dead +', 'KPI %']}
    }[lang]

    # --- 5. PROFILE CHI TIẾT ---
    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        html_card = f"""
        <div style="position: relative; width: 100%; margin: 60px auto 20px; font-family: 'Segoe UI', sans-serif;">
            <div style="position: absolute; top: -55px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 12px 40px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);">
                <div style="color: #00d4ff; font-size: 11px; font-weight: 900; letter-spacing: 2px;">MEMBER PROFILE</div>
                <div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 5px;">
                    <img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true" style="width: 40px;">
                    <div style="color: #ffffff; font-size: 28px; font-weight: bold;">{sel}</div>
                </div>
            </div>
            <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 85px 20px 25px 20px; box-shadow: inset 0 0 30px rgba(0, 212, 255, 0.1);">
                <div style="display: flex; justify-content: space-between; gap: 10px; margin-bottom: 25px;">
                    <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1; text-align: center; border-bottom: 3px solid #ffd700;"><div style="font-size: 10px; color: #8b949e;">{t['rank']}</div><div style="font-size: 20px; font-weight: 900; color: #ffd700;">#{int(d['Rank'])}</div></div>
                    <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; text-align: center; border-bottom: 3px solid #00d4ff;"><div style="font-size: 10px; color: #8b949e;">{t['pow']}</div><div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div></div>
                    <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; text-align: center; border-bottom: 3px solid #00ffcc;"><div style="font-size: 10px; color: #8b949e;">{t['kill']}</div><div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div></div>
                    <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; text-align: center; border-bottom: 3px solid #ff4b4b;"><div style="font-size: 10px; color: #8b949e;">{t['dead']}</div><div style="font-size: 20px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div></div>
                </div>
                <div style="background: rgba(26, 42, 58, 0.5); border-radius: 15px; padding: 25px 5px; display: flex; justify-content: space-around; align-items: center; border: 1px solid rgba(0, 212, 255, 0.2);">
                    <div style="text-align: center;">
                        <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                        <div style="color:#00ffff; font-size: 18px; font-weight:bold;">{d['KPI_K']}%</div>
                    </div>
                    <div style="text-align: center;">
                        <svg width="110" height="110" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                        <div style="color:#ffd700; font-size:26px; font-weight:bold;">{d['KPI_T']}%</div>
                    </div>
                    <div style="text-align: center;">
                        <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                        <div style="color:#ff4b4b; font-size: 18px; font-weight:bold;">{d['KPI_D']}%</div>
                    </div>
                </div>
            </div>
        </div>
        """
        components.html(html_card, height=530)

    # --- 6. BẢNG TABLE ---
    df_sorted = df.sort_values(by='Rank')
    rows_list = []
    for _, r in df_sorted.iterrows():
        rows_list.append(f"""
        <tr>
            <td><span style="background:linear-gradient(135deg, #ffd700, #b8860b); color:#000; padding:4px 10px; border-radius:6px; font-weight:900;">#{int(r['Rank'])}</span></td>
            <td><b style="color:#fff">{r['Tên_2']}</b><br><small style="color:#8b949e">ID: {r['ID']}</small></td>
            <td style="text-align:right">{int(r['Sức Mạnh_2']):,}</td>
            <td style="text-align:right; color:#00ffcc">{int(r['Tổng Tiêu Diệt_2']):,}</td>
            <td style="text-align:right; color:#ff4b4b">{int(r['Điểm Chết_2']):,}</td>
            <td style="text-align:right; color:#00d4ff">+{int(r['KI']):,}</td>
            <td style="text-align:right; color:#ff4b4b">+{int(r['DI']):,}</td>
            <td>
                <div style="width: 100px; background: #1a2a3a; height: 8px; border-radius: 4px; display: inline-block; margin-right: 8px;">
                    <div style="height: 100%; border-radius: 4px; background: linear-gradient(90deg, #00d4ff, #00ffcc); width:{min(r['KPI_T'], 100)}%"></div>
                </div>
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

    # Footer
    st.markdown(f'<div style="position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #8b949e; padding: 10px; text-align: center; border-top: 1px solid #1a2a3a; z-index:999;">🛡️ Admin Louis | v11.3 | Zalo: 0373274600</div>', unsafe_allow_html=True)
