import streamlit as st
import pandas as pd

# --- 1. CONFIG ---
st.set_page_config(page_title="FTD KPI 3625", layout="wide")

# Link ảnh (Giữ nguyên của Louis)
LOGO_MAIN = "https://github.com/thanhdt2106/rok-kpi-3625/blob/main/logo1.png?raw=true"

# --- 2. CSS TỐI ƯU ---
st.markdown("""
<style>
    .stApp { background-color: #050a0e; color: #e0e6ed; }
    .logo-container { text-align: center; margin-bottom: 20px; }
    .logo-img { width: 200px; }
    
    /* Style Table */
    .elite-table-container { background: #0d1b2a; border-radius: 10px; padding: 10px; overflow-x: auto; }
    table.elite-table { width: 100%; border-collapse: collapse; min-width: 900px; }
    .elite-table th { color: #00d4ff; border-bottom: 2px solid #00d4ff; padding: 10px; text-align: left; font-size: 12px; }
    .elite-table td { padding: 10px; border-bottom: 1px solid #1a2a3a; font-size: 14px; }
    
    .badge-rank { background: #ffd700; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
    .kpi-bar-bg { width: 100px; height: 8px; background: #1a2a3a; border-radius: 4px; display: inline-block; }
    .kpi-bar-fill { height: 100%; background: #00d4ff; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# --- 3. XỬ LÝ DỮ LIỆU ---
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=60)
def get_clean_data():
    try:
        df1 = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
        df2 = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())
        
        # Merge dữ liệu qua ID
        df = pd.merge(df1[['ID', 'Tên', 'Sức Mạnh', 'Tổng Tiêu Diệt', 'Điểm Chết']], 
                      df2[['ID', 'Tên', 'Sức Mạnh', 'Tổng Tiêu Diệt', 'Điểm Chết']], 
                      on='ID', suffixes=('_1', '_2'))

        # Hàm dọn dẹp số (Xóa dấu phẩy, khoảng trắng)
        def clean_num(value):
            s = str(value).replace(',', '').replace(' ', '')
            return pd.to_numeric(s, errors='coerce') or 0

        cols = ['Sức Mạnh_2', 'Tổng Tiêu Diệt_2', 'Điểm Chết_2', 'Tổng Tiêu Diệt_1', 'Điểm Chết_1']
        for c in cols:
            df[c] = df[c].apply(clean_num)

        # Tính KPI
        df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
        df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']
        
        def calculate_kpi(r):
            p = r['Sức Mạnh_2']
            target_k = 300e6 if p >= 45e6 else 250e6 if p >= 40e6 else 200e6
            target_d = 400e3 if p >= 30e6 else 300e3 if p >= 20e6 else 200e3
            pk = (r['KI'] / target_k * 100) if target_k > 0 else 0
            pdv = (r['DI'] / target_d * 100) if target_d > 0 else 0
            total = (pk + pdv) / 2
            return pd.Series([round(pk, 1), round(pdv, 1), round(total, 1)])

        df[['KPI_K', 'KPI_D', 'KPI_T']] = df.apply(calculate_kpi, axis=1)
        df['Rank'] = df['Tổng Tiêu Diệt_2'].rank(ascending=False, method='min').astype(int)
        return df.sort_values('Rank')
    except:
        return None

df = get_clean_data()

# --- 4. DISPLAY ---
if df is not None:
    st.markdown(f'<div class="logo-container"><img src="{LOGO_MAIN}" class="logo-img"></div>', unsafe_allow_html=True)
    
    # Bộ chia trang
    items_per_page = 20
    total_pages = (len(df) // items_per_page) + 1
    page = st.sidebar.number_input("Trang", min_value=1, max_value=total_pages, value=1)
    
    start_idx = (page - 1) * items_per_page
    df_page = df.iloc[start_idx : start_idx + items_per_page]

    rows = ""
    for _, r in df_page.iterrows():
        rows += f"""
        <tr>
            <td><span class="badge-rank">#{r['Rank']}</span></td>
            <td><b>{r['Tên_2']}</b><br><small>ID: {r['ID']}</small></td>
            <td>{int(r['Sức Mạnh_2']):,}</td>
            <td>{int(r['Tổng Tiêu Diệt_2']):,}</td>
            <td style="color:#ff4b4b">{int(r['Điểm Chết_2']):,}</td>
            <td style="color:#00ffff">{r['KPI_K']}%</td>
            <td style="color:#ff4b4b">{r['KPI_D']}%</td>
            <td>
                <div class="kpi-bar-bg"><div class="kpi-bar-fill" style="width:{min(r['KPI_T'], 100)}%"></div></div>
                <span style="color:#00ffcc">{r['KPI_T']}%</span>
            </td>
        </tr>
        """

    st.markdown(f"""
    <div class="elite-table-container">
        <table class="elite-table">
            <thead>
                <tr><th>HẠNG</th><th>CHIẾN BINH</th><th>SỨC MẠNH</th><th>TỔNG KILL</th><th>ĐIỂM CHẾT</th><th>KPI KILL</th><th>KPI DEAD</th><th>TỔNG KPI</th></tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.write(f"Tổng số: {len(df)} chiến binh")
