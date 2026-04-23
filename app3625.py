import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="FTD KPI | COMMAND CENTER", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SIÊU CSS & JS (FIX HIỂN THỊ & HIỆU ỨNG) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    .block-container { padding-top: 2rem !important; max-width: 98% !important; }
    
    /* STYLE CHO THANH KÉO (DRAWER) */
    #myDrawer {
        height: 100%; width: 0; position: fixed; z-index: 1000000;
        top: 0; left: 0; background-color: rgba(13, 27, 42, 0.98);
        overflow-x: hidden; transition: 0.5s; padding-top: 60px;
        border-right: 2px solid #00d4ff; box-shadow: 15px 0 30px rgba(0,0,0,0.7);
    }
    #myDrawer a {
        padding: 15px 25px; text-decoration: none; font-size: 15px;
        color: #e0e6ed; display: block; transition: 0.3s;
        border-bottom: 1px solid rgba(0,212,255,0.05);
    }
    #myDrawer .closebtn { position: absolute; top: 10px; right: 25px; font-size: 36px; color: #ff4b4b; }

    /* LOGO CENTER */
    .logo-container { display: flex; justify-content: center; width: 100%; margin-bottom: 20px; }
    .logo-img { width: 320px; filter: drop-shadow(0 0 15px rgba(0,212,255,0.4)); }

    /* TABLE STYLE */
    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 20px; margin-top: 20px; overflow-x: auto; }
    .elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
    .elite-table thead th { 
        background: rgba(0, 212, 255, 0.1); color: #00d4ff; text-align: left; 
        padding: 15px; font-size: 14px; border-bottom: 3px solid #00d4ff; 
    }
    .elite-table td { padding: 12px 15px; font-size: 14px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; }
    .rank-badge { 
        background: linear-gradient(135deg, #ffd700, #b8860b); color: #000; 
        padding: 4px 10px; border-radius: 6px; font-weight: 900; box-shadow: 0 0 10px rgba(255,215,0,0.4);
    }
    .kpi-bar-container { width: 100px; background: #1a2a3a; height: 8px; border-radius: 4px; display: inline-block; margin-right: 8px; }
    .kpi-bar-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #00d4ff, #00ffcc); }
    </style>

    <div id="myDrawer">
      <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
      <div style="color: #00d4ff; font-weight: bold; padding: 0 25px 20px; font-size: 18px; border-bottom: 1px solid #1e3a5a;">🛡️ ADMIN PANEL</div>
      <a>⚠️ Tài khoản thiếu KPI</a>
      <a>🏔️ Top 15 Đèo 4</a>
      <a>🌋 Top 15 Đèo 7</a>
      <a>👑 Top 15 Kingland</a>
    </div>

    <script>
    function openNav() { document.getElementById("myDrawer").style.width = "320px"; }
    function closeNav() { document.getElementById("myDrawer").style.width = "0"; }
    </script>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="color: #00d4ff; font-weight: bold; font-size: 18px; text-align: center; margin-bottom: 20px;">🛡️ COMMAND CENTER</div>', unsafe_allow_html=True)
    components.html("""
        <button onclick="parent.openNav()" style="width: 100%; background: #1a2a3a; color: #00d4ff; border: 1px solid #00d4ff; padding: 10px; border-radius: 5px; cursor: pointer; font-weight: bold; font-family: sans-serif;">
            ⚙️ CÀI ĐẶT HỆ THỐNG
        </button>
    """, height=50)
    st.divider()
    lang = st.radio("Ngôn ngữ", ["VN", "EN"], horizontal=True)
    menu = st.radio("Menu", ["📊 Bảng KPI", "👤 Tài khoản", "⚙️ Quản lý KPI"])
    st.info("Phiên bản v10.9 - Admin Louis")

# --- 4. DATA LOGIC (FIX LỖI MẤT DATA) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T)
        ds = pd.read_csv(URL_S)
        dt.columns = dt.columns.str.strip()
        ds.columns = ds.columns.str.strip()
        
        # Merge dữ liệu
        df = pd.merge(dt, ds, on='ID', suffixes=('_1', '_2'))
        
        # Ép kiểu dữ liệu
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
        # Tính KPI mục tiêu
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
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu: {e}")
        return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    st.markdown('<div class="logo-container"><img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true" class="logo-img"></div>', unsafe_allow_html=True)
    
    if menu == "📊 Bảng KPI":
        # Tìm kiếm
        sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder="👤 Tìm kiếm thành viên...", label_visibility="collapsed")
        
        if sel:
            d = df[df['Tên_2'] == sel].iloc[0]
            # PROFILE CARD (KHÔI PHỤC TOÀN BỘ HIỆU ỨNG)
            card_html = f"""
            <div style="position: relative; width: 100%; margin: 60px auto 20px; font-family: 'Segoe UI', sans-serif;">
                <div style="position: absolute; top: -50px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 12px 50px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; box-shadow: 0 0 25px rgba(0, 212, 255, 0.6); min-width: 400px;">
                    <div style="color: #00d4ff; font-size: 13px; font-weight: 900; letter-spacing: 2px; text-shadow: 0 0 5px #00d4ff;">PROFILE MEMBER</div>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-top:5px;">
                        <img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true" style="width: 45px;">
                        <div style="color: #ffffff; font-size: 28px; font-weight: bold; text-shadow: 0 0 15px rgba(255,255,255,0.7);">{sel}</div>
                    </div>
                    <div style="font-size: 13px; color: #ffffff; margin-top: 5px; font-weight: 600; text-shadow: 0 0 5px rgba(0, 212, 255, 0.5);">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                </div>
                <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 85px 25px 30px 25px; box-shadow: inset 0 0 50px rgba(0, 212, 255, 0.1); position: relative;">
                    <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 25px;">
                        <div style="background: #233549; border-radius: 10px; padding: 12px; flex: 1; text-align: center; border-bottom: 3px solid #00d4ff;">
                            <div style="font-size: 10px; color: #8b949e;">SỨC MẠNH</div>
                            <div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                        </div>
                        <div style="background: #233549; border-radius: 10px; padding: 12px; flex: 1; text-align: center; border-bottom: 3px solid #00ffcc;">
                            <div style="font-size: 10px; color: #8b949e;">TỔNG TIÊU DIỆT</div>
                            <div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                        </div>
                        <div style="background: #233549; border-radius: 10px; padding: 12px; flex: 1; text-align: center; border-bottom: 3px solid #ff4b4b;">
                            <div style="font-size: 10px; color: #ff4b4b;">ĐIỂM CHẾT</div>
                            <div style="font-size: 20px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                        </div>
                    </div>
                    <div style="background: rgba(26, 42, 58, 0.6); border-radius: 15px; padding: 25px 10px; display: flex; justify-content: space-around; align-items: center; border: 1px solid rgba(0, 212, 255, 0.1);">
                        <div style="text-align: center;">
                            <svg width="85" height="85" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#00ffff; font-size: 17px; font-weight:bold; margin-top:8px;">{d['KPI_K']}%</div>
                            <div style="font-size:10px; color:#00ffff; font-weight:900; margin-top:3px;">KILL KPI</div>
                        </div>
                        <div style="text-align: center;">
                            <svg width="115" height="115" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ffd700; font-size:24px; font-weight:bold; margin-top:8px;">{d['KPI_T']}%</div>
                            <div style="font-size:12px; color:#ffd700; font-weight:900; margin-top:3px;">TOTAL KPI</div>
                        </div>
                        <div style="text-align: center;">
                            <svg width="85" height="85" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ff4b4b; font-size: 17px; font-weight:bold; margin-top:8px;">{d['KPI_D']}%</div>
                            <div style="font-size:10px; color:#ff4b4b; font-weight:900; margin-top:3px;">DEAD KPI</div>
                        </div>
                    </div>
                    <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 6px; background: linear-gradient(90deg, transparent, #ffd700, transparent); box-shadow: 0 -2px 15px #ffd700;"></div>
                </div>
            </div>
            """
            components.html(card_html, height=560)

        # TABLE
        df_sorted = df.sort_values(by='Rank')
        table_rows = "".join([f"""
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
            </tr>
        """ for _, r in df_sorted.iterrows()])
        
        st.markdown(f"""
        <div class="table-wrapper">
            <table class="elite-table">
                <thead><tr><th>Hạng</th><th>Thành viên</th><th>Sức mạnh</th><th>Tổng Kill</th><th>Điểm Chết</th><th>Kill +</th><th>Dead +</th><th>KPI %</th></tr></thead>
                <tbody>{table_rows}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #8b949e; padding: 10px; text-align: center; border-top: 1px solid #1a2a3a; z-index:999;">🛡️ Admin Louis | v10.9 | Zalo: 0373274600</div>', unsafe_allow_html=True)
