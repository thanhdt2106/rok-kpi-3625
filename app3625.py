# app3625.py
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import requests
import os
import json

# ==============================================================================
# 1. KHAI BÁO HÀM ĐỌC FILE
# ==============================================================================
def read_file(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# ==============================================================================
# 2. CẤU HÌNH GIAO DIỆN CHUẨN ĐỒ HỌA HIGH-END UI (ẨN SẠCH TIÊU ĐỀ & HEADER MẶC ĐỊNH)
# ==============================================================================
st.set_page_config(page_title="FTD KPI SYSTEM", layout="wide", initial_sidebar_state="collapsed")

# Inject CSS để diệt tận gốc Header, Thụt lề mặc định, dòng chữ thừa và custom nút bấm Streamlit
st.markdown("""
    <style>
        /* Ẩn triệt để menu bar, footer, viền đen trên đầu và các khoảng trống mặc định của Streamlit */
        #MainMenu, footer, header, [data-testid="stHeader"] {
            visibility: hidden !important;
            display: none !important;
        }
        
        /* Đẩy toàn bộ nội dung sát lên trên, xóa padding thừa thãi */
        .block-container {
            padding-top: 0px !important;
            padding-bottom: 10px !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
            max-width: 100% !important;
        }
        
        iframe {width: 100% !important; border: none;}
        [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"] {display: none !important;}
        
        /* Cố định hộp chọn ngôn ngữ ở góc trên cùng bên phải (đúng vị trí khoanh tím) */
        .lang-fixed-topright {
            position: absolute;
            top: 15px;
            right: 25px;
            width: 90px;
            z-index: 999999;
        }

        /* KHU VỰC BOX WELCOME CINEMA CHUẨN TÂM MÀN HÌNH */
        .welcome-box-outer {
            text-align: center;
            padding: 50px 40px;
            background: linear-gradient(180deg, #1f242c 0%, #0f1319 100%);
            border-radius: 20px;
            border: 1px solid #38444d;
            margin: 8% auto 25px auto;
            max-width: 650px;
            box-shadow: 0 25px 55px rgba(0, 0, 0, 0.85);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        .welcome-box-outer h1 {
            color: #ffaa00; 
            font-size: 34px; 
            font-weight: 800;
            letter-spacing: 1.5px; 
            margin-bottom: 5px;
            text-shadow: 0 0 25px rgba(255, 170, 0, 0.3);
        }

        .welcome-box-outer p {
            color: #8b949e; 
            font-size: 15px; 
            font-weight: 500;
            letter-spacing: 0.5px;
        }

        /* KHU VỰC CHỨA BỘ NÚT BẤM CỦA STREAMLIT NẰM GỌN TRONG FORM */
        .buttons-wrapper-inside {
            max-width: 650px;
            margin: 0 auto;
            padding: 0 40px;
        }

        /* TRIỆT TIÊU TOÀN BỘ VIỀN XÁM, THIẾT KẾ ĐẬM CHẤT GAMING CHO NÚT STREAMLIT */
        div[data-testid="stBlock"] button[key="btn_member_key"],
        div[data-testid="stBlock"] button[key="btn_admin_key"] {
            border: none !important;
            outline: none !important;
            padding: 16px 30px !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            border-radius: 12px !important;
            width: 100% !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            box-shadow: 0 5px 20px rgba(0,0,0,0.5) !important;
            min-height: 55px !important;
        }

        /* NÚT BẤM MEMBER: GRADIENT XANH ĐẬM HIGH-TECH */
        div[data-testid="stBlock"] button[key="btn_member_key"] {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
            color: #38bdf8 !important;
        }
        div[data-testid="stBlock"] button[key="btn_member_key"]:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 0 28px rgba(37, 99, 235, 0.65) !important;
            transform: translateY(-3px) !important;
        }

        /* NÚT BẤM ADMIN: GRADIENT VÀNG HỔ PHÁCH RỰC RỠ */
        div[data-testid="stBlock"] button[key="btn_admin_key"] {
            background: linear-gradient(135deg, #ffaa00 0%, #d97706 100%) !important;
            color: #0d1117 !important;
        }
        div[data-testid="stBlock"] button[key="btn_admin_key"]:hover {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
            color: #000000 !important;
            box-shadow: 0 0 28px rgba(245, 158, 11, 0.65) !important;
            transform: translateY(-3px) !important;
        }
    </style>
""", unsafe_allow_html=True)

SHEET_ID = "15CrOFNFsIno34mX0EuXkLKdwiJgn3rrmcM-sEKmoKUQ"
GID1 = "0"
GID2 = "1325084102"

# ==============================================================================
# 3. KHỞI TẠO TRẠNG THÁI & TỪ ĐIỂN NGÔN NGỮ NGƯỜI DÙNG
# ==============================================================================
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "👋 CHÀO MỪNG"

if "is_admin_verified" not in st.session_state:
    st.session_state["is_admin_verified"] = False

if "lang" not in st.session_state:
    st.session_state["lang"] = "VN"

if "selected_sheet_index" not in st.session_state:
    st.session_state["selected_sheet_index"] = 0

lang_dict = {
    "VN": {
        "title": "FTD KPI SYSTEM",
        "select_role": "VUI LÒNG CHỌN VAI TRÒ ĐỂ TRUY CẬP HỆ THỐNG",
        "btn_member": "👤 BẠN LÀ MEMBER",
        "btn_admin": "🛡️ QUẢN TRỊ ADMIN",
        "admin_title": "🛡️ KHU VỰC QUẢN TRỊ VIÊN",
        "pass_placeholder": "Nhập mật khẩu Admin để mở khóa hệ thống...",
        "pass_label": "Mật khẩu Admin:",
        "login_success": "🔓 Xác thực thành công!",
        "login_fail": "❌ Mật khẩu không chính xác!",
        "select_sheet": "Chọn bảng tính cần thao tác:",
        "edit_title": "📝 Chỉnh sửa dữ liệu trực tiếp tab:",
        "save_btn": "💾 XÁC NHẬN LƯU VÀ ĐỒNG BỘ LÊN GOOGLE SHEETS",
        "syncing": "🚀 Đang tiến hành đồng bộ hóa lên Google Sheets...",
        "sync_success": "Thành công",
        "sync_fail": "Thất bại từ hệ thống Sheets",
        "conn_error": "Lỗi kết nối API Web App",
        "menu_view_kpi": "📊 Chuyển sang Xem KPI",
        "menu_logout": "↩️ Đăng xuất / Về màn hình chính",
        "menu_back_admin": "⚙️ Quay lại trang Setting Admin",
        "view_title_admin": "### 📊 CHẾ ĐỘ XEM TRƯỚC KPI THÀNH VIÊN",
        "view_title_member": "### 📊 TRA CỨU KPI THÀNH VIÊN CORES",
        "btn_back_welcome": "↩️ Quay lại Trang Đầu",
        "sheet_err": "Lỗi đồng bộ cấu trúc dữ liệu bảng tính:",
        "file_err": "Hệ thống không tìm thấy file style.css hoặc template.html tại thư mục gốc GitHub!",
        "tip": "💡 Mẹo: Bạn có thể click đúp vào ô để sửa số liệu, hoặc kéo thả, thêm hàng ở dưới bảng."
    },
    "EN": {
        "title": "FTD KPI SYSTEM",
        "select_role": "PLEASE SELECT YOUR ROLE TO ACCESS THE SYSTEM",
        "btn_member": "👤 I AM A MEMBER",
        "btn_admin": "🛡️ ADMIN DASHBOARD",
        "admin_title": "🛡️ ADMINISTRATOR PANEL",
        "pass_placeholder": "Enter Admin password to unlock system...",
        "pass_label": "Admin Password:",
        "login_success": "🔓 Verification successful!",
        "login_fail": "❌ Incorrect password!",
        "select_sheet": "Select worksheet to manage:",
        "edit_title": "📝 Direct data editor tab:",
        "save_btn": "💾 CONFIRM SAVE AND SYNC TO GOOGLE SHEETS",
        "syncing": "🚀 Synchronizing data to Google Sheets...",
        "sync_success": "Success",
        "sync_fail": "Failed from Sheets system",
        "conn_error": "Web App API Connection Error",
        "menu_view_kpi": "📊 Switch to KPI View",
        "menu_logout": "↩️ Logout / Home Screen",
        "menu_back_admin": "⚙️ Back to Admin Settings",
        "view_title_admin": "### 📊 MEMBERS KPI PREVIEW MODE",
        "view_title_member": "### 📊 CORES MEMBER KPI LOOKUP",
        "btn_back_welcome": "↩️ Back to Home",
        "sheet_err": "Worksheet structural synchronization error:",
        "file_err": "System missing style.css or template.html in GitHub root!",
        "tip": "💡 Tip: Double-click cells to edit data, drag-and-drop, or append new rows at the bottom."
    }
}

T = lang_dict[st.session_state["lang"]]

def load_csv_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    df = pd.read_csv(url, dtype=str)
    df.columns = df.columns.str.strip()
    return df

def get_kpi_kill_value(p):
    try: p = int(p)
    except: p = 0
    if p >= 100_000_000: return 600_000_000
    elif p >= 80_000_000: return 450_000_000
    return 300_000_000

def get_kpi_dead_value(p):
    try: p = int(p)
    except: p = 0
    if p >= 100_000_000: return 1_500_000
    elif p >= 90_000_000: return 1_200_000
    elif p >= 80_000_000: return 1_000_000
    elif p >= 70_000_000: return 800_000
    elif p >= 60_000_000: return 700_000
    elif p >= 50_000_000: return 600_000
    elif p >= 40_000_000: return 500_000
    elif p >= 30_000_000: return 400_000
    else: return 300_000

def on_sheet_change():
    if "Bảng 1" in st.session_state["sheet_select_key"] or "Base KPI" in st.session_state["sheet_select_key"]:
        st.session_state["selected_sheet_index"] = 0
    else:
        st.session_state["selected_sheet_index"] = 1

# ==============================================================================
# 4. ĐIỀU HƯỚNG GIAO DIỆN CHÍNH
# ==============================================================================

# ─── TRANG 1: MÀN HÌNH CHÀO MỪNG (SẠCH BÓNG RÁC, CHỈ CÒN ĐÚNG KHU VỰC CHỌN VÀ FORM) ───
if st.session_state["current_page"] == "👋 CHÀO MỪNG":
    # 1. Đặt hộp chọn ngôn ngữ nằm biệt lập ở góc trên bên phải trang web
    st.markdown('<div class="lang-fixed-topright">', unsafe_allow_html=True)
    lang_choice = st.selectbox("🌐", ["VN", "EN"], index=0 if st.session_state["lang"] == "VN" else 1, label_visibility="collapsed")
    if lang_choice != st.session_state["lang"]:
        st.session_state["lang"] = lang_choice
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Tạo Box Cinema bằng HTML thuần
    st.markdown(f"""
        <div class="welcome-box-outer">
            <h1>{T['title']}</h1>
            <div style="height: 2px; background: linear-gradient(90deg, transparent, #ffaa00, transparent); max-width: 380px; margin: 20px auto;"></div>
            <p>{T['select_role']}</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. Chèn 2 nút bấm Streamlit thật xịn nằm ngay dưới khung (Được style đè không viền hoàn toàn)
    st.markdown('<div class="buttons-wrapper-inside">', unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        if st.button(T['btn_member'], key="btn_member_key", use_container_width=True):
            st.session_state["current_page"] = "📊 TRANG CHỦ KPI"
            st.rerun()
            
    with btn_col2:
        if st.button(T['btn_admin'], key="btn_admin_key", use_container_width=True):
            st.session_state["current_page"] = "⚙️ QUẢN TRỊ ADMIN"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ─── TRANG 2: TRANG CHỈNH SỬA ADMIN ───
elif st.session_state["current_page"] == "⚙️ QUẢN TRỊ ADMIN":
    # Thanh điều hướng riêng biệt bên trong trang Admin
    st.markdown('<div style="background: linear-gradient(135deg, #161b22 0%, #0d1117 100%); padding: 15px 25px; border-radius: 12px; border: 1px solid #30363d; margin: 15px 15px 25px 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">', unsafe_allow_html=True)
    m_col1, m_col2, m_col3, m_col4 = st.columns([3.5, 2, 2.5, 2])
    with m_col1: 
        st.markdown(f"### {T['admin_title']}")
    with m_col2:
        if st.button(T["menu_view_kpi"], use_container_width=True):
            st.session_state["current_page"] = "📊 TRANG CHỦ KPI"
            st.rerun()
    with m_col3:
        if st.button(T["menu_logout"], use_container_width=True):
            st.session_state["is_admin_verified"] = False
            st.session_state["current_page"] = "👋 CHÀO MỪNG"
            st.rerun()
    with m_col4:
        lang_choice = st.selectbox("🌐", ["VN", "EN"], index=0 if st.session_state["lang"] == "VN" else 1, label_visibility="collapsed")
        if lang_choice != st.session_state["lang"]:
            st.session_state["lang"] = lang_choice
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if not st.session_state["is_admin_verified"]:
        st.markdown('<div style="padding: 0 15px;">', unsafe_allow_html=True)
        admin_password = st.text_input(T["pass_label"], type="password", placeholder=T["pass_placeholder"])
        if admin_password:
            try: target_pass = st.secrets["admin"]["password"]
            except KeyError:
                target_pass = "123"
                st.warning("⚠️ Chưa phát hiện cấu hình Secrets trên Cloud. Đang dùng pass tạm: 123")

            if admin_password == target_pass:
                st.session_state["is_admin_verified"] = True
                st.success(T["login_success"])
                st.rerun()
            else:
                st.error(T["login_fail"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state["is_admin_verified"]:
        st.markdown('<div style="padding: 0 15px;">', unsafe_allow_html=True)
        sheet_options = [
            "Bảng 1: KPI Gốc (0)" if st.session_state["lang"] == "VN" else "Table 1: Base KPI (0)", 
            "Bảng 2: Cập Nhật Mới (1325084102)" if st.session_state["lang"] == "VN" else "Table 2: New Update (1325084102)"
        ]
        
        st.selectbox(
            T["select_sheet"], 
            sheet_options, 
            index=st.session_state["selected_sheet_index"],
            key="sheet_select_key",
            on_change=on_sheet_change
        )
        
        if st.session_state["selected_sheet_index"] == 0:
            target_gid = GID1
            worksheet_name = "Sheet1"  
        else:
            target_gid = GID2
            worksheet_name = "Sheet2"  
            
        df_to_edit = load_csv_data(target_gid)
        
        st.markdown(f"#### {T['edit_title']} `{worksheet_name}`")
        st.info(T["tip"])
        edited_df = st.data_editor(df_to_edit, num_rows="dynamic", use_container_width=True)
        
        if st.button(T["save_btn"]):
            header = edited_df.columns.tolist()
            matrix_data = [header] + edited_df.fillna("").values.tolist()
            payload = {"worksheet": worksheet_name, "data": matrix_data}
            
            with st.spinner(T["syncing"]):
                try:
                    try: app_url = st.secrets["api"]["app_url"]
                    except KeyError: app_url = ""
                    response = requests.post(app_url, json=payload)
                    res_json = response.json()
                    
                    if res_json.get("status") == "success":
                        st.balloons()
                        st.success(f"{T['sync_success']}: {res_json.get('message')}")
                        st.cache_data.clear()
                    else:
                        st.error(f"{T['sync_fail']}: {res_json.get('message')}")
                except Exception as e:
                    st.error(f"{T['conn_error']}: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ─── TRANG 3: TRANG CHỦ XEM CARDS KPI CỦA THÀNH VIÊN ───
elif st.session_state["current_page"] == "📊 TRANG CHỦ KPI":
    if st.session_state["is_admin_verified"]:
        st.markdown('<div style="background: linear-gradient(135deg, #161b22 0%, #0d1117 100%); padding: 15px 25px; border-radius: 12px; border: 1px solid #30363d; margin: 15px 15px 25px 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">', unsafe_allow_html=True)
        u_col1, u_col2, u_col3 = st.columns([6, 2, 1])
        with u_col1: st.markdown(T["view_title_admin"])
        with u_col2:
            if st.button(T["menu_back_admin"], use_container_width=True, type="primary"):
                st.session_state["current_page"] = "⚙️ QUẢN TRỊ ADMIN"
                st.rerun()
        with u_col3:
            lang_choice = st.selectbox("🌐", ["VN", "EN"], index=0 if st.session_state["lang"] == "VN" else 1, label_visibility="collapsed")
            if lang_choice != st.session_state["lang"]:
                st.session_state["lang"] = lang_choice
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: linear-gradient(135deg, #161b22 0%, #0d1117 100%); padding: 15px 25px; border-radius: 12px; border: 1px solid #30363d; margin: 15px 15px 25px 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">', unsafe_allow_html=True)
        m_c1, m_c2, m_c3 = st.columns([6, 2, 1])
        with m_c1: st.markdown(T["view_title_member"])
        with m_c2:
            if st.button(T["btn_back_welcome"], use_container_width=True):
                st.session_state["current_page"] = "👋 CHÀO MỪNG"
                st.rerun()
        with m_c3:
            lang_choice = st.selectbox("🌐", ["VN", "EN"], index=0 if st.session_state["lang"] == "VN" else 1, label_visibility="collapsed")
            if lang_choice != st.session_state["lang"]:
                st.session_state["lang"] = lang_choice
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

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

    try: final_data = process_cards_data()
    except Exception as e:
        st.error(f"{T['sheet_err']} {e}")
        st.stop()

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
        st.markdown('<div style="padding: 0 15px;">', unsafe_allow_html=True)
        components.html(final_html, height=900, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(T["file_err"])
