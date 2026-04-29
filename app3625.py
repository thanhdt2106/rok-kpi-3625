import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== HIDE SIDEBAR + BACKGROUND =====
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none;}
.block-container {padding:0;}
body {background:#000;}
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

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    body {{
        margin:0;
        font-family:'Inter', sans-serif;
        background:black;
    }}

    .wrapper {{
        width:100%;
        height:100vh;
        background:url('https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true') center/cover no-repeat;
        display:flex;
        justify-content:center;
        align-items:center;
    }}

    /* ===== CARD FULL WIDTH ===== */
    .card {{
        width:90%;
        max-width:1200px;
        border-radius:30px;
        padding:40px;
        color:white;

        background:rgba(0,0,0,0.45);
        backdrop-filter:blur(6px);
        border:1px solid rgba(255,215,0,0.3);

        box-shadow:0 40px 100px rgba(0,0,0,0.9);
    }}

    /* ===== HEADER ===== */
    .top {{
        display:flex;
        align-items:center;
        gap:30px;
    }}

    .avatar {{
        width:110px;
        height:110px;
        border-radius:50%;
        border:3px solid gold;
        box-shadow:0 0 30px rgba(255,215,0,0.8);
    }}

    .name {{
        font-size:28px;
        color:#FFD700;
        font-weight:500;
    }}

    /* ===== INFO GRID ===== */
    .grid {{
        display:grid;
        grid-template-columns:1fr 1fr;
        margin-top:25px;
        gap:15px 40px;
        font-size:14px;
    }}

    .label {{
        color:#bbb;
    }}

    .value {{
        text-align:right;
        color:#fff;
    }}

    .row {{
        display:flex;
        justify-content:space-between;
        border-bottom:1px solid rgba(255,255,255,0.1);
        padding:8px 0;
    }}

    /* ===== FOOTER ===== */
    .footer {{
        display:flex;
        gap:20px;
        margin-top:30px;
    }}

    .box {{
        flex:1;
        padding:20px;
        border-radius:18px;
        background:rgba(0,0,0,0.5);
        text-align:center;
        border:1px solid rgba(255,255,255,0.1);
    }}

    .box.rank {{
        border:2px solid gold;
        box-shadow:0 0 25px rgba(255,215,0,0.5);
    }}

    .icon {{
        font-size:20px;
        margin-bottom:8px;
    }}

    .big {{
        font-size:16px;
    }}

    .percent {{
        font-size:12px;
        color:#aaa;
    }}

    </style>
    </head>

    <body>

    <div class="wrapper">

        <div class="card">

            <div class="top">
                <img src="https://i.pravatar.cc/150?u={p["Tên"]}" class="avatar">
                <div class="name">{p["Tên"]}</div>
            </div>

            <div class="grid">
                <div class="row"><span class="label">ID</span><span class="value">{int(p["ID"])}</span></div>
                <div class="row"><span class="label">Alliance</span><span class="value">{p["Liên Minh"]}</span></div>
                <div class="row"><span class="label">Kill</span><span class="value">{p["KPI_KILL"]:,}</span></div>
                <div class="row"><span class="label">Dead</span><span class="value">{p["KPI_DEAD"]:,}</span></div>
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

    components.html(html, height=900)

else:
    st.info("Nhập tên để tìm player")
