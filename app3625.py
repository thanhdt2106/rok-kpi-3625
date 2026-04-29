import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import re

st.set_page_config(page_title="FTD KPI SYSTEM", layout="wide", initial_sidebar_state="collapsed")

# CSS ẩn thành phần Streamlit
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid = "855089129"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

# --- XỬ LÝ LOGIC GỘP TÀI KHOẢN ---
df_raw = load_data()

def to_int(x):
    try: return int(str(x).replace(",", ""))
    except: return 0

df_raw["Power"] = df_raw["Sức Mạnh"].apply(to_int)
df_raw["Kill"] = df_raw["Tổng Tiêu Diệt"].apply(to_int)
df_raw["Dead"] = df_raw["Điểm Chết"].apply(to_int)

def process_data(df):
    # Hàm lấy "gốc tên" - Ví dụ "Louis 1" -> "louis"
    def get_root(name):
        match = re.search(r'^[a-zA-Z]+', str(name).strip())
        return match.group(0).lower() if match else str(name).lower()

    df['root_name'] = df['Tên'].apply(get_root)
    processed_data = []

    for _, group in df.groupby('root_name'):
        if len(group) > 1:
            # Lấy thằng to nhất làm chính
            main = group.loc[group['Power'].idxmax()].copy()
            # Gộp Dead (Điểm chết) từ các acc farm vào acc chính
            main['Dead'] = group['Dead'].sum()
            processed_data.append(main)
        else:
            processed_data.append(group.iloc[0])
    return pd.DataFrame(processed_data)

df = process_data(df_raw)

# --- KPI RULES ---
def kpi_kill(pow):
    if pow >= 100_000_000: return 600_000_000
    elif pow >= 90_000_000: return 550_000_000
    elif pow >= 80_000_000: return 450_000_000
    elif pow >= 70_000_000: return 300_000_000
    elif pow >= 60_000_000: return 250_000_000
    else: return 200_000_000

def kpi_dead(pow):
    if pow >= 100_000_000: return 1_500_000
    elif pow >= 90_000_000: return 1_200_000
    elif pow >= 80_000_000: return 1_000_000
    elif pow >= 70_000_000: return 800_000
    else: return 700_000

cards_html = ""
for _, row in df.iterrows():
    name, id_, all_ = str(row["Tên"]), str(row["ID"]), str(row["Liên Minh"])
    pow, kill, dead = row["Power"], row["Kill"], row["Dead"]
    kK, kD = kpi_kill(pow), kpi_dead(pow)
    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={name}"

    cards_html += f"""
    <div class="card" data-power="{pow}" data-kill="{kill}" data-dead="{dead}"
        onclick="openProfile('{name}','{id_}','{all_}','{pow}','{kill}','{dead}','{kK}','{kD}','{avatar}')">
        <div class="avatar-wrap"><img src="{avatar}"></div>
        <h3>{name}</h3>
        <p class="value">{pow:,}</p>
    </div>
    """

# --- GIAO DIỆN HTML ---
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ background: radial-gradient(circle at top, #111, #05070d); color: white; font-family: sans-serif; padding: 20px; }}
        #langBtn {{ position: fixed; top: 20px; right: 20px; background: gold; padding: 8px 15px; border-radius: 8px; cursor: pointer; color: black; font-weight: bold; z-index: 2000; }}
        
        .avatar-wrap {{
            width: 80px; height: 80px; margin: auto; border-radius: 50%; padding: 3px;
            background: linear-gradient(45deg, gold, orange);
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{ 0% {{transform: scale(1); shadow: 0 0 10px;}} 50% {{transform: scale(1.05); shadow: 0 0 25px;}} 100% {{transform: scale(1); shadow: 0 0 10px;}} }}
        .avatar-wrap img {{ width: 100%; border-radius: 50%; background: #222; }}

        .search {{ width: 100%; padding: 12px; background: #111; border: 1px solid #333; color: white; border-radius: 10px; margin-bottom: 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; }}
        .card {{ background: #161b22; padding: 15px; border-radius: 15px; text-align: center; border: 1px solid #333; cursor: pointer; transition: 0.3s; }}
        .card:hover {{ border-color: gold; transform: translateY(-5px); }}

        .modal {{ position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.9); display: none; justify-content: center; align-items: center; z-index: 3000; }}
        
        /* KHUNG PROFILE ĐÃ NHỎ LẠI */
        .profile-box {{ 
            width: 85%; max-width: 380px; background: #1b1f2e; padding: 20px; border-radius: 20px; border: 1px solid gold; 
        }}
        
        .bar {{ height: 10px; background: #333; border-radius: 5px; margin: 8px 0; overflow: hidden; }}
        .fill {{ height: 100%; background: gold; width: 0%; }}
        .stat-row {{ display: flex; gap: 8px; margin: 15px 0; }}
        .stat-card {{ flex: 1; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; text-align: center; font-size: 13px; }}
        .close-btn {{ width: 100%; padding: 10px; background: #ff4b4b; border: none; color: white; border-radius: 8px; cursor: pointer; margin-top: 15px; }}
    </style>
</head>
<body>
    <div id="langBtn">EN</div>
    <input class="search" id="searchInput" placeholder="🔍 Tìm kiếm..." onkeyup="search(this.value)">
    <div class="grid" id="grid">{cards_html}</div>
    <div class="modal" id="modal"><div class="profile-box" id="profileContent"></div></div>

    <script>
        let lang = "vn";
        function search(v){{
            v = v.toLowerCase();
            document.querySelectorAll('.card').forEach(c => c.style.display = c.innerText.toLowerCase().includes(v) ? 'block' : 'none');
        }}

        function openProfile(name, id, all, pow, kill, dead, kpiK, kpiD, avatar) {{
            document.getElementById('modal').style.display = 'flex';
            document.getElementById('profileContent').innerHTML = `
                <center>
                    <div class="avatar-wrap" style="width:70px; height:70px;"><img src="${{avatar}}"></div>
                    <h3 style="margin:10px 0 0 0;">${{name}}</h3>
                    <small style="color:gray;">ID: ${{id}} | ${{all}}</small>
                </center>
                <div class="stat-row">
                    <div class="stat-card">⚡ Power<br><b>${{Number(pow).toLocaleString()}}</b></div>
                    <div class="stat-card">🔥 Kills<br><b>${{Number(kill).toLocaleString()}}</b></div>
                    <div class="stat-card">💀 Dead<br><b>${{Number(dead).toLocaleString()}}</b></div>
                </div>
                <div style="font-size: 13px;">
                    <span>🔥 KPI Kill: 0 / ${{Number(kpiK).toLocaleString()}}</span>
                    <div class="bar"><div class="fill"></div></div>
                    <span>💀 KPI Dead: 0 / ${{Number(kpiD).toLocaleString()}}</span>
                    <div class="bar"><div class="fill"></div></div>
                </div>
                <button class="close-btn" onclick="document.getElementById('modal').style.display='none'">ĐÓNG</button>
            `;
        }}
    </script>
</body>
</html>
"""
components.html(html_content, height=900, scrolling=True)
