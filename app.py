# app.py
import streamlit as st

# Import các Class và Hàm từ module baccarat_engine
from baccarat_engine import (
    VisionScannerEngine,
    BaccaratInterfaceSystem,
    calculate_v68_1_fusion,
    get_ultimate_directive,
    parse_baccarat_input
)

# 1. KHỞI CHẠY CSS VÀ SIDEBAR (Phải đặt trước mọi logic khác)
BaccaratInterfaceSystem.inject_mobile_css()
decks, hist_p, hist_b, hist_t = BaccaratInterfaceSystem.render_sidebar()

# Khởi tạo session_state an toàn để không bị xóa dữ liệu khi load lại trang
if 'round_detailed_log' not in st.session_state:
    st.session_state.round_detailed_log = []

st.markdown("### ⚡ ORACLE TREND TRACKING v68.1")
st.caption("Giao diện lưới siêu nén chống vỡ dọc trên thiết bị di động Android / iOS")

# 2. KHÔNG GIAN CAMERA & QUÉT ẢNH TỰ ĐỘNG
img_file = VisionScannerEngine.render_camera_hud()

if img_file is not None:
    st.markdown('<div class="vision-btn-box">', unsafe_allow_html=True)
    vision_triggered = st.button("🔮 PHÂN TÍCH ẢNH VÀ ĐỒNG BỘ")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if vision_triggered:
        detected_roadmap = VisionScannerEngine.decode_and_parse_roadmap(img_file.getvalue())
        if detected_roadmap:
            for outcome in detected_roadmap:
                st.session_state.round_detailed_log.append({
                    'p_cards': [], 'b_cards': [], 'p_score': 0, 'b_score': 0, 'outcome': outcome
                })
            # Thay vì dùng st.rerun() dễ gây lặp vô hạn trên mobile, ta dùng st.fragment hoặc để Streamlit tự làm mới
            st.success(f"Đã đồng bộ thành công {len(detected_roadmap)} ván bài!")

st.markdown("---")

# 3. LUỒNG TÍNH TOÁN TOÁN HỌC
final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, streak_side, streak_count = calculate_v68_1_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t
)
cmd = get_ultimate_directive(final_p, final_b, trend_desc, streak_side, streak_count, st.session_state.round_detailed_log, hist_p, hist_b)

st.markdown(f'<div class="header-hud-bar">🎰 VÁN ĐÃ QUÉT: <b>{total_p + total_b + total_t}</b> | 🎴 CÒN LẠI: <b>{cards_left}</b> / {decks * 52}</div>', unsafe_allow_html=True)

# 4. KHỐI FORM NHẬP THỦ CÔNG
st.markdown('<p class="section-title">🎴 NHẬP QUÂN BÀI THỦ CÔNG</p>', unsafe_allow_html=True)
with st.form(key="manual_mobile_isolated_form", clear_on_submit=True):
    input_grid = st.columns(2)
    p_str = input_grid[0].text_input("🔵 PLAYER CARD:", placeholder="Ví dụ: 8 K")
    b_str = input_grid[1].text_input("🔴 BANKER CARD:", placeholder="Ví dụ: 7")
    st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
    calc_triggered = st.form_submit_button("🔥 KHỞI CHẠY MA TRẬN")
    st.markdown('</div>', unsafe_allow_html=True)

if calc_triggered and (p_str.strip() or b_str.strip()):
    p_list, b_list = parse_baccarat_input(p_str), parse_baccarat_input(b_str)
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    st.session_state.round_detailed_log.append({'p_cards': p_list, 'b_cards': b_list, 'p_score': p_score, 'b_score': b_score, 'outcome': outcome})

st.markdown("---")

# 5. KHỐI HIỂN THỊ CHỈ THỊ VÀO LỆNH TỐI HẬU
st.markdown(f'<div class="action-panel" style="background-color: {cmd["bg"]}; border: 1px solid {cmd["color"]}; color: {cmd["color"]};"><div class="action-status">{cmd["status"]}</div><div class="action-msg" style="color: #f1f5f9;">{cmd["msg"]}</div><div class="action-vol">MỨC CƯỢC: {cmd["size"]}</div></div>', unsafe_allow_html=True)

# 6. KHỐI 3 CỘT XÁC SUẤT NẰM NGANG
prob_grid = st.columns(3)
prob_grid[0].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER SOV</span><span class="metric-num" style="color:#00afb9;">{final_p:.1f}%</span><span class="metric-sub">Sl: {total_p}</span></div>', unsafe_allow_html=True)
prob_grid[1].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER SOV</span><span class="metric-num" style="color:#ff4757;">{final_b:.1f}%</span><span class="metric-sub">Sl: {total_b}</span></div>', unsafe_allow_html=True)
prob_grid[2].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE HYPER</span><span class="metric-num" style="color:#2ecc71;">{final_t:.1f}%</span><span class="metric-sub">Sl: {total_t}</span></div>', unsafe_allow_html=True)

# 7. NHẬT KÝ TIẾN TRÌNH TÍNH TOÁN
if st.session_state.round_detailed_log:
    st.markdown('<div class="score-log-hud"><b>📊 TIẾN TRÌNH KHẤU TRỪ BÀI VÀ ROADMAP:</b><br>', unsafe_allow_html=True)
    for idx, r in enumerate(st.session_state.round_detailed_log):
        st.markdown(f"• V{idx+1}: P:{r['p_score']}đ vs B:{r['b_score']}đ ➡️ **{r['outcome'].upper()}**")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
util_grid = st.columns(2)
if util_grid[0].button("⏪ HOÀN TÁC CŨ") and st.session_state.round_detailed_log:
    st.session_state.round_detailed_log.pop()
if util_grid[1].button("🔄 LÀM TRỐNG"):
    st.session_state.round_detailed_log = []
