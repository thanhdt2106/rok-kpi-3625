import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# DATA
df = pd.read_csv("data.csv")
df = df.sort_values(by="power", ascending=False).reset_index(drop=True)

# NAVBAR
st.markdown("""
<div class="navbar">
    <div class="logo">⚔️ ROK KPI DASHBOARD</div>
    <div class="menu">
        <div class="active">🏠 Trang chủ</div>
        <div>👤 Profile</div>
        <div>👥 Người dùng</div>
    </div>
    <div class="user">Admin</div>
</div>
""", unsafe_allow_html=True)

# TITLE
st.markdown('<div class="title">🏆 BẢNG XẾP HẠNG KPI</div>', unsafe_allow_html=True)

# HEADER TABLE
st.markdown("""
<div class="table-header">
<div>#</div>
<div>ID</div>
<div>NAME</div>
<div>POW</div>
<div>MAX</div>
<div>KILL T4</div>
<div>KILL T5</div>
<div>KILL</div>
<div>DEAD T4</div>
<div>DEAD T5</div>
<div>DEAD</div>
</div>
""", unsafe_allow_html=True)

# TABLE ROWS
for i, row in df.iterrows():
    rank = i + 1

    medal = ""
    if rank == 1:
        medal = "🥇"
    elif rank == 2:
        medal = "🥈"
    elif rank == 3:
        medal = "🥉"

    st.markdown(f"""
    <div class="table-row">
        <div>{medal}</div>
        <div>{row['id']}</div>

        <div class="name-cell">
            <div class="avatar"></div>
            {row['name']}
        </div>

        <div class="green">{row['power']:,}</div>
        <div class="yellow">{row['power_max']:,}</div>
        <div class="purple">{row['kill_t4']:,}</div>
        <div class="purple">{row['kill_t5']:,}</div>
        <div class="blue">{row['kill_total']:,}</div>
        <div class="red">{row['dead_t4']:,}</div>
        <div class="red">{row['dead_t5']:,}</div>
        <div class="red">{row['dead_total']:,}</div>
    </div>
    """, unsafe_allow_html=True)

# SIDEBAR KPI
with st.sidebar:
    st.markdown("## 👤 NGƯỜI DÙNG")

    player = st.selectbox("Chọn người chơi", df["name"])
    p = df[df["name"] == player].iloc[0]

    power = st.number_input("POW hiện tại", value=int(p["power"]))
    power_max = st.number_input("POW cao nhất", value=int(p["power_max"]))
    kill_t4 = st.number_input("Kill T4", value=int(p["kill_t4"]))
    kill_t5 = st.number_input("Kill T5", value=int(p["kill_t5"]))
    dead_t4 = st.number_input("Dead T4", value=int(p["dead_t4"]))
    dead_t5 = st.number_input("Dead T5", value=int(p["dead_t5"]))

    st.markdown(f"""
    <div class="summary">
        Kill: {kill_t4 + kill_t5:,}<br>
        Dead: {dead_t4 + dead_t5:,}
    </div>
    """, unsafe_allow_html=True)

    st.button("💾 Lưu")
