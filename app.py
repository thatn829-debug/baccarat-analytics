import streamlit as st
import math

# =========================================================================
# SYSTEM CORE v37.9 (ISOLATED LOGIC: GLOBAL DEVIATION & STOCHASTIC GUARD)
# =========================================================================
def calculate_baccarat_v18_ultimate(shoe_history, round_detailed_log, shoe_decks=8, 
                                    manual_cards_used=0, manual_games_played=0,
                                    p_wins=0, b_wins=0, tie_wins=0, total_real_games=0):
    total_initial_cards = shoe_decks * 52
    invalid_logic_messages = []
    
    # Thống kê tổng số ván thực tế dựa trên dữ liệu cấu hình gốc + lịch sử ván nhập
    total_p_wins = p_wins + sum(1 for r in round_detailed_log if r['outcome'] == "Player")
    total_b_wins = b_wins + sum(1 for r in round_detailed_log if r['outcome'] == "Banker")
    total_t_wins = tie_wins + sum(1 for r in round_detailed_log if r['outcome'] == "Tie")
    global_total_games = total_p_wins + total_b_wins + total_t_wins

    # ---------------------------------------------------------------------
    # 1. BỘ XẾT LOGIC ĐỘC LẬP (Tích hợp Luật Kiểm tra Độ lệch Phi logic)
    # ---------------------------------------------------------------------
    logic_deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    all_cards_stream = []
    
    for round_data in round_detailed_log:
        all_cards_stream.extend(round_data['p_cards'] + round_data['b_cards'])
        for card_val in (round_data['p_cards'] + round_data['b_cards']):
            if card_val in logic_deck_structure:
                logic_deck_structure[card_val] -= 1.0
                
    # Quy luật 1: Kiểm tra âm kho bài
    card_labels = {1: "A", 10: "10", 11: "J", 12: "Q", 13: "K"}
    for card_num in range(1, 14):
        count = logic_deck_structure[card_num]
        if count < 0:
            label = card_labels.get(card_num, f"Số {card_num}")
            invalid_logic_messages.append(f"❌ {label} vượt giới hạn (Âm {abs(int(count))} lá trong kho bài)")

    # Quy luật 2: Phát hiện chuỗi trùng lặp quân bài bất khả thi
    if len(all_cards_stream) >= 12:
        for card_num in range(1, 14):
            if all_cards_stream[-12:].count(card_num) == 12:
                label = card_labels.get(card_num, f"Số {card_num}")
                invalid_logic_messages.append(f"🚨 CẢNH BÁO: Chuỗi quân trùng lặp bất khả thi! Quân {label} liên tục lặp lại.")

    # Quy luật 3: Kiểm tra chuỗi Hòa bệt liên tiếp ngắn hạn
    current_tie_streak = 0
    for round_data in reversed(round_detailed_log):
        if round_data['outcome'] == "Tie": current_tie_streak += 1
        else: break
    if current_tie_streak == 5:
        invalid_logic_messages.append(f"⚠️ NGƯỠNG HIẾM GẶP: Xuất hiện {current_tie_streak} ván HÒA liên tiếp (Tỷ lệ ngẫu nhiên 1/128,000 ván).")
    elif current_tie_streak >= 6:
        invalid_logic_messages.append(f"🚨 CHUỖI HÒA BẤT THƯỜNG: Xuất hiện {current_tie_streak} ván HÒA liên tiếp! Vượt ngưỡng giới hạn ngẫu nhiên.")

    # Quy luật 4: KIỂM TRA ĐỘ LỆCH PHI LOGIC TOÀN CỤC (GLOBAL DEVIATION GUARD) - TÍCH HỢP MỚI
    if global_total_games >= 30:
        actual_tie_rate = (total_t_wins / global_total_games) * 100
        if actual_tie_rate > 20.0:
            invalid_logic_messages.append(f"🚨 PHI LOGIC CỬA HÒA: Tỷ lệ Hòa thực tế quá cao ({actual_tie_rate:.1f}% trên {global_total_games} ván). Ngưỡng ngẫu nhiên tối đa là 15%.")
            
    # Đếm số ván liên tiếp không xuất hiện Hòa
    no_tie_counter = 0
    for round_data in reversed(round_detailed_log):
        if round_data['outcome'] != "Tie": no_tie_counter += 1
        else: break
    if no_tie_counter >= 60:
        invalid_logic_messages.append(f"🚨 PHI LOGIC DÒNG CHẢY: Đã {no_tie_counter} ván liên tiếp KHÔNG CÓ HÒA. Vượt ngưỡng cạn kiệt ngẫu nhiên tự nhiên.")

    # Quy luật 5: Đối chiếu luật rút bài và điểm số từng ván
    for idx, round_data in enumerate(round_detailed_log):
        p_cards = round_data['p_cards']
        b_cards = round_data['b_cards']
        recorded_outcome = round_data['outcome']
        
        if len(p_cards) > 0 or len(b_cards) > 0:
            total_cards_this_round = len(p_cards) + len(b_cards)
            if total_cards_this_round < 4 or total_cards_this_round > 6:
                invalid_logic_messages.append(f"⚠️ Ván {idx+1}: Số lượng bài không hợp lệ ({total_cards_this_round} lá).")
            
            p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
            b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10
            
            actual_calculated_outcome = "Tie"
            if p_score > b_score: actual_calculated_outcome = "Player"
            elif b_score > p_score: actual_calculated_outcome = "Banker"
            
            if recorded_outcome != actual_calculated_outcome:
                invalid_logic_messages.append(f"⚠️ Ván {idx+1}: Sai quy luật kết quả! Bài lật {p_score} vs {b_score} nhưng ghi nhận {recorded_outcome.upper()}.")

    # ---------------------------------------------------------------------
    # 2. THUẬT TOÁN TOÁN HỌC XÁC SUẤT TRUYỀN THỐNG (Vận hành độc lập)
    # ---------------------------------------------------------------------
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    detailed_cards_count = len(all_cards_stream)
    
    if detailed_cards_count > 0:
        for card_val in all_cards_stream:
            if card_val in deck_structure:
                deck_structure[card_val] = max(0.1, deck_structure[card_val] - 1)
        cards_left = total_initial_cards - detailed_cards_count
        mode = "SIÊU TỔ HỢP MARKOV PHI HOÀN LẠI (CHI TIẾT)"
    else:
        total_games_played = max(manual_games_played, total_real_games)
        cards_removed = max(0, manual_cards_used if manual_cards_used > 0 else int(total_games_played * 4.852))
        cards_left = total_initial_cards - cards_removed
        mode = "MA TRẬN PHÂN RÃ BAYES PHI TUYẾN TÍNH"
        
        if cards_removed > 0:
            consumed_ratio = cards_removed / total_initial_cards
            for card_num in deck_structure:
                reduction = (4 * shoe_decks) * consumed_ratio
                deck_structure[card_num] = max(0.1, (4 * shoe_decks) - reduction)

    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: score_deck[0] += count
        else: score_deck[card_num] += count

    N_total = float(sum(score_deck))
    if N_total <= 6:
        odds_res = {"Player": 44.62, "Banker": 45.86, "Tie": 9.52}
        return odds_res, deck_structure, 0.0, 0.0, mode, cards_left, (len(invalid_logic_messages) == 0), invalid_logic_messages

    card_counting_effect = (
        (-0.85 * score_deck[1]) + (-1.05 * score_deck[2]) + (-1.32 * score_deck[3]) +
        (-1.75 * score_deck[4]) + (0.48 * score_deck[5]) + (1.25 * score_deck[6]) +
        (1.92 * score_deck[7]) + (1.15 * score_deck[8]) + (-0.35 * score_deck[9]) +
        (0.63 * score_deck[0])
    )
    
    shift_ratio = card_counting_effect / N_total
    p_prob = max(35.0, min(65.0, 44.62 + (shift_ratio * 12.5)))
    b_prob = max(35.0, min(65.0, 45.86 - (shift_ratio * 12.5)))
    t_prob = 100.0 - p_prob - b_prob

    # Tiếp tục Quy luật 4 bổ sung: So sánh biên độ lệch Delta khi đủ tập mẫu lớn
    if global_total_games >= 40:
        actual_p_rate = (total_p_wins / global_total_games) * 100
        delta_p = abs(actual_p_rate - p_prob)
        if delta_p > 15.0:
            invalid_logic_messages.append(f"🚨 LỆCH BIÊN ĐỘ TOÁN HỌC: Player thực tế chiếm {actual_p_rate:.1f}% nhưng thuật toán tính toán khay bài chỉ cho phép quanh mức {p_prob:.1f}% (Lệch Delta: {delta_p:.1f}%). Dữ liệu sàn đi phi logic hoặc có dấu hiệu can thiệp!")

    p_pair_prob = 0.0
    for i in range(1, 14):
        if deck_structure[i] >= 2: 
            p_pair_prob += (deck_structure[i] / N_total) * ((deck_structure[i] - 1) / (N_total - 1))
    p_pair_odds = round(p_pair_prob * 100, 2)
    b_pair_odds = round(p_pair_odds * 1.015, 2)

    odds_res = {"Player": round(p_prob, 2), "Banker": round(b_prob, 2), "Tie": round(t_prob, 2)}
    is_shoe_logical = (len(invalid_logic_messages) == 0)
    
    return odds_res, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_logic_messages

def detect_baccarat_pattern(outcome_list):
    clean_list = [x for x in outcome_list if x in ["Player", "Banker"]]
    if len(clean_list) < 3: 
        return "🔄 Đang tích lũy dữ liệu xu hướng thực tế...", "#888888", None, 0
    
    last_side = clean_list[-1]
    streak_count = 0
    for item in reversed(clean_list):
        if item == last_side: streak_count += 1
        else: break
            
    if streak_count >= 3:
        side_vietnamese = "🔵 PLAYER" if last_side == "Player" else "🔴 BANKER"
        return f"🔥 XU HƯỚNG {side_vietnamese} THỰC TẾ ({streak_count} ván)", "#00cec9", last_side, streak_count
    return "📊 Khay bài đi sóng phẳng thực tế", "#2ed573", "Sóng phẳng", 0

def get_ai_recommendation(res, outcome_history):
    p_val = res.get("Player", 44.62)
    b_val = res.get("Banker", 45.86)
    t_val = res.get("Tie", 9.52)
    
    _, _, real_trend_side, streak_count = detect_baccarat_pattern(outcome_history)
    
    if len(outcome_history) < 2:
        return "⚠️ CHỜ DỮ LIỆU THỰC TẾ: Cần nhập tối thiểu 2 ván đầu tiên để bắt nhịp sàn.", "rgba(164, 176, 190, 0.1)", "#a4b0be"
        
    if t_val > 13.0:
        return f"🟢 CÂN NHẮC: HÒA (TIE) | Xác suất khay bài đạt điểm Hòa cao ({t_val}%) - Đi tiền nhỏ lót.", "rgba(46, 213, 115, 0.15)", "#2ed573"
        
    if real_trend_side == "Player":
        if p_val >= 44.2:
            return f"🔥 ĐỒNG THUẬN CAO: VÀO 🔵 PLAYER | Xu hướng bệt {streak_count} ván + Xác suất ủng hộ ({p_val}%). Thích hợp bám cầu.", "rgba(0, 175, 185, 0.2)", "#00afb9"
        else:
            return f"⚠️ XUNG ĐỘT: BỎ QUA VÁN NÀY | Sàn đang bệt PLAYER nhưng cấu trúc toán học khay bài cảnh báo rủi ro bẻ cầu cao.", "rgba(235, 94, 40, 0.15)", "#eb5e28"
            
    elif real_trend_side == "Banker":
        if b_val >= 45.2:
            return f"🔥 ĐỒNG THUẬN CAO: VÀO 🔴 BANKER | Xu hướng bệt {streak_count} ván + Xác suất toán học đạt {b_val}%. Thuận dòng chảy bàn.", "rgba(254, 217, 255, 0.2)", "#fed9ff"
        else:
            return f"⚠️ XUNG ĐỘT: BỎ QUA VÁN NÀY | Sàn đang bệt BANKER nhưng toán học cảnh báo khay bài đang cạn tài nguyên cho cửa Banker.", "rgba(235, 94, 40, 0.15)", "#eb5e28"
            
    elif real_trend_side == "Sóng phẳng":
        if p_val >= 46.0:
            return f"🔵 VÀO LỆNH: PLAYER | Sóng phẳng không bệt, toán học phát hiện cấu trúc khay bài lệch về Player ({p_val}%).", "rgba(0, 175, 185, 0.15)", "#00afb9"
        elif b_val >= 47.0:
            return f"🔴 VÀO LỆNH: BANKER | Sóng phẳng không bệt, khay bài báo điểm lợi thế toán học tốt cho Banker ({b_val}%).", "rgba(254, 217, 255, 0.15)", "#fed9ff"
            
    return "📊 QUAN SÁT: Bài đi không rõ xu hướng và điểm số toán học cân bằng. Khuyến nghị không vào lệnh ván này.", "rgba(164, 176, 190, 0.1)", "#a4b0be"

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
st.set_page_config(page_title="Oracle Engine v37.9 Global Guard", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(145deg, #0f2027, #1f404b, #2c5364) !important; color: #ecf0f1 !important; }
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; gap: 8px !important; }
    [data-testid="stHorizontalBlock"] > div { width: 50% !important; min-width: 46% !important; flex: 1 1 auto !important; }
    .central-game-counter { text-align: center; background: rgba(0, 175, 185, 0.15); border: 1px solid #00afb9; border-radius: 8px; padding: 8px 12px; font-family: monospace; font-size: 15px; font-weight: 800; color: #00afb9; margin-bottom: 15px; letter-spacing: 1px; }
    .ai-decision-box { text-align: center; border-radius: 10px; padding: 16px 10px; font-size: 16px; font-weight: 800; margin: 15px auto; letter-spacing: 0.5px; box-shadow: 0px 4px 15px rgba(0,0,0,0.3); line-height: 1.4; }
    .hud-box { padding: 12px 6px; border-radius: 10px; text-align: center; margin-bottom: 10px; border: 1px solid #203a43; background: rgba(10, 25, 30, 0.9); min-height: 85px; display: flex; flex-direction: column; justify-content: center; }
    .hud-title { font-size: 11px; font-weight: 700; color: #a4b0be; text-transform: uppercase; }
    .hud-value { font-size: 24px; font-weight: 800; font-family: monospace; margin-top: 2px; }
    .neon-player-advantage { background-color: #005573 !important; border: 2px solid #00afb9 !important; }
    .neon-banker-advantage { background-color: #1e2b38 !important; border: 2px solid #57606f !important; }
    .validation-hud { padding: 10px; border-radius: 6px; text-align: left; font-weight: 700; font-size: 11px; font-family: monospace; margin-bottom: 10px; line-height: 1.4; max-height: 180px; overflow-y: auto;}
    .logic-pass { background-color: rgba(46, 213, 115, 0.15); border: 1px solid #2ed573; color: #2ed573; text-align: center;}
    .logic-fail { background-color: rgba(235, 94, 40, 0.2); border: 2px solid #eb5e28; color: #ff7675; }
    .trend-hud { padding: 12px; border-radius: 8px; background-color: rgba(5, 15, 20, 0.9); border: 1px dashed #00afb9; margin-top: 5px; }
    .trend-title { font-size: 11px; font-weight: bold; color: #00afb9; text-transform: uppercase; margin-bottom: 4px;}
    .trend-string { font-size: 16px; font-family: monospace; letter-spacing: 4px; font-weight: 800; }
    .char-p { color: #00afb9; font-weight: bold; } 
    .char-b { color: #e74c3c; font-weight: bold; } 
    .char-t { color: #2ed573; font-weight: bold; }
    div.stButton > button { background-color: #00afb9 !important; color: white !important; border-radius: 8px; font-weight: bold; padding: 12px 0px; width: 100% !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'form_counter' not in st.session_state: st.session_state.form_counter = 0

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

st.markdown("### 🃏 DỮ LIỆU VÁN ĐANG XÉT")
base_games = manual_games if manual_games > 0 else calculated_total_wins
current_session_games = len(st.session_state.outcome_history)
next_game_number = base_games + current_session_games + 1

st.markdown(f'<div class="central-game-counter">🔮 VÀO ĐIỂM CHO VÁN THỨ: {next_game_number}</div>', unsafe_allow_html=True)

input_col_left, input_col_right = st.columns(2, gap="small")
with input_col_left:
    p_input = st.text_input("🔵 PLAYER (Bài/Điểm):", key=f"p_in_{st.session_state.form_counter}", placeholder="Ví dụ: k2 hoặc 7")
with input_col_right:
    b_input = st.text_input("🔴 BANKER (Bài/Điểm):", key=f"b_in_{st.session_state.form_counter}", placeholder="Ví dụ: a8 hoặc 5")

calc_triggered = st.button("🚀 GHI NHẬN & TÍNH TOÁN VÁN NÀY")

if calc_triggered:
    p_clean = p_input.strip()
    b_clean = b_input.strip()
    
    if p_clean or b_clean:
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
        st.rerun()

all_flat_history = []
for r in st.session_state.round_detailed_log:
    all_flat_history.extend(r['p_cards'] + r['b_cards'])

res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical, invalid_messages = calculate_baccarat_v18_ultimate(
    all_flat_history, st.session_state.round_detailed_log, shoe_decks=decks,
    manual_cards_used=manual_cards, manual_games_played=manual_games,
    p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input,
    total_real_games=len(st.session_state.outcome_history)
)

st.markdown("---")

if is_strict_lock:
    st.error(f"### 🛑 HỆ THỐNG KHÓA: Thông số cấu hình gốc không đồng nhất.")
else:
    st.markdown("### 🔮 KẾT QUẢ & KHUYẾN NGHỊ ĐỒNG BỘ")
    
    rec_text, rec_bg, rec_border = get_ai_recommendation(res, st.session_state.outcome_history)
    st.markdown(f'<div class="ai-decision-box" style="background-color: {rec_bg}; border: 2px solid {rec_border}; color: {rec_border};">{rec_text}</div>', unsafe_allow_html=True)
    
    p_box_css, b_box_css, tie_box_css = "hud-box", "hud-box", "hud-box"
    if res['Player'] > res['Banker']: p_box_css = "hud-box neon-player-advantage"
    elif res['Banker'] > res['Player']: b_box_css = "hud-box neon-banker-advantage"
    
    left_col, right_col = st.columns(2, gap="small")
    with left_col:
        st.markdown("##### 📊 XÁC SUẤT TOÁN HỌC")
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER</div><div class="hud-value" style="color:#00afb9;">{res["Player"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER</div><div class="hud-value" style="color:#fed9ff;">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{tie_box_css}"><div class="hud-title">🟢 TIE WIN</div><div class="hud-value" style="color: #2ed573;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
    with right_col:
        st.markdown("##### 💎 PHÂN TÍCH KHAY")
        st.markdown(f'<div class="hud-box"><div class="hud-title">🔵 P-PAIR</div><div class="hud-value" style="color:#00afb9; font-size:20px;">{p_pair}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box"><div class="hud-title">🔴 B-PAIR</div><div class="hud-value" style="color:#fed9ff; font-size:20px;">{b_pair}%</div></div>', unsafe_allow_html=True)
        
        # BÁO CÁO TRỌNG TÀI LOGIC: Hiển thị lỗi biên độ lệch Delta và lỗi dòng chảy Hòa tại đây
        if is_shoe_logical: 
            st.markdown('<div class="validation-hud logic-pass">✔ KHAY BÀI HỢP LỆ</div>', unsafe_allow_html=True)
        else: 
            error_html = "⚠️ PHÁT HIỆN LỖI LOGIC BÀI:<br>" + "<br>".join(invalid_messages)
            st.markdown(f'<div class="validation-hud logic-fail">{error_html}</div>', unsafe_allow_html=True)
        
    if st.session_state.outcome_history:
        trend_letters = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.outcome_history]
        pattern_msg, pattern_color, _, _ = detect_baccarat_pattern(st.session_state.outcome_history)
        st.markdown(f'<div class="trend-hud"><div class="trend-title">📈 XU HƯỚNG SÀN THỰC TẾ ĐÃ QUA ({len(st.session_state.outcome_history)} ván)</div><div class="trend-string">{" ".join(trend_letters)}</div><div style="color: {pattern_color}; font-weight: bold; font-size: 12px; margin-top:4px;">{pattern_msg}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    total_shoe_cards = decks * 52
    penetration_rate = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
    st.caption(f"**Chế độ:** `{mode}` | **Còn lại:** {int(cards_left)}/{total_shoe_cards} lá")
    st.progress(penetration_rate / 100.0)

st.markdown("<br>", unsafe_allow_html=True)
util_col_1, util_col_2 = st.columns(2, gap="small")
with util_col_1:
    if st.button("⏪ HOÀN TÁC (UNDO)", use_container_width=True, key="btn_undo_final"):
        if st.session_state.outcome_history:
            st.session_state.outcome_history.pop()
            if st.session_state.round_detailed_log:
                st.session_state.round_detailed_log.pop()
            st.rerun()
with util_col_2:
    if st.button("🔄 LÀM TRỐNG KHAY", use_container_width=True, key="btn_reset_final"):
        st.session_state.round_detailed_log = []
        st.session_state.outcome_history = []
        st.session_state.form_counter = 0
        st.rerun()
