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
    background:rgba(10,20,30,0.9);
    box-shadow:0 25px 70px rgba(0,0,0,0.8);
    border:1px solid rgba(255,255,255,0.08);
    color:white;
}

/* ===== HERO (ẢNH CHỈ Ở ĐÂY) ===== */
.hero{
    height:220px;
    background:url('https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true');
    background-size:cover;
    background-position:center 70%;
    position:relative;
}

/* overlay làm tối */
.hero::after{
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(
        to bottom,
        rgba(0,0,0,0.6),
        rgba(0,0,0,0.3),
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

/* glow vàng */
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

/* ring */
.avatar{
    width:110px;
    height:110px;
    border-radius:50%;
    border:3px solid #FFD700;
    position:relative;
    z-index:2;
}

@keyframes pulse{
    0%{opacity:0.6; transform:translate(-50%,-50%) scale(1);}
    50%{opacity:1; transform:translate(-50%,-50%) scale(1.1);}
    100%{opacity:0.6; transform:translate(-50%,-50%) scale(1);}
}

/* ===== CONTENT ===== */
.content{
    padding-top:70px;
    padding-bottom:25px;
    padding-left:25px;
    padding-right:25px;
}

/* NAME */
.name{
    text-align:center;
    font-size:24px;
    font-weight:700;
    color:#FFD700;
    margin-bottom:25px;
}

/* ===== STATS ===== */
.stats{
    border-top:1px solid rgba(255,255,255,0.05);
}

.row{
    display:flex;
    justify-content:space-between;
    padding:14px 0;
    border-bottom:1px solid rgba(255,255,255,0.05);
}

.row span{
    color:#9aa4ad;
}

.row b{
    font-weight:600;
}

/* ===== FOOTER ===== */
.footer{
    display:flex;
    gap:12px;
    margin-top:25px;
}

.box{
    flex:1;
    padding:18px;
    border-radius:16px;
    background: rgba(255,255,255,0.03);
    text-align:center;
    transition:0.3s;
}

.box:hover{
    transform:translateY(-5px);
    box-shadow:0 0 15px rgba(255,215,0,0.3);
}

.dot{
    width:30px;
    height:30px;
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

components.html(html, height=1000)
