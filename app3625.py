import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ẨN UI STREAMLIT
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none;}
header {visibility:hidden;}
footer {visibility:hidden;}
.block-container {padding:0 !important; max-width:100% !important;}
</style>
""", unsafe_allow_html=True)

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
    font-family:system-ui;
}

/* ===== BODY ===== */
body{
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:#05080c;
}

/* ===== CARD ===== */
.card{
    width:420px;
    border-radius:30px;
    background:#081520;
    box-shadow:0 30px 90px rgba(0,0,0,0.9);
    border:1px solid rgba(255,215,0,0.2);
    color:white;
    overflow:visible;
    position:relative;
}

/* ===== HERO ===== */
.hero{
    height:280px;
    background:url('https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true');
    background-size:cover;
    background-position:center 50%;
    position:relative;
    border-top-left-radius:20px;
    border-top-right-radius:20px;
}

/* overlay */
.hero::after{
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(to bottom, rgba(0,0,0,0.4), #081520);
}

/* ===== AVATAR ===== */
.avatar-wrap{
    position:absolute;
    bottom:-70px;
    left:50%;
    transform:translateX(-50%);
    z-index:10;
}

/* 🔥 FIRE AURA */
.avatar-wrap::before{
    content:"";
    position:absolute;
    top:50%;
    left:50%;
    width:200px;
    height:200px;
    transform:translate(-50%,-50%);
    border-radius:50%;
    background: radial-gradient(circle, rgba(255,180,0,1), rgba(255,80,0,0.4), transparent 70%);
    filter:blur(25px);
    animation:fire 1.5s infinite alternate;
}

/* RING */
.avatar{
    width:120px;
    height:120px;
    border-radius:50%;
    border:4px solid #FFD700;
    position:relative;
    z-index:2;
}

/* ===== FIRE ANIMATION ===== */
@keyframes fire{
    0%{transform:translate(-50%,-50%) scale(1); opacity:0.7;}
    100%{transform:translate(-50%,-50%) scale(1.2); opacity:1;}
}

/* ===== CONTENT ===== */
.content{
    padding-top:100px;
    padding-bottom:25px;
    padding-left:25px;
    padding-right:25px;
}

/* NAME */
.name{
    text-align:center;
    font-size:26px;
    font-weight:800;
    color:#FFD700;
    text-shadow:0 0 15px rgba(255,200,0,0.8);
    margin-bottom:25px;
}

/* ===== STATS ===== */
.stats{
    border-radius:20px;
    padding:15px;
    background:rgba(0,0,0,0.5);
    border:1px solid rgba(255,215,0,0.15);
}

.row{
    display:flex;
    justify-content:space-between;
    padding:12px 5px;
    border-bottom:1px solid rgba(255,255,255,0.08);
}

.row:last-child{
    border-bottom:none;
}

.row span{
    color:#aaa;
}

/* ===== FOOTER ===== */
.footer{
    display:flex;
    gap:12px;
    margin-top:20px;
}

.box{
    flex:1;
    padding:18px;
    border-radius:18px;
    background:rgba(0,0,0,0.5);
    border:1px solid rgba(255,215,0,0.2);
    text-align:center;
    position:relative;
}

/* 🔥 RANK #1 EFFECT */
.box:first-child{
    box-shadow:0 0 25px rgba(255,200,0,0.6);
    border:2px solid #FFD700;
}

/* glow animation */
.box:first-child::before{
    content:"";
    position:absolute;
    inset:-2px;
    border-radius:18px;
    background:linear-gradient(45deg, gold, orange, gold);
    z-index:-1;
    filter:blur(10px);
    opacity:0.7;
    animation:glow 2s infinite linear;
}

@keyframes glow{
    0%{filter:blur(5px);}
    50%{filter:blur(15px);}
    100%{filter:blur(5px);}
}

.dot{
    width:35px;
    height:35px;
    background:#FFD700;
    border-radius:50%;
    margin:auto;
    margin-bottom:10px;
}

</style>
</head>

<body>

<div class="card">

    <div class="hero">
        <div class="avatar-wrap">
            <img src="https://i.pravatar.cc/150?img=12" class="avatar">
        </div>
    </div>

    <div class="content">

        <div class="name">Louis Noob</div>

        <div class="stats">
            <div class="row"><span>ID</span><b>71428274</b></div>
            <div class="row"><span>Alliance</span><b>[FT-D]</b></div>
            <div class="row"><span>Power</span><b>87M</b></div>
            <div class="row"><span>Kill</span><b>6.1B</b></div>
            <div class="row"><span>Dead</span><b>1.2B</b></div>
        </div>

        <div class="footer">
            <div class="box"><div class="dot"></div>#1</div>
            <div class="box"><div class="dot"></div>85%</div>
            <div class="box"><div class="dot"></div>92%</div>
        </div>

    </div>

</div>

</body>
</html>
"""

components.html(html, height=900)
