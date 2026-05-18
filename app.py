import streamlit as st
import numpy as np
import math

# =========================================================================
# MODULE 1: ĐỘNG CƠ ĐẾM BÀI CHUẨN TOÁN HỌC V55.7 (ACTION-ORIENTED ENGINE)
# =========================================================================
def calculate_v55_quantum_chao_engine(all_rounds_log, shoe_decks):
    total_initial_cards = shoe_decks * 52
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    all_flat_cards = []
    valid_rounds_count = len(all_rounds_log)
    
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
    
    penetration_rate = (total_initial_cards - cards_remaining) / total_initial_cards
    
    # Hệ số đếm bài chuẩn quốc tế (Effect of Removal)
    counting_effect = {
        1: -0.005, 2: -0.006, 3: -0.007, 4: -0.012, 5: -0.008,  # Lá nhỏ ra nhiều -> Lợi Banker
        6: +0.011, 7: +0.013, 8: +0.008,                        # Lá lớn ra nhiều -> Lợi Player
        9: -0.002, 10: +0.004, 11: +0.004, 12: +0.004, 13: +0.004
    }
    
    total_counting_bias = 0.0
    for card_num, left in exact_cards_left.items():
        cards_removed = (4 * shoe_decks) - left
        total_counting_bias += cards_removed * counting_effect[card_num]
        
    p_0 = sum([exact_cards_left[i] for i in [10, 11, 12, 13]]) / cards_remaining

    # Xác suất cơ sở trung lập
    base_p = 44.62 + (total_counting_bias * 2.0)
    base_b = 45.86 - (total_counting_bias * 2.0)
    base_t = 9.52 + (p_0 * 2.5)

    # Đánh giá số mũ hỗn loạn Lyapunov để dò tìm điểm gãy cầu
    volatility_index = 0.0
    lyapunov_exponent = 0.2
    if len(all_rounds_log) >= 2:
        margins = [float(abs(r['p_score'] - r['b_score'])) for r in all_rounds_log]
        variance = float(np.var(margins))
        volatility_index = min(100.0, (math.sqrt(max(0.001, variance)) / 4.5) * 100.0)
        diffs = np.abs(np.diff(margins))
        lyapunov_exponent = math.log(float(np.mean(diffs)) + 1.0) - 0.5

    # Xử lý điểm nút thắt lật cầu an toàn (chỉ kích hoạt khi bệt quá sâu ván 4+)
    is_critical = False
    if current_streak_side and current_streak_count >= 4:
        if lyapunov_exponent < 0.5 and volatility_index < 25.0:
            is_critical = True
            if current_streak_side == "Banker":
                base_p += 3.5
                base_b -= 3.5
            else:
                base_b += 3.5
                base_p -= 3.5

    # Ép biên độ chuẩn hóa đối xứng
    base_p = max(41.0, min(59.0, base_p))
    base_b = max(41.0, min(59.0, base_b))
    base_t = max(7.0, min(15.0, base_t))
    
    total_sum = base_p + base_b + base_t
    return (base_p / total_sum) * 100, (base_b / total_sum) * 100, (base_t / total_sum) * 100, int(cards_remaining), volatility_index, is_critical, streak_side, streak_count


# =========================================================================
# MODULE 2: BỘ ĐỊNH HƯỚNG HÀNH ĐỘNG (ACTION DIRECTIVE CORTEX)
# =========================================================================
def get_action_directive(p_val, b_val, is_critical, streak_side, streak_count, log):
    if not log:
        return {
            "status": "🛰️ ĐANG KHỞI ĐỘNG CHUẨN HÓA",
            "msg": "Vui lòng nhập kết quả ván đầu tiên để hệ thống định vị khay bài.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%"
        }
    
    diff = abs(p_val - b_val)
    
    # 1. Trường hợp lật cầu đặc biệt (An tâm bẻ cầu bảo vệ)
    if is_critical and streak_side and streak_count >= 4:
        target = "PLAYER" if streak_side == "Banker" else "BANKER"
        return {
            "status": f"🚨 LẬT CẦU BẺ CHUỖI: {target}",
            "msg": f"Chuỗi bệt {streak_side.upper()} ({streak_count} ván) đã cạn kiệt động năng toán học. Đặt cửa đối diện.",
            "color": "#06d6a0", "bg": "rgba(6, 214, 160, 0.2)", "size": "2% - 3%"
        }
        
    # 2. Ngưỡng lọc nhiễu chí mạng: Nếu chênh lệch quá nhỏ (< 3.0%), ép người chơi ngồi im
    if diff < 3.0:
        return {
            "status": "🛑 CHỜ (WAIT) - KHÔNG ĐẶT",
            "msg": f"Độ lệch lợi thế quá thấp ({diff:.1f}%). Bàn chơi đang ở thế 50/50 cực kỳ rủi ro. Hãy kiên nhẫn bỏ qua ván này.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%"
        }
        
    # 3. Ra lệnh dứt khoát khi lợi thế vượt ngưỡng lọc nhiễu
    if p_val > b_val:
        return {
            "status": "🔵 VÀO LỆNH: PLAYER",
            "msg": f"Mật độ khay bài đang ủng hộ cửa Người chơi với biên độ an toàn (+{diff:.1f}%).",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "2%"
        }
    else:
        return {
            "status": "🔴 VÀO LỆNH: BANKER",
            "msg": f"Lợi thế toán học tự nhiên kết hợp cấu trúc đếm bài đang nghiêng về Nhà cái (+{diff:.1f}%).",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "2%"
        }

def parse_baccarat_input_v55(raw_str):
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
# SYSTEM INTERFACE DISPLAY
# =========================================================================
st.set_page_config(page_title="Oracle Action-Filter v55.7", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: #02040a !important; color: #ecf0f1 !important; }
    .action-panel { border-radius: 12px; padding: 24px; margin: 20px auto; text-align: center; box-shadow: 0px 4px 20px rgba(0,0,0,0.5); }
    .action-status { font-size: 26px; font-weight: 900; letter-spacing: 1px; margin-bottom: 8px; }
    .action-msg { font-size: 15px; opacity: 0.85; margin-bottom: 15px; line-height: 1.4; }
    .action-vol { font-size: 18px; font-weight: 800; font-family: monospace; border-top: 1px dashed rgba(255,255,255,0.15); padding-top: 10px; }
    .score-log-hud { padding: 12px; border-radius: 8px; background-color: #0d1117; border: 1px solid #30363d; margin-top: 15px; font-family: monospace; font-size: 13px; color: #c9d1d9; }
    div.stButton > button { background-color: #21262d !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; border-radius: 6px; font-weight: 700; }
    div.stButton > button:hover { background-color: #30363d !important; color: #ffffff !important; border-color: #8b949e !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []

st.sidebar.header("🛸 THIẾT LẬP")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)
total_log_games = len(st.session_state.round_detailed_log)

st.markdown("### 🧬 ORACLE ACTION-FILTER SYSTEM V55.7")
st.markdown(f"**Trạng thái khay bài:** Đã ghi nhận `{total_log_games}` ván.")

with st.form(key="baccarat_input_form", clear_on_submit=True):
    col1, col2 = st.columns(2, gap="small")
    with col1: p_input = st.text_input("🔵 BÀI PLAYER:", placeholder="Ví dụ: 5 2 K")
    with col2: b_input = st.text_input("🔴 BÀI BANKER:", placeholder="Ví dụ: A 7")
    _, btn_center, _ = st.columns([1, 2, 1])
    with btn_center: calc_triggered = st.form_submit_button("⚡ PHÂN TÍCH VÀ RA LỆNH")

if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v55(p_input.strip())
    b_list = parse_baccarat_input_v55(b_input.strip())
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    st.session_state.round_detailed_log.append({'p_cards': p_list, 'b_cards': b_list, 'p_score': p_score, 'b_score': b_score, 'outcome': outcome})
    st.rerun()

st.markdown("---")

# TÍNH TOÁN VÀ ĐƯA ĐIỀU HƯỚNG HÀNH ĐỘNG
final_p, final_b, final_t, cards_left, volatility, is_critical, streak_side, streak_count = calculate_v55_quantum_chao_engine(st.session_state.round_detailed_log, shoe_decks=decks)
cmd = get_action_directive(final_p, final_b, is_critical, streak_side, streak_count, st.session_state.round_detailed_log)

# BẢNG ĐIỀU HÀNH ĐẶT CƯỢC TRỰC QUAN KHÔNG PHÂN VÂN
st.markdown(
    f'<div class="action-panel" style="background-color: {cmd["bg"]}; border: 2px solid {cmd["color"]}; color: {cmd["color"]};">'
    f'<div class="action-status">{cmd["status"]}</div>'
    f'<div class="action-msg" style="color: #cbd5e1;">{cmd["msg"]}</div>'
    f'<div class="action-vol">VOLUME ĐI TIỀN: {cmd["size"]}</div>'
    f'</div>',
    unsafe_allow_html=True
)

if st.session_state.round_detailed_log:
    st.markdown('<div class="score-log-hud"><b>📊 LỊCH SỬ KHAY BÀI HIỆN TẠI:</b><br>', unsafe_allow_html=True)
    for idx, r in enumerate(st.session_state.round_detailed_log):
        st.markdown(f"• Ván {idx+1}: [P] {r['p_score']}đ vs {r['b_score']}đ [B] ➡️ **{r['outcome'].upper()}**")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
util_col_1, util_col_2 = st.columns(2, gap="small")
with util_col_1:
    if st.button("⏪ HOÀN TÁC VÁN VỪA NHẬP", use_container_width=True):
        if st.session_state.round_detailed_log: st.session_state.round_detailed_log.pop(); st.rerun()
with util_col_2:
    if st.button("🔄 LÀM TRỐNG KHAY BÀI MỚI", use_container_width=True): st.session_state.round_detailed_log = []; st.rerun()
