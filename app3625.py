# app3625.py
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import requests
import os

# ==============================================================================
# 1. CẤU HÌNH GIAO DIỆN CHUẨN ĐỒ HỌA FULL SCREEN
# ==============================================================================
# Cho phép mở Sidebar mặc định để tiện thao tác (hoặc đổi thành "collapsed" nếu muốn mặc định ẩn)
st.set_page_config(page_title="FTD KPI SYSTEM", layout="wide", initial_sidebar_state="expanded")

# Inject CSS tối ưu khung nhìn chính và tùy chỉnh giao diện Sidebar Admin cho rực rỡ
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 10px !important; max-width: 100% !important;}
        iframe {width: 100% !important; border: none;}
        
        /* Tùy chỉnh hiệu ứng cho thanh Sidebar mượt mà hơn */
        [data-testid="stSidebar"] {
            background-color: #0d1117;
            border-right: 1px solid #21262d;
        }
    </style>
""", unsafe_allow_html=True)

# ─── THÔNG TIN GOOGLE SHEETS CỦA BẠN ───
SHEET_ID = "15CrOFNFsIno34mX0EuXkLKdwiJgn3rrmcM-sEKmoKUQ"
GID1 = "0"
GID2 = "1325084102"

# ==============================================================================
# 2. HÀM TẢI DỮ LIỆU TỪ GOOGLE SHEETS (DẠNG CSV ĐỂ ĐẠT TỐC ĐỘ CAO NHẤT)
# ==============================================================================
def load_csv_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    df = pd.read_csv(url, dtype=str)
    df.columns = df.columns.str.strip()
    return df

# ==============================================================================
# 3. ĐƯA TOÀN BỘ KHU VỰC ĐIỀU KHIỂN ĐĂNG NHẬP / SỬA DATA VÀO SIDEBAR
# ==============================================================================
with st.sidebar:
    st.markdown("## 🛡️ ADMIN PANEL")
    st.caption("Khu vực dành riêng cho Ban Quản Trị liên minh.")
    
    # Ô nhập mật khẩu Admin (Dữ liệu lấy từ mục Secrets đã cấu hình trên web)
    admin_password = st.text_input("Mật khẩu Admin", type="password", placeholder="Nhập pass để sửa...")
    
    # Khởi tạo trạng thái đăng nhập
    is_admin = False
    
    if admin_password:
        if admin_password == st.secrets["admin"]["password"]:
            is_admin = True
            st.success("🔓 Kích hoạt quyền Admin!")
            st.markdown("---")
            
            # Form chọn bảng tính cần chỉnh sửa
            sheet_option = st.selectbox("Chọn bảng tính cần thao tác:", [
                "Bảng 1: KPI Gốc (0)", 
                "Bảng 2: Cập Nhật Mới (1325084102)"
            ])
            
            # ⚠️ CHÚ Ý: Đảm bảo viết đúng tên Tab hiển thị trên file Google Sheets của bạn
            if "Bảng 1" in sheet_option:
                target_gid = GID1
                worksheet_name = "Sheet1"  # Thay bằng tên tab thực tế của Gid 855089129
            else:
                target_gid = GID2
                worksheet_name = "Sheet2"  # Thay bằng tên tab thực tế của Gid 316243863
                
            # Đọc dữ liệu thô phục vụ cho việc chỉnh sửa
            df_to_edit = load_csv_data(target_gid)
        else:
            st.error("❌ Mật khẩu không chính xác!")

st.markdown("---")

# ==============================================================================
# 4. HIỂN THỊ BẢNG CHỈNH SỬA Ở KHU VỰC CHÍNH KHI ADMIN ĐĂNG NHẬP THÀNH CÔNG
# ==============================================================================
# Nếu Admin đã log-in đúng, hiển thị bảng dữ liệu to rõ ràng ngay phía trên hệ thống Card
if is_admin:
    st.subheader(f"📝 Chỉnh sửa dữ liệu trực tiếp: {worksheet_name}")
    st.info("💡 Mẹo: Bạn có thể click đúp vào ô để sửa số liệu, hoặc kéo thả, thêm hàng ở dưới bảng.")
    
    # Tạo bảng tương tác thông minh diện tích lớn ở màn hình chính
    edited_df = st.data_editor(df_to_edit, num_rows="dynamic", use_container_width=True)
    
    # Nút bấm kích hoạt đồng bộ ngược lên Google Sheets
    if st.button("💾 XÁC NHẬN LƯU VÀ ĐỒNG BỘ LÊN GOOGLE SHEETS"):
        # Chuyển đổi dữ liệu bảng thành mảng Matrix (bao gồm Header) gửi lên Apps Script
        header = edited_df.columns.tolist()
        matrix_data = [header] + edited_df.fillna("").values.tolist()
        
        payload = {
            "worksheet": worksheet_name,
            "data": matrix_data
        }
        
        with st.spinner("🚀 Đang tiến hành đồng bộ hóa lên Google Sheets..."):
            try:
                response = requests.post(st.secrets["api"]["app_url"], json=payload)
                res_json = response.json()
                
                if res_json.get("status") == "success":
                    st.balloons()
                    st.success(f"Thành công: {res_json.get('message')}")
                    # Xóa bỏ bộ nhớ đệm cache để hệ thống Card cập nhật số liệu mới ngay lập tức
                    st.cache_data.clear()
                else:
                    st.error(f"Thất bại từ hệ thống Sheets: {res_json.get('message')}")
            except Exception as e:
                st.error(f"Lỗi kết nối API Web App: {e}")
                
    st.markdown("---")

# ==============================================================================
# 5. LOGIC XỬ LÝ DỮ LIỆU KPI & BIẾN ĐỔI SANG THẺ CARDS (USER VIEW)
# ==============================================================================
def get_kpi_kill_value(p):
    if p >= 100_000_000: return 600_000_000
    elif p >= 80_000_000: return 450_000_000
    return 300_000_000

def get_kpi_dead_value(p):
    if p >= 100_000_000: return 1_500_000
    elif p >= 90_000_000: return 1_200_000
    elif p >= 80_000_000: return 1_000_000
    elif p >= 70_000_000: return 800_000
    elif p >= 60_000_000: return 700_000
    elif p >= 50_000_000: return 600_000
    elif p >= 40_000_000: return 500_000
    elif p >= 30_000_000: return 400_000
    else: return 300_000

@st.cache_data(ttl=60)
def process_cards_data():
    df1 = load_csv_data(GID1)
    df2 = load_csv_data(GID2)

    def to_int(x):
        try: return int(str(x).replace(",", ""))
        except: return 0

    def find_col(df, keywords):
        for col in df.columns:
            if all(k.lower() in col.lower() for k in keywords):
                return col
        return None

    col_pow = find_col(df2, ["sức", "mạnh"]) or "Sức Mạnh"
    col_kill = find_col(df2, ["tổng", "tiêu", "diệt"]) or find_col(df2, ["kill"]) or "Tổng Tiêu Diệt"
    col_dead = find_col(df2, ["chết"]) or "Điểm Chết"
    col_t4, col_t5 = "T4", "T5"

    df1["ID_str"] = df1["ID"].astype(str).str.strip()
    df2["ID_str"] = df2["ID"].astype(str).str.strip()

    name_sheet2 = df2.set_index("ID_str")["Tên"].to_dict()
    pow_sheet2 = df2.set_index("ID_str")[col_pow].to_dict()
    kill_sheet2 = df2.set_index("ID_str")[col_kill].to_dict()
    dead_sheet2 = df2.set_index("ID_str")[col_dead].to_dict()
    
    t4_sheet1 = df1.set_index("ID_str")[col_t4].to_dict() if col_t4 in df1.columns else {}
    t5_sheet1 = df1.set_index("ID_str")[col_t5].to_dict() if col_t5 in df1.columns else {}
    t4_sheet2 = df2.set_index("ID_str")[col_t4].to_dict() if col_t4 in df2.columns else {}
    t5_sheet2 = df2.set_index("ID_str")[col_t5].to_dict() if col_t5 in df2.columns else {}

    col_dead_s1 = find_col(df1, ["chết"]) or "Điểm Chết"
    df1["Power_Goc"] = df1[find_col(df1, ["sức", "mạnh"]) or "Sức Mạnh"].apply(to_int)
    df1['Indiv_KPI_Dead'] = df1['Power_Goc'].apply(get_kpi_dead_value)
    df1['Group'] = df1['Tên'].apply(lambda x: str(x).split()[0].upper() if pd.notnull(x) else "")
    
    def calc_indiv_diff_dead(row):
        p_id = row['ID_str']
        d_s1 = to_int(row[col_dead_s1])
        d_s2 = to_int(dead_sheet2.get(p_id, d_s1))
        return d_s2 - d_s1

    df1['Indiv_Diff_Dead'] = df1.apply(calc_indiv_diff_dead, axis=1)
    group_kpi_dead_sum = df1.groupby('Group')['Indiv_KPI_Dead'].transform('sum')
    group_diff_dead_sum = df1.groupby('Group')['Indiv_Diff_Dead'].transform('sum')
    group_max_power = df1.groupby('Group')['Power_Goc'].transform('max')

    processed_list = []
    for i, row in df1.iterrows():
        p_id = row['ID_str']
        is_main = (row['Power_Goc'] == group_max_power[i])
        final_target_dead = group_kpi_dead_sum[i] if is_main else row['Indiv_KPI_Dead']
        diff_dead = group_diff_dead_sum[i] if is_main else row['Indiv_Diff_Dead']
        current_name = name_sheet2.get(p_id, row["Tên"])
        
        pow_s1 = to_int(row[find_col(df1, ["sức", "mạnh"]) or "Sức Mạnh"])
        dead_s1 = to_int(row[col_dead_s1])
        t4_s1 = to_int(t4_sheet1.get(p_id, 0))
        t5_s1 = to_int(t5_sheet1.get(p_id, 0))
        
        pow_s2 = to_int(pow_sheet2.get(p_id, pow_s1))
        kill_s2 = to_int(kill_sheet2.get(p_id, 0))
        dead_s2 = to_int(dead_sheet2.get(p_id, dead_s1))
        t4_s2 = to_int(t4_sheet2.get(p_id, 0))
        t5_s2 = to_int(t5_sheet2.get(p_id, 0))
        
        diff_t4_score = t4_s2 - t4_s1
        diff_t5_score = t5_s2 - t5_s1
        diff_kill_score = diff_t4_score + diff_t5_score
        diff_pow = pow_s2 - pow_s1
        
        final_target_kill = get_kpi_kill_value(row['Power_Goc'])
        real_pct_kill = round((diff_kill_score / final_target_kill) * 100, 1) if final_target_kill > 0 else 0.0
        real_pct_dead = round((diff_dead / final_target_dead) * 100, 1) if final_target_dead > 0 else 0.0
        real_pct_total = round((real_pct_kill + real_pct_dead) / 2, 1)
        
        bar_fill_kill = min(100, max(0, int(real_pct_kill)))
        bar_fill_dead = min(100, max(0, int(real_pct_dead)))
        bar_fill_total = min(100, max(0, int(real_pct_total)))
        
        processed_list.append({
            "name": current_name, "id": str(row["ID"]), "alliance": row.get("Liên Minh", "FTD"),
            "diff_pow": diff_pow, "diff_kill": diff_kill_score, "diff_dead": diff_dead,          
            "total_pow": pow_s2, "total_kill": kill_s2, "total_dead": dead_s2,            
            "diff_t4": diff_t4_score, "diff_t5": diff_t5_score,
            "real_pct_kill": real_pct_kill, "real_pct_dead": real_pct_dead, "real_pct_total": real_pct_total,
            "bar_fill_kill": bar_fill_kill, "bar_fill_dead": bar_fill_dead, "bar_fill_total": bar_fill_total,
            "final_kpi_dead": final_target_dead, "final_kpi_kill": final_target_kill
        })
    return processed_list

try:
    final_data = process_cards_data()
except Exception as e:
    st.error(f"Lỗi đồng bộ cấu trúc dữ liệu bảng tính: {e}")
    st.stop()

# DỰNG CARDS HTML
cards_html = ""
for item in final_data:
    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={item['name']}"
    cards_html += f"""
    <div class="card" data-id="{item['id']}" data-power="{item['diff_pow']}" data-kill="{item['diff_kill']}" data-dead="{item['diff_dead']}"
        onclick="openProfile('{item['name']}','{item['id']}','{item['alliance']}',
                             '{item['total_pow']}','{item['total_kill']}','{item['total_dead']}',
                             '{item['diff_kill']}','{item['diff_dead']}',
                             '{item['final_kpi_kill']}','{item['final_kpi_dead']}',
                             '{item['real_pct_kill']}','{item['real_pct_dead']}','{item['real_pct_total']}',
                             '{item['bar_fill_kill']}','{item['bar_fill_dead']}','{item['bar_fill_total']}',
                             '{item['diff_t4']}','{item['diff_t5']}','{avatar}')">
        <div class="avatar-wrap"><img src="{avatar}"></div>
        <div class="card-name">{item['name']}</div>
        <div class="value">⚡ {item['diff_pow']:,}</div>
    </div>
    """

style_css_content = read_file("style.css") if os.path.exists("style.css") else ""
html_template_content = read_file("template.html") if os.path.exists("template.html") else ""

if html_template_content and style_css_content:
    final_html = html_template_content.replace("{style_css}", style_css_content).replace("{cards_html}", cards_html)
    components.html(final_html, height=900, scrolling=True)
else:
    st.error("Thiếu file style.css hoặc template.html!")
