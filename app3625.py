import streamlit as st
import plotly.graph_objects as go

# 1. Thiết lập trang
st.set_page_config(layout="wide")

# 2. Inject CSS để tạo khung nổi xanh đậm giữa màn hình
st.markdown("""
    <style>
    /* Nền tối phía sau */
    .stApp {
        background-color: #050a0e !important;
    }

    /* Tạo khung nổi chính */
    [data-testid="stVerticalBlock"] > div:has(div.floating-card) {
        display: flex;
        justify-content: center;
    }

    .floating-card {
        background: linear-gradient(145deg, #0a3d62, #062c43); /* Màu xanh đậm */
        border: 2px solid #3282b8;
        border-radius: 20px;
        padding: 40px;
        width: 100%;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 
                    inset 0 0 15px rgba(50, 130, 184, 0.3);
        color: white;
    }

    /* Tùy chỉnh các ô thông số nhỏ bên trong */
    .stat-box {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    .s-label { color: #bbe1fa; font-size: 12px; text-transform: uppercase; font-weight: bold; }
    .s-value { display: block; font-size: 24px; font-weight: 800; margin-top: 5px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. Hàm vẽ biểu đồ (Sửa lỗi ValueError từ ảnh của bạn)
def draw_kpi(pct, color, title):
    try: val = float(pct)
    except: val = 0.0
    
    fig = go.Figure(go.Pie(
        hole=0.7, values=[val, max(0, 100-val)],
        marker=dict(colors=[color, "rgba(255,255,255,0.05)"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        # SỬA LỖI: Không dùng fontWeight trong Plotly, dùng thẻ <b>
        title={'text': f"<b>{title}</b>", 'y':0.95, 'x':0.5, 'xanchor':'center', 'font':{'color':'white', 'size':14}},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, b=0, l=10, r=10), height=200,
        annotations=[dict(text=f"<b>{val}%</b>", x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=20))]
    )
    return fig

# 4. Hiển thị nội dung
# Dùng container để bao bọc toàn bộ nội dung vào khung
with st.container():
    # Thẻ div mở đầu để nhận CSS floating-card
    st.markdown('<div class="floating-card">', unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 style="margin:0; font-size:40px;">战士: 56 3IMAD</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#bbe1fa; margin-bottom:30px;">ID: 154411253 | <span style="color:#ffd700;">[[C/56]PRAETORIA]</span></p>', unsafe_allow_html=True)
    
    # Hàng thông số (Stats)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown('<div class="stat-box"><span class="s-label">Tiêu Diệt</span><span class="s-value">3,358,382</span></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="stat-box"><span class="s-label">Sức Mạnh</span><span class="s-value">13,212,420</span></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="stat-box"><span class="s-label">Điểm Chết</span><span class="s-value">0</span></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="stat-box"><span class="s-label">Xếp Hạng</span><span class="s-value" style="color:#ffd700">S-RANK</span></div>', unsafe_allow_html=True)
    
    st.markdown('<div style="text-align:center; margin-top:40px; font-weight:bold; color:#bbe1fa;">TIẾN ĐỘ CHIẾN DỊCH KVK</div>', unsafe_allow_html=True)
    
    # Hàng biểu đồ
    k1, k2, k3 = st.columns(3)
    with k1: st.plotly_chart(draw_kpi(0, "#00ffff", "KPI KILL"), use_container_width=True)
    with k2: st.plotly_chart(draw_kpi(0, "#ff4b4b", "KPI DEAD"), use_container_width=True)
    with k3: st.plotly_chart(draw_kpi(0, "#ffd700", "TOTAL KPI"), use_container_width=True)
    
    # Thẻ đóng div
    st.markdown('</div>', unsafe_allow_html=True)
