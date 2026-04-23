import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="FTD KPI | COMMAND CENTER", layout="wide")

# --- 2. GIAO DIỆN (CSS NÂNG CẤP) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e6ed; }
    
    /* Hiệu ứng kính mờ cho Card */
    .command-card {
        background: rgba(26, 28, 35, 0.8);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        border: 1px solid rgba(0, 212, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    .player-name {
        color: #ffffff; font-size: 45px; font-weight: 800; 
        line-height: 1; margin-bottom: 5px;
        text-transform: uppercase; letter-spacing: -1px;
    }

    .id-tag { color: #00d4ff; font-family: monospace; font-size: 14px; margin-bottom: 25px; }
    
    .stat-box { margin-bottom: 20px; }
    .stat-label { color: #8899a6; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
    .stat-value { color: #ffffff; font-size: 22px; font-weight: bold; }
    
    /* Tinh chỉnh thanh tiến độ nhỏ */
    .stProgress { height: 4px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ VÒNG TRÒN KPI LỒNG NHAU (CHUYÊN NGHIỆP) ---
def draw_kpi_circles(kpi_total, kpi_kill, kpi_dead):
    fig = go.Figure()

    # Cấu hình chung cho các vòng tròn
    rings = [
        {'value': kpi_total, 'color': '#00d4ff', 'radius': 1.0, 'name': 'TOTAL'},
        {'value': kpi_kill, 'color': '#fbbf24', 'radius': 0.8, 'name': 'KILL'},
        {'value': kpi_dead, 'color': '#f87171', 'radius': 0.6, 'name': 'DEAD'}
    ]

    for ring in rings:
        # Vòng nền mờ
        fig.add_trace(go.Pie(
            hole=ring['radius'] - 0.1, values=[100], 
            marker=dict(colors=['rgba(255,255,255,0.05)']),
            showlegend=False, hoverinfo='skip'
        ))
        # Vòng dữ liệu thực
        fig.add_trace(go.Pie(
            hole=ring['radius'] - 0.1, 
            values=[ring['value'], 100 - ring['value'] if ring['value'] < 100 else 0],
            marker=dict(colors=[ring['color'], 'rgba(0,0,0,0)']),
            showlegend=False, hoverinfo='label+percent',
            direction='clockwise', sort=False
        ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0),
        annotations=[dict(text=f"{kpi_total}%", x=0.5, y=0.5, font_size=40, font_color="#00d4ff", showarrow=False)]
    )
    return fig

# --- 4. XỬ LÝ DỮ LIỆU (Giữ nguyên logic của bạn) ---
# ... (Phần load_data giữ nguyên như code bạn đã gửi) ...
# (Giả định hàm load_data đã chạy và có biến df)

# --- 5. HIỂN THỊ CHI TIẾT ---
# Giả sử người dùng đã chọn một player 'sel'
if df is not None and sel != L["select"]:
    d = df[df['Tên_2'] == sel].iloc[0]
    
    # Tính toán tỷ lệ phần trăm riêng cho từng loại để vẽ vòng tròn
    kpi_kill = max(0.0, min(float(d['KI']) / d['GK'], 1.0)) * 100 if d['GK'] > 0 else 0
    kpi_dead = max(0.0, min(float(d['DI']) / d['GD'], 1.0)) * 100 if d['GD'] > 0 else 0
    kpi_total = float(d['KPI'])

    # Bố cục 2 cột theo phong cách NBA Card
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown(f"""
            <div class="command-card">
                <div class="player-name">{sel}</div>
                <div class="id-tag">ID: {d['ID']} • {d['Liên Minh_2']}</div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                    <div class="stat-box">
                        <div class="stat-label">Sức Mạnh</div>
                        <div class="stat-value">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Tổng Tiêu Diệt</div>
                        <div class="stat-value">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                </div>
                
                <hr style="border: 0.5px solid rgba(255,255,255,0.1); margin: 20px 0;">
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                    <div>
                        <div class="stat-label">Mục Tiêu Kill</div>
                        <div style="color:#fbbf24; font-size:18px; font-weight:bold;">{int(d['GK']):,}</div>
                        <p style="font-size:11px; color:#8899a6;">Đã đạt: {int(d['KI']):,}</p>
                    </div>
                    <div>
                        <div class="stat-label">Mục Tiêu Dead</div>
                        <div style="color:#f87171; font-size:18px; font-weight:bold;">{int(d['GD']):,}</div>
                        <p style="font-size:11px; color:#8899a6;">Đã đạt: {int(d['DI']):,}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Hiển thị vòng tròn KPI lồng nhau
        st.plotly_chart(draw_kpi_circles(kpi_total, kpi_kill, kpi_dead), use_container_width=True)

    # Bảng tổng hợp bên dưới giữ nguyên
    st.divider()
    st.subheader(L["table"])
    # ... (Phần dataframe giữ nguyên) ...
