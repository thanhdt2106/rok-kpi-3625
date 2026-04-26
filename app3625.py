import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ===== LINK =====
SHEET_ID = "1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE"

URL_BEFORE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617"
URL_AFTER  = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335"

# ===== LOAD DATA =====
@st.cache_data(ttl=30)
def load_data():
    df_before = pd.read_csv(URL_BEFORE)
    df_after  = pd.read_csv(URL_AFTER)

    # clean column
    df_before.columns = df_before.columns.str.strip()
    df_after.columns  = df_after.columns.str.strip()

    # ID dạng string
    df_before["ID"] = df_before["ID"].astype(str)
    df_after["ID"]  = df_after["ID"].astype(str)

    # merge theo ID
    df = pd.merge(df_before, df_after, on="ID", suffixes=("_1", "_2"))

    # convert number
    cols = [
        "Tổng Tiêu Diệt_1","Tổng Tiêu Diệt_2",
        "Điểm Chết_1","Điểm Chết_2",
        "T4_2","T5_2","Sức Mạnh_2"
    ]

    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    # tính tăng
    df["Kill_Up"]  = df["Tổng Tiêu Diệt_2"] - df["Tổng Tiêu Diệt_1"]
    df["Dead_Up"]  = df["Điểm Chết_2"] - df["Điểm Chết_1"]

    # sort theo kill tăng
    df = df.sort_values(by="Kill_Up", ascending=False)

    # Rank thay STT
    df["Rank"] = range(1, len(df)+1)

    return df

df = load_data()

# ===== HIỂN THỊ TEST =====
st.title("TEST LOAD DATA")

st.dataframe(
    df[[
        "Rank",
        "Tên_2",
        "ID",
        "Liên Minh_2",
        "Tổng Tiêu Diệt_2",
        "Kill_Up",
        "Sức Mạnh_2",
        "T4_2",
        "T5_2",
        "Điểm Chết_2",
        "Dead_Up"
    ]],
    use_container_width=True
)
