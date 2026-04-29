import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

SHEET_ID = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
GID = "855089129"

@st.cache_data(ttl=60)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
    df = pd.read_csv(url)

    df.columns = df.columns.str.strip()

    df = df.rename(columns={
        "Tên": "name",
        "ID": "id",
        "Liên Minh": "alliance",
        "Tổng Tiêu Diệt": "kill",
        "Điểm Chết": "dead",
        "Sức Mạnh": "power"
    })

    for col in ["kill", "dead", "power"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

df = load_data()
data_json = json.dumps(df.to_dict(orient="records"))

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>

body {
    margin:0;
    background:#050b18;
    color:white;
    font-family:Arial;
}

.container {
    padding:30px;
}

.search {
    width:100%;
    padding:15px;
    border-radius:10px;
    border:none;
    background:#111;
    color:white;
    margin-bottom:20px;
}

.grid {
    display:grid;
    grid-template-columns:repeat(auto-fill, minmax(180px,1fr));
    gap:25px;
}

.card {
    background:#0d1425;
    padding:20px;
    border-radius:20px;
    text-align:center;
    cursor:pointer;
    transition:0.3s;
}

.card:hover {
    transform:scale(1.05);
    box-shadow:0 0 25px gold;
}

.avatar {
    width:70px;
    height:70px;
    border-radius:50%;
    border:3px solid gold;
    box-shadow:0 0 20px gold;
    margin-bottom:10px;
}

.modal {
    position:fixed;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.9);
    display:none;
    justify-content:center;
    align-items:center;
}

.profile {
    width:85%;
    max-width:900px;
    background:#0d1425;
    padding:30px;
    border-radius:20px;
    position:relative;
}

.close {
    position:absolute;
    right:15px;
    top:15px;
    cursor:pointer;
    font-size:20px;
}

.box {
    background:#111;
    padding:15px;
    border-radius:10px;
    margin:10px 0;
}

.bar {
    height:10px;
    background:#222;
    border-radius:10px;
    overflow:hidden;
    margin-top:10px;
}

.bar-fill {
    height:100%;
    background:gold;
}

</style>
</head>

<body>

<div class="container">

<input class="search" id="search" placeholder="🔍 Nhập tên..." onkeyup="render()">

<div class="grid" id="grid"></div>

</div>

<div class="modal" id="modal">
<div class="profile">
<div class="close" onclick="closeProfile()">✖</div>
<div id="profileContent"></div>
</div>
</div>

<script>

let data = DATA_PLACEHOLDER;

function getKillTarget(power){
    if(power >= 100000000) return 600000000;
    if(power >= 90000000) return 550000000;
    if(power >= 80000000) return 450000000;
    if(power >= 70000000) return 300000000;
    if(power >= 60000000) return 250000000;
    return 200000000;
}

function getDeadTarget(power){
    if(power >= 100000000) return 1500000;
    if(power >= 90000000) return 1200000;
    if(power >= 80000000) return 1000000;
    if(power >= 70000000) return 800000;
    return 700000;
}

function render(){
    let keyword = document.getElementById("search").value.toLowerCase();

    let filtered = data.filter(p =>
        p.name && p.name.toLowerCase().includes(keyword)
    );

    let sorted = filtered.sort((a,b)=>b.power-a.power);

    let html = "";

    sorted.forEach((p,i)=>{
        html += `
        <div class="card" onclick='openProfile(${JSON.stringify(p)}, ${i+1})'>
            <img class="avatar" src="https://api.dicebear.com/7.x/adventurer/png?seed=${p.name}">
            <div>${p.name}</div>
            <div>${Number(p.power).toLocaleString()}</div>
        </div>
        `;
    });

    document.getElementById("grid").innerHTML = html;
}

function openProfile(p, rank){

    let killTarget = getKillTarget(p.power);
    let deadTarget = getDeadTarget(p.power);

    let killPercent = Math.min((p.kill / killTarget)*100, 100);
    let deadPercent = Math.min((p.dead / deadTarget)*100, 100);

    document.getElementById("modal").style.display="flex";

    document.getElementById("profileContent").innerHTML = `
        <div style="text-align:center">
            <img class="avatar" src="https://api.dicebear.com/7.x/adventurer/png?seed=${p.name}">
            <h2>${p.name}</h2>
        </div>

        <div class="box">🆔 ${p.id}</div>
        <div class="box">🏰 ${p.alliance}</div>
        <div class="box">🏆 Rank #${rank}</div>
        <div class="box">⚡ ${Number(p.power).toLocaleString()}</div>
        <div class="box">🔥 ${Number(p.kill).toLocaleString()}</div>
        <div class="box">💀 ${Number(p.dead).toLocaleString()}</div>

        <h3>🔥 KPI Kill</h3>
        <div>${Number(p.kill).toLocaleString()} / ${killTarget.toLocaleString()} (${killPercent.toFixed(0)}%)</div>
        <div class="bar"><div class="bar-fill" style="width:${killPercent}%"></div></div>

        <h3>💀 KPI Dead</h3>
        <div>${Number(p.dead).toLocaleString()} / ${deadTarget.toLocaleString()} (${deadPercent.toFixed(0)}%)</div>
        <div class="bar"><div class="bar-fill" style="width:${deadPercent}%"></div></div>
    `;
}

function closeProfile(){
    document.getElementById("modal").style.display="none";
}

render();

</script>

</body>
</html>
"""

html = html.replace("DATA_PLACEHOLDER", data_json)

components.html(html, height=1000)
