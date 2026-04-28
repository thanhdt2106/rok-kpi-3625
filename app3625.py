import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# ===== FIX FULL WIDTH + HIDE HEADER =====
st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}

.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

section.main > div {
    max-width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ===== PATH =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===== LOAD CSS =====
def load_css():
    with open(os.path.join(BASE_DIR, "style.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ===== LOAD DATA =====
df = pd.read_csv(os.path.join(BASE_DIR, "data.csv"))

# ===== SIDEBAR =====
st.sidebar.title("🎮 Select Player")
selected_name = st.sidebar.selectbox("Player", df["name"])

player = df[df["name"] == selected_name].iloc[0]

# ===== SORT =====
df_sorted = df.sort_values("power", ascending=False).reset_index(drop=True)

# ===== LAYOUT =====
col1, col2 = st.columns([1.1, 1])

# ================= LEFT =================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🏆 Ranking")

    # ===== TOP 3 =====
    top3 = df_sorted.head(3)

    cols = st.columns(3)
    medals = ["🥈", "🥇", "🥉"]

    for i, (col, (_, row)) in enumerate(zip(cols, top3.iterrows())):
        with col:
            st.markdown(f"""
            <div class="top-player">
                <div class="avatar glow"></div>
                <div class="name">{row['name']}</div>
                <div class="score">{row['power']:,}$</div>
                <div class="medal">{medals[i]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### All Players")

    # ===== LIST =====
    for i, row in df_sorted.iterrows():
        active = "active" if row["name"] == selected_name else ""

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
    st.markdown('<div class="card profile">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="avatar big glow"></div>
    <h2>{player['name']}</h2>
    <p class="sub">Member since 2025</p>
    """, unsafe_allow_html=True)

    # STATS
    st.markdown(f"""
    <div class="stats">
        <div><span>Last Game</span><b>Today</b></div>
        <div><span>Winnings</span><b>{player['power']:,}$</b></div>
        <div><span>Games</span><b>{player['games']}</b></div>
    </div>
    """, unsafe_allow_html=True)

    # BUTTONS
    st.markdown("""
    <div class="buttons">
        <button class="follow">Follow</button>
        <button class="msg">Message</button>
    </div>
    """, unsafe_allow_html=True)

    # BADGES
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
