import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(layout="wide")

# ===== DATA DEMO =====
data = [
    {
        "name": "Louis Noob",
        "id": "71428274",
        "power": "87.424.868",
        "kill_total": "6.119.626.641",
        "kill_t5": "0",
        "kill_t4": "0",
        "rank": "#1",
        "kpi_kill": "85%",
        "kpi_deal": "92%",
        "avatar": "https://i.pravatar.cc/150?img=1"
    },
    {
        "name": "VICTORIUS",
        "id": "12345678",
        "power": "65.000.000",
        "kill_total": "3.200.000.000",
        "kill_t5": "100.000",
        "kill_t4": "500.000",
        "rank": "#2",
        "kpi_kill": "70%",
        "kpi_deal": "80%",
        "avatar": "https://i.pravatar.cc/150?img=2"
    }
]

df = pd.DataFrame(data)

# ===== SELECT PLAYER =====
st.title("🎮 ROK PLAYER DASHBOARD")

selected = st.selectbox("Chọn Player", df["name"])

player = df[df["name"] == selected].iloc[0]

# ===== PROFILE HTML =====
html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body{{margin:0;background:#072b3a;font-family:Arial;}}

/* HEADER */
.header{{
    background:linear-gradient(#ffd54f,#e6a700);
    height:220px;
    border-bottom-left-radius:25px;
    border-bottom-right-radius:25px;
    position:relative;
}}

/* AVATAR */
.avatar-wrap{{
    position:absolute;
    bottom:-70px;
    left:50%;
    transform:translateX(-50%);
    text-align:center;
}}

.avatar-frame{{
    width:130px;height:130px;border-radius:50%;
    padding:5px;
    background:conic-gradient(#ffcc00,#ff6600,#ffcc00);
    box-shadow:0 0 30px gold;
}}

.avatar{{
    width:100%;height:100%;
    border-radius:50%;
    background:url("{player['avatar']}") center/cover;
}}

.name{{
    margin-top:10px;
    color:white;
    font-size:20px;
    font-weight:bold;
    text-shadow:0 0 10px gold;
}}

.container{{margin-top:100px;padding:15px;}}

.energy{{color:white;font-size:14px;}}

.bar{{height:10px;background:#083544;border-radius:10px;overflow:hidden;margin-top:5px;}}

.fill{{width:45%;height:100%;background:linear-gradient(to right,#00ff87,#00c853);}}

/* PROFILE */
.profile{{
    margin-top:15px;
    background:linear-gradient(#1f6d8c,#15546b);
    border-radius:15px;
    padding:15px;
    color:white;
    border:2px solid rgba(255,255,255,0.08);
}}

/* ROW */
.row{{
    display:flex;
    justify-content:space-between;
    margin:6px 0;
    padding:8px 10px;
    background:rgba(255,255,255,0.05);
    border-radius:8px;
}}

.row span:last-child{{
    color:#ffd54f;
    font-weight:bold;
}}

/* MEDALS */
.medals{{display:flex;gap:10px;margin-top:15px;}}

.card{{
    flex:1;
    background:rgba(255,255,255,0.05);
    border-radius:12px;
    padding:10px;
    text-align:center;
}}

.icon{{
    width:60px;height:60px;border-radius:50%;
    background:radial-gradient(circle,#ffd700,#ff9800);
    margin:auto;
}}

</style>
</head>

<body>

<div class="header">
    <div class="avatar-wrap">
        <div class="avatar-frame">
            <div class="avatar"></div>
        </div>
        <div class="name">{player['name']}</div>
    </div>
</div>

<div class="container">

<div class="energy">
    Điểm hành động 471 / 1,850
    <div class="bar"><div class="fill"></div></div>
</div>

<div class="profile">

<div class="row"><span>ID</span><span>{player['id']}</span></div>
<div class="row"><span>Pow hiện tại</span><span>{player['power']}</span></div>
<div class="row"><span>Tổng kill tăng</span><span>{player['kill_total']}</span></div>
<div class="row"><span>Kill T5 tăng</span><span>{player['kill_t5']}</span></div>
<div class="row"><span>Kill T4 tăng</span><span>{player['kill_t4']}</span></div>

<div class="medals">
    <div class="card">
        <div class="icon"></div>
        <div>RANK</div>
        <b>{player['rank']}</b>
    </div>

    <div class="card">
        <div class="icon"></div>
        <div>KPI KILL</div>
        <b>{player['kpi_kill']}</b>
    </div>

    <div class="card">
        <div class="icon"></div>
        <div>KPI DEAL</div>
        <b>{player['kpi_deal']}</b>
    </div>
</div>

</div>
</div>

</body>
</html>
"""

components.html(html, height=900)
