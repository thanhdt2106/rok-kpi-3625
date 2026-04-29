import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ===== CẤU HÌNH FULL MÀN HÌNH =====
st.set_page_config(page_title="FTD KPI SYSTEM", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid = "855089129"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ===== CLEAN DATA =====
def to_int(x):
    try: return int(str(x).replace(",", ""))
    except: return 0

df["Power"] = df["Sức Mạnh"].apply(to_int)
df["Kill"] = df["Tổng Tiêu Diệt"].apply(to_int)
df["Dead"] = df["Điểm Chết"].apply(to_int)

# ===== KPI RULES =====
def kpi_kill(pow):
    if pow >= 100_000_000: return 600_000_000
    elif pow >= 90_000_000: return 550_000_000
    elif pow >= 80_000_000: return 450_000_000
    elif pow >= 70_000_000: return 300_000_000
    elif pow >= 60_000_000: return 250_000_000
    else: return 200_000_000

def kpi_dead(pow):
    if pow >= 100_000_000: return 1_500_000
    elif pow >= 90_000_000: return 1_200_000
    elif pow >= 80_000_000: return 1_000_000
    elif pow >= 70_000_000: return 800_000
    else: return 700_000

# ===== BUILD CARDS =====
cards_html = ""
for _, row in df.iterrows():
    name, id_, alliance = str(row["Tên"]), str(row["ID"]), str(row["Liên Minh"])
    power, kill, dead = row["Power"], row["Kill"], row["Dead"]
    kpiK, kpiD = kpi_kill(power), kpi_dead(power)
    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={name}"

    cards_html += f"""
    <div class="card" data-power="{power}" data-kill="{kill}" data-dead="{dead}"
        onclick="openProfile('{name}','{id_}','{alliance}','{power}','{kill}','{dead}','{kpiK}','{kpiD}','{avatar}')">
        <div class="avatar-wrap"><img src="{avatar}"></div>
        <h3>{name}</h3>
        <p class="value">{power:,}</p>
    </div>
    """

# ===== GIAO DIỆN HTML/CSS/JS =====
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            background: radial-gradient(circle at top, #111, #05070d);
            color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px;
        }}
        
        /* Hiệu ứng hào quang cho Avatar */
        .avatar-wrap {{
            width: 85px; height: 85px; margin: auto; border-radius: 50%; padding: 3px;
            background: linear-gradient(45deg, #ffd700, #ff8c00);
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.7);
            animation: pulse-gold 2s infinite;
        }}
        @keyframes pulse-gold {{
            0% {{ box-shadow: 0 0 10px rgba(255, 215, 0, 0.5); }}
            50% {{ box-shadow: 0 0 25px rgba(255, 215, 0, 0.9); }}
            100% {{ box-shadow: 0 0 10px rgba(255, 215, 0, 0.5); }}
        }}
        .avatar-wrap img {{ width: 100%; height: 100%; border-radius: 50%; background: #222; }}

        .search {{
            width: 100%; padding: 15px; background: #111; border: 1px solid #333;
            color: white; border-radius: 12px; margin-bottom: 20px; box-sizing: border-box;
        }}

        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; }}
        
        .card {{
            background: #161b22; padding: 20px; border-radius: 20px; text-align: center;
            border: 1px solid #333; cursor: pointer; transition: 0.3s;
        }}
        .card:hover {{ transform: translateY(-10px); border-color: gold; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }}

        .filters {{ display: flex; gap: 10px; margin-bottom: 20px; }}
        .filter {{ padding: 10px 15px; background: #222; border-radius: 8px; cursor: pointer; border: 1px solid #444; }}
        .filter.active {{ background: gold; color: black; font-weight: bold; }}

        /* Modal Profile */
        .modal {{
            position: fixed; top:0; left:0; width:100%; height:100%;
            background: rgba(0,0,0,0.95); display: none; justify-content: center; align-items: center; z-index: 1000;
        }}
        .profile-box {{
            width: 90%; max-width: 500px; background: #1b1f2e; padding: 30px; border-radius: 25px; border: 1px solid gold;
        }}
        .bar {{ height: 12px; background: #333; border-radius: 10px; margin: 10px 0; overflow: hidden; }}
        .fill {{ height: 100%; background: linear-gradient(90deg, gold, #ffa500); width: 0%; transition: 1s; }}
        
        .stat-row {{ display: flex; gap: 10px; margin: 20px 0; }}
        .stat-card {{ flex: 1; background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; text-align: center; }}
        
        .close-btn {{
            width: 100%; padding: 12px; background: #ff4b4b; border: none; color: white;
            border-radius: 10px; cursor: pointer; margin-top: 20px; font-weight: bold;
        }}
    </style>
</head>
<body>

    <input class="search" id="searchInput" placeholder="🔍 Nhập tên chiến binh..." onkeyup="search(this.value)">

    <div class="filters">
        <div class="filter active" onclick="setMode('power', this)">⚡ SỨC MẠNH</div>
        <div class="filter" onclick="setMode('kill', this)">🔥 TIÊU DIỆT</div>
        <div class="filter" onclick="setMode('dead', this)">💀 ĐIỂM CHẾT</div>
    </div>

    <div class="grid" id="grid">{cards_html}</div>

    <div class="modal" id="modal">
        <div class="profile-box" id="profileContent"></div>
    </div>

    <script>
        function search(val) {{
            val = val.toLowerCase();
            document.querySelectorAll('.card').forEach(c => {{
                c.style.display = c.innerText.toLowerCase().includes(val) ? 'block' : 'none';
            }});
        }}

        function setMode(mode, el) {{
            document.querySelectorAll('.filter').forEach(f => f.classList.remove('active'));
            el.classList.add('active');
            let grid = document.getElementById('grid');
            let cards = Array.from(grid.getElementsByClassName('card'));
            cards.sort((a,b) => Number(b.dataset[mode]) - Number(a.dataset[mode]));
            grid.innerHTML = "";
            cards.forEach(c => {{
                c.querySelector('.value').innerText = Number(c.dataset[mode]).toLocaleString();
                grid.appendChild(c);
            }});
        }}

        function openProfile(name, id, all, pow, kill, dead, kpiK, kpiD, avatar) {{
            document.getElementById('modal').style.display = 'flex';
            // TIẾN ĐỘ ĐƯỢC SET VỀ 0 NHƯ YÊU CẦU
            document.getElementById('profileContent').innerHTML = `
                <center>
                    <div class="avatar-wrap" style="width:100px; height:100px;">
                        <img src="${{avatar}}">
                    </div>
                    <h2 style="margin:10px 0 5px 0;">${{name}}</h2>
                    <code style="color:gold;">ID: ${{id}} | ${{all}}</code>
                </center>

                <div class="stat-row">
                    <div class="stat-card">⚡ Power<br><b>${{Number(pow).toLocaleString()}}</b></div>
                    <div class="stat-card">🔥 Kills<br><b>${{Number(kill).toLocaleString()}}</b></div>
                    <div class="stat-card">💀 Dead<br><b>${{Number(dead).toLocaleString()}}</b></div>
                </div>

                <div style="margin-top:20px;">
                    <span>🔥 KPI Tiêu diệt: <b>0</b> / ${{Number(kpiK).toLocaleString()}}</span>
                    <div class="bar"><div class="fill" style="width: 0%"></div></div>
                </div>

                <div style="margin-top:15px;">
                    <span>💀 KPI Điểm chết: <b>0</b> / ${{Number(kpiD).toLocaleString()}}</span>
                    <div class="bar"><div class="fill" style="width: 0%"></div></div>
                </div>

                <button class="close-btn" onclick="closeProfile()">QUAY LẠI</button>
            `;
        }}

        function closeProfile() {{
            document.getElementById('modal').style.display = 'none';
        }}
    </script>
</body>
</html>
"""

components.html(html_content, height=1000, scrolling=True)
