import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== LOAD DATA =====
sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
gid = "855089129"

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
df = pd.read_csv(url)

# ===== CLEAN DATA =====
df["Tổng Tiêu Diệt"] = pd.to_numeric(df["Tổng Tiêu Diệt"], errors="coerce")
df["Sức Mạnh"] = pd.to_numeric(df["Sức Mạnh"], errors="coerce")

# ===== KPI CALC =====
df["KPI_KILL"] = df["Tổng Tiêu Diệt"]
df["KPI_DEAD"] = df["T5"]

# rank theo kill
df = df.sort_values("KPI_KILL", ascending=False)
df["Rank"] = range(1, len(df)+1)

# ===== SEARCH =====
player_name = st.text_input("🔍 Nhập tên người chơi")

if player_name:
    player = df[df["Tên"].str.contains(player_name, case=False, na=False)]

    if len(player) == 0:
        st.error("Không tìm thấy người chơi")
        st.stop()

    p = player.iloc[0]

    # KPI %
    max_kill = df["KPI_KILL"].max()
    max_dead = df["KPI_DEAD"].max()

    kill_pct = int(p["KPI_KILL"] / max_kill * 100)
    dead_pct = int(p["KPI_DEAD"] / max_dead * 100)

    html = f"""
    <html>
    <head>
    <style>

    body {{
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
        background:#05080c;
        font-family:system-ui;
    }}

    .card {{
        width:420px;
        border-radius:30px;
        background:#081520;
        color:white;
        overflow:visible;
        position:relative;
    }}

    .hero {{
        height:220px;
        background:url('https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true');
        background-size:cover;
        position:relative;
    }}

    .avatar-wrap {{
        position:absolute;
        bottom:-60px;
        left:50%;
        transform:translateX(-50%);
    }}

    .avatar {{
        width:110px;
        height:110px;
        border-radius:50%;
        border:3px solid gold;
    }}

    .content {{
        padding-top:80px;
        padding:80px 20px 20px;
    }}

    .name {{
        text-align:center;
        font-size:24px;
        color:gold;
        margin-bottom:20px;
    }}

    .row {{
        display:flex;
        justify-content:space-between;
        padding:10px 0;
        border-bottom:1px solid rgba(255,255,255,0.1);
    }}

    .footer {{
        display:flex;
        gap:10px;
        margin-top:20px;
    }}

    .box {{
        flex:1;
        background:#111;
        padding:15px;
        border-radius:15px;
        text-align:center;
        position:relative;
    }}

    .box:first-child {{
        border:2px solid gold;
    }}

    .dot {{
        width:25px;
        height:25px;
        background:gold;
        border-radius:50%;
        margin:auto;
        margin-bottom:8px;
    }}

    .btn {{
        position:absolute;
        right:10px;
        top:10px;
        background:red;
        width:20px;
        height:20px;
        border-radius:50%;
        font-size:12px;
        color:white;
        display:flex;
        align-items:center;
        justify-content:center;
        cursor:pointer;
    }}

    </style>
    </head>

    <body>

    <div class="card">

        <div class="hero">
            <div class="avatar-wrap">
                <img src="https://i.pravatar.cc/150?u={p["Tên"]}" class="avatar">
            </div>
        </div>

        <div class="content">

            <div class="name">{p["Tên"]}</div>

            <div class="row"><span>ID</span><b>{int(p["ID"])}</b></div>
            <div class="row"><span>Alliance</span><b>{p["Liên Minh"]}</b></div>
            <div class="row">
                <span>Kill</span>
                <b>{p["KPI_KILL"]:,}</b>
                <div class="btn">!</div>
            </div>
            <div class="row">
                <span>Dead</span>
                <b>{p["KPI_DEAD"]:,}</b>
                <div class="btn">!</div>
            </div>

            <div class="footer">
                <div class="box">
                    <div class="dot"></div>
                    #{p["Rank"]}
                </div>

                <div class="box">
                    <div class="dot"></div>
                    {p["KPI_KILL"]:,}<br>{kill_pct}%
                </div>

                <div class="box">
                    <div class="dot"></div>
                    {p["KPI_DEAD"]:,}<br>{dead_pct}%
                </div>
            </div>

        </div>

    </div>

    </body>
    </html>
    """

    components.html(html, height=750)

else:
    st.info("Nhập tên để tìm player")
