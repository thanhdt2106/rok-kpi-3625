import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

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

    kp = min(int(kill / kpiK * 100), 100)
    dp = min(int(dead / kpiD * 100), 100)

    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={name}"

    cards_html += f"""
    <div class="card" onclick="openProfile('{name}','{id_}','{alliance}','{power}','{kill}','{dead}','{kpiK}','{kpiD}','{kp}','{dp}','{avatar}')">
        <div class="avatar-wrap">
            <img src="{avatar}">
        </div>
        <h3>{name}</h3>
        <p>{power:,}</p>
    </div>
    """

# ===== HTML =====
html = f"""
<html>
<head>
<style>
body {{
    background: radial-gradient(circle at top, #111, #05070d);
    color:white;
    font-family:Arial;
}}

.search {{
    width:100%;
    padding:15px;
    font-size:18px;
    border-radius:12px;
    border:none;
    margin-bottom:25px;
    background:#111;
    color:white;
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
    position:relative;
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
    box-shadow:0 0 15px gold;
}}

.avatar-wrap img {{
    width:100%;
    height:100%;
    border-radius:50%;
    background:#111;
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
}}

.profile {{
    width:850px;
    background:linear-gradient(145deg,#0f111a,#1b1f2e);
    border-radius:25px;
    padding:30px;
    box-shadow:0 0 40px rgba(255,215,0,0.3);
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
    padding:4px;
    background:linear-gradient(45deg,gold,orange);
    box-shadow:0 0 20px gold;
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
    backdrop-filter: blur(10px);
    border:1px solid rgba(255,255,255,0.1);
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

</style>
</head>

<body>

<input class="search" placeholder="🔍 Nhập tên..." onkeyup="search(this.value)">

<div class="grid">{cards_html}</div>

<div class="modal" id="modal">
<div class="profile" id="profile"></div>
</div>

<script>
function search(val){{
    val = val.toLowerCase()
    document.querySelectorAll(".card").forEach(c=>{{
        c.style.display = c.innerText.toLowerCase().includes(val) ? "block":"none"
    }})
}}

function openProfile(name,id,alliance,power,kill,dead,kpiK,kpiD,kp,dp,avatar){{
    document.getElementById("modal").style.display="flex"

    document.getElementById("profile").innerHTML = `
    <div class="profile-top">
        <div class="avatar-big"><img src="${{avatar}}"></div>
        <div>
            <h2>${{name}}</h2>
            <p>ID: ${{id}}</p>
            <p>${{alliance}}</p>
        </div>
    </div>

    <div class="row">
        <div class="box">⚡ ${{Number(power).toLocaleString()}}</div>
        <div class="box">🔥 ${{Number(kill).toLocaleString()}}</div>
        <div class="box">💀 ${{Number(dead).toLocaleString()}}</div>
    </div>

    <h3>🔥 KPI Kill</h3>
    <div class="bar"><div class="fill" style="width:${{kp}}%"></div></div>
    <p>${{kill}} / ${{kpiK}} (${{kp}}%)</p>

    <h3>💀 KPI Dead</h3>
    <div class="bar"><div class="fill" style="width:${{dp}}%"></div></div>
    <p>${{dead}} / ${{kpiD}} (${{dp}}%)</p>

    <br>
    <button onclick="closeProfile()">Close</button>
    `
}}

function closeProfile(){{
    document.getElementById("modal").style.display="none"
}}
</script>

</body>
</html>
"""

components.html(html, height=900, scrolling=True)
