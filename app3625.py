import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# ===== LOAD CSS =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===== LOAD DATA =====
df = pd.read_csv(os.path.join(BASE_DIR, "data.csv"))
df = df.sort_values("power", ascending=False).reset_index(drop=True)

# ===== SESSION (CLICK PLAYER) =====
if "selected" not in st.session_state:
    st.session_state.selected = df.iloc[0]["name"]

# ===== LAYOUT =====
col1, col2 = st.columns([1.2, 1])

# ================= LEFT =================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🏆 Ranking")

    # ===== TOP 3 =====
    top3 = df.head(3)
    cols = st.columns([1, 1.2, 1])

    for i, (col, (_, row)) in enumerate(zip(cols, top3.iterrows())):
        with col:
            st.markdown(f"""
            <div class="top-player">
                <div class="avatar big"></div>
                <div class="name">{row['name']}</div>
                <div class="score">{row['power']:,}$</div>
                <div class="medal">{['🥈','🥇','🥉'][i]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### All Players")

    # ===== LIST (CLICKABLE) =====
    for i, row in df.iterrows():
        active = "active" if row["name"] == st.session_state.selected else ""

        if st.button(f"{i+1}. {row['name']}   {row['power']:,}$", key=i):
            st.session_state.selected = row["name"]

        st.markdown(f"""
        <div class="row {active}">
            <div class="left">
                <div class="avatar small"></div>
                <span>{i+1}. {row['name']}</span>
            </div>
            <div class="right">{row['power']:,}$</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================= RIGHT =================
with col2:
    player = df[df["name"] == st.session_state.selected].iloc[0]

    st.markdown('<div class="card profile">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="avatar big glow"></div>
    <h2>{player['name']}</h2>
    <p class="sub">Member since 2025</p>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stats">
        <div><span>Last Game</span><b>Today</b></div>
        <div><span>Winnings</span><b>{player['power']:,}$</b></div>
        <div><span>Games</span><b>{player['games']}</b></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="buttons">
        <button class="follow">Follow</button>
        <button class="msg">Message</button>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h4>Awards & Badges</h4>
    <div class="badges">
        <div class="badge gold"></div>
        <div class="badge green"></div>
        <div class="badge purple"></div>
        <div class="badge gray"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
