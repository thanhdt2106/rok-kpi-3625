import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== LOAD DATA GOOGLE SHEET =====
@st.cache_data
def load_data():
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid = "855089129"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)

    # rename cho chắc
    df.columns = [c.strip() for c in df.columns]

    return df

df = load_data()

# ===== SEARCH =====
search = st.text_input("🔎 Nhập tên người chơi")

if search:
    df = df[df["Tên"].str.contains(search, case=False, na=False)]

# ===== RENDER HTML =====
html = ""

for _, row in df.head(1).iterrows():
    html += f"""
    <html>
    <head>
    <style>
    body {{
        margin:0;
        background:#020c1b;
        font-family:Arial;
        color:white;
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
    }}

    .card {{
        width:70%;
        height:65%;
        border-radius:25px;
        background:url("https://i.imgur.com/6Iej2c3.jpg") center/cover no-repeat;
        position:relative;
        overflow:hidden;
        box-shadow:0 0 60px rgba(255,215,0,0.3);
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
        box-shadow:0 0 20px gold;
    }}

    .name {{
        font-size:26px;
        color:gold;
        font-weight:bold;
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
        backdrop-filter:blur(10px);
    }}

    .stats {{
        display:flex;
        gap:20px;
        margin-top:20px;
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

    </style>
    </head>

    <body>
        <div class="card">
            <div class="overlay"></div>

            <div class="content">

                <div>
                    <div class="top">
                        <img src="https://api.dicebear.com/7.x/adventurer/png?seed={row['Tên']}" class="avatar"/>
                        <div class="name">{row['Tên']}</div>
                    </div>

                    <div class="info">
                        <div class="box">ID<br><b>{row['ID']}</b></div>
                        <div class="box">Alliance<br><b>{row['Liên Minh']}</b></div>
                        <div class="box">Power<br><b>{row['Tổng Tiêu Diệt']:,}</b></div>
                        <div class="box">Dead<br><b>{row['Điểm Chết']:,}</b></div>
                    </div>
                </div>

                <div class="stats">
                    <div class="stat highlight">
                        🏆<br><b>#{row['STT']}</b>
                    </div>

                    <div class="stat">
                        🔥<br><b>{row['T5']:,}</b>
                    </div>

                    <div class="stat">
                        💀<br><b>{row['Điểm Chết']:,}</b>
                    </div>
                </div>

            </div>
        </div>
    </body>
    </html>
    """

# ===== RENDER =====
components.html(html, height=700, scrolling=False)
