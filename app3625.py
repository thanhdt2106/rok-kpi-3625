import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Load CSS
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Load data
df = pd.read_csv("data.csv")

# Sidebar chọn player
player_names = df["name"].tolist()
selected = st.sidebar.selectbox("Select Player", player_names)

player = df[df["name"] == selected].iloc[0]

# Layout
col1, col2 = st.columns([1,1])

# LEFT - RANK
with col1:
    st.markdown("### 🏆 Rank")

    # Top 3
    top3 = df.sort_values("power", ascending=False).head(3)

    st.markdown('<div class="top3">', unsafe_allow_html=True)
    for i, row in top3.iterrows():
        st.markdown(f"""
        <div class="top-player">
            <div class="avatar"></div>
            <div>{row['name']}</div>
            <div class="score">{row['power']}$</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # List
    st.markdown("#### Ranking List")

    ranked = df.sort_values("power", ascending=False)

    for i, row in ranked.iterrows():
        st.markdown(f"""
        <div class="row">
            <div class="left">
                <div class="avatar small"></div>
                <span>{row['name']}</span>
            </div>
            <div class="right">{row['power']}$</div>
        </div>
        """, unsafe_allow_html=True)

# RIGHT - PROFILE
with col2:
    st.markdown("### 👤 Profile")

    st.markdown(f"""
    <div class="profile">
        <div class="avatar big"></div>
        <h2>{player['name']}</h2>
        <p>Member since 2025</p>

        <div class="stats">
            <div><span>Last Game</span><b>Today</b></div>
            <div><span>Winnings</span><b>{player['power']}$</b></div>
            <div><span>Games</span><b>{player['games']}</b></div>
        </div>

        <div class="buttons">
            <button class="follow">Follow</button>
            <button class="msg">Message</button>
        </div>

        <h3>Awards</h3>
        <div class="badges">
            <div class="badge"></div>
            <div class="badge"></div>
            <div class="badge"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
