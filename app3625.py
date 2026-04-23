import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="FTD KPI | COMMAND CENTER", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. SIÊU CSS (FULL ENGLISH & NEW PROGRESS BARS) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"] { display: none !important; width: 0px !important; }
    header { visibility: hidden; }

    .main .block-container {
        max-width: 100% !important;
        padding: 0.5rem 1.5rem !important;
    }

    .stApp { background-color: #050a0e; color: #e0e6ed; }
    
    .header-left-text {
        color: #00d4ff;
        font-weight: 900;
        font-size: 22px;
        text-shadow: 0 0 10px #00d4ff;
        font-family: 'Segoe UI', sans-serif;
    }

    /* TABLE STYLE */
    .table-wrapper { 
        background: rgba(13, 27, 42, 0.6); 
        border: 1px solid #1e3a5a; 
        border-radius: 12px; 
        padding: 15px; 
        margin-top: 10px;
        overflow-x: auto;
    }
    .elite-table { width: 100%; border-collapse: collapse; min-width: 850px;}
    .elite-table thead th { 
        background: rgba(0, 212, 255, 0.1); color: #00d4ff; 
        text-align: center !important; 
        padding: 12px; font-size: 13px; border-bottom: 3px solid #00d4ff; 
    }
    .elite-table td { padding: 10px 15px; font-size: 13px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; }

    /* PROGRESS BAR TRONG PROFILE */
    .progress-container { width: 100%; background: #1a2a3a; height: 12px; border-radius: 6px; margin-top: 5px; position: relative; }
    .progress-fill-kill { height: 100%; border-radius: 6px; background: linear-gradient(90deg, #00d4ff, #00ffcc); }
    .progress-fill-dead { height: 100%; border-radius: 6px; background: linear-gradient(90deg, #ff4b4b, #ff7676); }
    .progress-text { font-size: 11px; color: #fff; display: flex; justify-content: space-between; margin-top: 2px; font-weight: bold; }
    </style>
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

# --- 4. HEADER (TEXT LEFT - SEARCH RIGHT) ---
if df is not None:
    h_col1, h_col2 = st.columns([1, 1])
    with h_col1:
        st.markdown('<div class="header-left-text">FIGHT TO DEAD 3625</div>', unsafe_allow_html=True)
    with h_col2:
        sel = st.selectbox("", sorted(df['Tên_2'].dropna().unique()), index=None, placeholder="🔍 Search member name...", label_visibility="collapsed")

    # --- 5. PROFILE CHI TIẾT ---
    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # Định dạng rút gọn số triệu (M) cho Progress Bar
        cur_k = f"{d['KI']/1e6:.1f}M"
        tar_k = f"{d['T_K']/1e6:.0f}M"
        cur_d = f"{d['DI']/1e3:.1f}K"
        tar_d = f"{d['T_D']/1e3:.0f}K"

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
            
            <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 80px 25px 30px 25px; box-shadow: inset 0 0 30px rgba(0, 212, 255, 0.1);">
                <div style="display: flex; justify-content: space-between; gap: 10px; margin-bottom: 30px; flex-wrap: wrap;">
                    <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1; min-width: 100px; text-align: center; border-bottom: 3px solid #ffd700;">
                        <div style="font-size: 10px; color: #8b949e;">RANK</div>
                        <div style="font-size: 20px; font-weight: 900; color: #ffd700;">#{int(d['Rank'])}</div>
                    </div>
                    <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; min-width: 120px; text-align: center; border-bottom: 3px solid #00d4ff;"><div style="font-size: 10px; color: #8b949e;">POWER</div><div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div></div>
                    <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; min-width: 120px; text-align: center; border-bottom: 3px solid #00ffcc;"><div style="font-size: 10px; color: #8b949e;">TOTAL KILL</div><div style="font-size: 20px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div></div>
                    <div style="background: #233549; border-radius: 8px; padding: 12px; flex: 1.5; min-width: 120px; text-align: center; border-bottom: 3px solid #ff4b4b;"><div style="font-size: 10px; color: #8b949e;">DEAD PT</div><div style="font-size: 20px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div></div>
                </div>

                <div style="background: rgba(26, 42, 58, 0.5); border-radius: 15px; padding: 25px; border: 1px solid rgba(0, 212, 255, 0.2);">
                    <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 25px;">
                        <div style="text-align: center;">
                            <svg width="70" height="70" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#00ffff; font-size: 14px; font-weight:bold; margin-top:5px;">{d['KPI_K']}%</div>
                            <div style="font-size:9px; color:#8b949e;">KILL KPI</div>
                        </div>
                        <div style="text-align: center;">
                            <svg width="100" height="100" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="4" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ffd700; font-size:24px; font-weight:bold;">{d['KPI_T']}%</div>
                            <div style="font-size:11px; color:#ffd700; font-weight:bold;">TOTAL SCORE</div>
                        </div>
                        <div style="text-align: center;">
                            <svg width="70" height="70" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ff4b4b; font-size: 14px; font-weight:bold; margin-top:5px;">{d['KPI_D']}%</div>
                            <div style="font-size:9px; color:#8b949e;">DEAD KPI</div>
                        </div>
                    </div>

                    <div style="max-width: 500px; margin: 0 auto;">
                        <div style="margin-bottom: 15px;">
                            <div class="progress-text"><span>Kill Progress</span><span>{cur_k} / {tar_k}</span></div>
                            <div class="progress-container"><div class="progress-fill-kill" style="width:{min(d['KPI_K'], 100)}%"></div></div>
                        </div>
                        <div>
                            <div class="progress-text"><span>Dead Progress</span><span>{cur_d} / {tar_d}</span></div>
                            <div class="progress-container"><div class="progress-fill-dead" style="width:{min(d['KPI_D'], 100)}%"></div></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        components.html(html_card, height=580)

    # --- 6. BẢNG TABLE (FULL ENGLISH) ---
    df_sorted = df.sort_values(by='Rank')
    headers = ['Rank', 'Member', 'Power', 'Total Kill', 'Dead Pt', 'Kill +', 'Dead +', 'KPI %']
    rows_list = []
    for _, r in df_sorted.iterrows():
        rows_list.append(f"""
        <tr>
            <td><span style="background:linear-gradient(135deg, #ffd700, #b8860b); color:#000; padding:4px 10px; border-radius:6px; font-weight:900;">#{int(r['Rank'])}</span></td>
            <td><b style="color:#fff">{r['Tên_2']}</b><br><small style="color:#8b949e">ID: {r['ID']}</small></td>
            <td style="text-align:right">{int(r['Sức Mạnh_2']):,}</td>
            <td style="text-align:right; color:#00ffcc">{int(r['Tổng Tiêu Diệt_2']):,}</td>
            <td style="text-align:right; color:#ff4b4b">{int(r['Điểm Chết_2']):,}</td>
            <td style="text-align:right; color:#00d4ff">+{int(r['KI']):,}</td>
            <td style="text-align:right; color:#ff4b4b">+{int(r['DI']):,}</td>
            <td>
                <div style="width: 80px; background: #1a2a3a; height: 6px; border-radius: 4px; display: inline-block; margin-right: 8px;">
                    <div style="height: 100%; border-radius: 4px; background: linear-gradient(90deg, #00d4ff, #00ffcc); width:{min(r['KPI_T'], 100)}%"></div>
                </div>
                <span style="color:#ffd700; font-weight:bold">{r['KPI_T']}%</span>
            </td>
        </tr>""")

    table_html = f"""
    <div class="table-wrapper">
        <table class="elite-table">
            <thead><tr>{"".join([f"<th>{h}</th>" for h in headers])}</tr></thead>
            <tbody>{"".join(rows_list)}</tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)

    # Footer
    st.markdown(f'<div style="position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #8b949e; padding: 10px; text-align: center; border-top: 1px solid #1a2a3a; z-index:999;">🛡️ Admin Louis | v11.4 | English Mode</div>', unsafe_allow_html=True)
