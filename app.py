import streamlit as st
import math

# =========================================================================
# MODULE 1: BỘ TRỌNG TÀI LOGIC (ĐỘC LẬP)
# =========================================================================
def verify_shoe_integrity(round_detailed_log, shoe_decks, global_total_games, total_t_wins, total_p_wins, p_prob):
    invalid_logic_messages = []
    
    # 1.1 Kiểm tra âm kho bài
    logic_deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    for round_data in round_detailed_log:
        for card_val in (round_data['p_cards'] + round_data['b_cards']):
            if card_val in logic_deck_structure:
                logic_deck_structure[card_val] -= 1.0
                
    card_labels = {1: "A", 10: "10", 11: "J", 12: "Q", 13: "K"}
    for card_num in range(1, 14):
        count = logic_deck_structure[card_num]
        if count < 0:
            label = card_labels.get(card_num, f"Số {card_num}")
            invalid_logic_messages.append(f"❌ {label} vượt giới hạn (Âm {abs(int(count))} lá trong kho bài)")

    # 1.2 Strict Snapshot Identity Guard
    if len(round_detailed_log) >= 2:
        identical_streak = 1
        for i in range(len(round_detailed_log) - 1, 0, -1):
            current_round = round_detailed_log[i]
            previous_round = round_detailed_log[i-1]
            
            curr_p = sorted([c for c in current_round['p_cards'] if c > 0])
            curr_b = sorted([c for c in current_round['b_cards'] if c > 0])
            prev_p = sorted([c for c in previous_round['p_cards'] if c > 0])
            prev_b = sorted([c for c in previous_round['b_cards'] if c > 0])
            
            is_p_duplicate = (curr_p == prev_p and len(curr_p) > 0)
            is_b_duplicate = (curr_b == prev_b and len(curr_b) > 0)
            is_cross_duplicate = (curr_p == prev_b and len(curr_p) > 0) or (curr_b == prev_p and len(curr_b) > 0)
            
            if is_p_duplicate or is_b_duplicate or is_cross_duplicate:
                identical_streak += 1
            else:
                break
                
        if identical_streak == 3:
            invalid_logic_messages.append(f"⚠️ SIÊU BIẾN DẠNG TRÙNG LẶP: Phát hiện {identical_streak} ván liên tiếp lật ra các quân bài thực tế giống hệt nhau!")
        elif identical_streak >= 4:
            invalid_logic_messages.append(f"🚨 LỖI PHI THỰC TẾ (KẸT VÒNG LẶP): Chuỗi {identical_streak} ván trùng khít hoàn toàn quân bài thực tế!")

    # 1.3 Kiểm tra chuỗi Hòa bệt liên tiếp
    current_tie_streak = 0
    for round_data in reversed(round_detailed_log):
        if round_data['outcome'] == "Tie": current_tie_streak += 1
        else: break
    if current_tie_streak >= 6:
        invalid_logic_messages.append(f"🚨 CHUỖI HÒA BẤT THƯỜNG: Xuất hiện {current_tie_streak} ván HÒA liên tiếp!")

    # 1.4 Kiểm tra tỷ lệ cửa Hòa hệ thống
    if global_total_games >= 30:
        actual_tie_rate = (total_t_wins / global_total_games) * 100
        if actual_tie_rate > 25.0:
            invalid_logic_messages.append(f"🚨 PHI LOGIC CỬA HÒA: Tỷ lệ Hòa thực tế quá cao ({actual_tie_rate:.1f}%).")
            
    # 1.5 Kiểm tra cạn kiệt dòng chảy Hòa
    no_tie_counter = 0
    for round_data in reversed(round_detailed_log):
        if round_data['outcome'] != "Tie": no_tie_counter += 1
        else: break
    if no_tie_counter >= 60:
        invalid_logic_messages.append(f"🚨 PHI LOGIC DÒNG CHẢY: Đã {no_tie_counter} ván liên tiếp KHÔNG CÓ HÒA.")

    # 1.6 Kiểm tra lệch biên độ Delta toán học
    if global_total_games >= 40:
        actual_p_rate = (total_p_wins / global_total_games) * 100
        delta_p = abs(actual_p_rate - p_prob)
        if delta_p > 20.0:
            invalid_logic_messages.append(f"🚨 LỆCH BIÊN ĐỘ TOÁN HỌC: Player chiếm {actual_p_rate:.1f}% nhưng khay bài báo {p_prob:.1f}% (Delta: {delta_p:.1f}%).")

    # 1.7 Đối chiếu luật tính điểm của sàn
    for idx, round_data in enumerate(round_detailed_log):
        p_cards = round_data['p_cards']
        b_cards = round_data['b_cards']
        if len(p_cards) > 0 or len(b_cards) > 0:
            p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
            b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10
            actual_calc = "Tie"
            if p_score > b_score: actual_calc = "Player"
            elif b_score > p_score: actual_calc = "Banker"
            if round_data['outcome'] != actual_calc:
                invalid_logic_messages.append(f"⚠️ Ván {idx+1}: Bài lật {p_score} vs {b_score} nhưng ghi nhận {round_data['outcome'].upper()}.")

    return invalid_logic_messages


# =========================================================================
# BỘ TRỢ LÝ TOÁN HỌC: TRÍCH XUẤT CẤU TRÚC KHAY BÀI THỜI GIAN THỰC
# =========================================================================
def get_current_shoe_state(all_cards_stream, shoe_decks, manual_cards_used, manual_games_played, total_real_games, t_wins, p_wins, b_wins):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    detailed_cards_count = len(all_cards_stream)
    
    global_games = max(manual_games_played, manual_games_played + total_real_games)
    estimated_cards_removed = int(global_games * 4.852)
    cards_removed = max(manual_cards_used, estimated_cards_removed)
    cards_left = total_initial_cards - max(detailed_cards_count, cards_removed)
    
    if global_games > 0:
        tie_ratio = t_wins / global_games
        p_ratio = p_wins / global_games
        b_ratio = b_wins / global_games
        
        if tie_ratio > 0.095:
            bonus_factor = 1.0 + (tie_ratio - 0.095) * 3.5
            deck_structure[10] *= bonus_factor
            deck_structure[11] *= bonus_factor
            deck_structure[12] *= bonus_factor
            deck_structure[13] *= bonus_factor
            
        if p_ratio > 0.55:
            for n in [2, 3, 4]: deck_structure[n] *= 1.15
        if b_ratio > 0.55:
            for n in [5, 6, 7]: deck_structure[n] *= 1.15

    if detailed_cards_count > 0:
        for card_val in all_cards_stream:
            if card_val in deck_structure:
                deck_structure[card_val] = max(0.01, deck_structure[card_val] - 1.0)
                
    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: score_deck[0] += count
        else: score_deck[card_num] += count
        
    return score_deck, sum(score_deck), cards_left


# =========================================================================
# MODULE 2: TÁCH ĐỘC LẬP TÍNH XÁC SUẤT (PLAYER - BANKER - TIE)
# =========================================================================

def calculate_player_probability(score_deck, N_total, global_games):
    """Module độc lập tính toán xác suất Player thắng dựa trên mật độ bài"""
    if global_games == 0 or N_total <= 6: return 44.62
    card_counting_effect = (
        (-0.85 * score_deck[1]) + (-1.05 * score_deck[2]) + (-1.32 * score_deck[3]) +
        (-1.75 * score_deck[4]) + (0.48 * score_deck[5]) + (1.25 * score_deck[6]) +
        (1.92 * score_deck[7]) + (1.15 * score_deck[8]) + (-0.35 * score_deck[9]) +
        (0.63 * score_deck[0])
    )
    shift_ratio = card_counting_effect / N_total
    return 44.62 + (shift_ratio * 13.5)


def calculate_banker_probability(score_deck, N_total, global_games):
    """Module độc lập tính toán xác suất Banker thắng dựa trên mật độ bài"""
    if global_games == 0 or N_total <= 6: return 45.86
    card_counting_effect = (
        (-0.85 * score_deck[1]) + (-1.05 * score_deck[2]) + (-1.32 * score_deck[3]) +
        (-1.75 * score_deck[4]) + (0.48 * score_deck[5]) + (1.25 * score_deck[6]) +
        (1.92 * score_deck[7]) + (1.15 * score_deck[8]) + (-0.35 * score_deck[9]) +
        (0.63 * score_deck[0])
    )
    shift_ratio = card_counting_effect / N_total
    return 45.86 - (shift_ratio * 13.5)


def calculate_tie_probability(score_deck, N_total, t_wins, global_games):
    """Module độc lập tính toán xác suất Hòa thích ứng sâu với thực tế sảnh"""
    if global_games == 0 or N_total <= 6: return 9.52
    base_t_prob = 9.52 + (score_deck[0] / N_total * 5.0)
    
    if global_games > 5:
        actual_tie_weight = t_wins / global_games
        return (base_t_prob * 0.6) + (actual_tie_weight * 100.0 * 0.4)
    return base_t_prob


# =========================================================================
# AUXILIARY FUNCTIONS & ADVANCED AI ENGINE
# =========================================================================
def detect_baccarat_pattern(outcome_list):
    clean_list = [x for x in outcome_list if x in ["Player", "Banker"]]
    if len(clean_list) < 3: return "🔄 Đang tích lũy dữ liệu xu hướng thực tế...", "#888888", None, 0
    last_side = clean_list[-1]
    streak_count = 0
    for item in reversed(clean_list):
        if item == last_side: streak_count += 1
        else: break
    if streak_count >= 3:
        side_vietnamese = "🔵 PLAYER" if last_side == "Player" else "🔴 BANKER"
        return f"🔥 XU HƯỚNG {side_vietnamese} THỰC TẾ ({streak_count} ván)", "#00cec9", last_side, streak_count
    return "📊 Khay bài đi sóng phẳng thực tế", "#2ed573", "Sóng phẳng", 0

def get_ai_recommendation_v2(p_val, b_val, t_val, outcome_history, round_detailed_log):
    _, _, real_trend_side, streak_count = detect_baccarat_pattern(outcome_history)
    
    if t_val > 14.0: 
        return f"🟢 CẦU BIẾN ĐỘNG - VÀO LỆNH HÒA (TIE): Xác suất thích ứng thực tế đạt {t_val}% (Bàn có tín hiệu bệt Hòa liên tục).", "rgba(46, 213, 115, 0.15)", "#2ed573"
        
    if len(outcome_history) < 2: 
        return "⚠️ CHỜ DỮ LIỆU THỰC TẾ: Cần nhập tối thiểu 2 ván đầu tiên để kích hoạt bộ lọc cầu.", "rgba(164, 176, 190, 0.1)", "#a4b0be"
    
    last_round = round_detailed_log[-1] if round_detailed_log else None
    last_p_cards = last_round['p_cards'] if last_round else []
    last_b_cards = last_round['b_cards'] if last_round else []
    last_p_score = sum([0 if c >= 10 else c for c in last_p_cards]) % 10 if last_p_cards else 0
    last_b_score = sum([0 if c >= 10 else c for c in last_b_cards]) % 10 if last_b_cards else 0

    if real_trend_side == "Player":
        if p_val >= 44.5: 
            return f"🔥 THUẬN CẦU XU HƯỚNG: ĐU THEO 🔵 PLAYER | Sàn đang bệt ({streak_count} ván) + Xác suất khay toán học ủng hộ giữ nền ({p_val}%).", "rgba(0, 175, 185, 0.2)", "#00afb9"
        else:
            if b_val >= 52.5 or (streak_count >= 5 and b_val >= 49.0):
                return f"⚡ LỆNH BẺ CẦU TOÁN HỌC: VÀO 🔴 BANKER | Phát hiện lệch khay cực đại! Toán học báo {b_val}%, kho bài cạn lá hỗ trợ Player, cầu bệt ván thứ {streak_count} sắp gãy.", "rgba(254, 217, 255, 0.25)", "#fed9ff"
            else:
                return f"🛡️ PHÒNG THỦ (SÀN ĐÈ TOÁN HỌC): TIẾP TỤC ĐU 🔵 PLAYER | Cầu bệt sàn ăn đứt tỷ lệ lệch nhẹ của toán học ({b_val}% chưa đủ lực bẻ).", "rgba(0, 175, 185, 0.15)", "#00afb9"

    elif real_trend_side == "Banker":
        if b_val >= 45.5: 
            return f"🔥 THUẬN CẦU XU HƯỚNG: ĐU THEO 🔴 BANKER | Sàn đang bệt ({streak_count} ván) + Xác suất toán học đạt chuẩn lợi thế cấu trúc ({b_val}%).", "rgba(254, 217, 255, 0.2)", "#fed9ff"
        else:
            if p_val >= 51.5 or (streak_count >= 5 and p_val >= 48.0):
                return f"⚡ LỆNH BẺ CẦU TOÁN HỌC: VÀO 🔵 PLAYER | Khay bài hết sạch lá Tây/Lá bù cho Banker. Toán học đạt {p_val}%, ép gãy cầu bệt thực tế ván thứ {streak_count}!", "rgba(0, 175, 185, 0.25)", "#00afb9"
            else:
                return f"🛡️ PHÒNG THỦ (SÀN ĐÈ TOÁN HỌC): TIẾP TỤC ĐU 🔴 BANKER | Xu hướng sàn lấn lướt toán học lệch nhẹ ({p_val}% chưa đủ lực gồng bẻ).", "rgba(254, 217, 255, 0.15)", "#fed9ff"

    elif real_trend_side == "Sóng phẳng":
        score_diff = abs(last_p_score - last_b_score)
        if p_val >= 46.5: 
            if score_diff <= 2 and last_b_score > last_p_score:
                return f"🔵 VÀO LỆNH CAO: PLAYER | Toán học báo lợi thế ({p_val}%) + Phản đòn điểm số thực tế ván trước (Banker thắng suýt soát).", "rgba(0, 175, 185, 0.2)", "#00afb9"
            return f"🔵 VÀO LỆNH: PLAYER | Cấu trúc khay bài nghiêng mạnh về cửa Player ({p_val}%).", "rgba(0, 175, 185, 0.15)", "#00afb9"
        elif b_val >= 47.5: 
            if score_diff <= 2 and last_p_score > last_b_score:
                return f"🔴 VÀO LỆNH CAO: BANKER | Lợi thế toán học ({b_val}%) + Điểm thực tế ép đổi cầu (Player ván trước ăn may nút thấp).", "rgba(254, 217, 255, 0.2)", "#fed9ff"
            return f"🔴 VÀO LỆNH: BANKER | Khay bài báo lợi thế toán học tốt cho Banker ({b_val}%).", "rgba(254, 217, 255, 0.15)", "#fed9ff"
            
    return "📊 QUAN SÁT TIẾP: Cầu nhiễu loạn, điểm số thực tế và xác suất triệt tiêu lẫn nhau. Không vào lệnh ván này.", "rgba(164, 176, 190, 0.1)", "#a4b0be"

def parse_baccarat_input_v37(raw_str):
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
st.set_page_config(page_title="Oracle Engine v40.1 Pure Balance", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(145deg, #0f2027, #1f404b, #2c5364) !important; color: #ecf0f1 !important; }
    
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
    }
    div[data-testid="stHorizontalBlock"] > div {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    .central-game-counter { text-align: center; background: rgba(0, 175, 185, 0.15); border: 1px solid #00afb9; border-radius: 8px; padding: 8px 12px; font-family: monospace; font-size: 15px; font-weight: 800; color: #00afb9; margin-bottom: 12px; }
    .ai-decision-box { text-align: center; border-radius: 10px; padding: 14px 10px; font-size: 15px; font-weight: 800; margin: 12px auto; box-shadow: 0px 4px 15px rgba(0,0,0,0.3); line-height: 1.4; }
    .hud-box { padding: 12px 4px; border-radius: 10px; text-align: center; margin-bottom: 8px; border: 1px solid #203a43; background: rgba(10, 25, 30, 0.9); min-height: 85px; display: flex; flex-direction: column; justify-content: center; }
    .hud-title { font-size: 11px; font-weight: 700; color: #a4b0be; text-transform: uppercase; }
    .hud-value { font-size: 26px; font-weight: 800; font-family: monospace; margin-top: 1px; }
    .neon-player-advantage { background-color: #005573 !important; border: 2px solid #00afb9 !important; }
    .neon-banker-advantage { background-color: #1e2b38 !important; border: 2px solid #e74c3c !important; }
    .validation-hud { padding: 8px; border-radius: 6px; text-align: left; font-weight: 700; font-size: 11px; font-family: monospace; margin-bottom: 10px; line-height: 1.4; max-height: 150px; overflow-y: auto;}
    .logic-pass { background-color: rgba(46, 213, 115, 0.15); border: 1px solid #2ed573; color: #2ed573; text-align: center;}
    .logic-warn { background-color: rgba(254, 202, 87, 0.15); border: 2px solid #feca57; color: #feca57; }
    .logic-fail { background-color: rgba(235, 94, 40, 0.2); border: 2px solid #eb5e28; color: #ff7675; }
    .table-switch-lock { background: linear-gradient(90deg, #ff416c, #ff4b2b); border: 3px solid #ffffff; border-radius: 12px; color: white !important; font-size: 16px; font-weight: 900; padding: 20px 12px; text-align: center; box-shadow: 0px 0px 20px #ff4b2b; margin: 15px 0px; letter-spacing: 0.5px; }
    .trend-hud { padding: 10px; border-radius: 8px; background-color: rgba(5, 15, 20, 0.9); border: 1px dashed #00afb9; margin-top: 5px; }
    .trend-title { font-size: 10px; font-weight: bold; color: #00afb9; text-transform: uppercase; margin-bottom: 4px;}
    .trend-string { font-size: 15px; font-family: monospace; letter-spacing: 3px; font-weight: 800; }
    .char-p { color: #00afb9; font-weight: bold; } 
    .char-b { color: #e74c3c; font-weight: bold; } 
    .char-t { color: #2ed573; font-weight: bold; }
    
    div.stButton > button { background-color: #00afb9 !important; color: white !important; border-radius: 8px; font-weight: bold; padding: 8px 0px; font-size: 14px !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'form_counter' not in st.session_state: st.session_state.form_counter = 0
if 'logic_fail_counter' not in st.session_state: st.session_state.logic_fail_counter = 0

if 'frozen_base_games' not in st.session_state: st.session_state.frozen_base_games = None
if 'session_added_games' not in st.session_state: st.session_state.session_added_games = 0

st.sidebar.header("⚙️ CẤU HÌNH KHAY BÀI")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.header("### 📊 THIẾT LẬP THÔNG SỐ GỐC")
manual_cards = st.sidebar.number_input("Số LÁ BÀI đã chia:", min_value=0, max_value=decks*52, value=0)
manual_games = st.sidebar.number_input("Tổng số ván đã chạy:", min_value=0, max_value=150, value=0)

p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0)

calculated_total_wins = p_wins_input + b_wins_input + tie_wins_input
is_strict_lock = (manual_games > 0 and calculated_total_wins > 0 and manual_games != calculated_total_wins)

live_base = manual_games if manual_games > 0 else calculated_total_wins

if st.session_state.frozen_base_games is None or st.session_state.session_added_games == 0:
    st.session_state.frozen_base_games = live_base

st.markdown("### 🃏 DỮ LIỆU VÁN ĐANG XÉT")
next_game_number = st.session_state.frozen_base_games + st.session_state.session_added_games

st.markdown(f'<div class="central-game-counter">🔮 VÀO ĐIỂM CHO VÁN THỨ: {next_game_number}</div>', unsafe_allow_html=True)

# Input UI
input_row_col1, input_row_col2 = st.columns(2, gap="small")
with input_row_col1:
    p_input = st.text_input("🔵 PLAYER:", key=f"p_in_{st.session_state.form_counter}", placeholder="k2 hoặc 7")
with input_row_col2:
    b_input = st.text_input("🔴 BANKER:", key=f"b_in_{st.session_state.form_counter}", placeholder="a8 hoặc 5")

st.write("")

btn_layout_l, btn_layout_center, btn_layout_r = st.columns([1, 4, 1], gap="small")
with btn_layout_center:
    calc_triggered = st.button("🚀 GHI NHẬN & TÍNH TOÁN", use_container_width=True)

if calc_triggered:
    p_clean = p_input.strip()
    b_clean = b_input.strip()
    
    if not p_clean and not b_clean:
        st.warning("⚠️ Vui lòng nhập điểm thực tế!")
    else:
        p_list = parse_baccarat_input_v37(p_clean)
        b_list = parse_baccarat_input_v37(b_clean)
        
        p_score_eval = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
        b_score_eval = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
        
        if len(p_clean) == 1 and p_clean.isdigit() and len(b_clean) == 1 and b_clean.isdigit():
            p_score_eval = int(p_clean)
            b_score_eval = int(b_clean)
            
        current_outcome = "Tie"
        if p_score_eval > b_score_eval: current_outcome = "Player"
        elif b_score_eval > p_score_eval: current_outcome = "Banker"
        
        st.session_state.round_detailed_log.append({
            'p_cards': p_list,
            'b_cards': b_list,
            'outcome': current_outcome
        })
        st.session_state.outcome_history.append(current_outcome)
        st.session_state.form_counter += 1
        st.session_state.session_added_games += 1  
        st.rerun()

all_flat_history = []
for r in st.session_state.round_detailed_log:
    all_flat_history.extend(r['p_cards'] + r['b_cards'])

total_p_wins = p_wins_input + sum(1 for r in st.session_state.round_detailed_log if r['outcome'] == "Player")
total_b_wins = b_wins_input + sum(1 for r in st.session_state.round_detailed_log if r['outcome'] == "Banker")
total_t_wins = tie_wins_input + sum(1 for r in st.session_state.round_detailed_log if r['outcome'] == "Tie")
global_total_games = total_p_wins + total_b_wins + total_t_wins

# BƯỚC THU THẬP TRẠNG THÁI KHAY BÀI CHUNG
score_deck, N_total, cards_left = get_current_shoe_state(
    all_flat_history, shoe_decks=decks, manual_cards_used=manual_cards, 
    manual_games_played=manual_games, total_real_games=len(st.session_state.outcome_history),
    t_wins=total_t_wins, p_wins=total_p_wins, b_wins=total_b_wins
)

# BƯỚC GỌI CÁC MODULE TOÁN HỌC ĐỘC LẬP
raw_p = calculate_player_probability(score_deck, N_total, global_total_games)
raw_b = calculate_banker_probability(score_deck, N_total, global_total_games)
raw_t = calculate_tie_probability(score_deck, N_total, total_t_wins, global_total_games)

# Đồng bộ hóa tổng biên để phân phối xác suất luôn chuẩn 100%
total_raw_sum = raw_p + raw_b + raw_t
final_p = round(max(20.0, min(70.0, (raw_p / total_raw_sum) * 100.0)), 2)
final_b = round(max(20.0, min(70.0, (raw_b / total_raw_sum) * 100.0)), 2)
final_t = round(100.0 - final_p - final_b, 2)

invalid_messages = verify_shoe_integrity(
    st.session_state.round_detailed_log, shoe_decks=decks, 
    global_total_games=global_total_games, total_t_wins=total_t_wins, 
    total_p_wins=total_p_wins, p_prob=final_p
)

st.session_state.logic_fail_counter = len(invalid_messages)

st.markdown("---")

if is_strict_lock:
    st.error(f"### 🛑 HỆ THỐNG KHÓA: Thông số cấu hình gốc không đồng nhất.")
else:
    if st.session_state.logic_fail_counter >= 3:
        st.markdown(
            f'<div class="table-switch-lock">'
            f'🚨 PHÁT HIỆN GIAN LẬN LIÊN TỤC: ĐỔI BÀN NGAY LẬP TỨC!<br>'
            f'<span style="font-size:12px; font-weight:normal;">Hệ thống phát hiện {st.session_state.logic_fail_counter} lỗi phi thực tế. '
            f'Bàn chơi bị bẻ cong hoàn toàn!</span>'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown("### 🔮 KẾT QUẢ & KHUYẾN NGHỊ ĐỒNG BỘ")
        
        rec_text, rec_bg, rec_border = get_ai_recommendation_v2(final_p, final_b, final_t, st.session_state.outcome_history, st.session_state.round_detailed_log)
        st.markdown(f'<div class="ai-decision-box" style="background-color: {rec_bg}; border: 2px solid {rec_border}; color: {rec_border};">{rec_text}</div>', unsafe_allow_html=True)
        
        p_box_css, b_box_css = "hud-box", "hud-box"
        if final_p > final_b: p_box_css = "hud-box neon-player-advantage"
        elif final_b > final_p: b_box_css = "hud-box neon-banker-advantage"
        
        col_p, col_b, col_t = st.columns(3, gap="small")
        with col_p:
            st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER</div><div class="hud-value" style="color:#00afb9;">{final_p}%</div></div>', unsafe_allow_html=True)
        with col_b:
            st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER</div><div class="hud-value" style="color:#ff4757;">{final_b}%</div></div>', unsafe_allow_html=True)
        with col_t:
            st.markdown(f'<div class="hud-box"><div class="hud-title">🟢 TIE WIN</div><div class="hud-value" style="color: #2ed573;">{final_t}%</div></div>', unsafe_allow_html=True)
            
        st.write("")
        if st.session_state.logic_fail_counter == 0: 
            st.markdown('<div class="validation-hud logic-pass">✔ KHAY BÀI HỢP LỆ THEO TIÊU CHUẨN TOÁN HỌC PHÂN RÃ</div>', unsafe_allow_html=True)
        elif st.session_state.logic_fail_counter == 1:
            error_html = "⚠️ CHÚ Ý BIẾN ĐỘNG BÀI:<br>" + "<br>".join(invalid_messages)
            st.markdown(f'<div class="validation-hud logic-warn">{error_html}</div>', unsafe_allow_html=True)
        else:
            error_html = f"🚨 BIẾN DẠNG NGUY HIỂM ({st.session_state.logic_fail_counter} lỗi):<br>" + "<br>".join(invalid_messages)
            st.markdown(f'<div class="validation-hud logic-fail">{error_html}</div>', unsafe_allow_html=True)
            
        if st.session_state.outcome_history:
            trend_letters = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.outcome_history]
            pattern_msg, pattern_color, _, _ = detect_baccarat_pattern(st.session_state.outcome_history)
            st.markdown(f'<div class="trend-hud"><div class="trend-title">📈 XU HƯỚNG SÀN THỰC TẾ ĐÃ QUA ({len(st.session_state.outcome_history)} ván)</div><div class="trend-string">{" ".join(trend_letters)}</div><div style="color: {pattern_color}; font-weight: bold; font-size: 12px; margin-top:4px;">{pattern_msg}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    total_shoe_cards = decks * 52
    penetration_rate = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
    st.caption(f"**Chế độ:** `ANTI-BIAS ENGINE (V40.1)` | **Còn lại:** {int(cards_left)}/{total_shoe_cards} lá")
    st.progress(penetration_rate / 100.0)

st.markdown("<br>", unsafe_allow_html=True)
util_col_1, util_col_2 = st.columns(2, gap="small")
with util_col_1:
    if st.button("⏪ HOÀN TÁC (UNDO)", use_container_width=True, key="btn_undo_final"):
        if st.session_state.outcome_history:
            st.session_state.outcome_history.pop()
            if st.session_state.round_detailed_log:
                st.session_state.round_detailed_log.pop()
            if st.session_state.session_added_games > 0:
                st.session_state.session_added_games -= 1
            st.rerun()
with util_col_2:
    if st.button("🔄 LÀM TRỐNG (ĐỔI BÀN)", use_container_width=True, key="btn_reset_final"):
        st.session_state.round_detailed_log = []
        st.session_state.outcome_history = []
        st.session_state.form_counter = 0
        st.session_state.logic_fail_counter = 0
        st.session_state.session_added_games = 0
        st.session_state.frozen_base_games = None  
        st.rerun()
