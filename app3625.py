import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# LOAD CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = pd.read_csv("data.csv")
df.columns = df.columns.str.strip().str.lower()
df = df.sort_values("power", ascending=False).reset_index(drop=True)

# ===== LAYOUT =====
left, right = st.columns([2.2,1])

# ================= LEFT =================
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("## 🏆 BẢNG XẾP HẠNG KPI")

    # HEADER
    st.markdown("""
    <div class="table-header">
        <div>#</div>
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

    # ROWS
    for i,row in df.iterrows():

        medal = "🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else i+1

        st.markdown(f"""
        <div class="row">
            <div class="rank">{medal}</div>

            <div class="name">
                <div class="avatar"></div>
                {row['name']}
            </div>

            <div class="pow">{row['power']:,}</div>
            <div class="max">{row['power_max']:,}</div>

            <div class="t4">{row['kill_t4']:,}</div>
            <div class="t5">{row['kill_t5']:,}</div>
            <div class="kill">{row['kill_total']:,}</div>

            <div class="d4">{row['dead_t4']:,}</div>
            <div class="d5">{row['dead_t5']:,}</div>
            <div class="dead">{row['dead_total']:,}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= RIGHT =================
with right:
    st.markdown('<div class="card side">', unsafe_allow_html=True)

    st.markdown("## 👤 NGƯỜI DÙNG")

    player = st.selectbox("Chọn người chơi", df["name"])
    idx = df[df["name"]==player].index[0]

    p = df.loc[idx]

    power = st.number_input("POW hiện tại", value=int(p["power"]))
    power_max = st.number_input("POW cao nhất", value=int(p["power_max"]))

    kill_t4 = st.number_input("Kill T4", value=int(p["kill_t4"]))
    kill_t5 = st.number_input("Kill T5", value=int(p["kill_t5"]))

    dead_t4 = st.number_input("Dead T4", value=int(p["dead_t4"]))
    dead_t5 = st.number_input("Dead T5", value=int(p["dead_t5"]))

    kill_total = kill_t4 + kill_t5
    dead_total = dead_t4 + dead_t5

    st.markdown(f"""
    <div class="summary">
    Kill: {kill_total:,} <br>
    Dead: {dead_total:,}
    </div>
    """, unsafe_allow_html=True)

    if st.button("💾 Lưu"):
        df.loc[idx] = [
            p["id"], player,
            power, power_max,
            kill_t4, kill_t5, kill_total,
            dead_t4, dead_t5, dead_total
        ]
        df.to_csv("data.csv", index=False)
        st.success("Đã lưu!")

    st.markdown("</div>", unsafe_allow_html=True)
