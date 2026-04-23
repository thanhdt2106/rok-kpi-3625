import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. SIÊU CSS (ÉP LOGO KỊCH TRẦN) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    
    /* ÉP SÁT NỘI DUNG LÊN TRÊN CÙNG */
    .main .block-container {
        max-width: 98% !important;
        padding-top: 0rem !important; 
        margin-top: -45px !important; 
    }

    /* LOGO CHÍNH */
    .logo-container { 
        display: flex; justify-content: center; width: 100%; 
        margin-top: 5px !important; margin-bottom: 20px; 
    }
    .logo-img { width: 320px; filter: drop-shadow(0 0 15px rgba(0,212,255,0.6)); }

    /* TABLE STYLE */
    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 20px; margin-top: 15px; }
    .elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
    .elite-table thead th { 
        background: rgba(0, 212, 255, 0.1); color: #00d4ff; 
        text-align: center !important; padding: 15px; font-size: 13px; border-bottom: 3px solid #00d4ff; 
    }
    .elite-table td { padding: 12px 15px; font-size: 14px; border-bottom: 1px solid #1a2a3a; text-align: center; }
    .rank-badge { background: linear-gradient(135deg, #ffd700, #b8860b); color: #000; padding: 4px 10px; border-radius: 6px; font-weight: 900; }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR & LANG ---
with st.sidebar:
    st.markdown('<div style="color: #00d4ff; font-weight: bold; font-size: 20px; text-align: center; margin-bottom: 20px;">🛡️ COMMAND CENTER</div>', unsafe_allow_html=True)
    lang = st.radio("Language", ["VN", "EN"], horizontal=True)
    t = {
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
    }[lang]
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
        cols = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in cols:
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

# --- 5. HIỂN THỊ ---
if df is not None:
    st.markdown('<div class="logo-container"><img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true" class="logo-img"></div>', unsafe_allow_html=True)
    
    if menu in t["menu"][:2]:
        sel = st.selectbox("", sorted(df['Tên_2'].dropna().unique()), index=None, placeholder=t["search"], label_visibility="collapsed")
        
        if sel:
            d = df[df['Tên_2'] == sel].iloc[0]
            # KHÔI PHỤC CARD PROFILE (GỒM ID, LIÊN MINH VÀ VÒNG TRÒN KPI)
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
                        <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; text-align: center; border-bottom: 3px solid #00d4ff;">
                            <div style="font-size: 10px; color: #8b949e;">{t['pow']}</div>
                            <div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                        </div>
                        <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; text-align: center; border-bottom: 3px solid #00ffcc;">
                            <div style="font-size: 10px; color: #8b949e;">{t['kill']}</div>
                            <div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                        </div>
                    </div>

                    <div style="background: rgba(26, 42, 58, 0.5); border-radius: 15px; padding: 25px 5px; display: flex; justify-content: space-around; align-items: center; border: 1px solid rgba(0, 212, 255, 0.2);">
                        <div style="text-align: center;">
                            <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#00ffff; font-size: 18px; font-weight:bold;">{d['KPI_K']}%</div>
                            <div style="font-size:10px; color:#00ffff; font-weight:bold;">KILL KPI</div>
                        </div>
                        <div style="text-align: center;">
                            <svg width="110" height="110" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ffd700; font-size:26px; font-weight:bold;">{d['KPI_T']}%</div>
                            <div style="font-size:12px; color:#ffd700; font-weight:bold;">TOTAL KPI</div>
                        </div>
                        <div style="text-align: center;">
                            <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ff4b4b; font-size: 18px; font-weight:bold;">{d['KPI_D']}%</div>
                            <div style="font-size:10px; color:#ff4b4b; font-weight:bold;">DEAD KPI</div>
                        </div>
                    </div>
                </div>
            </div>
            """
            components.html(html_card, height=530)

        # BẢNG DỮ LIỆU
        df_sorted = df.sort_values(by='Rank')
        rows = []
        for _, r in df_sorted.iterrows():
            rows.append(f"<tr><td><span class='rank-badge'>#{int(r['Rank'])}</span></td><td><b>{r['Tên_2']}</b><br><small>ID: {r['ID']}</small></td><td>{int(r['Sức Mạnh_2']):,}</td><td style='color:#00ffcc'>{int(r['Tổng Tiêu Diệt_2']):,}</td><td style='color:#ff4b4b'>{int(r['Điểm Chết_2']):,}</td><td style='color:#00d4ff'>+{int(r['KI']):,}</td><td style='color:#ff4b4b'>+{int(r['DI']):,}</td><td><span style='color:#ffd700; font-weight:bold'>{r['KPI_T']}%</span></td></tr>")
        st.markdown(f'<div class="table-wrapper"><table class="elite-table"><thead><tr>{"".join([f"<th>{h}</th>" for h in t["headers"]])}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>', unsafe_allow_html=True)

    st.markdown(f'<div style="position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #8b949e; padding: 10px; text-align: center; border-top: 1px solid #1a2a3a; z-index:999;">🛡️ Admin Louis | v10.9</div>', unsafe_allow_html=True)
