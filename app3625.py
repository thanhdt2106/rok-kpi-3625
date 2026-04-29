import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ====== LOAD DATA GOOGLE SHEET ======
@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid = "855089129"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)

    # chuẩn hóa tên cột
    df.columns = df.columns.str.strip()

    return df

df = load_data()

# ====== CLEAN DATA ======
def to_int(x):
    try:
        return int(str(x).replace(",", ""))
    except:
        return 0

df["Power"] = df["Sức Manh"].apply(to_int)
df["Kill"] = df["Tổng Tiêu Diệt"].apply(to_int)
df["Dead"] = df["Điểm chết"].apply(to_int)

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

# ===== BUILD HTML =====
cards_html = ""

for i, row in df.iterrows():
    name = str(row["Tên"])
    id_ = str(row["ID"])
    alliance = str(row["Liên Minh"])
    power = row["Power"]
    kill = row["Kill"]
    dead = row["Dead"]

    kpiK = kpi_kill(power)
    kpiD = kpi_dead(power)

    kill_percent = min(int(kill / kpiK * 100), 100)
    dead_percent = min(int(dead / kpiD * 100), 100)

    cards_html += f"""
    <div class="card" onclick="openProfile('{name}','{id_}','{alliance}','{power}','{kill}','{dead}','{kpiK}','{kpiD}','{kill_percent}','{dead_percent}')">
        <img src="https://api.dicebear.com/7.x/adventurer/svg?seed={name}">
        <h3>{name}</h3>
        <p>{power:,}</p>
    </div>
    """

html = f"""
<html>
<head>
<style>
body {{
    background:#0b0f1a;
    color:white;
    font-family:Arial;
}}

.search {{
    width:100%;
    padding:15px;
    font-size:18px;
    border-radius:10px;
    border:none;
    margin-bottom:20px;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
    gap:20px;
}}

.card {{
    background:#111;
    padding:20px;
    border-radius:15px;
    text-align:center;
    cursor:pointer;
    transition:0.3s;
    border:1px solid #222;
}}

.card:hover {{
    transform:scale(1.05);
    box-shadow:0 0 20px gold;
}}

.card img {{
    width:70px;
    border-radius:50%;
    border:2px solid gold;
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
    width:800px;
    background:#111;
    border-radius:20px;
    padding:30px;
}}

.row {{
    display:flex;
    gap:20px;
    margin-top:15px;
}}

.box {{
    flex:1;
    background:#1a1a1a;
    padding:15px;
    border-radius:10px;
}}

.bar {{
    height:10px;
    background:#333;
    border-radius:5px;
    overflow:hidden;
}}

.fill {{
    height:100%;
    background:gold;
}}

</style>
</head>

<body>

<input class="search" placeholder="🔍 Nhập tên người chơi..." onkeyup="search(this.value)">

<div class="grid" id="grid">
{cards_html}
</div>

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

function openProfile(name,id,alliance,power,kill,dead,kpiK,kpiD,kp,dp){{
    document.getElementById("modal").style.display="flex"

    document.getElementById("profile").innerHTML = `
    <h2>${{name}}</h2>

    <div class="row">
        <div class="box">🆔 ${{id}}</div>
        <div class="box">🏰 ${{alliance}}</div>
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
