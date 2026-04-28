import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(layout="wide")

# ===== LOAD CSS =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===== LOAD DATA =====
df = pd.read_csv(os.path.join(BASE_DIR, "data.csv"))
df = df.sort_values("power", ascending=False).reset_index(drop=True)

# ===== SESSION =====
if "selected" not in st.session_state:
    st.session_state.selected = df.iloc[0]["name"]

# ===== LAYOUT =====
col1, col2 = st.columns([1.2, 1])

# ================= LEFT =================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🏆 Ranking")

    # TOP 3
    top3 = df.head(3)
    cols = st.columns([1, 1.3, 1])

    for i, (col, (_, row)) in enumerate(zip(cols, top3.iterrows())):
        with col:
            st.markdown(f"""
            <div class="top-player">
                <div class="avatar big"></div>
                <div>{row['name']}</div>
                <div>{row['power']:,}$</div>
                <div>{['🥈','🥇','🥉'][i]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### All Players")

    # LIST CLICK
    for i, row in df.iterrows():
        active = "active" if row["name"] == st.session_state.selected else ""

        if st.button("", key=f"btn{i}"):
            st.session_state.selected = row["name"]

        st.markdown(f"""
        <div class="row {active}">
            <div class="left">
                <div class="avatar small"></div>
                <span>{i+1}. {row['name']}</span>
            </div>
            <div>{row['power']:,}$</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================= RIGHT =================
with col2:
    player = df[df["name"] == st.session_state.selected].iloc[0]

    st.markdown('<div class="card profile">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="avatar big"></div>
    <h2>{player['name']}</h2>
    <p class="sub">Member since 2025</p>
    """, unsafe_allow_html=True)

    # STATS
    st.markdown(f"""
    <div class="stats">
        <div><span>Kill</span><b>{player['kill']}</b></div>
        <div><span>Dead</span><b>{player['dead']}</b></div>
        <div><span>Games</span><b>{player['games']}</b></div>
    </div>
    """, unsafe_allow_html=True)

    # ===== RADAR KPI =====
    categories = ['Kill', 'Dead', 'Power', 'Gather', 'Activity']

    values = [
        player['kill'],
        player['dead'],
        player['power'] / max(df['power']) * 100,
        player['gather'],
        player['activity']
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line=dict(color='#00c6ff', width=3),
        fillcolor='rgba(0,198,255,0.3)'
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="#0b0f17",
            radialaxis=dict(
                visible=True,
                range=[0,100],
                gridcolor="rgba(255,255,255,0.1)"
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(color="white")
            )
        ),
        showlegend=False,
        paper_bgcolor="#0b0f17",
        margin=dict(l=10, r=10, t=10, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)

    # BUTTON
    st.markdown("""
    <div class="buttons">
        <button class="follow">Follow</button>
        <button class="msg">Message</button>
    </div>
    """, unsafe_allow_html=True)

    # BADGES
    st.markdown("""
    <div class="badges">
        <div class="badge gold"></div>
        <div class="badge green"></div>
        <div class="badge purple"></div>
        <div class="badge gray"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
