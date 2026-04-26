import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== CSS =====
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none;}
header {visibility:hidden;}
.block-container {padding:0;margin:0;}

body{
background: radial-gradient(circle at top,#020617,#000814);
color:white;
font-family:'Segoe UI';
}

.table-wrap{
margin:20px;
border:1px solid rgba(34,211,238,.3);
border-radius:16px;
overflow:hidden;
box-shadow:0 0 20px rgba(34,211,238,.1);
}

table{width:100%;border-collapse:collapse;}

th,td{
padding:10px;
text-align:center;
font-size:12px;
}

tr:hover{background:rgba(34,211,238,.08);}

.kill{color:#facc15;}
.power{color:#22d3ee;}
.death{color:#ef4444;}
.up{color:#22c55e;}
.down{color:#ef4444;}

.avatar{
width:30px;height:30px;border-radius:50%;
border:2px solid #22d3ee;
box-shadow:0 0 8px #22d3ee;
}
</style>
""", unsafe_allow_html=True)

# ===== DATA (GIỮ NGUYÊN) =====
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    dt = pd.read_csv(URL_T).rename(columns=lambda x: x.strip())
    ds = pd.read_csv(URL_S).rename(columns=lambda x: x.strip())

    for d in [dt, ds]:
        d['ID'] = d['ID'].astype(str).str.replace(r'\.0$', '', regex=True)

    df = pd.merge(dt, ds, on='ID', suffixes=('_1', '_2'))

    df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
    df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']

    df['Rank'] = df['KI'].rank(ascending=False, method='min').astype(int)

    df['KPI'] = ((df['KI'] / 200_000_000) * 100).clip(0,100).round(1)

    return df

df = load_data()

# ===== SEARCH =====
search = st.text_input("🔍 Search")

if search:
    df = df[df['Tên_2'].str.contains(search, case=False) | df['ID'].astype(str).str.contains(search)]

# ===== TABLE =====
df = df.sort_values("KI", ascending=False)

rows = ""
for i, r in df.iterrows():
    rows += f"""
<tr>
<td>{int(r['Rank'])}</td>

<td style="display:flex;align-items:center;gap:10px;">
<img src="https://api.dicebear.com/7.x/bottts/svg?seed={r['Tên_2']}" class="avatar">
{r['Tên_2']}
</td>

<td>{r['ID']}</td>
<td style="color:#f97316">{r['Liên Minh_2']}</td>

<td class="kill">{int(r['Tổng Tiêu Diệt_2']):,}<br>
<span class="up">▲ {int(r['KI']):,}</span></td>

<td class="power">{int(r['Sức Mạnh_2']):,}</td>

<td class="death">{int(r['Điểm Chết_2']):,}<br>
<span class="down">▼ {int(r['DI']):,}</span></td>

<td style="color:#22d3ee;font-weight:bold">{r['KPI']}%</td>

</tr>
"""

st.markdown(f"""
<div class="table-wrap">
<table>
<thead>
<tr>
<th>#</th>
<th>Player</th>
<th>ID</th>
<th>Alliance</th>
<th>Kill</th>
<th>Power</th>
<th>Death</th>
<th>KPI</th>
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>
""", unsafe_allow_html=True)

# ===== PROFILE (CHỌN 1 PLAYER) =====
st.markdown("### 🎯 PLAYER PROFILE")

player = st.selectbox("Chọn Player", df['Tên_2'])

p = df[df['Tên_2']==player].iloc[0]

kpi = p['KPI']

components.html(f"""
<div style="padding:20px;color:white;text-align:center">

<img src="https://api.dicebear.com/7.x/bottts/svg?seed={p['Tên_2']}" 
style="width:90px;border-radius:50%;border:3px solid #22d3ee;box-shadow:0 0 15px #22d3ee;">

<h2 style="text-shadow:0 0 10px #22d3ee">{p['Tên_2']}</h2>

<div style="border:1px solid #22d3ee;padding:6px 12px;border-radius:10px;display:inline-block;">
🏆 Rank #{int(p['Rank'])}
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:20px">

<div>⚔ Kill<br>{int(p['Tổng Tiêu Diệt_2']):,}<br><span style="color:#22c55e">▲ {int(p['KI']):,}</span></div>

<div>⚡ Power<br>{int(p['Sức Mạnh_2']):,}</div>

<div>💀 Death<br>{int(p['Điểm Chết_2']):,}<br><span style="color:#ef4444">▼ {int(p['DI']):,}</span></div>

<div>🏰 {p['Liên Minh_2']}</div>

</div>

<div style="margin-top:20px">
<div style="
width:140px;height:140px;border-radius:50%;
margin:auto;
display:flex;align-items:center;justify-content:center;
font-size:22px;font-weight:bold;
background:conic-gradient(#22d3ee {kpi}%, #1e293b 0);
box-shadow:0 0 25px #22d3ee;
">
{kpi}%
</div>
<div>KPI</div>
</div>

</div>
""", height=500)
