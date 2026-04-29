import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="FTD KPI SYSTEM", layout="wide", initial_sidebar_state="collapsed")

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

# ===== CLEAN =====
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
        <p class="value">{power:,}</p>
    </div>
    """

# ===== HTML =====
html = f"""
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">

<style>

body {{
    background: radial-gradient(circle at top, #111, #05070d);
    color:white;
    font-family:Arial;
    margin:0;
    font-size: clamp(14px, 2vw, 16px);
    -webkit-tap-highlight-color: transparent;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
    gap:25px;
}}

.card {{
    background:linear-gradient(145deg,#0f111a,#1b1f2e);
    padding:20px;
    border-radius:20px;
    text-align:center;
    cursor:pointer;
    transition:0.3s;
    border:1px solid #222;
    touch-action: manipulation;
}}

.card:hover {{
    transform:translateY(-8px) scale(1.05);
    box-shadow:0 0 25px gold;
}}

.avatar-wrap {{
    width:80px;
    height:80px;
    margin:auto;
    border-radius:50%;
    padding:3px;
    background:linear-gradient(45deg,gold,orange);
}}

.avatar-wrap img {{
    width:100%;
    border-radius:50%;
}}

.search {{
    width:100%;
    padding:12px;
    border-radius:12px;
    border:none;
    margin-bottom:20px;
    background:#111;
    color:white;
}}

.filters {{
    display:flex;
    gap:10px;
    margin-bottom:15px;
}}

.filter {{
    padding:10px 15px;
    background:#111;
    border-radius:10px;
    cursor:pointer;
}}

.filter.active {{
    background:gold;
    color:black;
}}

.modal {{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.9);
    display:none;
    justify-content:center;
    align-items:center;
    backdrop-filter: blur(6px);
}}

.profile {{
    width:850px;
    background:#111;
    border-radius:25px;
    padding:30px;
}}

.profile-top {{
    display:flex;
    align-items:center;
    gap:20px;
}}

.avatar-big {{
    width:90px;
    height:90px;
    border-radius:50%;
}}

.avatar-big img {{
    width:100%;
    border-radius:50%;
}}

.row {{
    display:flex;
    gap:15px;
    margin-top:20px;
}}

.box {{
    flex:1;
    background:rgba(255,255,255,0.05);
    padding:15px;
    border-radius:12px;
}}

.bar {{
    height:10px;
    background:#222;
    border-radius:10px;
    overflow:hidden;
}}

.fill {{
    height:100%;
    background:linear-gradient(90deg,gold,orange);
}}

button {{
    margin-top:20px;
    padding:10px;
    border:none;
    border-radius:10px;
    background:gold;
    color:black;
    cursor:pointer;
}}

#langBtn {{
position:fixed;
top:10px;
right:15px;
background:gold;
color:black;
padding:5px 10px;
border-radius:8px;
cursor:pointer;
z-index:999;
font-size:12px;
}}

/* ===== MOBILE ===== */
@media (max-width: 768px){{

    .grid{{ grid-template-columns:repeat(2,1fr); gap:15px; }}

    .card{{ padding:12px; }}

    .avatar-wrap{{ width:60px;height:60px; }}

    .profile{{ width:100%; border-radius:20px 20px 0 0; padding:15px; }}

    .modal{{ align-items:flex-end; }}

    .profile-top{{ flex-direction:column; text-align:center; }}

    .row{{ flex-direction:column; }}

}}

</style>
</head>

<body>

<div id="langBtn">EN</div>

<input class="search" placeholder="🔍 Nhập tên..." onkeyup="search(this.value)">

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

const TEXT = {{
    vn: {{search:"🔍 Nhập tên...",id:"ID",alliance:"Alliance",exit:"EXIT"}},
    en: {{search:"🔍 Search...",id:"ID",alliance:"Alliance",exit:"EXIT"}}
}}

document.getElementById("langBtn").onclick = function(){{
    lang = lang === "vn" ? "en" : "vn"
    this.innerText = lang.toUpperCase()
    document.querySelector(".search").placeholder = TEXT[lang].search
}}

function setMode(m){{
    mode = m
    document.querySelectorAll(".filter").forEach(f=>f.classList.remove("active"))
    event.target.classList.add("active")

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

function openProfile(name,id,alliance,power,kill,dead,kpiK,kpiD,avatar){{
    document.getElementById("modal").style.display="flex"

    document.getElementById("profile").innerHTML = `
    <div class="profile-top">
        <div class="avatar-big"><img src="${{avatar}}"></div>
        <div>
            <h2>${{name}}</h2>
            <p>ID: ${{id}}</p>
            <p>Alliance: ${{alliance}}</p>
        </div>
    </div>

    <div class="row">
        <div class="box">⚡ ${{Number(power).toLocaleString()}}</div>
        <div class="box">🔥 ${{Number(kill).toLocaleString()}}</div>
        <div class="box">💀 ${{Number(dead).toLocaleString()}}</div>
    </div>

    <button onclick="closeProfile()">EXIT</button>
    `
}}

function closeProfile(){{
    document.getElementById("modal").style.display="none"
}}

</script>

</body>
</html>
"""

components.html(html, height=850, scrolling=True)
