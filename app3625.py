import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# ================= CONFIG =================
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# ================= HIDE SIDEBAR =================
st.markdown("""
<style>
section[data-testid="stSidebar"] {display:none !important;}
header {display:none !important;}
footer {display:none !important;}
#MainMenu {visibility:hidden;}

.block-container {
    padding:0 !important;
    max-width:100% !important;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
SHEET_ID = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
GID = "855089129"

url = f"https://opensheet.elk.sh/{SHEET_ID}/{GID}"

@st.cache_data(ttl=30)
def load_data():
    return pd.read_json(url)

df = load_data()

# ================= SEARCH =================
name_list = df["Tên"].dropna().tolist()
search = st.text_input("", placeholder="🔍 Nhập tên người chơi...")

player = df.iloc[0]

if search:
    result = df[df["Tên"].str.contains(search, case=False, na=False)]
    if not result.empty:
        player = result.iloc[0]

# ================= DATA =================
name = player.get("Tên","N/A")
pid = player.get("ID","N/A")
alliance = player.get("Liên Minh","N/A")

kill = int(player.get("Tổng Tiêu Diệt",0))
dead = int(player.get("Điểm Chết",0))

# RANK
df_sorted = df.sort_values(by="Tổng Tiêu Diệt", ascending=False)
rank = df_sorted.index.get_loc(player.name) + 1

# KPI (demo target)
kill_target = 15000000000
dead_target = 12000000000

kill_percent = min(100, int(kill/kill_target*100))
dead_percent = min(100, int(dead/dead_target*100))

# FORMAT
def fmt(n):
    return f"{n:,}"

def fmtB(n):
    return f"{n/1e9:.1f}B"

# ================= HTML =================
html = f"""
<!DOCTYPE html>
<html>
<head>
<style>

*{{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI;}}

body{{
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background: radial-gradient(circle at top,#0b1a2a,#050b12);
}}

.card{{
    width:65vw;
    height:65vh;
    border-radius:30px;
    overflow:hidden;
    position:relative;
    box-shadow:0 0 60px rgba(255,180,0,0.2);
}}

.card::before{{
    content:"";
    position:absolute;
    inset:0;
    background:url("https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true") center/cover;
    filter:brightness(0.9);
}}

.card::after{{
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.75));
}}

.content{{
    position:relative;
    z-index:2;
    height:100%;
    padding:40px;
    color:white;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
}}

.top{{
    display:flex;
    align-items:center;
    gap:20px;
}}

.avatar{{
    width:90px;
    height:90px;
    border-radius:50%;
    border:3px solid gold;
    box-shadow:0 0 25px gold;
}}

.name{{
    font-size:28px;
    color:#ffd700;
}}

.info{{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:15px;
}}

.box{{
    background:rgba(0,0,0,0.4);
    padding:12px;
    border-radius:12px;
    backdrop-filter:blur(6px);
}}

.label{{font-size:12px;opacity:.6;}}
.value{{font-size:16px;margin-top:5px;}}

.stats{{
    display:flex;
    gap:20px;
}}

.stat{{
    flex:1;
    background:rgba(0,0,0,0.45);
    padding:25px;
    border-radius:18px;
    text-align:center;
}}

.rank{{
    border:2px solid gold;
    box-shadow:0 0 25px gold;
}}

.bar{{height:6px;background:#222;border-radius:10px;margin-top:10px;overflow:hidden;}}
.fill{{height:100%;background:gold;}}

</style>
</head>

<body>

<div class="card">
<div class="content">

<div class="top">
<img src="https://i.pravatar.cc/150" class="avatar">
<div class="name">{name}</div>
</div>

<div class="info">
<div class="box"><div class="label">ID</div><div class="value">{pid}</div></div>
<div class="box"><div class="label">Alliance</div><div class="value">{alliance}</div></div>
<div class="box"><div class="label">Kill</div><div class="value">{fmt(kill)}</div></div>
<div class="box"><div class="label">Dead</div><div class="value">{fmt(dead)}</div></div>
</div>

<div class="stats">

<div class="stat rank">
<div>🏆</div>
<div>{rank}</div>
<div>Rank</div>
</div>

<div class="stat">
<div>🔥</div>
<div>{fmtB(kill)}</div>
<div>{kill_percent}%</div>
<div class="bar"><div class="fill" style="width:{kill_percent}%"></div></div>
</div>

<div class="stat">
<div>💀</div>
<div>{fmtB(dead)}</div>
<div>{dead_percent}%</div>
<div class="bar"><div class="fill" style="width:{dead_percent}%"></div></div>
</div>

</div>

</div>
</div>

</body>
</html>
"""

components.html(html, height=900)
