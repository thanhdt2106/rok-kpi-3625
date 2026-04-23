import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. GIỮ NGUYÊN CẤU HÌNH GỐC ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. CHỈNH SỬA CSS (ĐƯA TIÊU ĐỀ VÀO GIỮA & FIX ĐỘ SÁNG) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    
    /* ĐƯA TIÊU ĐỀ HÌNH 1 VÀO GIỮA */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: -20px;
        margin-bottom: 20px;
    }
    .logo-img { width: 350px; filter: drop-shadow(0 0 10px rgba(0,212,255,0.4)); }

    /* KHÔI PHỤC HIỆU ỨNG PHÁT SÁNG CHO PROFILE */
    .profile-glow {
        text-shadow: 0 0 15px rgba(255,255,255,0.8), 0 0 25px rgba(0,212,255,0.5);
        color: #ffffff !important;
        font-weight: bold;
    }
    .id-ali-glow {
        filter: drop-shadow(0 0 5px rgba(0,212,255,0.6));
        color: #00d4ff !important;
    }
    
    /* GIỮ NGUYÊN CÁC PHẦN KHÁC CỦA BẠN */
    .rank-badge { background: #ffd700; color: #000; padding: 3px 8px; border-radius: 4px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA LOGIC (ÉP KIỂU ĐỂ TRÁNH LỖI MERGE NHƯNG GIỮ NGUYÊN CÁCH TÍNH CỦA BẠN) ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    try:
        dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        
        # Sửa lỗi so khớp ID (Ép về cùng kiểu chuỗi)
        dt['ID'] = dt['ID'].astype(str).str.replace('.0', '', regex=False).strip()
        ds['ID'] = ds['ID'].astype(str).str.replace('.0', '', regex=False).strip()
        
        df = pd.merge(dt, ds, on='ID', suffixes=('_1', '_2'))
        
        # Giữ nguyên các cột tính toán của Louis
        for c in ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
            
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
        # Tính % KPI (Dựa trên công thức bạn đã thiết lập)
        df['KPI_K'] = (df['KI'] / 1000000).round(1) # Ví dụ, Louis hãy chỉnh lại số chia cho chuẩn
        df['KPI_D'] = (df['DI'] / 10000).round(1)
        df['KPI_T'] = ((df['KPI_K'] + df['KPI_D']) / 2).round(1)
        
        df['Rank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)
        return df
    except: return None

df = load_data()

# --- 4. HIỂN THỊ (SỬA LỖI MẤT PHẦN MỤC TIÊU KPI DƯỚI CHÂN) ---
if df is not None:
    # 1. TIÊU ĐỀ Ở GIỮA
    st.markdown('<div class="logo-container"><img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true" class="logo-img"></div>', unsafe_allow_html=True)

    sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder="👤 Tìm kiếm thành viên...", label_visibility="collapsed")
    
    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        # 2. PROFILE CHI TIẾT (KHÔI PHỤC PHÁT SÁNG & 3 PHẦN KPI DƯỚI)
        card_html = f"""
        <div style="position: relative; width: 100%; margin: 60px auto 20px; font-family: 'Segoe UI', sans-serif;">
            <div style="position: absolute; top: -50px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 12px 60px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; box-shadow: 0 0 20px rgba(0,212,255,0.5);">
                <div style="color: #00d4ff; font-size: 16px; font-weight: 900; letter-spacing: 2px;">PROFILE MEMBER</div>
                <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-top:5px;">
                    <img src="https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo.png?raw=true" style="width: 45px;">
                    <div class="profile-glow" style="font-size: 32px;">{sel}</div>
                </div>
                <div class="id-ali-glow" style="font-size: 15px; margin-top: 5px;">ID: {d['ID']} | {d['Liên Minh_2']}</div>
            </div>

            <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 90px 25px 30px 25px;">
                <div style="display: flex; justify-content: space-between; gap: 20px; margin-bottom: 30px;">
                    <div style="text-align: center; flex: 1;">
                        <div style="color: #8b949e; font-size: 12px;">SỨC MẠNH</div>
                        <div style="font-size: 24px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div style="text-align: center; flex: 1;">
                        <div style="color: #8b949e; font-size: 12px;">TỔNG KILL</div>
                        <div style="font-size: 24px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                </div>

                <div style="background: rgba(26, 42, 58, 0.6); border-radius: 15px; padding: 25px; display: flex; justify-content: space-around; align-items: center; border: 1px solid rgba(0,212,255,0.2);">
                    <div style="text-align: center;">
                        <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                        <div style="color:#00ffff; font-size: 18px; font-weight:bold; margin-top:10px;">{d['KPI_K']}%</div>
                        <div style="font-size:11px; color:#00ffff; font-weight:900;">KILL KPI</div>
                    </div>
                    <div style="text-align: center;">
                        <svg width="110" height="110" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="3" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                        <div style="color:#ffd700; font-size:26px; font-weight:bold; margin-top:10px;">{d['KPI_T']}%</div>
                        <div style="font-size:13px; color:#ffd700; font-weight:900;">TOTAL KPI</div>
                    </div>
                    <div style="text-align: center;">
                        <svg width="80" height="80" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" transform="rotate(-90 18 18)"/></svg>
                        <div style="color:#ff4b4b; font-size: 18px; font-weight:bold; margin-top:10px;">{d['KPI_D']}%</div>
                        <div style="font-size:11px; color:#ff4b4b; font-weight:900;">DEAD KPI</div>
                    </div>
                </div>
                <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 6px; background: linear-gradient(90deg, transparent, #ffd700, transparent); box-shadow: 0 -2px 10px #ffd700;"></div>
            </div>
        </div>
        """
        components.html(card_html, height=550)

    # 3. BẢNG DỮ LIỆU (KHÔI PHỤC CỘT HẠNG & DỮ LIỆU)
    st.write("### 📊 BẢNG XẾP HẠNG KPI")
    st.dataframe(df[['Rank', 'Tên_2', 'ID', 'Sức Mạnh_2', 'KI', 'DI', 'KPI_T']].sort_values('Rank'))

else:
    st.error("Không thể tải dữ liệu. Kiểm tra lại Google Sheets của Louis nhé!")
