import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== XOÁ SIDEBAR + FULL SCREEN =====
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none !important;}
[data-testid="collapsedControl"] {display:none !important;}
section[data-testid="stSidebar"] {display:none !important;}
.block-container {padding:0 !important;}
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

body {{
    background: radial-gradient(circle at top, #111, #05070d);
    color:white;
    font-family:Arial;
    margin:0;
}}

.search {{
    width:80%;
    margin:20px auto;
    display:block;
    padding:12px;
    font-size:16px;
    border-radius:12px;
    border:none;
    background:#111;
    color:white;
}}

.lang {{
    position:absolute;
    top:15px;
    right:20px;
    background:gold;
    color:black;
    padding:8px 12px;
    border-radius:10px;
    cursor:pointer;
    font-weight:bold;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
    gap:25px;
    padding:20px;
}}

.card {{
    background:linear-gradient(145deg,#0f111a,#1b1f2e);
    padding:20px;
    border-radius:20px;
    text-align:center;
    cursor:pointer;
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

.modal {{
    position:fixed;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.9);
    display:none;
    justify-content:center;
    align-items:center;
}}

.profile {{
    width:850px;
    background:#111;
    padding:30px;
    border-radius:20px;
}}

</style>
</head>

<body>

<div class="lang" onclick="toggleLang()">EN</div>

<input class="search" id="searchInput" placeholder="🔍 Nhập tên..." onkeyup="search(this.value)">

<div class="grid">{cards_html}</div>

<div class="modal" id="modal">
<div class="profile" id="profile"></div>
</div>

<script>

let lang = "vn"

function toggleLang(){{
    lang = lang === "vn" ? "en" : "vn"
    document.querySelector(".lang").innerText = lang.toUpperCase()

    document.getElementById("searchInput").placeholder =
        lang==="vn" ? "🔍 Nhập tên..." : "🔍 Search..."
}}

function search(val){{
    val = val.toLowerCase()
    document.querySelectorAll(".card").forEach(c=>{{
        c.style.display = c.innerText.toLowerCase().includes(val) ? "block":"none"
    }})
}}

function openProfile(name,id,alliance,power,kill,dead,kpiK,kpiD,kp,dp,avatar){{
    document.getElementById("modal").style.display="flex"

    let t = {{
        vn: ["ID","Liên Minh","Sức Mạnh","Tiêu Diệt","Tử Trận","KPI Tiêu Diệt","KPI Tử Trận","ĐÓNG"],
        en: ["ID","Alliance","Power","Kill","Dead","KPI Kill","KPI Dead","CLOSE"]
    }}[lang]

    document.getElementById("profile").innerHTML = `
    <h2>${{name}}</h2>
    <p>${{t[0]}}: ${{id}}</p>
    <p>${{t[1]}}: ${{alliance}}</p>

    <p>⚡ ${{t[2]}}: ${{power}}</p>
    <p>🔥 ${{t[3]}}: ${{kill}}</p>
    <p>💀 ${{t[4]}}: ${{dead}}</p>

    <h3>${{t[5]}}</h3>
    <p>0 / ${{kpiK}}</p>

    <h3>${{t[6]}}</h3>
    <p>0 / ${{kpiD}}</p>

    <button onclick="closeProfile()">❌ ${{t[7]}}</button>
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
