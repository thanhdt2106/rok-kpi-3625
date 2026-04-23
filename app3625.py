import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CONFIG ---
st.set_page_config(
    page_title="FTD KPI | COMMAND CENTER", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Saira:wght@400;600;800&display=swap');

    [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"] { display: none !important; width: 0px !important; }
    header { visibility: hidden; }
    .main .block-container { max-width: 100% !important; padding: 0.5rem 1.5rem !important; }
    
    .stApp { 
        background-color: #050a0e; 
        color: #e0e6ed;
        font-family: 'Saira', sans-serif; 
    }
    
    .header-left-text {
        font-family: 'Rajdhani', sans-serif;
        color: #00d4ff;
        font-weight: 700;
        font-size: 26px;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.4);
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .table-wrapper { 
        background: rgba(13, 27, 42, 0.4); 
        border: 1px solid #1e3a5a; 
        border-radius: 8px; padding: 15px; margin-top: 10px; overflow-x: auto;
    }
    .elite-table { width: 100%; border-collapse: collapse; min-width: 1300px;}
    .elite-table thead th { 
        font-family: 'Rajdhani', sans-serif;
        background: rgba(0, 212, 255, 0.05); color: #00d4ff; 
        text-align: center !important; padding: 12px; font-size: 12px; 
        border-bottom: 2px solid #00d4ff; text-transform: uppercase;
    }
    .elite-table td { 
        padding: 12px 8px; font-size: 13px; color: #e0e6ed; border-bottom: 1px solid #1a2a3a; 
    }
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

# --- 4. HEADER & SEARCH ---
if df is not None:
    h_col1, h_col2 = st.columns([1, 1])
    with h_col1:
        st.markdown('<div class="header-left-text">FIGHT TO DEAD 3625</div>', unsafe_allow_html=True)
    with h_col2:
        sel = st.selectbox(
            "", 
            sorted(df['Tên_2'].dropna().unique()), 
            index=None, 
            placeholder="🔍 Enter your Name or ID here...", 
            label_visibility="collapsed"
        )

    # --- 5. FULL DETAILED PROFILE CARD (RESTORED ALL 4 TOP BOXES) ---
    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        cur_k = f"{d['KI']/1e6:.1f}M"
        tar_k = f"{d['T_K']/1e6:.0f}M"
        cur_d = f"{d['DI']/1e3:.1f}K"
        tar_d = f"{d['T_D']/1e3:.0f}K"

        html_card = f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Saira:wght@400;700&display=swap');
            .stat-box {{ background: rgba(35, 53, 73, 0.5); border-radius: 6px; padding: 12px; text-align: center; }}
            .stat-label {{ font-size: 10px; color: #8b949e; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }}
            .stat-value {{ font-family: 'Rajdhani', sans-serif; font-size: 22px; font-weight: 700; color: #fff; }}
            .mini-bar-box {{ margin-top: 8px; width: 100px; margin-left: auto; margin-right: auto; }}
            .mini-progress-container {{ width: 100%; background: #0d151f; height: 5px; border-radius: 3px; overflow: hidden; margin: 4px 0; }}
            .mini-fill-k {{ height: 100%; background: #00d4ff; }}
            .mini-fill-d {{ height: 100%; background: #ff4b4b; }}
            .target-label {{ font-family: 'Saira', sans-serif; font-size: 10px; color: #ffd700; font-weight: 700; text-transform: uppercase; }}
            .current-label {{ font-family: 'Rajdhani', sans-serif; font-size: 15px; color: #fff; font-weight: 700; }}
        </style>

        <div style="position: relative; max-width: 950px; margin: 55px auto 15px; font-family: 'Saira', sans-serif;">
            <div style="position: absolute; top: -40px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 1px solid #00d4ff; border-radius: 8px; padding: 10px 25px; z-index: 10; text-align: center; border-bottom: 3px solid #ffd700; width: 340px;">
                <div style="display: flex; align-items: center; justify-content: center; gap: 12px;">
                    <img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true" style="width: 32px;">
                    <div style="font-family: 'Rajdhani', sans-serif; color: #ffffff; font-size: 24px; font-weight: 700;">{sel}</div>
                </div>
                <div style="font-size: 12px; color: #8b949e; margin-top: 2px;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
            </div>
            
            <div style="background: rgba(13, 25, 47, 0.98); border: 1px solid #00d4ff; border-radius: 12px; padding: 60px 20px 20px 20px;">
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px;">
                    <div class="stat-box" style="border-bottom: 2px solid #ffd700;">
                        <div class="stat-label">RANK</div>
                        <div class="stat-value" style="color: #ffd700;">#{int(d['Rank'])}</div>
                    </div>
                    <div class="stat-box" style="border-bottom: 2px solid #00d4ff;">
                        <div class="stat-label">POWER</div>
                        <div class="stat-value">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div class="stat-box" style="border-bottom: 2px solid #00ffcc;">
                        <div class="stat-label">TOTAL KILL</div>
                        <div class="stat-value" style="color: #00ffcc;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                    <div class="stat-box" style="border-bottom: 2px solid #ff4b4b;">
                        <div class="stat-label">DEAD PT</div>
                        <div class="stat-value" style="color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                    </div>
                </div>

                <div style="background: rgba(26, 42, 58, 0.3); border-radius: 8px; padding: 25px 10px; border: 1px solid rgba(0, 212, 255, 0.1); display: flex; justify-content: space-around; align-items: flex-start;">
                    <div style="text-align: center;">
                        <svg width="55" height="55" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                        <div style="font-family: 'Rajdhani', sans-serif; color:#00ffff; font-size: 16px; font-weight:700; margin-top:4px;">{d['KPI_K']}%</div>
                        <div class="mini-bar-box">
                            <div class="current-label">{cur_k}</div>
                            <div class="mini-progress-container"><div class="mini-fill-k" style="width:{min(d['KPI_K'], 100)}%"></div></div>
                            <div class="target-label">Target: {tar_k}</div>
                        </div>
                    </div>

                    <div style="text-align: center;">
                        <svg width="85" height="85" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="4" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                        <div style="font-family: 'Rajdhani', sans-serif; color:#ffd700; font-size:28px; font-weight:700;">{d['KPI_T']}%</div>
                        <div style="font-size:12px; color:#ffd700; font-weight:700; letter-spacing:1px;">TOTAL KPI</div>
                    </div>

                    <div style="text-align: center;">
                        <svg width="55" height="55" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                        <div style="font-family: 'Rajdhani', sans-serif; color:#ff4b4b; font-size: 16px; font-weight:700; margin-top:4px;">{d['KPI_D']}%</div>
                        <div class="mini-bar-box">
                            <div class="current-label">{cur_d}</div>
                            <div class="mini-progress-container"><div class="mini-fill-d" style="width:{min(d['KPI_D'], 100)}%"></div></div>
                            <div class="target-label">Target: {tar_d}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        components.html(html_card, height=520)

    # --- 6. TABLE ---
    df_sorted = df.sort_values(by='Rank')
    headers = ['Rank', 'Member', 'Alliance', 'Power', 'Base Kill', 'Total Kill', 'Kill (+)', 'Base Death', 'Total Death', 'Death (+)', 'KPI %']
    
    rows_list = []
    for _, r in df_sorted.iterrows():
        rows_list.append(f"""
        <tr>
            <td style="font-family: 'Rajdhani', sans-serif; font-weight:700; color:#ffd700; text-align:center;">#{int(r['Rank'])}</td>
            <td><b style="color:#fff;">{r['Tên_2']}</b></td>
            <td style="text-align:center; color:#8b949e; font-size:11px;">{r['Liên Minh_2']}</td>
            <td style="text-align:right; font-family: 'Rajdhani', sans-serif;">{int(r['Sức Mạnh_2']):,}</td>
            <td style="text-align:right; color:#8b949e; font-size:12px;">{int(r['Tổng Tiêu Diệt_1']):,}</td>
            <td style="text-align:right; color:#e0e6ed;">{int(r['Tổng Tiêu Diệt_2']):,}</td>
            <td style="text-align:right; color:#00d4ff; font-weight:bold;">+{int(r['KI']):,}</td>
            <td style="text-align:right; color:#8b949e; font-size:12px;">{int(r['Điểm Chết_1']):,}</td>
            <td style="text-align:right; color:#e0e6ed;">{int(r['Điểm Chết_2']):,}</td>
            <td style="text-align:right; color:#ff4b4b; font-weight:bold;">+{int(r['DI']):,}</td>
            <td style="text-align:center;"><span style="font-family: 'Rajdhani', sans-serif; color:#ffd700; font-weight:700;">{r['KPI_T']}%</span></td>
        </tr>""")

    st.markdown(f'<div class="table-wrapper"><table class="elite-table"><thead><tr>{"".join([f"<th>{h}</th>" for h in headers])}</tr></thead><tbody>{"".join(rows_list)}</tbody></table></div>', unsafe_allow_html=True)

    # Footer
    st.markdown(f'<div style="position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #8b949e; padding: 10px; text-align: center; border-top: 1px solid #1a2a3a; z-index:999; font-size:12px; font-family: Rajdhani;">🛡️ ADMIN LOUIS | V12.6 | FULL PROFILE INTERFACE</div>', unsafe_allow_html=True)
