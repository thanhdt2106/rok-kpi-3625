import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS RESET NỀN ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .main-header {
        color: #00d4ff; text-align: center; font-size: 32px;
        font-weight: bold; padding: 10px; text-transform: uppercase;
    }
    .stSelectbox { max-width: 500px; margin: 0 auto; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. TẢI DỮ LIỆU ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
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
            pk = round(max(0.0, float(r['KI']) / gk) * 100, 1) if gk > 0 else 0.0
            pdv = round(max(0.0, float(r['DI']) / gd) * 100, 1) if gd > 0 else 0.0
            return pd.Series([pk, pdv, round((pk + pdv) / 2, 1), f"{gk/1e6:,.0f}M", f"{gd/1e3:,.0f}K"])
        
        df[['KPI_K', 'KPI_D', 'KPI_T', 'T_K', 'T_D']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 4. HIỂN THỊ ---
if df is not None:
    st.markdown('<div class="main-header">🛡️ COMMAND CENTER 3625</div>', unsafe_allow_html=True)
    
    _, col_search, _ = st.columns([1, 2, 1])
    with col_search:
        sel = st.selectbox("CHỌN THỐNG ĐỐC:", [ "--- Chọn tên ---"] + sorted(df['Tên_2'].unique()))
    
    if sel != "--- Chọn tên ---":
        d = df[df['Tên_2'] == sel].iloc[0]
        
        _, col_mid, _ = st.columns([1, 2, 1])
        with col_mid:
            # HTML CARD: Sáng hơn, chữ to, chia 2 hàng
            html_card = f"""
            <div style="background: linear-gradient(180deg, #16213e 0%, #0f3460 100%); 
                        border: 2px solid #4ecca3; border-radius: 20px; padding: 25px; 
                        color: #e9ecef; font-family: 'Segoe UI', sans-serif; 
                        box-shadow: 0 15px 35px rgba(0,0,0,0.6); text-align: center;">
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;">
                    <div style="text-align: left;">
                        <div style="font-size: 26px; font-weight: 900; color: #4ecca3; text-transform: uppercase;">{sel}</div>
                        <div style="font-size: 13px; color: #94a3b8;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                    </div>
                    <div style="background: #ffd700; color: #1a1a1a; padding: 8px 15px; border-radius: 10px; font-weight: 900; font-size: 18px;">
                        RANK {d['KillRank']}
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 25px;">
                    <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(78,204,163,0.2);">
                        <div style="font-size: 10px; color: #94a3b8; font-weight: bold;">SỨC MẠNH</div>
                        <div style="font-size: 18px; font-weight: bold; color: white;">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(78,204,163,0.2);">
                        <div style="font-size: 10px; color: #ffd700; font-weight: bold;">TỔNG KILL</div>
                        <div style="font-size: 18px; font-weight: bold; color: #ffd700;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                    <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(78,204,163,0.2);">
                        <div style="font-size: 10px; color: #ff4b4b; font-weight: bold;">ĐIỂM CHẾT</div>
                        <div style="font-size: 18px; font-weight: bold; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                    </div>
                </div>

                <div style="display: flex; justify-content: space-around; align-items: flex-end;">
                    <div style="text-align: center;">
                        <svg width="80" height="80" viewBox="0 0 36 36">
                            <circle cx="18" cy="18" r="16" fill="none" stroke="#2d3436" stroke-width="3"></circle>
                            <circle cx="18" cy="18" r="16" fill="none" stroke="#4ecca3" stroke-width="3" 
                                    stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"></circle>
                            <text x="18" y="20.5" text-anchor="middle" font-size="8" font-weight="bold" fill="white">{d['KPI_K']}%</text>
                        </svg>
                        <div style="font-size: 9px; margin-top: 8px; font-weight: bold;">KPI KILL</div>
                        <div style="font-size: 8px; color: #94a3b8;">Mục tiêu: {d['T_K']}</div>
                    </div>

                    <div style="text-align: center;">
                        <svg width="100" height="100" viewBox="0 0 36 36">
                            <circle cx="18" cy="18" r="16" fill="none" stroke="#2d3436" stroke-width="2.5"></circle>
                            <circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" 
                                    stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"></circle>
                            <text x="18" y="21" text-anchor="middle" font-size="9" font-weight="900" fill="#ffd700">{d['KPI_T']}%</text>
                        </svg>
                        <div style="font-size: 11px; margin-top: 5px; font-weight: bold; color: #ffd700;">TOTAL KPI</div>
                    </div>

                    <div style="text-align: center;">
                        <svg width="80" height="80" viewBox="0 0 36 36">
                            <circle cx="18" cy="18" r="16" fill="none" stroke="#2d3436" stroke-width="3"></circle>
                            <circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" 
                                    stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round" transform="rotate(-90 18 18)"></circle>
                            <text x="18" y="20.5" text-anchor="middle" font-size="8" font-weight="bold" fill="white">{d['KPI_D']}%</text>
                        </svg>
                        <div style="font-size: 9px; margin-top: 8px; font-weight: bold;">KPI DEAD</div>
                        <div style="font-size: 8px; color: #94a3b8;">Mục tiêu: {d['T_D']}</div>
                    </div>
                </div>
            </div>
            """
            components.html(html_card, height=500)

    st.divider()
    st.dataframe(df[['Tên_2', 'ID', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'KPI_T']].sort_values(by='KPI_T', ascending=False), use_container_width=True)
