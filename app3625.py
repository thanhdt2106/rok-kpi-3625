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
    background:#0b0f1a;
    font-family: 'Segoe UI', sans-serif;
}

/* XÓA padding mặc định Streamlit */
.block-container{
    padding:0 !important;
}
.main{
    padding:0 !important;
}

/* CENTER CARD */
.wrapper{
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}

/* CARD */
.card{
    width:65vw;
    height:65vh;
    border-radius:28px;
    overflow:hidden;
    position:relative;

    /* nền ảnh nằm TRONG card */
    background-image:url("https://github.com/thanhdt2106/rok-kpi-3625/blob/main/anhnen.png?raw=true");
    background-size:cover;
    background-position:center;

    box-shadow:0 0 80px rgba(0,0,0,0.8);
}

/* overlay giúp chữ nổi */
.overlay{
    position:absolute;
    inset:0;
    background:linear-gradient(
        to bottom,
        rgba(0,0,0,0.3),
        rgba(0,0,0,0.75)
    );
}

/* CONTENT */
.content{
    position:relative;
    z-index:2;
    padding:40px;
    color:white;
}

/* HEADER */
.header{
    display:flex;
    align-items:center;
    gap:20px;
}

/* AVATAR */
.avatar{
    width:90px;
    height:90px;
    border-radius:50%;
    border:3px solid gold;
    box-shadow:0 0 25px gold;
}

/* NAME */
.name{
    font-size:28px;
    font-weight:500;
    color:#ffd700;
    letter-spacing:1px;
}

/* INFO GRID */
.info{
    margin-top:30px;
    display:grid;
    grid-template-columns: repeat(4, 1fr);
    gap:20px;
}

.item{
    backdrop-filter: blur(6px);
    background:rgba(0,0,0,0.35);
    padding:12px 16px;
    border-radius:12px;
}

.label{
    font-size:12px;
    opacity:0.7;
}

.value{
    font-size:18px;
    margin-top:4px;
}

/* BOX KPI */
.kpi{
    margin-top:40px;
    display:grid;
    grid-template-columns: repeat(3,1fr);
    gap:20px;
}

.box{
    padding:20px;
    border-radius:18px;
    text-align:center;
    backdrop-filter: blur(10px);
    background:rgba(0,0,0,0.4);
    border:1px solid rgba(255,255,255,0.1);
}

/* BOX HIGHLIGHT */
.box.active{
    border:2px solid gold;
    box-shadow:0 0 20px rgba(255,215,0,0.7);
}

.icon{
    font-size:22px;
    margin-bottom:8px;
}

.big{
    font-size:18px;
}

.sub{
    font-size:12px;
    opacity:0.7;
}

</style>
</head>

<body>

<div class="wrapper">

    <div class="card">

        <div class="overlay"></div>

        <div class="content">

            <div class="header">
                <img class="avatar" src="https://i.pravatar.cc/150">
                <div class="name">L Gạo Nút 亗</div>
            </div>

            <div class="info">
                <div class="item">
                    <div class="label">ID</div>
                    <div class="value">16925269</div>
                </div>

                <div class="item">
                    <div class="label">Alliance</div>
                    <div class="value">[FT-D]FIGHT TO DEAD</div>
                </div>

                <div class="item">
                    <div class="label">Kill</div>
                    <div class="value">5,826,515,379</div>
                </div>

                <div class="item">
                    <div class="label">Dead</div>
                    <div class="value">3,418,388,660</div>
                </div>
            </div>

            <div class="kpi">

                <div class="box active">
                    <div class="icon">🏆</div>
                    <div class="big">#12</div>
                </div>

                <div class="box">
                    <div class="icon">🔥</div>
                    <div class="big">5.8B</div>
                    <div class="sub">38%</div>
                </div>

                <div class="box">
                    <div class="icon">💀</div>
                    <div class="big">3.4B</div>
                    <div class="sub">28%</div>
                </div>

            </div>

        </div>

    </div>

</div>

</body>
</html>
"""

components.html(html, height=900)
