import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

SHEET_ID = "1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE"

URL_BEFORE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617"
URL_AFTER  = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335"

@st.cache_data(ttl=30)
def load_data():
    df1 = pd.read_csv(URL_BEFORE)
    df2 = pd.read_csv(URL_AFTER)

    # ===== CLEAN COLUMN =====
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # ===== FIX ID (QUAN TRỌNG NHẤT) =====
    for df in [df1, df2]:
        df["ID"] = (
            df["ID"]
            .astype(str)
            .str.replace(".0", "", regex=False)
            .str.strip()
        )

    # ===== DROP ID RỖNG =====
    df1 = df1[df1["ID"] != "nan"]
    df2 = df2[df2["ID"] != "nan"]

    # ===== REMOVE DUP =====
    df1 = df1.drop_duplicates(subset="ID")
    df2 = df2.drop_duplicates(subset="ID")

    # ===== MERGE =====
    df = pd.merge(df1, df2, on="ID", suffixes=("_1", "_2"))

    # ===== CONVERT NUMBER =====
    num_cols = [
        "Tổng Tiêu Diệt_1","Tổng Tiêu Diệt_2",
        "Điểm Chết_1","Điểm Chết_2",
        "T4_2","T5_2","Sức Mạnh_2"
    ]

    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    # ===== CALC =====
    df["Kill_Up"] = df["Tổng Tiêu Diệt_2"] - df["Tổng Tiêu Diệt_1"]
    df["Dead_Up"] = df["Điểm Chết_2"] - df["Điểm Chết_1"]

    # ===== SORT =====
    df = df.sort_values(by="Kill_Up", ascending=False)

    df["Rank"] = range(1, len(df)+1)

    return df

df = load_data()

st.title("TEST LOAD DATA FIXED")

st.write("Rows:", len(df))

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
