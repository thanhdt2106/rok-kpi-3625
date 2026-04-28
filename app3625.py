import streamlit as st

st.set_page_config(layout="wide")

# CSS
st.markdown("""
<style>
body {background:#0b3b52;}

.row {
    display:flex;
    justify-content:space-between;
    color:white;
    margin:6px 0;
    font-size:14px;
}

.energy {color:white;}

.bar {
    height:10px;
    background:#0a2c3a;
    border-radius:10px;
    overflow:hidden;
}

.fill {
    width:40%;
    height:100%;
    background:limegreen;
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
""", unsafe_allow_html=True)

# 👉 HTML GỘP 1 KHỐI DUY NHẤT
st.markdown("""
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
""", unsafe_allow_html=True)
