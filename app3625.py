import streamlit as st
import streamlit.components.v1 as components

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>

body {
    margin: 0;
    font-family: Arial;
    background: url("https://i.imgur.com/YOUR_IMAGE.jpg") no-repeat center;
    background-size: cover;
}

/* OVERLAY */
.overlay {
    position: fixed;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.6);
}

/* CARD */
.card {
    width: 400px;
    margin: 60px auto;
    padding: 25px;
    border-radius: 20px;
    background: rgba(0, 40, 50, 0.9);
    box-shadow: 0 0 30px rgba(0,255,200,0.3);
    text-align: center;
    color: white;
    position: relative;
    z-index: 2;
}

/* TITLE */
.title {
    font-size: 26px;
    font-weight: bold;
    color: gold;
}

/* AVATAR */
.avatar {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    border: 4px solid gold;
    box-shadow: 0 0 20px gold;
    margin-top: 15px;
}

/* INFO */
.row {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    margin-top: 8px;
    border-radius: 10px;
    background: rgba(255,255,255,0.05);
}

/* KPI */
.kpi {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}

.box {
    flex: 1;
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 10px;
}

.circle {
    width: 45px;
    height: 45px;
    margin: auto;
    border-radius: 50%;
    background: gold;
}

</style>
</head>

<body>

<div class="overlay"></div>

<div class="card">

    <div class="title">
        FIGHT TO DEAD<br>3625
    </div>

    <img src="https://i.pravatar.cc/150" class="avatar">

    <h2>Louis Noob</h2>

    <div class="row"><span>ID</span><span>71428274</span></div>
    <div class="row"><span>ALLIANCE</span><span>[FT-D]</span></div>
    <div class="row"><span>POWER</span><span>87M</span></div>
    <div class="row"><span>KILL</span><span>6.1B</span></div>
    <div class="row"><span>DEAD</span><span>1.2B</span></div>

    <div class="kpi">
        <div class="box"><div class="circle"></div><p>#1</p></div>
        <div class="box"><div class="circle"></div><p>85%</p></div>
        <div class="box"><div class="circle"></div><p>92%</p></div>
    </div>

</div>

</body>
</html>
"""

components.html(html_code, height=700)
