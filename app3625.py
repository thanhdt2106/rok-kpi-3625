import streamlit as st
import streamlit.components.v1 as components

html = """
<!DOCTYPE html>
<html>
<head>
<style>

body{
    margin:0;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    font-family:system-ui;
    background: radial-gradient(circle at top, #0f2a33, #05080c);
}

/* CARD */
.card{
    width:380px;
    padding:30px;
    border-radius:24px;
    background: rgba(15, 30, 40, 0.85);
    backdrop-filter: blur(10px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.8);
    color:white;
}

/* HEADER */
.title{
    text-align:center;
    font-size:24px;
    font-weight:800;
    color:#FFD700;
    letter-spacing:1px;
}

.server{
    text-align:center;
    color:#7f8c8d;
    margin-bottom:20px;
}

/* AVATAR */
.avatar-wrap{
    display:flex;
    justify-content:center;
    margin:20px 0;
}

.avatar{
    width:95px;
    height:95px;
    border-radius:50%;
    border:2px solid #FFD700;
}

/* NAME */
.name{
    text-align:center;
    font-size:20px;
    font-weight:600;
    margin-bottom:25px;
}

/* STATS LIST */
.stats{
    border-top:1px solid rgba(255,255,255,0.05);
    border-bottom:1px solid rgba(255,255,255,0.05);
}

.row{
    display:flex;
    justify-content:space-between;
    padding:12px 5px;
    border-bottom:1px solid rgba(255,255,255,0.05);
}

.row:last-child{
    border-bottom:none;
}

.row span{
    color:#9aa4ad;
}

.row b{
    font-weight:600;
}

/* FOOTER CARDS */
.footer{
    display:flex;
    gap:10px;
    margin-top:20px;
}

.box{
    flex:1;
    padding:15px;
    border-radius:14px;
    background: rgba(255,255,255,0.03);
    text-align:center;
    transition:0.2s;
}

.box:hover{
    transform:translateY(-3px);
    background: rgba(255,255,255,0.06);
}

.dot{
    width:28px;
    height:28px;
    background:#FFD700;
    border-radius:50%;
    margin:auto;
    margin-bottom:8px;
}

</style>
</head>

<body>

<div class="card">

    <div class="title">FIGHT TO DEAD</div>
    <div class="server">#3625</div>

    <div class="avatar-wrap">
        <img src="https://i.pravatar.cc/150?img=5" class="avatar">
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
        <div class="box"><div class="dot"></div>#1</div>
        <div class="box"><div class="dot"></div>85%</div>
        <div class="box"><div class="dot"></div>92%</div>
    </div>

</div>

</body>
</html>
"""

components.html(html, height=650)
