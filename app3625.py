import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== XOÁ SIDEBAR =====
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none !important;}
[data-testid="collapsedControl"] {display:none !important;}
section[data-testid="stSidebar"] {display:none !important;}
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

    kp = min(int(kill / kpiK * 100), 100)
    dp = min(int(dead / kpiD * 100), 100)

    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={name}"

    cards_html += f"""
    <div class="card"
        data-power="{power}"
        data-kill="{kill}"
        data-dead="{dead}"
        onclick="openProfile('{name}','{id_}','{alliance}','{power}','{kill}','{dead}','{kpiK}','{kpiD}','{kp}','{dp}','{avatar}')">

        <div class="avatar-wrap">
            <img src="{avatar}">
        </div>
        <h3>{name}</h3>
        <p class="value">{power:,}</p>
    </div>
    """

# ===== HTML =====
html = f"""
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>

/* ===== SEARCH XỊN ===== */
.search-box {{
    position:relative;
    width:100%;
    margin-bottom:25px;
}}

.search {{
    width:100%;
    padding:15px 50px 15px 15px;
    font-size:18px;
    border-radius:12px;
    border:none;
    background:#111;
    color:white;
}}

.search-icon {{
    position:absolute;
    right:15px;
    top:50%;
    transform:translateY(-50%);
    font-size:20px;
    opacity:0.7;
}}

/* ===== LANG SWITCH ===== */
.lang {{
    position:absolute;
    top:10px;
    right:20px;
    cursor:pointer;
    padding:8px 15px;
    background:gold;
    border-radius:10px;
    color:black;
    font-weight:bold;
}}

</style>
</head>

<body>

<div class="lang" onclick="toggleLang()">EN</div>

<div class="search-box">
    <input class="search" id="searchInput" placeholder="🔍 Nhập tên..." onkeyup="search(this.value)">
    <div class="search-icon">🔍</div>
</div>

<div class="filters">
    <div class="filter active" onclick="setMode('power')">⚡ POWER</div>
    <div class="filter" onclick="setMode('kill')">🔥 KILL</div>
    <div class="filter" onclick="setMode('dead')">💀 DEAD</div>
</div>

<div class="grid" id="grid">{cards_html}</div>

<div class="modal" id="modal">
<div class="profile" id="profile"></div>
</div>

<script>

let mode = "power"
let lang = "vn"

function toggleLang(){{
    lang = lang === "vn" ? "en" : "vn"
    document.querySelector(".lang").innerText = lang.toUpperCase()

    document.getElementById("searchInput").placeholder =
        lang==="vn" ? "🔍 Nhập tên..." : "🔍 Search player..."
}}

function setMode(m){{
    mode = m
    let cards = Array.from(document.querySelectorAll(".card"))
    cards.sort((a,b)=> b.dataset[mode] - a.dataset[mode])

    let grid = document.getElementById("grid")
    grid.innerHTML=""

    cards.forEach(c=>{{
        c.querySelector(".value").innerText = Number(c.dataset[mode]).toLocaleString()
        grid.appendChild(c)
    }})
}}

function search(val){{
    val = val.toLowerCase()
    document.querySelectorAll(".card").forEach(c=>{{
        c.style.display = c.innerText.toLowerCase().includes(val) ? "block":"none"
    }})
}}

function openProfile(name,id,alliance,power,kill,dead,kpiK,kpiD,kp,dp,avatar){{
    document.getElementById("modal").style.display="flex"

    let text = {{
        vn: {{
            id:"ID",
            alliance:"Liên Minh",
            power:"Sức Mạnh",
            kill:"Tiêu Diệt",
            dead:"Tử Trận",
            kpiK:"KPI Tiêu Diệt",
            kpiD:"KPI Tử Trận",
            close:"❌ ĐÓNG"
        }},
        en: {{
            id:"ID",
            alliance:"Alliance",
            power:"Power",
            kill:"Kill",
            dead:"Dead",
            kpiK:"KPI Kill",
            kpiD:"KPI Dead",
            close:"❌ CLOSE"
        }}
    }}

    let t = text[lang]

    document.getElementById("profile").innerHTML = `
    <div class="profile-top">
        <div class="avatar-big"><img src="${{avatar}}"></div>
        <div>
            <h2>${{name}}</h2>
            <p>${{t.id}}: ${{id}}</p>
            <p>${{t.alliance}}: ${{alliance}}</p>
        </div>
    </div>

    <div class="row">
        <div class="box">⚡ ${{t.power}}<br>${{Number(power).toLocaleString()}}</div>
        <div class="box">🔥 ${{t.kill}}<br>${{Number(kill).toLocaleString()}}</div>
        <div class="box">💀 ${{t.dead}}<br>${{Number(dead).toLocaleString()}}</div>
    </div>

    <h3>🔥 ${{t.kpiK}}</h3>
    <div class="bar"><div class="fill" style="width:0%"></div></div>
    <p>0 / ${{kpiK.toLocaleString()}}</p>

    <h3>💀 ${{t.kpiD}}</h3>
    <div class="bar"><div class="fill" style="width:0%"></div></div>
    <p>0 / ${{kpiD.toLocaleString()}}</p>

    <br>
    <button onclick="closeProfile()">${{t.close}}</button>
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
