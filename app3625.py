import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ================= CONFIG =================
SHEET_ID = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
GID = "855089129"

# ================= LOAD DATA =================
@st.cache_data(ttl=60)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={GID}"
    df = pd.read_csv(url)

    # 🔥 FIX LỖI CỘT
    df.columns = df.columns.str.strip()

    return df

df = load_data()

# ================= SEARCH =================
search = st.text_input("🔍 Nhập tên người chơi")

if search:
    df = df[df["Tên"].str.contains(search, case=False, na=False)]

# ================= BUILD HTML =================
players_html = ""

for _, row in df.head(30).iterrows():
    name = str(row.get("Tên", "Unknown"))
    player_id = str(row.get("ID", ""))
    alliance = str(row.get("Liên Minh", ""))
    power = int(row.get("Tổng Tiêu Diệt", 0))
    dead = int(row.get("Điểm Chết", 0))

    avatar = f"https://api.dicebear.com/7.x/adventurer/png?seed={name}"

    players_html += f"""
    <div class="card"
        onclick="openProfile('{name}', '{player_id}', '{alliance}', '{power}', '{dead}', '{avatar}')">
        
        <img src="{avatar}">
        <div class="name">{name}</div>
        <small>{power:,}</small>
    </div>
    """

# ================= HTML =================
html = f"""
<html>
<head>
<meta charset="UTF-8">

<style>
body {{
    margin:0;
    background:linear-gradient(135deg,#0b0f1a,#05070d);
    font-family:sans-serif;
    color:white;
}}

.title {{
    text-align:center;
    font-size:32px;
    margin:20px;
    font-weight:bold;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill,160px);
    gap:20px;
    justify-content:center;
    padding:20px;
}}

.card {{
    background:rgba(255,255,255,0.05);
    padding:15px;
    border-radius:20px;
    text-align:center;
    cursor:pointer;
    transition:0.3s;
    backdrop-filter:blur(10px);
}}

.card:hover {{
    transform:scale(1.05);
    box-shadow:0 0 20px gold;
}}

.card img {{
    width:80px;
    border-radius:50%;
    border:3px solid gold;
}}

.name {{
    margin-top:10px;
    font-weight:bold;
}}

.popup {{
    position:fixed;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    width:65%;
    max-width:900px;
    background:rgba(0,0,0,0.85);
    border-radius:25px;
    padding:30px;
    display:none;
    z-index:1000;
    box-shadow:0 0 40px gold;
}}

.overlay {{
    position:fixed;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.7);
    top:0;
    left:0;
    display:none;
    z-index:999;
}}

.close {{
    position:absolute;
    right:20px;
    top:10px;
    font-size:28px;
    cursor:pointer;
}}

.profile-top {{
    display:flex;
    align-items:center;
    gap:20px;
    margin-bottom:20px;
}}

.profile-top img {{
    width:100px;
    border-radius:50%;
    border:4px solid gold;
}}

.stats {{
    display:flex;
    gap:20px;
    flex-wrap:wrap;
}}

.stat {{
    flex:1;
    min-width:150px;
    background:rgba(255,255,255,0.08);
    padding:15px;
    border-radius:15px;
}}

</style>
</head>

<body>

<div class="title">🔥 ROK MEMBER DASHBOARD</div>

<div class="grid">
{players_html}
</div>

<div class="overlay" id="overlay" onclick="closeProfile()"></div>

<div class="popup" id="popup">
    <div class="close" onclick="closeProfile()">✖</div>

    <div class="profile-top">
        <img id="p_avatar">
        <h2 id="p_name"></h2>
    </div>

    <div class="stats">
        <div class="stat">ID<br><b id="p_id"></b></div>
        <div class="stat">Alliance<br><b id="p_alliance"></b></div>
        <div class="stat">Power<br><b id="p_power"></b></div>
        <div class="stat">Dead<br><b id="p_dead"></b></div>
    </div>
</div>

<script>
function openProfile(name,id,alliance,power,dead,avatar){{
    document.getElementById("popup").style.display="block";
    document.getElementById("overlay").style.display="block";

    document.getElementById("p_name").innerText = name;
    document.getElementById("p_id").innerText = id;
    document.getElementById("p_alliance").innerText = alliance;
    document.getElementById("p_power").innerText = Number(power).toLocaleString();
    document.getElementById("p_dead").innerText = Number(dead).toLocaleString();
    document.getElementById("p_avatar").src = avatar;
}}

function closeProfile(){{
    document.getElementById("popup").style.display="none";
    document.getElementById("overlay").style.display="none";
}}
</script>

</body>
</html>
"""

components.html(html, height=900, scrolling=True)
