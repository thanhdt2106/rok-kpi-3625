import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ================= LOAD DATA =================
@st.cache_data(ttl=30)
def load_data():
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid = "855089129"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    df = pd.read_csv(url)

    # Chuẩn hoá cột
    df.columns = df.columns.str.strip().str.lower()

    return df

df = load_data()

# ================= MAP COLUMN =================
col_map = {
    "name": "tên",
    "id": "id",
    "alliance": "liên minh",
    "kill": "tổng tiêu diệt",
    "power": "sức mạnh",
    "dead": "điểm chết"
}

# ================= SEARCH =================
st.title("🔥 ROK MEMBER DASHBOARD")

search = st.text_input("🔍 Nhập tên người chơi")

if search:
    df_filtered = df[df[col_map["name"]].astype(str).str.contains(search, case=False, na=False)]
else:
    df_filtered = df

# ================= VIEW STATE =================
if "profile" not in st.session_state:
    st.session_state.profile = None

# ================= LIST =================
if st.session_state.profile is None:

    for i, row in df_filtered.iterrows():

        col1, col2, col3 = st.columns([1,6,2])

        with col1:
            st.image(f"https://api.dicebear.com/7.x/adventurer/png?seed={row[col_map['name']]}", width=60)

        with col2:
            st.markdown(f"""
            <div style="
                padding:15px;
                border-radius:15px;
                background:#111;
                border:1px solid rgba(255,255,255,0.05);
            ">
                <b style="color:gold">{row[col_map['name']]}</b><br>
                Power: {row[col_map['power']]:,}<br>
                Kill: {row[col_map['kill']]:,}
            </div>
            """, unsafe_allow_html=True)

        with col3:
            if st.button("Xem", key=i):
                st.session_state.profile = row.to_dict()
                st.rerun()

# ================= PROFILE =================
else:
    p = st.session_state.profile

    st.markdown(f"""
    <div style="
        width:70%;
        margin:auto;
        padding:40px;
        border-radius:25px;
        background:url('https://i.imgur.com/6Iej2c3.jpg');
        background-size:cover;
        color:white;
        position:relative;
    ">

        <div style="
            position:absolute;
            inset:0;
            background:rgba(0,0,0,0.7);
            border-radius:25px;
        "></div>

        <div style="position:relative;z-index:2">

            <div style="display:flex;align-items:center;margin-bottom:20px;">
                <img src="https://api.dicebear.com/7.x/adventurer/png?seed={p[col_map['name']]}" 
                style="width:90px;height:90px;border-radius:50%;border:3px solid gold;margin-right:15px;"/>
                
                <h2 style="color:gold;">{p[col_map['name']]}</h2>
            </div>

            <div style="display:flex;gap:20px;flex-wrap:wrap;">

                <div style="flex:1;background:#111;padding:20px;border-radius:15px;">
                    <small>ID</small><br>{p[col_map['id']]}
                </div>

                <div style="flex:1;background:#111;padding:20px;border-radius:15px;">
                    <small>Alliance</small><br>{p[col_map['alliance']]}
                </div>

                <div style="flex:1;background:#111;padding:20px;border-radius:15px;">
                    <small>Power</small><br>{p[col_map['power']]:,}
                </div>

                <div style="flex:1;background:#111;padding:20px;border-radius:15px;">
                    <small>Kill</small><br>{p[col_map['kill']]:,}
                </div>

                <div style="flex:1;background:#111;padding:20px;border-radius:15px;">
                    <small>Dead</small><br>{p[col_map['dead']]:,}
                </div>

            </div>

        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅ Quay lại"):
        st.session_state.profile = None
        st.rerun()
