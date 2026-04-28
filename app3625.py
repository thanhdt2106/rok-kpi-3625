import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(layout="wide")

# ===== LOAD CSS =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===== DATA =====
df = pd.read_csv("data.csv")
df = df.sort_values("power", ascending=False).reset_index(drop=True)

if "selected" not in st.session_state:
    st.session_state.selected = df.iloc[0]["name"]

col1, col2 = st.columns([1.2,1])

# ================= LEFT =================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🏆 Ranking")

    # TOP 3 PODIUM
    top3 = df.head(3)
    cols = st.columns([1,1.4,1])

    medals = ["🥈","🥇","🥉"]

    for i,(col,(_,row)) in enumerate(zip(cols,top3.iterrows())):
        with col:
            st.markdown(f"""
            <div class="podium">
                <div class="avatar big"></div>
                <div class="medal">{medals[i]}</div>
                <div class="name">{row['name']}</div>
                <div class="score">{row['power']:,}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### All Players")

    max_power = df["power"].max()

    for i,row in df.iterrows():
        active = "active" if row["name"]==st.session_state.selected else ""

        if st.button("", key=i):
            st.session_state.selected = row["name"]

        percent = int(row["power"]/max_power*100)

        st.markdown(f"""
        <div class="row {active}">
            <div class="left">
                <div class="avatar small"></div>
                <span>{i+1}. {row['name']}</span>
            </div>
            <div class="right">
                <div class="bar">
                    <div class="fill" style="width:{percent}%"></div>
                </div>
                <span>{row['power']:,}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= RIGHT =================
with col2:
    p = df[df["name"]==st.session_state.selected].iloc[0]

    st.markdown('<div class="card profile">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="avatar big glow"></div>
    <h2>{p['name']}</h2>
    <p>ID: {p['id']}</p>
    """, unsafe_allow_html=True)

    # KPI
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi">⚔️<br>{p['kill_total']:,}</div>
        <div class="kpi">💀<br>{p['dead_t4']+p['dead_t5']:,}</div>
        <div class="kpi">🌾<br>{p['resource']:,}</div>
        <div class="kpi">🤝<br>{p['help']:,}</div>
    </div>
    """, unsafe_allow_html=True)

    # RADAR
    categories = ['Kill','Dead','Power','Farm','Support']
    values = [
        p['kill_total']/1000000,
        (p['dead_t4']+p['dead_t5'])/100000,
        p['power']/max(df['power'])*100,
        p['resource']/1000000,
        p['help']
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
            radialaxis=dict(visible=True, range=[0,100])
        ),
        showlegend=False,
        paper_bgcolor="#0b0f17"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
