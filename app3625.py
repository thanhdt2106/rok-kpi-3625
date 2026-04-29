import streamlit as st

# ================= CONFIG =================
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= CSS =================
st.markdown("""
<style>

/* ===== REMOVE STREAMLIT UI ===== */
section[data-testid="stSidebar"] {display:none !important;}
header {visibility:hidden;}
footer {visibility:hidden;}
#MainMenu {visibility:hidden;}

/* ===== FULL WIDTH ===== */
.block-container {
    padding:0 !important;
    max-width:100% !important;
}

/* ===== BACKGROUND ===== */
html, body, [class*="css"]  {
    background: radial-gradient(circle at top, #0b1a2a, #050b12);
}

/* ===== CENTER WRAPPER ===== */
.wrapper{
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}

/* ===== CARD ===== */
.card{
    width:65vw;
    height:65vh;
    border-radius:28px;
    overflow:hidden;
    position:relative;
    box-shadow:0 0 60px rgba(255,180,0,0.15);
}

/* ===== BACKGROUND IMAGE INSIDE CARD ===== */
.card::before{
    content:"";
    position:absolute;
    inset:0;
    background:url("https://i.imgur.com/your-image.jpg") center/cover no-repeat;
    filter:brightness(0.85);
    z-index:1;
}

/* ===== DARK OVERLAY ===== */
.card::after{
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.7));
    z-index:2;
}

/* ===== CONTENT ===== */
.content{
    position:relative;
    z-index:3;
    padding:40px;
    color:white;
    height:100%;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
}

/* ===== TOP ===== */
.top{
    display:flex;
    align-items:center;
    gap:20px;
}

/* AVATAR */
.avatar{
    width:90px;
    height:90px;
    border-radius:50%;
    border:3px solid #ffd700;
    box-shadow:0 0 20px #ffd700;
}

/* NAME */
.name{
    font-size:28px;
    color:#ffd700;
    letter-spacing:1px;
}

/* ===== INFO ROW ===== */
.info{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:15px;
    margin-top:20px;
}

.info-box{
    background:rgba(0,0,0,0.35);
    padding:12px 15px;
    border-radius:12px;
    backdrop-filter:blur(6px);
}

.label{
    font-size:12px;
    opacity:0.6;
}

.value{
    font-size:16px;
    margin-top:4px;
}

/* ===== STATS ===== */
.stats{
    display:flex;
    gap:20px;
}

.stat{
    flex:1;
    background:rgba(0,0,0,0.4);
    border-radius:18px;
    padding:25px;
    text-align:center;
    backdrop-filter:blur(10px);
    transition:0.3s;
}

.stat:hover{
    transform:translateY(-5px);
    box-shadow:0 0 25px rgba(255,200,0,0.3);
}

/* ICON */
.icon{
    font-size:22px;
    margin-bottom:10px;
}

/* VALUE */
.stat-value{
    font-size:20px;
    margin-bottom:5px;
}

/* SUB */
.sub{
    font-size:13px;
    opacity:0.6;
}

/* RANK HIGHLIGHT */
.rank{
    border:2px solid #ffd700;
    box-shadow:0 0 25px rgba(255,215,0,0.6);
}

</style>
""", unsafe_allow_html=True)

# ================= DATA DEMO =================
name = "L Gạo Nút"
avatar = "https://i.pravatar.cc/150"
id_player = "16925269"
alliance = "[FT-D]FIGHT TO DEAD"
kill = "5,826,515,379"
dead = "3,418,388,660"

rank = "#12"
kill_kpi = "5.8B"
kill_percent = "38%"
dead_kpi = "3.4B"
dead_percent = "28%"

# ================= UI =================
st.markdown(f"""
<div class="wrapper">

    <div class="card">
        <div class="content">

            <!-- TOP -->
            <div class="top">
                <img src="{avatar}" class="avatar"/>
                <div class="name">{name}</div>
            </div>

            <!-- INFO -->
            <div class="info">
                <div class="info-box">
                    <div class="label">ID</div>
                    <div class="value">{id_player}</div>
                </div>

                <div class="info-box">
                    <div class="label">Alliance</div>
                    <div class="value">{alliance}</div>
                </div>

                <div class="info-box">
                    <div class="label">Kill</div>
                    <div class="value">{kill}</div>
                </div>

                <div class="info-box">
                    <div class="label">Dead</div>
                    <div class="value">{dead}</div>
                </div>
            </div>

            <!-- STATS -->
            <div class="stats">

                <div class="stat rank">
                    <div class="icon">🏆</div>
                    <div class="stat-value">{rank}</div>
                    <div class="sub">Rank</div>
                </div>

                <div class="stat">
                    <div class="icon">🔥</div>
                    <div class="stat-value">{kill_kpi}</div>
                    <div class="sub">{kill_percent}</div>
                </div>

                <div class="stat">
                    <div class="icon">💀</div>
                    <div class="stat-value">{dead_kpi}</div>
                    <div class="sub">{dead_percent}</div>
                </div>

            </div>

        </div>
    </div>

</div>
""", components.html(html, height=900)
