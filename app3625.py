# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ================= CSS =================
st.markdown("""
<style>
body {background:#050a0e;color:white;}
.header {
font-size:28px;
font-weight:bold;
color:#00d4ff;
text-shadow:0 0 15px #00d4ff;
}

.card {
background:#0f172a;
border-radius:14px;
padding:15px;
box-shadow:0 0 15px rgba(0,212,255,.2);
}

.player-name{
font-size:26px;
font-weight:bold;
color:white;
text-shadow:0 0 12px #00d4ff;
}

.rank-box{
margin-top:8px;
display:inline-block;
padding:6px 14px;
border:1px solid #00d4ff;
border-radius:10px;
color:#ffd700;
font-weight:bold;
}

.kpi-circle{
width:140px;
height:140px;
border-radius:50%;
display:flex;
align-items:center;
justify-content:center;
font-size:26px;
font-weight:bold;
margin:auto;
box-shadow:0 0 25px #00d4ff;
}
</style>
""", unsafe_allow_html=True)

# ================= DATA =================
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    dt = pd.read_csv(URL_T)
    ds = pd.read_csv(URL_S)

    dt.columns = dt.columns.str.strip()
    ds.columns = ds.columns.str.strip()

    dt['ID'] = dt['ID'].astype(str)
    ds['ID'] = ds['ID'].astype(str)

    df = pd.merge(dt, ds, on='ID', suffixes=('_1','_2'))

    for c in ['Tổng Tiêu Diệt_1','Tổng Tiêu Diệt_2','Điểm Chết_1','Điểm Chết_2','Sức Mạnh_2']:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
    df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']

    df = df.sort_values(by='KI', ascending=False)
    df['Rank'] = range(1,len(df)+1)

    df['Search'] = df['Tên_2'] + " (" + df['ID'] + ")"

    df['KPI'] = ((df['KI']/200_000_000)+(df['DI']/300_000))*50
    df['KPI'] = df['KPI'].clip(0,100)

    return df

df = load_data()

# ================= HEADER =================
st.markdown('<div class="header">🏆 BẢNG XẾP HẠNG PRO MAX</div>', unsafe_allow_html=True)

# ================= SEARCH =================
search = st.selectbox("", df['Search'], index=None, placeholder="🔍 Tìm player...")

# ================= PROFILE =================
if search:
    p = df[df['Search']==search].iloc[0]

    kpi = int(p['KPI'])

    html = f"""
    <div class="card" style="margin-top:20px;text-align:center;">
        <img src="https://api.dicebear.com/7.x/bottts/svg?seed={p['Tên_2']}" 
        style="width:90px;border-radius:50%;box-shadow:0 0 20px #00d4ff;">

        <div class="player-name">{p['Tên_2']}</div>

        <div class="rank-box">
        &#127942; Rank #{int(p['Rank'])}
        </div>

        <div style="margin-top:15px;">
            ⚡ Power: {int(p['Sức Mạnh_2']):,}<br>
            ⚔ Kill: {int(p['Tổng Tiêu Diệt_2']):,} (+{int(p['KI']):,})<br>
            💀 Death: {int(p['Điểm Chết_2']):,} (+{int(p['DI']):,})
        </div>

        <div style="margin-top:20px;">
            <div class="kpi-circle"
            style="background:conic-gradient(#00d4ff {kpi}%, #1e293b 0);">
            {kpi}%
            </div>
            KPI
        </div>
    </div>
    """

    components.html(html, height=400)

# ================= TABLE =================
st.markdown("### 📊 Top Ranking")

table_html = "<div class='card'><table style='width:100%;text-align:center;'>"
table_html += "<tr><th>#</th><th>Name</th><th>Kill+</th><th>Death+</th><th>KPI</th></tr>"

for _,r in df.head(30).iterrows():
    table_html += f"""
    <tr>
    <td style="color:#ffd700;">#{int(r['Rank'])}</td>
    <td>{r['Tên_2']}</td>
    <td style="color:#00d4ff;">+{int(r['KI']):,}</td>
    <td style="color:#ff4b4b;">+{int(r['DI']):,}</td>
    <td style="color:#ffd700;">{int(r['KPI'])}%</td>
    </tr>
    """

table_html += "</table></div>"

st.markdown(table_html, unsafe_allow_html=True)
