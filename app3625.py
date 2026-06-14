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

# ===== 2. KPI RULES =====
def get_kpi_kill_value(p):
    if p >= 100_000_000: return 600_000_000
    elif p >= 80_000_000: return 450_000_000
    return 300_000_000

def get_kpi_dead_value(p):
    if p >= 100_000_000: return 1_500_000
    elif p >= 90_000_000: return 1_200_000
    elif p >= 80_000_000: return 1_000_000
    elif p >= 70_000_000: return 800_000
    elif p >= 60_000_000: return 700_000
    elif p >= 50_000_000: return 600_000
    elif p >= 40_000_000: return 500_000
    elif p >= 30_000_000: return 400_000
    else: return 300_000

# ===== 3. LOAD VÀ XỬ LÝ DỮ LIỆU =====
@st.cache_data(ttl=60)
def load_and_process_data():
    sheet_id = "1CzGPseLzdRK1V-6qy7KD5T58sBRSGjQi"
    gid1 = "855089129"
    gid2 = "316243863"
    
    url1 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid1}"
    url2 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid2}"
    
    df1 = pd.read_csv(url1)
    df2 = pd.read_csv(url2)
    
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    def to_int(x):
        try: return int(str(x).replace(",", ""))
        except: return 0

    def find_col(df, keywords):
        for col in df.columns:
            if all(k.lower() in col.lower() for k in keywords):
                return col
        return None

    col_pow = find_col(df2, ["sức", "mạnh"]) or "Sức Mạnh"
    col_kill = find_col(df2, ["tổng", "tiêu", "diệt"]) or find_col(df2, ["kill"]) or "Tổng Tiêu Diệt"
    col_dead = find_col(df2, ["chết"]) or "Điểm Chết"
    
    col_t4 = "T4"
    col_t5 = "T5"

    df1["ID_str"] = df1["ID"].astype(str).str.strip()
    df2["ID_str"] = df2["ID"].astype(str).str.strip()

    name_sheet2 = df2.set_index("ID_str")["Tên"].to_dict()
    pow_sheet2 = df2.set_index("ID_str")[col_pow].to_dict()
    kill_sheet2 = df2.set_index("ID_str")[col_kill].to_dict()
    dead_sheet2 = df2.set_index("ID_str")[col_dead].to_dict()
    
    t4_sheet1 = df1.set_index("ID_str")[col_t4].to_dict() if col_t4 in df1.columns else {}
    t5_sheet1 = df1.set_index("ID_str")[col_t5].to_dict() if col_t5 in df1.columns else {}
    t4_sheet2 = df2.set_index("ID_str")[col_t4].to_dict() if col_t4 in df2.columns else {}
    t5_sheet2 = df2.set_index("ID_str")[col_t5].to_dict() if col_t5 in df2.columns else {}

    col_dead_s1 = find_col(df1, ["chết"]) or "Điểm Chết"
    df1["Power_Goc"] = df1[find_col(df1, ["sức", "mạnh"]) or "Sức Mạnh"].apply(to_int)
    df1['Indiv_KPI_Dead'] = df1['Power_Goc'].apply(get_kpi_dead_value)
    
    df1['Group'] = df1['Tên'].apply(lambda x: str(x).split()[0].upper() if pd.notnull(x) else "")
    
    def calc_indiv_diff_dead(row):
        p_id = row['ID_str']
        d_s1 = to_int(row[col_dead_s1])
        d_s2 = to_int(dead_sheet2.get(p_id, d_s1))
        return d_s2 - d_s1

    df1['Indiv_Diff_Dead'] = df1.apply(calc_indiv_diff_dead, axis=1)

    group_kpi_dead_sum = df1.groupby('Group')['Indiv_KPI_Dead'].transform('sum')
    group_diff_dead_sum = df1.groupby('Group')['Indiv_Diff_Dead'].transform('sum')
    group_max_power = df1.groupby('Group')['Power_Goc'].transform('max')

    processed_list = []
    for i, row in df1.iterrows():
        p_id = row['ID_str']
        is_main = (row['Power_Goc'] == group_max_power[i])
        
        final_target_dead = group_kpi_dead_sum[i] if is_main else row['Indiv_KPI_Dead']
        diff_dead = group_diff_dead_sum[i] if is_main else row['Indiv_Diff_Dead']
        
        current_name = name_sheet2.get(p_id, row["Tên"])
        
        pow_s1 = to_int(row[find_col(df1, ["sức", "mạnh"]) or "Sức Mạnh"])
        dead_s1 = to_int(row[col_dead_s1])
        t4_s1 = to_int(t4_sheet1.get(p_id, 0))
        t5_s1 = to_int(t5_sheet1.get(p_id, 0))
        
        pow_s2 = to_int(pow_sheet2.get(p_id, pow_s1))
        kill_s2 = to_int(kill_sheet2.get(p_id, 0))
        dead_s2 = to_int(dead_sheet2.get(p_id, dead_s1))
        t4_s2 = to_int(t4_sheet2.get(p_id, 0))
        t5_s2 = to_int(t5_sheet2.get(p_id, 0))
        
        diff_t4_score = t4_s2 - t4_s1
        diff_t5_score = t5_s2 - t5_s1
        
        diff_kill_score = diff_t4_score + diff_t5_score
        diff_pow = pow_s2 - pow_s1
        
        final_target_kill = get_kpi_kill_value(row['Power_Goc'])
        
        real_pct_kill = round((diff_kill_score / final_target_kill) * 100, 1) if final_target_kill > 0 else 0.0
        real_pct_dead = round((diff_dead / final_target_dead) * 100, 1) if final_target_dead > 0 else 0.0
        
        real_pct_total = round((real_pct_kill + real_pct_dead) / 2, 1)
        
        bar_fill_kill = min(100, max(0, int(real_pct_kill)))
        bar_fill_dead = min(100, max(0, int(real_pct_dead)))
        bar_fill_total = min(100, max(0, int(real_pct_total)))
        
        processed_list.append({
            "name": current_name,
            "id": str(row["ID"]),
            "alliance": row.get("Liên Minh", "FTD"),
            
            "diff_pow": diff_pow,
            "diff_kill": diff_kill_score, 
            "diff_dead": diff_dead,          
            
            "total_pow": pow_s2,
            "total_kill": kill_s2, 
            "total_dead": dead_s2,           
            
            "diff_t4": diff_t4_score,
            "diff_t5": diff_t5_score,
            
            "real_pct_kill": real_pct_kill,
            "real_pct_dead": real_pct_dead,
            "real_pct_total": real_pct_total,
            
            "bar_fill_kill": bar_fill_kill,
            "bar_fill_dead": bar_fill_dead,
            "bar_fill_total": bar_fill_total,
            
            "final_kpi_dead": final_target_dead,
            "final_kpi_kill": final_target_kill
        })
    return processed_list

try:
    final_data = load_and_process_data()
except Exception as e:
    st.error(f"Lỗi đồng bộ cấu trúc dữ liệu bảng tính: {e}")
    st.stop()

# ===== 4. BUILD HTML CARDS =====
cards_html = ""
for item in final_data:
    avatar = f"https://api.dicebear.com/7.x/adventurer/svg?seed={item['name']}"
    cards_html += f"""
    <div class="card" data-id="{item['id']}" data-power="{item['diff_pow']}" data-kill="{item['diff_kill']}" data-dead="{item['diff_dead']}"
        onclick="openProfile('{item['name']}','{item['id']}','{item['alliance']}',
                             '{item['total_pow']}','{item['total_kill']}','{item['total_dead']}',
                             '{item['diff_kill']}','{item['diff_dead']}',
                             '{item['final_kpi_kill']}','{item['final_kpi_dead']}',
                             '{item['real_pct_kill']}','{item['real_pct_dead']}','{item['real_pct_total']}',
                             '{item['bar_fill_kill']}','{item['bar_fill_dead']}','{item['bar_fill_total']}',
                             '{item['diff_t4']}','{item['diff_t5']}','{avatar}')">
        <div class="avatar-wrap"><img src="{avatar}"></div>
        <div class="card-name">{item['name']}</div>
        <div class="value">⚡ {item['diff_pow']:,}</div>
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
        #langBtn {{ position: fixed; top: 15px; right: 15px; background: gold; color: black; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-weight: bold; z-index: 2000; }}
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
        .filter {{ flex: 1; padding: 10px; background: #222; border-radius: 8px; text-align: center; font-size: 11px; cursor: pointer; border: 1px solid #333; }}
        .filter.active {{ background: gold; color: black; font-weight: bold; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; }}
        .card {{ background: #161b22; padding: 15px; border-radius: 18px; text-align: center; border: 1px solid #222; cursor: pointer; transition: 0.3s; }}
        .card:hover {{ border-color: gold; transform: translateY(-5px); }}
        .card-name {{ font-weight: bold; font-size: 14px; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .value {{ color: gold; font-family: monospace; font-size: 12px; }}
        
        .modal {{ position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.9); display: none; justify-content: center; align-items: center; z-index: 3000; }}
        .profile-box {{ width: 88%; max-width: 380px; background: #1b1f2e; padding: 25px; border-radius: 25px; border: 1px solid gold; position: relative; }}
        .stat-row {{ display: flex; gap: 8px; margin: 20px 0; }}
        .stat-card {{ flex: 1; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 12px; text-align: center; font-size: 10px; position: relative; }}
        .stat-card b {{ font-size: 11px; color: gold; display: block; margin-top: 5px; }}
        
        .info-trigger {{ background: #ffd700; color: #000; border: none; border-radius: 50%; width: 16px; height: 16px; font-size: 10px; font-weight: bold; cursor: pointer; display: inline-block; margin-left: 4px; line-height: 16px; text-align: center; vertical-align: middle; }}
        .info-trigger:hover {{ background: #fff; }}
        
        .t-detail-box {{ display: none; background: #0f111a; border: 1px dashed #ffd700; padding: 10px; margin-top: 8px; border-radius: 8px; font-size: 11px; text-align: left; }}
        .t-detail-box div {{ display: flex; justify-content: space-between; margin: 4px 0; color: #ccc; }}
        .t-detail-box span {{ color: #00ffcc; font-family: monospace; font-weight: bold; }}

        .kpi-section {{ font-size: 12px; margin-top: 15px; }}
        .kpi-label {{ display: flex; justify-content: space-between; margin-bottom: 5px; font-weight: bold; }}
        .pct-tag {{ color: #00ffcc; font-family: monospace; background: rgba(0,255,204,0.1); padding: 1px 6px; border-radius: 4px; margin-left: 5px; }}
        .bar {{ height: 10px; background: #333; border-radius: 5px; margin-bottom: 12px; overflow: hidden; }}
        .fill {{ height: 100%; background: linear-gradient(90deg, #ffd700, #ff8c00); width: 0%; transition: width 0.4s ease-in-out; }}
        .fill-total {{ background: linear-gradient(90deg, #00ffcc, #0099ff) !important; }}
        
        .alert-box {{ background: rgba(255,255,255,0.04); border-left: 4px solid gold; padding: 12px; border-radius: 6px; margin-top: 15px; font-size: 12px; line-height: 1.4; text-align: left; }}
        .close-btn {{ width: 100%; padding: 12px; background: #ff4b4b; color: white; border: none; border-radius: 10px; cursor: pointer; margin-top: 15px; font-weight: bold; }}
    </style>
</head>
<body>
    <div id="langBtn">EN</div>
    <input class="search" id="searchInput" placeholder="🔍 Nhập tên hoặc ID..." onkeyup="search(this.value)">
    <div class="filters">
        <div class="filter active" id="fPow" onclick="setMode('power', this)">⚡ SỨC MẠNH BIẾN ĐỘNG</div>
        <div class="filter" id="fKill" onclick="setMode('kill', this)">🔥 TIÊU DIỆT BIẾN ĐỘNG</div>
        <div class="filter" id="fDead" onclick="setMode('dead', this)">💀 ĐIỂM CHẾT BIẾN ĐỘNG</div>
    </div>
    <div class="grid" id="grid">{cards_html}</div>
    <div class="modal" id="modal"><div class="profile-box" id="profileContent"></div></div>

<script>
    let activeProfileData = null; 
    let lang = "vn";

    const TEXT = {{
        vn: {{ 
            search: "🔍 Nhập tên hoặc ID...", 
            pow: "⚡ SỨC MẠNH BIẾN ĐỘNG", 
            kill: "🔥 TIÊU DIỆT BIẾN ĐỘNG", 
            dead: "💀 ĐIỂM CHẾT BIẾN ĐỘNG", 
            
            lbl_pow: "⚡ SỨC MẠNH",
            lbl_kill: "🔥 TIÊU DIỆT",
            lbl_dead: "💀 ĐIỂM CHẾT",
            
            box_title: "BIẾN ĐỘNG ĐIỂM TIÊU DIỆT",
            box_t4: "• Điểm T4 tăng thêm:",
            box_t5: "• Điểm T5 tăng thêm:",
            box_total: "• Tổng điểm (T4 + T5):",
            
            kK_label: "🔥 KPI Tiêu Diệt (T4+T5)", 
            kD_label: "💀 KPI Điểm chết", 
            kT_label: "📊 KPI TỔNG ĐẠT ĐƯỢC",
            exit: "QUAY LẠI",
            
            msg_perfect: "Đỉnh đấy bro 😎",
            msg_good: "Cũng khá ổn đấy nhưng cần cố gắng thêm 🫣",
            msg_warn: "Bạn cần nộp phạt Rss để ở lại hoặc nhận vé bay miễn phí và rời đi 💸",
            msg_kick: "Vui lòng rời đi trước ngày 26/9 🚨"
        }},
        en: {{ 
            search: "🔍 Search name or ID...", 
            pow: "⚡ POWER CHANGE", 
            kill: "🔥 KILLS CHANGE", 
            dead: "💀 DEAD CHANGE", 
            
            lbl_pow: "⚡ POWER",
            lbl_kill: "🔥 KILLS",
            lbl_dead: "💀 DEAD",
            
            box_title: "KILL POINTS CHANGE",
            box_t4: "• T4 Points Gained:",
            box_t5: "• T5 Points Gained:",
            box_total: "• Total Points (T4 + T5):",
            
            kK_label: "🔥 Kills KPI (T4+T5)", 
            kD_label: "💀 Dead KPI", 
            kT_label: "📊 OVERALL KPI ACHIEVED",
            exit: "CLOSE",
            
            msg_perfect: "Absolute beast, bro! 😎",
            msg_good: "Not bad, but you need to push harder 🫣",
            msg_warn: "Pay RSS fine to stay, or take a free passport and leave 💸",
            msg_kick: "Please migrate out before Sept 26th 🚨"
        }}
    }};

    document.getElementById("langBtn").onclick = function() {{
        lang = lang === "vn" ? "en" : "vn";
        this.innerText = lang.toUpperCase();
        
        document.getElementById("searchInput").placeholder = TEXT[lang].search;
        document.getElementById("fPow").innerText = TEXT[lang].pow;
        document.getElementById("fKill").innerText = TEXT[lang].kill;
        document.getElementById("fDead").innerText = TEXT[lang].dead;
        
        let activeFilter = document.querySelector('.filter.active');
        if(activeFilter) {{
            let mode = activeFilter.id === 'fPow' ? 'power' : (activeFilter.id === 'fKill' ? 'kill' : 'dead');
            updateCardValues(mode);
        }}
        
        if (activeProfileData) {{
            renderModalContent();
        }}
    }};

    function search(v) {{
        v = v.toLowerCase();
        document.querySelectorAll('.card').forEach(c => {{
            const name = c.querySelector('.card-name').innerText.toLowerCase();
            const id = c.getAttribute('data-id').toLowerCase();
            if (name.includes(v) || id.includes(v)) {{
                c.style.display = 'block';
            }} else {{
                c.style.display = 'none';
            }}
        }});
    }}

    function setMode(m, el) {{
        document.querySelectorAll('.filter').forEach(f => f.classList.remove('active'));
        el.classList.add('active');
        let grid = document.getElementById('grid');
        let cards = Array.from(grid.getElementsByClassName('card'));
        cards.sort((a,b) => Number(b.dataset[m]) - Number(a.dataset[m]));
        grid.innerHTML = "";
        cards.forEach(c => grid.appendChild(c));
        updateCardValues(m);
    }}

    function updateCardValues(m) {{
        document.querySelectorAll('.card').forEach(c => {{
            let prefix = m === 'power' ? '⚡ ' : (m === 'kill' ? '🔥 ' : '💀 ');
            c.querySelector('.value').innerText = prefix + Number(c.dataset[m]).toLocaleString();
        }});
    }}

    function toggleTDetail() {{
        let box = document.getElementById('tDetailBox');
        if(box.style.display === 'none' || box.style.display === '') {{
            box.style.display = 'block';
        }} else {{
            box.style.display = 'none';
        }}
    }}

    function openProfile(name, id, all, tPow, tKill, tDead, dKill, dDead, kK, kD, realPctK, realPctD, realPctT, barK, barD, barT, dt4, dt5, avatar) {{
        activeProfileData = {{ name, id, all, tPow, tKill, tDead, dKill, dDead, kK, kD, realPctK, realPctD, realPctT, barK, barD, barT, dt4, dt5, avatar }};
        document.getElementById('modal').style.display = 'flex';
        renderModalContent();
    }}

    function renderModalContent() {{
        if (!activeProfileData) return;
        let d = activeProfileData;
        let t = TEXT[lang];
        
        let systemMsg = "";
        let alertBorderColor = "#ff4b4b"; 
        let pct = Number(d.realPctT);
        
        if(pct >= 100) {{
            systemMsg = t.msg_perfect;
            alertBorderColor = "#00ffcc";
        }} else if(pct >= 70) {{
            systemMsg = t.msg_good;
            alertBorderColor = "gold";
        }} else if(pct >= 50) {{
            systemMsg = t.msg_warn;
            alertBorderColor = "#ff9900";
        }} else {{
            systemMsg = t.msg_kick;
            alertBorderColor = "#ff4b4b";
        }}
        
        document.getElementById('profileContent').innerHTML = `
            <center>
                <div class="avatar-wrap" style="width:70px; height:70px;"><img src="${{d.avatar}}"></div>
                <h3 style="margin:10px 0 5px 0;">${{d.name}}</h3>
                <small style="color:#888;">ID: ${{d.id}} | ${{d.all}}</small>
            </center>
            
            <div class="stat-row">
                <div class="stat-card">${{t.lbl_pow}}<br><b>${{Number(d.tPow).toLocaleString()}}</b></div>
                <div class="stat-card">
                    ${{t.lbl_kill}} <button class="info-trigger" onclick="toggleTDetail()">!</button>
                    <br><b>${{Number(d.tKill).toLocaleString()}}</b>
                </div>
                <div class="stat-card">${{t.lbl_dead}}<br><b>${{Number(d.tDead).toLocaleString()}}</b></div>
            </div>
            
            <div class="t-detail-box" id="tDetailBox">
                <div style="color: gold; font-weight: bold; margin-bottom: 5px; text-align: center;">${{t.box_title}}</div>
                <div>${{t.box_t4}} <span>${{Number(d.dt4) > 0 ? '+' : ''}}${{Number(d.dt4).toLocaleString()}}</span></div>
                <div>${{t.box_t5}} <span>${{Number(d.dt5) > 0 ? '+' : ''}}${{Number(d.dt5).toLocaleString()}}</span></div>
                <div style="border-top: 1px dashed #333; margin-top: 5px; padding-top: 5px;">${{t.box_total}} <span style="color: gold;">${{Number(d.dKill).toLocaleString()}}</span></div>
            </div>

            <div class="kpi-section">
                <div class="kpi-label">
                    <span>${{t.kK_label}} <span class="pct-tag">${{d.realPctK}}%</span></span>
                    <span>${{Number(d.dKill).toLocaleString()}} / ${{Number(d.kK).toLocaleString()}}</span>
                </div>
                <div class="bar"><div class="fill" style="width: ${{d.barK}}%;"></div></div>
                
                <div class="kpi-label">
                    <span>${{t.kD_label}} <span class="pct-tag">${{d.realPctD}}%</span></span>
                    <span>${{Number(d.dDead).toLocaleString()}} / ${{Number(d.kD).toLocaleString()}}</span>
                </div>
                <div class="bar"><div class="fill" style="width: ${{d.barD}}%;"></div></div>
                
                <hr style="border: 0; border-top: 1px solid #333; margin: 15px 0;">
                
                <div class="kpi-label" style="color: #00ffcc;">
                    <span>${{t.kT_label}} <span class="pct-tag" style="background: rgba(0,255,150,0.2); color: #00ffcc; font-weight: bold;">${{d.realPctT}}%</span></span>
                </div>
                <div class="bar"><div class="fill fill-total" style="width: ${{d.barT}}%;"></div></div>
            </div>
            
            <div class="alert-box" style="border-left-color: ${{alertBorderColor}};">
                <b style="color: ${{alertBorderColor}}; font-size: 11px; display:block; margin-bottom:4px;">SYSTEM NOTICE:</b>
                <span>${{systemMsg}}</span>
            </div>
            
            <button class="close-btn" onclick="closeProfile()">${{t.exit}}</button>
        `;
    }}

    function closeProfile() {{
        document.getElementById('modal').style.display = 'none';
        activeProfileData = null;
    }}
</script>
</body>
</html>
"""

components.html(html_content, height=1000, scrolling=True)
