import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS CĂN GIỮA & GIAO DIỆN TỐI ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .main-header {
        color: #00d4ff; text-align: center; font-size: 32px;
        font-weight: bold; padding: 15px; text-transform: uppercase;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
    }
    /* Căn giữa ô tìm kiếm */
    .stSelectbox { max-width: 500px; margin: 0 auto; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. QUẢN LÝ NGÔN NGỮ ---
_, col_l = st.columns([4, 1])
with col_l:
    lang = st.radio("LANG:", ["VN", "EN"], horizontal=True, label_visibility="collapsed")

L = {
    "VN": {"header": "🛡️ QUẢN LÝ KPI 3625", "search": "🔍 CHỌN CHIẾN BINH:", "select": "--- Chọn tên ---", "target": "Mục tiêu:"},
    "EN": {"header": "🛡️ KPI MANAGEMENT 3625", "search": "🔍 SELECT WARRIOR:", "select": "--- Select name ---", "target": "Target:"}
}[lang]

# --- 4. TẢI DỮ LIỆU ---
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
            # KPI định mức (Louis có thể chỉnh lại số này cho chuẩn KvK)
            gk = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 200e6
            gd = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = max(0.0, float(r['KI']) / gk) if gk > 0 else 0.0
            pdv = max(0.0, float(r['DI']) / gd) if gd > 0 else 0.0
            return pd.Series([round(pk * 100, 1), round(pdv * 100, 1), round(((pk + pdv) / 2) * 100, 1), f"{gk/1e6:,.0f}M", f"{gd/1e3:,.0f}K"])
        
        df[['KPI_K', 'KPI_D', 'KPI_T', 'T_K', 'T_D']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    st.markdown(f'<div class="main-header">{L["header"]}</div>', unsafe_allow_html=True)
    
    _, col_search, _ = st.columns([1, 2, 1])
    with col_search:
        sel = st.selectbox(L["search"], [L["select"]] + sorted(df['Tên_2'].unique()), label_visibility="collapsed")
    
    if sel != L["select"]:
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # ÉP KHUNG VÀO GIỮA
        _, col_mid, _ = st.columns([1, 2, 1])
        
        with col_mid:
            html_card = f"""
            <div style="background: #0d1117; border: 2px solid #00d4ff; border-radius: 15px; padding: 25px; color: white; font-family: sans-serif; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <div>
                        <div style="font-size: 28px; font-weight: 800; color: #00d4ff;">{sel}</div>
                        <div style="font-size: 13px; color: #8b949e;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                    </div>
                    <div style="background: #ffd700; color: #000; padding: 5px 15px; border-radius: 8px; font-weight: bold; font-size: 18px;">
                        #{d['KillRank']}
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 20px;">
                    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 10px; color: #8b949e;">SỨC MẠNH</div>
                        <div style="font-size: 18px; font-weight: bold;">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 10px; color: #ffd700;">TỔNG KILL</div>
                        <div style="font-size: 18px; font-weight: bold; color: #ffd700;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 10px; color: #ff4b4b;">ĐIỂM CHẾT</div>
                        <div style="font-size: 18px; font-weight: bold; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                    </div>
                </div>

                <div style="display: flex; justify-content: space-around; align-items: center; background: rgba(0,212,255,0.03); padding: 20px; border-radius: 12px; border: 1px dashed rgba(0,212,255,0.2);">
                    <div style="text-align: center;">
                        <div style="position: relative; width: 80px; height: 80px; margin: 0 auto 10px;">
                            <svg viewBox="0 0 36 36" style="width: 80px; height: 80px; transform: rotate(-90deg);">
                                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#222" stroke-width="3"/>
                                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100"/>
                            </svg>
                            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 14px; font-weight: bold;">{d['KPI_K']}%</div>
                        </div>
                        <div style="font-size: 9px; color: #00ffff; font-weight: bold;">KPI KILL</div>
                        <div style="font-size: 9px; color: #8b949e;">{L['target']}: {d['T_K']}</div>
                    </div>

                    <div style="text-align: center;">
                        <div style="position: relative; width: 80px; height: 80px; margin: 0 auto 10px;">
                            <svg viewBox="0 0 36 36" style="width: 80px; height: 80px; transform: rotate(-90deg);">
                                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#222" stroke-width="3"/>
                                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100"/>
                            </svg>
                            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 14px; font-weight: bold;">{d['KPI_D']}%</div>
                        </div>
                        <div style="font-size: 9px; color: #ff4b4b; font-weight: bold;">KPI DEAD</div>
                        <div style="font-size: 9px; color: #8b949e;">{L['target']}: {d['T_D']}</div>
                    </div>

                    <div style="text-align: center;">
                        <div style="position: relative; width: 100px; height: 100px; margin: 0 auto 5px;">
                            <svg viewBox="0 0 36 36" style="width: 100px; height: 100px; transform: rotate(-90deg);">
                                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#222" stroke-width="2"/>
                                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#ffd700" stroke-width="3" stroke-dasharray="{min(d['KPI_T'], 100)}, 100"/>
                            </svg>
                            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 20px; font-weight: 900; color: #ffd700;">{d['KPI_T']}%</div>
                        </div>
                        <div style="font-size: 10px; color: #ffd700; font-weight: bold;">TOTAL KPI</div>
                    </div>
                </div>
            </div>
            """
            components.html(html_card, height=450)

    # Dữ liệu bảng phía dưới
    st.divider()
    st.dataframe(df[['Tên_2', 'ID', 'Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'KPI_T']].sort_values(by='Tổng Tiêu Diệt_2', ascending=False), use_container_width=True)
