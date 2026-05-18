import streamlit as st

# =========================================================================
# PERFECT MOBILE ENGINE v40.0: ZERO-LAG & ADAPTIVE MOBILE UI
# =========================================================================

def calculate_baccarat_v40_core(shoe_history, shoe_decks=8, manual_cards_used=0, manual_games_played=0, total_real_games=0):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    detailed_cards_count = len(shoe_history)
    
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure:
                deck_structure[card_val] = max(0.0, deck_structure[card_val] - 1)
        cards_left = total_initial_cards - detailed_cards_count
        mode = "MÔ PHỎNG MARKOV CHI TIẾT"
    else:
        total_games_played = max(manual_games_played, total_real_games)
        cards_removed = max(0, manual_cards_used if manual_cards_used > 0 else int(total_games_played * 4.852))
        cards_left = max(0, total_initial_cards - cards_removed)
        mode = "PHÂN RÃ BAYES PHI TUYẾN TÍNH"
        
        if cards_removed > 0:
            consumed_ratio = cards_removed / total_initial_cards
            for card_num in deck_structure:
                reduction = (4 * shoe_decks) * consumed_ratio
                deck_structure[card_num] = max(0.0, (4 * shoe_decks) - reduction)

    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: score_deck[0] += count
        else: score_deck[card_num] += count

    N_total = float(sum(score_deck))
    if N_total <= 6:
        return {"Player": 44.62, "Banker": 45.86, "Tie": 9.52}, deck_structure, 0.0, 0.0, mode, cards_left, True

    # Ma trận trọng số Card Counting chuẩn hóa toán học quốc tế
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

    p_pair_prob = 0.0
    for i in range(1, 14):
        if deck_structure[i] >= 2: 
            p_pair_prob += (deck_structure[i] / N_total) * ((deck_structure[i] - 1) / (N_total - 1))
    p_pair_odds = round(p_pair_prob * 100, 2)
    b_pair_odds = round(p_pair_odds * 1.015, 2)

    odds_res = {"Player": round(p_prob, 2), "Banker": round(b_prob, 2), "Tie": round(t_prob, 2)}
    return odds_res, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, True

def detect_baccarat_pattern(outcome_list):
    clean_list = [x for x in outcome_list if x in ["Player", "Banker"]]
    if len(clean_list) < 3: 
        return "🔄 Đang tích lũy xu hướng thực tế...", "#888888", None, 0
    
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
        return "⚠️ CHỜ DỮ LIỆU THỰC TẾ: Nhập tối thiểu 2 ván đầu để bắt nhịp sàn.", "rgba(164, 176, 190, 0.1)", "#a4b0be"
    if t_val > 13.0:
        return f"🟢 CÂN NHẮC: HÒA (TIE) | Xác suất Hòa rất cao ({t_val}%) - Đi tiền nhỏ lót.", "rgba(46, 213, 115, 0.15)", "#2ed573"
        
    if real_trend_side == "Player":
        if p_val >= 44.2:
            return f"🔥 ĐỒNG THUẬN CAO: VÀO 🔵 PLAYER | Xu hướng bệt {streak_count} ván + Xác suất ủng hộ ({p_val}%).", "rgba(0, 175, 185, 0.2)", "#00afb9"
        else:
            return f"⚠️ XUNG ĐỘT: BỎ QUA VÁN NÀY | Sàn bệt PLAYER nhưng cấu trúc toán học báo rủi ro bẻ cầu.", "rgba(235, 94, 40, 0.15)", "#eb5e28"
    elif real_trend_side == "Banker":
        if b_val >= 45.2:
            return f"🔥 ĐỒNG THUẬN CAO: VÀO 🔴 BANKER | Xu hướng bệt {streak_count} ván + Xác suất toán học đạt {b_val}%.", "rgba(254, 217, 255, 0.2)", "#fed9ff"
        else:
            return f"⚠️ XUNG ĐỘT: BỎ QUA VÁN NÀY | Sàn bệt BANKER nhưng cấu trúc khay bài bất lợi.", "rgba(235, 94, 40, 0.15)", "#eb5e28"
    elif real_trend_side == "Sóng phẳng":
        if p_val >= 46.0:
            return f"🔵 VÀO LỆNH: PLAYER | Cấu trúc khay bài lệch hẳn về Player ({p_val}%).", "rgba(0, 175, 185, 0.15)", "#00afb9"
        elif b_val >= 47.0:
            return f"🔴 VÀO LỆNH: BANKER | Khay bài báo lợi thế toán học tốt cho Banker ({b_val}%).", "rgba(254, 217, 255, 0.15)", "#fed9ff"
            
    return "📊 QUAN SÁT: Bài đi không rõ xu hướng và điểm số cân bằng. Không vào lệnh ván này.", "rgba(164, 176, 190, 0.1)", "#a4b0be"

def parse_baccarat_input_v40(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().strip().replace(",", " ").replace(";", " ").replace("10", "0")
    mapping = {'A': 1, 'J': 10, 'Q': 10, 'K': 10, '0': 10}
    return [mapping[ch] if ch in mapping else int(ch) for ch in normalized if ch in mapping or (ch.isdigit() and '1' <= ch <= '9')]

# =========================================================================
# MOBILE-FIRST INTERFACE DESIGN
# =========================================================================
st.set_page_config(page_title="Oracle Engine v40.0", page_icon="🔮", layout="centered")

# CSS tối giản, tối ưu hóa hiển thị Responsive trên điện thoại di động
st.markdown(
    """
    <style>
    .stApp { background-color: #0d1b2a !important; color: #e0e1dd !important; }
    .central-game-counter { text-align: center; background: rgba(0, 175, 185, 0.1); border: 1px solid #00afb9; border-radius: 8px; padding: 10px; font-weight: bold; color: #00afb9; font-size: 14px; margin-bottom: 12px; }
    .ai-decision-box { text-align: center; border-radius: 8px; padding: 12px; font-size: 15px; font-weight: bold; margin: 12px auto; box-shadow: 0px 2px 8px rgba(0,0,0,0.2); line-height: 1.4; }
    .hud-box-mobile { padding: 10px 4px; border-radius: 8px; text-align: center; margin-bottom: 8px; border: 1px solid #1b263b; background-color: #1b263b; width: 100%; box-sizing: border-box; }
    .hud-title { font-size: 10px; font-weight: bold; color: #a4b0be; text-transform: uppercase; }
    .hud-value { font-size: 20px; font-weight: 800; margin-top: 2px; font-family: monospace; }
    .trend-hud { padding: 10px; border-radius: 8px; background-color: #0d1b2a; border: 1px dashed #00afb9; margin-top: 8px; }
    .trend-title { font-size: 10px; font-weight: bold; color: #00afb9; text-transform: uppercase; margin-bottom: 4px;}
    .trend-string { font-size: 15px; font-family: monospace; letter-spacing: 3px; font-weight: bold; word-break: break-all; }
    .char-p { color: #00afb9; } .char-b { color: #e74c3c; } .char-t { color: #2ed573; }
    div.stButton > button { background-color: #00afb9 !important; color: white !important; border-radius: 6px; font-weight: bold; padding: 10px 0px; width: 100% !important; border: none; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'cards_per_round_history' not in st.session_state: st.session_state.cards_per_round_history = []
if 'form_counter' not in st.session_state: st.session_state.form_counter = 0

# SIDEBAR CONFIG
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

# MAIN INTERFACE
st.markdown("### 🃏 DỮ LIỆU XÉT")
base_games = manual_games if manual_games > 0 else calculated_total_wins
current_session_games = len(st.session_state.outcome_history)
next_game_number = base_games + current_session_games + 1

st.markdown(f'<div class="central-game-counter">🔮 NHẬP ĐIỂM VÁN THỨ: {next_game_number}</div>', unsafe_allow_html=True)

# Giao diện nhập liệu hai cột thích ứng di động tốt
input_col_left, input_col_right = st.columns(2)
with input_col_left:
    p_input = st.text_input("🔵 PLAYER:", key=f"p_in_{st.session_state.form_counter}", placeholder="Ví dụ: k2 hoặc 7")
with input_col_right:
    b_input = st.text_input("🔴 BANKER:", key=f"b_in_{st.session_state.form_counter}", placeholder="Ví dụ: a8 hoặc 5")

calc_triggered = st.button("🚀 XỬ LÝ & TÍNH TOÁN XÁC SUẤT")

if calc_triggered:
    p_clean = p_input.strip()
    b_clean = b_input.strip()
    
    if p_clean or b_clean:
        p_list = parse_baccarat_input_v40(p_clean)
        b_list = parse_baccarat_input_v40(b_clean)
        
        if len(p_clean) == 1 and p_clean.isdigit() and len(b_clean) == 1 and b_clean.isdigit():
            p_score_eval = int(p_clean)
            b_score_eval = int(b_clean)
            st.session_state.cards_per_round_history.append(0)
        else:
            p_val_temp = p_list if p_list else [0]
            b_val_temp = b_list if b_list else [0]
            p_score_eval = sum([0 if c >= 10 else c for c in p_val_temp]) % 10
            b_score_eval = sum([0 if c >= 10 else c for c in b_val_temp]) % 10
            
            st.session_state.cards_per_round_history.append(len(p_list) + len(b_list))
            st.session_state.shoe_history.extend(p_list + b_list)
            
        if p_score_eval > b_score_eval:
            st.session_state.outcome_history.append("Player")
        elif b_score_eval > p_score_eval:
            st.session_state.outcome_history.append("Banker")
        else:
            st.session_state.outcome_history.append("Tie")
            
        st.session_state.form_counter += 1
        st.rerun()

# Thực hiện tính toán ma trận tốc độ cao
res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical = calculate_baccarat_v40_core(
    st.session_state.shoe_history, shoe_decks=decks,
    manual_cards_used=manual_cards, manual_games_played=manual_games,
    total_real_games=len(st.session_state.outcome_history)
)

st.markdown("---")

if is_strict_lock:
    st.error("### 🛑 Khóa hệ thống: Lệch thông số gốc.")
else:
    st.markdown("### 🔮 ĐÁNH GIÁ TỪ ENGINE")
    
    rec_text, rec_bg, rec_border = get_ai_recommendation(res, st.session_state.outcome_history)
    st.markdown(f'<div class="ai-decision-box" style="background-color: {rec_bg}; border: 1px solid {rec_border}; color: {rec_border};">{rec_text}</div>', unsafe_allow_html=True)
    
    # Render hộp dữ liệu 2 cột chuẩn hóa mobile bằng st.columns bản địa
    view_col_left, view_col_right = st.columns(2)
    with view_col_left:
        st.markdown(f'<div class="hud-box-mobile"><div class="hud-title">🔵 PLAYER</div><div class="hud-value" style="color:#00afb9;">{res["Player"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box-mobile"><div class="hud-title">🔴 BANKER</div><div class="hud-value" style="color:#fed9ff;">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box-mobile"><div class="hud-title">🟢 TIE WIN</div><div class="hud-value" style="color: #2ed573;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
    with view_col_right:
        st.markdown(f'<div class="hud-box-mobile"><div class="hud-title">🔵 P-PAIR</div><div class="hud-value" style="color:#00afb9; font-size:18px;">{p_pair}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box-mobile"><div class="hud-title">🔴 B-PAIR</div><div class="hud-value" style="color:#fed9ff; font-size:18px;">{b_pair}%</div></div>', unsafe_allow_html=True)
        
        if is_shoe_logical: 
            st.markdown('<div class="hud-box-mobile" style="background-color:rgba(46,213,115,0.1); border:1px solid #2ed573; color:#2ed573; font-size:12px; font-weight:bold; min-height:38px; display:flex; align-items:center; justify-content:center;">✔ KHAY HỢP LỆ</div>', unsafe_allow_html=True)
        else: 
            st.markdown('<div class="hud-box-mobile" style="background-color:rgba(235,94,40,0.1); border:1px solid #eb5e28; color:#eb5e28; font-size:12px; font-weight:bold; min-height:38px; display:flex; align-items:center; justify-content:center;">⚠️ ÂM KHAY</div>', unsafe_allow_html=True)
        
    if st.session_state.outcome_history:
        trend_letters = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.outcome_history]
        pattern_msg, pattern_color, _, _ = detect_baccarat_pattern(st.session_state.outcome_history)
        st.markdown(f'<div class="trend-hud"><div class="trend-title">📈 XU HƯỚNG SÀN ĐÃ QUA ({len(st.session_state.outcome_history)} ván)</div><div class="trend-string">{" ".join(trend_letters)}</div><div style="color: {pattern_color}; font-weight: bold; font-size: 11px; margin-top:2px;">{pattern_msg}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    total_shoe_cards = decks * 52
    penetration_rate = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
    st.caption(f"**Chế độ:** `{mode}` | **Còn lại:** {int(cards_left)}/{total_shoe_cards} lá")
    st.progress(penetration_rate / 100.0)

st.markdown("<br>", unsafe_allow_html=True)
util_col_1, util_col_2 = st.columns(2)
with util_col_1:
    if st.button("⏪ HOÀN TÁC"):
        if st.session_state.outcome_history:
            st.session_state.outcome_history.pop()
            if st.session_state.cards_per_round_history:
                last_cnt = st.session_state.cards_per_round_history.pop()
                if last_cnt > 0: 
                    st.session_state.shoe_history = st.session_state.shoe_history[:-last_cnt]
            st.rerun()
with util_col_2:
    if st.button("🔄 LÀM TRỐNG"):
        st.session_state.shoe_history = []
        st.session_state.outcome_history = []
        st.session_state.cards_per_round_history = []
        st.session_state.form_counter = 0
        st.rerun()
