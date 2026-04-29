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
    player = df[df["Tên"].str.contains(name, case=False, na=False)]

    if len(player) == 0:
        st.error("Không tìm thấy")
        st.stop()

    p = player.iloc[0]

    max_kill = df["KPI_KILL"].max()
    max_dead = df["KPI_DEAD"].max()

    kill_pct = int(p["KPI_KILL"] / max_kill * 100)
    dead_pct = int(p["KPI_DEAD"] / max_dead * 100)

    html = f"""
    <html>
    <head>
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    body {{
        margin:0;
        background:#05080c;
        font-family:'Inter', sans-serif;
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
    }}

    .card {{
        width:420px;
        border-radius:24px;
        overflow:hidden;
        background:rgba(10,20,30,0.85);
        backdrop-filter:blur(12px);
        border:1px solid rgba(255,215,0,0.15);
        box-shadow:0 20px 60px rgba(0,0,0,0.8);
        color:#eaeaea;
    }}

    .hero {{
        height:280px;
        background:url('https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true') center/cover;
        position:relative;
    }}



    .avatar-wrap {{
        position:absolute;
        bottom:-45px;
        left:50%;
        transform:translateX(-50%);
        z-index:10;
    }}

    .avatar {{
        width:100px;
        height:100px;
        border-radius:50%;
        border:2px solid #d4af37;
        box-shadow:0 0 20px rgba(212,175,55,0.5);
    }}

    .content {{
        padding:70px 24px 24px;
    }}

    .name {{
        text-align:center;
        font-size:20px;
        font-weight:500;
        color:#d4af37;
        margin-bottom:20px;
        letter-spacing:0.5px;
    }}

    .row {{
        display:flex;
        justify-content:space-between;
        padding:10px 0;
        border-bottom:1px solid rgba(255,255,255,0.06);
        font-size:13px;
    }}

    .row span {{
        color:#9aa4ad;
    }}

    .row div {{
        color:#eaeaea;
    }}

    .footer {{
        display:flex;
        gap:10px;
        margin-top:20px;
    }}

    .box {{
        flex:1;
        padding:14px 10px;
        border-radius:14px;
        background:rgba(255,255,255,0.03);
        border:1px solid rgba(255,255,255,0.06);
        text-align:center;
        transition:0.25s;
    }}

    .box:hover {{
        transform:translateY(-3px);
        border-color:#d4af37;
    }}

    .box.rank {{
        border:1px solid #d4af37;
        background:rgba(212,175,55,0.05);
    }}

    .icon {{
        font-size:16px;
        margin-bottom:6px;
        opacity:0.8;
    }}

    .value {{
        font-size:13px;
        font-weight:400;
        margin-bottom:4px;
    }}

    .percent {{
        font-size:11px;
        color:#8c949c;
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

            <div class="row"><span>ID</span><div>{int(p["ID"])}</div></div>
            <div class="row"><span>Alliance</span><div>{p["Liên Minh"]}</div></div>
            <div class="row"><span>Kill</span><div>{p["KPI_KILL"]:,}</div></div>
            <div class="row"><span>Dead</span><div>{p["KPI_DEAD"]:,}</div></div>

            <div class="footer">

                <div class="box rank">
                    <div class="icon">🏆</div>
                    <div class="value">#{p["Rank"]}</div>
                </div>

                <div class="box">
                    <div class="icon">🔥</div>
                    <div class="value">{p["KPI_KILL"]:,}</div>
                    <div class="percent">{kill_pct}%</div>
                </div>

                <div class="box">
                    <div class="icon">💀</div>
                    <div class="value">{p["KPI_DEAD"]:,}</div>
                    <div class="percent">{dead_pct}%</div>
                </div>

            </div>

        </div>

    </div>

    </body>
    </html>
    """

    components.html(html, height=700)

else:
    st.info("Nhập tên để tìm player")
