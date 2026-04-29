import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== CONFIG =====
SHEET_ID = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
GID = "855089129"

@st.cache_data(ttl=60)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
    df = pd.read_csv(url)

    # FIX COLUMN
    df.columns = df.columns.str.strip()

    rename_map = {
        "Tên": "name",
        "ID": "id",
        "Liên Minh": "alliance",
        "Tổng Tiêu Diệt": "kill",
        "Điểm Chết": "dead",
        "Sức Mạnh": "power"
    }

    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    for col in ["kill", "dead", "power"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

df = load_data()

search = st.text_input("🔍 Nhập tên...")

# ===== HTML UI =====
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>

body {{
    margin:0;
    background:#050b18;
    color:white;
    font-family:Arial;
}}

.container {{
    padding:30px;
}}

.search {{
    width:100%;
    padding:15px;
    border-radius:10px;
    border:none;
    background:#111;
    color:white;
    font-size:16px;
    margin-bottom:20px;
}}

.filters {{
    display:flex;
    gap:20px;
    margin-bottom:30px;
}}

.filter {{
    flex:1;
    padding:20px;
    text-align:center;
    border-radius:15px;
    background:#111;
    cursor:pointer;
    font-weight:bold;
    transition:0.3s;
}}

.filter:hover {{
    box-shadow:0 0 20px gold;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill, minmax(180px,1fr));
    gap:25px;
}}

.card {{
    background:#0d1425;
    padding:20px;
    border-radius:20px;
    text-align:center;
    cursor:pointer;
    transition:0.3s;
}}

.card:hover {{
    transform:scale(1.05);
    box-shadow:0 0 25px gold;
}}

.avatar {{
    width:70px;
    height:70px;
    border-radius:50%;
    border:3px solid gold;
    margin:auto;
    margin-bottom:10px;
    box-shadow:0 0 20px gold;
}}

.name {{
    font-weight:bold;
}}

.value {{
    color:#aaa;
    font-size:14px;
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
    width:80%;
    max-width:900px;
    background:#0d1425;
    padding:30px;
    border-radius:20px;
    position:relative;
}}

.close {{
    position:absolute;
    top:15px;
    right:15px;
    font-size:20px;
    cursor:pointer;
}}

.box {{
    background:#111;
    padding:15px;
    border-radius:10px;
    margin:10px 0;
}}

</style>
</head>

<body>

<div class="container">

<div class="filters">
<div class="filter" onclick="setMode('power')">⚡ POWER</div>
<div class="filter" onclick="setMode('kill')">🔥 KILL</div>
<div class="filter" onclick="setMode('dead')">💀 DEAD</div>
</div>

<div class="grid" id="grid"></div>

</div>

<div class="modal" id="modal">
<div class="profile" id="profile">
<div class="close" onclick="closeProfile()">✖</div>
<div id="profileContent"></div>
</div>
</div>

<script>

let data = {df.to_dict(orient="records")};
let mode = "power";

function render() {{
    let sorted = [...data].sort((a,b)=>b[mode]-a[mode]);

    let html = "";

    sorted.forEach((p,i)=>{{
        html += `
        onclick='openProfile(${{JSON.stringify(p)}}, ${{i+1}})'
            <img class="avatar" src="https://api.dicebear.com/7.x/adventurer/png?seed=${{p.name}}">
            <div class="name">${{p.name}}</div>
            <div class="value">${{p[mode].toLocaleString()}}</div>
        </div>
        `;
    }});

    document.getElementById("grid").innerHTML = html;
}}

function setMode(m) {{
    mode = m;
    render();
}}

function openProfile(p, rank) {{

    document.getElementById("modal").style.display="flex";

    document.getElementById("profileContent").innerHTML = `
        <h2>${{p.name}}</h2>

        <div class="box">🆔 ID: ${{p.id}}</div>
        <div class="box">🏰 Alliance: ${{p.alliance}}</div>
        <div class="box">🏆 Rank: #${{rank}}</div>
        <div class="box">⚡ Power: ${{p.power.toLocaleString()}}</div>
        <div class="box">🔥 Kill: ${{p.kill.toLocaleString()}}</div>
        <div class="box">💀 Dead: ${{p.dead.toLocaleString()}}</div>

        <h3>🔥 KPI Kill</h3>
        <div class="box">0 / 0 (0%)</div>

        <h3>💀 KPI Dead</h3>
        <div class="box">0 / 0 (0%)</div>
    `;
}}

function closeProfile() {{
    document.getElementById("modal").style.display="none";
}}

render();

</script>

</body>
</html>
"""

components.html(html, height=1000)
