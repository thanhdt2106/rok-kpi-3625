import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="ROK Dashboard", layout="wide")

# ================== LOAD DATA ==================
@st.cache_data(ttl=30)
def load_data():
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid = "855089129"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    return df

df = load_data()

# ================== STYLE ==================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background: #0b1220;
}

/* CARD PLAYER */
.card {
    width: 100%;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 15px;
    background: linear-gradient(145deg, #111827, #0b1220);
    border: 1px solid rgba(255,255,255,0.05);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 25px rgba(255, 200, 0, 0.3);
}

/* PROFILE CARD */
.profile {
    width: 70%;
    margin: auto;
    padding: 40px;
    border-radius: 25px;
    background-size: cover;
    background-position: center;
    color: white;
    position: relative;
}

.overlay {
    position:absolute;
    inset:0;
    background:rgba(0,0,0,0.6);
    border-radius:25px;
}

.content {
    position:relative;
    z-index:2;
}

/* AVATAR */
.avatar {
    width:90px;
    height:90px;
    border-radius:50%;
    border:3px solid gold;
    margin-right:15px;
}

/* STATS BOX */
.stat-box {
    flex:1;
    padding:20px;
    border-radius:15px;
    text-align:center;
    background:rgba(0,0,0,0.5);
    backdrop-filter: blur(10px);
}

/* SEARCH */
input {
    border-radius:10px !important;
}
</style>
""", unsafe_allow_html=True)

# ================== SEARCH ==================
st.title("🔥 ROK MEMBER DASHBOARD")

search = st.text_input("🔍 Nhập tên người chơi")

# ================== FILTER ==================
if search:
    df_filtered = df[df["Name"].str.contains(search, case=False, na=False)]
else:
    df_filtered = df

# ================== VIEW MODE ==================
if "view_profile" not in st.session_state:
    st.session_state.view_profile = None

# ================== LIST MEMBER ==================
if st.session_state.view_profile is None:

    st.subheader("👥 Danh sách thành viên")

    for i, row in df_filtered.iterrows():
        col1, col2 = st.columns([1, 6])

        with col1:
            st.image(f"https://api.dicebear.com/7.x/adventurer/png?seed={row['Name']}", width=60)

        with col2:
            st.markdown(f"""
            <div class="card">
                <b>{row['Name']}</b><br>
                Power: {row.get('Power','N/A')}<br>
                Kill: {row.get('Kill','N/A')}
            </div>
            """, unsafe_allow_html=True)

        if st.button(f"Xem profile {row['Name']}", key=i):
            st.session_state.view_profile = row.to_dict()
            st.rerun()

# ================== PROFILE ==================
else:
    p = st.session_state.view_profile

    bg = "https://i.imgur.com/6Iej2c3.jpg"

    st.markdown(f"""
    <div class="profile" style="background-image:url('{bg}')">
        <div class="overlay"></div>

        <div class="content">

            <div style="display:flex;align-items:center;margin-bottom:20px;">
                <img class="avatar" src="https://api.dicebear.com/7.x/adventurer/png?seed={p['Name']}"/>
                <h2 style="color:gold;">{p['Name']}</h2>
            </div>

            <div style="display:flex;gap:20px;margin-top:20px;">
                <div class="stat-box">
                    <small>ID</small><br>
                    {p.get('ID','N/A')}
                </div>

                <div class="stat-box">
                    <small>Alliance</small><br>
                    {p.get('Alliance','N/A')}
                </div>

                <div class="stat-box">
                    <small>Kill</small><br>
                    {p.get('Kill','N/A')}
                </div>

                <div class="stat-box">
                    <small>Dead</small><br>
                    {p.get('Dead','N/A')}
                </div>
            </div>

        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅ Quay lại"):
        st.session_state.view_profile = None
        st.rerun()
