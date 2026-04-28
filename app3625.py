import streamlit as st

st.set_page_config(layout="centered")

# CSS custom
st.markdown("""
<style>

body {
    background-color:#0b3b52;
}

/* HEADER */
.header {
    background: radial-gradient(circle at top, #ffd54f, #e6a700);
    height:200px;
    border-bottom-left-radius:20px;
    border-bottom-right-radius:20px;
    position:relative;
}

/* AVATAR */
.avatar-wrap {
    position:absolute;
    top:100px;
    left:50%;
    transform:translate(-50%, -50%);
    text-align:center;
}

.avatar {
    width:120px;
    height:120px;
    border-radius:50%;
    border:5px solid gold;
    background:url("https://i.pravatar.cc/150") center/cover;
    box-shadow:0 0 25px gold;
    margin:auto;
}

.badge {
    display:inline-block;
    width:30px;
    height:30px;
    border-radius:50%;
    margin:5px 2px;
    background:gold;
}

/* CONTAINER */
.container {
    margin-top:80px;
}

/* ENERGY */
.energy {
    color:white;
    font-size:14px;
}

.bar {
    background:#0a2c3a;
    border-radius:10px;
    overflow:hidden;
    height:10px;
    margin-top:5px;
}

.fill {
    width:40%;
    height:100%;
    background:limegreen;
}

/* PROFILE */
.profile {
    margin-top:15px;
    background:linear-gradient(#1f6d8c,#15546b);
    border-radius:15px;
    padding:15px;
    color:white;
}

.name {
    font-size:24px;
    font-weight:bold;
}

/* ROW */
.row {
    display:flex;
    justify-content:space-between;
    margin-top:8px;
}

/* MEDALS */
.medals {
    display:flex;
    gap:10px;
    margin-top:15px;
}

.card {
    flex:1;
    background:rgba(255,255,255,0.05);
    border-radius:12px;
    text-align:center;
    padding:10px;
}

.icon {
    width:60px;
    height:60px;
    border-radius:50%;
    background:gold;
    margin:auto;
}

/* MENU */
.menu {
    display:flex;
    justify-content:space-around;
    margin-top:20px;
}

.menu div {
    width:50px;
    height:50px;
    border-radius:50%;
    background:#1e6a87;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="header">
    <div class="avatar-wrap">
        <div class="avatar"></div>
        <div>
            <span class="badge"></span>
            <span class="badge"></span>
            <span class="badge"></span>
            <span class="badge"></span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# CONTENT
st.markdown('<div class="container">', unsafe_allow_html=True)

# ENERGY
st.markdown("""
<div class="energy">
    Điểm hành động 431 / 1,850
    <div class="bar">
        <div class="fill"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# PROFILE
st.markdown("""

st.markdown("""
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
""", unsafe_allow_html=True)
