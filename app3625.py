import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ====== LOAD DATA GOOGLE SHEET ======
SHEET_ID = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
GID = "855089129"

@st.cache_data(ttl=30)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={GID}"
    df = pd.read_csv(url)
    return df

df = load_data()

# ====== SEARCH ======
search = st.text_input("🔍 Nhập tên người chơi")

if search:
    df = df[df["Tên"].str.contains(search, case=False, na=False)]

players_html = ""

for i, row in df.head(20).iterrows():
    name = row["Tên"]
    power = row["Tổng Tiêu Diệt"]
    avatar = f"https://api.dicebear.com/7.x/adventurer/png?seed={name}"

    players_html += f"""
    <div class="card" onclick="openProfile('{name}', '{row['ID']}', '{row['Liên Minh']}', '{power}', '{row['Điểm chết']}')">
        <img src="{avatar}">
        <div>{name}</div>
        <small>{power:,}</small>
    </div>
    """

html = f"""
<html>
<head>
<style>
body {{
    background:#0b0f1a;
    font-family:sans-serif;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill,150px);
    gap:20px;
    justify-content:center;
}}

.card {{
    background:#111;
    padding:15px;
    border-radius:15px;
    text-align:center;
    cursor:pointer;
    transition:0.3s;
}}

.card:hover {{
    transform:scale(1.05);
    box-shadow:0 0 15px gold;
}}

.card img {{
    width:70px;
    border-radius:50%;
    border:2px solid gold;
}}

.popup {{
    position:fixed;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    width:65%;
    background:#111;
    border-radius:20px;
    padding:30px;
    display:none;
    z-index:999;
}}

.overlay {{
    position:fixed;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.7);
    display:none;
    top:0;
    left:0;
}}

.close {{
    position:absolute;
    right:20px;
    top:10px;
    font-size:25px;
    cursor:pointer;
}}
</style>
</head>

<body>

<div class="grid">
{players_html}
</div>

<div class="overlay" id="overlay" onclick="closeProfile()"></div>

<div class="popup" id="popup">
    <div class="close" onclick="closeProfile()">×</div>
    <h2 id="p_name"></h2>
    <p>ID: <span id="p_id"></span></p>
    <p>Alliance: <span id="p_alliance"></span></p>
    <p>Power: <span id="p_power"></span></p>
    <p>Dead: <span id="p_dead"></span></p>
</div>

<script>
function openProfile(name,id,alliance,power,dead){{
    document.getElementById("popup").style.display="block";
    document.getElementById("overlay").style.display="block";

    document.getElementById("p_name").innerText = name;
    document.getElementById("p_id").innerText = id;
    document.getElementById("p_alliance").innerText = alliance;
    document.getElementById("p_power").innerText = power;
    document.getElementById("p_dead").innerText = dead;
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
