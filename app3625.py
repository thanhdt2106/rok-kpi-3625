import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG (GIỮ THANH TASKBAR GỐC) ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. SIÊU CSS & JS (FIX NGĂN KÉO & HIỆU ỨNG GLOW) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    [data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #00d4ff; }
    .block-container { padding-top: 1rem !important; max-width: 98% !important; }

    /* STYLE CHO THANH KÉO (DRAWER) */
    #myDrawer {
        height: 100%; width: 0; position: fixed; z-index: 999999;
        top: 0; left: 0; background-color: rgba(13, 27, 42, 0.98);
        overflow-x: hidden; transition: 0.5s; padding-top: 60px;
        border-right: 2px solid #00d4ff; box-shadow: 15px 0 30px rgba(0,0,0,0.7);
    }
    #myDrawer a {
        padding: 15px 25px; text-decoration: none; font-size: 15px; color: #e0e6ed;
        display: block; transition: 0.3s; border-bottom: 1px solid rgba(0,212,255,0.05);
    }
    #myDrawer .closebtn { position: absolute; top: 10px; right: 25px; font-size: 36px; color: #ff4b4b; }

    /* TABLE STYLE */
    .table-wrapper { background: rgba(13, 27, 42, 0.6); border: 1px solid #1e3a5a; border-radius: 12px; padding: 20px; margin-top: 20px; }
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
    </style>

    <div id="myDrawer">
      <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
      <div style="color: #00d4ff; font-weight: bold; padding: 0 25px 20px; font-size: 18px; border-bottom: 1px solid #1e3a5a;">📋 QUẢN TRỊ VIÊN</div>
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
    components.html("""<button onclick="parent.openNav()" style="width: 100%; background: #1a2a3a; color: #00d4ff; border: 1px solid #00d4ff; padding: 10px; border-radius: 5px; cursor: pointer; font-weight: bold;">⚙️ CÀI ĐẶT HỆ THỐNG</button>""", height=50)
    st.divider()
    menu = st.radio("Menu", ["📊 Bảng KPI", "👤 Tài khoản"])
    st.info(f"Admin Louis | v10.9")

# --- 4. DATA LOGIC (TRIỆT TIÊU LỖI MERGE ID) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        
        # QUAN TRỌNG: Ép ID về dạng String để không bị lỗi Merge
        dt['ID'] = dt['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        ds['ID'] = ds['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
        
        df = pd.merge(dt.drop_duplicates('ID'), ds.drop_duplicates('ID'), on='ID', suffixes=('_1', '_2'))
        
        # Xử lý số liệu
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
            
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
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
        st.error(f"Lỗi: {e}")
        return None

df = load_data()

# --- 5. HIỂN THỊ ---
if df is not None:
    st.markdown('<div style="display: flex; justify-content: center;"><img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true" width="300"></div>', unsafe_allow_html=True)
    
    if menu == "📊 Bảng KPI":
        sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder="👤 Tìm kiếm thành viên...", label_visibility="collapsed")
        
        if sel:
            d = df[df['Tên_2'] == sel].iloc[0]
            # PROFILE CARD VỚI MỤC TIÊU DƯỚI VÒNG TRÒN
            card_html = f"""
            <div style="position: relative; width: 100%; margin: 60px auto 20px; font-family: sans-serif;">
                <div style="position: absolute; top: -50px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 12px 50px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; box-shadow: 0 0 25px #00d4ff66; min-width: 350px;">
                    <div style="color: #00d4ff; font-size: 12px; font-weight: 900; letter-spacing: 2px;">PROFILE MEMBER</div>
                    <div style="color: #ffffff; font-size: 28px; font-weight: bold; text-shadow: 0 0 15px #ffffff88;">{sel}</div>
                    <div style="font-size: 13px; color: #ffffff; font-weight: 600;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
                </div>
                <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 85px 25px 35px; position: relative;">
                    <div style="display: flex; justify-content: space-around; margin-bottom: 25px;">
                        <div style="text-align: center;">
                            <div style="font-size: 10px; color: #8b949e;">SỨC MẠNH</div>
                            <div style="font-size: 22px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 10px; color: #8b949e;">TỔNG TIÊU DIỆT</div>
                            <div style="font-size: 22px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 10px; color: #ff4b4b;">ĐIỂM CHẾT</div>
                            <div style="font-size: 22px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                        </div>
                    </div>
                    <div style="background: rgba(26, 42, 58, 0.6); border-radius: 15px; padding: 25px; display: flex; justify-content: space-around; align-items: center; border: 1px solid #00d4ff33;">
                        <div style="text-align: center;">
                            <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#00ffff; font-size: 16px; font-weight:bold; margin-top:8px;">{d['KPI_K']}%</div>
                            <div style="font-size:10px; color:#00ffff; font-weight:900; margin-top:2px;">KPI KILL</div>
                        </div>
                        <div style="text-align: center;">
                            <svg width="110" height="110" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ffd700; font-size:24px; font-weight:bold; margin-top:8px;">{d['KPI_T']}%</div>
                            <div style="font-size:12px; color:#ffd700; font-weight:900; margin-top:2px;">TOTAL KPI</div>
                        </div>
                        <div style="text-align: center;">
                            <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                            <div style="color:#ff4b4b; font-size: 16px; font-weight:bold; margin-top:8px;">{d['KPI_D']}%</div>
                            <div style="font-size:10px; color:#ff4b4b; font-weight:900; margin-top:2px;">KPI DEAD</div>
                        </div>
                    </div>
                    <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 6px; background: linear-gradient(90deg, transparent, #ffd700, transparent); box-shadow: 0 -2px 15px #ffd700;"></div>
                </div>
            </div>
            """
            components.html(card_html, height=540)

        # BẢNG TABLE
        df_sorted = df.sort_values(by='Rank')
        rows = "".join([f"<tr><td><span class='rank-badge'>#{int(r['Rank'])}</span></td><td><b>{r['Tên_2']}</b><br><small>ID: {r['ID']}</small></td><td style='text-align:right'>{int(r['Sức Mạnh_2']):,}</td><td style='text-align:right; color:#00ffcc'>{int(r['Tổng Tiêu Diệt_2']):,}</td><td style='text-align:right; color:#ff4b4b'>{int(r['Điểm Chết_2']):,}</td><td style='text-align:right; color:#00d4ff'>+{int(r['KI']):,}</td><td style='text-align:right; color:#ff4b4b'>+{int(r['DI']):,}</td><td style='color:#ffd700; font-weight:bold'>{r['KPI_T']}%</td></tr>" for _, r in df_sorted.iterrows()])
        st.markdown(f"<div class='table-wrapper'><table class='elite-table'><thead><tr><th>Hạng</th><th>Thành viên</th><th>Sức mạnh</th><th>Tổng Kill</th><th>Điểm Chết</th><th>Kill +</th><th>Dead +</th><th>KPI %</th></tr></thead><tbody>{rows}</tbody></table></div>", unsafe_allow_html=True)

    st.markdown('<div style="text-align: center; color: #8b949e; padding: 20px;">🛡️ Admin Louis | v10.9</div>', unsafe_allow_html=True)
