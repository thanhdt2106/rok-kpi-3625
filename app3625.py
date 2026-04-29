import streamlit as st

st.set_page_config(layout="centered")

st.markdown("""
<style>

/* FIX STREAMLIT DEFAULT */
.block-container {
    max-width: 100% !important;
    padding: 0 !important;
}

/* BACKGROUND */
.bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: url("https://i.imgur.com/YOUR_IMAGE.jpg") center/cover no-repeat;
    z-index: -2;
}

.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0,0,0,0.65);
    z-index: -1;
}

/* CARD */
.content {
    width: 400px;
    margin: 60px auto;
    padding: 25px;
    border-radius: 20px;
    background: rgba(0, 40, 50, 0.85);
    backdrop-filter: blur(10px);
    box-shadow: 0 0 30px rgba(0,255,200,0.2);
    text-align: center;
    color: white;
}

/* TITLE */
.title {
    font-size: 26px;
    font-weight: bold;
    color: gold;
    text-shadow: 0 0 10px orange;
}

.title span {
    font-size: 18px;
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

/* NAME */
.name {
    margin-top: 10px;
    font-size: 20px;
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

.label {
    color: #aaa;
}

.value {
    color: gold;
    font-weight: bold;
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
    background: radial-gradient(circle, gold, orange);
    box-shadow: 0 0 15px gold;
}

.box p {
    font-size: 12px;
    color: #ccc;
    margin: 5px 0;
}

.box b {
    color: white;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="bg"></div>
<div class="overlay"></div>

<div class="content">

    <div class="title">
        FIGHT TO DEAD<br>
        <span>3625</span>
    </div>

    <img src="https://i.pravatar.cc/150" class="avatar">

    <h2 class="name">Louis Noob</h2>

    <div class="row">
        <div class="label">ID</div>
        <div class="value">71428274</div>
    </div>

    <div class="row">
        <div class="label">LIÊN MINH</div>
        <div class="value">[FT-D]FIGHT TO DEAD</div>
    </div>

    <div class="row">
        <div class="label">POWER</div>
        <div class="value">87.424.868</div>
    </div>

    <div class="row">
        <div class="label">KILL</div>
        <div class="value">6.119.626.641</div>
    </div>

    <div class="row">
        <div class="label">DEAD</div>
        <div class="value">1.245.678.910</div>
    </div>

    <div class="kpi">

        <div class="box">
            <div class="circle"></div>
            <p>RANK</p>
            <b>#1</b>
        </div>

        <div class="box">
            <div class="circle"></div>
            <p>KPI KILL</p>
            <b>85%</b>
        </div>

        <div class="box">
            <div class="circle"></div>
            <p>KPI DEAL</p>
            <b>92%</b>
        </div>

    </div>

</div>
""", unsafe_allow_html=True)
