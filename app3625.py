# app3625.py
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import requests
import os

# ==============================================================================
# 1. CẤU HÌNH GIAO DIỆN CHUẨN ĐỒ HỌA FULL SCREEN
# ==============================================================================
st.set_page_config(page_title="FTD KPI SYSTEM", layout="wide", initial_sidebar_state="collapsed")

# Inject CSS ẩn hoàn toàn thanh Sidebar và làm đẹp các khung container
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 10px !important; max-width: 100% !important;}
        iframe {width: 100% !important; border: none;}
        
        /* Ẩn triệt để Sidebar mặc định của Streamlit */
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stSidebarCollapseButton"] {display: none !important;}
        
        /* Định dạng khung Welcome Page & Menu */
        .welcome-box {
            text-align: center;
            padding: 40px;
            background-color: #0d1117;
            border-radius: 12px;
            border: 1px solid #21262d;
            margin: 10% auto;
            max-width: 600px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
        .menu-container {
            background-color: #0d1117;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #21262d;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ─── THÔNG TIN GOOGLE SHEETS ───
SHEET_ID = "15CrOFNFsIno34mX0EuXkLKdwiJgn3rrmcM-sEKmoKUQ"
GID1 = "0"
GID2 = "1325084102"

# ==============================================================================
# 2. ĐỊNH NGHĨA CÁC HÀM BỔ TRỢ
# ==============================================================================
def read_file(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def load_csv_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    df = pd.read_csv(url, dtype=str)
    df.columns = df.columns.str.strip()
    return df

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

# Khởi tạo trạng thái trang mặc định khi vừa truy cập là trang Chào Mừng
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "👋 CHÀO MỪNG"

# Khởi tạo quyền Admin
if "is_admin_verified" not in st.session_state:
    st.session_state["is_admin_verified"] = False


# ==============================================================================
# 3. ĐIỀU HƯỚNG GIAO DIỆN THEO LỰA CHỌN
# ==============================================================================

# ─── TRANG 1: TRANG CHÀO MỪNG CHÍNH (WELCOME PAGE) ───
if st.session_state["current_page"] == "👋 CHÀO MỪNG":
    st.markdown("""
        <div class="welcome-box">
            <h1 style='color: #ffaa00; margin-bottom: 10px;'>👋 WELCOME</h1>
            <h3 style='color: #ffffff; margin-bottom: 30px;'>Chào mừng đến với Hệ thống DKP / KPI của Vương Quốc 3625</h3>
            <p style='color: #8b949e; margin-bottom: 40px;'>Vui lòng lựa chọn vai trò của bạn để tiếp tục truy cập hệ thống:</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tạo 2 cột nút bấm lớn ở giữa màn hình chào mừng
    w_col1, w_col2 = st.columns(2)
    with w_col1:
        if st.button("👤 Bạn là Member", use_container_width=True, type="secondary"):
            st.session_state["current_page"] = "📊 TRANG CHỦ KPI"
            st.rerun()
            
    with w_col2:
        if st.button("🛡️ Bạn là ADMIN ?", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "⚙️ QUẢN TRỊ ADMIN"
            st.rerun()

# ─── TRANG 2: TRANG CHỈNH SỬA ADMIN ───
elif st.session_state["current_page"] == "⚙️ QUẢN TRỊ ADMIN":
    # Menu ngang cho phép Admin chuyển đổi qua lại nhanh giữa 2 trang
    st.markdown('<div class="menu-container">', unsafe_allow_html=True)
    m_col1, m_col2, m_col3 = st.columns([5, 2, 2])
    with m_col1: st.markdown("### ⚙️ BAN QUẢN TRỊ ADMIN")
    with m_col2:
        if st.button("📊 Chuyển sang Xem KPI", use_container_width=True):
            st.session_state["current_page"] = "📊 TRANG CHỦ KPI"
            st.rerun()
    with m_col3:
        if st.button("↩️ Đăng xuất / Về màn hình chính", use_container_width=True):
            st.session_state["is_admin_verified"] = False
            st.session_state["current_page"] = "👋 CHÀO MỪNG"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Nếu chưa xác thực mật khẩu thì bắt nhập mật khẩu trước
    if not st.session_state["is_admin_verified"]:
        admin_password = st.text_input("Nhập mật khẩu Admin để mở khóa hệ thống:", type="password", placeholder="••••••••")
        if admin_password:
            if admin_password == st.secrets["admin"]["password"]:
                st.session_state["is_admin_verified"] = True
                st.success("🔓 Xác thực thành công!")
                st.rerun()
            else:
                st.error("❌ Mật khẩu không chính xác!")
    
    # Khi đã xác thực mật khẩu thành công, mở toàn bộ bảng sửa dữ liệu
    if st.session_state["is_admin_verified"]:
        sheet_option = st.selectbox("Chọn bảng tính cần thao tác:", [
            "Bảng 1: KPI Gốc (0)", 
            "Bảng 2: Cập Nhật Mới (1325084102)"
        ])
        
        if "Bảng 1" in sheet_option:
            target_gid = GID1
            worksheet_name = "Sheet1"  
        else:
            target_gid = GID2
            worksheet_name = "Sheet2"  
            
        df_to_edit = load_csv_data(target_gid)
        
        st.markdown(f"#### 📝 Chỉnh sửa dữ liệu trực tiếp tab: `{worksheet_name}`")
        edited_df = st.data_editor(df_to_edit, num_rows="dynamic", use_container_width=True)
        
        if st.button("💾 XÁC NHẬN LƯU VÀ ĐỒNG BỘ LÊN GOOGLE SHEETS"):
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
                        st.cache_data.clear()
                    else:
                        st.error(f"Thất bại từ hệ thống Sheets: {res_json.get('message')}")
                except Exception as e:
                    st.error(f"Lỗi kết nối API Web App: {e}")

# ─── TRANG 3: TRANG CHỦ XEM CARDS KPI CỦA THÀNH VIÊN ───
elif st.session_state["current_page"] == "📊 TRANG CHỦ KPI":
    # Nếu là Admin đang đứng ở trang xem KPI, hiện thanh Menu ngang để quay lại Setting
    if st.session_state["is_admin_verified"]:
        st.markdown('<div class="menu-container">', unsafe_allow_html=True)
        u_col1, u_col2 = st.columns([7, 2])
        with u_col1: st.markdown("### 📊 CHẾ ĐỘ XEM TRƯỚC KPI THÀNH VIÊN")
        with u_col2:
            if st.button("⚙️ Quay lại trang Setting Admin", use_container_width=True, type="primary"):
                st.session_state["current_page"] = "⚙️ QUẢN TRỊ ADMIN"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Nếu là Member thường, hiện nút nhỏ ở góc trên để quay lại trang chào mừng nếu muốn
        m_c1, m_c2 = st.columns([7, 2])
        with m_c1: st.markdown("### 📊 TRA CỨU KPI THÀNH VIÊN CORES")
        with m_c2:
            if st.button("↩️ Quay lại Trang Đầu", use_container_width=True):
                st.session_state["current_page"] = "👋 CHÀO MỪNG"
                st.rerun()

    # Thao tác xử lý và tính toán Cards Data
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

    # DỰNG THẺ CARDS HTML
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

    style_css_content = read_file("style.css")
    html_template_content = read_file("template.html")

    if html_template_content and style_css_content:
        final_html = html_template_content.replace("{style_css}", style_css_content).replace("{cards_html}", cards_html)
        components.html(final_html, height=900, scrolling=True)
    else:
        st.error("Hệ thống không tìm thấy file style.css hoặc template.html tại thư mục gốc GitHub!")
