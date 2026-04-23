import streamlit as st
import plotly.graph_objects as go

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide")

# --- CSS TẠO KHUNG NỔI GIỮA MÀN HÌNH ---
st.markdown("""
    <style>
    /* Nền tối sâu phía sau để khung nổi bật lên */
    .stApp {
        background-color: #050a0e !important;
    }

    /* Container chính căn giữa */
    .flex-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px 0;
    }

    /* Hiệu ứng khung nổi màu xanh đậm (Glassmorphism) */
    .floating-card {
        background: linear-gradient(145deg, #0f4c75, #082d45);
        border: 2px solid #3282b8;
        border-radius: 20px;
        padding: 40px;
        width: 85%;
        max-width: 1000px;
        /* Tạo bóng đổ để có hiệu ứng nổi 3D */
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 
                    inset 0 0 20px rgba(50, 130, 184, 0.2);
        color: white;
        text-align: left;
    }

    /* Hiệu ứng bóng bẩy cho các ô thông số */
    .stat-box {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .stat-box:hover {
        transform: translateY(-5px); /* Hiệu ứng nổi lên khi di chuột vào */
        border-color: #3282b8;
    }

    .label { color: #bbe1fa; font-size: 11px; font-weight: bold; text-transform: uppercase; }
    .value { font-size: 24px; font-weight: 800; display: block; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM VẼ BIỂU ĐỒ (SỬA LỖI VALUEERROR) ---
def draw_chart(pct, color, title):
    try: val = float(pct)
    except: val = 0.0
    
    fig = go.Figure(go.Pie(
        hole=0.7, values=[val, max(0, 100-val)],
        marker=dict(colors=[color, "rgba(255,255,255,0.05)"]),
        showlegend=False, hoverinfo='skip'
    ))
    fig.update_layout(
        title={'text': f"<b>{title}</b>", 'y':0.95, 'x':0.5, 'xanchor':'center', 'font':{'color':'white','size':14}},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, b=0, l=10, r=10), height=180,
        annotations=[dict(text=f"<b>{val}%</b>", x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=20))]
    )
    return fig

# --- DỮ LIỆU ---
d = {
    "Tên": "56 3IMAD",
    "ID": "154411253",
    "Liên Minh": "[[C/56]PRAETORIA]",
    "Tiêu Diệt": 3358382,
    "Sức Mạnh": 13212420,
    "KPI_K": 0.0, "KPI_D": 0.0, "KPI_T": 0.0
}

# --- BẮT ĐẦU HIỂN THỊ ---
# Bao bọc toàn bộ trong một class flex để căn giữa
st.markdown('<div class="flex-container">', unsafe_allow_html=True)

# Mở khung nổi
st.markdown(f"""
    <div class="floating-card">
        <div style="margin-bottom: 30px;">
            <h1 style="margin:0; font-size:45px; letter-spacing: 2px;">战士: {d['Tên']}</h1>
            <p style="color:#bbe1fa; font-size:16px;">ID: {d['ID']} | <span style="color:#ffd700;">{d['Liên Minh']}</span></p>
        </div>
    """, unsafe_allow_html=True)

# Chia cột thông số bên trong khung
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="stat-box"><span class="label">Tiêu Diệt</span><span class="value">{d["Tiêu Diệt"]:,}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-box"><span class="label">Sức Mạnh</span><span class="value">{d["Sức Mạnh"]:,}</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="stat-box"><span class="label">Điểm Chết</span><span class="value">0</span></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="stat-box"><span class="label">Xếp Hạng</span><span class="value" style="color:#ffd700">S-RANK</span></div>', unsafe_allow_html=True)

st.markdown('<div style="margin-top:40px; text-align:center;"><p class="label">Tiến độ chiến dịch KVK</p></div>', unsafe_allow_html=True)

# Biểu đồ KPI
k1, k2, k3 = st.columns(3)
with k1: st.plotly_chart(draw_chart(d['KPI_K'], "#00ffff", "KPI KILL"), use_container_width=True, config={'displayModeBar': False})
with k2: st.plotly_chart(draw_chart(d['KPI_D'], "#ff4b4b", "KPI DEAD"), use_container_width=True, config={'displayModeBar': False})
with k3: st.plotly_chart(draw_chart(d['KPI_T'], "#ffd700", "TỔNG KPI"), use_container_width=True, config={'displayModeBar': False})

# Đóng khung nổi và flex-container
st.markdown('</div></div>', unsafe_allow_html=True)
