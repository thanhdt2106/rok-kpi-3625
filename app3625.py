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
        
        # Chuyển đổi số liệu
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        # Tính toán chênh lệch
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

# --- 4. HEADER ---
if df is not None:
    h_col1, h_col2 = st.columns([1, 1])
    with h_col1:
        st.markdown('<div class="header-left-text">FIGHT TO DEAD 3625</div>', unsafe_allow_html=True)
    with h_col2:
        sel = st.selectbox("", sorted(df['Tên_2'].dropna().unique()), index=None, placeholder="🔍 Search member name...", label_visibility="collapsed")

    # --- 5. PROFILE (Giữ nguyên giao diện gọn) ---
    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        html_card = f"""
        <div style="background: rgba(13, 25, 47, 0.98); border: 1px solid #00d4ff; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 20px;">
            <h2 style="font-family: 'Rajdhani', sans-serif; color: #fff; margin: 0;">{sel}</h2>
            <p style="color: #ffd700; font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: 20px;">Total KPI: {d['KPI_T']}%</p>
        </div>
        """
        st.write("") # Spacer
        components.html(html_card, height=120)

    # --- 6. TABLE (BASE + TOTAL + DIFF) ---
    df_sorted = df.sort_values(by='Rank')
    
    headers = [
        'Rank', 'Member', 'Alliance', 'Power', 
        'Base Kill', 'Total Kill', 'Kill (+)', 
        'Base Death', 'Total Death', 'Death (+)', 'KPI %'
    ]
    
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
            <td style="text-align:right; color:#00d4ff; font-family: 'Rajdhani', sans-serif; font-weight:bold;">+{int(r['KI']):,}</td>
            
            <td style="text-align:right; color:#8b949e; font-size:12px;">{int(r['Điểm Chết_1']):,}</td>
            <td style="text-align:right; color:#e0e6ed;">{int(r['Điểm Chết_2']):,}</td>
            <td style="text-align:right; color:#ff4b4b; font-family: 'Rajdhani', sans-serif; font-weight:bold;">+{int(r['DI']):,}</td>
            
            <td style="text-align:center;">
                <span style="font-family: 'Rajdhani', sans-serif; color:#ffd700; font-weight:700;">{r['KPI_T']}%</span>
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
    st.markdown(f'<div style="position: fixed; left: 0; bottom: 0; width: 100%; background: #050a0e; color: #8b949e; padding: 10px; text-align: center; border-top: 1px solid #1a2a3a; z-index:999; font-size:12px; font-family: Rajdhani;">🛡️ ADMIN LOUIS | V12.2 | BASE & CURRENT DATA COMPARISON</div>', unsafe_allow_html=True)
