import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== LOAD DATA =====
sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
gid = "855089129"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

df = pd.read_csv(url)

# ===== CLEAN =====
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

    body {{
        background:#05080c;
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
        font-family:system-ui;
    }}

    .card {{
        width:420px;
        border-radius:30px;
        overflow:hidden;
        background:rgba(10,20,30,0.9);
        backdrop-filter:blur(12px);
        box-shadow:0 25px 80px rgba(0,0,0,0.8);
        border:1px solid rgba(255,215,0,0.2);
        color:white;
    }}

    .hero {{
        height:220px;
        background:url('https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true') center/cover;
        position:relative;
    }}

    .hero::after {{
        content:"";
        position:absolute;
        inset:0;
        background:linear-gradient(to bottom, rgba(0,0,0,0.5), #081520);
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
        padding:80px 25px 25px;
    }}

    .name {{
        text-align:center;
        font-size:24px;
        font-weight:700;
        color:#FFD700;
        margin-bottom:25px;
    }}

    .row {{
        display:flex;
        justify-content:space-between;
        padding:12px 0;
        border-bottom:1px solid rgba(255,255,255,0.08);
    }}

    .footer {{
        display:flex;
        gap:12px;
        margin-top:20px;
    }}

    .box {{
        flex:1;
        padding:15px;
        border-radius:16px;
        background:rgba(255,255,255,0.03);
        text-align:center;
    }}

    .box.rank {{
        border:2px solid gold;
        box-shadow:0 0 15px rgba(255,215,0,0.5);
    }}

    .dot {{
        width:30px;
        height:30px;
        background:#FFD700;
        border-radius:50%;
        margin:auto;
        margin-bottom:8px;
    }}

    .percent {{
        color:#aaa;
        font-size:13px;
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
            <div class="row"><span>Kill</span><b>{p["KPI_KILL"]:,}</b></div>
            <div class="row"><span>Dead</span><b>{p["KPI_DEAD"]:,}</b></div>

            <div class="footer">
                <div class="box rank">
                    <div class="dot"></div>
                    #{p["Rank"]}
                </div>

                <div class="box">
                    <div class="dot"></div>
                    {p["KPI_KILL"]:,}
                    <div class="percent">{kill_pct}%</div>
                </div>

                <div class="box">
                    <div class="dot"></div>
                    {p["KPI_DEAD"]:,}
                    <div class="percent">{dead_pct}%</div>
                </div>
            </div>

        </div>

    </div>

    </body>
    </html>
    """

    components.html(html, height=720)

else:
    st.info("Nhập tên để tìm player")
