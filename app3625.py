import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="FTD KPI SYSTEM", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 2. LOAD VÀ XỬ LÝ DỮ LIỆU
@st.cache_data(ttl=60)
def get_processed_data():
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid = "855089129"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    df_raw = pd.read_csv(url)
    df_raw.columns = df_raw.columns.str.strip()

    def to_int(x):
        try: return int(str(x).replace(",", ""))
        except: return 0

    # Chuyển đổi số liệu
    data_list = []
    for _, row in df_raw.iterrows():
        data_list.append({
            "Tên": str(row.get("Tên", "")),
            "ID": str(row.get("ID", "")),
            "Liên Minh": str(row.get("Liên Minh", "")),
            "Power": to_int(row.get("Sức Mạnh", 0)),
            "Kill": to_int(row.get("Tổng Tiêu Diệt", 0)),
            "Dead": to_int(row.get("Điểm Chết", 0))
        })

    # LOGIC GỘP: Dùng Dictionary để gom nhóm theo từ đầu tiên của tên
    merged = {}
    for item in data_list:
        name = item["Tên"]
        # Lấy từ đầu tiên làm gốc (Ví dụ: "Louis 1" -> "louis")
        root = name.split()[0].lower() if name.split() else name.lower()
        
        if root not in merged:
            merged[root] = item
        else:
            # Nếu Power thằng mới to hơn, lấy thằng mới làm acc chính
            if item["Power"] > merged[root]["Power"]:
                old_dead = merged[root]["Dead"]
                merged[root] = item
                merged[root]["Dead"] += old_dead # Gộp Dead cũ vào acc mới to hơn
            else:
                # Nếu thằng mới là acc phụ, cộng dồn Dead vào acc chính hiện tại
                merged[root]["Dead"] += item["Dead"]
    
    return list(merged.values())

# Thực thi lấy dữ liệu
try:
    final_data = get_processed_data()
except Exception as e:
    st.error(f"Lỗi kết nối dữ liệu: {e}")
    st.stop()

# 3. KPI RULES
def kpi_kill(pow):
    if pow >= 100_000_000: return 600_000_000
    elif pow >= 90_000_000: return 550_000_000
    elif pow >= 80_000_000: return 450_000_000
    else: return 300_000_000

def kpi_dead(pow):
    if pow >= 100_000_000: return 1_500_000
    elif pow >= 80_000_000: return 1_000_000
    else: return 800_000

# 4. TẠO DANH SÁCH THẺ (CARDS)
cards_html = ""
for row in final_data:
    name, id_, alliance = row["Tên"], row["ID"], row["Liên Minh"]
    power, kill, dead = row["Power"], row["Kill"], row["Dead"]
    kK, kD = kpi_kill(power), kpi_dead(power)
    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={name}"

    cards_html += f"""
    <div class="card" data-power="{power}" data-kill="{kill}" data-dead="{dead}"
        onclick="openProfile('{name}','{id_}','{alliance}','{power}','{kill}','{dead}','{kK}','{kD}','{avatar}')">
        <div class="avatar-wrap"><img src="{avatar}"></div>
        <div class="card-name">{name}</div>
        <div class="value">{power:,}</div>
    </div>
    """

# 5. GIAO DIỆN HTML/CSS/JS
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ background: #05070d; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; }}
        #langBtn {{ position: fixed; top: 15px; right: 15px; background: gold; color: black; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-weight: bold; z-index: 100; }}
        
        .avatar-wrap {{
            width: 70px; height: 70px; margin: 0 auto 10px; border-radius: 50%; padding: 3px;
            background: linear-gradient(45deg, #ffd700, #ff8c00);
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{ 0% {{opacity:0.8}} 50% {{opacity:1; box-shadow: 0 0 25px gold;}} 100% {{opacity:0.8}} }}
        .avatar-wrap img {{ width: 100%; height: 100%; border-radius: 50%; background: #111; }}

        .search {{ width: 100%; padding: 12px; background: #111; border: 1px solid #333; color: white; border-radius: 10px; margin-bottom: 15px; box-sizing: border-box; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; }}
        .card {{ background: #161b22; padding: 15px; border-radius: 15px; text-align: center; border: 1px solid #222; cursor: pointer; }}
        .card-name {{ font-weight: bold; font-size: 14px; margin-bottom: 5px; white-space: nowrap; overflow: hidden; }}
        .value {{ color: gold; font-family: monospace; font-size: 13px; }}

        .filters {{ display: flex; gap: 5px; margin-bottom: 15px; }}
        .filter {{ flex: 1; padding: 8px; background: #222; border-radius: 6px; text-align: center; font-size: 12px; cursor: pointer; border: 1px solid #333; }}
        .filter.active {{ background: gold; color: black; font-weight: bold; border-color: gold; }}

        .modal {{ position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.9); display: none; justify-content: center; align-items: center; z-index: 1000; }}
        .profile-box {{ width: 85%; max-width: 350px; background: #1b1f2e; padding: 20px; border-radius: 20px; border: 1px solid gold; }}
        
        .stat-row {{ display: flex; gap: 5px; margin: 15px 0; }}
        .stat-card {{ flex: 1; background: rgba(255,255,255,0.05); padding: 8px; border-radius: 8px; text-align: center; font-size: 11px; }}
        .bar {{ height: 8px; background: #333; border-radius: 4px; margin: 5px 0; overflow: hidden; }}
        .fill {{ height: 100%; background: gold; width: 0%; }}
        .close-btn {{ width: 100%; padding: 10px; background: #ff4b4b; color: white; border: none; border-radius: 8px; cursor: pointer; margin-top: 15px; font-weight: bold; }}
    </style>
</head>
<body>

<div id="langBtn">EN</div>
<input class="search" id="searchInput" placeholder="🔍 Nhập tên..." onkeyup="search(this.value)">

<div class="filters">
    <div class="filter active" id="fPow" onclick="setMode('power', this)">SỨC MẠNH</div>
    <div class="filter" id="fKill" onclick="setMode('kill', this)">TIÊU DIỆT</div>
    <div class="filter" id="fDead" onclick="setMode('dead', this)">ĐIỂM CHẾT</div>
</div>

<div class="grid" id="grid">{cards_html}</div>

<div class="modal" id="modal">
    <div class="profile-box" id="profileContent"></div>
</div>

<script>
    let lang = "vn";
    const TEXT = {{
        vn: {{ search: "🔍 Nhập tên...", pow: "SỨC MẠNH", kill: "TIÊU DIỆT", dead: "ĐIỂM CHẾT", exit: "ĐÓNG" }},
        en: {{ search: "🔍 Search name...", pow: "POWER", kill: "KILL", dead: "DEAD", exit: "CLOSE" }}
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
            c.style.display = c.innerText.toLowerCase().includes(v) ? 'block' : 'none';
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
            c.querySelector('.value').innerText = Number(c.dataset[m]).toLocaleString();
            grid.appendChild(c);
        }});
    }}

    function openProfile(name, id, all, pow, kill, dead, kpiK, kpiD, avatar) {{
        document.getElementById('modal').style.display = 'flex';
        document.getElementById('profileContent').innerHTML = `
            <center>
                <div class="avatar-wrap" style="width:60px; height:60px;"><img src="${{avatar}}"></div>
                <h3 style="margin:5px 0;">${{name}}</h3>
                <small style="color:#888;">ID: ${{id}} | ${{all}}</small>
            </center>
            <div class="stat-row">
                <div class="stat-card">POWER<br><b>${{Number(pow).toLocaleString()}}</b></div>
                <div class="stat-card">KILL<br><b>${{Number(kill).toLocaleString()}}</b></div>
                <div class="stat-card">DEAD<br><b>${{Number(dead).toLocaleString()}}</b></div>
            </div>
            <div style="font-size: 12px;">
                <p style="margin:5px 0;">🔥 KPI Kill: 0 / ${{Number(kpiK).toLocaleString()}}</p>
                <div class="bar"><div class="fill"></div></div>
                <p style="margin:5px 0;">💀 KPI Dead: 0 / ${{Number(kpiD).toLocaleString()}}</p>
                <div class="bar"><div class="fill"></div></div>
            </div>
            <button class="close-btn" onclick="document.getElementById('modal').style.display='none'">${{TEXT[lang].exit}}</button>
        `;
    }}
</script>
</body>
</html>
"""

components.html(html_content, height=1000, scrolling=True)
