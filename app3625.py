import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ===== 1. CẤU HÌNH FULL MÀN HÌNH =====
st.set_page_config(page_title="FTD KPI SYSTEM", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ===== 2. LOAD VÀ XỬ LÝ DỮ LIỆU (GỘP FARM) =====
@st.cache_data(ttl=60)
def load_and_process_data():
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid = "855089129"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()

    def to_int(x):
        try: return int(str(x).replace(",", ""))
        except: return 0

    # Chuyển đổi dữ liệu số
    df["Power"] = df["Sức Mạnh"].apply(to_int)
    df["Kill"] = df["Tổng Tiêu Diệt"].apply(to_int)
    df["Dead"] = df["Điểm Chết"].apply(to_int)
    
    # Tạo cột "Gốc tên" để nhận diện gia đình (Ví dụ: "Louis 1" -> "LOUIS")
    df['Group'] = df['Tên'].apply(lambda x: str(x).split()[0].upper() if pd.notnull(x) else "")

    # Tính tổng Dead của cả nhóm farm
    group_dead_totals = df.groupby('Group')['Dead'].transform('sum')
    # Tìm Power lớn nhất trong nhóm để xác định Acc chính
    group_max_power = df.groupby('Group')['Power'].transform('max')

    processed_list = []
    for i, row in df.iterrows():
        # Tài khoản chính là tài khoản có Power bằng Power lớn nhất trong Group
        is_main = (row['Power'] == group_max_power[i])
        
        # Nếu là acc chính, lấy tổng Dead của cả nhóm farm. Nếu là acc farm, giữ nguyên hoặc ẩn.
        final_dead = group_dead_totals[i] if is_main else row['Dead']
        
        processed_list.append({
            "name": row["Tên"],
            "id": row["ID"],
            "alliance": row["Liên Minh"],
            "pow": row["Power"],
            "kill": row["Kill"],
            "dead": final_dead,
            "is_farm": not is_main
        })
    return processed_list

try:
    final_data = load_and_process_data()
except Exception as e:
    st.error(f"Lỗi tải dữ liệu: {e}")
    st.stop()

# ===== 3. KPI RULES =====
def kpi_kill(p):
    if p >= 100_000_000: return 600_000_000
    elif p >= 80_000_000: return 450_000_000
    return 300_000_000

def kpi_dead(p):
    if p >= 100_000_000: return 1_500_000
    elif p >= 80_000_000: return 1_000_000
    return 800_000

# ===== 4. BUILD HTML CARDS =====
cards_html = ""
for item in final_data:
    # Nếu muốn ẩn hoàn toàn các acc farm khỏi danh sách hiển thị, bỏ comment dòng dưới:
    # if item['is_farm']: continue

    kK = kpi_kill(item['pow'])
    kD = kpi_dead(item['pow'])
    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={item['name']}"

    cards_html += f"""
    <div class="card" data-power="{item['pow']}" data-kill="{item['kill']}" data-dead="{item['dead']}"
        onclick="openProfile('{item['name']}','{item['id']}','{item['alliance']}','{item['pow']}','{item['kill']}','{item['dead']}','{kK}','{kD}','{avatar}')">
        <div class="avatar-wrap"><img src="{avatar}"></div>
        <div class="card-name">{item['name']}</div>
        <div class="value">{item['pow']:,}</div>
    </div>
    """

# ===== 5. GIAO DIỆN HTML/CSS/JS =====
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ background: #05070d; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; }}
        
        #langBtn {{ 
            position: fixed; top: 15px; right: 15px; background: gold; color: black; 
            padding: 6px 12px; border-radius: 8px; cursor: pointer; font-weight: bold; z-index: 2000; 
        }}

        .avatar-wrap {{
            width: 75px; height: 75px; margin: 0 auto 10px; border-radius: 50%; padding: 3px;
            background: linear-gradient(45deg, #ffd700, #ff8c00);
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
            animation: pulse-gold 2s infinite;
        }}
        @keyframes pulse-gold {{
            0% {{ box-shadow: 0 0 10px rgba(255, 215, 0, 0.4); transform: scale(1); }}
            50% {{ box-shadow: 0 0 25px rgba(255, 215, 0, 0.8); transform: scale(1.03); }}
            100% {{ box-shadow: 0 0 10px rgba(255, 215, 0, 0.4); transform: scale(1); }}
        }}
        .avatar-wrap img {{ width: 100%; height: 100%; border-radius: 50%; background: #111; }}

        .search {{ width: 100%; padding: 12px; background: #111; border: 1px solid #333; color: white; border-radius: 12px; margin-bottom: 15px; box-sizing: border-box; }}
        
        .filters {{ display: flex; gap: 8px; margin-bottom: 15px; }}
        .filter {{ flex: 1; padding: 10px; background: #222; border-radius: 8px; text-align: center; font-size: 12px; cursor: pointer; border: 1px solid #333; }}
        .filter.active {{ background: gold; color: black; font-weight: bold; }}

        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; }}
        .card {{ background: #161b22; padding: 15px; border-radius: 18px; text-align: center; border: 1px solid #222; cursor: pointer; transition: 0.3s; }}
        .card:hover {{ border-color: gold; transform: translateY(-5px); }}
        .card-name {{ font-weight: bold; font-size: 14px; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .value {{ color: gold; font-family: monospace; font-size: 13px; }}

        /* Profile Thu Nhỏ */
        .modal {{ position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.9); display: none; justify-content: center; align-items: center; z-index: 3000; }}
        .profile-box {{ width: 85%; max-width: 360px; background: #1b1f2e; padding: 25px; border-radius: 25px; border: 1px solid gold; box-shadow: 0 0 30px rgba(0,0,0,0.5); }}
        
        .stat-row {{ display: flex; gap: 8px; margin: 20px 0; }}
        .stat-card {{ flex: 1; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 12px; text-align: center; font-size: 11px; }}
        .stat-card b {{ font-size: 13px; color: gold; }}

        .bar {{ height: 10px; background: #333; border-radius: 5px; margin: 8px 0; overflow: hidden; }}
        .fill {{ height: 100%; background: linear-gradient(90deg, gold, orange); width: 0%; transition: 1.5s; }}
        
        .close-btn {{ width: 100%; padding: 12px; background: #ff4b4b; color: white; border: none; border-radius: 10px; cursor: pointer; margin-top: 20px; font-weight: bold; }}
    </style>
</head>
<body>

    <div id="langBtn">EN</div>
    <input class="search" id="searchInput" placeholder="🔍 Nhập tên chiến binh..." onkeyup="search(this.value)">

    <div class="filters">
        <div class="filter active" id="fPow" onclick="setMode('power', this)">⚡ SỨC MẠNH</div>
        <div class="filter" id="fKill" onclick="setMode('kill', this)">🔥 TIÊU DIỆT</div>
        <div class="filter" id="fDead" onclick="setMode('dead', this)">💀 ĐIỂM CHẾT</div>
    </div>

    <div class="grid" id="grid">{cards_html}</div>

    <div class="modal" id="modal"><div class="profile-box" id="profileContent"></div></div>

<script>
    let lang = "vn";
    const TEXT = {{
        vn: {{ search: "🔍 Nhập tên chiến binh...", pow: "⚡ SỨC MẠNH", kill: "🔥 TIÊU DIỆT", dead: "💀 ĐIỂM CHẾT", exit: "QUAY LẠI" }},
        en: {{ search: "🔍 Search warrior...", pow: "⚡ POWER", kill: "🔥 KILL", dead: "💀 DEAD", exit: "CLOSE" }}
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
        document.querySelectorAll('.card').forEach(c => {{
            c.style.display = c.innerText.toLowerCase().includes(v) ? 'block' : 'none';
        }});
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

    function openProfile(name, id, all, pow, kill, dead, kK, kD, avatar) {{
        document.getElementById('modal').style.display = 'flex';
        document.getElementById('profileContent').innerHTML = `
            <center>
                <div class="avatar-wrap" style="width:70px; height:70px;"><img src="${{avatar}}"></div>
                <h3 style="margin:10px 0 5px 0;">${{name}}</h3>
                <small style="color:#888;">ID: ${{id}} | ${{all}}</small>
            </center>

            <div class="stat-row">
                <div class="stat-card">POWER<br><b>${{Number(pow).toLocaleString()}}</b></div>
                <div class="stat-card">KILL<br><b>${{Number(kill).toLocaleString()}}</b></div>
                <div class="stat-card">DEAD<br><b>${{Number(dead).toLocaleString()}}</b></div>
            </div>

            <div style="font-size: 13px;">
                <p style="margin:5px 0;">🔥 KPI Tiêu diệt: 0 / ${{Number(kK).toLocaleString()}}</p>
                <div class="bar"><div class="fill"></div></div>
                <p style="margin:5px 0;">💀 KPI Điểm chết: 0 / ${{Number(kD).toLocaleString()}}</p>
                <div class="bar"><div class="fill"></div></div>
            </div>

            <button class="close-btn" onclick="document.getElementById('modal').style.display='none'">${{TEXT[lang].exit}}</button>
        `;
    }}
</script>
</body>
</html>
"""

components.html(html_content, height=1000, scrolling=True)
