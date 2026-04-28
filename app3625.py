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

/* energy */
.energy {
    color:white;
    padding:20px;
}

.bar {
    height:10px;
    background:#0a2c3a;
    border-radius:10px;
    overflow:hidden;
}

.fill {
    width:40%;
    height:100%;
    background:#39d353;
}

/* row */
.row {
    display:flex;
    justify-content:space-between;
    color:white;
    padding:5px 20px;
}

/* medals */
.medals {
    display:flex;
    gap:15px;
    padding:20px;
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
}
</style>
</head>

<body>

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

</body>
</html>
"""

components.html(html_code, height=600)
