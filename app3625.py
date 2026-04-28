import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# ===== PATH (QUAN TRỌNG) =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_css():
    css_path = os.path.join(BASE_DIR, "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

data_path = os.path.join(BASE_DIR, "data.csv")
df = pd.read_csv(data_path)

# ===== SIDEBAR =====
st.sidebar.title("🎮 Select Player")
players = df["name"].tolist()
selected_name = st.sidebar.selectbox("Player", players)

player = df[df["name"] == selected_name].iloc[0]

# ===== SORT RANK =====
df_sorted = df.sort_values("power", ascending=False).reset_index(drop=True)

# ===== LAYOUT =====
col1, col2 = st.columns([1.1, 1])

# ================= LEFT - RANK =================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h3>🏆 Ranking</h3>", unsafe_allow_html=True)

    # TOP 3
    top3 = df_sorted.head(3)

    st.markdown('<div class="top3">', unsafe_allow_html=True)

    medals = ["🥈", "🥇", "🥉"]

    for i, row in top3.iterrows():
        st.markdown(f"""
        <div class="top-player">
            <div class="avatar glow"></div>
            <div class="name">{row['name']}</div>
            <div class="score">{row['power']:,}$</div>
            <div class="medal">{medals[i]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # LIST
    st.markdown("<h4>All Players</h4>", unsafe_allow_html=True)

    for i, row in df_sorted.iterrows():
        highlight = "active" if row["name"] == selected_name else ""

        st.markdown(f"""
        <div class="row {highlight}">
            <div class="left">
                <div class="avatar small"></div>
                <span>{i+1}. {row['name']}</span>
            </div>
            <div class="right">{row['power']:,}$</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================= RIGHT - PROFILE =================
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
