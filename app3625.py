import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ===== 1. CẤU HÌNH FULL MÀN HÌNH =====
st.set_page_config(page_title="FTD KPI SYSTEM", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        #MainMenu, footer, header {visibility: hidden;}
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
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid1 = "855089129"
    gid2 = "316243863"
    
    url1 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid1}"
    url2 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid2}"
    
    df1 = pd.read_csv(url1)
    df2 = pd.read_csv(url2)
    
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    def to_int(x):
        try: return int(str(x).replace(",", ""))
        except: return 0

    # Đồng bộ ID dạng chuỗi text sạch để so khớp chính xác
    df1["ID_str"] = df1["ID"].astype(str).str.strip()
    df2["ID_str"] = df2["ID"].astype(str).str.strip()

    # Tạo các danh mục map từ Sheet 2 theo ID để so sánh đối chiếu
    name_sheet2 = df2.set_index("ID_str")["Tên"].to_dict()
    pow_sheet2 = df2.set_index("ID_str")["Sức Mạnh"].to_dict()
    kill_sheet2 = df2.set_index("ID_str")["Tổng Tiêu Diệt"].to_dict()
    dead_sheet2 = df2.set_index("ID_str")["Điểm Chết"].to_dict()

    # Tính toán các mốc KPI dựa trên dữ liệu nền gốc (Sheet 1)
    df1["Power_Goc"] = df1["Sức Mạnh"].apply(to_int)
    df1['Indiv_KPI_Dead'] = df1['Power_Goc'].apply(get_kpi_dead_value)
    df1['Group'] = df1['Tên'].apply(lambda x: str(x).split()[0].upper() if pd.notnull(x) else "")
    group_kpi_dead_sum = df1.groupby('Group')['Indiv_KPI_Dead'].transform('sum')
    group_max_power = df1.groupby('Group')['Power_Goc'].transform('max')

    processed_list = []
    for i, row in df1.iterrows():
        p_id = row['ID_str']
        is_main = (row['Power_Goc'] == group_max_power[i])
        final_target_dead = group_kpi_dead_sum[i] if is_main else row['Indiv_KPI_Dead']
        final_target_kill = get_kpi_kill_value(row['Power_Goc'])
        
        # Lấy TÊN MỚI NHẤT trong game từ Sheet 2
        current_name = name_sheet2.get(p_id, row["Tên"])
        
        # --- LẤY SỐ LIỆU MỐC BAN ĐẦU (Sheet 1) ---
        pow_s1 = to_int(row["Sức Mạnh"])
        kill_s1 = to_int(row["Tổng Tiêu Diệt"])
        dead_s1 = to_int(row["Điểm Chết"])
        
        # --- LẤY SỐ LIỆU SAU KHI THAY ĐỔI (Sheet 2) ---
        pow_s2 = to_int(pow_sheet2.get(p_id, pow_s1))
        kill_s2 = to_int(kill_sheet2.get(p_id, kill_s1))
        dead_s2 = to_int(dead_sheet2.get(p_id, dead_s1))
        
        # --- TÍNH TOÁN SỐ LIỆU THAY ĐỔI (CHÊNH LỆCH TĂNG THÊM) ---
        # Sử dụng max(0, ...) để tránh số âm nếu có sai sót nhập liệu dữ liệu giảm
        diff_pow = max(0, pow_s2 - pow_s1)
        diff_kill = max(0, kill_s2 - kill_s1)
        diff_dead = max(0, dead_s2 - dead_s1)
        
        # Tính toán % chiều dài thanh fill KPI dựa trên số liệu thay đổi này
        pct_fill_kill = min(100, int((diff_kill / final_target_kill) * 100)) if final_target_kill > 0 else 0
        pct_fill_dead = min(100, int((diff_dead / final_target_dead) * 100)) if final_target_dead > 0 else 0
        
        processed_list.append({
            "name": current_name,
            "id": str(row["ID"]),
            "alliance": row["Liên Minh"],
            
            # Gán hoàn toàn số liệu thay đổi (tăng thêm) vào biến chính để hiển thị ra trang chủ và bộ lọc
            "pow": diff_pow,
            "kill": diff_kill,
            "dead": diff_dead,
            
            # Biến phục vụ thanh progress KPI
            "pct_kill": pct_fill_kill,
            "pct_dead": pct_fill_dead,
            
            "final_kpi_dead": final_target_dead,
            "final_kpi_kill": final_target_kill,
            "is_farm": not is_main
        })
    return processed_list

try:
    final_data = load_and_process_data()
except Exception as e:
    st.error(f"Lỗi đồng bộ dữ liệu thay đổi: {e}")
    st.stop()

# ===== 4. BUILD HTML CARDS =====
cards_html = ""
for item in final_data:
    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={item['name']}"
    # Card hiển thị giá trị mặc định lúc đầu là Sức mạnh tăng thêm (Item['pow'])
    cards_html += f"""
    <div class="card" data-id="{item['id']}" data-power="{item['pow']}" data-kill="{item['kill']}" data-dead="{item['dead']}"
        onclick="openProfile('{item['name']}','{item['id']}','{item['alliance']}','{item['pow']}','{item['kill']}','{item['dead']}','{item['final_kpi_kill']}','{item['final_kpi_dead']}','{item['pct_kill']}','{item['pct_dead']}','{avatar}')">
        <div class="avatar-wrap"><img src="{avatar}"></div>
        <div class="card-name">{item['name']}</div>
        <div class="value">⚡ {item['pow']:,}</div>
    </div>
    """

# ===== 5. GIAO DIỆN HTML/CSS/JS =====
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ background: #05070d; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; }}
        #langBtn {{ position: fixed; top: 15px; right: 15px; background: gold; color: black; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-weight: bold; z-index: 2000; }}
        .avatar-wrap {{
            width: 75px; height: 75px; margin: 0 auto 10px; border-radius: 50%; padding: 3px;
            background: linear-gradient(45deg, #ffd700, #ff8c00);
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
            animation: pulse-gold 2s infinite;
        }}
        @keyframes pulse-gold {{
            0% {{ box-shadow: 0 0 10px rgba(255, 215, 0, 0.4); transform: scale(1); }}
            50% {{ box-shadow: 0 0 25px rgba(255, 215, 0, 0.8); transform: scale(1.03); }}
            100% {{ box-shadow: 0 0 10px rgba(255, 215, 0, 0.4); transform: scale(1); }}
        }}
        .avatar-wrap img {{ width: 100%; height: 100%; border-radius: 50%; background: #111; }}
        .search {{ width: 100%; padding: 12px; background: #111; border: 1px solid #333; color: white; border-radius: 12px; margin-bottom: 15px; box-sizing: border-box; }}
        .filters {{ display: flex; gap: 8px; margin-bottom: 15px; }}
        .filter {{ flex: 1; padding: 10px; background: #222; border-radius: 8px; text-align: center; font-size: 11px; cursor: pointer; border: 1px solid #333; }}
        .filter.active {{ background: gold; color: black; font-weight: bold; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; }}
        .card {{ background: #161b22; padding: 15px; border-radius: 18px; text-align: center; border: 1px solid #222; cursor: pointer; transition: 0.3s; }}
        .card:hover {{ border-color: gold; transform: translateY(-5px); }}
        .card-name {{ font-weight: bold; font-size: 14px; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .value {{ color: gold; font-family: monospace; font-size: 12px; }}
        .modal {{ position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.9); display: none; justify-content: center; align-items: center; z-index: 3000; }}
        .profile-box {{ width: 88%; max-width: 360px; background: #1b1f2e; padding: 25px; border-radius: 25px; border: 1px solid gold; }}
        .stat-row {{ display: flex; gap: 8px; margin: 20px 0; }}
        .stat-card {{ flex: 1; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 12px; text-align: center; font-size: 10px; }}
        .stat-card b {{ font-size: 12px; color: gold; display: block; margin-top: 5px; }}
        .kpi-section {{ font-size: 12px; margin-top: 15px; }}
        .kpi-label {{ display: flex; justify-content: space-between; margin-bottom: 5px; }}
        .bar {{ height: 10px; background: #333; border-radius: 5px; margin-bottom: 12px; overflow: hidden; }}
        .fill {{ height: 100%; background: linear-gradient(90deg, #ffd700, #ff8c00); width: 0%; transition: width 0.4s ease-in-out; }}
        .close-btn {{ width: 100%; padding: 12px; background: #ff4b4b; color: white; border: none; border-radius: 10px; cursor: pointer; margin-top: 15px; font-weight: bold; }}
    </style>
</head>
<body>
    <div id="langBtn">EN</div>
    <input class="search" id="searchInput" placeholder="🔍 Nhập tên hoặc ID..." onkeyup="search(this.value)">
    <div class="filters">
        <div class="filter active" id="fPow" onclick="setMode('power', this)">⚡ SỨC MẠNH TĂNG</div>
        <div class="filter" id="fKill" onclick="setMode('kill', this)">🔥 TIÊU DIỆT TĂNG</div>
        <div class="filter" id="fDead" onclick="setMode('dead', this)">💀 ĐIỂM CHẾT TĂNG</div>
    </div>
    <div class="grid" id="grid">{cards_html}</div>
    <div class="modal" id="modal"><div class="profile-box" id="profileContent"></div></div>

<script>
    let lang = "vn";
    const TEXT = {{
        vn: {{ search: "🔍 Nhập tên hoặc ID...", pow: "⚡ SỨC MẠNH TĂNG", kill: "🔥 TIÊU DIỆT TĂNG", dead: "💀 ĐIỂM CHẾT TĂNG", kK_label: "🔥 KPI Tiêu diệt", kD_label: "💀 KPI Điểm chết", exit: "QUAY LẠI" }},
        en: {{ search: "🔍 Search name or ID...", pow: "⚡ POWER INCREASED", kill: "🔥 KILLS INCREASED", dead: "💀 DEAD INCREASED", kK_label: "🔥 Kills KPI", kD_label: "💀 Dead KPI", exit: "CLOSE" }}
    }};

    document.getElementById("langBtn").onclick = function() {{
        lang = lang === "vn" ? "en" : "vn";
        this.innerText = lang.toUpperCase();
        document.getElementById("searchInput").placeholder = TEXT[lang].search;
        document.getElementById("fPow").innerText = TEXT[lang].pow;
        document.getElementById("fKill").innerText = TEXT[lang].kill;
        document.getElementById("fDead").innerText = TEXT[lang].dead;
    }};

    function search(v) {{
        v = v.toLowerCase();
        document.querySelectorAll('.card').forEach(c => {{
            const name = c.querySelector('.card-name').innerText.toLowerCase();
            const id = c.getAttribute('data-id').toLowerCase();
            if (name.includes(v) || id.includes(v)) {{
                c.style.display = 'block';
            }} else {{
                c.style.display = 'none';
            }}
        }});
    }}

    function setMode(m, el) {{
        document.querySelectorAll('.filter').forEach(f => f.classList.remove('active'));
        el.classList.add('active');
        let grid = document.getElementById('grid');
        let cards = Array.from(grid.getElementsByClassName('card'));
        cards.sort((a,b) => Number(b.dataset[m]) - Number(a.dataset[m]));
        grid.innerHTML = "";
        cards.forEach(c => {{
            let prefix = m === 'power' ? '⚡ ' : (m === 'kill' ? '🔥 ' : '💀 ');
            c.querySelector('.value').innerText = prefix + Number(c.dataset[m]).toLocaleString();
            grid.appendChild(c);
        }});
    }}

    // Hàm nhận dữ liệu hiển thị (Đều đã là số liệu chênh lệch tăng thêm)
    function openProfile(name, id, all, pow, kill, dead, kK, kD, pctK, pctD, avatar) {{
        let t = TEXT[lang];
        document.getElementById('modal').style.display = 'flex';
        document.getElementById('profileContent').innerHTML = `
            <center>
                <div class="avatar-wrap" style="width:70px; height:70px;"><img src="${{avatar}}"></div>
                <h3 style="margin:10px 0 5px 0;">${{name}}</h3>
                <small style="color:#888;">ID: ${{id}} | ${{all}}</small>
            </center>
            <div class="stat-row">
                <div class="stat-card">⚡ SỨC MẠNH TĂNG<br><b>${{Number(pow).toLocaleString()}}</b></div>
                <div class="stat-card">🔥 TIÊU DIỆT TĂNG<br><b>${{Number(kill).toLocaleString()}}</b></div>
                <div class="stat-card">💀 ĐIỂM CHẾT TĂNG<br><b>${{Number(dead).toLocaleString()}}</b></div>
            </div>
            <div class="kpi-section">
                <div class="kpi-label"><span>${{t.kK_label}}</span><span>${{Number(kill).toLocaleString()}} / ${{Number(kK).toLocaleString()}}</span></div>
                <div class="bar"><div class="fill" style="width: ${{pctK}}%;"></div></div>
                
                <div class="kpi-label"><span>${{t.kD_label}}</span><span>${{Number(dead).toLocaleString()}} / ${{Number(kD).toLocaleString()}}</span></div>
                <div class="bar"><div class="fill" style="width: ${{pctD}}%;"></div></div>
            </div>
            <button class="close-btn" onclick="document.getElementById('modal').style.display='none'">${{t.exit}}</button>
        `;
    }}
</script>
</body>
</html>
"""

components.html(html_content, height=1000, scrolling=True)
