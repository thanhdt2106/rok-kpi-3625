import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. SIÊU CSS & JS (TỐI ƯU RESPONSIVE CHO ĐIỆN THOẠI) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    
    /* ĐẨY SÁT LÊN TRÊN VÀ TỐI ƯU MOBILE PADDING */
    .main .block-container {
        max-width: 98% !important;
        padding-top: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* LOGO TỰ CO GIÃN */
    .logo-container { display: flex; justify-content: center; width: 100%; margin-bottom: 20px; }
    .logo-img { width: 100%; max-width: 320px; height: auto; filter: drop-shadow(0 0 15px rgba(0,212,255,0.6)); }

    /* NGĂN KÉO (DRAWER) */
    #myDrawer {
        height: 100%; width: 0; position: fixed; z-index: 1000000;
        top: 0; left: 0; background-color: rgba(13, 27, 42, 0.98);
        overflow-x: hidden; transition: 0.5s; padding-top: 60px;
        border-right: 2px solid #00d4ff; box-shadow: 15px 0 30px rgba(0,0,0,0.7);
    }

    /* TABLE MOBILE: CHO PHÉP CUỘN NGANG */
    .table-wrapper { 
        background: rgba(13, 27, 42, 0.6); 
        border: 1px solid #1e3a5a; 
        border-radius: 12px; 
        padding: 10px; 
        margin-top: 20px; 
        overflow-x: auto; /* Quan trọng để không vỡ bảng trên điện thoại */
    }
    .elite-table { width: 100%; min-width: 600px; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
    
    .elite-table thead th { 
        background: rgba(0, 212, 255, 0.1); color: #00d4ff; 
        text-align: center !important; 
        padding: 10px; font-size: 13px; border-bottom: 3px solid #00d4ff; 
    }
    
    .elite-table td { padding: 8px; font-size: 13px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; }
    .rank-badge { 
        background: linear-gradient(135deg, #ffd700, #b8860b); color: #000; 
        padding: 2px 6px; border-radius: 4px; font-weight: 900; font-size: 11px;
    }

    /* TỐI ƯU CÁC NÚT TRÊN MOBILE */
    button { width: 100% !important; }

    /* CSS CHO PROFILE CARD - SỬ DỤNG MEDIA QUERIES ĐỂ TỰ THAY ĐỔI THEO MÀN HÌNH */
    @media only screen and (max-width: 600px) {
        .kpi-circles { flex-direction: column !important; gap: 20px !important; }
        .stats-grid { flex-wrap: wrap !important; }
        .stat-box { flex: 1 1 40% !important; margin-bottom: 10px; }
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
    st.markdown('<div class="logo-container"><img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true" class="logo-img"></div>', unsafe_allow_html=True)
    
    if menu in t["menu"][:2]:
        sel = st.selectbox("", sorted(df['Tên_2'].dropna().unique()), index=None, placeholder=t["search"], label_visibility="collapsed")
        
        if sel:
            d = df[df['Tên_2'] == sel].iloc[0]
            # PROFILE CARD ĐÃ ĐƯỢC FIX RESPONSIVE (DÙNG FLEX-WRAP)
            html_card = f"""
            <div style="position: relative; width: 100%; max-width: 800px; margin: 60px auto 20px; font-family: 'Segoe UI', sans-serif;">
                <div style="position: absolute; top: -50px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 10px 20px; z-index: 10; text-align: center; width: 80%; max-width: 300px; box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);">
                    <div style="color: #00d4ff; font-size: 10px; font-weight: 900; letter-spacing: 2px;">MEMBER PROFILE</div>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 5px;">
                        <img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true" style="width: 30px;">
                        <div style="color: #ffffff; font-size: 18px; font-weight: bold;">{sel}</div>
                    </div>
                </div>

                <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 60px 15px 20px 15px;">
                    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-bottom: 20px;">
                        <div style="background: #233549; border-radius: 8px; padding: 10px; flex: 1 1 100px; text-align: center; border-bottom: 3px solid #ffd700;">
                            <div style="font-size: 10px; color: #8b949e;">{t['rank']}</div>
                            <div style="font-size: 16px; font-weight: 900; color: #ffd700;">#{int(d['Rank'])}</div>
                        </div>
                        <div style="background: #233549; border-radius: 8px; padding: 10px; flex: 1 1 140px; text-align: center; border-bottom: 3px solid #00d4ff;">
                            <div style="font-size: 10px; color: #8b949e;">{t['pow']}</div>
                            <div style="font-size: 16px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                        </div>
                        <div style="background: #233549; border-radius: 8px; padding: 10px; flex: 1 1 140px; text-align: center; border-bottom: 3px solid #00ffcc;">
                            <div style="font-size: 10px; color: #8b949e;">{t['kill']}</div>
                            <div style="font-size: 16px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                        </div>
                    </div>

                    <div style="background: rgba(26, 42, 58, 0.5); border-radius: 15px; padding: 15px; display: flex; flex-wrap: wrap; justify-content: space-around; align-items: center; gap: 15px;">
                        <div style="text-align: center; flex: 1 1 80px;">
                            <svg width="60" height="60" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#00ffff; font-size: 14px; font-weight:bold;">{d['KPI_K']}%</div>
                            <div style="font-size:8px; color:#00ffff;">KILL KPI</div>
                        </div>
                        <div style="text-align: center; flex: 1 1 100px;">
                            <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ffd700; font-size: 20px; font-weight:bold;">{d['KPI_T']}%</div>
                            <div style="font-size:10px; color:#ffd700;">TOTAL</div>
                        </div>
                        <div style="text-align: center; flex: 1 1 80px;">
                            <svg width="60" height="60" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ff4b4b; font-size: 14px; font-weight:bold;">{d['KPI_D']}%</div>
                            <div style="font-size:8px; color:#ff4b4b;">DEAD KPI</div>
                        </div>
                    </div>
                </div>
            </div>
            """
            components.html(html_card, height=450)

        # --- BẢNG TABLE ---
        df_sorted = df.sort_values(by='Rank')
        rows_list = []
        for _, r in df_sorted.iterrows():
            rows_list.append(f"""
            <tr>
                <td><span class="rank-badge">#{int(r['Rank'])}</span></td>
                <td><b style="color:#fff">{r['Tên_2']}</b></td>
                <td style="text-align:right">{int(r['Sức Mạnh_2']):,}</td>
                <td style="text-align:right; color:#00ffcc">{int(r['Tổng Tiêu Diệt_2']):,}</td>
                <td style="text-align:right; color:#ff4b4b">{int(r['Điểm Chết_2']):,}</td>
                <td style="text-align:right; color:#00d4ff">+{int(r['KI']):,}</td>
                <td style="text-align:right; color:#ff4b4b">+{int(r['DI']):,}</td>
                <td style="text-align:center"><span style="color:#ffd700; font-weight:bold">{r['KPI_T']}%</span></td>
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

    st.markdown(f'<div style="position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #8b949e; padding: 5px; text-align: center; border-top: 1px solid #1a2a3a; z-index:999; font-size:10px;">🛡️ Admin Louis | v10.9</div>', unsafe_allow_html=True)
