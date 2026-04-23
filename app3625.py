import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH & CSS (Tái tạo layout NBA/Game chuyên nghiệp) ---
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #111111; color: #ffffff; }
    
    /* Container chính cho Profile Card */
    .profile-container {
        background: #1a1c23;
        border-radius: 15px;
        padding: 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #2d2f36;
    }

    /* Cột bên trái: Thông tin văn bản */
    .info-column { flex: 1; }
    
    .first-name { color: #8899a6; font-size: 24px; margin-bottom: -10px; }
    .last-name { color: #ffffff; font-size: 60px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }
    
    .id-section { display: flex; align-items: center; gap: 15px; margin: 20px 0; }
    .alliance-logo { background: #ffcc00; border-radius: 50%; width: 40px; height: 40px; }
    .id-text { color: #ffffff; font-size: 18px; font-weight: 600; }

    .main-stats { display: flex; gap: 50px; margin-top: 30px; border-bottom: 1px solid #333; padding-bottom: 20px; }
    .stat-item { display: flex; flex-direction: column; }
    .stat-label { color: #8899a6; font-size: 14px; text-transform: uppercase; }
    .stat-val { color: #ffffff; font-size: 32px; font-weight: 700; }

    .sub-stats-grid { display: grid; grid-template-columns: 120px 1fr; gap: 15px; margin-top: 20px; color: #8899a6; font-size: 14px; }
    .sub-label { font-weight: bold; }
    .sub-val { color: #ffffff; }

    /* Cột bên phải: Vòng tròn KPI */
    .kpi-column { flex: 1; display: flex; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀM VẼ VÒNG TRÒN KPI (Multi-Ring Chart) ---
def draw_nba_kpi(kpi_total, kpi_kill, kpi_dead):
    fig = go.Figure()

    # Vòng 1 (Ngoài cùng - Total)
    fig.add_trace(go.Pie(hole=0.85, values=[kpi_total, 100-kpi_total if kpi_total < 100 else 0],
                         marker=dict(colors=['#ffcc00', '#222']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))
    
    # Vòng 2 (Giữa - Kill)
    fig.add_trace(go.Pie(hole=0.75, values=[kpi_kill, 100-kpi_kill if kpi_kill < 100 else 0],
                         marker=dict(colors=['#00d4ff', '#222']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))
    
    # Vòng 3 (Trong cùng - Dead)
    fig.add_trace(go.Pie(hole=0.65, values=[kpi_dead, 100-kpi_dead if kpi_dead < 100 else 0],
                         marker=dict(colors=['#ffffff', '#222']), showlegend=False, hoverinfo='skip', direction='clockwise', sort=False))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0), width=450, height=450,
        annotations=[dict(text=f"KPI<br>{kpi_total}%", x=0.5, y=0.5, font_size=25, font_color="white", showarrow=False, align="center")]
    )
    return fig

# --- 3. LOGIC HIỂN THỊ (Giả định dữ liệu đã có từ file trước) ---
# (Phần này tôi dùng dữ liệu mẫu để bạn thấy form, bạn hãy thay bằng biến 'd' từ df của bạn)
if 'df' in locals() or True: # Force hiển thị mẫu
    # Dữ liệu giả lập để test form
    player_name = "NAVYD"
    player_id = "12345678"
    alliance = "FTD"
    power = "55,000,000"
    kill_total = "1,250,500,000"
    
    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        st.markdown(f"""
            <div class="info-column">
                <div class="first-name">Warrior</div>
                <div class="last-name">{player_name}</div>
                
                <div class="id-section">
                    <div class="alliance-logo"></div>
                    <div class="id-text">#{player_id} | {alliance}</div>
                    <div style="border:1px solid #444; padding:5px 15px; border-radius:20px; font-size:12px;">FOLLOW +</div>
                </div>

                <div class="main-stats">
                    <div class="stat-item">
                        <div class="stat-label">Power</div>
                        <div class="stat-val">{power}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Total Kills</div>
                        <div class="stat-val">{kill_total}</div>
                    </div>
                </div>

                <div class="sub-stats-grid">
                    <div class="sub-label">Alliance:</div><div class="sub-val">Fight to Dead [FTD]</div>
                    <div class="sub-label">Kingdom:</div><div class="sub-val">3625</div>
                    <div class="sub-label">Status:</div><div class="sub-val">Active - Frontline</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_right:
        # Giả định % KPI đạt được
        st.plotly_chart(draw_nba_kpi(85, 90, 70), use_container_width=True, config={'displayModeBar': False})

    # Bảng stats chi tiết nằm dưới cùng giống hình mẫu
    st.markdown("<br>", unsafe_allow_html=True)
    stats_data = {
        "Phase": ["KvK Pass 4", "KvK Pass 7", "Current Season"],
        "Kills": ["20M", "45M", "100M"],
        "Deads": ["200K", "500K", "1.2M"],
        "DKP": ["1.2B", "2.5B", "5.1B"],
        "KPI": ["95%", "102%", "88%"]
    }
    st.table(pd.DataFrame(stats_data))
