# app.py
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os

# ===== 1. CẤU HÌNH FULL MÀN HÌNH =====
st.set_page_config(page_title="FTD KPI SYSTEM", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        #MainMenu, footer, header {visibility: hidden;}
        iframe {width: 100% !important; border: none;}
    </style>
""", unsafe_allow_html=True)

# ===== 2. KPI RULES =====
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

# ===== 3. LOAD VÀ XỬ LÝ DỮ LIỆU =====
@st.cache_data(ttl=60)
def load_and_process_data():
    sheet_id = "15CrOFNFsIno34mX0EuXkLKdwiJgn3rrmcM-sEKmoKUQ"
    gid1 = "0"
    gid2 = "1325084102"
    
    url1 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid1}"
    url2 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid2}"
    
    df1 = pd.read_csv(url1)
    df2 = pd.read_csv(url2)
    
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

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
    
    col_t4 = "T4"
    col_t5 = "T5"

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
            "name": current_name,
            "id": str(row["ID"]),
            "alliance": row.get("Liên Minh", "FTD"),
            "diff_pow": diff_pow,
            "diff_kill": diff_kill_score, 
            "diff_dead": diff_dead,          
            "total_pow": pow_s2,
            "total_kill": kill_s2, 
            "total_dead": dead_s2,            
            "diff_t4": diff_t4_score,
            "diff_t5": diff_t5_score,
            "real_pct_kill": real_pct_kill,
            "real_pct_dead": real_pct_dead,
            "real_pct_total": real_pct_total,
            "bar_fill_kill": bar_fill_kill,
            "bar_fill_dead": bar_fill_dead,
            "bar_fill_total": bar_fill_total,
            "final_kpi_dead": final_target_dead,
            "final_kpi_kill": final_target_kill
        })
    return processed_list

try:
    final_data = load_and_process_data()
except Exception as e:
    st.error(f"Lỗi đồng bộ cấu trúc dữ liệu bảng tính: {e}")
    st.stop()

# ===== 4. DỰNG HTML CARDS DỰA TRÊN DATA =====
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

# ===== 5. ĐỌC FILE TÀI NGUYÊN GIAO DIỆN =====
def read_file(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    return ""

style_css_content = read_file("style.css")
html_template_content = read_file("template.html")

# Trộn dữ liệu vào khung xương HTML
if html_template_content and style_css_content:
    final_html = html_template_content.replace("{style_css}", style_css_content).replace("{cards_html}", cards_html)
else:
    st.error("Không tìm thấy tệp cấu hình giao diện `style.css` hoặc `template.html`!")
    st.stop()

# Hiển thị tích hợp Component lên Streamlit
components.html(final_html, height=900, scrolling=True)
