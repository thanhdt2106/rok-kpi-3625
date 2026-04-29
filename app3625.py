import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== LOAD DATA =====
@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid = "855089129"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df.columns = [c.strip() for c in df.columns]
    return df

df = load_data()

# ===== SEARCH =====
search = st.text_input("🔎 Nhập tên người chơi")

if search:
    df_filtered = df[df["Tên"].str.contains(search, case=False, na=False)]
else:
    df_filtered = df

# ===== BUILD MEMBER GRID =====
cards_html = ""

for _, row in df_filtered.head(20).iterrows():
    cards_html += f"""
    <div class="member" onclick="showProfile('{row['Tên']}')">
        <img src="https://api.dicebear.com/7.x/adventurer/png?seed={row['Tên']}"/>
        <div class="m-name">{row['Tên']}</div>
        <div class="m-power">{row['Tổng Tiêu Diệt']:,}</div>
    </div>
    """

# ===== PROFILE DATA (JS) =====
import json
data_json = df.to_json(orient="records", force_ascii=False)

# ===== HTML =====
html = f"""
<html>
<head>
<style>

body {{
    margin:0;
    background:#020c1b;
    font-family:Arial;
    color:white;
}}

/* ===== HEADER ===== */
.header {{
    padding:20px 40px;
    font-size:28px;
    font-weight:bold;
    color:gold;
}}

/* ===== GRID ===== */
.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill, minmax(180px,1fr));
    gap:20px;
    padding:20px 40px;
}}

.member {{
    background:rgba(255,255,255,0.05);
    border-radius:15px;
    padding:15px;
    text-align:center;
    cursor:pointer;
    transition:0.3s;
}}

.member:hover {{
    transform:scale(1.05);
    box-shadow:0 0 20px gold;
}}

.member img {{
    width:60px;
    height:60px;
    border-radius:50%;
    border:2px solid gold;
}}

.m-name {{
    margin-top:10px;
    font-weight:bold;
}}

.m-power {{
    font-size:12px;
    opacity:0.7;
}}

/* ===== PROFILE MODAL ===== */
.modal {{
    position:fixed;
    inset:0;
    background:rgba(0,0,0,0.8);
    display:none;
    justify-content:center;
    align-items:center;
}}

.card {{
    width:70%;
    height:65%;
    border-radius:25px;
    background:url("https://i.imgur.com/6Iej2c3.jpg") center/cover;
    position:relative;
    overflow:hidden;
}}

.overlay {{
    position:absolute;
    inset:0;
    background:rgba(0,0,0,0.65);
}}

.content {{
    position:relative;
    z-index:2;
    padding:30px;
    height:100%;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
}}

.top {{
    display:flex;
    align-items:center;
    gap:15px;
}}

.avatar {{
    width:80px;
    height:80px;
    border-radius:50%;
    border:3px solid gold;
}}

.name {{
    font-size:26px;
    color:gold;
}}

.info {{
    display:flex;
    gap:15px;
    margin-top:15px;
}}

.box {{
    flex:1;
    background:rgba(255,255,255,0.08);
    padding:15px;
    border-radius:12px;
}}

.stats {{
    display:flex;
    gap:20px;
}}

.stat {{
    flex:1;
    background:rgba(0,0,0,0.6);
    padding:20px;
    border-radius:15px;
    text-align:center;
}}

.highlight {{
    border:2px solid gold;
    box-shadow:0 0 20px gold;
}}

.close {{
    position:absolute;
    top:15px;
    right:20px;
    cursor:pointer;
    font-size:20px;
}}

</style>
</head>

<body>

<div class="header">🔥 ROK MEMBER DASHBOARD</div>

<div class="grid">
{cards_html}
</div>

<!-- PROFILE -->
<div class="modal" id="modal">
    <div class="card">
        <div class="overlay"></div>
        <div class="content" id="profile"></div>
        <div class="close" onclick="closeModal()">✖</div>
    </div>
</div>

<script>

const data = {data_json};

function showProfile(name) {{
    const player = data.find(p => p["Tên"] === name);

    document.getElementById("profile").innerHTML = `
        <div>
            <div class="top">
                <img class="avatar" src="https://api.dicebear.com/7.x/adventurer/png?seed=${{player["Tên"]}}">
                <div class="name">${{player["Tên"]}}</div>
            </div>

            <div class="info">
                <div class="box">ID<br><b>${{player["ID"]}}</b></div>
                <div class="box">Alliance<br><b>${{player["Liên Minh"]}}</b></div>
                <div class="box">Power<br><b>${{player["Tổng Tiêu Diệt"]}}</b></div>
                <div class="box">Dead<br><b>${{player["Điểm Chết"]}}</b></div>
            </div>
        </div>

        <div class="stats">
            <div class="stat highlight">🏆<br>#${{player["STT"]}}</div>
            <div class="stat">🔥<br>${{player["T5"]}}</div>
            <div class="stat">💀<br>${{player["Điểm Chết"]}}</div>
        </div>
    `;

    document.getElementById("modal").style.display = "flex";
}}

function closeModal() {{
    document.getElementById("modal").style.display = "none";
}}

</script>

</body>
</html>
"""

components.html(html, height=900, scrolling=False)
