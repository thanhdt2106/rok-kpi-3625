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

/* ===== BACKGROUND FULL ===== */
body{
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:url('https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true') center/cover no-repeat;
    overflow:hidden;
}

/* ===== FIRE PARTICLES ===== */
body::before{
    content:"";
    position:absolute;
    width:100%;
    height:100%;
    background: radial-gradient(circle, rgba(255,140,0,0.15) 1px, transparent 1px);
    background-size:3px 3px;
    animation:move 20s linear infinite;
}

@keyframes move{
    from{transform:translateY(0);}
    to{transform:translateY(-200px);}
}

/* ===== CARD ===== */
.card{
    width:420px;
    border-radius:30px;
    padding:25px;
    background:rgba(10,20,30,0.6);
    backdrop-filter:blur(15px);
    border:1px solid rgba(255,215,0,0.2);
    box-shadow:0 0 40px rgba(255,180,0,0.2);
    color:white;
    text-align:center;
}

/* ===== AVATAR GLOW ===== */
.avatar-wrap{
    position:relative;
    margin-bottom:15px;
}

.avatar{
    width:110px;
    height:110px;
    border-radius:50%;
    position:relative;
    z-index:2;
}

/* glow vòng ngoài */
.avatar-wrap::before{
    content:"";
    position:absolute;
    top:50%;
    left:50%;
    width:140px;
    height:140px;
    transform:translate(-50%,-50%);
    border-radius:50%;
    background: radial-gradient(circle, rgba(255,215,0,0.8), transparent 70%);
    filter:blur(10px);
    animation:pulse 2s infinite;
}

/* ring vàng */
.avatar-wrap::after{
    content:"";
    position:absolute;
    top:50%;
    left:50%;
    width:125px;
    height:125px;
    transform:translate(-50%,-50%);
    border-radius:50%;
    border:3px solid #FFD700;
}

@keyframes pulse{
    0%{opacity:0.6; transform:translate(-50%,-50%) scale(1);}
    50%{opacity:1; transform:translate(-50%,-50%) scale(1.1);}
    100%{opacity:0.6; transform:translate(-50%,-50%) scale(1);}
}

/* ===== NAME ===== */
.name{
    font-size:26px;
    font-weight:700;
    margin-bottom:20px;
    background:linear-gradient(#FFD700,#ffae00);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

/* ===== STATS ===== */
.stats{
    margin-top:10px;
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
    color:#ccc;
}

.row b{
    color:#fff;
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
    transform:translateY(-5px);
    box-shadow:0 0 20px rgba(255,215,0,0.3);
}

.icon{
    width:40px;
    height:40px;
    margin:auto;
    margin-bottom:10px;
    border-radius:50%;
    background:#FFD700;
}

</style>
</head>

<body>

<div class="card">

    <div class="avatar-wrap">
        <img src="https://i.pravatar.cc/150?img=12" class="avatar">
    </div>

    <div class="name">Louis Noob</div>

    <div class="stats">
        <div class="row"><span>ID</span><b>71428274</b></div>
        <div class="row"><span>Alliance</span><b>[FT-D]</b></div>
        <div class="row"><span>Power</span><b>87M</b></div>
        <div class="row"><span>Kill</span><b>6.1B</b></div>
        <div class="row"><span>Dead</span><b>1.2B</b></div>
    </div>

    <div class="footer">
        <div class="box"><div class="icon"></div>#1</div>
        <div class="box"><div class="icon"></div>85%</div>
        <div class="box"><div class="icon"></div>92%</div>
    </div>

</div>

</body>
</html>
"""

components.html(html, height=900)
