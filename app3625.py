# --- 5. GIAO DIỆN CHÍNH ---
if df is not None:
    # Logo & Slogan
    st.markdown(f"""
        <div class="logo-container">
            <img src="{LOGO_MAIN}" class="logo-img">
            <div class="slogan">{L['slogan']}</div>
        </div>
    """, unsafe_allow_html=True)

    # Thêm CSS cho Bảng mới (Elite Table)
    st.markdown("""
        <style>
        .elite-table-container {
            background: rgba(13, 27, 42, 0.9);
            border: 1px solid #1e3a5a;
            border-radius: 12px;
            padding: 5px;
            overflow-x: auto;
            margin-top: 20px;
        }
        table.elite-table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Segoe UI', sans-serif;
            min-width: 1000px;
        }
        .elite-table thead {
            background: linear-gradient(90deg, #162a3e 0%, #1c3d5a 100%);
            border-bottom: 2px solid #00d4ff;
        }
        .elite-table th {
            padding: 15px 12px;
            text-align: left;
            font-size: 11px;
            color: #00d4ff;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .elite-table tr {
            border-bottom: 1px solid #1a2a3a;
            transition: 0.2s;
        }
        .elite-table tr:hover {
            background: rgba(0, 212, 255, 0.08);
        }
        .elite-table td {
            padding: 12px;
            font-size: 14px;
            color: #e0e6ed;
        }
        
        /* Màu sắc các cột */
        .val-name { font-weight: bold; color: #ffffff; }
        .val-id { color: #8b949e; font-size: 11px; }
        .val-power { color: #ffffff; font-weight: bold; }
        .val-kill { color: #00ffcc; font-weight: bold; }
        .val-dead { color: #ff4b4b; font-weight: bold; }
        .badge-rank {
            background: #ffd700;
            color: #000;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 900;
            font-size: 12px;
        }

        /* Thanh KPI Mini */
        .kpi-bar-bg {
            width: 60px;
            height: 6px;
            background: #1a2a3a;
            border-radius: 3px;
            display: inline-block;
            vertical-align: middle;
            margin-right: 8px;
        }
        .kpi-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #00d4ff, #00ffcc);
            box-shadow: 0 0 8px #00d4ff;
            border-radius: 3px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Thanh tìm kiếm
    sel = st.selectbox("", sorted(df['Tên_2'].unique()), index=None, placeholder=L['search'], label_visibility="collapsed")

    # Hiển thị Card Profile (Giữ nguyên của Louis)
    if sel:
        d = df[df['Tên_2'] == sel].iloc[0]
        html_card = f"""
        <div style="position: relative; width: 100%; margin: 60px auto 10px; font-family: 'Segoe UI', sans-serif;">
            <div style="position: absolute; top: -50px; left: 50%; transform: translateX(-50%); background: #1c2e3e; border: 2px solid #00d4ff; border-radius: 12px; padding: 12px 40px; z-index: 10; text-align: center; border-bottom: 4px solid #ffd700; box-shadow: 0 8px 25px rgba(0,0,0,0.8); min-width: 450px;">
                <div style="color: #00d4ff; font-size: 11px; font-weight: 900; letter-spacing: 2px; margin-bottom: 5px;">PROFILE MEMBER</div>
                <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
                    <img src="{LOGO_PROFILE}" style="width: 50px; height: 50px; object-fit: contain;">
                    <div style="color: #ffffff; font-size: 28px; font-weight: bold; text-shadow: 0 0 10px #00d4ff;">{sel}</div>
                </div>
                <div style="font-size: 13px; margin-top: 8px;">
                    <b style="color: #ffd700;">ID:</b> <span style="color: #fff;">{d['ID']}</span> | 
                    <b style="color: #00ffcc;">ALLIANCE:</b> <span style="color: #fff;">{d['Liên Minh_2']}</span>
                </div>
            </div>
            <div style="background: rgba(13, 25, 47, 0.98); border: 2px solid #00d4ff; border-radius: 15px; padding: 85px 20px 20px 20px;">
                <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 25px;">
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3.5px solid #00d4ff;">
                        <div style="font-size: 10px; color: #8b949e; font-weight: bold;">{L['pow']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #fff;">{int(d['Sức Mạnh_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3.5px solid #00ffcc;">
                        <div style="font-size: 10px; color: #8b949e; font-weight: bold;">{L['tk']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #fff;">{int(d['Tổng Tiêu Diệt_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-bottom: 3.5px solid #ff4b4b;">
                        <div style="font-size: 10px; color: #ff4b4b; font-weight: bold;">{L['td']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #ff4b4b;">{int(d['Điểm Chết_2']):,}</div>
                    </div>
                    <div style="background: #233549; border-radius: 10px; padding: 15px; flex: 0.6; text-align: center; border-bottom: 3.5px solid #ffd700;">
                        <div style="font-size: 10px; color: #ffd700; font-weight: bold;">{L['rank']}</div>
                        <div style="font-size: 22px; font-weight: 900; color: #ffd700;">#{d['KillRank']}</div>
                    </div>
                </div>
                <div style="background: #1a2a3a; border-radius: 15px; padding: 30px; border-bottom: 5px solid #ffd700; display: flex; justify-content: space-around; align-items: center;">
                    <div style="text-align: center;">
                        <div style="position: relative; width: 90px; height: 90px; margin: 0 auto;">
                            <svg viewBox="0 0 36 36" style="width: 90px; height: 90px; transform: rotate(-90deg);">
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="4"></circle>
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#00ffff" stroke-width="3.5" stroke-dasharray="{min(d['KPI_K'], 100)}, 100" stroke-linecap="round"></circle>
                            </svg>
                            <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:16px; font-weight:bold; color: #00ffff;">{d['KPI_K']}%</div>
                        </div>
                        <div style="font-size: 11px; color: #00ffff; font-weight: bold; margin-top: 10px;">KPI KILL</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="position: relative; width: 130px; height: 130px; margin: 0 auto;">
                            <svg viewBox="0 0 36 36" style="width: 130px; height: 130px; transform: rotate(-90deg);">
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="4"></circle>
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#ffd700" stroke-width="4" stroke-dasharray="{min(d['KPI_T'], 100)}, 100" stroke-linecap="round"></circle>
                            </svg>
                            <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:24px; font-weight:900; color:#ffd700;">{d['KPI_T']}%</div>
                        </div>
                        <div style="font-size: 15px; color: #ffd700; font-weight: bold; margin-top: 10px;">TOTAL KPI</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="position: relative; width: 90px; height: 90px; margin: 0 auto;">
                            <svg viewBox="0 0 36 36" style="width: 90px; height: 90px; transform: rotate(-90deg);">
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#0d151f" stroke-width="4"></circle>
                                <circle cx="18" cy="18" r="16" fill="none" stroke="#ff4b4b" stroke-width="3.5" stroke-dasharray="{min(d['KPI_D'], 100)}, 100" stroke-linecap="round"></circle>
                            </svg>
                            <div style="position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:16px; font-weight:bold; color: #ff4b4b;">{d['KPI_D']}%</div>
                        </div>
                        <div style="font-size: 11px; color: #ff4b4b; font-weight: bold; margin-top: 10px;">KPI DEAD</div>
                    </div>
                </div>
            </div>
        </div>
        """
        components.html(html_card, height=580)

    # --- TẠO BẢNG HTML TÙY CHỈNH ---
    df_sorted = df.sort_values(by='KillRank')
    
    # Header bảng
    h = L['cols']
    table_header = f"""
        <thead>
            <tr>
                <th>{h[3]}</th><th>{h[0]}</th><th>{h[4]}</th><th>{h[5]}</th>
                <th>{h[6]}</th><th>{h[7]}</th><th>{h[8]}</th><th>{h[9]}</th>
            </tr>
        </thead>
    """
    
    # Body bảng
    table_rows = ""
    for _, r in df_sorted.iterrows():
        kpi_val = float(r['KPI_T'])
        bar_width = min(kpi_val, 100)
        
        table_rows += f"""
            <tr>
                <td><span class="badge-rank">#{int(r['KillRank'])}</span></td>
                <td><span class="val-name">{r['Tên_2']}</span><br><span class="val-id">ID: {r['ID']}</span></td>
                <td class="val-power">{int(r['Sức Mạnh_2']):,}</td>
                <td class="val-kill">{int(r['Tổng Tiêu Diệt_2']):,}</td>
                <td class="val-dead">{int(r['Điểm Chết_2']):,}</td>
                <td style="color:#00ffff">{int(r['KI']):,}</td>
                <td style="color:#ff4b4b">{int(r['DI']):,}</td>
                <td>
                    <div class="kpi-bar-bg"><div class="kpi-bar-fill" style="width: {bar_width}%;"></div></div>
                    <span style="color:#00ffcc; font-weight:bold;">{kpi_val}%</span>
                </td>
            </tr>
        """
    
    full_table_html = f"""
    <div class="elite-table-container">
        <table class="elite-table">
            {table_header}
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    """
    
    st.markdown(full_table_html, unsafe_allow_html=True)

    # Footer
    st.markdown(f'<div class="footer">🛡️ Discord: <b>louiss.nee</b> | Zalo: <b>0.3.7.3.2.7.4.6.0.0</b></div>', unsafe_allow_html=True)
