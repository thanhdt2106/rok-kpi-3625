import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

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

/* ===== BACKGROUND ===== */
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
    border-radius:28px;
    overflow:hidden;
    box-shadow:0 25px 70px rgba(0,0,0,0.9);
    border:1px solid rgba(255,255,255,0.08);
    color:white;
}

/* ===== HERO (ẢNH NỀN CỦA BẠN) ===== */
.hero{
    height:260px;
    background:url('https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true') center/cover no-repeat;
    position:relative;
}

/* overlay cho dễ nhìn */
.hero::after{
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(to bottom, rgba(0,0,0,0.2), #0b1a22 90%);
}

/* ===== AVATAR ===== */
.avatar-wrap{
    position:absolute;
    bottom:-50px;
    left:50%;
    transform:translateX(-50%);
    z-index:2;
}

.avatar{
    width:100px;
    height:100px;
    border-radius:50%;
    border:3px solid #FFD700;
}

/* ===== CONTENT ===== */
.content{
    background:#0b1a22;
    padding-top:70px;
    padding-bottom:25px;
    padding-left:25px;
    padding-right:25px;
}

/* NAME */
.name{
    text-align:center;
    font-size:22px;
    font-weight:600;
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

components.html(html, height=650)
