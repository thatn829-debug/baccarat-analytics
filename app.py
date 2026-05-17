import streamlit as st
import pandas as pd

# =========================================================================
# SYSTEM CORE v19.5: CENTRALIZED GAME COUNTER & AUTO-CLEAR INTEGRATION
# =========================================================================
def calculate_baccarat_v18_ultimate(p_cards, b_cards, shoe_history, shoe_decks=8, 
                                    manual_cards_used=0, manual_games_played=0,
                                    p_wins=0, b_wins=0, tie_wins=0):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}

    if manual_cards_used > total_initial_cards or manual_games_played > int(total_initial_cards / 4):
        return "❌ Bất hợp lý: Cấu hình vượt quá giới hạn vật lý của khay bài!", {}, 0.0, 0.0, "LỖI", total_initial_cards, False, []

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
        return "⚠️ Cảnh báo: Khay bài không đủ quân để thiết lập không gian mẫu!", deck_structure, 0.0, 0.0, mode, cards_left, is_shoe_logical, invalid_cards_list

    p_pair_prob = 0.0
    for i in range(1, 14):
        if deck_structure[i] >= 2:
            p_pair_prob += (deck_structure[i] / N_total) * ((deck_structure[i] - 1) / (N_total - 1))
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

    if not p_cards and not b_cards:
        odds_res = {
            "Player": 44.62,
            "Banker": 45.86,
            "Tie": 9.52
        }
        return odds_res, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list

    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] -= 1

    player_wins, banker_wins, ties = 0.0, 0.0, 0.0
    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    if len(p_cards) == 2 and len(b_cards) == 2 and (p_score >= 8 or b_score >= 8):
        if p_score > b_score: player_wins = 1.0
        elif b_score > p_score: banker_wins = 1.0
        else: ties = 1.0
    else:
        if len(p_cards) >= 2 and p_score >= 6:
            if b_score <= 5 and len(b_cards) == 2:
                for card3_b in range(10):
                    w_b = score_deck[card3_b]
                    if w_b > 0:
                        prob_b = w_b / N_total
                        final_b = (b_score + card3_b) % 10
                        if p_score > final_b: player_wins += prob_b
                        elif final_b > p_score: banker_wins += prob_b
                        else: ties += prob_b
            else:
                if p_score > b_score: player_wins = 1.0
                elif b_score > p_score: banker_wins = 1.0
                else: ties = 1.0
        else:
            for card3_p in range(10):
                w_p = score_deck[card3_p]
                if w_p <= 0: continue
                prob_p = w_p / N_total
                final_p = (p_score + card3_p) % 10
                
                b_draws = False
                if b_score <= 2: b_draws = True
                elif b_score == 3 and card3_p != 8: b_draws = True
                elif b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]: b_draws = True
                elif b_score == 5 and card3_p in [4, 5, 6, 7]: b_draws = True
                elif b_score == 6 and card3_p in [6, 7]: b_draws = True
                
                if b_draws:
                    for card3_b in range(10):
                        w_b = score_deck[card3_b]
                        if w_b > 0:
                            prob_b = w_b / (N_total - 1.0 if N_total > 1 else 1)
                            final_b = (b_score + card3_b) % 10
                            combined_weight = prob_p * prob_b
                            if final_p > final_b: player_wins += combined_weight
                            elif final_b > final_p: banker_wins += combined_weight
                            else: ties += combined_weight
                else:
                    if final_p > b_score: player_wins += prob_p
                    elif b_score > final_p: banker_wins += prob_p
                    else: ties += prob_p

    total_prob = player_wins + banker_wins + ties
    if total_prob == 0: total_prob = 1.0

    odds_res = {
        "Player": round((player_wins / total_prob) * 100, 2),
        "Banker": round((banker_wins / total_prob) * 100, 2),
        "Tie": round((ties / total_prob) * 100, 2)
    }
    
    return odds_res, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list

def detect_baccarat_pattern(outcome_list):
    clean_list = [x for x in outcome_list if x in ["Player", "Banker"]]
    if len(clean_list) < 4: return "🔄 Đang tích lũy dữ liệu...", "#888888"
    last_side = clean_list[-1]
    streak_count = 0
    for item in reversed(clean_list):
        if item == last_side: streak_count += 1
        else: break
    if streak_count >= 4:
        side_vietnamese = "🔵 PLAYER" if last_side == "Player" else "🔴 BANKER"
        return f"🔥 BỆT {side_vietnamese} ({streak_count} ván!)", "#00cec9"
    return "📊 Khay bài đi sóng phẳng", "#2ed573"

# =========================================================================
# INTERFACE DESIGN & STYLES (MỆNH THỦY - MỆNH MỘC)
# =========================================================================
st.set_page_config(page_title="Oracle Engine v19.5 Phong Thủy", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(145deg, #0f2027, #1f404b, #2c5364) !important;
        color: #ecf0f1 !important;
    }
    
    /* Ép cột song song di động */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        gap: 8px !important;
    }
    [data-testid="stHorizontalBlock"] > div {
        width: 50% !important;
        min-width: 46% !important;
        flex: 1 1 auto !important;
    }

    /* Thiết kế nhãn đếm số ván trung tâm */
    .central-game-counter {
        text-align: center;
        background: rgba(0, 175, 185, 0.15);
        border: 1px solid #00afb9;
        border-radius: 8px;
        padding: 6px 12px;
        font-family: monospace;
        font-size: 15px;
        font-weight: 800;
        color: #00afb9;
        margin-bottom: 12px;
        letter-spacing: 1px;
        box-shadow: 0 0 10px rgba(0, 175, 185, 0.2);
    }

    .hud-box { 
        padding: 12px 6px; 
        border-radius: 10px; 
        text-align: center; 
        margin-bottom: 10px; 
        border: 1px solid #203a43; 
        background: rgba(10, 25, 30, 0.9); 
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        min-height: 85px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .hud-title { font-size: 11px; font-weight: 700; color: #a4b0be; letter-spacing: 0.5px; text-transform: uppercase; }
    .hud-value { font-size: 24px; font-weight: 800; font-family: monospace; margin-top: 2px; }
    
    .neon-player-advantage { 
        background-color: #005573 !important; 
        border: 2px solid #00afb9 !important; 
        box-shadow: 0 0 12px rgba(0, 175, 185, 0.5); 
    }
    .neon-banker-advantage { 
        background-color: #1e2b38 !important; 
        border: 2px solid #57606f !important; 
    }
    .neon-tie-alert { 
        border: 2px solid #2ed573 !important; 
        box-shadow: 0 0 12px rgba(46, 213, 115, 0.5); 
    }
    
    .validation-hud { padding: 10px; border-radius: 6px; text-align: center; font-weight: 700; font-size: 12px; font-family: monospace; margin-bottom: 10px; }
    .logic-pass { background-color: rgba(46, 213, 115, 0.15); border: 1px solid #2ed573; color: #2ed573; }
    .logic-fail { background-color: rgba(235, 94, 40, 0.15); border: 1px solid #eb5e28; color: #eb5e28; }
    
    .trend-hud { padding: 12px; border-radius: 8px; background-color: rgba(5, 15, 20, 0.9); border: 1px dashed #00afb9; margin-top: 5px; }
    .trend-title { font-size: 11px; font-weight: bold; color: #00afb9; text-transform: uppercase; margin-bottom: 4px;}
    .trend-string { font-size: 16px; font-family: monospace; letter-spacing: 4px; font-weight: 800; white-space: nowrap; overflow-x: auto; }
    
    .char-p { color: #00afb9; font-weight: bold; } 
    .char-b { color: #ffffff; font-weight: bold; opacity: 0.7; } 
    .char-t { color: #2ed573; font-weight: bold; }
    
    .stProgress > div > div > div > div { background-color: #2ed573 !important; }
    
    div.stButton > button:first-child {
        background-color: #00afb9 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        padding: 10px 0px;
    }
    div.stButton > button[id^="undo_btn"] {
        background-color: #d63031 !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None
if 'cards_per_round_history' not in st.session_state: st.session_state.cards_per_round_history = []

# Sidebar cấu hình khay bài
st.sidebar.header("⚙️ CẤU HÌNH KHAY BÀI")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 THIẾT LẬP THÔNG SỐ")
manual_cards = st.sidebar.number_input("Số LÁ BÀI đã chia (nếu biết):", min_value=0, max_value=decks*52, value=0)
manual_games = st.sidebar.number_input("Tổng số ván đã chạy:", min_value=0, max_value=150, value=0)

p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0)

calculated_total_wins = p_wins_input + b_wins_input + tie_wins_input
is_strict_lock = (manual_games > 0 and calculated_total_wins > 0 and manual_games != calculated_total_wins)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 RESET TOÀN BỘ KHAY BÀI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.outcome_history = []
    st.session_state.cards_per_round_history = []
    st.session_state.last_results = None
    if 'p_input_val' in st.session_state: st.session_state.p_input_val = ""
    if 'b_input_val' in st.session_state: st.session_state.b_input_val = ""
    st.rerun()

# --- KHU VỰC HIỂN THỊ SỐ VÁN TIẾP THEO TRUNG TÂM ---
st.markdown("### 🃏 DỮ LIỆU VÁN ĐANG XÉT")

# Tính toán số thứ tự ván tiếp theo chính xác dựa trên cấu hình + thực tế gõ tay
base_games = manual_games if manual_games > 0 else calculated_total_wins
current_session_games = len(st.session_state.outcome_history)
next_game_number = base_games + current_session_games + 1

st.markdown(f'<div class="central-game-counter">🔮 VÁN TIẾP THEO: VÁN THỨ {next_game_number}</div>', unsafe_allow_html=True)

# Hai ô nhập điểm xếp song song ngay dưới nhãn đếm số ván
input_col_left, input_col_right = st.columns(2, gap="small")

with input_col_left:
    p_input = st.text_input("🔵 PLAYER:", value="", placeholder="Ví dụ: 5,K,2", key="p_input_val")

with input_col_right:
    b_input = st.text_input("🔴 BANKER:", value="", placeholder="Ví dụ: J,7", key="b_input_val")

def clean_and_parse_input(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().replace(",", " ").replace(";", " ")
    raw_tokens = normalized.split()
    
    result_list = []
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13, '10': 10}
    
    for token in raw_tokens:
        token = token.strip()
        if not token: continue
        
        if token in mapping:
            result_list.append(mapping[token])
        elif token.isdigit():
            val = int(token)
            if 2 <= val <= 9:
                result_list.append(val)
        else:
            sub_i = 0
            while sub_i < len(token):
                if token[sub_i:sub_i+2] == "10":
                    result_list.append(10)
                    sub_i += 2
                elif token[sub_i] in mapping:
                    result_list.append(mapping[token[sub_i]])
                    sub_i += 1
                elif token[sub_i].isdigit():
                    v = int(token[sub_i])
                    if 2 <= v <= 9:
                        result_list.append(v)
                    sub_i += 1
                else:
                    sub_i += 1
    return result_list

action_col_1, action_col_2 = st.columns(2, gap="small")

with action_col_1:
    calc_triggered = st.button("🚀 GHI & TÍNH TOÁN", use_container_width=True)

with action_col_2:
    undo_triggered = st.button("⏪ HOÀN TÁC (UNDO)", use_container_width=True, id="undo_btn")

if undo_triggered:
    if st.session_state.outcome_history and st.session_state.cards_per_round_history:
        st.session_state.outcome_history.pop()
        last_round_cards_count = st.session_state.cards_per_round_history.pop()
        if last_round_cards_count > 0:
            st.session_state.shoe_history = st.session_state.shoe_history[:-last_round_cards_count]
        
        st.session_state.last_results = calculate_baccarat_v18_ultimate(
            [], [], st.session_state.shoe_history, shoe_decks=decks,
            manual_cards_used=manual_cards, manual_games_played=manual_games,
            p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
        )
        st.toast("⏪ Đã hoàn tác ván bài vừa nhập thành công!", icon="↩️")
        st.rerun()
    else:
        st.toast("⚠️ Chưa có dữ liệu ván nào trong phiên này để hoàn tác!", icon="❌")

if not st.session_state.last_results:
    st.session_state.last_results = calculate_baccarat_v18_ultimate(
        [], [], st.session_state.shoe_history, shoe_decks=decks,
        manual_cards_used=manual_cards, manual_games_played=manual_games,
        p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
    )

if calc_triggered:
    p_list = clean_and_parse_input(p_input)
    b_list = clean_and_parse_input(b_input)
    
    core_output = calculate_baccarat_v18_ultimate(
        p_list, b_list, st.session_state.shoe_history, shoe_decks=decks,
        manual_cards_used=manual_cards, manual_games_played=manual_games,
        p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
    )
    
    if isinstance(core_output, str):
        st.session_state.last_results = (core_output, {}, 0.0, 0.0, "LỖI", 0, False, [])
    else:
        st.session_state.last_results = core_output
        if p_list or b_list:
            p_score_eval = sum([0 if c >= 10 else c for c in p_list]) % 10
            b_score_eval = sum([0 if c >= 10 else c for c in b_list]) % 10
            if p_score_eval > b_score_eval:
                st.session_state.outcome_history.append("Player")
            elif b_score_eval > p_score_eval:
                st.session_state.outcome_history.append("Banker")
            else:
                st.session_state.outcome_history.append("Tie")
                
            total_cards_this_round = len(p_list) + len(b_list)
            st.session_state.cards_per_round_history.append(total_cards_this_round)
            st.session_state.shoe_history.extend(p_list + b_list)
            
        st.session_state.p_input_val = ""
        st.session_state.b_input_val = ""
        st.rerun()

st.markdown("---")

if is_strict_lock:
    st.error(f"### 🛑 HỆ THỐNG KHÓA: Số ván tổng lệch với tổng số ván thắng lẻ. Vui lòng kiểm tra sidebar.")
else:
    if st.session_state.last_results:
        results_data = st.session_state.last_results
        if isinstance(results_data, str):
            st.error(results_data)
        else:
            res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical, invalid_cards = results_data
            
            p_box_css = "hud-box"
            b_box_css = "hud-box"
            tie_box_css = "hud-box"
            if res['Player'] > res['Banker'] and res['Player'] > res['Tie']: p_box_css = "hud-box neon-player-advantage"
            elif res['Banker'] > res['Player'] and res['Banker'] > res['Tie']: b_box_css = "hud-box neon-banker-advantage"
            if res['Tie'] > 12.5: tie_box_css = "hud-box neon-tie-alert"
            
            st.markdown("### 🔮 KẾT QUẢ PHÂN TÍCH THỦY MỘC TRẬN")
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
                
                if is_shoe_logical: 
                    st.markdown('<div class="validation-hud logic-pass">✔ KHAY HỢP LỆ</div>', unsafe_allow_html=True)
                else: 
                    st.markdown('<div class="validation-hud logic-fail">⚠️ ÂM KHAY BÀI</div>', unsafe_allow_html=True)
                
            if st.session_state.outcome_history:
                trend_letters = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.outcome_history]
                pattern_msg, pattern_color = detect_baccarat_pattern(st.session_state.outcome_history)
                st.markdown(f'<div class="trend-hud"><div class="trend-title">📈 XU HƯỚNG SÀN ({len(st.session_state.outcome_history)} ván)</div><div class="trend-string">{" ".join(trend_letters)}</div><div style="color: {pattern_color}; font-weight: bold; font-size: 12px; margin-top:4px;">{pattern_msg}</div></div>', unsafe_allow_html=True)

            st.markdown("---")
            total_shoe_cards = decks * 52
            penetration_rate = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
            st.caption(f"**Chế độ:** `{mode}` | **Còn lại:** {int(cards_left)}/{total_shoe_cards} lá")
            st.progress(penetration_rate / 100.0)
