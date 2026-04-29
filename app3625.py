import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. Cấu hình trang cơ bản
st.set_page_config(page_title="FTD KPI SYSTEM", layout="wide", initial_sidebar_state="collapsed")

# 2. Xóa bỏ Sidebar hoàn toàn và mở rộng full màn hình bằng CSS
st.markdown("""
    <style>
        /* Ẩn sidebar hoàn toàn */
        [data-testid="stSidebar"], .st-emotion-cache-16ids9v {
            display: none;
        }
        /* Xóa padding và mở rộng nội dung chính */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        /* Ẩn menu và footer của Streamlit để giống web thật hơn */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
@st.cache_data(ttl=60)
def load_data():
    # Giữ nguyên logic load data của bạn
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid = "855089129"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        # Fallback data nếu link lỗi để bạn test giao diện
        return pd.DataFrame(columns=["Tên", "ID", "Liên Minh", "Sức Mạnh", "Tổng Tiêu Diệt", "Điểm Chết"])

df = load_data()

# ===== CLEAN (Giữ nguyên logic cũ) =====
def to_int(x):
    try: return int(str(x).replace(",", ""))
    except: return 0

df["Power"] = df["Sức Mạnh"].apply(to_int)
df["Kill"] = df["Tổng Tiêu Diệt"].apply(to_int)
df["Dead"] = df["Điểm Chết"].apply(to_int)

# ===== KPI (Giữ nguyên logic cũ) =====
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

# ===== BUILD CARD HTML =====
cards_html = ""
for _, row in df.iterrows():
    name = str(row["Tên"])
    id_ = str(row["ID"])
    alliance = str(row["Liên Minh"])
    power, kill, dead = row["Power"], row["Kill"], row["Dead"]
    kpiK, kpiD = kpi_kill(power), kpi_dead(power)
    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={name}"

    cards_html += f"""
    <div class="card" data-power="{power}" data-kill="{kill}" data-dead="{dead}" 
         onclick="openProfile('{name}','{id_}','{alliance}','{power}','{kill}','{dead}','{kpiK}','{kpiD}','{avatar}')">
        <div class="avatar-wrap"><img src="{avatar}"></div>
        <h3>{name}</h3>
        <p class="value">{power:,}</p>
    </div>
    """

# ===== HTML & CSS CHÍNH =====
html_code = f"""
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body {{
        background: radial-gradient(circle at top, #111, #05070d);
        color:white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin:0;
        padding: 20px; /* Thêm chút padding để nội dung không dính sát mép trình duyệt */
    }}
    .search {{
        width:100%; padding:15px; font-size:16px; border-radius:12px; border:1px solid #333;
        margin-bottom:20px; background:#111; color:white; box-sizing: border-box;
    }}
    .grid {{
        display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:20px;
    }}
    .card {{
        background:linear-gradient(145deg,#0f111a,#1b1f2e); padding:20px; border-radius:20px;
        text-align:center; cursor:pointer; transition:0.3s; border:1px solid #222;
    }}
    .card:hover {{ transform:translateY(-8px); box-shadow:0 0 20px rgba(255,215,0,0.3); border-color: gold; }}
    .avatar-wrap {{ width:80px; height:80px; margin:auto; border-radius:50%; padding:3px; background:linear-gradient(45deg,gold,orange); }}
    .avatar-wrap img {{ width:100%; height:100%; border-radius:50%; }}
    
    /* Modal Styles */
    .modal {{ position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.9); display:none; justify-content:center; align-items:center; z-index:9999; }}
    .profile {{ width:90%; max-width:600px; background:#1b1f2e; border-radius:25px; padding:30px; border:1px solid #444; }}
    .row {{ display:flex; gap:10px; margin-top:20px; }}
    .box {{ flex:1; background:rgba(255,255,255,0.05); padding:10px; border-radius:12px; text-align:center; }}
    .bar {{ height:10px; background:#222; border-radius:10px; margin: 10px 0; overflow:hidden; }}
    .fill {{ height:100%; background:linear-gradient(90deg,gold,orange); transition: 0.5s; }}
    .filters {{ display:flex; gap:10px; margin-bottom:20px; }}
    .filter {{ padding:10px 20px; background:#111; border-radius:10px; cursor:pointer; border: 1px solid #333; }}
    .filter.active {{ background:gold; color:black; font-weight:bold; }}
    #langBtn {{ position:fixed; top:20px; right:20px; background:gold; color:black; padding:8px 15px; border-radius:8px; cursor:pointer; font-weight:bold; }}
    button.exit-btn {{ background: #ff4b4b; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; margin-top: 20px; width: 100%; }}
</style>
</head>
<body>
    <div id="langBtn">EN</div>
    <input class="search" id="searchInput" placeholder="🔍 Nhập tên..." onkeyup="search(this.value)">
    
    <div class="filters">
        <div class="filter active" onclick="setMode('power', this)">⚡ POWER</div>
        <div class="filter" onclick="setMode('kill', this)">🔥 KILL</div>
        <div class="filter" onclick="setMode('dead', this)">💀 DEAD</div>
    </div>

    <div class="grid" id="grid">{cards_html}</div>

    <div class="modal" id="modal">
        <div class="profile" id="profile"></div>
    </div>

<script>
    let mode = "power";
    let lang = "vn";

    const TEXT = {{
        vn: {{ search: "🔍 Nhập tên...", id: "🆔 ID", alliance: "🏰 Alliance", exit: "ĐÓNG" }},
        en: {{ search: "🔍 Search name...", id: "🆔 ID", alliance: "🏰 Alliance", exit: "CLOSE" }}
    }};

    document.getElementById("langBtn").onclick = function() {{
        lang = lang === "vn" ? "en" : "vn";
        this.innerText = lang.toUpperCase();
        document.getElementById("searchInput").placeholder = TEXT[lang].search;
    }};

    function setMode(m, el) {{
        mode = m;
        document.querySelectorAll(".filter").forEach(f=>f.classList.remove("active"));
        el.classList.add("active");

        let grid = document.getElementById("grid");
        let cards = Array.from(grid.getElementsByClassName("card"));
        
        cards.sort((a,b)=> Number(b.dataset[mode]) - Number(a.dataset[mode]));
        grid.innerHTML = "";
        cards.forEach(c=> {{
            c.querySelector(".value").innerText = Number(c.dataset[mode]).toLocaleString();
            grid.appendChild(c);
        }});
    }}

    function search(val) {{
        val = val.toLowerCase();
        document.querySelectorAll(".card").forEach(c=> {{
            c.style.display = c.innerText.toLowerCase().includes(val) ? "block" : "none";
        }});
    }}

    function openProfile(name,id,alliance,power,kill,dead,kpiK,kpiD,avatar) {{
        let t = TEXT[lang];
        let pctK = Math.min((kill/kpiK)*100, 100);
        let pctD = Math.min((dead/kpiD)*100, 100);

        document.getElementById("modal").style.display="flex";
        document.getElementById("profile").innerHTML = `
            <div style="display:flex; gap:20px; align-items:center;">
                <img src="${{avatar}}" style="width:80px; border-radius:50%; border:3px solid gold;">
                <div>
                    <h2 style="margin:0">${{name}}</h2>
                    <p style="margin:5px 0; opacity:0.8;">${{t.id}}: ${{id}} | ${{t.alliance}}: ${{alliance}}</p>
                </div>
            </div>
            <div class="row">
                <div class="box">⚡ Power<br>${{Number(power).toLocaleString()}}</div>
                <div class="box">🔥 Kill<br>${{Number(kill).toLocaleString()}}</div>
                <div class="box">💀 Dead<br>${{Number(dead).toLocaleString()}}</div>
            </div>
            <h4 style="margin:20px 0 5px 0;">🔥 KPI Kill (${{pctK.toFixed(1)}}%)</h4>
            <div class="bar"><div class="fill" style="width:${{pctK}}%"></div></div>
            <small>${{Number(kill).toLocaleString()}} / ${{Number(kpiK).toLocaleString()}}</small>

            <h4 style="margin:20px 0 5px 0;">💀 KPI Dead (${{pctD.toFixed(1)}}%)</h4>
            <div class="bar"><div class="fill" style="width:${{pctD}}%"></div></div>
            <small>${{Number(dead).toLocaleString()}} / ${{Number(kpiD).toLocaleString()}}</small>
            
            <button class="exit-btn" onclick="closeProfile()">${{t.exit}}</button>
        `;
    }}

    function closeProfile() {{ document.getElementById("modal").style.display="none"; }}
</script>
</body>
</html>
"""

# 3. Hiển thị với chiều rộng tối đa (use_container_width không áp dụng cho components.html nên dùng CSS trên)
components.html(html_code, height=1000, scrolling=True)
