import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="FTD KPI | COMMAND CENTER", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SIÊU CSS & JAVASCRIPT (THANH KÉO TRƯỢT & STYLE GỐC) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    .block-container { padding-top: 0rem !important; max-width: 98% !important; }
    header { visibility: hidden; }

    /* STYLE CHO THANH KÉO (DRAWER) */
    #myDrawer {
        height: 100%; width: 0; position: fixed; z-index: 999999;
        top: 0; left: 0; background-color: rgba(13, 27, 42, 0.98);
        overflow-x: hidden; transition: 0.5s; padding-top: 60px;
        border-right: 2px solid #00d4ff; box-shadow: 15px 0 30px rgba(0,0,0,0.7);
    }
    #myDrawer a {
        padding: 15px 25px; text-decoration: none; font-size: 15px;
        color: #e0e6ed; display: block; transition: 0.3s;
        border-bottom: 1px solid rgba(0,212,255,0.05); font-family: 'Segoe UI';
    }
    #myDrawer .closebtn { position: absolute; top: 10px; right: 25px; font-size: 36px; color: #ff4b4b; }
    .drawer-title { color: #00d4ff; font-weight: bold; padding: 0 25px 20px; font-size: 18px; border-bottom: 1px solid #1e3a5a; }

    /* STYLE BẢNG DỮ LIỆU GỐC */
    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 20px; margin-top: 20px; }
    .elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
    .elite-table thead th { 
        background: rgba(0, 212, 255, 0.1); color: #00d4ff; text-align: left; 
        padding: 15px; font-size: 15px; border-bottom: 3px solid #00d4ff; 
    }
    .elite-table td { padding: 12px 15px; font-size: 15px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; }
    .rank-badge { background: #ffd700; color: #000; padding: 3px 8px; border-radius: 4px; font-weight: 900; }
    .kpi-bar-container { width: 100px; background: #1a2a3a; height: 8px; border-radius: 4px; display: inline-block; vertical-align: middle; margin-right: 10px; }
    .kpi-bar-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #00d4ff, #00ffcc); }
    </style>

    <div id="myDrawer">
      <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
      <div class="drawer-title">📋 THÔNG TIN NHANH</div>
      <a>⚠️ Tài khoản thiếu KPI</a>
      <a>🏔️ Top 15 Đèo 4</a>
      <a>🌋 Top 15 Đèo 7</a>
      <a>👑 Top 15 Kingland</a>
      <a>📅 Dữ liệu: KV7 - 2026</a>
    </div>

    <script>
    function openNav() { document.getElementById("myDrawer").style.width = "320px"; }
    function closeNav() { document.getElementById("myDrawer").style.width = "0"; }
    </script>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (KHÔNG RELOAD - GIỮ NGUYÊN EN/VN) ---
with st.sidebar:
    st.markdown('<div style="color: #00d4ff; font-weight: bold; font-size: 18px; text-align: center; margin-bottom: 20px;">🛡️ COMMAND CENTER</div>', unsafe_allow_html=True)
    
    # Nút mở Drawer bằng JS
    components.html("""
        <button onclick="parent.openNav()" style="width: 100%; background: #1a2a3a; color: #00d4ff; border: 1px solid #00d4ff; padding: 10px; border-radius: 5px; cursor: pointer; font-weight: bold; font-family: sans-serif;">
            ⚙️ CÀI ĐẶT HỆ THỐNG
        </button>
    """, height=50)

    st.divider()
    st.write("**NGÔN NGỮ / LANGUAGE**")
    lang = st.radio("Lang", ["VN", "EN"], horizontal=True, label_visibility="collapsed")
    
    st.divider()
    st.write("**MENU**")
    menu = st.radio("Menu", ["📊 Bảng KPI", "👤 Tài khoản", "⚙️ Quản lý KPI"], label_visibility="collapsed")
    
    st.divider()
    st.info("Phiên bản v10.9 - Admin Louis")

# --- 4. DATA LOGIC (KHÔI PHỤC TOÀN BỘ) ---
texts = {
    "VN": {
        "search": "👤 Tìm kiếm thành viên...", "pow": "SỨC MẠNH", "tk": "TỔNG TIÊU DIỆT", "td": "ĐIỂM CHẾT",
        "cols": ['Hạng', 'Thành viên', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']
    },
    "EN": {
        "search": "👤 Search member name...", "pow": "POWER", "tk": "TOTAL KILL", "td": "TOTAL DEAD",
        "cols": ['Rank', 'Member', 'Power', 'Total Kill', 'Total Dead', 'Kill Inc', 'Dead Inc', 'KPI %']
    }
}
L = texts[lang]

SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        for d in [dt, ds]:
            d['ID'] = d['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
            d['Tên'] = d['Tên'].fillna('Unknown').astype(str).str.strip()
        df = pd.merge(dt.drop_duplicates('ID'), ds.drop_duplicates('ID'), on='ID', suffixes=('_1', '_2'))
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        df['KillRank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)
        
        def get_metrics(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 200e6
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = max(0.0, float(r['KI']) / gk) if gk > 0 else 0.0
            pdv = max(0.0, float(r['DI']) / gd) if gd > 0 else 0.0
            return pd.Series([round(pk * 100, 1), round(pdv * 100, 1), round(((pk + pdv) / 2) * 100, 1)])
        df[['KPI_K', 'KPI_D', 'KPI_T']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ CHÍNH ---
if df is not None:
    if menu == "📊 Bảng KPI":
        st.markdown(f'<div style="text-align:center; margin-top:-20px;"><img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true" width="280"></div>', unsafe_allow_html=True)
        
        sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder=L['search'], label_visibility="collapsed")
        
        # KHÔI PHỤC PROFILE CARD (SVG)
        if sel:
            d = df[df['Tên_2'] == sel].iloc[0]
            html_card = f"""
            <div style="position: relative; width: 100%; margin: 60px auto 10px; font-family: 'Segoe UI', sans-serif;">
                <div style="position: absolute; top: -50px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 12px 40px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; box-shadow: 0 8px 25px rgba(0,0,0,0.8); min-width: 420px;">
                    <div style="color: #00d4ff; font-size: 11px; font-weight: 900; letter-spacing: 2px;">PROFILE MEMBER</div>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-top:5px;">
                        <img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true" style="width: 45px;">
                        <div style="color: #ffffff; font-size: 26px; font-weight: bold;">{sel}</div>
                    </div>
                    <div style="font-size: 12px; color: #8b949e; margin-top: 5px;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                </div>
                <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 80px 20px 20px 20px;">
                    <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 20px;">
                        <div style="background: #233549; border-radius: 10px; padding: 12px; flex: 1; text-align: center; border-bottom: 3px solid #00d4ff;">
                            <div style="font-size: 10px; color: #8b949e;">{L['pow']}</div>
                            <div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                        </div>
                        <div style="background: #233549; border-radius: 10px; padding: 12px; flex: 1; text-align: center; border-bottom: 3px solid #00ffcc;">
                            <div style="font-size: 10px; color: #8b949e;">{L['tk']}</div>
                            <div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                        </div>
                        <div style="background: #233549; border-radius: 10px; padding: 12px; flex: 1; text-align: center; border-bottom: 3px solid #ff4b4b;">
                            <div style="font-size: 10px; color: #ff4b4b;">{L['td']}</div>
                            <div style="font-size: 20px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                        </div>
                    </div>
                    <div style="background: #1a2a3a; border-radius: 15px; padding: 25px; border-bottom: 5px solid #ffd700; display: flex; justify-content: space-around; align-items: center;">
                        <div style="text-align: center;">
                            <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#00ffff; font-weight:bold; margin-top:5px;">{d['KPI_K']}%</div><div style="font-size:9px; color:#8b949e;">KILL KPI</div>
                        </div>
                        <div style="text-align: center;">
                            <svg width="110" height="110" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ffd700; font-size:22px; font-weight:bold; margin-top:5px;">{d['KPI_T']}%</div><div style="font-size:12px; color:#ffd700; font-weight:bold;">TOTAL KPI</div>
                        </div>
                        <div style="text-align: center;">
                            <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ff4b4b; font-weight:bold; margin-top:5px;">{d['KPI_D']}%</div><div style="font-size:9px; color:#8b949e;">DEAD KPI</div>
                        </div>
                    </div>
                </div>
            </div>
            """
            components.html(html_card, height=520)

        # KHÔI PHỤC BẢNG DỮ LIỆU CHUẨN
        df_sorted = df.sort_values(by='KillRank')
        rows_list = []
        for _, r in df_sorted.iterrows():
            rows_list.append(f"""
            <tr>
                <td><span class="rank-badge">#{int(r['KillRank'])}</span></td>
                <td><b>{r['Tên_2']}</b><br><small style="color:#8b949e">ID: {r['ID']}</small></td>
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

        h = L['cols']
        table_html = f"""
        <div class="table-wrapper">
            <table class="elite-table">
                <thead><tr><th>{h[0]}</th><th>{h[1]}</th><th style="text-align:right">{h[2]}</th><th style="text-align:right">{h[3]}</th><th style="text-align:right">{h[4]}</th><th style="text-align:right">{h[5]}</th><th style="text-align:right">{h[6]}</th><th>{h[7]}</th></tr></thead>
                <tbody>{"".join(rows_list)}</tbody>
            </table>
        </div>
        """
        st.markdown(table_html, unsafe_allow_html=True)

    st.markdown('<div style="position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #8b949e; padding: 10px; text-align: center; border-top: 1px solid #1a2a3a; z-index:999;">🛡️ Admin Louis | v10.9 | Zalo: 0373274600</div>', unsafe_allow_html=True)
else:
    st.error("Không thể kết nối dữ liệu Google Sheets. Louis hãy kiểm tra link CSV nhé!")
