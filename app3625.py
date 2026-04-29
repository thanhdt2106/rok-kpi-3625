import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ===== CONFIG =====
st.set_page_config(layout="wide")

st.markdown("""
<style>
[data-testid="stSidebar"] {display:none}
header, footer {display:none}
</style>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi/export?format=csv&gid=855089129"
    df = pd.read_csv(url)

    df.columns = df.columns.str.strip()

    df = df.rename(columns={
        "Tên": "Name",
        "ID": "ID",
        "Liên Minh": "Alliance",
        "Tổng Tiêu Diệt": "Kill",
        "Điểm Chết": "Dead",
        "Sức Mạnh": "Power"
    })

    for col in ["Kill","Dead","Power"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

df = load_data()

# ===== SESSION =====
if "sort" not in st.session_state:
    st.session_state.sort = "Power"

# ===== SEARCH =====
search = st.text_input("🔍 Nhập tên người chơi")

df_show = df.copy()
if search:
    df_show = df[df["Name"].str.contains(search, case=False, na=False)]

# ===== FILTER BUTTONS =====
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⚡ POWER"):
        st.session_state.sort = "Power"

with col2:
    if st.button("🔥 KILL"):
        st.session_state.sort = "Kill"

with col3:
    if st.button("💀 DEAD"):
        st.session_state.sort = "Dead"

# ===== SORT =====
df_show = df_show.sort_values(st.session_state.sort, ascending=False).reset_index(drop=True)

# ===== CARD HTML =====
cards = ""

for i, row in df_show.iterrows():
    rank = i + 1
    name = row["Name"]
    value = int(row[st.session_state.sort])

    cards += f"""
    <div class="card">
        <div class="rank">#{rank}</div>
        <img src="https://api.dicebear.com/7.x/adventurer/png?seed={name}">
        <h3>{name}</h3>
        <p>{value:,}</p>
    </div>
    """

# ===== HTML =====
html = f"""
<style>
body {{
    background:#0b1220;
    color:white;
    font-family:sans-serif;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
    gap:20px;
}}

.card {{
    background:#111;
    padding:20px;
    border-radius:15px;
    text-align:center;
}}

.rank {{
    color:gold;
}}

.card img {{
    width:70px;
    border-radius:50%;
    border:3px solid gold;
}}
</style>

<div class="grid">
{cards}
</div>
"""

components.html(html, height=800)
