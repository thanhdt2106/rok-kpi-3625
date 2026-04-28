import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

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
    background: radial-gradient(circle at top, #ffd54f, #e6a700);
    height:260px;
    position:relative;
    border-bottom-left-radius:30px;
    border-bottom-right-radius:30px;
}

/* AVATAR FRAME (ROK STYLE) */
.avatar-wrap{
    position:absolute;
    bottom:-60px;
    left:50%;
    transform:translateX(-50%);
    text-align:center;
}

/* vòng lửa */
.avatar-frame{
    width:140px;
    height:140px;
    border-radius:50%;
    padding:6px;
    background: conic-gradient(#ffcc00, #ff6600, #ffcc00);
    animation:spin 4s linear infinite;
    box-shadow:0 0 30px gold;
}

@keyframes spin{
    0%{transform:rotate(0deg);}
    100%{transform:rotate(360deg);}
}

/* avatar */
.avatar{
    width:100%;
    height:100%;
    border-radius:50%;
    background:url("https://i.pravatar.cc/200") center/cover;
}

/* badges */
.badges{
    margin-top:10px;
}
.badge{
    width:22px;
    height:22px;
    background:gold;
    display:inline-block;
    border-radius:50%;
    margin:3px;
    box-shadow:0 0 10px gold;
}

/* MAIN */
.container{
    margin-top:90px;
    padding:20px;
}

/* ENERGY */
.energy{
    color:white;
    font-size:14px;
}

.bar{
    height:12px;
    background:#083544;
    border-radius:10px;
    overflow:hidden;
    margin-top:5px;
}

.fill{
    width:40%;
    height:100%;
    background:linear-gradient(to right,#3cff00,#00c853);
}

/* PROFILE BOX */
.profile{
    background:linear-gradient(#1f6d8c,#15546b);
    border-radius:20px;
    padding:20px;
    margin-top:15px;
    color:white;
    box-shadow:0 0 20px rgba(0,0,0,0.6);
}

/* NAME */
.name{
    font-size:26px;
    font-weight:bold;
    margin-bottom:10px;
}

/* ROW */
.row{
    display:flex;
    justify-content:space-between;
    margin:6px 0;
}

/* MEDALS */
.medals{
    display:flex;
    gap:15px;
    margin-top:20px;
}

.card{
    flex:1;
    background:rgba(255,255,255,0.05);
    border-radius:15px;
    padding:15px;
    text-align:center;
    transition:0.3s;
}

.card:hover{
    transform:translateY(-5px);
    box-shadow:0 0 20px gold;
}

/* icon medal */
.icon{
    width:70px;
    height:70px;
    border-radius:50%;
    background:radial-gradient(circle,#ffd700,#ff9800);
    margin:auto;
    box-shadow:0 0 20px gold;
}

/* text */
.title{
    margin-top:10px;
    font-size:13px;
}

.value{
    font-weight:bold;
    margin-top:5px;
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
    Điểm hành động 431 / 1,850
    <div class="bar"><div class="fill"></div></div>
</div>

<div class="profile">

<div class="name">Louis Noob</div>

<div class="row"><span>Nền văn minh</span><span>Đức</span></div>
<div class="row"><span>Liên minh</span><span>[FT-D]FIGHT TO DEAD</span></div>
<div class="row"><span>Sức mạnh</span><span>87.424.868</span></div>
<div class="row"><span>Điểm Tiêu Diệt</span><span>6.119.626.641</span></div>
<div class="row"><span>Điểm Chiến Công</span><span>0</span></div>
<div class="row"><span>Điểm Cao Nhất</span><span>0</span></div>

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
</div>

</body>
</html>
"""

components.html(html, height=850)
