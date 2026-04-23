import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide", initial_sidebar_state="expanded")

# Link các ảnh
LOGO_MAIN = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true"
LOGO_PROFILE = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true"

# --- 2. SIÊU CSS (FIX LOGO CAO & SIDEBAR) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .block-container { padding-top: 0rem !important; max-width: 98% !important; }
    header { visibility: hidden; height: 0px !important; }

    /* Logo cao nhất */
    .logo-container { 
        display: flex; 
        justify-content: center; 
        margin-top: -20px; 
        margin-bottom: 10px; 
    }
    .logo-img { width: 280px; filter: drop-shadow(0px 0px 10px rgba(0, 212, 255, 0.4)); }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    
    /* Bảng dữ liệu */
    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 20px; }
    .elite-table { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
    .elite-table thead th { 
        background: rgba(0, 212, 255, 0.1); color: #00d4ff; text-align: left; 
        padding: 15px; font-size: 16px; border-bottom: 3px solid #00d4ff; 
    }
    .elite-table td { padding: 14px 15px; font-size: 16px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; }
    .rank-badge { background: #ffd700; color: #000; padding: 4px 10px; border-radius: 6px; font-weight: 900; font-size: 14px; }
    .kpi-bar-container { width: 100px; background: #1a2a3a; height: 8px; border-radius: 4px; display: inline-block; vertical-align: middle; margin-right: 10px; }
    .kpi-bar-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #00d4ff, #00ffcc); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: rgba(5, 10, 14, 0.95); color: #8b949e; padding: 10px; font-size: 13px; text-align: center; border-top: 1px solid #1a2a3a; z-index: 999; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (CHỨA EN/VN & SETTING) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff; text-align:center;'>SETTINGS</h2>", unsafe_allow_html=True)
    lang = st.radio("NGÔN NGỮ / LANGUAGE", ["VN", "EN"], horizontal=True)
    st.divider()
    menu = st.radio("MENU", ["📊 Bảng KPI", "👤 Tài khoản", "⚙️ Quản lý"])
    st.divider()
    st.write("Admin: Louis")

# --- 4. DỮ LIỆU ---
texts = {
    "VN": {
        "search": "👤 Tìm kiếm thành viên...", "pow": "SỨC MẠNH", "tk": "TỔNG TIÊU DIỆT", "td": "ĐIỂM CHẾT", "rank": "HẠNG",
        "cols": ['Hạng', 'Thành viên', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']
    },
    "EN": {
        "search": "👤 Search member name...", "pow": "POWER", "tk": "TOTAL KILL", "td": "TOTAL DEAD", "rank": "RANK",
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
        # Đọc dữ liệu từ Google Sheets
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        
        # Tiền xử lý ID và Tên
        for d in [dt, ds]:
            d['ID'] = d['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
            d['Tên'] = d['Tên'].fillna('Unknown').astype(str).str.strip()
        
        # Gộp dữ liệu
        df_merge = pd.merge(dt.drop_duplicates('ID'), ds.drop_duplicates('ID'), on='ID', suffixes=('_1', '_2'))
        
        # Chuyển đổi số liệu
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df_merge[c] = pd.to_numeric(df_merge[c].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        df_merge['KI'] = df_merge['Tổng Tiêu Diệt_2'] - df_merge['Tổng Tiêu Diệt_1']
        df_merge['DI'] = df_merge['Điểm Chết_2'] - df_merge['Điểm Chết_1']
        df_merge['KillRank'] = df_merge['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)
        
        def calc_kpi(r):
            p = r['Sức Mạnh_2']
            gk = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 200e6
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = max(0.0, float(r['KI']) / gk) if gk > 0 else 0.0
            pdv = max(0.0, float(r['DI']) / gd) if gd > 0 else 0.0
            return pd.Series([round(pk * 100, 1), round(pdv * 100, 1), round(((pk + pdv) / 2) * 100, 1)])
            
        df_merge[['KPI_K', 'KPI_D', 'KPI_T']] = df_merge.apply(calc_kpi, axis=1)
        return df_merge
    except Exception as e:
        return None

# Gọi hàm load dữ liệu
df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    # Logo
    st.markdown(f'<div class="logo-container"><img src="{LOGO_MAIN}" class="logo-img"></div>', unsafe_allow_html=True)

    if menu == "📊 Bảng KPI":
        sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder=L['search'], label_visibility="collapsed")
        
        if sel:
            d = df[df['Tên_2'] == sel].iloc[0]
            # Hiển thị Card Profile (Giữ nguyên giao diện đẹp của Louis)
            html_card = f"""
            <div style="position: relative; width: 100%; margin: 60px auto 10px; font-family: 'Segoe UI', sans-serif;">
                <div style="position: absolute; top: -50px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 12px 40px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; box-shadow: 0 8px 25px rgba(0,0,0,0.8); min-width: 450px;">
                    <div style="color: #00d4ff; font-size: 11px; font-weight: 900; letter-spacing: 2px; margin-bottom: 5px;">PROFILE MEMBER</div>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
                        <img src="{LOGO_PROFILE}" style="width: 50px; height: 50px; object-fit: contain;">
                        <div style="color: #ffffff; font-size: 28px; font-weight: bold;">{sel}</div>
                    </div>
                    <div style="font-size: 13px; margin-top: 8px; color: #fff;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                </div>
                <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 85px 20px 20px 20px;">
                    <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 25px;">
                        <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3.5px solid #00d4ff;">
                            <div style="font-size: 10px; color: #8b949e; font-weight: bold;">{L['pow']}</div>
                            <div style="font-size: 22px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                        </div>
                        <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3.5px solid #00ffcc;">
                            <div style="font-size: 10px; color: #8b949e; font-weight: bold;">{L['tk']}</div>
                            <div style="font-size: 22px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                        </div>
                        <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3.5px solid #ff4b4b;">
                            <div style="font-size: 10px; color: #ff4b4b; font-weight: bold;">{L['td']}</div>
                            <div style="font-size: 22px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                        </div>
                    </div>
                    <div style="background: #1a2a3a; border-radius: 15px; padding: 30px; border-bottom: 5px solid #ffd700; display: flex; justify-content: space-around; align-items: center;">
                        <div style="text-align: center;">
                            <div style="position: relative; width: 90px; height: 90px; margin: 0 auto;">
                                <svg viewBox="0 0 36 36" style="width: 90px; height: 90px; transform: rotate(-90deg);">
                                    <circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="4"></circle>
                                    <circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3.5" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round"></circle>
                                </svg>
                                <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:16px; font-weight:bold; color: #00ffff;">{d['KPI_K']}%</div>
                            </div>
                            <div style="font-size: 11px; color: #00ffff; font-weight: bold; margin-top: 10px;">KPI KILL</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="position: relative; width: 130px; height: 130px; margin: 0 auto;">
                                <svg viewBox="0 0 36 36" style="width: 130px; height: 130px; transform: rotate(-90deg);">
                                    <circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="4"></circle>
                                    <circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="4" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round"></circle>
                                </svg>
                                <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:24px; font-weight:900; color:#ffd700;">{d['KPI_T']}%</div>
                            </div>
                            <div style="font-size: 15px; color: #ffd700; font-weight: bold; margin-top: 10px;">TOTAL KPI</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="position: relative; width: 90px; height: 90px; margin: 0 auto;">
                                <svg viewBox="0 0 36 36" style="width: 90px; height: 90px; transform: rotate(-90deg);">
                                    <circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="4"></circle>
                                    <circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3.5" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round"></circle>
                                </svg>
                                <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:16px; font-weight:bold; color: #ff4b4b;">{d['KPI_D']}%</div>
                            </div>
                            <div style="font-size: 11px; color: #ff4b4b; font-weight: bold; margin-top: 10px;">KPI DEAD</div>
                        </div>
                    </div>
                </div>
            </div>
            """
            components.html(html_card, height=580)

        # Bảng dữ liệu
        df_sorted = df.sort_values(by='KillRank')
        rows = []
        for _, r in df_sorted.iterrows():
            rows.append(f"""
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
                <tbody>{"".join(rows)}</tbody>
            </table>
        </div>
        """
        st.markdown(table_html, unsafe_allow_html=True)

    elif menu == "👤 Tài khoản":
        st.subheader("Thông tin tài khoản")
        st.write("Chức năng đang phát triển...")

    elif menu == "⚙️ Quản lý":
        st.subheader("Quản lý hệ thống")
        st.write("Dành cho Admin Louis")

    st.markdown(f'<div class="footer">🛡️ Discord: louiss.nee | Zalo: 0.3.7.3.2.7.4.6.0.0</div>', unsafe_allow_html=True)
else:
    st.error("⚠️ Lỗi tải dữ liệu. Hãy kiểm tra lại quyền chia sẻ của Google Sheets.")
