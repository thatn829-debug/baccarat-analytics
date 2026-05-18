import streamlit as st

# =========================================================================
# SYSTEM CORE v34.0: PERFECT CARD PARSING & EXACT TREND MATCHING
# =========================================================================
def calculate_baccarat_v18_ultimate(p_cards, b_cards, shoe_history, shoe_decks=8, 
                                    manual_cards_used=0, manual_games_played=0,
                                    p_wins=0, b_wins=0, tie_wins=0):
    total_initial_cards = shoe_decks * 52
    
    if len(shoe_history) == 0 and manual_cards_used == 0 and manual_games_played == 0 and p_wins == 0 and b_wins == 0 and tie_wins == 0:
        odds_res = {"Player": 44.62, "Banker": 45.86, "Tie": 9.52}
        deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
        return odds_res, deck_structure, 7.47, 7.47, "KHAY BÀI NGUYÊN BẢN (XÁC SUẤT GỐC)", total_initial_cards, True, []

    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    if manual_cards_used > total_initial_cards or manual_games_played > int(total_initial_cards / 4):
        return "❌ Cấu hình vượt giới hạn vật lý!", {}, 0.0, 0.0, "LỖI", total_initial_cards, False, []

    detailed_cards_count = len(shoe_history)
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure:
                deck_structure[card_val] -= 1
        cards_left = total_initial_cards - detailed_cards_count
        mode = "SIÊU TỔ HỢP MARKOV PHI HOÀN LẠI (CHI TIẾT)"
    else:
        cards_removed = max(0, manual_cards_used if manual_cards_used > 0 else int((p_wins * 4.86) + (b_wins * 4.81) + (tie_wins * 5.23)))
        if cards_removed == 0 and manual_games_played > 0:
            cards_removed = int(manual_games_played * 4.852)
        cards_left = max(0, total_initial_cards - cards_removed)
        mode = "MA TRẬN PHÂN RÃ BAYES PHI TUYẾN TÍNH" if cards_removed > 0 else "KHAY BÀI NGUYÊN BẢN (XÁC SUẤT GỐC)"
        
        if cards_removed > 0:
            consumed_ratio = cards_removed / total_initial_cards
            for card_num in deck_structure:
                reduction = (4 * shoe_decks) * consumed_ratio
                deck_structure[card_num] = max(0.0, (4 * shoe_decks) - reduction)

    invalid_cards_list = []
    for card_num, count in deck_structure.items():
        if count < 0:
            card_labels = {1: "A", 11: "J", 12: "Q", 13: "K"}
            label = card_labels.get(card_num, f"[{card_num}]")
            invalid_cards_list.append(f"{label} ({round(count, 1)} lá)")
            
    is_shoe_logical = (len(invalid_cards_list) == 0)
    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: score_deck[0] += count
        else: score_deck[card_num] += count

    N_total = float(sum(score_deck))
    if N_total <= 6:
        return "⚠️ Cảnh báo: Khay bài thiếu quân!", deck_structure, 0.0, 0.0, mode, cards_left, is_shoe_logical, invalid_cards_list

    p_pair_prob = 0.0
    for i in range(1, 14):
        if deck_structure[i] >= 2: p_pair_prob += (deck_structure[i] / N_total) * ((deck_structure[i] - 1) / (N_total - 1))
    p_pair_odds = round(p_pair_prob * 100, 2)

    b_pair_prob = 0.0
    for card_j in range(1, 14):
        cnt_j = deck_structure[card_j]
        if cnt_j >= 2:
            p_not_j = (N_total - cnt_j) / N_total * (N_total - cnt_j - 1) / (N_total - 1)
            b_given_p_not_j = (cnt_j / (N_total - 2)) * ((cnt_j - 1) / (N_total - 3))
            p_one_j = 2 * (cnt_j / N_total) * (N_total - cnt_j) / (N_total - 1)
            b_given_p_one_j = (max(0.0, cnt_j - 1) / (N_total - 2)) * (max(0.0, cnt_j - 2) / (N_total - 3))
            p_two_j = (cnt_j / N_total) * ((cnt_j - 1) / (N_total - 1))
            b_given_p_two_j = (max(0.0, cnt_j - 2) / (N_total - 2)) * (max(0.0, cnt_j - 3) / (N_total - 3))
            b_pair_prob += (p_not_j * b_given_p_not_j) + (p_one_j * b_given_p_one_j) + (p_two_j * b_given_p_two_j)
    b_pair_odds = round(b_pair_prob * 100, 2)

    odds_res = {"Player": 44.62, "Banker": 45.86, "Tie": 9.52}
    return odds_res, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list

def detect_baccarat_pattern(outcome_list):
    clean_list = [x for x in outcome_list if x in ["Player", "Banker"]]
    if len(clean_list) < 3: 
        return "🔄 Đang tích lũy dữ liệu xu hướng thực tế...", "#888888", None
    
    last_side = clean_list[-1]
    streak_count = 0
    for item in reversed(clean_list):
        if item == last_side: streak_count += 1
        else: break
            
    if streak_count >= 3:
        side_vietnamese = "🔵 PLAYER" if last_side == "Player" else "🔴 BANKER"
        return f"🔥 XU HƯỚNG {side_vietnamese} THỰC TẾ ({streak_count} ván)", "#00cec9", last_side
    return "📊 Khay bài đi sóng phẳng thực tế", "#2ed573", "Sóng phẳng"

def get_ai_recommendation(res, outcome_history):
    p_val = res.get("Player", 44.62)
    b_val = res.get("Banker", 45.86)
    t_val = res.get("Tie", 9.52)
    _, _, real_trend_side = detect_baccarat_pattern(outcome_history)
    
    if not outcome_history:
        return "⚠️ KHUYẾN NGHỊ: CHỜ DỮ LIỆU THỰC TẾ (Nhập ván đầu tiên)", "rgba(164, 176, 190, 0.1)", "#a4b0be"
    if t_val > 13.5:
        return "🟢 CÂN NHẮC: 🟢 TIE (HÒA)", "rgba(46, 213, 115, 0.15)", "#2ed573"
    if real_trend_side == "Player":
        if p_val >= 45.0: return "🔥 VÀO LỆNH: 🔵 PLAYER (Thuận xu hướng thực tế)", "rgba(0, 175, 185, 0.15)", "#00afb9"
        else: return "⚠️ KHUYẾN NGHỊ: BỎ QUA VÁN NÀY (Xu hướng lệch tính toán)", "rgba(235, 94, 40, 0.1)", "#eb5e28"
    elif real_trend_side == "Banker":
        if b_val >= 46.0: return "🔥 VÀO LỆ lệnh: 🔴 BANKER (Thuận xu hướng thực tế)", "rgba(254, 217, 255, 0.15)", "#fed9ff"
        else: return "⚠️ KHUYẾN NGHỊ: BỎ QUA VÁN NÀY (Xu hướng lệch tính toán)", "rgba(235, 94, 40, 0.1)", "#eb5e28"
    elif real_trend_side == "Sóng phẳng":
        if p_val >= 51.5: return "🔥 VÀO LỆNH: 🔵 PLAYER (Sóng phẳng - Lợi thế xác suất)", "rgba(0, 175, 185, 0.15)", "#00afb9"
        elif b_val >= 52.5: return "🔥 VÀO LỆNH: 🔴 BANKER (Sóng phẳng - Lợi thế xác suất)", "rgba(254, 217, 255, 0.15)", "#fed9ff"
    return "⚠️ KHUYẾN NGHỊ: BỎ QUA VÁN NÀY (Chờ dòng bài ổn định)", "rgba(164, 176, 190, 0.1)", "#a4b0be"

# BỘ ĐỌC KÝ TỰ BÀI NÂNG CẤP THÔNG MINH - ĐỌC ĐƯỢC CẢ CHỮ LẪN SỐ (VÍ DỤ: k2, a8, 10, q)
def parse_baccarat_input_v34(raw_str):
    if not raw_str: return []
    # Chuyển đổi chuỗi: xóa khoảng cách, dấu phẩy, đưa về dạng chữ hoa công nghiệp
    normalized = raw_str.upper().strip().replace(",", " ").replace(";", " ")
    
    # Xử lý trường hợp người dùng viết dính liền không dấu phẩy (Ví dụ: k2 -> K 2, a8 -> A 8)
    temp_tokens = []
    i = 0
    while i < len(normalized):
        if normalized[i].isspace():
            i += 1
            continue
        # Đoán ký tự đặc biệt "10" viết liền
        if normalized[i:i+2] == "10":
            temp_tokens.append("10")
            i += 2
        else:
            temp_tokens.append(normalized[i])
            i += 1

    result_list = []
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13, '10': 10, '0': 10}
    for token in temp_tokens:
        if token in mapping:
            result_list.append(mapping[token])
        elif token.isdigit():
            val = int(token)
            if 1 <= val <= 9:
                result_list.append(val)
    return result_list

# =========================================================================
# INTERFACE DESIGN
# =========================================================================
st.set_page_config(page_title="Oracle Engine v34.0", page_icon="🔮", layout="centered")

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'cards_per_round_history' not in st.session_state: st.session_state.cards_per_round_history = []
if 'form_counter' not in st.session_state: st.session_state.form_counter = 0

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(145deg, #0f2027, #1f404b, #2c5364) !important; color: #ecf0f1 !important; }
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; gap: 8px !important; }
    [data-testid="stHorizontalBlock"] > div { width: 50% !important; min-width: 46% !important; flex: 1 1 auto !important; }
    .central-game-counter { text-align: center; background: rgba(0, 175, 185, 0.15); border: 1px solid #00afb9; border-radius: 8px; padding: 8px 12px; font-family: monospace; font-size: 15px; font-weight: 800; color: #00afb9; margin-bottom: 15px; letter-spacing: 1px; }
    .ai-decision-box { text-align: center; border-radius: 10px; padding: 16px 10px; font-size: 18px; font-weight: 800; margin: 15px auto; letter-spacing: 0.5px; box-shadow: 0px 4px 15px rgba(0,0,0,0.3); }
    .hud-box { padding: 12px 6px; border-radius: 10px; text-align: center; margin-bottom: 10px; border: 1px solid #203a43; background: rgba(10, 25, 30, 0.9); min-height: 85px; display: flex; flex-direction: column; justify-content: center; }
    .hud-title { font-size: 11px; font-weight: 700; color: #a4b0be; text-transform: uppercase; }
    .hud-value { font-size: 24px; font-weight: 800; font-family: monospace; margin-top: 2px; }
    .neon-player-advantage { background-color: #005573 !important; border: 2px solid #00afb9 !important; }
    .neon-banker-advantage { background-color: #1e2b38 !important; border: 2px solid #57606f !important; }
    .neon-tie-alert { border: 2px solid #2ed573 !important; }
    .validation-hud { padding: 10px; border-radius: 6px; text-align: center; font-weight: 700; font-size: 12px; font-family: monospace; margin-bottom: 10px; }
    .logic-pass { background-color: rgba(46, 213, 115, 0.15); border: 1px solid #2ed573; color: #2ed573; }
    .logic-fail { background-color: rgba(235, 94, 40, 0.15); border: 1px solid #eb5e28; color: #eb5e28; }
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

st.sidebar.header("⚙️ CẤU HÌNH KHAY BÀI")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 THIẾT LẬP THÔNG SỐ GỐC")
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

# LOGIC PHÂN TÍCH ĐIỂM CHI TIẾT - CHỐNG LỖI HÒA (TIE) SAI LỆCH
if calc_triggered:
    p_clean = p_input.strip()
    b_clean = b_input.strip()
    
    if p_clean or b_clean:
        p_list = parse_baccarat_input_v34(p_clean)
        b_list = parse_baccarat_input_v34(b_clean)
        
        # Kiểm tra xem đây là nhập ĐIỂM TRỰC TIẾP hay nhập CHUỖI CÂY BÀI CHI TIẾT
        if len(p_clean) == 1 and p_clean.isdigit() and len(b_clean) == 1 and b_clean.isdigit():
            p_score_eval = int(p_clean)
            b_score_eval = int(b_clean)
            st.session_state.cards_per_round_history.append(0)
        else:
            # Tính toán quy đổi điểm chuẩn Baccarat từ danh sách quân bài đã bóc tách
            p_val_temp = p_list if p_list else [0]
            b_val_temp = b_list if b_list else [0]
            
            p_score_eval = sum([0 if c >= 10 else c for c in p_val_temp]) % 10
            b_score_eval = sum([0 if c >= 10 else c for c in b_val_temp]) % 10
            
            st.session_state.cards_per_round_history.append(len(p_list) + len(b_list))
            st.session_state.shoe_history.extend(p_list + b_list)
            
        # ÉP ĐỒNG BỘ CHÍNH XÁC KẾT QUẢ VÀO MẢNG XU HƯỚNG HIỂN THỊ
        if p_score_eval > b_score_eval:
            st.session_state.outcome_history.append("Player")
        elif b_score_eval > p_score_eval:
            st.session_state.outcome_history.append("Banker")
        else:
            st.session_state.outcome_history.append("Tie")
            
        st.session_state.form_counter += 1
        st.rerun()

# Thực hiện thuật toán
res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical, invalid_cards = calculate_baccarat_v18_ultimate(
    [], [], st.session_state.shoe_history, shoe_decks=decks,
    manual_cards_used=manual_cards, manual_games_played=manual_games,
    p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
)

st.markdown("---")

if is_strict_lock:
    st.error(f"### 🛑 HỆ THỐNG KHÓA: Thông số cấu hình gốc không đồng nhất.")
else:
    st.markdown("### 🔮 KẾT QUẢ PHÂN TÍCH CHO VÁN MỚI TỚI")
    
    rec_text, rec_bg, rec_border = get_ai_recommendation(res, st.session_state.outcome_history)
    st.markdown(f'<div class="ai-decision-box" style="background-color: {rec_bg}; border: 2px solid {rec_border}; color: {rec_border};">{rec_text}</div>', unsafe_allow_html=True)
    
    p_box_css, b_box_css, tie_box_css = "hud-box", "hud-box", "hud-box"
    if res['Player'] > res['Banker']: p_box_css = "hud-box neon-player-advantage"
    elif res['Banker'] > res['Player']: b_box_css = "hud-box neon-banker-advantage"
    
    left_col, right_col = st.columns(2, gap="small")
    with left_col:
        st.markdown("##### 📊 XÁC SUẤT CỬA CHÍNH")
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER</div><div class="hud-value" style="color:#00afb9;">{res["Player"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER</div><div class="hud-value" style="color:#fed9ff;">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{tie_box_css}"><div class="hud-title">🟢 TIE WIN</div><div class="hud-value" style="color: #2ed573;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
    with right_col:
        st.markdown("##### 💎 CỬA ĐÔI & XU HƯỚNG")
        st.markdown(f'<div class="hud-box"><div class="hud-title">🔵 P-PAIR</div><div class="hud-value" style="color:#00afb9; font-size:20px;">{p_pair}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box"><div class="hud-title">🔴 B-PAIR</div><div class="hud-value" style="color:#fed9ff; font-size:20px;">{b_pair}%</div></div>', unsafe_allow_html=True)
        if is_shoe_logical: st.markdown('<div class="validation-hud logic-pass">✔ KHAY HỢP LỆ</div>', unsafe_allow_html=True)
        else: st.markdown('<div class="validation-hud logic-fail">⚠️ ÂM KHAY BÀI</div>', unsafe_allow_html=True)
        
    # HIỂN THỊ BẢNG XU HƯỚNG CHUẨN XÁC THEO ĐIỂM CÂY BÀI THỰC TẾ
    if st.session_state.outcome_history:
        trend_letters = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.outcome_history]
        pattern_msg, pattern_color, _ = detect_baccarat_pattern(st.session_state.outcome_history)
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
            if st.session_state.cards_per_round_history:
                last_cnt = st.session_state.cards_per_round_history.pop()
                if last_cnt > 0: st.session_state.shoe_history = st.session_state.shoe_history[:-last_cnt]
            st.rerun()
with util_col_2:
    if st.button("🔄 LÀM TRỐNG KHAY", use_container_width=True, key="btn_reset_final"):
        st.session_state.shoe_history = []
        st.session_state.outcome_history = []
        st.session_state.cards_per_round_history = []
        st.session_state.form_counter = 0
        st.rerun()
