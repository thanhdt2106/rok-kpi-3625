import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CSS CHỐNG NỀN ĐEN & CĂN GIỮA ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .stSelectbox { max-width: 400px; margin: 0 auto; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. XỬ LÝ DỮ LIỆU (Giữ nguyên logic của Louis) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'

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
            pk = round(max(0.0, float(r['KI']) / gk) * 100, 1)
            pdv = round(max(0.0, float(r['DI']) / gd) * 100, 1)
            return pd.Series([pk, pdv, round((pk + pdv) / 2, 1), f"{gk/1e6:,.0f}M", f"{gd/1e3:,.0f}K"])
            
        df[['KPI_K', 'KPI_D', 'KPI_T', 'T_K', 'T_D']] = df.apply(get_metrics, axis=1)
        return df
    except: return None

df = load_data()

# --- 4. HIỂN THỊ GIAO DIỆN ---
if df is not None:
    st.write("<h2 style='text-align:center; color:#00d4ff;'>🛡️ FTD KPI COMMANDER</h2>", unsafe_allow_html=True)
    
    sel = st.selectbox("TRA CỨU THỐNG ĐỐC:", ["--- Chọn tên ---"] + sorted(df['Tên_2'].unique()))
    
    if sel != "--- Chọn tên ---":
        d = df[df['Tên_2'] == sel].iloc[0]
        
        # HTML & CSS GIAO DIỆN MỚI
        html_card = f"""
        <div style="position: relative; width: 1000px; margin: 50px auto; font-family: sans-serif;">
            
            <div style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); 
                        background: #223344; border: 2px solid #00d4ff; border-radius: 15px; 
                        padding: 15px 40px; z-index: 10; box-shadow: 0 5px 20px rgba(0,0,0,0.5); min-width: 300px;">
                <div style="color: #00d4ff; font-size: 22px; font-weight: 900; margin-bottom: 5px; text-align:center;">PROFILE MEMBER</div>
                <div style="color: #4ecca3; font-size: 24px; font-weight: bold; text-align:center;">{sel}</div>
                <div style="color: #8b949e; font-size: 11px; text-align:center;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
            </div>

            <div style="background: rgba(13, 25, 47, 0.95); border: 2px solid #005577; border-radius: 10px; 
                        padding: 60px 20px 20px 20px; display: flex; align-items: center; justify-content: space-between;">
                
                <div style="display: flex; gap: 15px; flex: 1;">
                    <div style="background: #2a3b4c; border-radius: 8px; padding: 15px; text-align: center; flex: 1;">
                        <div style="font-size: 10px; color: #8b949e;">SỨC MẠNH</div>
                        <div style="font-size: 18px; font-weight: bold; color: white;">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div style="background: #2a3b4c; border-radius: 8px; padding: 15px; text-align: center; flex: 1;">
                        <div style="font-size: 10px; color: #8b949e;">TỔNG KILL</div>
                        <div style="font-size: 18px; font-weight: bold; color: white;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                </div>

                <div style="width: 280px;"></div>

                <div style="display: flex; gap: 15px; align-items: center; flex: 1.5;">
                    <div style="background: #2a3b4c; border-radius: 8px; padding: 15px; text-align: center; flex: 1;">
                        <div style="font-size: 10px; color: #8b949e;">ĐIỂM CHẾT</div>
                        <div style="font-size: 18px; font-weight: bold; color: white;">{int(d['Điểm Chết_2']):,}</div>
                    </div>
                    
                    <div style="text-align: center;">
                        <div style="position: relative; width: 60px; height: 60px; margin: 0 auto;">
                            <svg viewBox="0 0 36 36" style="width: 60px; height: 60px; transform: rotate(-90deg);">
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#1a2634" stroke-width="3"></circle>
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" 
                                        stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round"></circle>
                            </svg>
                            <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:12px; font-weight:bold;">{d['KPI_D']}%</div>
                        </div>
                        <div style="font-size: 8px; color: #ff4b4b; font-weight: bold; margin-top: 5px;">KPI DEAD</div>
                    </div>

                    <div style="text-align: center;">
                        <div style="position: relative; width: 60px; height: 60px; margin: 0 auto;">
                            <svg viewBox="0 0 36 36" style="width: 60px; height: 60px; transform: rotate(-90deg);">
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#1a2634" stroke-width="3"></circle>
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" 
                                        stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round"></circle>
                            </svg>
                            <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:12px; font-weight:bold; color:#ffd700;">{d['KPI_T']}%</div>
                        </div>
                        <div style="font-size: 8px; color: #ffd700; font-weight: bold; margin-top: 5px;">TOTAL KPI</div>
                    </div>
                </div>
            </div>

            <div style="background: #2a3b4c; border-radius: 10px; width: 300px; margin: 15px auto 0; padding: 10px; text-align: center; border: 1px solid #445566;">
                <div style="font-size: 10px; color: #8b949e;">HẠNG HIỆN TẠI</div>
                <div style="font-size: 20px; font-weight: 900; color: #ffd700;">#{d['KillRank']}</div>
            </div>

        </div>
        """
        components.html(html_card, height=450)

    st.divider()
    st.dataframe(df[['Tên_2', 'ID', 'Sức Mạnh_2', 'KPI_T']].sort_values(by='KPI_T', ascending=False), use_container_width=True)
