import streamlit as st

# =========================================================================
# SYSTEM CORE v8.6: FINITE SIMULATION ENGINE WITH VERTICAL UI CONFIG
# =========================================================================
def calculate_baccarat_ultimate_core(p_cards, b_cards, shoe_history, shoe_decks=8, 
                                     manual_cards_used=0, manual_games_played=0,
                                     p_wins=0, b_wins=0, tie_wins=0):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    sum_wins_games = p_wins + b_wins + tie_wins
    effective_games = manual_games_played if manual_games_played > sum_wins_games else sum_wins_games

    if manual_cards_used > total_initial_cards:
        return f"❌ Bất hợp lý: Số lá bài đã dùng ({manual_cards_used} lá) vượt quá tổng số bài trong khay ({total_initial_cards} lá)!", {}, 0.0, 0.0, "LỖI DỮ LIỆU", total_initial_cards

    if effective_games > int(total_initial_cards / 4):
        return f"❌ Bất hợp lý: Số ván đã chạy vượt quá giới hạn vật lý của khay bài!", {}, 0.0, 0.0, "LỖI DỮ LIỆU", total_initial_cards

    detailed_cards_count = len(shoe_history)
    
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure and deck_structure[card_val] > 0:
                deck_structure[card_val] -= 1
        cards_left = total_initial_cards - detailed_cards_count
        mode = "MÔ HÌNH TOÁN TỔ HỢP RỜI RẠC ĐA BIẾN (CHÍNH XÁC TUYỆT ĐỐI)"
    else:
        cards_removed = 0
        if manual_cards_used > 0:
            cards_removed = manual_cards_used
            mode = "ƯỚC LƯỢNG TIỆM CẬN BẬC CAO (THEO SỐ LƯỢNG LÁ)"
        elif sum_wins_games > 0:
            cards_removed = int((p_wins * 4.8633) + (b_wins * 4.8118) + (tie_wins * 5.2312))
            if manual_games_played > sum_wins_games:
                cards_removed += int((manual_games_played - sum_wins_games) * 4.9315)
            mode = f"MA TRẬN PHÂN RÃ TRỌNG SỐ THỜI GIAN THỰC (~{cards_removed} LÁ)"
        elif manual_games_played > 0:
            cards_removed = int(manual_games_played * 4.9315) 
            mode = f"ƯỚC LƯỢNG TUYỆT ĐỐI THEO SỐ VÁN (~{cards_removed} LÁ)"
        else:
            cards_removed = 0
            mode = "KHAY BÀI NGUYÊN BẢN (XÁC SUẤT GỐC NHÀ CÁI)"

        cards_left = max(0, total_initial_cards - cards_removed)
        if cards_removed > 0:
            ratio = cards_left / total_initial_cards
            for card_num in deck_structure:
                deck_structure[card_num] = (4 * shoe_decks) * ratio

    N = float(sum(deck_structure.values()))
    if N <= 6:
        return "⚠️ Cảnh báo: Khay bài đã vơi quá giới hạn an toàn để tính toán!", {}, 0.0, 0.0, mode, cards_left
    
    # CHI TIẾT TÍNH TOÁN CỬA ĐÔI (HYPERGEOMETRIC ĐA LỚP)
    p_pair_prob = 0.0
    for count in deck_structure.values():
        if count >= 2: p_pair_prob += (count / N) * ((count - 1) / (N - 1))
    p_pair_odds = round(p_pair_prob * 100, 2)

    b_pair_prob = 0.0
    if N > 3:
        for b_count in deck_structure.values():
            if b_count >= 2:
                p_rem_0 = ((N - b_count) / N) * ((N - b_count - 1) / (N - 1))
                p_rem_1 = 2 * (b_count / N) * ((N - b_count) / (N - 1))
                p_rem_2 = (b_count / N) * ((b_count - 1) / (N - 1))
                b_pair_prob += (p_rem_0 * (b_count / (N - 2)) * ((b_count - 1) / (N - 3)) +
                                p_rem_1 * (max(0.0, b_count - 1) / (N - 2)) * (max(0.0, b_count - 2) / (N - 3)) +
                                p_rem_2 * (max(0.0, b_count - 2) / (N - 2)) * (max(0.0, b_count - 3) / (N - 3)))
    b_pair_odds = round(b_pair_prob * 100, 2)

    # MA TRẬN TỔ HỢP ĐIỂM SỐ BACCARAT
    score_deck = {i: 0.0 for i in range(10)}
    for card_num, count in deck_structure.items():
        score_deck[0 if card_num >= 10 else card_num] += count

    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] -= 1

    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left

    current_sum = float(sum(score_deck.values()))
    if current_sum <= 0: return {"Player": 44.62, "Banker": 45.86, "Tie": 9.52}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left
        
    player_wins, banker_wins, ties = 0.0, 0.0, 0.0

    if p_score >= 6:  
        if b_score <= 5:  
            for card3_b in range(10):
                w_b = score_deck[card3_b]
                if w_b > 0:
                    prob_b = w_b / current_sum
                    final_b = (b_score + card3_b) % 10
                    if p_score > final_b: player_wins += prob_b
                    elif final_b > p_score: banker_wins += prob_b
                    else: ties += prob_b
        else:  
            if p_score > b_score: player_wins += 1.0
            elif b_score > p_score: banker_wins += 1.0
            else: ties += 1.0
    else:  
        for card3_p in range(10):
            w_p = score_deck[card3_p]
            if w_p > 0:
                prob_p = w_p / current_sum
                final_p = (p_score + card3_p) % 10
                
                rem_sum_after_p = current_sum - 1.0
                b_draws = False
                if b_score <= 2: b_draws = True
                elif b_score == 3 and card3_p != 8: b_draws = True
                elif b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]: b_draws = True
                elif b_score == 5 and card3_p in [4, 5, 6, 7]: b_draws = True
                elif b_score == 6 and card3_p in [6, 7]: b_draws = True
                
                if b_draws and rem_sum_after_p > 0:
                    for card3_b in range(10):
                        available_b = score_deck[card3_b] - (1.0 if card3_b == card3_p else 0.0)
                        if available_b > 0:
                            prob_b = available_b / rem_sum_after_p
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
    return odds_res, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left

# =========================================================================
# INTERFACE DESIGN & STYLES
# =========================================================================
st.set_page_config(page_title="Oracle Ultimate Edge v8.6", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stColumn"] { width: 50% !important; min-width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'game_counter' not in st.session_state: st.session_state.game_counter = 0
if 'last_results' not in st.session_state: st.session_state.last_results = None
if 'last_played_cards' not in st.session_state: st.session_state.last_played_cards = ""
if 'live_logs' not in st.session_state: st.session_state.live_logs = []
if 'last_cards_added' not in st.session_state: st.session_state.last_cards_added = []

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ Cấu HÌnh Hệ Thống")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Thiết lập nhanh khay bài")
manual_cards = st.sidebar.number_input("Số LÁ BÀI đã chia (nếu biết):", min_value=0, max_value=decks*52, value=0, step=1)
manual_games = st.sidebar.number_input("Tổng số ván đã chạy:", min_value=0, max_value=150, value=0, step=1)

# NÂNG CẤP: Xếp dọc các trường nhập bàn thắng chi tiết theo yêu cầu
st.sidebar.markdown("**Chi tiết số bàn thắng từng cửa (Hàng dọc):**")
p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0, step=1)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0, step=1)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0, step=1)

st.sidebar.markdown("---")
if st.session_state.live_logs:
    if st.sidebar.button("↩️ HOÀN TÁC VÁN VỪA NHẬP", use_container_width=True):
        if st.session_state.last_cards_added:
            num_to_remove = len(st.session_state.last_cards_added[-1])
            if num_to_remove <= len(st.session_state.shoe_history):
                st.session_state.shoe_history = st.session_state.shoe_history[:-num_to_remove]
            st.session_state.last_cards_added.pop()
        st.session_state.live_logs.pop()
        st.session_state.game_counter = max(0, st.session_state.game_counter - 1)
        st.session_state.last_results = None
        st.session_state.last_played_cards = ""
        st.rerun()

if st.sidebar.button("🔄 RESET KHAY BÀI MỚI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.game_counter = 0
    st.session_state.last_results = None
    st.session_state.last_played_cards = ""
    st.session_state.live_logs = []
    st.session_state.last_cards_added = []
    st.rerun()

calculated_total_games = p_wins_input + b_wins_input + tie_wins_input
# Đồng bộ biến gốc ban đầu
base_games_count = manual_games if manual_games > calculated_total_games else calculated_total_games

# NÂNG CẤP LOGIC: Số ván ở ngoài nhảy tăng dần tịnh tiến dựa vào số ván gốc + số ván đã gõ thực tế
display_game = base_games_count + len(st.session_state.live_logs)

# --- OUTPUT SCREEN MATRIX ---
if st.session_state.last_results:
    results_data = st.session_state.last_results
    
    if isinstance(results_data[0], str) and results_data[0].startswith("❌"):
        st.error(results_data[0])
    elif isinstance(results_data[0], str) and results_data[0].startswith("⚠️"):
        st.warning(results_data[0])
    else:
        res, p_pair, b_pair, remaining_deck, current_mode, cards_left = results_data
        
        left_result_col, right_pair_col = st.columns(2)
        with left_result_col:
            st.markdown("#### 📊 Cửa Chính")
            st.metric("🔵 PLAYER", f"{res['Player']}%")
            st.markdown(f"<p style='color:gray; font-size:11px; margin-top:-12px;'>Payout: 1 ăn 1.00</p>", unsafe_allow_html=True)
            st.metric("🔴 BANKER", f"{res['Banker']}%")
            st.markdown(f"<p style='color:gray; font-size:11px; margin-top:-12px;'>Payout: 1 ăn 0.95</p>", unsafe_allow_html=True)
            st.metric("🟢 TIE WIN", f"{res['Tie']}%")
            st.progress(res['Banker'] / 100 if res['Banker'] > 0 else 0)
            
        with right_pair_col:
            st.markdown("#### 💎 Cửa Đôi")
            st.metric("🔵 CON ĐÔI", f"{p_pair}%", delta="🔥 LỢI THẾ" if p_pair > 7.47 else "⚖️ BÌNH THƯỜNG")
            st.metric("🔴 CÁI ĐÔI", f"{b_pair}%", delta="🔥 LỢI THẾ" if b_pair > 7.47 else "⚖️ BÌNH THƯỜNG")

        st.markdown("---")
        
        st.markdown("### 💰 Phân Tích Ma Trận Quản Lý Vốn")
        k_col1, k_col2 = st.columns(2)
        max_side = "Player" if res['Player'] > res['Banker'] else "Banker"
        max_prob = res[max_side] / 100.0
        
        b = 0.95 if max_side == "Banker" else 1.00
        q = 1.0 - max_prob
        kelly_per = ((b * max_prob) - q) / b * 100
        kelly_per = max(0.0, kelly_per)
        
        with k_col1:
            if res['Player'] == 100.0 or res['Banker'] == 100.0:
                st.success(f"🎯 LỆNH TỐI CAO: Vào **{max_side.upper()}** (Tỷ lệ: 100%)")
            elif kelly_per > 0.1:
                safe_investment = round(kelly_per / 4, 2)
                if safe_investment >= 0.25:
                    st.info(f"✨ GỢI Ý: Vào **{max_side.upper()}** (Vốn khuyên dùng: {safe_investment}%)")
                else:
                    st.warning("⚖️ BIÊN ĐỘ MỎNG: Lợi thế quá thấp. Khuyên dùng: BỎ QUA.")
            else:
                st.warning("⚖️ CÂN BẰNG: Không tìm thấy lợi thế toán học tốt. BỎ QUA.")
                
        with k_col2:
            st.caption(f"Chế độ quét ma trận:\n{current_mode}")

        total_shoe_cards = decks * 52
        cards_used_calc = total_shoe_cards - cards_left
        penetration_rate = min(100.0, (cards_used_calc / total_shoe_cards) * 100)
        st.markdown(f"**Độ chín khay bài (Shoe Penetration): {round(penetration_rate, 1)}%**")
        st.progress(penetration_rate / 100.0)

        with st.expander("📊 Chi tiết cấu trúc ma trận khay bài còn lại"):
            st.write(f"Số lá bài còn lại ước tính trong khay: **{int(cards_left)} / {total_shoe_cards}** lá.")
            cols = st.columns(5)
            labels_13 = {1: "A", 11: "J", 12: "Q", 13: "K"}
            for idx, (num, cnt) in enumerate(remaining_deck.items()):
                card_label = labels_13.get(num, f"[{num}]")
                cols[idx % 5].text(f"{card_label}: {round(cnt, 1)} lá")
else:
    st.info("🔮 Vui lòng điền điểm số ván hiện tại vào ô bên dưới để kích hoạt hệ quét toán học.")

st.markdown("---")

# --- DATA INPUT ROW ---
head_col, status_col = st.columns([2, 1])
with head_col:
    st.subheader("🃏 Điền điểm ván này")
with status_col:
    # NÂNG CẤP: Hiển thị số hiệu ván tiếp theo tăng dần tự động dựa trên cấu trúc đã chơi
    st.markdown(f"<div style='text-align: right; margin-top: 10px; font-weight: bold; color: #ff4b4b;'>#Ván hiện tại: {display_game}</div>", unsafe_allow_html=True)

col_p, col_b = st.columns(2)
with col_p: p_input = st.text_input("PLAYER (Lá bài):", value="", placeholder="Ví dụ: 5,K,2")
with col_b: b_input = st.text_input("BANKER (Lá bài):", value="", placeholder="Ví dụ: J,7")

def clean_and_parse_input(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().replace(" ", "")
    tokens = []
    i = 0
    if "," in normalized:
        parts = normalized.split(",")
        for p in parts:
            p_clean = "".join([c for c in p if c in "2345678910AJQK"])
            if p_clean: tokens.append(p_clean)
    else:
        while i < len(normalized):
            if normalized[i:i+2] == "10":
                tokens.append("10")
                i += 2
            elif normalized[i] in "23456789AJQK":
                tokens.append(normalized[i])
                i += 1
            else: i += 1
                
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    result_list = []
    for tok in tokens:
        if tok in mapping: result_list.append(mapping[tok])
        elif tok.isdigit():
            val = int(tok)
            if 2 <= val <= 10: result_list.append(val)
    return result_list

# --- ACTION TRIGGER ---
if st.button("🚀 KÍCH HOẠT QUÉT MA TRẬN PHÂN TÍCH TỐI HẬU", use_container_width=True, type="primary"):
    current_game_signature = f"P:{p_input.strip().upper()}|B:{b_input.strip().upper()}"
    
    if not p_input.strip() and not b_input.strip():
        st.warning("⚠️ Bạn chưa nhập điểm cho ván này. Hãy điền bài vào ô Player và Banker!")
    elif current_game_signature == st.session_state.last_played_cards:
        st.error("⛔ CHẶN TRÙNG LẶP: Bạn vừa chạy ván này rồi! Vui lòng nhập điểm số của ván mới tiếp theo.")
    else:
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        
        if p_list or b_list:
            p_calc = p_list[:2]
            b_calc = b_list[:2]
            
            core_output = calculate_baccarat_ultimate_core(
                p_calc, b_calc, st.session_state.shoe_history, shoe_decks=decks,
                manual_cards_used=manual_cards, manual_games_played=base_games_count,
                p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
            )
            
            if isinstance(core_output, str):
                st.session_state.last_results = (core_output, {}, 0.0, 0.0, "LỖI", 0)
            else:
                res, remaining_deck, p_pair, b_pair, mode, cards_left = core_output
                st.session_state.last_results = (res, p_pair, b_pair, remaining_deck, mode, cards_left)
                
                if not mode.startswith("LỖI"):
                    st.session_state.last_played_cards = current_game_signature
                    all_added = p_list + b_list
                    st.session_state.shoe_history.extend(all_added)
                    st.session_state.last_cards_added.append(all_added)
                    
                    # Cập nhật số ván log thực tế tịnh tiến tăng dần dựa trên tổng số ván tích lũy
                    actual_index = display_game + 1
                    st.session_state.live_logs.append(f"Ván {actual_index}: Player({p_input.strip()}) vs Banker({b_input.strip()})")
                    
                    st.session_state.game_counter = display_game + 1
                    st.rerun()

# --- LIVE HISTORY LOG LOGIC DISPLAY ---
if st.session_state.live_logs:
    st.markdown("---")
    with st.expander("📝 Nhật ký khay bài hiện tại (Live Shoe Logs)", expanded=True):
        for log in reversed(st.session_state.live_logs):
            st.text(log)
