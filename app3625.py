import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== LOAD DATA =====
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi/export?format=csv&gid=855089129"
    df = pd.read_csv(url)

    df.columns = df.columns.str.strip()

    df = df.rename(columns={
        "Tên": "Name",
        "ID": "ID",
        "Liên Minh": "Alliance",
        "Tổng Tiêu Diệt": "Kill",
        "Điểm Chết": "Dead",
        "Sức Mạnh": "Power"
    })

    for col in ["Kill","Dead","Power"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

df = load_data()

# ===== KPI =====
def get_kpi_kill(p):
    if p>=100e6: return 600e6
    elif p>=90e6: return 550e6
    elif p>=80e6: return 450e6
    elif p>=70e6: return 300e6
    elif p>=60e6: return 250e6
    else: return 200e6

def get_kpi_dead(p):
    if p>=100e6: return 1.5e6
    elif p>=90e6: return 1.2e6
    elif p>=80e6: return 1e6
    elif p>=70e6: return 800e3
    else: return 700e3

# ===== FARM DEAD =====
def calc_dead(df):
    res={}
    for name in df["Name"].unique():
        p=df[df["Name"]==name]
        main=p.sort_values("Power",ascending=False).iloc[0]
        total=main["Dead"]

        for _,r in p.iterrows():
            if r["Power"]<main["Power"]:
                if r["Power"]>=40e6: total+=700000
                elif r["Power"]>=30e6: total+=500000
                elif r["Power"]>=20e6: total+=300000

        res[name]=int(total)
    return res

dead_map=calc_dead(df)

# ===== PASS DATA TO JS =====
df_json = df.to_json(orient="records")

# ===== HTML =====
html = f"""
<html>
<head>
<style>
body {{
    margin:0;
    background:linear-gradient(135deg,#0b1220,#05070d);
    color:white;
    font-family:sans-serif;
}}

.topbar {{
    display:flex;
    gap:10px;
    justify-content:center;
    padding:15px;
}}

.btn {{
    padding:10px 20px;
    background:#111;
    border-radius:10px;
    cursor:pointer;
}}

.btn:hover {{box-shadow:0 0 15px gold;}}

.search {{
    display:block;
    margin:10px auto;
    padding:10px;
    width:60%;
    border-radius:10px;
    border:none;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(170px,1fr));
    gap:20px;
    padding:20px;
}}

.card {{
    background:#111;
    padding:15px;
    border-radius:20px;
    text-align:center;
    cursor:pointer;
    position:relative;
    transition:0.3s;
}}

.card:hover {{
    transform:scale(1.05);
    box-shadow:0 0 20px gold;
}}

.rank {{
    position:absolute;
    top:10px;
    left:10px;
    color:gold;
}}

.card img {{
    width:70px;
    border-radius:50%;
    border:3px solid gold;
}}

.profile {{
    position:fixed;
    top:0;left:0;
    width:100%;height:100%;
    background:rgba(0,0,0,0.85);
    display:none;
    justify-content:center;
    align-items:center;
}}

.box {{
    width:65%;
    background:#111;
    padding:30px;
    border-radius:25px;
}}

.bar {{
    height:12px;
    background:#333;
    border-radius:10px;
    margin:5px 0;
}}

.fill {{
    height:100%;
    background:gold;
    border-radius:10px;
}}
</style>
</head>

<body>

<input class="search" placeholder="🔍 Search..." onkeyup="search(this.value)">

<div class="topbar">
<div class="btn" onclick="sortData('Power')">⚡ Power</div>
<div class="btn" onclick="sortData('Kill')">🔥 Kill</div>
<div class="btn" onclick="sortData('Dead')">💀 Dead</div>
</div>

<div id="grid" class="grid"></div>

<div id="profile" class="profile">
<div class="box">
<div id="content"></div>
<button onclick="closeProfile()">Close</button>
</div>
</div>

<script>

let data = {df_json};
let current = [...data];

// ===== SEARCH =====
function search(val){{
 val=val.toLowerCase();
 current=data.filter(x=>x.Name.toLowerCase().includes(val));
 render();
}}

// ===== SORT =====
function sortData(key){{
 current.sort((a,b)=>b[key]-a[key]);
 render();
}}

// ===== RENDER =====
function render(){{
 let html="";
 current.forEach((x,i)=>{{
 html+=`
 <div class="card" onclick="openProfile('${{x.Name}}',${{i+1}})">
 <div class="rank">#${{i+1}}</div>
 <img src="https://api.dicebear.com/7.x/adventurer/png?seed=${{x.Name}}">
 <h3>${{x.Name}}</h3>
 <p>${{Number(x.Power).toLocaleString()}}</p>
 </div>`;
 }});
 document.getElementById("grid").innerHTML=html;
}}

// ===== PROFILE =====
function openProfile(name,rank){{
 let p=data.find(x=>x.Name===name);

 let power=p.Power;
 let kill=p.Kill;
 let dead=p.Dead;

 let kpiK = power>=100e6?600e6:power>=90e6?550e6:power>=80e6?450e6:power>=70e6?300e6:power>=60e6?250e6:200e6;
 let kpiD = power>=100e6?1.5e6:power>=90e6?1.2e6:power>=80e6?1e6:power>=70e6?800000:700000;

 let kp = Math.min(100, Math.round(kill/kpiK*100));
 let dp = Math.min(100, Math.round(dead/kpiD*100));

 document.getElementById("profile").style.display="flex";

 document.getElementById("content").innerHTML=`
 <h2>${{p.Name}}</h2>
 <p>ID: ${{p.ID}}</p>
 <p>Alliance: ${{p.Alliance}}</p>
 <p>Rank: #${{rank}}</p>
 <p>Power: ${{Number(power).toLocaleString()}}</p>
 <p>Kill: ${{Number(kill).toLocaleString()}}</p>
 <p>Dead: ${{Number(dead).toLocaleString()}}</p>

 <h3>🔥 KPI Kill</h3>
 <div class="bar"><div class="fill" style="width:${{kp}}%"></div></div>
 <p>${{kill}} / ${{kpiK}} (${{kp}}%)</p>

 <h3>💀 KPI Dead</h3>
 <div class="bar"><div class="fill" style="width:${{dp}}%"></div></div>
 <p>${{dead}} / ${{kpiD}} (${{dp}}%)</p>
 `;
}}

function closeProfile(){{
 document.getElementById("profile").style.display="none";
}}

render();

</script>

</body>
</html>
"""

components.html(html, height=900)
