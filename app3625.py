import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ====== ẨN STREAMLIT ======
st.markdown("""
<style>
#MainMenu, header, footer {visibility:hidden;}
.block-container {padding-top:0;}
</style>
""", unsafe_allow_html=True)

# ====== CONFIG ======
SHEET_ID = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
GID = "855089129"

# ====== LOAD DATA ======
@st.cache_data(ttl=60)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={GID}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ====== SEARCH ======
search = st.text_input("🔍 Nhập tên người chơi")

if search:
    df = df[df["Tên"].str.contains(search, case=False, na=False)]

# ====== SORT TOP ======
df = df.sort_values(by="Tổng Tiêu Diệt", ascending=False)

# ====== BUILD CARD ======
players_html = ""

for i, row in df.head(40).iterrows():
    name = str(row.get("Tên", "Unknown"))
    pid = str(row.get("ID", ""))
    alliance = str(row.get("Liên Minh", ""))
    power = int(row.get("Tổng Tiêu Diệt", 0))
    dead = int(row.get("Điểm chết", 0))

    avatar = f"https://api.dicebear.com/7.x/adventurer/png?seed={name}"

    glow = "gold" if i < 3 else "#00ffe0"

    players_html += f"""
    <div class="card"
        onclick="openProfile('{name}','{pid}','{alliance}','{power}','{dead}','{avatar}')">

        <div class="rank">#{i+1}</div>

        <img src="{avatar}">

        <div class="name">{name}</div>
        <div class="power">{power:,}</div>

    </div>
    """

# ====== HTML ======
html = f"""
<html>
<head>
<meta charset="UTF-8">

<style>
body {{
    margin:0;
    background:url('https://images.unsplash.com/photo-1605902711622-cfb43c44367f') center/cover no-repeat;
    font-family:sans-serif;
    color:white;
}}

.overlay-bg {{
    position:fixed;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.75);
}}

.title {{
    text-align:center;
    font-size:40px;
    padding:20px;
    font-weight:bold;
    color:gold;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill,180px);
    gap:25px;
    justify-content:center;
    padding:20px;
}}

.card {{
    background:rgba(0,0,0,0.6);
    border-radius:20px;
    padding:15px;
    text-align:center;
    cursor:pointer;
    transition:0.3s;
    position:relative;
}}

.card:hover {{
    transform:scale(1.1);
    box-shadow:0 0 25px gold;
}}

.card img {{
    width:90px;
    border-radius:50%;
    border:3px solid gold;
}}

.rank {{
    position:absolute;
    top:10px;
    left:10px;
    font-size:14px;
    color:gold;
}}

.name {{
    margin-top:10px;
    font-weight:bold;
}}

.power {{
    font-size:13px;
    color:#ccc;
}}

.popup {{
    position:fixed;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    width:65%;
    background:rgba(0,0,0,0.9);
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
    background:rgba(0,0,0,0.8);
    display:none;
}}

.profile-top {{
    display:flex;
    gap:20px;
    align-items:center;
}}

.profile-top img {{
    width:120px;
    border-radius:50%;
    border:4px solid gold;
}}

.stats {{
    margin-top:20px;
    display:flex;
    gap:20px;
}}

.stat {{
    flex:1;
    background:rgba(255,255,255,0.1);
    padding:20px;
    border-radius:15px;
    text-align:center;
}}
</style>
</head>

<body>

<div class="overlay-bg"></div>

<div class="title">🔥 ROK PRO MAX DASHBOARD</div>

<div class="grid">
{players_html}
</div>

<div class="overlay" id="overlay" onclick="closeProfile()"></div>

<div class="popup" id="popup">

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
