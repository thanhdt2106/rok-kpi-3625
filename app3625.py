import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ================= CONFIG =================
REQUIRED_COLS = [
    "id","name","power","power_max",
    "kill_t4","kill_t5","kill_total",
    "dead_t4","dead_t5","dead_total"
]

DATA_FILE = "data.csv"

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    # clean column
    df.columns = df.columns.str.strip().str.lower()

    # check missing
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        st.error(f"❌ Thiếu cột: {missing}")
        st.stop()

    return df

df = load_data()

# ================= SAVE DATA =================
def save_data(df):
    df.to_csv(DATA_FILE, index=False)
    st.cache_data.clear()

# ================= MENU =================
if "menu" not in st.session_state:
    st.session_state.menu = "Trang chủ"

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Trang chủ"):
        st.session_state.menu = "Trang chủ"

with col2:
    if st.button("👤 Profile"):
        st.session_state.menu = "Profile"

with col3:
    if st.button("⚙️ Người dùng"):
        st.session_state.menu = "Người dùng"

# ================= TRANG CHỦ =================
if st.session_state.menu == "Trang chủ":

    st.markdown("## 🏆 BẢNG KPI")

    df_sorted = df.sort_values("power", ascending=False)

    st.dataframe(df_sorted[REQUIRED_COLS], use_container_width=True)

# ================= PROFILE =================
elif st.session_state.menu == "Profile":

    player = st.selectbox("Chọn người chơi", df["name"])
    p = df[df["name"] == player].iloc[0]

    st.markdown(f"## 👤 {p['name']}")
    st.caption(f"ID: {p['id']}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("⚡ Power", f"{p['power']:,}")
    col2.metric("🏆 Max Power", f"{p['power_max']:,}")
    col3.metric("⚔️ Kill", f"{p['kill_total']:,}")
    col4.metric("💀 Dead", f"{p['dead_total']:,}")

# ================= EDIT KPI =================
elif st.session_state.menu == "Người dùng":

    st.markdown("## ⚙️ CHỈNH KPI")

    player = st.selectbox("Chọn người chơi", df["name"])
    idx = df[df["name"] == player].index[0]

    col1, col2 = st.columns(2)

    with col1:
        power = st.number_input("Power hiện tại", value=int(df.loc[idx,"power"]))
        power_max = st.number_input("Power cao nhất", value=int(df.loc[idx,"power_max"]))

        kill_t4 = st.number_input("Kill T4", value=int(df.loc[idx,"kill_t4"]))
        kill_t5 = st.number_input("Kill T5", value=int(df.loc[idx,"kill_t5"]))

    with col2:
        dead_t4 = st.number_input("Dead T4", value=int(df.loc[idx,"dead_t4"]))
        dead_t5 = st.number_input("Dead T5", value=int(df.loc[idx,"dead_t5"]))

    # AUTO CALC
    kill_total = kill_t4 + kill_t5
    dead_total = dead_t4 + dead_t5

    st.info(f"⚔️ Kill tổng: {kill_total:,}")
    st.info(f"💀 Dead tổng: {dead_total:,}")

    if st.button("💾 Lưu thay đổi"):
        df.loc[idx] = [
            df.loc[idx,"id"],
            player,
            power,
            power_max,
            kill_t4,
            kill_t5,
            kill_total,
            dead_t4,
            dead_t5,
            dead_total
        ]
        save_data(df)
        st.success("✅ Đã lưu!")
