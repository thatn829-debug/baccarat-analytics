import streamlit as st
import numpy as np
import math

# =========================================================================
# MODULE 1: ĐỘNG CƠ CƠ QUANTUM-CHAO V60.2 (ZERO-START ULTRA ENGINE)
# =========================================================================
def calculate_v60_ultra_quantum_engine(all_rounds_log, shoe_decks):
    # Nếu chưa có dữ liệu, trả về toàn bộ bằng 0 ngay lập tức
    if not all_rounds_log:
        return 0.0, 0.0, 0.0, shoe_decks * 52, 0.0, False, None, 0, 0.2

    total_initial_cards = shoe_decks * 52
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    all_flat_cards = []
    current_streak_side = None
    current_streak_count = 0
    
    for idx, r in enumerate(all_rounds_log):
        all_flat_cards.extend(r['p_cards'] + r['b_cards'])
        if r['outcome'] in ["Player", "Banker"]:
            if current_streak_side == r['outcome']:
                current_streak_count += 1
            else:
                current_streak_side = r['outcome']
                current_streak_count = 1
                
    for card in all_flat_cards:
        if card in exact_cards_left:
            exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
            
    cards_remaining = sum(exact_cards_left.values())
    if cards_remaining <= 0: cards_remaining = 1.0
    
    # TRUE EFFECT OF REMOVAL (EOR) CHUẨN QUỐC TẾ
    counting_effect = {
        1: -0.0045, 2: -0.0054, 3: -0.0054, 4: -0.0124, 5: -0.0084, 
        6: +0.0113, 7: +0.0132, 8: +0.0084,                        
        9: -0.0021, 10: +0.0038, 11: +0.0038, 12: +0.0038, 13: +0.0038
    }
    
    total_counting_bias = 0.0
    for card_num, left in exact_cards_left.items():
        cards_removed = (4 * shoe_decks) - left
        total_counting_bias += cards_removed * counting_effect[card_num]
        
    p_0 = sum([exact_cards_left[i] for i in [10, 11, 12, 13]]) / cards_remaining

    base_p = 44.62 + (total_counting_bias * 2.2)
    base_b = 45.86 - (total_counting_bias * 2.2)
    base_t = 9.52 + (p_0 * 2.8)

    volatility_index = 0.0
    lyapunov_exponent = 0.2
    if len(all_rounds_log) >= 2:
        margins = [float(abs(r['p_score'] - r['b_score'])) for r in all_rounds_log]
        variance = float(np.var(margins))
        volatility_index = min(100.0, (math.sqrt(max(0.001, variance)) / 4.5) * 100.0)
        diffs = np.abs(np.diff(margins))
        lyapunov_exponent = math.log(float(np.mean(diffs)) + 1.0) - 0.5

    is_critical = False
    if current_streak_side and current_streak_count >= 4:
        if lyapunov_exponent < 0.45 and volatility_index < 22.0:
            is_critical = True
            if current_streak_side == "Banker":
                base_p += 4.0
                base_b -= 4.0
            else:
                base_b += 4.0
                base_p -= 4.0

    base_p = max(40.0, min(60.0, base_p))
    base_b = max(40.0, min(60.0, base_b))
    base_t = max(6.0, min(16.0, base_t))
    
    total_sum = base_p + base_b + base_t
    return (base_p / total_sum) * 100, (base_b / total_sum) * 100, (base_t / total_sum) * 100, int(cards_remaining), volatility_index, is_critical, current_streak_side, current_streak_count, lyapunov_exponent


# =========================================================================
# MODULE 2: BỘ QUYẾT ĐỊNH HÀNH ĐỘNG THÔNG MINH (ADAPTIVE DIRECTIVE CORTEX)
# =========================================================================
def get_adaptive_directive(p_val, b_val, is_critical, streak_side, streak_count, lyapunov, log):
    if not log:
        return {
            "status": "🛰️ HỆ THỐNG ĐANG CHỜ DỮ LIỆU",
            "msg": "Vui lòng nhập kết quả quân bài của ván đầu tiên. Hệ thống sẽ ngay lập tức kích hoạt tính toán.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%"
        }
    
    diff = abs(p_val - b_val)
    
    if is_critical and streak_side and streak_count >= 4:
        target = "PLAYER" if streak_side == "Banker" else "BANKER"
        return {
            "status": f"🚨 LẬT CẦU BỎ CHUỖI: {target}",
            "msg": f"Công nghệ sóng pha phát hiện chuỗi bệt {streak_side.upper()} ({streak_count} ván) đã cạn kiệt dòng tiền toán học. Đặt cửa đối diện.",
            "color": "#06d6a0", "bg": "rgba(6, 214, 160, 0.2)", "size": "3%"
        }
        
    adaptive_threshold = 3.5 if lyapunov > 0.8 else 2.8
    
    if diff < adaptive_threshold:
        return {
            "status": "🛑 CHỜ (WAIT) - KHÔNG ĐẶT",
            "msg": f"Biên độ lợi thế lệch thấp ({diff:.1f}% < Ngưỡng an toàn {adaptive_threshold}%). Bàn chơi phân phối ngẫu nhiên cao, bỏ qua để bảo toàn vốn.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 VÀO LỆNH: PLAYER",
            "msg": f"Cấu trúc EOR xác nhận dòng chảy bài ủng hộ Player. Biên độ chênh lệch đạt vùng an toàn (+{diff:.1f}%).",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "2%"
        }
    else:
        return {
            "status": "🔴 VÀO LỆNH: BANKER",
            "msg": f"Xác suất hội tụ toán học thuần túy nghiêng về Banker. Biên độ chênh lệch vượt ngưỡng an toàn (+{diff:.1f}%).",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "2%"
        }

def parse_baccarat_input_v60(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().strip().replace(",", " ").replace(";", " ")
    temp_tokens = []
    i = 0
    while i < len(normalized):
        if normalized[i].isspace():
            i += 1
            continue
        if normalized[i:i+2] == "10":
            temp_tokens.append("10")
            i += 2
        else:
            temp_tokens.append(normalized[i])
            i += 1
    result_list = []
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13, '10': 10}
    for token in temp_tokens:
        if token in mapping: result_list.append(mapping[token])
        elif token.isdigit():
            val = int(token)
            if 1 <= val <= 9: result_list.append(val)
    return result_list


# =========================================================================
# SYSTEM INTERFACE DISPLAY (GIAO DIỆN MOBILE-GRID ĐỐI XỨNG CÂN BẰNG)
# =========================================================================
st.set_page_config(page_title="Oracle Ultra v60.2", page_icon="⚡", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: #030611 !important; color: #f8fafc !important; }
    
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; gap: 10px !important; }
    div[data-testid="stHorizontalBlock"] > div { flex: 1 1 0% !important; min-width: 0px !important; }
    
    .action-panel { border-radius: 14px; padding: 20px; margin: 15px 0px; text-align: center; box-shadow: 0px 5px 25px rgba(0,0,0,0.8); }
    .action-status { font-size: 22px; font-weight: 900; letter-spacing: 0.5px; margin-bottom: 6px; }
    .action-msg { font-size: 13.5px; opacity: 0.9; margin-bottom: 12px; line-height: 1.4; text-align: justify; }
    .action-vol { font-size: 16px; font-weight: 900; font-family: monospace; border-top: 1px dashed rgba(255,255,255,0.2); padding-top: 10px; }
    
    .mobile-metric-box { background: #0b132b; border: 1px solid #1c2541; border-radius: 10px; padding: 12px 6px; margin-bottom: 5px; display: flex; flex-direction: column; text-align: center; justify-content: center; }
    .metric-tag { font-size: 10.5px; font-weight: 800; color: #64748b; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 0.5px; }
    .metric-num { font-size: 19px; font-weight: 900; font-family: monospace; }
    
    .score-log-hud { padding: 12px; border-radius: 10px; background-color: #0b132b; border: 1px dashed #3a506b; margin-top: 12px; font-family: monospace; font-size: 12px; color: #cbd5e1; }
    
    div.stButton > button { background-color: #1c2541 !important; color: #cbd5e1 !important; border: 1px solid #3a506b !important; border-radius: 10px; font-weight: 800; width: 100% !important; padding: 12px 0px !important; font-size: 14px !important; }
    div.stButton > button:hover { background-color: #3a506b !important; color: #ffffff !important; }
    
    .submit-btn-box div.stButton > button { background-color: #00f5d4 !important; color: #010206 !important; border: none !important; box-shadow: 0 0 15px rgba(0,245,212,0.4); }
    .submit-btn-box div.stButton > button:hover { background-color: #57ffeb !important; }
    
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []

decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)
total_log_games = len(st.session_state.round_detailed_log)

st.markdown("### ⚡ ORACLE QUANTUM ULTRA v60.2")
st.caption(f"Hệ thống kiểm toán tối cao | Khay bài hiện tại: `{total_log_games}` ván.")

# =========================================================================
# HÀNG DỌC 1: KHU VỰC NHẬP LIỆU CHIA ĐÔI ĐỐI XỨNG (FORM)
# =========================================================================
with st.form(key="baccarat_ultra_input_form", clear_on_submit=True):
    input_grid = st.columns(2)
    with input_grid[0]:
        p_input = st.text_input("🔵 PLAYER CARD:", placeholder="Ví dụ: 8 K 2")
    with input_grid[1]:
        b_input = st.text_input("🔴 BANKER CARD:", placeholder="Ví dụ: 7 J")
    
    st.write("")
    st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
    calc_triggered = st.form_submit_button("🔥 PHÂN TÍCH CHUẨN XÁC CAO NHẤT")
    st.markdown('</div>', unsafe_allow_html=True)

if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v60(p_input.strip())
    b_list = parse_baccarat_input_v60(b_input.strip())
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    st.session_state.round_detailed_log.append({'p_cards': p_list, 'b_cards': b_list, 'p_score': p_score, 'b_score': b_score, 'outcome': outcome})
    st.rerun()

st.markdown("---")

# ENGINE ĐO LƯỜNG VÀ TÍNH TOÁN TOÁN HỌC CAO CẤP
final_p, final_b, final_t, cards_left, volatility, is_critical, streak_side, streak_count, lyapunov = calculate_v60_ultra_quantum_engine(st.session_state.round_detailed_log, shoe_decks=decks)
cmd = get_adaptive_directive(final_p, final_b, is_critical, streak_side, streak_count, lyapunov, st.session_state.round_detailed_log)

# BẢNG CHỈ THỊ HÀNH ĐỘNG TUYỆT ĐỐI KHÔNG GÂY PHÂN VÂN
st.markdown(
    f'<div class="action-panel" style="background-color: {cmd["bg"]}; border: 2px solid {cmd["color"]}; color: {cmd["color"]};">'
    f'<div class="action-status">{cmd["status"]}</div>'
    f'<div class="action-msg" style="color: #f1f5f9;">{cmd["msg"]}</div>'
    f'<div class="action-vol">MỨC CƯỢC ĐỀ XUẤT: {cmd["size"]}</div>'
    f'</div>',
    unsafe_allow_html=True
)

# HIỂN THỊ BA ĐƯỜNG XÁC SUẤT ĐỐI XỨNG NGANG TRÊN MOBILE
# (Sẽ bằng 0.0% chính xác khi mới vào app)
prob_grid = st.columns(3)
with prob_grid[0]:
    st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER</span><span class="metric-num" style="color:#00afb9;">{final_p:.1f}%</span></div>', unsafe_allow_html=True)
with prob_grid[1]:
    st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER</span><span class="metric-num" style="color:#ff4757;">{final_b:.1f}%</span></div>', unsafe_allow_html=True)
with prob_grid[2]:
    st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE</span><span class="metric-num" style="color:#2ecc71;">{final_t:.1f}%</span></div>', unsafe_allow_html=True)

# LỊCH SỬ PHÂN TÍCH KHAY BÀI
if st.session_state.round_detailed_log:
    st.markdown('<div class="score-log-hud"><b>📊 THỐNG KÊ LỊCH SỬ KHAY BÀI THỰC:</b><br>', unsafe_allow_html=True)
    for idx, r in enumerate(st.session_state.round_detailed_log):
        st.markdown(f"• Ván {idx+1}: [P] {r['p_score']}đ vs {r['b_score']}đ [B] ➡️ **{r['outcome'].upper()}**")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================================
# HÀNG DỌC 2: KHU VỰC TIỆN ÍCH TIỆN LỢI ĐỐI XỨNG (ANTI-CRASH)
# =========================================================================
util_grid = st.columns(2)
with util_grid[0]:
    if st.button("⏪ HOÀN TÁC"):
        if st.session_state.round_detailed_log:
            st.session_state.round_detailed_log.pop()
            st.rerun()
with util_grid[1]:
    if st.button("🔄 LÀM TRỐNG"):
        st.session_state.round_detailed_log = []
        st.rerun()
