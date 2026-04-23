import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG (Rộng toàn màn hình) ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS TỔNG THỂ (Tối ưu hóa không gian) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    
    /* Làm gọn thanh tìm kiếm */
    .stSelectbox { width: 100% !important; }
    
    /* Loại bỏ padding dư thừa của Streamlit để rộng hơn */
    .block-container { padding-top: 2rem; padding-bottom: 0rem; padding-left: 2rem; padding-right: 2rem; }
    
    /* Style cho bảng */
    [data-testid="stDataFrame"] { background: #1a2a3a; border-radius: 10px; border: 1px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. QUẢN LÝ NGÔN NGỮ ---
# Đẩy ngôn ngữ và tìm kiếm sang trái
col_search, col_header, col_lang = st.columns([1.5, 4, 1])

with col_lang:
    lang = st.radio("LANG:", ["VN", "EN"], horizontal=True, label_visibility="collapsed")

texts = {
    "VN": {
        "header": "🛡️ HỆ THỐNG QUẢN TRỊ 3625", "search": "🔍 TÌM THÀNH VIÊN:",
        "select": "--- Chọn tên ---", "pow": "SỨC MẠNH", "tk": "TỔNG TIÊU DIỆT", 
        "td": "ĐIỂM CHẾT", "rank": "HẠNG", "target": "Mục tiêu",
        "cols": ['Tên', 'ID', 'Liên minh', 'Hạng', 'Sức mạnh', 'Tổng Kill', 'Điểm Chết', 'Kill +', 'Dead +', 'KPI %']
    },
    "EN": {
        "header": "🛡️ COMMAND CENTER 3625", "search": "🔍 SEARCH MEMBER:",
        "select": "--- Select name ---", "pow": "POWER", "tk": "TOTAL KILL", 
        "td": "TOTAL DEAD", "rank": "RANK", "target": "Target",
        "cols": ['Name', 'ID', 'Alliance', 'Rank', 'Power', 'Total Kill', 'Total Dead', 'Kill Inc', 'Dead Inc', 'KPI %']
    }
}
L = texts[lang]

# --- 4. TẢI DỮ LIỆU ---
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
            return pd.Series([round(pk * 100, 1), round(pdv * 100, 1), round(((pk + pdv) / 2) * 100, 1), f"{gk/1e6:,.0f}M", f"{gd/1e3:,.0f}K"])
            
        df[['KPI_K', 'KPI_D', 'KPI_T', 'T_K', 'T_D']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ GIAO DIỆN ---
if df is not None:
    # Header chính giữa
    with col_header:
        st.markdown(f"<h2 style='text-align:center; color:#00d4ff; font-weight:bold; margin-top:-10px;'>{L['header']}</h2>", unsafe_allow_html=True)
    
    # Thanh tìm kiếm bên trái
    with col_search:
        sel = st.selectbox(L["search"], [L["select"]] + sorted(df['Tên_2'].unique()))

    if sel != L["select"]:
        d = df[df['Tên_2'] == sel].iloc[0]
        
        html_card = f"""
        <div style="position: relative; width: 100%; margin: 60px auto 20px; font-family: 'Segoe UI', sans-serif;">
            
            <div style="position: absolute; top: -40px; left: 50%; transform: translateX(-50%); 
                        background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; 
                        padding: 12px 60px; z-index: 10; text-align: center;
                        border-bottom: 4px solid #ffd700; box-shadow: 0 8px 15px rgba(0,0,0,0.5);">
                <div style="color: #00d4ff; font-size: 14px; font-weight: 900; letter-spacing: 2px;">PROFILE MEMBER</div>
                <div style="color: #ffffff; font-size: 28px; font-weight: bold; margin: 2px 0;">{sel}</div>
                <div style="color: #8b949e; font-size: 11px;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
            </div>

            <div style="background: rgba(13, 25, 47, 0.95); border: 2px solid #00d4ff; border-radius: 15px; padding: 70px 20px 20px 20px; box-shadow: inset 0 0 20px rgba(0,212,255,0.2);">
                <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 30px;">
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3px solid #ffd700; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">
                        <div style="font-size: 10px; color: #8b949e; font-weight: bold;">{L['pow']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3px solid #ffd700; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">
                        <div style="font-size: 10px; color: #8b949e; font-weight: bold;">{L['tk']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3px solid #ffd700; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">
                        <div style="font-size: 10px; color: #ff4b4b; font-weight: bold;">{L['td']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 0.6; text-align: center; border-bottom: 3px solid #ffd700; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">
                        <div style="font-size: 10px; color: #ffd700; font-weight: bold;">{L['rank']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #ffd700;">#{d['KillRank']}</div>
                    </div>
                </div>

                <div style="background: #1a2a3a; border-radius: 15px; padding: 30px; border-bottom: 5px solid #ffd700; box-shadow: 0 10px 20px rgba(0,0,0,0.6); display: flex; justify-content: space-around; align-items: center;">
                    <div style="text-align: center;">
                        <div style="position: relative; width: 90px; height: 90px; margin: 0 auto; background: #121e2a; border-radius: 50%;">
                            <svg viewBox="0 0 36 36" style="width: 90px; height: 90px; transform: rotate(-90deg);">
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="4"></circle>
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3.5" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round"></circle>
                            </svg>
                            <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:16px; font-weight:bold;">{d['KPI_K']}%</div>
                        </div>
                        <div style="font-size: 11px; color: #00ffff; font-weight: bold; margin-top: 10px;">KPI KILL</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="position: relative; width: 130px; height: 130px; margin: 0 auto; background: #121e2a; border-radius: 50%;">
                            <svg viewBox="0 0 36 36" style="width: 130px; height: 130px; transform: rotate(-90deg);">
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="4"></circle>
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="4" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round"></circle>
                            </svg>
                            <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:24px; font-weight:900; color:#ffd700;">{d['KPI_T']}%</div>
                        </div>
                        <div style="font-size: 15px; color: #ffd700; font-weight: bold; margin-top: 10px;">TOTAL KPI</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="position: relative; width: 90px; height: 90px; margin: 0 auto; background: #121e2a; border-radius: 50%;">
                            <svg viewBox="0 0 36 36" style="width: 90px; height: 90px; transform: rotate(-90deg);">
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="4"></circle>
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3.5" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round"></circle>
                            </svg>
                            <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:16px; font-weight:bold;">{d['KPI_D']}%</div>
                        </div>
                        <div style="font-size: 11px; color: #ff4b4b; font-weight: bold; margin-top: 10px;">KPI DEAD</div>
                    </div>
                </div>
            </div>
        </div>
        """
        components.html(html_card, height=580)

    st.divider()
    
    # Bảng danh sách full width
    display_df = df[['Tên_2', 'ID', 'Liên Minh_2', 'KillRank', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'KI', 'DI', 'KPI_T']].copy()
    display_df.columns = L['cols']
    
    # Format
    for col in L['cols'][4:9]:
        display_df[col] = display_df[col].apply(lambda x: f"{int(x):,}")
    display_df[L['cols'][9]] = display_df[L['cols'][9]].apply(lambda x: f"{x}%")

    st.dataframe(display_df.sort_values(by=L['cols'][3]), use_container_width=True, hide_index=True, height=600)
