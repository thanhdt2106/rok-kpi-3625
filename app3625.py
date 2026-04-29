import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== HIDE STREAMLIT =====
st.markdown("""
<style>
#MainMenu, header, footer {visibility:hidden;}
.block-container {padding-top:0;}
</style>
""", unsafe_allow_html=True)

# ===== CONFIG =====
SHEET_ID = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
GID = "855089129"

# ===== LOAD DATA =====
@st.cache_data(ttl=60)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={GID}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ===== SEARCH =====
search = st.text_input("🔍 Nhập tên người chơi")

if search:
    df = df[df["Tên"].str.contains(search, case=False, na=False)]

# ===== SORT =====
df = df.sort_values(by="Tổng Tiêu Diệt", ascending=False).reset_index(drop=True)

# ===== KPI FUNCTION =====
def get_kpi_kill(pow):
    if pow > 100_000_000: return 600_000_000
    elif pow > 90_000_000: return 550_000_000
    elif pow > 80_000_000: return 450_000_000
    elif pow > 70_000_000: return 300_000_000
    elif pow > 60_000_000: return 250_000_000
    else: return 200_000_000

def get_kpi_dead(pow):
    if pow > 100_000_000: return 1_500_000
    elif pow > 90_000_000: return 1_200_000
    elif pow > 80_000_000: return 1_000_000
    elif pow > 70_000_000: return 800_000
    else: return 700_000

# ===== FARM DEAD LOGIC =====
def calculate_dead_with_farm(df):
    result = {}

    for name in df["Tên"].unique():
        same = df[df["Tên"] == name]

        main = same.loc[same["Tổng Tiêu Diệt"].idxmax()]
        total_dead = main["Điểm chết"]

        for _, r in same.iterrows():
            pow = r["Tổng Tiêu Diệt"]

            if pow > 40_000_000:
                total_dead += 700_000
            elif pow > 30_000_000:
                total_dead += 500_000
            elif pow > 20_000_000:
                total_dead += 300_000

        result[name] = total_dead

    return result

dead_map = calculate_dead_with_farm(df)

# ===== BUILD HTML =====
cards = ""

for i, row in df.head(40).iterrows():
    name = str(row["Tên"])
    pid = str(row["ID"])
    alliance = str(row["Liên Minh"])
    power = int(row["Tổng Tiêu Diệt"])
    dead = int(dead_map.get(name, row["Điểm chết"]))

    kill_kpi = get_kpi_kill(power)
    dead_kpi = get_kpi_dead(power)

    kill_percent = min(int(power / kill_kpi * 100), 100)
    dead_percent = min(int(dead / dead_kpi * 100), 100)

    avatar = f"https://api.dicebear.com/7.x/adventurer/png?seed={name}"

    cards += f"""
    <div class="card"
    onclick="openProfile('{name}','{pid}','{alliance}','{power}','{dead}','{i+1}','{kill_kpi}','{dead_kpi}','{avatar}')">
        <img src="{avatar}">
        <div>{name}</div>
        <small>#{i+1}</small>
    </div>
    """

# ===== HTML =====
html = f"""
<html>
<head>
<style>
body {{
background:#0b0f1a;
color:white;
font-family:sans-serif;
}}

.grid {{
display:grid;
grid-template-columns:repeat(auto-fill,160px);
gap:20px;
justify-content:center;
}}

.card {{
background:#111;
padding:15px;
border-radius:20px;
text-align:center;
cursor:pointer;
}}

.card img {{
width:80px;
border-radius:50%;
border:2px solid gold;
}}

.popup {{
position:fixed;
top:50%;
left:50%;
transform:translate(-50%,-50%);
width:70%;
background:#111;
padding:30px;
border-radius:20px;
display:none;
}}

.bar {{
height:12px;
background:#333;
border-radius:10px;
margin-top:5px;
}}

.fill {{
height:100%;
background:gold;
border-radius:10px;
}}
</style>
</head>

<body>

<div class="grid">
{cards}
</div>

<div class="popup" id="popup">

<h2 id="p_name"></h2>

<p>🆔 ID: <span id="p_id"></span></p>
<p>🏰 Alliance: <span id="p_alliance"></span></p>
<p>⚔ Kill: <span id="p_power"></span></p>
<p>💀 Dead: <span id="p_dead"></span></p>
<p>🏆 Rank: <span id="p_rank"></span></p>

<h3>🔥 KPI Kill</h3>
<div id="kill_text"></div>
<div class="bar"><div id="kill_bar" class="fill"></div></div>

<h3>💀 KPI Dead</h3>
<div id="dead_text"></div>
<div class="bar"><div id="dead_bar" class="fill"></div></div>

<button onclick="closeProfile()">Close</button>

</div>

<script>
function openProfile(name,id,alliance,power,dead,rank,killkpi,deadkpi,avatar){{
document.getElementById("popup").style.display="block";

document.getElementById("p_name").innerText=name;
document.getElementById("p_id").innerText=id;
document.getElementById("p_alliance").innerText=alliance;
document.getElementById("p_power").innerText=Number(power).toLocaleString();
document.getElementById("p_dead").innerText=Number(dead).toLocaleString();
document.getElementById("p_rank").innerText=rank;

let kpercent=Math.min(power/killkpi*100,100);
let dpercent=Math.min(dead/deadkpi*100,100);

document.getElementById("kill_text").innerText=
Number(power).toLocaleString()+" / "+Number(killkpi).toLocaleString()+" ("+Math.round(kpercent)+"%)";

document.getElementById("dead_text").innerText=
Number(dead).toLocaleString()+" / "+Number(deadkpi).toLocaleString()+" ("+Math.round(dpercent)+"%)";

document.getElementById("kill_bar").style.width=kpercent+"%";
document.getElementById("dead_bar").style.width=dpercent+"%";
}}

function closeProfile(){{
document.getElementById("popup").style.display="none";
}}
</script>

</body>
</html>
"""

components.html(html, height=900)
