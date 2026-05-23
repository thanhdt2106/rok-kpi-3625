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

    # Chuyển ID sang string và xóa khoảng trắng để map chính xác tuyệt đối
    df1["ID_str"] = df1["ID"].astype(str).str.strip()
    df2["ID_str"] = df2["ID"].astype(str).str.strip()

    # Tạo từ điển lưu dữ liệu mới từ Sheet 2 phục vụ phép trừ
    kill_sheet2 = df2.set_index("ID_str")["Tổng Tiêu Diệt"].to_dict()
    dead_sheet2 = df2.set_index("ID_str")["Điểm Chết"].to_dict()

    # Các logic tính toán cơ bản dựa theo dữ liệu nền (Sức mạnh nền ở Sheet 1)
    df1["Power"] = df1["Sức Mạnh"].apply(to_int)
    df1['Indiv_KPI_Dead'] = df1['Power'].apply(get_kpi_dead_value)
    df1['Group'] = df1['Tên'].apply(lambda x: str(x).split()[0].upper() if pd.notnull(x) else "")
    group_kpi_dead_sum = df1.groupby('Group')['Indiv_KPI_Dead'].transform('sum')
    group_max_power = df1.groupby('Group')['Power'].transform('max')

    processed_list = []
    for i, row in df1.iterrows():
        p_id = row['ID_str']
        is_main = (row['Power'] == group_max_power[i])
        final_target_dead = group_kpi_dead_sum[i] if is_main else row['Indiv_KPI_Dead']
        final_target_kill = get_kpi_kill_value(row['Power'])
        
        # Số liệu gốc tại trận (Sheet 1)
        kill_s1 = to_int(row["Tổng Tiêu Diệt"])
        dead_s1 = to_int(row["Điểm Chết"])
        
        # Số liệu mới nhất sau khi tăng (Sheet 2)
        kill_s2 = to_int(kill_sheet2.get(p_id, kill_s1))
        dead_s2 = to_int(dead_sheet2.get(p_id, dead_s1))
        
        # Lấy hiệu số: Dữ liệu thực tế tăng thêm = Sheet 2 - Sheet 1
        increased_kill = max(0, kill_s2 - kill_s1)
        increased_dead = max(0, dead_s2 - dead_s1)
        
        processed_list.append({
            "name": row["Tên"],
            "id": str(row["ID"]),
            "alliance": row["Liên Minh"],
            "pow": row["Power"],
            "kill": increased_kill, # Đưa lượng dữ liệu tăng thêm lên Web
            "dead": increased_dead, # Đưa lượng dữ liệu tăng thêm lên Web
            "final_kpi_dead": final_target_dead,
            "final_kpi_kill": final_target_kill,
            "is_farm": not is_main
        })
    return processed_list

try:
    final_data = load_and_process_data()
except Exception as e:
    st.error(f"Lỗi xử lý dữ liệu tăng trưởng: {e}")
    st.stop()

# ===== 4. BUILD HTML CARDS =====
cards_html = ""
for item in final_data:
    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={item['name']}"
    cards_html += f"""
    <div class="card" data-id="{item['id']}" data-power="{item['pow']}" data-kill="{item['kill']}" data-dead="{item['dead']}"
        onclick="openProfile('{item['name']}','{item['id']}','{item['alliance']}','{item['pow']}','{item['kill']}','{item['dead']}','{item['final_kpi_kill']}','{item['final_kpi_dead']}','{avatar}')">
        <div class="avatar-wrap"><img src="{avatar}"></div>
        <div class="card-name">{item['name']}</div>
        <div class="value">⚡ {item['pow']:,}</div>
    </div>
    """

# ===== 5. GIAO DIỆN HTML/CSS/JS (GIỮ NGUYÊN HOÀN TOÀN) =====
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
        .fill {{ height: 100%; background: linear-gradient(90deg, gold, orange); width: 0%; }}
        .close-btn {{ width: 100%; padding: 12px; background: #ff4b4b; color: white; border: none; border-radius: 10px; cursor: pointer; margin-top: 15px; font-weight: bold; }}
    </style>
</head>
<body>
    <div id="langBtn">EN</div>
    <input class="search" id="searchInput" placeholder="🔍 Nhập tên hoặc ID..." onkeyup="search(this.value)">
    <div class="filters">
        <div class="filter active" id="fPow" onclick="setMode('power', this)">⚡ SỨC MẠNH</div>
        <div class="filter" id="fKill" onclick="setMode('kill', this)">🔥 TIÊU DIỆT</div>
        <div class="filter" id="fDead" onclick="setMode('dead', this)">💀 ĐIỂM CHẾT</div>
    </div>
    <div class="grid" id="grid">{cards_html}</div>
    <div class="modal" id="modal"><div class="profile-box" id="profileContent"></div></div>

<script>
    let lang = "vn";
    const TEXT = {{
        vn: {{ search: "🔍 Nhập tên hoặc ID...", pow: "⚡ SỨC MẠNH", kill: "🔥 TIÊU DIỆT", dead: "💀 ĐIỂM CHẾT", kK_label: "🔥 KPI Tiêu diệt", kD_label: "💀 KPI Điểm chết", exit: "QUAY LẠI" }},
        en: {{ search: "🔍 Search name or ID...", pow: "⚡ POWER", kill: "🔥 KILLS", dead: "💀 DEAD", kK_label: "🔥 Kills KPI", kD_label: "💀 Dead KPI", exit: "CLOSE" }}
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

    function openProfile(name, id, all, pow, kill, dead, kK, kD, avatar) {{
        let t = TEXT[lang];
        document.getElementById('modal').style.display = 'flex';
        document.getElementById('profileContent').innerHTML = `
            <center>
                <div class="avatar-wrap" style="width:70px; height:70px;"><img src="${{avatar}}"></div>
                <h3 style="margin:10px 0 5px 0;">${{name}}</h3>
                <small style="color:#888;">ID: ${{id}} | ${{all}}</small>
            </center>
            <div class="stat-row">
                <div class="stat-card">⚡ POWER<br><b>${{Number(pow).toLocaleString()}}</b></div>
                <div class="stat-card">🔥 KILL<br><b>${{Number(kill).toLocaleString()}}</b></div>
                <div class="stat-card">💀 DEAD<br><b>${{Number(dead).toLocaleString()}}</b></div>
            </div>
            <div class="kpi-section">
                <div class="kpi-label"><span>${{t.kK_label}}</span><span>0 / ${{Number(kK).toLocaleString()}}</span></div>
                <div class="bar"><div class="fill"></div></div>
                <div class="kpi-label"><span>${{t.kD_label}}</span><span>0 / ${{Number(kD).toLocaleString()}}</span></div>
                <div class="bar"><div class="fill"></div></div>
            </div>
            <button class="close-btn" onclick="document.getElementById('modal').style.display='none'">${{t.exit}}</button>
        `;
    }}
</script>
</body>
</html>
"""

components.html(html_content, height=1000, scrolling=True)
