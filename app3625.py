import streamlit as st

st.set_page_config(layout="centered")

# =========================
# CSS GAME UI
# =========================
st.markdown("""
<style>

body {
    background: #061e26;
}

.card {
    position: relative;
    width: 420px;
    margin: auto;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.7);
}

/* BACKGROUND */
.bg {
    position: absolute;
    width: 100%;
    height: 100%;
    background: url("https://i.imgur.com/your-image.jpg") center/cover;
    filter: brightness(0.4);
}

/* OVERLAY */
.overlay {
    position: absolute;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, rgba(0,0,0,0.2), #062a35 80%);
}

/* CONTENT */
.content {
    position: relative;
    z-index: 2;
    padding: 20px;
    color: white;
    text-align: center;
}

/* TITLE */
.title {
    font-size: 32px;
    font-weight: bold;
    color: gold;
}

.title span {
    font-size: 22px;
}

/* AVATAR */
.avatar-wrap {
    margin-top: 10px;
}

.avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 4px solid gold;
    box-shadow: 0 0 20px gold;
}

/* NAME */
.name {
    margin: 10px 0;
}

/* INFO BOX */
.info {
    background: rgba(0,0,0,0.6);
    border-radius: 15px;
    padding: 10px;
    margin-top: 15px;
}

.row {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.row:last-child {
    border-bottom: none;
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
    justify-content: space-between;
    margin-top: 20px;
}

.box {
    width: 30%;
    background: rgba(0,0,0,0.6);
    padding: 15px;
    border-radius: 12px;
}

.circle {
    width: 50px;
    height: 50px;
    background: gold;
    border-radius: 50%;
    margin: auto;
}

</style>
""", unsafe_allow_html=True)

# =========================
# UI HTML
# =========================
st.markdown(f"""
<div class="card">

    <div class="bg"></div>
    <div class="overlay"></div>

    <div class="content">

        <div class="title">
            FIGHT TO DEAD<br>
            <span>3625</span>
        </div>

        <div class="avatar-wrap">
            <img src="https://i.pravatar.cc/150" class="avatar">
        </div>

        <h2 class="name">Louis Noob</h2>

        <div class="info">

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
</div>
""", unsafe_allow_html=True)
