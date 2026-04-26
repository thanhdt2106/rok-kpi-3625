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

.title{
font-size:28px;
font-weight:bold;
color:#22d3ee;
text-shadow:0 0 12px #22d3ee;
padding:20px;
}

.table-wrapper{
margin:20px;
border:1px solid rgba(34,211,238,.3);
border-radius:16px;
overflow:hidden;
box-shadow:0 0 20px rgba(34,211,238,.2);
}

table{
width:100%;
border-collapse:collapse;
}

th{
background:#020617;
color:#22d3ee;
padding:10px;
}

td{
padding:10px;
text-align:center;
}

tr:hover{
background:rgba(34,211,238,.08);
cursor:pointer;
}

.rank{
color:#facc15;
font-weight:bold;
}

.kpi{
color:#22d3ee;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ===== DATA =====
SHEET_ID = '1MJQSE3siwFWmQNdJmbbJ6RsilvcoxWTu-r6h-UdHugE'
URL_T = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=731741617'
URL_S = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=371969335'

@st.cache_data(ttl=30)
def load_data():
    dt = pd.read_csv(URL_T)
    ds = pd.read_csv(URL_S)

    for d in [dt, ds]:
        d['ID'] = d['ID'].astype(str).str.replace(r'\.0$', '', regex=True)

    df = pd.merge(dt, ds, on='ID', suffixes=('_1', '_2'))

    # FIX NUMBER
    cols = [
        'Tổng Tiêu Diệt_1','Tổng Tiêu Diệt_2',
        'Điểm Chết_1','Điểm Chết_2',
        'Sức Mạnh_2'
    ]

    for c in cols:
        df[c] = pd.to_numeric(
            df[c].astype(str).str.replace(r'[^\d.]','', regex=True),
            errors='coerce'
        ).fillna(0)

    df['KI'] = df['Tổng Tiêu Diệt_2'] - df['Tổng Tiêu Diệt_1']
    df['DI'] = df['Điểm Chết_2'] - df['Điểm Chết_1']

    df = df.sort_values(by='KI', ascending=False)
    df['Rank'] = range(1, len(df)+1)

    return df

df = load_data()

# ===== HEADER =====
st.markdown('<div class="title">🏆 BẢNG XẾP HẠNG TỔNG HỢP</div>', unsafe_allow_html=True)

# ===== TABLE HTML =====
rows = ""
for _, r in df.iterrows():
    kpi = min(100, round((r['KI']/300_000_000)*100,1))
    rows += f"""
    <tr onclick="showProfile('{r['Tên_2']}','{r['ID']}','{r['Liên Minh_2']}',{int(r['KI'])},{int(r['DI'])},{int(r['Sức Mạnh_2'])},{kpi},{int(r['Rank'])})">
        <td class="rank">#{int(r['Rank'])}</td>
        <td>{r['Tên_2']}</td>
        <td>{r['ID']}</td>
        <td>{r['Liên Minh_2']}</td>
        <td style="color:#22d3ee;">+{int(r['KI']):,}</td>
        <td style="color:#ef4444;">+{int(r['DI']):,}</td>
        <td>{int(r['Sức Mạnh_2']):,}</td>
        <td class="kpi">{kpi}%</td>
    </tr>
    """

html = f"""
<div class="table-wrapper">
<table>
<thead>
<tr>
<th>#</th>
<th>Name</th>
<th>ID</th>
<th>Alliance</th>
<th>Kill+</th>
<th>Dead+</th>
<th>Power</th>
<th>KPI</th>
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>

<div id="profile" style="display:none; position:fixed; right:0; top:0; width:35%; height:100%; background:#020617; padding:20px; box-shadow:-10px 0 20px rgba(0,0,0,.5);"></div>

<script>
function showProfile(name,id,alliance,kill,dead,power,kpi,rank){

document.getElementById("profile").style.display="block";

document.getElementById("profile").innerHTML = `
<h2 style="color:#22d3ee; text-shadow:0 0 10px #22d3ee;">${name}</h2>
<div>ID: ${id}</div>
<div>Alliance: ${alliance}</div>

<div style="margin-top:20px;padding:10px;border:1px solid #22d3ee;border-radius:10px;">
🏆 Rank #${rank}
</div>

<div style="margin-top:20px;">
⚔ Kill: ${kill.toLocaleString()}<br>
💀 Dead: ${dead.toLocaleString()}<br>
⚡ Power: ${power.toLocaleString()}
</div>

<div style="margin-top:30px;text-align:center;">
<div style="
width:150px;height:150px;
border-radius:50%;
background:conic-gradient(#22d3ee ${kpi}%, #1e293b 0);
display:flex;
align-items:center;
justify-content:center;
margin:auto;
font-size:22px;
box-shadow:0 0 20px #22d3ee;
">
${kpi}%
</div>
<div style="margin-top:10px;">KPI</div>
</div>

<div style="margin-top:20px;text-align:center;">
<button onclick="document.getElementById('profile').style.display='none'">Close</button>
</div>
`;
}
</script>
"""

components.html(html, height=900, scrolling=False)
