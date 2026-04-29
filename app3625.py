import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ================== CONFIG ==================
st.set_page_config(layout="wide")
st.markdown("<style>header, footer, .stDeployButton {display:none}</style>", unsafe_allow_html=True)

# ================== LOAD DATA ==================
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
        "Tổng Chết": "Dead",
        "Tổng Sức Mạnh": "Power"
    })

    for col in ["Kill", "Dead", "Power"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

df = load_data()

# ================== KPI ==================
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

def calculate_dead_with_farm(df):
    result = {}
    for name in df["Name"].unique():
        players = df[df["Name"] == name]
        main = players.sort_values("Power", ascending=False).iloc[0]
        total_dead = main["Dead"]

        for _, row in players.iterrows():
            if row["Power"] < main["Power"]:
                if row["Power"] >= 40_000_000:
                    total_dead += 700_000
                elif row["Power"] >= 30_000_000:
                    total_dead += 500_000
                elif row["Power"] >= 20_000_000:
                    total_dead += 300_000

        result[name] = total_dead
    return result

dead_map = calculate_dead_with_farm(df)

# ================== SEARCH ==================
search = st.text_input("🔍 Nhập tên người chơi")

df_show = df.copy()
if search:
    df_show = df[df["Name"].str.contains(search, case=False, na=False)]

# ================== HTML UI ==================
cards = ""

for i, row in df_show.iterrows():
    name = row["Name"]
    power = int(row["Power"])

    cards += f"""
    <div class="card" onclick="openProfile('{name}')">
        <img src="https://api.dicebear.com/7.x/adventurer/png?seed={name}">
        <h3>{name}</h3>
        <p>{power:,}</p>
    </div>
    """

# ================== PROFILE DATA ==================
profiles = ""

for name in df["Name"].unique():
    p = df[df["Name"] == name].sort_values("Power", ascending=False).iloc[0]

    power = int(p["Power"])
    kill = int(p["Kill"])
    dead = int(dead_map[name])

    kpi_kill = get_kpi_kill(power)
    kpi_dead = get_kpi_dead(power)

    kill_pct = min(100, int(kill / kpi_kill * 100))
    dead_pct = min(100, int(dead / kpi_dead * 100))

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
                <div>Dead<br><b>{dead:,}</b></div>
            </div>

            <div class="kpi">
                <h3>🔥 KPI Kill</h3>
                <div class="bar"><div style="width:{kill_pct}%"></div></div>
                <p>{kill:,} / {kpi_kill:,} ({kill_pct}%)</p>

                <h3>💀 KPI Dead</h3>
                <div class="bar"><div style="width:{dead_pct}%"></div></div>
                <p>{dead:,} / {kpi_dead:,} ({dead_pct}%)</p>
            </div>
        </div>
    </div>
    """

# ================== FINAL HTML ==================
html = f"""
<html>
<head>
<style>
body {{
    background:#0b1220;
    color:white;
    font-family:sans-serif;
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
}}

.card:hover {{
    transform:scale(1.05);
    box-shadow:0 0 20px gold;
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
    background:rgba(0,0,0,0.9);
    display:none;
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
    align-items:center;
    gap:20px;
}}

.top img {{
    width:80px;
    border-radius:50%;
    border:4px solid gold;
}}

.info {{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:15px;
    margin-top:20px;
}}

.kpi {{
    margin-top:30px;
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
    border-radius:10px;
}}

.close {{
    float:right;
    cursor:pointer;
    font-size:25px;
}}
</style>

<script>
function openProfile(name){{
    document.getElementById("profile-"+name).style.display="flex";
}}
function closeProfile(){{
    document.querySelectorAll(".profile").forEach(p=>p.style.display="none");
}}
</script>
</head>

<body>

<div class="grid">
{cards}
</div>

{profiles}

</body>
</html>
"""

components.html(html, height=900)
