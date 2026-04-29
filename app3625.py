import streamlit as st
import streamlit.components.v1 as components

# ================= CONFIG =================
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# ================= XOÁ SIDEBAR THẬT =================
st.markdown("""
<style>
section[data-testid="stSidebar"] {display:none !important;}
[data-testid="stSidebarNav"] {display:none !important;}
header {display:none !important;}
footer {display:none !important;}
#MainMenu {visibility:hidden;}

.block-container {
    padding:0 !important;
    max-width:100% !important;
}

[data-testid="stAppViewContainer"] {
    margin-left:0 !important;
}
</style>
""", unsafe_allow_html=True)

# ================= HTML UI =================
html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family: 'Segoe UI', sans-serif;
}

body{
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background: radial-gradient(circle at top,#0b1a2a,#050b12);
}

/* CARD */
.card{
    width:65vw;
    height:65vh;
    border-radius:30px;
    overflow:hidden;
    position:relative;
    box-shadow:0 0 60px rgba(255,180,0,0.2);
}

/* BACKGROUND */
.card::before{
    content:"";
    position:absolute;
    inset:0;
    background:url("https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true") center/cover;
    filter:brightness(0.9);
}

/* OVERLAY */
.card::after{
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.75));
}

/* CONTENT */
.content{
    position:relative;
    z-index:2;
    height:100%;
    padding:40px;
    color:white;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
}

/* TOP */
.top{
    display:flex;
    align-items:center;
    gap:20px;
}

.avatar{
    width:90px;
    height:90px;
    border-radius:50%;
    border:3px solid gold;
    box-shadow:0 0 25px gold;
}

.name{
    font-size:28px;
    color:#ffd700;
}

/* INFO */
.info{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:15px;
}

.box{
    background:rgba(0,0,0,0.4);
    padding:12px;
    border-radius:12px;
    backdrop-filter:blur(6px);
}

.label{font-size:12px;opacity:.6;}
.value{font-size:16px;margin-top:5px;}

/* STATS */
.stats{
    display:flex;
    gap:20px;
}

.stat{
    flex:1;
    background:rgba(0,0,0,0.45);
    padding:25px;
    border-radius:18px;
    text-align:center;
    backdrop-filter:blur(10px);
}

.rank{
    border:2px solid gold;
    box-shadow:0 0 25px gold;
}

.icon{font-size:22px;margin-bottom:10px;}
.stat-value{font-size:20px;}
.sub{font-size:13px;opacity:.6;}

</style>
</head>

<body>

<div class="card">
    <div class="content">

        <div class="top">
            <img src="https://i.pravatar.cc/150" class="avatar">
            <div class="name">L Gạo Nút</div>
        </div>

        <div class="info">
            <div class="box">
                <div class="label">ID</div>
                <div class="value">16925269</div>
            </div>

            <div class="box">
                <div class="label">Alliance</div>
                <div class="value">[FT-D]</div>
            </div>

            <div class="box">
                <div class="label">Kill</div>
                <div class="value">5,826,515,379</div>
            </div>

            <div class="box">
                <div class="label">Dead</div>
                <div class="value">3,418,388,660</div>
            </div>
        </div>

        <div class="stats">

            <div class="stat rank">
                <div class="icon">🏆</div>
                <div class="stat-value">#12</div>
                <div class="sub">Rank</div>
            </div>

            <div class="stat">
                <div class="icon">🔥</div>
                <div class="stat-value">5.8B</div>
                <div class="sub">38%</div>
            </div>

            <div class="stat">
                <div class="icon">💀</div>
                <div class="stat-value">3.4B</div>
                <div class="sub">28%</div>
            </div>

        </div>

    </div>
</div>

</body>
</html>
"""

# ================= RENDER =================
components.html(html, height=900, scrolling=False)
