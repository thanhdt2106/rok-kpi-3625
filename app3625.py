import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# Link các ảnh
LOGO_MAIN = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true"
LOGO_PROFILE = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true"

# --- 2. SIÊU CSS (Tăng cỡ chử và fix layout) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .block-container { padding-top: 0.5rem !important; max-width: 98% !important; }
    header { visibility: hidden; height: 0px !important; }

    /* Logo & Slogan */
    .logo-container { display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 10px; margin-bottom: 20px; }
    .logo-img { width: 280px; filter: drop-shadow(0px 0px 10px rgba(0, 212, 255, 0.4)); }
    .slogan { color: #00d4ff; font-size: 18px; font-weight: bold; margin-top: 8px; text-transform: uppercase; letter-spacing: 1px; }

    /* BẢNG ELITE - FIX CHỬ TO & ĐẸP */
    .table-wrapper {
        background: rgba(13, 27, 42, 0.6);
        border: 1px solid #1e3a5a;
        border-radius: 12px;
        padding: 20px;
        margin-top: 30px;
    }
    .elite-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Segoe UI', sans-serif;
    }
    .elite-table thead th {
        background: rgba(0, 212, 255, 0.1);
        color: #00d4ff;
        text-align: left;
        padding: 18px 15px;
        font-size: 15px; /* Tăng cỡ chử tiêu đề */
        border-bottom: 3px solid #00d4ff;
    }
    .elite-table tbody tr {
        border-bottom: 1px solid #1a2a3a;
    }
    .elite-table tbody tr:hover {
        background: rgba(0, 212, 255, 0.1) !important;
    }
    .elite-table td {
        padding: 16px 15px;
        font-size: 16px; /* Tăng cỡ chử nội dung */
        color: #e0e6ed;
    }
    
    .rank-badge { background: #ffd700; color: #000; padding: 4px 10px; border-radius: 6px; font-weight: 900; font-size: 14px; }
    .kpi-bar-container { width: 120px; background: #1a2a3a; height: 10px; border-radius: 5px; display: inline-block; vertical-align: middle; margin-right: 10px; }
    .kpi-bar-fill { height: 100%; border-radius: 5px; background: linear-gradient(90deg, #00d4ff, #00ffcc); }

    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: rgba(5, 10, 14, 0.95); color: #8b949e; padding: 10px; font-size: 13px; text-align: center; border-top: 1px solid #1a2a3a; z-index: 999; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ĐIỀU KHIỂN NGÔN NGỮ ---
col_space, col_lang = st.columns([8, 1])
with col_lang:
    lang = st.radio("", ["VN", "EN"], horizontal=True, label_visibility="collapsed")

# --- 4. DỮ LIỆU ---
texts = {
    "VN": {
        "search": "👤 Tìm kiếm thành viên...", "pow": "SỨC MẠNH", "tk": "TỔNG TIÊU DIỆT", "td": "ĐIỂM CHẾT", "rank": "HẠNG",
        "slogan": "Chào mừng đến trang web quản lý KPI 3625",
        "cols": ['Hạng', 'Thành viên', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill Inc', 'Dead Inc', 'KPI %']
    },
    "EN": {
        "search": "👤 Search member name...", "pow": "POWER", "tk": "TOTAL KILL", "td": "TOTAL DEAD", "rank": "RANK",
        "slogan": "Welcome to the 3625 KPI Management Website",
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
            p = r['Sức Mạnh_2']; gk = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 200e6
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = max(0.0, float(r['KI']) / gk) if gk > 0 else 0.0
            pdv = max(0.0, float(r['DI']) / gd) if gd > 0 else 0.0
            return pd.Series([round(pk * 100, 1), round(pdv * 100, 1), round(((pk + pdv) / 2) * 100, 1)])
            
        df[['KPI_K', 'KPI_D', 'KPI_T']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. GIAO DIỆN ---
if df is not None:
    # Logo & Slogan
    st.markdown(f'<div class="logo-container"><img src="{LOGO_MAIN}" class="logo-img"><div class="slogan">{L["slogan"]}</div></div>', unsafe_allow_html=True)
    
    # Tìm kiếm
    sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder=L['search'], label_visibility="collapsed")

    # --- CARD PROFILE CHI TIẾT (GIỮ NGUYÊN FORM GỐC CỦA LOUIS) ---
    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        html_card = f"""
        <div style="position: relative; width: 100%; margin: 60px auto 30px; font-family: 'Segoe UI', sans-serif;">
            <div style="position: absolute; top: -50px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 15px 50px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; box-shadow: 0 8px 25px rgba(0,0,0,0.8); min-width: 480px;">
                <div style="color: #00d4ff; font-size: 11px; font-weight: 900; letter-spacing: 2px; margin-bottom: 5px;">PROFILE MEMBER</div>
                <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
                    <img src="{LOGO_PROFILE}" style="width: 55px; height: 55px; object-fit: contain;">
                    <div style="color: #ffffff; font-size: 32px; font-weight: bold; text-shadow: 0 0 10px #00d4ff;">{sel}</div>
                </div>
                <div style="font-size: 14px; margin-top: 8px; color: #fff;">
                    <b style="color: #ffd700;">ID:</b> {d['ID']} | <b style="color: #00ffcc;">ALLIANCE:</b> {d['Liên Minh_2']}
                </div>
            </div>
            <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 20px; padding: 100px 30px 30px 30px;">
                <div style="display: flex; justify-content: space-between; gap: 20px; margin-bottom: 30px;">
                    <div style="background: #233549; border-radius: 12px; padding: 20px; flex: 1; text-align: center; border-bottom: 4px solid #00d4ff;">
                        <div style="font-size: 12px; color: #8b949e; font-weight: bold;">{L['pow']}</div>
                        <div style="font-size: 24px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 12px; padding: 20px; flex: 1; text-align: center; border-bottom: 4px solid #00ffcc;">
                        <div style="font-size: 12px; color: #8b949e; font-weight: bold;">{L['tk']}</div>
                        <div style="font-size: 24px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 12px; padding: 20px; flex: 1; text-align: center; border-bottom: 4px solid #ff4b4b;">
                        <div style="font-size: 12px; color: #ff4b4b; font-weight: bold;">{L['td']}</div>
                        <div style="font-size: 24px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                    </div>
                </div>
                <div style="background: #1a2a3a; border-radius: 15px; padding: 30px; display: flex; justify-content: space-around; align-items: center; border-bottom: 5px solid #ffd700;">
                    <div style="text-align: center;">
                        <div style="font-size: 40px; color: #ffd700; font-weight: 900;">{d['KPI_T']}%</div>
                        <div style="font-size: 14px; color: #8b949e; font-weight: bold;">TOTAL KPI PERFORMANCE</div>
                    </div>
                </div>
            </div>
        </div>
        """
        components.html(html_card, height=520)

    # --- BẢNG TRANG CHỦ (TĂNG CỠ CHỬ & FIX LẶP) ---
    df_sorted = df.sort_values(by='KillRank')
    
    # Tạo nội dung hàng - Dùng f-string an toàn
    rows_list = []
    for _, r in df_sorted.iterrows():
        k_val = float(r['KPI_T'])
        k_bar = min(k_val, 100)
        row = f"""
        <tr>
            <td><span class="rank-badge">#{int(r['KillRank'])}</span></td>
            <td><b>{r['Tên_2']}</b><br><small style="color:#8b949e">ID: {r['ID']}</small></td>
            <td style="text-align:right">{int(r['Sức Mạnh_2']):,}</td>
            <td style="text-align:right; color:#00ffcc">{int(r['Tổng Tiêu Diệt_2']):,}</td>
            <td style="text-align:right; color:#ff4b4b">{int(r['Điểm Chết_2']):,}</td>
            <td style="text-align:right; color:#00d4ff">+{int(r['KI']):,}</td>
            <td style="text-align:right; color:#ff4b4b">+{int(r['DI']):,}</td>
            <td>
                <div class="kpi-bar-container"><div class="kpi-bar-fill" style="width:{k_bar}%"></div></div>
                <span style="color:#ffd700; font-weight:bold">{k_val}%</span>
            </td>
        </tr>"""
        rows_list.append(row)

    h = L['cols']
    all_rows = "".join(rows_list)
    
    table_html = f"""
    <div class="table-wrapper">
        <table class="elite-table">
            <thead>
                <tr>
                    <th>{h[0]}</th><th>{h[1]}</th><th style="text-align:right">{h[2]}</th><th style="text-align:right">{h[3]}</th>
                    <th style="text-align:right">{h[4]}</th><th style="text-align:right">{h[5]}</th><th style="text-align:right">{h[6]}</th><th>{h[7]}</th>
                </tr>
            </thead>
            <tbody>
                {all_rows}
            </tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)
    
    st.markdown(f'<div class="footer">🛡️ Discord: <b>louiss.nee</b> | Zalo: <b>0.3.7.3.2.7.4.6.0.0</b></div>', unsafe_allow_html=True)
else:
    st.error("⚠️ Không thể tải dữ liệu.")
