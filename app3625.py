import streamlit as st

st.set_page_config(layout="wide")

# ✅ GLOBAL CSS (xoá toàn bộ style mặc định Streamlit)
st.markdown("""
<style>

/* ===== REMOVE STREAMLIT DEFAULT ===== */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

header, footer {
    visibility: hidden;
}

/* ===== BACKGROUND FULL SCREEN ===== */
.stApp {
    background: radial-gradient(circle at top, #0f2a33, #05080c);
}

/* ===== CENTER WRAP ===== */
.wrapper{
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
}

/* ===== CARD ===== */
.card{
    width:420px;
    padding:35px;
    border-radius:24px;
    background: rgba(15, 30, 40, 0.85);
    backdrop-filter: blur(12px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.8);
    border:1px solid rgba(255,255,255,0.05);
    color:white;
    font-family:system-ui;
}

/* ===== HEADER ===== */
.title{
    text-align:center;
    font-size:26px;
    font-weight:800;
    color:#FFD700;
    letter-spacing:1px;
}

.server{
    text-align:center;
    color:#7f8c8d;
    margin-bottom:20px;
}

/* ===== AVATAR ===== */
.avatar-wrap{
    display:flex;
    justify-content:center;
    margin:20px 0;
}

.avatar{
    width:100px;
    height:100px;
    border-radius:50%;
    border:2px solid #FFD700;
}

/* ===== NAME ===== */
.name{
    text-align:center;
    font-size:22px;
    font-weight:600;
    margin-bottom:25px;
}

/* ===== STATS ===== */
.stats{
    border-top:1px solid rgba(255,255,255,0.05);
    border-bottom:1px solid rgba(255,255,255,0.05);
}

.row{
    display:flex;
    justify-content:space-between;
    padding:14px 5px;
    border-bottom:1px solid rgba(255,255,255,0.05);
}

.row:last-child{
    border-bottom:none;
}

.row span{
    color:#9aa4ad;
}

.row b{
    font-weight:600;
}

/* ===== FOOTER ===== */
.footer{
    display:flex;
    gap:12px;
    margin-top:25px;
}

.box{
    flex:1;
    padding:18px;
    border-radius:16px;
    background: rgba(255,255,255,0.03);
    text-align:center;
    transition:0.25s;
    cursor:pointer;
}

.box:hover{
    transform:translateY(-5px);
    background: rgba(255,255,255,0.07);
}

/* ===== DOT ===== */
.dot{
    width:30px;
    height:30px;
    background:#FFD700;
    border-radius:50%;
    margin:auto;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)


# ✅ HTML UI
st.markdown("""
<div class="wrapper">

    <div class="card">

        <div class="title">FIGHT TO DEAD</div>
        <div class="server">#3625</div>

        <div class="avatar-wrap">
            <img src="https://i.pravatar.cc/150?img=12" class="avatar">
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

</div>
""" components.html(html, height=600)
