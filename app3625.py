import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# ===== LOAD CSS =====
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===== LOAD DATA =====
df = pd.read_csv("data.csv")

# ===== MENU =====
menu = st.session_state.get("menu", "Trang chủ")

col_menu = st.columns([1,2,2,2,1])
with col_menu[1]:
    if st.button("🏠 Trang chủ"):
        st.session_state.menu = "Trang chủ"
with col_menu[2]:
    if st.button("👤 Profile"):
        st.session_state.menu = "Profile"
with col_menu[3]:
    if st.button("⚙️ Người dùng"):
        st.session_state.menu = "Người dùng"

menu = st.session_state.get("menu", "Trang chủ")

# ================== TRANG CHỦ ==================
if menu == "Trang chủ":
    st.markdown("## 🏆 BẢNG KPI")

    st.dataframe(
        df[[
            "id","name","power","power_max",
            "kill_t4","kill_t5","kill_total",
            "dead_t4","dead_t5","dead_total"
        ]],
        use_container_width=True
    )

# ================== PROFILE ==================
elif menu == "Profile":
    player = st.selectbox("Chọn người chơi", df["name"])

    p = df[df["name"]==player].iloc[0]

    st.markdown(f"""
    ### 👤 {p['name']}
    ID: {p['id']}
    """)

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("⚡ Power", f"{p['power']:,}")
    col2.metric("🏆 Max Power", f"{p['power_max']:,}")
    col3.metric("⚔️ Kill", f"{p['kill_total']:,}")
    col4.metric("💀 Dead", f"{p['dead_total']:,}")

# ================== NGƯỜI DÙNG (EDIT KPI) ==================
elif menu == "Người dùng":

    st.markdown("## ⚙️ CHỈNH KPI")

    player = st.selectbox("Chọn người chơi", df["name"])
    idx = df[df["name"]==player].index[0]

    # INPUT KPI
    power = st.number_input("Power hiện tại", value=int(df.loc[idx,"power"]))
    power_max = st.number_input("Power cao nhất", value=int(df.loc[idx,"power_max"]))

    kill_t4 = st.number_input("Kill T4", value=int(df.loc[idx,"kill_t4"]))
    kill_t5 = st.number_input("Kill T5", value=int(df.loc[idx,"kill_t5"]))

    dead_t4 = st.number_input("Dead T4", value=int(df.loc[idx,"dead_t4"]))
    dead_t5 = st.number_input("Dead T5", value=int(df.loc[idx,"dead_t5"]))

    # AUTO CALC
    kill_total = kill_t4 + kill_t5
    dead_total = dead_t4 + dead_t5

    st.markdown(f"""
    **Kill tổng:** {kill_total:,}  
    **Dead tổng:** {dead_total:,}
    """)

    # SAVE
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
        df.to_csv("data.csv", index=False)
        st.success("Đã lưu!")
