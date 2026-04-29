import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ❌ XÓA SIDEBAR
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none;}
.block-container {padding:0;}
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

def to_int(x):
    try:
        return int(str(x).replace(",", ""))
    except:
        return 0

df["Power"] = df["Sức Mạnh"].apply(to_int)
df["Kill"] = df["Tổng Tiêu Diệt"].apply(to_int)
df["Dead"] = df["Điểm Chết"].apply(to_int)

# ===== KPI =====
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

# ===== BUILD CARD =====
cards_html = ""

for _, row in df.iterrows():
    name = str(row["Tên"])
    id_ = str(row["ID"])
    alliance = str(row["Liên Minh"])
    power = row["Power"]
    kill = row["Kill"]
    dead = row["Dead"]

    kpiK = kpi_kill(power)
    kpiD = kpi_dead(power)

    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={name}"

    cards_html += f"""
    <div class="card"
    data-power="{power}"
    data-kill="{kill}"
    data-dead="{dead}"
    onclick="openProfile('{name}','{id_}','{alliance}','{power}','{kill}','{dead}','{kpiK}','{kpiD}','{avatar}')">

        <div class="avatar-wrap">
            <img src="{avatar}">
        </div>
        <h3>{name}</h3>
        <p class="stat">{power}</p>
    </div>
    """

# ===== HTML =====
html = f"""
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>

body {{
    background: radial-gradient(circle at top, #111, #05070d);
    color:white;
    font-family:Arial;
    margin:0;
}}

.top-box {{
    display:flex;
    gap:15px;
    margin:20px;
}}

.mode {{
    flex:1;
    padding:15px;
    text-align:center;
    background:#111;
    border-radius:12px;
    cursor:pointer;
    border:1px solid #333;
}}

.mode:hover {{
    box-shadow:0 0 15px gold;
}}

.search {{
    width:95%;
    margin:20px;
    padding:15px;
    border-radius:12px;
    background:#111;
    color:white;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
    gap:20px;
    padding:20px;
}}

.card {{
    background:#111;
    padding:20px;
    border-radius:20px;
    text-align:center;
    cursor:pointer;
    transition:0.3s;
}}

.card:hover {{
    transform:scale(1.05);
    box-shadow:0 0 20px gold;
}}

.avatar-wrap {{
    width:80px;
    height:80px;
    margin:auto;
    border-radius:50%;
    padding:3px;
    background:gold;
}}

.avatar-wrap img {{
    width:100%;
    border-radius:50%;
}}

.modal {{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:black;
    display:none;
    justify-content:center;
    align-items:center;
}}

.profile {{
    width:90%;
    max-width:800px;
}}

.close-btn {{
    background:red;
    color:white;
    padding:10px 20px;
    border:none;
    border-radius:10px;
    cursor:pointer;
    font-weight:bold;
}}

</style>
</head>

<body>

<div class="top-box">
    <div class="mode" onclick="setMode('power')">⚡ POWER</div>
    <div class="mode" onclick="setMode('kill')">🔥 KILL</div>
    <div class="mode" onclick="setMode('dead')">💀 DEAD</div>
</div>

<input class="search" placeholder="🔍 Nhập tên..." onkeyup="search(this.value)">

<div class="grid" id="grid">
{cards_html}
</div>

<div class="modal" id="modal">
<div class="profile" id="profile"></div>
</div>

<script>

let mode = "power"

function setMode(m){{
    mode = m
    let cards = Array.from(document.querySelectorAll(".card"))

    cards.sort((a,b)=> b.dataset[mode] - a.dataset[mode])

    let grid = document.getElementById("grid")
    grid.innerHTML=""
    cards.forEach((c,i)=>{{
        c.querySelector(".stat").innerText = Number(c.dataset[mode]).toLocaleString()
        grid.appendChild(c)
    }})
}}

function search(val){{
    val = val.toLowerCase()
    document.querySelectorAll(".card").forEach(c=>{{
        c.style.display = c.innerText.toLowerCase().includes(val) ? "block":"none"
    }})
}}

function openProfile(name,id,alliance,power,kill,dead,kpiK,kpiD,avatar){{
    document.getElementById("modal").style.display="flex"

    document.getElementById("profile").innerHTML = `
    <h2>${{name}}</h2>
    <p>🆔 ID: ${{id}}</p>
    <p>🏰 Alliance: ${{alliance}}</p>

    <p>⚡ Power: ${{Number(power).toLocaleString()}}</p>
    <p>🔥 Kill: ${{Number(kill).toLocaleString()}}</p>
    <p>💀 Dead: ${{Number(dead).toLocaleString()}}</p>

    <h3>🔥 KPI Kill</h3>
    <p>0 / ${{Number(kpiK).toLocaleString()}}</p>

    <h3>💀 KPI Dead</h3>
    <p>0 / ${{Number(kpiD).toLocaleString()}}</p>

    <br>
    <button class="close-btn" onclick="closeProfile()">❌ BYE BRO</button>
    `
}}

function closeProfile(){{
    document.getElementById("modal").style.display="none"
}}

</script>

</body>
</html>
"""

components.html(html, height=1000, scrolling=True)
