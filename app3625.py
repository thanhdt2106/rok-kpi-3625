import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ===== CẤU HÌNH FULL MÀN HÌNH =====
st.set_page_config(page_title="FTD KPI SYSTEM", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid = "855089129"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

# ===== XỬ LÝ LOGIC GỘP DEAD CHO ACC FARM =====
def process_warriors(df_raw):
    # Làm sạch số
    def to_int(x):
        try: return int(str(x).replace(",", ""))
        except: return 0

    df_raw["Power"] = df_raw["Sức Mạnh"].apply(to_int)
    df_raw["Kill"] = df_raw["Tổng Tiêu Diệt"].apply(to_int)
    df_raw["Dead"] = df_raw["Điểm Chết"].apply(to_int)
    
    # Tạo "Gốc tên" (Lấy từ đầu tiên, ví dụ: "Louis 1" -> "Louis")
    # Nếu tên chỉ có 1 cụm, nó lấy cả tên đó.
    df_raw['root_name'] = df_raw['Tên'].apply(lambda x: str(x).split()[0].lower() if pd.notnull(x) else "")

    final_list = []
    # Gom nhóm theo gốc tên
    for _, group in df_raw.groupby('root_name'):
        if len(group) > 1:
            # Tìm acc chính (Power cao nhất trong nhóm)
            main_idx = group['Power'].idxmax()
            main_acc = group.loc[main_idx].copy()
            # Gộp tổng điểm chết của cả nhóm (chính + farm)
            main_acc['Dead'] = group['Dead'].sum()
            final_list.append(main_acc)
        else:
            final_list.append(group.iloc[0])
            
    return pd.DataFrame(final_list)

# Thực thi xử lý
try:
    df_raw = load_data()
    df = process_warriors(df_raw)
except Exception as e:
    st.error(f"Lỗi dữ liệu: {e}")
    st.stop()

# ===== KPI RULES =====
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

# ===== BUILD CARDS HTML =====
cards_html = ""
for _, row in df.iterrows():
    name, id_, alliance = str(row["Tên"]), str(row["ID"]), str(row["Liên Minh"])
    power, kill, dead = row["Power"], row["Kill"], row["Dead"]
    kK, kD = kpi_kill(power), kpi_dead(power)
    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={name}"

    cards_html += f"""
    <div class="card" data-power="{power}" data-kill="{kill}" data-dead="{dead}"
        onclick="openProfile('{name}','{id_}','{alliance}','{power}','{kill}','{dead}','{kK}','{kD}','{avatar}')">
        <div class="avatar-wrap"><img src="{avatar}"></div>
        <h3>{name}</h3>
        <p class="value">{power:,}</p>
    </div>
    """

# ===== GIAO DIỆN HTML/CSS/JS =====
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ background: radial-gradient(circle at top, #111, #05070d); color: white; font-family: sans-serif; margin: 0; padding: 20px; }}
        
        #langBtn {{ position: fixed; top: 15px; right: 15px; background: gold; color: black; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-weight: bold; z-index: 2000; font-size: 14px; }}

        /* Avatar phát sáng */
        .avatar-wrap {{
            width: 80px; height: 80px; margin: auto; border-radius: 50%; padding: 3px;
            background: linear-gradient(45deg, gold, #ff8c00);
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.7);
            animation: pulse-gold 2s infinite;
        }}
        @keyframes pulse-gold {{
            0% {{ box-shadow: 0 0 8px rgba(255, 215, 0, 0.5); transform: scale(1); }}
            50% {{ box-shadow: 0 0 20px rgba(255, 215, 0, 0.9); transform: scale(1.02); }}
            100% {{ box-shadow: 0 0 8px rgba(255, 215, 0, 0.5); transform: scale(1); }}
        }}
        .avatar-wrap img {{ width: 100%; height: 100%; border-radius: 50%; background: #222; }}

        .search {{ width: 100%; padding: 12px; background: #111; border: 1px solid #333; color: white; border-radius: 10px; margin-bottom: 20px; box-sizing: border-box; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; }}
        .card {{ background: #161b22; padding: 15px; border-radius: 15px; text-align: center; border: 1px solid #333; cursor: pointer; transition: 0.3s; }}
        .card:hover {{ border-color: gold; transform: translateY(-5px); }}

        .filters {{ display: flex; gap: 8px; margin-bottom: 15px; }}
        .filter {{ padding: 8px 12px; background: #222; border-radius: 8px; cursor: pointer; font-size: 13px; border: 1px solid #444; }}
        .filter.active {{ background: gold; color: black; font-weight: bold; }}

        .modal {{ position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.9); display: none; justify-content: center; align-items: center; z-index: 3000; }}
        
        /* Profile nhỏ gọn */
        .profile-box {{ width: 85%; max-width: 380px; background: #1b1f2e; padding: 20px; border-radius: 20px; border: 1px solid gold; }}
        
        .stat-row {{ display: flex; gap: 8px; margin: 15px 0; }}
        .stat-card {{ flex: 1; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; text-align: center; font-size: 12px; }}
        .bar {{ height: 10px; background: #333; border-radius: 5px; margin: 8px 0; overflow: hidden; }}
        .fill {{ height: 100%; background: gold; width: 0%; transition: 1s; }}
        .close-btn {{ width: 100%; padding: 10px; background: #ff4b4b; border: none; color: white; border-radius: 8px; cursor: pointer; margin-top: 15px; font-weight: bold; }}
    </style>
</head>
<body>

<div id="langBtn">EN</div>
<input class="search" id="searchInput" placeholder="🔍 Nhập tên..." onkeyup="search(this.value)">

<div class="filters">
    <div class="filter active" id="fPow" onclick="setMode('power', this)">⚡ POWER</div>
    <div class="filter" id="fKill" onclick="setMode('kill', this)">🔥 KILL</div>
    <div class="filter" id="fDead" onclick="setMode('dead', this)">💀 DEAD</div>
</div>

<div class="grid" id="grid">{cards_html}</div>

<div class="modal" id="modal">
    <div class="profile-box" id="profileContent"></div>
</div>

<script>
    let lang = "vn";
    const TEXT = {{
        vn: {{ search: "🔍 Nhập tên...", pow: "⚡ POWER", kill: "🔥 KILL", dead: "💀 DEAD", kpiK: "🔥 KPI Kill", kpiD: "💀 KPI Dead", exit: "ĐÓNG" }},
        en: {{ search: "🔍 Search name...", pow: "⚡ POWER", kill: "🔥 KILL", dead: "💀 DEAD", kpiK: "🔥 Kill KPI", kpiD: "💀 Dead KPI", exit: "CLOSE" }}
    }};

    document.getElementById("langBtn").onclick = function() {{
        lang = lang === "vn" ? "en" : "vn";
        this.innerText = lang.toUpperCase();
        document.getElementById("searchInput").placeholder = TEXT[lang].search;
        document.getElementById("fPow").innerText = TEXT[lang].pow;
        document.getElementById("fKill").innerText = TEXT[lang].kill;
        document.getElementById("fDead").innerText = TEXT[lang].dead;
    }};

    function search(v) {{
        v = v.toLowerCase();
        document.querySelectorAll('.card').forEach(c => c.style.display = c.innerText.toLowerCase().includes(v) ? 'block' : 'none');
    }}

    function setMode(m, el) {{
        document.querySelectorAll('.filter').forEach(f => f.classList.remove('active'));
        el.classList.add('active');
        let grid = document.getElementById('grid');
        let cards = Array.from(grid.getElementsByClassName('card'));
        cards.sort((a,b) => Number(b.dataset[m]) - Number(a.dataset[m]));
        grid.innerHTML = "";
        cards.forEach(c => {{
            c.querySelector('.value').innerText = Number(c.dataset[m]).toLocaleString();
            grid.appendChild(c);
        }});
    }}

    function openProfile(name, id, all, pow, kill, dead, kpiK, kpiD, avatar) {{
        let t = TEXT[lang];
        document.getElementById('modal').style.display = 'flex';
        document.getElementById('profileContent').innerHTML = `
            <center>
                <div class="avatar-wrap" style="width:70px; height:70px;"><img src="${{avatar}}"></div>
                <h3 style="margin:10px 0 5px 0;">${{name}}</h3>
                <small style="color:gray;">ID: ${{id}} | ${{all}}</small>
            </center>
            <div class="stat-row">
                <div class="stat-card">⚡ Power<br><b>${{Number(pow).toLocaleString()}}</b></div>
                <div class="stat-card">🔥 Kills<br><b>${{Number(kill).toLocaleString()}}</b></div>
                <div class="stat-card">💀 Dead<br><b>${{Number(dead).toLocaleString()}}</b></div>
            </div>
            <div style="font-size: 13px;">
                <span>${{t.kpiK}}: <b>0</b> / ${{Number(kpiK).toLocaleString()}}</span>
                <div class="bar"><div class="fill" style="width:0%"></div></div>
                <span>${{t.kpiD}}: <b>0</b> / ${{Number(kpiD).toLocaleString()}}</span>
                <div class="bar"><div class="fill" style="width:0%"></div></div>
            </div>
            <button class="close-btn" onclick="document.getElementById('modal').style.display='none'">${{t.exit}}</button>
        `;
    }}
</script>
</body>
</html>
"""

components.html(html_content, height=1000, scrolling=True)
