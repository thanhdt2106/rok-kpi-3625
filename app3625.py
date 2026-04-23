import streamlit as st

import pandas as pd

import streamlit.components.v1 as components



# --- 1. CẤU HÌNH TRANG ---

st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")



# --- 2. SIÊU CSS & JS (CUSTOM TASKBAR) ---

st.markdown("""

    <style>

    /* Giao diện tổng thể */

    .stApp { background-color: #050a0e; color: #e0e6ed; }

    

    /* ẨN CÁC PHẦN DƯ THỪA CỦA STREAMLIT */

    #MainMenu {visibility: hidden;}

    header {visibility: hidden;}

    footer {visibility: hidden;}

    [data-testid="stSidebar"] { display: none; } /* Ẩn luôn sidebar để dùng Header mới */



    /* ÉP NỘI DUNG SÁT TASKBAR */

    .main .block-container {

        max-width: 98% !important;

        padding-top: 65px !important; /* Khoảng cách để không bị đè bởi Header */

    }



    /* THANH TASKBAR MỚI */

    .custom-header {

        position: fixed; top: 0; left: 0; width: 100%; height: 60px;

        background: rgba(13, 27, 42, 0.95);

        border-bottom: 2px solid #00d4ff;

        display: flex; align-items: center; justify-content: space-between;

        padding: 0 20px; z-index: 999999;

        box-shadow: 0 4px 20px rgba(0,0,0,0.5);

    }



    /* PHẦN BÊN TRÁI: LOGO + TEXT */

    .header-left { display: flex; align-items: center; gap: 10px; }

    .header-logo { width: 35px; filter: drop-shadow(0 0 5px #00d4ff); }

    .header-title { 

        font-weight: 900; font-size: 16px; color: #fff; 

        letter-spacing: 1px; text-shadow: 0 0 10px #00d4ff;

        font-family: 'Segoe UI', sans-serif;

    }



    /* PHẦN GIỮA: Ô TÌM KIẾM (Sẽ được xử lý qua Streamlit container) */

    .header-mid { flex-grow: 1; max-width: 400px; padding: 0 20px; }



    /* PHẦN BÊN PHẢI: BUTTONS */

    .header-right { display: flex; align-items: center; gap: 15px; }

    .nav-btn {

        background: transparent; border: 1px solid rgba(0, 212, 255, 0.3);

        color: #e0e6ed; padding: 6px 12px; border-radius: 4px;

        cursor: pointer; font-size: 14px; transition: 0.3s;

    }

    .nav-btn:hover { background: #00d4ff; color: #000; box-shadow: 0 0 10px #00d4ff; }



    /* NGĂN KÉO SETTINGS */

    #myDrawer {

        height: 100%; width: 0; position: fixed; z-index: 1000001;

        top: 0; right: 0; background-color: rgba(13, 27, 42, 0.98);

        overflow-x: hidden; transition: 0.5s; padding-top: 60px;

        border-left: 2px solid #00d4ff;

    }

    #myDrawer a { padding: 15px 25px; text-decoration: none; font-size: 15px; color: #e0e6ed; display: block; border-bottom: 1px solid rgba(0,212,255,0.05); }

    #myDrawer .closebtn { position: absolute; top: 10px; left: 25px; font-size: 36px; color: #ff4b4b; }



    /* TABLE ELITE */

    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 20px; margin-top: 20px; }

    .elite-table { width: 100%; border-collapse: collapse; }

    .elite-table thead th { background: rgba(0, 212, 255, 0.1); color: #00d4ff; text-align: center!important; padding: 15px; border-bottom: 3px solid #00d4ff; }

    .elite-table td { padding: 12px; border-bottom: 1px solid #1a2a3a; text-align: center; }

    </style>



    <div id="myDrawer">

      <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>

      <div style="color: #00d4ff; font-weight: bold; padding: 0 25px 20px; font-size: 18px; border-bottom: 1px solid #1e3a5a;">📋 SYSTEM SETTINGS</div>

      <a>⚠️ Missing KPI Accounts</a>

      <a>🏔️ Pass 4 Rankings</a>

      <a>🌋 Pass 7 Rankings</a>

      <a>👑 Kingland Stats</a>

    </div>



    <script>

    function openNav() { document.getElementById("myDrawer").style.width = "320px"; }

    function closeNav() { document.getElementById("myDrawer").style.width = "0"; }

    </script>

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

            return pd.Series([pk, pdv, round((pk + pdv) / 2, 1), tk, td])

            

        df[['KPI_K', 'KPI_D', 'KPI_T', 'T_K', 'T_D']] = df.apply(calc_kpi, axis=1)

        df['Rank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)

        return df

    except: return None



df = load_data()



# --- 4. RENDER CUSTOM HEADER ---

if df is not None:

    # Header Container

    st.markdown("""

        <div class="custom-header">

            <div class="header-left">

                <img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true" class="header-logo">

                <span class="header-title">FIGHT TO DEAD 3625</span>

            </div>

            <div id="search-anchor" class="header-mid"></div>

            <div class="header-right" id="nav-right">

            </div>

        </div>

    """, unsafe_allow_html=True)



    # Đưa các widget Streamlit vào vị trí Header bằng cách dùng columns ảo hoặc CSS absolute

    # Để đơn giản và mượt nhất, ta dùng 3 columns ở đầu trang đè lên Header

    head_col1, head_col2, head_col3 = st.columns([1, 2, 1])



    with head_col2:

        # THANH TÌM KIẾM NẰM GIỮA

        search_label = "👤 Tìm kiếm..." if "VN" else "👤 Search..."

        sel = st.selectbox("", sorted(df['Tên_2'].dropna().unique()), index=None, placeholder=search_label, label_visibility="collapsed")



    with head_col3:

        # CÔNG TẮC VN/EN VÀ NÚT BẤM (Dùng container để đẩy sang phải)

        c1, c2, c3 = st.columns([1, 1, 1])

        with c1: lang = st.selectbox("", ["VN", "EN"], label_visibility="collapsed")

        with c2: 

            if st.button("👤", help="User Profile"): menu = "👤 Tài khoản"

        with c3:

            components.html("""<button onclick="parent.openNav()" style="background:transparent; border:1px solid #00d4ff; color:#00d4ff; width:35px; height:35px; border-radius:5px; cursor:pointer;">⚙️</button>""", height=40)



    # --- 5. HIỂN THỊ NỘI DUNG CHÍNH ---

    t = {

        "VN": {"rank": "HẠNG", "pow": "SỨC MẠNH", "kill": "TỔNG KILL", "dead": "ĐIỂM CHẾT", "target": "Mục tiêu", "headers": ['Hạng', 'Thành viên', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']},

        "EN": {"rank": "RANK", "pow": "POWER", "kill": "TOTAL KILL", "dead": "DEAD POINT", "target": "Target", "headers": ['Rank', 'Member', 'Power', 'Total Kill', 'Dead Pt', 'Kill +', 'Dead +', 'KPI %']}

    }[lang]



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

                <div style="font-size: 12px; color: #e0e6ed; opacity: 0.8;">ID: {d['ID']} | {d['Liên Minh_2']}</div>

            </div>

            <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 85px 20px 25px 20px;">

                <div style="display: flex; justify-content: space-between; gap: 10px; margin-bottom: 25px;">

                    <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1; text-align: center; border-bottom: 3px solid #ffd700;">

                        <div style="font-size: 10px; color: #8b949e;">{t['rank']}</div>

                        <div style="font-size: 20px; font-weight: 900; color: #ffd700;">#{int(d['Rank'])}</div>

                    </div>

                    <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; text-align: center; border-bottom: 3px solid #00d4ff;"><div style="font-size: 10px; color: #8b949e;">{t['pow']}</div><div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div></div>

                    <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; text-align: center; border-bottom: 3px solid #00ffcc;"><div style="font-size: 10px; color: #8b949e;">{t['kill']}</div><div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div></div>

                </div>

                <div style="background: rgba(26, 42, 58, 0.5); border-radius: 15px; padding: 25px 5px; display: flex; justify-content: space-around; align-items: center; border: 1px solid rgba(0, 212, 255, 0.2);">

                    <div style="text-align: center;">

                        <svg width="75" height="75" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>

                        <div style="color:#00ffff; font-size: 16px; font-weight:bold;">{d['KPI_K']}%</div><div style="font-size:9px; color:#00ffff;">KILL KPI</div>

                    </div>

                    <div style="text-align: center;">

                        <svg width="100" height="100" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>

                        <div style="color:#ffd700; font-size:24px; font-weight:bold;">{d['KPI_T']}%</div><div style="font-size:11px; color:#ffd700;">TOTAL KPI</div>

                    </div>

                    <div style="text-align: center;">

                        <svg width="75" height="75" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>

                        <div style="color:#ff4b4b; font-size: 16px; font-weight:bold;">{d['KPI_D']}%</div><div style="font-size:9px; color:#ff4b4b;">DEAD KPI</div>

                    </div>

                </div>

            </div>

        </div>

        """

        components.html(html_card, height=520)



    # --- BẢNG DỮ LIỆU ---

    df_sorted = df.sort_values(by='Rank')

    rows = []

    for _, r in df_sorted.iterrows():

        rows.append(f"<tr><td><span class='rank-badge'>#{int(r['Rank'])}</span></td><td><b>{r['Tên_2']}</b><br><small>ID: {r['ID']}</small></td><td style='text-align:right'>{int(r['Sức Mạnh_2']):,}</td><td style='text-align:right; color:#00ffcc'>{int(r['Tổng Tiêu Diệt_2']):,}</td><td style='text-align:right; color:#ff4b4b'>{int(r['Điểm Chết_2']):,}</td><td style='text-align:right; color:#00d4ff'>+{int(r['KI']):,}</td><td style='text-align:right; color:#ff4b4b'>+{int(r['DI']):,}</td><td><span style='color:#ffd700; font-weight:bold'>{r['KPI_T']}%</span></td></tr>")

    

    st.markdown(f'<div class="table-wrapper"><table class="elite-table"><thead><tr>{"".join([f"<th>{h}</th>" for h in t["headers"]])}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>', unsafe_allow_html=True)



    # Footer

    st.markdown(f'<div style="position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #8b949e; padding: 10px; text-align: center; border-top: 1px solid #1a2a3a; z-index:999; font-size:11px;">🛡️ Admin Louis | v11.0 | FTD COMMAND CENTER</div>', unsafe_allow_html=True)
