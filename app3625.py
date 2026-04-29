import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ====== ẨN STREAMLIT ======
st.set_page_config(layout="wide")
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none}
header, footer {display:none}
</style>
""", unsafe_allow_html=True)

# ====== LOAD DATA ======
@st.cache_data(ttl=60)
def load_data():
    SHEET_ID = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    GID = "855089129"

    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
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

    for col in ["Kill", "Dead", "Power"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

df = load_data()

# ===== KPI =====
def get_kpi_kill(power):
    if power >= 100_000_000: return 600_000_000
    elif power >= 90_000_000: return 550_000_000
    elif power >= 80_000_000: return 450_000_000
    elif power >= 70_000_000: return 300_000_000
    elif power >= 60_000_000: return 250_000_000
    else: return 200_000_000

def get_kpi_dead(power):
    if power >= 100_000_000: return 1_500_000
    elif power >= 90_000_000: return 1_200_000
    elif power >= 80_000_000: return 1_000_000
    elif power >= 70_000_000: return 800_000
    else: return 700_000

# ===== FARM DEAD =====
def calc_dead(df):
    result = {}
    for name in df["Name"].unique():
        p = df[df["Name"] == name]
        main = p.sort_values("Power", ascending=False).iloc[0]
        total = main["Dead"]

        for _, r in p.iterrows():
            if r["Power"] < main["Power"]:
                if r["Power"] >= 40_000_000: total += 700_000
                elif r["Power"] >= 30_000_000: total += 500_000
                elif r["Power"] >= 20_000_000: total += 300_000

        result[name] = total
    return result

dead_map = calc_dead(df)

# ===== SORT TYPE =====
sort_type = st.session_state.get("sort", "Power")

# ===== HTML CARDS =====
cards = ""
df_sorted = df.sort_values(sort_type, ascending=False).reset_index(drop=True)

for i, row in df_sorted.iterrows():
    rank = i + 1
    name = row["Name"]
    value = int(row[sort_type])

    cards += f"""
    <div class="card" onclick="openProfile('{name}')">
        <div class="rank">#{rank}</div>
        <img src="https://api.dicebear.com/7.x/adventurer/png?seed={name}">
        <h3>{name}</h3>
        <p>{value:,}</p>
    </div>
    """

# ===== PROFILE =====
profiles = ""

for name in df["Name"].unique():
    p = df[df["Name"] == name].sort_values("Power", ascending=False).iloc[0]

    power = int(p["Power"])
    kill = int(p["Kill"])
    dead = int(dead_map[name])

    kpi_k = get_kpi_kill(power)
    kpi_d = get_kpi_dead(power)

    kp = int(kill / kpi_k * 100)
    dp = int(dead / kpi_d * 100)

    profiles += f"""
    <div id="profile-{name}" class="profile">
        <div class="box">

            <span class="close" onclick="closeProfile()">×</span>

            <div class="top">
                <img src="https://api.dicebear.com/7.x/adventurer/png?seed={name}">
                <h1>{name}</h1>
            </div>

            <div class="info">
                <div>ID<br><b>{p['ID']}</b></div>
                <div>Alliance<br><b>{p['Alliance']}</b></div>
                <div>Power<br><b>{power:,}</b></div>
                <div>Kill<br><b>{kill:,}</b></div>
                <div>Dead<br><b>{dead:,}</b></div>
            </div>

            <div class="kpi">
                <h3>🔥 KPI Kill</h3>
                <div class="bar"><div style="width:{kp}%"></div></div>
                <p>{kill:,}/{kpi_k:,} ({kp}%)</p>

                <h3>💀 KPI Dead</h3>
                <div class="bar"><div style="width:{dp}%"></div></div>
                <p>{dead:,}/{kpi_d:,} ({dp}%)</p>
            </div>

        </div>
    </div>
    """

# ===== HTML FULL =====
html = f"""
<html>
<head>
<style>
body {{
    background:#0b1220;
    color:white;
    font-family:sans-serif;
}}

.topbar {{
    display:flex;
    gap:20px;
    margin-bottom:20px;
}}

.boxbtn {{
    flex:1;
    padding:15px;
    background:#111;
    border-radius:15px;
    text-align:center;
    cursor:pointer;
}}

.boxbtn:hover {{
    box-shadow:0 0 15px gold;
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
    position:relative;
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
    top:0;
    left:0;
    width:100%;
    height:100%;
    display:none;
    background:rgba(0,0,0,0.9);
    justify-content:center;
    align-items:center;
}}

.box {{
    width:65%;
    background:#111;
    padding:30px;
    border-radius:20px;
}}

.top {{
    display:flex;
    gap:20px;
    align-items:center;
}}

.top img {{
    width:80px;
    border-radius:50%;
    border:4px solid gold;
}}

.info {{
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:10px;
    margin-top:20px;
}}

.bar {{
    height:10px;
    background:#333;
    border-radius:10px;
    margin:5px 0;
}}

.bar div {{
    height:100%;
    background:gold;
}}

.close {{
    float:right;
    cursor:pointer;
}}
</style>

<script>
function setSort(type){{
    window.parent.postMessage({{type:type}}, "*");
}}

function openProfile(name){{
    document.getElementById("profile-"+name).style.display="flex";
}}

function closeProfile(){{
    document.querySelectorAll(".profile").forEach(p=>p.style.display="none");
}}
</script>
</head>

<body>

<div class="topbar">
    <div class="boxbtn" onclick="setSort('Power')">⚡ POWER</div>
    <div class="boxbtn" onclick="setSort('Kill')">🔥 KILL</div>
    <div class="boxbtn" onclick="setSort('Dead')">💀 DEAD</div>
</div>

<div class="grid">
{cards}
</div>

{profiles}

</body>
</html>
"""

components.html(html, height=900)
