import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== FIX UI =====
st.markdown("""
<style>
section[data-testid="stSidebar"] {display: none !important;}
header {visibility: hidden;}
.block-container {padding:0;}
html, body {background:transparent;}
</style>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
gid = "855089129"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

df = pd.read_csv(url)

df["Tổng Tiêu Diệt"] = pd.to_numeric(df["Tổng Tiêu Diệt"], errors="coerce")
df["T5"] = pd.to_numeric(df["T5"], errors="coerce")

df["KPI_KILL"] = df["Tổng Tiêu Diệt"]
df["KPI_DEAD"] = df["T5"]

df = df.sort_values("KPI_KILL", ascending=False)
df["Rank"] = range(1, len(df)+1)

# ===== SEARCH =====
name = st.text_input("🔍 Nhập tên người chơi")

if name:
    p = df[df["Tên"].str.contains(name, case=False, na=False)].iloc[0]

    max_kill = df["KPI_KILL"].max()
    max_dead = df["KPI_DEAD"].max()

    kill_pct = int(p["KPI_KILL"] / max_kill * 100)
    dead_pct = int(p["KPI_DEAD"] / max_dead * 100)

    html = f"""
    <html>
    <head>
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');

    body {{
        margin:0;
        font-family:'Inter', sans-serif;
    }}

    /* ===== CENTER ===== */
    

    /* ===== CARD (ẢNH NẰM Ở ĐÂY) ===== */
    .card {{
       width:95%;
max-width:1400px;

    min-height:500px; /* thêm dòng này */

        /* 👉 ẢNH NẰM TRONG CARD */
        background:
       linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.6)),
        url('https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true');

        background-size:cover;
        background-position:center;

        box-shadow:0 30px 80px rgba(0,0,0,0.8);
    }}

    /* ===== HEADER ===== */
    .top {{
        display:flex;
        align-items:center;
        gap:20px;
    }}

    .avatar {{
        width:90px;
        height:90px;
        border-radius:50%;
        border:3px solid gold;
        box-shadow:0 0 25px gold;
    }}

    .name {{
        font-size:26px;
        color:#FFD700;
    }}

    /* ===== GRID ===== */
    .grid {{
        margin-top:25px;
        display:grid;
        grid-template-columns:1fr 1fr;
        gap:15px 40px;
    }}

    .row {{
        display:flex;
        justify-content:space-between;
        border-bottom:1px solid rgba(255,255,255,0.2);
        padding:8px 0;
        font-size:14px;
    }}

    .label {{
        color:#ccc;
    }}

    .value {{
        color:white;
    }}

    /* ===== BOX ===== */
    .footer {{
        display:flex;
        gap:20px;
        margin-top:30px;
    }}

    .box {{
        flex:1;
        padding:20px;
        border-radius:18px;
        background:rgba(0,0,0,0.6);
        text-align:center;
        border:1px solid rgba(255,255,255,0.2);
    }}

    .rank {{
        border:2px solid gold;
        box-shadow:0 0 20px gold;
    }}

    .icon {{
        font-size:20px;
    }}

    .big {{
        font-size:15px;
        margin-top:5px;
    }}

    .percent {{
        font-size:12px;
        color:#bbb;
    }}

    </style>
    </head>

    <body>

    <div class="wrap">

        <div class="card">

            <div class="top">
                <img src="https://i.pravatar.cc/150?u={p["Tên"]}" class="avatar">
                <div class="name">{p["Tên"]}</div>
            </div>

            <div class="grid">
                <div class="row"><span class="label">ID</span><span>{int(p["ID"])}</span></div>
                <div class="row"><span class="label">Alliance</span><span>{p["Liên Minh"]}</span></div>
                <div class="row"><span class="label">Kill</span><span>{p["KPI_KILL"]:,}</span></div>
                <div class="row"><span class="label">Dead</span><span>{p["KPI_DEAD"]:,}</span></div>
            </div>

            <div class="footer">

                <div class="box rank">
                    <div class="icon">🏆</div>
                    <div class="big">#{p["Rank"]}</div>
                </div>

                <div class="box">
                    <div class="icon">🔥</div>
                    <div class="big">{p["KPI_KILL"]:,}</div>
                    <div class="percent">{kill_pct}%</div>
                </div>

                <div class="box">
                    <div class="icon">💀</div>
                    <div class="big">{p["KPI_DEAD"]:,}</div>
                    <div class="percent">{dead_pct}%</div>
                </div>

            </div>

        </div>

    </div>

    </body>
    </html>
    """

    components.html(html, height=700)
