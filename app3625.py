import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. SIÊU CSS & JS (THÊM LẠI TASKBAR VÀ GIỮ NGUYÊN CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    
    /* ĐẨY SÁT LÊN TRÊN */
    .main .block-container {
        max-width: 98% !important;
        padding-top: 0rem !important;
        margin: auto !important;
    }
    header { visibility: hidden !important; }

    /* TASKBAR (THANH ĐIỀU HƯỚNG TRÊN CÙNG) */
    .navbar {
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(13, 27, 42, 0.9); padding: 10px 20px;
        border-bottom: 1px solid #00d4ff; position: sticky; top: 0; z-index: 999;
    }
    .nav-btn {
        background: transparent; color: #00d4ff; border: 1px solid #00d4ff;
        padding: 5px 15px; border-radius: 4px; cursor: pointer; font-weight: bold;
    }

    /* HIỆU ỨNG PHÁT SÁNG CHO LOGO CHÍNH */
    .logo-container { display: flex; justify-content: center; width: 100%; margin-bottom: 5px; margin-top: 10px; }
    .logo-img { width: 320px; filter: drop-shadow(0 0 15px rgba(0,212,255,0.6)); }

    /* NGĂN KÉO (DRAWER) */
    #myDrawer {
        height: 100%; width: 0; position: fixed; z-index: 1000000;
        top: 0; left: 0; background-color: rgba(13, 27, 42, 0.98);
        overflow-x: hidden; transition: 0.5s; padding-top: 60px;
        border-right: 2px solid #00d4ff; box-shadow: 15px 0 30px rgba(0,0,0,0.7);
    }
    #myDrawer a {
        padding: 15px 25px; text-decoration: none; font-size: 15px; color: #e0e6ed;
        display: block; transition: 0.3s; border-bottom: 1px solid rgba(0,212,255,0.05);
    }
    #myDrawer .closebtn { position: absolute; top: 10px; right: 25px; font-size: 36px; color: #ff4b4b; }

    /* TABLE STYLE */
    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 20px; margin-top: 20px; }
    .elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
    
    /* CĂN GIỮA TIÊU ĐỀ */
    .elite-table thead th { 
        background: rgba(0, 212, 255, 0.1); color: #00d4ff; 
        text-align: center !important; 
        padding: 15px; font-size: 14px; border-bottom: 3px solid #00d4ff; 
    }
    
    .elite-table td { padding: 12px 15px; font-size: 14px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; }
    .rank-badge { 
        background: linear-gradient(135deg, #ffd700, #b8860b); color: #000; 
        padding: 4px 10px; border-radius: 6px; font-weight: 900;
    }
    .kpi-bar-container { width: 100px; background: #1a2a3a; height: 8px; border-radius: 4px; display: inline-block; margin-right: 8px; }
    .kpi-bar-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #00d4ff, #00ffcc); }
    </style>

    <div class="navbar">
        <button class="nav-btn" onclick="openNav()">☰ SYSTEM SETTINGS</button>
        <div style="color: #00d4ff; font-weight: bold; font-size: 14px;">FTD COMMAND CENTER</div>
    </div>

    <div id="myDrawer">
      <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
      <div style="color: #00d4ff; font-weight: bold; padding: 0 25px 20px; font-size: 18px; border-bottom: 1px solid #1e3a5a;">📋 QUICK INFO</div>
      <a>⚠️ Missing KPI Accounts</a>
      <a>🏔️ Top 15 Pass 4</a>
      <a>🌋 Top 15 Pass 7</a>
      <a>👑 Top 15 Kingland</a>
    </div>

    <script>
    function openNav() { document.getElementById("myDrawer").style.width = "320px"; }
    function closeNav() { document.getElementById("myDrawer").style.width = "0"; }
    </script>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR & LANG ---
with st.sidebar:
    st.markdown('<div style="color: #00d4ff; font-weight: bold; font-size: 18px; text-align: center; margin-bottom: 20px;">🛡️ COMMAND CENTER</div>', unsafe_allow_html=True)
    st.divider()
    lang = st.radio("Language", ["VN", "EN"], horizontal=True)
    
    texts = {
        "VN": {
            "menu": ["📊 Bảng KPI", "👤 Tài khoản", "⚙️ Quản lý KPI"],
            "search": "👤 Tìm kiếm thành viên...",
            "rank": "HẠNG", "pow": "SỨC MẠNH", "kill": "TỔNG KILL", "dead": "ĐIỂM CHẾT",
            "target": "Mục tiêu", "headers": ['Hạng', 'Thành viên', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']
        },
        "EN": {
            "menu": ["📊 KPI Leaderboard", "👤 Profile", "⚙️ Management"],
            "search": "👤 Search member...",
            "rank": "RANK", "pow": "POWER", "kill": "TOTAL KILL", "dead": "DEAD POINT",
            "target": "Target", "headers": ['Rank', 'Member', 'Power', 'Total Kill', 'Dead Pt', 'Kill +', 'Dead +', 'KPI %']
        }
    }
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

# --- 5. HIỂN THỊ ---
if df is not None:
    # HIỂN THỊ LOGO SÁT TRÊN
    st.markdown('<div class="logo-container"><img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true" class="logo-img"></div>', unsafe_allow_html=True)
    
    if menu in t["menu"][:2]:
        sel = st.selectbox("", sorted(df['Tên_2'].dropna().unique()), index=None, placeholder=t["search"], label_visibility="collapsed")
        
        if sel:
            d = df[df['Tên_2'] == sel].iloc[0]
            # GIỮ NGUYÊN FORM PROFILE CHI TIẾT CỦA LOUIS
            html_card = f"""
            <div style="position: relative; width: 100%; margin: 60px auto 20px; font-family: 'Segoe UI', sans-serif;">
                <div style="position: absolute; top: -55px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 12px 40px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);">
                    <div style="color: #00d4ff; font-size: 11px; font-weight: 900; letter-spacing: 2px; text-shadow: 0 0 5px #00d4ff;">MEMBER PROFILE</div>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 5px;">
                        <img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true" style="width: 40px; filter: drop-shadow(0 0 8px #ffd700);">
                        <div style="color: #ffffff; font-size: 28px; font-weight: bold; text-shadow: 0 0 10px #fff;">{sel}</div>
                    </div>
                    <div style="font-size: 12px; color: #e0e6ed; opacity: 0.8;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                </div>

                <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 85px 20px 25px 20px; box-shadow: inset 0 0 30px rgba(0, 212, 255, 0.1);">
                    <div style="display: flex; justify-content: space-between; gap: 10px; margin-bottom: 25px;">
                        <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1; text-align: center; border-bottom: 3px solid #ffd700; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                            <div style="font-size: 10px; color: #8b949e;">{t['rank']}</div>
                            <div style="font-size: 20px; font-weight: 900; color: #ffd700;">#{int(d['Rank'])}</div>
                        </div>
                        <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; text-align: center; border-bottom: 3px solid #00d4ff;">
                            <div style="font-size: 10px; color: #8b949e;">{t['pow']}</div>
                            <div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                        </div>
                        <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; text-align: center; border-bottom: 3px solid #00ffcc;">
                            <div style="font-size: 10px; color: #8b949e;">{t['kill']}</div>
                            <div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                        </div>
                        <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; text-align: center; border-bottom: 3px solid #ff4b4b;">
                            <div style="font-size: 10px; color: #8b949e;">{t['dead']}</div>
                            <div style="font-size: 20px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                        </div>
                    </div>

                    <div style="background: rgba(26, 42, 58, 0.5); border-radius: 15px; padding: 25px 5px; display: flex; justify-content: space-around; align-items: center; border: 1px solid rgba(0, 212, 255, 0.2);">
                        <div style="text-align: center;">
                            <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#00ffff; font-size: 18px; font-weight:bold;">{d['KPI_K']}%</div>
                            <div style="font-size:10px; color:#00ffff; font-weight:bold;">KILL KPI</div>
                            <div style="font-size:9px; color:#8b949e; margin-top:5px;">{t['target']}: {int(d['T_K']):,}</div>
                        </div>
                        <div style="text-align: center;">
                            <svg width="110" height="110" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ffd700; font-size:26px; font-weight:bold; text-shadow: 0 0 10px #ffd700;">{d['KPI_T']}%</div>
                            <div style="font-size:12px; color:#ffd700; font-weight:bold;">TOTAL KPI</div>
                        </div>
                        <div style="text-align: center;">
                            <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ff4b4b; font-size: 18px; font-weight:bold;">{d['KPI_D']}%</div>
                            <div style="font-size:10px; color:#ff4b4b; font-weight:bold;">DEAD KPI</div>
                            <div style="font-size:9px; color:#8b949e; margin-top:5px;">{t['target']}: {int(d['T_D']):,}</div>
                        </div>
                    </div>
                </div>
            </div>
            """
            components.html(html_card, height=530)

        # --- BẢNG TABLE (CĂN GIỮA TIÊU ĐỀ) ---
        df_sorted = df.sort_values(by='Rank')
        rows_list = []
        for _, r in df_sorted.iterrows():
            rows_list.append(f"""
            <tr>
                <td><span class="rank-badge">#{int(r['Rank'])}</span></td>
                <td><b style="color:#fff">{r['Tên_2']}</b><br><small style="color:#8b949e">ID: {r['ID']}</small></td>
                <td style="text-align:right">{int(r['Sức Mạnh_2']):,}</td>
                <td style="text-align:right; color:#00ffcc">{int(r['Tổng Tiêu Diệt_2']):,}</td>
                <td style="text-align:right; color:#ff4b4b">{int(r['Điểm Chết_2']):,}</td>
                <td style="text-align:right; color:#00d4ff">+{int(r['KI']):,}</td>
                <td style="text-align:right; color:#ff4b4b">+{int(r['DI']):,}</td>
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

    st.markdown(f'<div style="position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #8b949e; padding: 10px; text-align: center; border-top: 1px solid #1a2a3a; z-index:999;">🛡️ Admin Louis | v10.9 | Zalo: 0373274600</div>', unsafe_allow_html=True)
