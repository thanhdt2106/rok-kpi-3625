import streamlit as st
import streamlit.components.v1 as components

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin:0;
    background:#0b3b52;
    font-family:Arial;
}

/* HEADER */
.header {
    background: linear-gradient(#f7c948, #e6a700);
    height:220px;
    border-radius:0 0 25px 25px;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
}

/* AVATAR */
.avatar {
    width:110px;
    height:110px;
    border-radius:50%;
    border:5px solid gold;
    background:url("https://i.pravatar.cc/150") center/cover;
    box-shadow:0 0 25px gold;
}

/* BADGES */
.badges span {
    display:inline-block;
    width:18px;
    height:18px;
    margin:6px;
    background:gold;
    border-radius:50%;
}

/* CONTENT */
.container {
    padding:20px;
}

/* ENERGY */
.energy {
    color:white;
    font-size:14px;
}

.bar {
    height:10px;
    background:#0a2c3a;
    border-radius:10px;
    overflow:hidden;
    margin-top:5px;
}

.fill {
    width:40%;
    height:100%;
    background:#39d353;
}

/* ROW */
.row {
    display:flex;
    justify-content:space-between;
    color:white;
    margin:6px 0;
}

/* MEDALS */
.medals {
    display:flex;
    gap:15px;
    margin-top:20px;
}

.card {
    flex:1;
    background:rgba(255,255,255,0.05);
    border-radius:15px;
    padding:20px;
    text-align:center;
    color:white;
}

.icon {
    width:60px;
    height:60px;
    background:gold;
    border-radius:50%;
    margin:auto;
    box-shadow:0 0 15px gold;
}
</style>
</head>

<body>

<div class="header">
    <div class="avatar"></div>
    <div class="badges">
        <span></span><span></span><span></span><span></span>
    </div>
</div>

<div class="container">

<div class="energy">
    Điểm hành động 431 / 1,850
    <div class="bar"><div class="fill"></div></div>
</div>

<div class="row"><span>Nền văn minh</span><span>Đức</span></div>
<div class="row"><span>Liên minh</span><span>[FT-D]FIGHT TO DEAD</span></div>
<div class="row"><span>Sức mạnh</span><span>87.424.868</span></div>
<div class="row"><span>Điểm Tiêu Diệt</span><span>6.119.626.641</span></div>
<div class="row"><span>Điểm Chiến Công</span><span>0</span></div>
<div class="row"><span>Điểm Cao Nhất</span><span>0</span></div>

<div class="medals">
    <div class="card">
        <div class="icon"></div>
        <div>Olympia</div>
        <div><b>Thanh Đồng</b></div>
    </div>

    <div class="card">
        <div class="icon"></div>
        <div>Osiris</div>
        <div><b>37 Win</b></div>
    </div>

    <div class="card">
        <div class="icon"></div>
        <div>KVK</div>
        <div><b>3x Red</b></div>
    </div>
</div>

</div>

</body>
</html>
"""

components.html(html_code, height=800)
