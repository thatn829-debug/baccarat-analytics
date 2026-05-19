# app.py
import streamlit as st
import baccarat_engine as be

# Khởi chạy giao diện và lấy cấu hình dữ liệu đầu vào
be.BaccaratInterfaceSystem.inject_mobile_css()
decks, hist_p, hist_b, hist_t = be.BaccaratInterfaceSystem.render_sidebar()

if 'round_detailed_log' not in st.session_state:
    st.session_state.round_detailed_log = []

st.markdown("### ⚡ ORACLE TREND TRACKING v68.1")

# 1. KHÔNG GIAN XỬ LÝ ẢNH CHỤP BÀN CHƠI
img_file = be.VisionScannerEngine.render_camera_hud()
if img_file is not None:
    if st.button("🔮 PHÂN TÍCH ẢNH VÀ ĐỒNG BỘ"):
        detected = be.VisionScannerEngine.decode_and_parse_roadmap(img_file.getvalue())
        if detected:
            for outcome in detected:
                st.session_state.round_detailed_log.append({'outcome': outcome})
            st.success(f"Đã đồng bộ {len(detected)} ván từ bảng hạt gỗ!")

st.markdown("---")

# 2. LUỒNG TÍNH TOÁN VÀ ĐÁNH GIÁ KẾT QUẢ
final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, _, _ = be.calculate_v68_1_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t
)
cmd = be.get_ultimate_directive(final_p, final_b)

st.markdown(f'<div class="header-hud-bar">🎰 VÁN ĐÃ QUÉT: <b>{total_p + total_b + total_t}</b> | 🎴 CÒN LẠI: <b>{cards_left}</b></div>', unsafe_allow_html=True)

# 3. KHỐI NHẬP LIỆU THỦ CÔNG
st.markdown('<p class="section-title">🎴 NHẬP QUÂN BÀI THỦ CÔNG</p>', unsafe_allow_html=True)
with st.form(key="manual_form", clear_on_submit=True):
    cols = st.columns(2)
    p_str = cols[0].text_input("🔵 PLAYER CARD:")
    b_str = cols[1].text_input("🔴 BANKER CARD:")
    calc_triggered = st.form_submit_button("🔥 KHỞI CHẠY MA TRẬN")

if calc_triggered and (p_str.strip() or b_str.strip()):
    p_list, b_list = be.parse_baccarat_input(p_str), be.parse_baccarat_input(b_str)
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    st.session_state.round_detailed_log.append({'outcome': outcome})

st.markdown("---")

# 4. KHỐI HIỂN THỊ CHỈ THỊ VÀ BẢNG XÁC SUẤT
st.markdown(f'<div class="action-panel" style="background-color: {cmd["bg"]}; border: 1px solid {cmd["color"]}; color: {cmd["color"]};"><div class="action-status">{cmd["status"]}</div><div class="action-msg" style="color: #f1f5f9;">{cmd["msg"]}</div></div>', unsafe_allow_html=True)

prob_grid = st.columns(3)
prob_grid[0].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER</span><br><span class="metric-num" style="color:#00afb9;">{final_p:.1f}%</span></div>', unsafe_allow_html=True)
prob_grid[1].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER</span><br><span class="metric-num" style="color:#ff4757;">{final_b:.1f}%</span></div>', unsafe_allow_html=True)
prob_grid[2].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE</span><br><span class="metric-num" style="color:#2ecc71;">{final_t:.1f}%</span></div>', unsafe_allow_html=True)

# 5. TIỆN ÍCH DỌN DẸP DỮ LIỆU
st.markdown("<br>", unsafe_allow_html=True)
util_cols = st.columns(2)
if util_cols[0].button("⏪ HOÀN TÁC") and st.session_state.round_detailed_log:
    st.session_state.round_detailed_log.pop()
if util_cols[1].button("🔄 LÀM TRỐNG"):
    st.session_state.round_detailed_log = []
