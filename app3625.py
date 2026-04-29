import streamlit as st
import streamlit.components.v1 as components

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>

body{
    margin:0;
    background:#0b0f14;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    font-family:system-ui;
}

/* CARD */
.card{
    width:380px;
    background:linear-gradient(180deg,#0f2027,#0b1218);
    border-radius:20px;
    padding:30px 25px;
    box-shadow:0 10px 40px rgba(0,0,0,0.6);
    color:white;
}

/* HEADER */
.title{
    text-align:center;
    font-size:22px;
    font-weight:700;
    color:#FFD700;
}

.server{
    text-align:center;
    font-size:14px;
    color:#aaa;
    margin-bottom:20px;
}

/* AVATAR */
.avatar-wrap{
    display:flex;
    justify-content:center;
    margin:15px 0;
}

.avatar{
    width:90px;
    height:90px;
    border-radius:50%;
    border:3px solid #FFD700;
}

/* NAME */
.name{
    text-align:center;
    font-size:20px;
    font-weight:600;
    margin-bottom:20px;
}

/* STATS */
.stats{
    display:flex;
    flex-direction:column;
    gap:10px;
}

.row{
    display:flex;
    justify-content:space-between;
    background:#111a22;
    padding:10px 15px;
    border-radius:10px;
}

.row span{
    color:#888;
}

.row b{
    font-weight:600;
}

/* FOOT */
.footer{
    display:flex;
    justify-content:space-between;
    margin-top:20px;
}

.box{
    flex:1;
    background:#111a22;
    border-radius:12px;
    padding:15px;
    margin:5px;
    text-align:center;
}

.dot{
    width:30px;
    height:30px;
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
        <img src="https://i.pravatar.cc/150" class="avatar">
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

components.html(html_code, height=600)
