import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(layout="wide")

# ================= LOAD DATA =================
@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid = "855089129"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)

    df.columns = df.columns.str.strip()

    rename_map = {
        "Tên": "Name",
        "Liên Minh": "Alliance",
        "Tổng Tiêu Diệt": "Kill",
        "Điểm chết": "Dead",
        "Sức Mạnh": "Power",
        "ID": "ID"
    }

    for k, v in rename_map.items():
        if k in df.columns:
            df.rename(columns={k: v}, inplace=True)

    return df

df = load_data()

# ================= HTML BUILD =================
cards = ""
for i, row in df.iterrows():
    name = str(row.get("Name", "Unknown"))
    power = int(row.get("Power", 0))
    kill = int(row.get("Kill", 0))
    dead = int(row.get("Dead", 0))
    alliance = str(row.get("Alliance", "-"))
    pid = str(row.get("ID", "-"))

    cards += f"""
    <div class="card" onclick="openProfile({i})">
        <img src="https://api.dicebear.com/7.x/adventurer/png?seed={name}">
        <div class="name">{name}</div>
        <div class="power">{power:,}</div>
    </div>
    """

# ================= HTML =================
html = f"""
<html>
<head>
<style>
body {{
    margin:0;
    background:#0b0f1a;
    font-family:Arial;
    color:white;
}}

.title {{
    font-size:32px;
    font-weight:bold;
    padding:20px;
}}

.search {{
    width:90%;
    margin:0 auto;
    display:block;
    padding:12px;
    border-radius:10px;
    border:none;
    margin-bottom:20px;
}}

.toolbar {{
    display:flex;
    gap:10px;
    justify-content:center;
    margin-bottom:20px;
}}

.btn {{
    padding:10px 20px;
    border-radius:10px;
    background:#111;
    cursor:pointer;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(150px,1fr));
    gap:15px;
    padding:20px;
}}

.card {{
    background:#111;
    padding:15px;
    border-radius:15px;
    text-align:center;
    cursor:pointer;
    transition:0.2s;
}}

.card:hover {{
    transform:scale(1.05);
}}

.card img {{
    width:60px;
    border-radius:50%;
}}

.name {{
    margin-top:10px;
}}

.power {{
    color:gold;
    font-size:12px;
}}

/* PROFILE */
.profile {{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.9);
    display:none;
    align-items:center;
    justify-content:center;
}}

.profile-box {{
    width:60%;
    background:#111;
    padding:30px;
    border-radius:20px;
}}

.close {{
    float:right;
    cursor:pointer;
    font-size:20px;
}}
</style>
</head>

<body>

<div class="title">🔥 ROK DASHBOARD</div>

<input class="search" placeholder="Search player..." onkeyup="search(this.value)">

<div class="toolbar">
    <div class="btn" onclick="sortData('Power')">Power</div>
    <div class="btn" onclick="sortData('Kill')">Kill</div>
    <div class="btn" onclick="sortData('Dead')">Dead</div>
</div>

<div id="grid" class="grid">
{cards}
</div>

<div id="profile" class="profile">
    <div class="profile-box">
        <div class="close" onclick="closeProfile()">X</div>
        <div id="profileContent"></div>
    </div>
</div>

<script>

let data = {df.to_json(orient="records")};
let current = [...data];

// SEARCH
function search(val) {{
    val = val.toLowerCase();
    current = data.filter(x => (x.Name || "").toLowerCase().includes(val));
    render();
}}

// SORT
function sortData(key) {{
    current.sort((a,b)=>b[key]-a[key]);
    render();
}}

// RENDER
function render() {{
    let html = "";
    current.forEach((x,i)=>{{
        html += `
        <div class="card" onclick="openProfile(${i})">
            <img src="https://api.dicebear.com/7.x/adventurer/png?seed=${{x.Name}}">
            <div class="name">${{x.Name}}</div>
            <div class="power">${{Number(x.Power).toLocaleString()}}</div>
        </div>`;
    }});
    document.getElementById("grid").innerHTML = html;
}}

// PROFILE
function openProfile(i) {{
    let p = current[i];

    document.getElementById("profile").style.display="flex";

    document.getElementById("profileContent").innerHTML = `
        <h2>${{p.Name}}</h2>
        <p>ID: ${{p.ID}}</p>
        <p>Alliance: ${{p.Alliance}}</p>
        <p>Power: ${{Number(p.Power).toLocaleString()}}</p>
        <p>Kill: ${{Number(p.Kill).toLocaleString()}}</p>
        <p>Dead: ${{Number(p.Dead).toLocaleString()}}</p>
    `;
}}

function closeProfile() {{
    document.getElementById("profile").style.display="none";
}}

</script>

</body>
</html>
"""

components.html(html, height=900, scrolling=True)
