import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="centered")

html = """
<!DOCTYPE html>
<html>
<head>
<style>
body{
    margin:0;
    background:#072b3a;
    font-family:Arial;
}

/* HEADER */
.header{
    background:linear-gradient(#ffd54f,#e6a700);
    height:220px;
    border-bottom-left-radius:25px;
    border-bottom-right-radius:25px;
    position:relative;
}

/* AVATAR */
.avatar-wrap{
    position:absolute;
    bottom:-60px;
    left:50%;
    transform:translateX(-50%);
    text-align:center;
}

.avatar-frame{
    width:130px;
    height:130px;
    border-radius:50%;
    padding:5px;
    background:conic-gradient(#ffcc00,#ff6600,#ffcc00);
    box-shadow:0 0 30px gold;
}

.avatar{
    width:100%;
    height:100%;
    border-radius:50%;
    background:url("https://i.pravatar.cc/200") center/cover;
}

/* BADGE */
.badges{
    margin-top:8px;
}
.badge{
    width:20px;
    height:20px;
    background:gold;
    border-radius:50%;
    display:inline-block;
    margin:2px;
}

/* MAIN */
.container{
    margin-top:80px;
    padding:15px;
}

/* ENERGY */
.energy{
    color:white;
    font-size:14px;
}

.bar{
    height:10px;
    background:#083544;
    border-radius:10px;
    overflow:hidden;
    margin-top:5px;
}

.fill{
    width:45%;
    height:100%;
    background:linear-gradient(to right,#00ff87,#00c853);
}

/* PROFILE BOX */
.profile{
    margin-top:15px;
    background:
        linear-gradient(#1f6d8c,#15546b),
        repeating-linear-gradient(
            0deg,
            rgba(255,255,255,0.02),
            rgba(255,255,255,0.02) 2px,
            transparent 2px,
            transparent 4px
        );
    border-radius:15px;
    padding:15px;
    color:white;
    border:2px solid rgba(255,255,255,0.08);
    box-shadow:
        inset 0 0 10px rgba(255,255,255,0.1),
        0 0 10px rgba(0,0,0,0.8);
}

/* NAME */
.name{
    display:inline-block;
    background:#0d4f6a;
    padding:8px 15px;
    border-radius:10px;
    font-size:22px;
    font-weight:bold;
    box-shadow:inset 0 2px 5px rgba(0,0,0,0.6);
    margin-bottom:10px;
}

/* ROW BOX (QUAN TRỌNG) */
.row{
    display:flex;
    justify-content:space-between;
    margin:6px 0;
    padding:8px 10px;

    background:rgba(255,255,255,0.05);
    border-radius:8px;

    border:1px solid rgba(255,255,255,0.08);

    box-shadow:
        inset 0 1px 2px rgba(255,255,255,0.05),
        inset 0 -2px 5px rgba(0,0,0,0.4);
}

/* VALUE TEXT */
.row span:last-child{
    color:#ffd54f;
    font-weight:bold;
    text-shadow:0 0 5px gold;
}

/* MEDALS */
.medals{
    display:flex;
    gap:10px;
    margin-top:15px;
}

.card{
    flex:1;
    background:rgba(255,255,255,0.05);
    border-radius:12px;
    padding:10px;
    text-align:center;
}

/* ICON MEDAL */
.icon{
    width:60px;
    height:60px;
    border-radius:50%;
    background:radial-gradient(circle,#ffd700,#ff9800);
    margin:auto;
    box-shadow:0 0 15px gold;
}

.title{
    font-size:12px;
    margin-top:5px;
}

.value{
    font-weight:bold;
    margin-top:5px;
}

/* MENU */
.menu{
    display:flex;
    justify-content:space-around;
    margin-top:20px;
}

.menu div{
    width:45px;
    height:45px;
    border-radius:50%;
    background:#1e6a87;
    box-shadow:0 4px 10px rgba(0,0,0,0.6);
}
</style>
</head>

<body>

<div class="header">
    <div class="avatar-wrap">
        <div class="avatar-frame">
            <div class="avatar"></div>
        </div>
        <div class="badges">
            <span class="badge"></span>
            <span class="badge"></span>
            <span class="badge"></span>
            <span class="badge"></span>
        </div>
    </div>
</div>

<div class="container">

<div class="energy">
    Điểm hành động 471 / 1,850
    <div class="bar"><div class="fill"></div></div>
</div>

<div class="profile">

<div class="name">Louis Noob</div>

<div class="row"><span>🌍 Nền văn minh</span><span>Đức</span></div>
<div class="row"><span>🏰 Liên minh</span><span>[FT-D]FIGHT TO DEAD</span></div>
<div class="row"><span>⚔️ Sức mạnh</span><span>87.424.868</span></div>
<div class="row"><span>💀 Điểm Tiêu Diệt</span><span>6.119.626.641</span></div>
<div class="row"><span>🎖️ Điểm Chiến Công</span><span>0</span></div>
<div class="row"><span>🏆 Điểm Cao Nhất</span><span>0</span></div>

<div class="medals">
    <div class="card">
        <div class="icon"></div>
        <div class="title">Olympia</div>
        <div class="value">Thanh Đồng</div>
    </div>

    <div class="card">
        <div class="icon"></div>
        <div class="title">Osiris</div>
        <div class="value">37 Win</div>
    </div>

    <div class="card">
        <div class="icon"></div>
        <div class="title">KVK</div>
        <div class="value">3x Red</div>
    </div>
</div>

</div>

<div class="menu">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
</div>

</div>

</body>
</html>
"""

components.html(html, height=900)
