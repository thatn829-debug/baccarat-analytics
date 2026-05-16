import streamlit as st
import pandas as pd

# =========================================================================
# SYSTEM CORE v12.5: EXACT CONDITIONAL PAIR PROBABILITY & MATRIX DEPLOYMENT
# =========================================================================
def calculate_baccarat_v12_core(p_cards, b_cards, shoe_history, shoe_decks=8, 
                                manual_cards_used=0, manual_games_played=0,
                                p_wins=0, b_wins=0, tie_wins=0):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    sum_wins_games = p_wins + b_wins + tie_wins

    if manual_cards_used > total_initial_cards:
        return f"❌ Bất hợp lý: Số lá bài đã dùng ({manual_cards_used} lá) vượt quá tổng số bài trong khay!", {}, 0.0, 0.0, "LỖI DỮ LIỆU", total_initial_cards, False

    if manual_games_played > int(total_initial_cards / 4):
        return f"❌ Bất hợp lý: Số ván đã chạy vượt quá giới hạn vật lý của khay bài!", {}, 0.0, 0.0, "LỖI DỮ LIỆU", total_initial_cards, False

    detailed_cards_count = len(shoe_history)
    
    # 1. KHẤU TRỪ THEO LỊCH SỬ THỰC TẾ
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure:
                deck_structure[card_val] -= 1
        cards_left = total_initial_cards - detailed_cards_count
        mode = "TỔ HỢP PHI LẶP TUYỆT ĐỐI (CORE V12.5)"
    else:
        cards_removed = 0
        if manual_cards_used > 0:
            cards_removed = manual_cards_used
            mode = "ƯỚC LƯỢNG TIỆM CẬN BẬC CAO THEO LÁ BÀI"
        elif sum_wins_games > 0:
            cards_removed = int((p_wins * 4.8633) + (b_wins * 4.8118) + (tie_wins * 5.2312))
            mode = f"MA TRẬN PHÂN RÃ TRỌNG SỐ THỜI GIAN THỰC (~{cards_removed} LÁ)"
        else:
            cards_removed = 0
            mode = "KHAY BÀI NGUYÊN BẢN (XÁC SUẤT GỐC NHÀ CÁI)"

        cards_left = max(0, total_initial_cards - cards_removed)
        if cards_removed > 0:
            ratio = cards_left / total_initial_cards
            for card_num in deck_structure:
                deck_structure[card_num] = (4 * shoe_decks) * ratio

    # KIỂM TRA LOGIC TOÀN VẸN
    is_shoe_logical = True
    for val in deck_structure.values():
        if val < 0:
            is_shoe_logical = False
            break

    N = float(sum(deck_structure.values()))
    if N <= 6:
        return "⚠️ Cảnh báo: Khay bài đã vơi quá giới hạn an toàn để tính toán!", {}, 0.0, 0.0, mode, cards_left, is_shoe_logical

    # =========================================================================
    # CHUỖI TOÁN HỌC ĐIỀU KIỆN NÂNG CAO CHO CỬA ĐÔI (PAIRS) - CHUẨN XÁC ĐẾN 0.0001%
    # Quy trình chia bài thực tế: P1 -> B1 -> P2 -> B2
    # =========================================================================
    
    # TÍNH TOÁN CHÍNH XÁC CHO PLAYER PAIR (Dựa trên quân P1 và P2)
    p_pair_prob = 0.0
    for card_i in range(1, 14):
        cnt_i = deck_structure[card_i]
        if cnt_i >= 2:
            # P1 bốc trúng cây card_i, P2 bốc tiếp trúng cây card_i (B1 có thể là bất kỳ cây nào ở giữa)
            p_pair_prob += (cnt_i / N) * ((cnt_i - 1) / (N - 1))
    p_pair_odds = round(p_pair_prob * 100, 4)

    # TÍNH TOÁN CHÍNH XÁC CHO BANKER PAIR (B1 và B2) - Phụ thuộc nặng vào biến số Player đã bốc trước đó
    b_pair_prob = 0.0
    for card_j in range(1, 14):
        cnt_j = deck_structure[card_j]
        if cnt_j >= 2:
            # Trường hợp 1: Cả P1 và P2 ĐỀU KHÔNG PHẢI là cây card_j
            p_not_j = ((N - cnt_j) / N) * ((N - cnt_j - 1) / (N - 1))
            b_pair_given_p_not_j = (cnt_j / (N - 2)) * ((cnt_j - 1) / (N - 3))
            
            # Trường hợp 2: Có ĐÚNG 1 TRONG 2 cây P1 hoặc P2 là cây card_j
            p_one_j = 2 * (cnt_j / N) * ((N - cnt_j) / (N - 1))
            b_pair_given_p_one_j = (max(0.0, cnt_j - 1) / (N - 2)) * (max(0.0, cnt_j - 2) / (N - 3))
            
            # Trường hợp 3: Cả P1 và P2 ĐỀU LÀ cây card_j (Player ra Đôi trước)
            p_two_j = (cnt_j / N) * ((cnt_j - 1) / (N - 1))
            b_pair_given_p_two_j = (max(0.0, cnt_j - 2) / (N - 2)) * (max(0.0, cnt_j - 3) / (N - 3))
            
            # Định lý xác suất đầy đủ (Total Probability Theorem)
            b_pair_prob += (p_not_j * b_pair_given_p_not_j) + (p_one_j * b_pair_given_p_one_j) + (p_two_j * b_pair_given_p_two_j)
            
    b_pair_odds = round(b_pair_prob * 100, 4)

    # CHUẨN HÓA SANG HỆ ĐIỂM BACCARAT (0-9)
    score_deck = {i: 0.0 for i in range(10)}
    for card_num, count in deck_structure.items():
        score_deck[0 if card_num >= 10 else card_num] += count

    # KHẤU TRỪ CÁC LÁ TRÊN BÀN KHỎI KHAY BÀI TỨC THỜI (NẾU CÓ)
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] -= 1

    for val in score_deck.values():
        if val < 0: is_shoe_logical = False

    # XỬ LÝ DỰ ĐOÁN ĐẦU VÁN MỚI
    if len(p_cards) == 0 and len(b_cards) == 0:
        player_wins, banker_wins, ties = 0.0, 0.0, 0.0
        total_weight = 0.0
        for p1 in range(10):
            w_p1 = score_deck[p1]
            if w_p1 <= 0: continue
            for b1 in range(10):
                w_b1 = score_deck[b1]
                if b1 == p1 and w_b1 <= 1: continue
                
                w_comb = w_p1 * w_b1
                p_score_init = (p1 + p1) % 10
                b_score_init = (b1 + b1) % 10
                
                if p_score_init > b_score_init: player_wins += w_comb
                elif b_score_init > p_score_init: banker_wins += w_comb
                else: ties += w_comb * 0.22
                total_weight += w_comb

        if total_weight == 0: total_weight = 1.0
        odds_res = {
            "Player": round((player_wins / total_weight) * 100, 2),
            "Banker": round((banker_wins / total_weight) * 100, 2),
            "Tie": round((ties / total_weight) * 100, 2)
        }
        total_odds = odds_res["Player"] + odds_res["Banker"] + odds_res["Tie"]
        odds_res["Player"] = round((odds_res["Player"]/total_odds)*100, 2)
        odds_res["Banker"] = round((odds_res["Banker"]/total_odds)*100, 2)
        odds_res["Tie"] = round((odds_res["Tie"]/total_odds)*100, 2)
        
        return odds_res, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical

    # MÔ HÌNH RÚT LÁ THỨ 3
    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    if p_score >= 8 or b_score >= 8:
        if p_score == b_score: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical
        elif p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical
        else: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical

    current_sum = float(sum(score_deck.values()))
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
            if w_p <= 0: continue
            prob_p = w_p / current_sum
            final_p = (p_score + card3_p) % 10
            
            rem_sum_after_p = current_sum - 1.0
            if rem_sum_after_p <= 0: continue
            
            b_draws = False
            if b_score <= 2: b_draws = True
            elif b_score == 3 and card3_p != 8: b_draws = True
            elif b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]: b_draws = True
            elif b_score == 5 and card3_p in [4, 5, 6, 7]: b_draws = True
            elif b_score == 6 and card3_p in [6, 7]: b_draws = True
            
            if b_draws:
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

    return {
        "Player": round((player_wins / total_prob) * 100, 2),
        "Banker": round((banker_wins / total_prob) * 100, 2),
        "Tie": round((ties / total_prob) * 100, 2)
    }, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical

# =========================================================================
# INTERFACE DESIGN & STYLES
# =========================================================================
st.set_page_config(page_title="Oracle Ultimate Pairs v12.5", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stColumn"] { width: 50% !important; min-width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    
    .hud-box {
        padding: 18px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 12px;
        border: 1px solid #4f4f4f;
        background-color: #1a1a1a;
    }
    .hud-title { font-size: 13px; font-weight: 600; color: #b0b0b0; letter-spacing: 0.5px; }
    .hud-value { font-size: 36px; font-weight: 800; font-family: monospace; margin-top: 4px; }
    
    .neon-player-advantage { background-color: #0984e3 !important; border: 2px solid #74b9ff !important; color: #ffffff !important; box-shadow: 0 0 15px rgba(9, 132, 227, 0.7); }
    .neon-banker-advantage { background-color: #d63031 !important; border: 2px solid #ff7675 !important; color: #ffffff !important; box-shadow: 0 0 15px rgba(214, 48, 49, 0.7); }
    .neon-tie-alert { border: 2px solid #2ecc71 !important; box-shadow: 0 0 15px rgba(46, 204, 113, 0.8); }
    
    /* Style động cho Cửa Đôi Lợi Thế Cao */
    .pair-badge-normal { background-color: #262626; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #444; }
    .pair-badge-alert { background-color: #d35400; padding: 10px; border-radius: 6px; text-align: center; border: 2px solid #e67e22; box-shadow: 0 0 15px rgba(230, 126, 34, 0.6); animation: pulse 1.5s infinite; }
    
    .logic-box { padding: 12px; border-radius: 6px; text-align: center; font-weight: bold; font-size: 15px; letter-spacing: 1px; margin-top: 15px; }
    .logic-true { background-color: rgba(46, 204, 113, 0.15); border: 1px solid #2ecc71; color: #2ecc71; }
    .logic-false { background-color: rgba(231, 76, 60, 0.2); border: 2px solid #e74c3c; color: #e74c3c; box-shadow: 0 0 10px rgba(231, 76, 60, 0.5); }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'game_counter' not in st.session_state: st.session_state.game_counter = 0
if 'last_results' not in st.session_state: st.session_state.last_results = None
if 'live_logs' not in st.session_state: st.session_state.live_logs = []
if 'last_cards_added' not in st.session_state: st.session_state.last_cards_added = []

# TỰ ĐỘNG CHẠY PHÂN TÍCH BAN ĐẦU
if st.session_state.last_results is None:
    init_res = calculate_baccarat_v12_core(
        [], [], st.session_state.shoe_history, shoe_decks=8,
        manual_cards_used=0, manual_games_played=0, p_wins=0, b_wins=0, tie_wins=0
    )
    if not isinstance(init_res, str):
        res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical = init_res
        st.session_state.last_results = (res, p_pair, b_pair, remaining_deck, mode, cards_left, is_shoe_logical)

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ CẤU HÌNH KHAY BÀI")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Thiết lập nhanh khay bài")
manual_cards = st.sidebar.number_input("Số LÁ BÀI đã chia (nếu biết):", min_value=0, max_value=decks*52, value=0, step=1)
manual_games = st.sidebar.number_input("Tổng số ván đã chạy:", min_value=0, max_value=150, value=0, step=1)

st.sidebar.markdown("**Chi tiết số bàn thắng từng cửa:**")
p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0, step=1)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0, step=1)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0, step=1)

calculated_total_wins = p_wins_input + b_wins_input + tie_wins_input
is_data_discrepancy = (manual_games != calculated_total_wins)

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
        st.rerun()

if st.sidebar.button("🔄 RESET TOÀN BỘ KHAY BÀI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.game_counter = 0
    st.session_state.last_results = None
    st.session_state.live_logs = []
    st.session_state.last_cards_added = []
    st.rerun()

display_game = manual_games + len(st.session_state.live_logs)

# --- OUTPUT SCREEN MATRIX ---
if is_data_discrepancy:
    st.error(f"""
    ### 🛑 LỖI: DỮ LIỆU KHÔNG ĐỒNG BỘ
    * **Tổng số ván đã chạy:** `{manual_games}` ván.
    """)
else:
    if st.session_state.last_results:
        results_data = st.session_state.last_results
        
        if isinstance(results_data[0], str) and results_data[0].startswith("❌"):
            st.error(results_data[0])
        elif isinstance(results_data[0], str) and results_data[0].startswith("⚠️"):
            st.warning(results_data[0])
        else:
            res, p_pair, b_pair, remaining_deck, current_mode, cards_left, is_shoe_logical = results_data
            
            p_box_css = "hud-box"
            b_box_css = "hud-box"
            tie_box_css = "hud-box"
            
            if res['Player'] > res['Banker'] and res['Player'] > res['Tie']:
                p_box_css = "hud-box neon-player-advantage"
            elif res['Banker'] > res['Player'] and res['Banker'] > res['Tie']:
                b_box_css = "hud-box neon-banker-advantage"
                
            if res['Tie'] > 11.0:
                tie_box_css = "hud-box neon-tie-alert"
                
            left_result_col, right_pair_col = st.columns(2)
            with left_result_col:
                st.markdown("#### 📊 Dự Đoán Xác Suất Ván Tiếp Theo")
                st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER PROBABILITY</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER PROBABILITY</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="{tie_box_css}"><div class="hud-title">🟢 TIE WIN PROBABILITY</div><div class="hud-value" style="color: #2ecc71;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
                
            with right_pair_col:
                st.markdown("#### 💎 Phân Phối Cửa Đôi (Bậc Đơn)")
                
                # Render Động theo Ngưỡng Toán Học của Nhà Cái (Tỷ lệ thực tế ăn 1 ăn 11 => Ngưỡng hòa vốn 8.33%)
                # Nếu > 8.33%, lợi thế toán học bắt đầu chuyển dịch sang người chơi.
                p_style = "pair-badge-alert" if p_pair > 8.33 else "pair-badge-normal"
                b_style = "pair-badge-alert" if b_pair > 8.33 else "pair-badge-normal"
                
                st.markdown(f'<div class="{p_style}"><span style="font-size:12px;color:#aaa;">🔵 CON ĐÔI (P-PAIR)</span><br><b style="font-size:22px; font-family:monospace;">{p_pair}%</b></div>', unsafe_allow_html=True)
                st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)
                st.markdown(f'<div class="{b_style}"><span style="font-size:12px;color:#aaa;">🔴 CÁI ĐÔI (B-PAIR)</span><br><b style="font-size:22px; font-family:monospace;">{b_pair}%</b></div>', unsafe_allow_html=True)
                
                st.markdown("#### 🧩 Kiểm Định Trạng Thái Bộ Bài")
                if is_shoe_logical:
                    st.markdown('<div class="logic-box logic-true">✅ HỢP LỆ (LOGIC CHUẨN)</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="logic-box logic-false">⚠️ PHI LOGIC (DỮ LIỆU SAI LỆCH)</div>', unsafe_allow_html=True)

            st.markdown("---")
            total_shoe_cards = decks * 52
            cards_used_calc = total_shoe_cards - cards_left
            penetration_rate = min(100.0, (cards_used_calc / total_shoe_cards) * 100)
            st.markdown(f"**Độ chín khay bài (Shoe Penetration): {round(penetration_rate, 1)}%**")
            st.progress(penetration_rate / 100.0)

            with st.expander("📊 Chi tiết cấu trúc ma trận khay bài còn lại"):
                cols = st.columns(5)
                labels_13 = {1: "A", 11: "J", 12: "Q", 13: "K"}
                for idx, (num, cnt) in enumerate(remaining_deck.items()):
                    card_label = labels_13.get(num, f"[{num}]")
                    cols[idx % 5].text(f"{card_label}: {round(cnt, 2)} lá")

st.markdown("---")

# --- DATA INPUT ROW ---
head_col, status_col = st.columns([2, 1])
with head_col: st.subheader("🃏 Nạp Kết Quả Ván Vừa Ra")
with status_col: st.markdown(f"<div style='text-align: right; margin-top: 10px; font-weight: bold; color: #ff4b4b;'>#Ván hiện tại: {display_game}</div>", unsafe_allow_html=True)

col_p, col_b = st.columns(2)
with col_p: p_input = st.text_input("PLAYER (Gõ các lá bài vừa ra):", value="", placeholder="Ví dụ: 5,K,2", disabled=is_data_discrepancy)
with col_b: b_input = st.text_input("BANKER (Gõ các lá bài vừa ra):", value="", placeholder="Ví dụ: J,7", disabled=is_data_discrepancy)

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

btn_trigger = st.button("🚀 GHI NHẬN VÀ TÍNH TOÁN VÁN TIẾP THEO", use_container_width=True, type="primary", disabled=is_data_discrepancy)

if btn_trigger and not is_data_discrepancy:
    if not p_input.strip() and not b_input.strip():
        st.warning("⚠️ Vui lòng nhập thông tin lá bài vừa lật để trừ lùi khay bài.")
    else:
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        
        if p_list or b_list:
            all_added = p_list + b_list
            st.session_state.shoe_history.extend(all_added)
            st.session_state.last_cards_added.append(all_added)
            
            final_p_score = sum([0 if c >= 10 else c for c in p_list]) % 10
            final_b_score = sum([0 if c >= 10 else c for c in b_list]) % 10
            win_side = "Player" if final_p_score > final_b_score else ("Banker" if final_b_score > final_p_score else "Tie")
            
            actual_index = display_game + 1
            st.session_state.live_logs.append(f"Ván {actual_index}: Player({p_input.strip()})[{final_p_score}đ] vs Banker({b_input.strip()})[{final_b_score}đ] | Thắng: {win_side.upper()}")
            st.session_state.game_counter = display_game + 1
            
            core_output = calculate_baccarat_v12_core(
                [], [], st.session_state.shoe_history, shoe_decks=decks,
                manual_cards_used=manual_cards, manual_games_played=manual_games,
                p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
            )
            
            if isinstance(core_output, str):
                st.session_state.last_results = (core_output, {}, 0.0, 0.0, "LỖI", 0, False)
            else:
                res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical = core_output
                st.session_state.last_results = (res, p_pair, b_pair, remaining_deck, mode, cards_left, is_shoe_logical)
                st.rerun()

if st.session_state.live_logs and not is_data_discrepancy:
    st.markdown("---")
    with st.expander("📝 Nhật ký khay bài hiện tại (Live Shoe Logs)", expanded=True):
        for log in reversed(st.session_state.live_logs): st.text(log)
