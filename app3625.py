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
    background: radial-gradient(circle at top, #ffe082, #ffb300);
    height:260px;
    position:relative;
    border-bottom-left-radius:30px;
    border-bottom-right-radius:30px;
}

/* AVATAR */
.avatar-wrap{
    position:absolute;
    bottom:-65px;
    left:50%;
    transform:translateX(-50%);
}

/* vòng lửa glow mạnh hơn */
.avatar-frame{
    width:150px;
    height:150px;
    border-radius:50%;
    padding:6px;
    background: conic-gradient(#ffcc00, #ff6f00, #ffcc00);
    animation:spin 5s linear infinite;
    box-shadow:0 0 40px #ffcc00, 0 0 80px #ff9800;
}

@keyframes spin{
    0%{transform:rotate(0deg);}
    100%{transform:rotate(360deg);}
}

.avatar{
    width:100%;
    height:100%;
    border-radius:50%;
    background:url("https://i.pravatar.cc/200") center/cover;
}

/* TEXT GLOW */
.glow-text{
    color:#fff;
    text-shadow:0 0 5px #fff, 0 0 10px gold, 0 0 20px gold;
}

/* CONTAINER */
.container{
    margin-top:100px;
    padding:20px;
}

/* ENERGY */
.energy{
    color:#fff;
    font-size:14px;
    text-shadow:0 0 5px cyan;
}

.bar{
    height:12px;
    background:#083544;
    border-radius:10px;
    overflow:hidden;
}

.fill{
    width:40%;
    height:100%;
    background:linear-gradient(90deg,#00ff87,#00c853);
    box-shadow:0 0 10px #00ff87;
}

/* PROFILE BOX */
.profile{
    background:linear-gradient(#1f6d8c,#15546b);
    border-radius:20px;
    padding:20px;
    margin-top:15px;
    color:white;
    box-shadow:
        inset 0 0 20px rgba(255,255,255,0.1),
        0 0 20px rgba(0,0,0,0.8);
}

/* ROW */
.row{
    display:flex;
    justify-content:space-between;
    margin:8px 0;
    font-size:15px;
}

.row span:last-child{
    color:#ffd54f;
    text-shadow:0 0 5px gold;
}

/* MEDALS */
.medals{
    display:flex;
    gap:15px;
    margin-top:20px;
}

/* CARD EFFECT */
.card{
    flex:1;
    background:linear-gradient(#1a4f63,#0d3445);
    border-radius:15px;
    padding:15px;
    text-align:center;
    position:relative;
    overflow:hidden;
    transition:0.3s;
}

/* viền sáng chạy */
.card::before{
    content:"";
    position:absolute;
    inset:0;
    border-radius:15px;
    padding:2px;
    background:linear-gradient(45deg, gold, transparent, gold);
    -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
}

/* hover giống game */
.card:hover{
    transform:translateY(-6px) scale(1.03);
    box-shadow:0 0 25px gold;
}

/* ICON */
.icon{
    width:70px;
    height:70px;
    border-radius:50%;
    background:radial-gradient(circle,#ffd700,#ff9800);
    margin:auto;
    box-shadow:0 0 25px gold;
}

/* TITLE */
.title{
    margin-top:10px;
    font-size:13px;
    color:#ccc;
}

/* VALUE */
.value{
    font-weight:bold;
    color:#fff;
    text-shadow:0 0 10px gold;
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
    </div>
</div>

<div class="container">

<div class="energy glow-text">
    Điểm hành động 431 / 1,850
    <div class="bar"><div class="fill"></div></div>
</div>

<div class="profile">

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

components.html(html, height=900)
