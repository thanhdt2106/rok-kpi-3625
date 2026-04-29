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

/* ===== BACKGROUND NGOÀI ===== */
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
    overflow:hidden;
    background:rgba(10,20,30,0.85);
    backdrop-filter:blur(12px);
    box-shadow:0 30px 80px rgba(0,0,0,0.9);
    border:1px solid rgba(255,215,0,0.15);
    color:white;
    position:relative;
}

/* ===== HERO (ẢNH) ===== */
.hero{
    height:230px;
    background:url('https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true');
    background-size:cover;
    background-position:center 70%;
    position:relative;
    overflow:hidden;
}

/* ===== GOD LIGHT ===== */
.hero::before{
    content:"";
    position:absolute;
    top:-50%;
    left:50%;
    transform:translateX(-50%);
    width:300px;
    height:400px;
    background:radial-gradient(circle, rgba(255,215,0,0.35), transparent 70%);
    filter:blur(40px);
    animation:lightMove 4s ease-in-out infinite;
}

/* overlay */
.hero::after{
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(
        to bottom,
        rgba(0,0,0,0.5),
        rgba(0,0,0,0.2),
        rgba(10,20,30,1)
    );
}

/* ===== AVATAR ===== */
.avatar-wrap{
    position:absolute;
    bottom:-55px;
    left:50%;
    transform:translateX(-50%);
    z-index:2;
}

/* GLOW MẠNH */
.avatar-wrap::before{
    content:"";
    position:absolute;
    top:50%;
    left:50%;
    width:160px;
    height:160px;
    transform:translate(-50%,-50%);
    border-radius:50%;
    background: radial-gradient(circle, rgba(255,215,0,1), transparent 70%);
    filter:blur(20px);
    animation:pulse 2s infinite;
}

.avatar{
    width:110px;
    height:110px;
    border-radius:50%;
    border:3px solid #FFD700;
    position:relative;
    z-index:2;
}

/* ===== ANIMATION ===== */
@keyframes pulse{
    0%{opacity:0.6; transform:translate(-50%,-50%) scale(1);}
    50%{opacity:1; transform:translate(-50%,-50%) scale(1.2);}
    100%{opacity:0.6; transform:translate(-50%,-50%) scale(1);}
}

@keyframes lightMove{
    0%{opacity:0.4; transform:translateX(-50%) translateY(0);}
    50%{opacity:0.8; transform:translateX(-50%) translateY(20px);}
    100%{opacity:0.4; transform:translateX(-50%) translateY(0);}
}

/* ===== CONTENT ===== */
.content{
    padding:75px 25px 25px;
}

/* NAME */
.name{
    text-align:center;
    font-size:26px;
    font-weight:700;
    background:linear-gradient(#FFD700,#ffae00);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:25px;
}

/* ===== STATS ===== */
.stats{
    border-radius:20px;
    padding:15px;
    background:rgba(0,0,0,0.4);
    border:1px solid rgba(255,215,0,0.1);
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
    background:rgba(0,0,0,0.4);
    border:1px solid rgba(255,215,0,0.15);
    transition:0.3s;
}

.box:hover{
    transform:translateY(-6px);
    box-shadow:0 0 25px rgba(255,215,0,0.4);
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

components.html(html, height=700)
