import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. SIÊU CSS & JS (ÉP LOGO LÊN SÁT THANH TOOLBAR) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    
    /* TRIỆT TIÊU KHOẢNG TRỐNG MẶC ĐỊNH CỦA STREAMLIT */
    .main .block-container {
        max-width: 98% !important;
        padding-top: 0rem !important;  /* Đưa nội dung lên sát Toolbar */
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        margin: 0 auto !important;
    }

    /* ĐIỀU CHỈNH LOGO SÁT MÉP TRÊN */
    .logo-container { 
        display: flex; 
        justify-content: center; 
        width: 100%; 
        margin-top: 0px !important; /* Xóa khoảng cách trên */
        margin-bottom: 10px; 
        padding-top: 5px;
    }
    .logo-img { 
        width: 100%; 
        max-width: 280px; /* Thu nhỏ nhẹ logo để cân đối hơn */
        height: auto; 
        filter: drop-shadow(0 0 15px rgba(0,212,255,0.6)); 
    }

    /* NGĂN KÉO (DRAWER) */
    #myDrawer {
        height: 100%; width: 0; position: fixed; z-index: 1000000;
        top: 0; left: 0; background-color: rgba(13, 27, 42, 0.98);
        overflow-x: hidden; transition: 0.5s; padding-top: 60px;
        border-right: 2px solid #00d4ff; box-shadow: 15px 0 30px rgba(0,0,0,0.7);
    }
    #myDrawer a { padding: 15px 25px; text-decoration: none; font-size: 15px; color: #e0e6ed; display: block; transition: 0.3s; border-bottom: 1px solid rgba(0,212,255,0.05); }
    #myDrawer .closebtn { position: absolute; top: 10px; right: 25px; font-size: 36px; color: #ff4b4b; }

    /* TABLE MOBILE RESPONSIVE */
    .table-wrapper { 
        background: rgba(13, 27, 42, 0.6); 
        border: 1px solid #1e3a5a; 
        border-radius: 12px; 
        padding: 15px; 
        margin-top: 15px; 
        overflow-x: auto; 
    }
    .elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; min-width: 700px; }
    .elite-table thead th { background: rgba(0, 212, 255, 0.1); color: #00d4ff; text-align: center !important; padding: 12px; font-size: 14px; border-bottom: 3px solid #00d4ff; }
    .elite-table td { padding: 10px 15px; font-size: 13px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; }
    
    /* RESPONSIVE CHO FOOTER */
    @media only screen and (max-width: 600px) {
        .stMarkdown div p { font-size: 11px !important; }
        .logo-img { max-width: 200px; } /* Logo nhỏ hơn nữa trên điện thoại để tiết kiệm chỗ */
    }
    </style>

    <div id="myDrawer">
      <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
      <div style="color: #00d4ff; font-weight: bold; padding: 0 25px 20px; font-size: 18px; border-bottom: 1px solid #1e3a5a;">📋 QUICK INFO</div>
      <a>⚠️ Missing KPI Accounts</a>
      <a>🏔️ Top 15 Pass 4</a>
      <a>🌋 Top 15 Pass 7</a>
      <a>👑 Top 15 Kingland</a>
    </div>

    <script>
    function openNav() { document.getElementById("myDrawer").style.width = "300px"; }
    function closeNav() { document.getElementById("myDrawer").style.width = "0"; }
    </script>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR & LANG ---
with st.sidebar:
    st.markdown('<div style="color: #00d4ff; font-weight: bold; font-size: 18px; text-align: center; margin-bottom: 20px;">🛡️ COMMAND CENTER</div>', unsafe_allow_html=True)
    components.html("""
        <button onclick="parent.openNav()" style="width: 100%; background: #1a2a3a; color: #00d4ff; border: 1px solid #00d4ff; padding: 10px; border-radius: 5px; cursor: pointer; font-weight: bold; font-family: sans-serif;">
            ⚙️ SYSTEM SETTINGS
        </button>
    """, height=50)
    st.divider()
    lang = st.radio("Language", ["VN", "EN"], horizontal=True)
    texts = {"VN": {"menu": ["📊 Bảng KPI", "👤 Tài khoản", "⚙️ Quản lý KPI"], "search": "👤 Tìm kiếm thành viên...", "rank": "HẠNG", "pow": "SỨC MẠNH", "kill": "TỔNG KILL", "dead": "ĐIỂM CHẾT", "target": "Mục tiêu", "headers": ['Hạng', 'Thành viên', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']},
             "EN": {"menu": ["📊 KPI Leaderboard", "👤 Profile", "⚙️ Management"], "search": "👤 Search member...", "rank": "RANK", "pow": "POWER", "kill": "TOTAL KILL", "dead": "DEAD POINT", "target": "Target", "headers": ['Rank', 'Member', 'Power', 'Total Kill', 'Dead Pt', 'Kill +', 'Dead +', 'KPI %']}}
    t = texts[lang]
    menu = st.radio("Menu", t["menu"])

# --- 4. DATA LOGIC ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        for d in [dt, ds]: d['ID'] = d['ID'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        df = pd.merge(dt.drop_duplicates('ID'), ds.drop_duplicates('ID'), on='ID', suffixes=('_1', '_2'))
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        def calc_kpi(r):
            p, tk, td = r['Sức Mạnh_2'], (300e6 if r['Sức Mạnh_2'] >= 45e6 else 200e6), (400e3 if r['Sức Mạnh_2'] >= 30e6 else 200e3)
            pk, pdv = round((r['KI']/tk*100),1) if tk>0 else 0, round((r['DI']/td*100),1) if td>0 else 0
            return pd.Series([pk, pdv, round((pk+pdv)/2,1), tk, td])
        df[['KPI_K', 'KPI_D', 'KPI_T', 'T_K', 'T_D']] = df.apply(calc_kpi, axis=1)
        df['Rank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    # LOGO HIỆN TẠI ĐÃ ĐƯỢC ÉP SÁT LÊN TRÊN QUA CSS
    st.markdown('<div class="logo-container"><img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true" class="logo-img"></div>', unsafe_allow_html=True)
    
    if menu in t["menu"][:2]:
        sel = st.selectbox("", sorted(df['Tên_2'].dropna().unique()), index=None, placeholder=t["search"], label_visibility="collapsed")
        if sel:
            d = df[df['Tên_2'] == sel].iloc[0]
            html_card = f"""
            <style>
                .profile-container {{ position: relative; width: 100%; margin: 55px auto 15px; font-family: 'Segoe UI', sans-serif; }}
                .profile-header {{ position: absolute; top: -50px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 10px 30px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; min-width: 220px; }}
                .profile-body {{ background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 75px 15px 20px 15px; }}
                .stats-row {{ display: flex; justify-content: space-between; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }}
                .stat-box {{ background: #233549; border-radius: 8px; padding: 10px; flex: 1 1 110px; text-align: center; border-bottom: 3px solid #00d4ff; }}
                .kpi-row {{ background: rgba(26, 42, 58, 0.5); border-radius: 15px; padding: 20px 5px; display: flex; justify-content: space-around; align-items: center; border: 1px solid rgba(0, 212, 255, 0.2); flex-wrap: wrap; gap: 15px; }}
            </style>
            <div class="profile-container">
                <div class="profile-header">
                    <div style="color: #00d4ff; font-size: 10px; font-weight: 900; letter-spacing: 1px;">MEMBER PROFILE</div>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 3px;">
                        <img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true" style="width: 35px;">
                        <div style="color: #ffffff; font-size: 22px; font-weight: bold;">{sel}</div>
                    </div>
                </div>
                <div class="profile-body">
                    <div class="stats-row">
                        <div class="stat-box" style="border-bottom-color: #ffd700;"><small>{t['rank']}</small><br><b>#{int(d['Rank'])}</b></div>
                        <div class="stat-box"><small>{t['pow']}</small><br><b>{int(d['Sức Mạnh_2']):,}</b></div>
                        <div class="stat-box" style="border-bottom-color: #00ffcc;"><small>{t['kill']}</small><br><b>{int(d['Tổng Tiêu Diệt_2']):,}</b></div>
                        <div class="stat-box" style="border-bottom-color: #ff4b4b;"><small>{t['dead']}</small><br><b>{int(d['Điểm Chết_2']):,}</b></div>
                    </div>
                    <div class="kpi-row">
                        <div style="text-align: center;"><svg width="60" height="60" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg><div style="color:#00ffff; font-size: 14px; font-weight:bold;">{d['KPI_K']}%</div></div>
                        <div style="text-align: center;"><svg width="90" height="90" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg><div style="color:#ffd700; font-size:22px; font-weight:bold;">{d['KPI_T']}%</div><small style="color:#ffd700">TOTAL</small></div>
                        <div style="text-align: center;"><svg width="60" height="60" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg><div style="color:#ff4b4b; font-size: 14px; font-weight:bold;">{d['KPI_D']}%</div></div>
                    </div>
                </div>
            </div>
            """
            components.html(html_card, height=480)

        # --- BẢNG TABLE ---
        df_sorted = df.sort_values(by='Rank')
        rows_list = []
        for _, r in df_sorted.iterrows():
            rows_list.append(f"<tr><td><span class='rank-badge'>#{int(r['Rank'])}</span></td><td><b>{r['Tên_2']}</b><br><small>ID: {r['ID']}</small></td><td style='text-align:right'>{int(r['Sức Mạnh_2']):,}</td><td style='text-align:right; color:#00ffcc'>{int(r['Tổng Tiêu Diệt_2']):,}</td><td style='text-align:right; color:#ff4b4b'>{int(r['Điểm Chết_2']):,}</td><td style='text-align:right; color:#00d4ff'>+{int(r['KI']):,}</td><td style='text-align:right; color:#ff4b4b'>+{int(r['DI']):,}</td><td><span style='color:#ffd700; font-weight:bold'>{r['KPI_T']}%</span></td></tr>")

        st.markdown(f'<div class="table-wrapper"><table class="elite-table"><thead><tr>{"".join([f"<th>{h}</th>" for h in t["headers"]])}</tr></thead><tbody>{"".join(rows_list)}</tbody></table></div>', unsafe_allow_html=True)

    st.markdown(f'<div style="position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #8b949e; padding: 10px; text-align: center; border-top: 1px solid #1a2a3a; z-index:999; font-size:10px;">🛡️ Admin Louis | v10.9 | Zalo: 0373274600</div>', unsafe_allow_html=True)
