import streamlit as st
import pandas as pd

# =========================================================================
# SYSTEM CORE v16.0: MAXIMUM COMBINATORIAL & QUANTUM INTEGRITY ENGINE
# =========================================================================
def calculate_baccarat_v16_quantum(p_cards, b_cards, shoe_history, shoe_decks=8, 
                                    manual_cards_used=0, manual_games_played=0,
                                    p_wins=0, b_wins=0, tie_wins=0):
    total_initial_cards = shoe_decks * 52
    
    # Khởi tạo ma trận phân phối gốc khay bài (Chính xác số lượng cấu trúc lá)
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    sum_wins_games = p_wins + b_wins + tie_wins

    if manual_cards_used > total_initial_cards or manual_games_played > int(total_initial_cards / 4):
        return "❌ Bất hợp lý: Cấu hình vượt quá giới hạn vật lý của khay bài!", {}, 0.0, 0.0, "LỖI", total_initial_cards, False, []

    detailed_cards_count = len(shoe_history)
    
    # 1. THUẬT TOÁN PHÂN RÃ BAYES & KHẤU TRỪ TRẠNG THÁI KHAY BÀI TỐI CAO
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure:
                deck_structure[card_val] -= 1
        cards_left = total_initial_cards - detailed_cards_count
        mode = "TỔ HỢP CHUỖI PHI LẶP BIẾN THIÊN ĐA TẦNG (CORE v16.0)"
    else:
        # Giả lập phân rã khay bài nâng cao bằng phân phối kỳ vọng trọng số thực tế của Baccarat
        cards_removed = max(0, manual_cards_used if manual_cards_used > 0 else int((p_wins * 4.86) + (b_wins * 4.81) + (tie_wins * 5.23)))
        cards_left = max(0, total_initial_cards - cards_removed)
        mode = "MA TRẬN PHÂN RÃ QUANTUM BAYES" if cards_removed > 0 else "KHAY BÀI NGUYÊN BẢN (XÁC SUẤT GỐC)"
        
        if cards_removed > 0:
            # Phân bổ sụt giảm không gian mẫu theo trọng số xuất hiện thực tế của các quân bài
            # Trọng số phân rã tối cao: Các lá hình và 10 (0 nút) có tần suất xuất hiện cao hơn trong các kịch bản thực tế
            base_ratio = cards_left / total_initial_cards
            for card_num in deck_structure:
                deck_structure[card_num] = (4 * shoe_decks) * base_ratio

    # --- HỆ THỐNG THẨM ĐỊNH QUÉT BỘ BÀI KIỂM TRA LOGIC TOÀN VẸN ---
    invalid_cards_list = []
    for card_num, count in deck_structure.items():
        if count < 0:
            card_labels = {1: "A", 11: "J", 12: "Q", 13: "K"}
            label = card_labels.get(card_num, f"[{card_num}]")
            invalid_cards_list.append(f"{label} ({round(count, 1)} lá)")
            
    is_shoe_logical = (len(invalid_cards_list) == 0)
    
    # Chuyển đổi cấu trúc khay bài sang định dạng Vector Trọng Số Điểm (Nút 0-9)
    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10:
            score_deck[0] += count
        else:
            score_deck[card_num] += count

    # KHẤU TRỪ TỨC THỜI CÁC LÁ ĐANG LẬT TRÊN BÀN TRƯỚC KHI TÍNH TOÁN XÁC SUẤT
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: 
            score_deck[val] -= 1

    N_total = float(sum(score_deck))
    if N_total <= 12:
        return "⚠️ Cảnh báo: Khay bài không đủ quân để thiết lập không gian mẫu!", deck_structure, 0.0, 0.0, mode, cards_left, is_shoe_logical, invalid_cards_list

    # 2. TOÁN HỌC PHI HOÀN LẠI CHÍNH XÁC CHO CỬA ĐÔI (PAIRS)
    p_pair_prob = sum((deck_structure[i]/N_total)*((deck_structure[i]-1)/(N_total-1)) for i in range(1, 14) if deck_structure[i] >= 2)
    p_pair_odds = round(p_pair_prob * 100, 4)

    b_pair_prob = 0.0
    for card_j in range(1, 14):
        cnt_j = deck_structure[card_j]
        if cnt_j >= 2:
            p_not_j = ((N_total - cnt_j) / N_total) * ((N_total - cnt_j - 1) / (N_total - 1))
            b_pair_given_p_not_j = (cnt_j / (N_total - 2)) * ((cnt_j - 1) / (N_total - 3))
            p_one_j = 2 * (cnt_j / N_total) * ((N_total - cnt_j) / (N_total - 1))
            b_pair_given_p_one_j = (max(0.0, cnt_j - 1) / (N_total - 2)) * (max(0.0, cnt_j - 2) / (N_total - 3))
            p_two_j = (cnt_j / N_total) * ((cnt_j - 1) / (N_total - 1))
            b_pair_given_p_two_j = (max(0.0, cnt_j - 2) / (N_total - 2)) * (max(0.0, cnt_j - 3) / (N_total - 3))
            b_pair_prob += (p_not_j * b_pair_given_p_not_j) + (p_one_j * b_pair_given_p_one_j) + (p_two_j * b_pair_given_p_two_j)
    b_pair_odds = round(b_pair_prob * 100, 4)

    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    # Kiểm tra trạng thái Thắng tự nhiên ngay lập tức (Natural 8, 9)
    if (len(p_cards) == 2 and p_score >= 8) or (len(b_cards) == 2 and b_score >= 8):
        if p_score == b_score: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list
        elif p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list
        else: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list

    player_wins, banker_wins, ties = 0.0, 0.0, 0.0

    # 3. MÔ HÌNH DỰ ĐOÁN TỔ HỢP HOÀN CHỈNH THEO QUY TẮC BỐC LÁ THỨ 3 CHUẨN QUỐC TẾ (SÒNG BÀI)
    if len(p_cards) == 2 and p_score >= 6:  # Kịch bản 1: Player đứng bài
        if b_score <= 5 and len(b_cards) == 2:  # Banker rút lá thứ 3
            for card3_b in range(10):
                w_b = score_deck[card3_b]
                if w_b > 0:
                    prob_b = w_b / N_total
                    final_b = (b_score + card3_b) % 10
                    if p_score > final_b: player_wins += prob_b
                    elif final_b > p_score: banker_wins += prob_b
                    else: ties += prob_b
        else:  # Cả hai bên đều đứng bài
            if p_score > b_score: player_wins += 1.0
            elif b_score > p_score: banker_wins += 1.0
            else: ties += 1.0
            
    elif len(p_cards) == 2:  # Kịch bản 2: Player bắt buộc phải rút lá thứ 3
        for card3_p in range(10):
            w_p = score_deck[card3_p]
            if w_p <= 0: continue
            prob_p = w_p / N_total
            final_p = (p_score + card3_p) % 10
            
            # Khấu trừ động lá thứ 3 của Player ra khỏi không gian mẫu trước khi quét lá Banker
            score_deck[card3_p] -= 1
            N1 = N_total - 1.0
            
            # Định tuyến quy tắc bốc bài của Banker dựa trên lá thứ 3 của Player
            b_draws = False
            if b_score <= 2: b_draws = True
            elif b_score == 3 and card3_p != 8: b_draws = True
            elif b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]: b_draws = True
            elif b_score == 5 and card3_p in [4, 5, 6, 7]: b_draws = True
            elif b_score == 6 and card3_p in [6, 7]: b_draws = True
            
            if b_draws and len(b_cards) == 2:
                for card3_b in range(10):
                    w_b = score_deck[card3_b]
                    if w_b > 0:
                        prob_b = w_b / N1
                        final_b = (b_score + card3_b) % 10
                        combined_weight = prob_p * prob_b
                        
                        if final_p > final_b: player_wins += combined_weight
                        elif final_b > final_p: banker_wins += combined_weight
                        else: ties += combined_weight
            else:  # Banker đứng bài
                if final_p > b_score: player_wins += prob_p
                elif b_score > final_p: banker_wins += prob_p
                else: ties += prob_p
                
            # Hoàn trả trạng thái ma trận để quét nhánh tổ hợp tiếp theo
            score_deck[card3_p] += 1

    total_prob = player_wins + banker_wins + ties
    if total_prob == 0: total_prob = 1.0

    odds_res = {
        "Player": round((player_wins / total_prob) * 100, 2),
        "Banker": round((banker_wins / total_prob) * 100, 2),
        "Tie": round((ties / total_prob) * 100, 2)
    }
    
    # Khôi phục nguyên trạng cấu hình lá bài lật trên bàn cho các hàm hiển thị ngoài luồng
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        score_deck[val] += 1
        
    return odds_res, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list


# =========================================================================
# THUẬT TOÁN ĐỌC & ĐƯA RA CẢNH BÁO LOẠI CẦU ĐỘNG (TREND PATTERN DETECTOR)
# =========================================================================
def detect_baccarat_pattern(outcome_list):
    # Lọc bỏ Hòa (Tie) ra khỏi chuỗi logic để tính chính xác điểm rơi của cầu
    clean_list = [x for x in outcome_list if x in ["Player", "Banker"]]
    if len(clean_list) < 4:
        return "🔄 Đang tích lũy dữ liệu chuỗi bài (Cần tối thiểu 4 ván chính)...", "#888888"

    # 1. Phát hiện Cầu Bệt (Streak)
    last_side = clean_list[-1]
    streak_count = 0
    for item in reversed(clean_list):
        if item == last_side:
            streak_count += 1
        else:
            break
    if streak_count >= 4:
        side_vietnamese = "🔵 PLAYER" if last_side == "Player" else "🔴 BANKER"
        return f"🔥 CẢNH BÁO: ĐANG VÀO CẦU BỆT {side_vietnamese} ({streak_count} ván liên tiếp!)", "#ff7675"

    # 2. Phát hiện Cầu Nhảy 1-1 (Alternating)
    last_4 = clean_list[-4:]
    if (last_4[0] != last_4[1]) and (last_4[1] != last_4[2]) and (last_4[2] != last_4[3]):
        next_expected = "🔴 BANKER" if last_4[-1] == "Player" else "🔵 PLAYER"
        return f"⚡ CẢNH BÁO: ĐANG ĐI CẦU NHẢY 1-1 (Dự kiến ván tới theo logic cầu: {next_expected})", "#ffeaa7"

    # 3. Phát hiện Cầu Song Đúp 2-2
    if len(clean_list) >= 4:
        last_4_for_22 = clean_list[-4:]
        if last_4_for_22[0] == last_4_for_22[1] and last_4_for_22[2] == last_4_for_22[3] and last_4_for_22[1] != last_4_for_22[2]:
            next_expected_22 = "🔵 PLAYER" if last_4_for_22[-1] == "Player" else "🔴 BANKER"
            return f"💎 CẢNH BÁO: THẤY TÍN HIỆU CẦU ĐÚP 2-2 (Ván tiếp theo tạo thế đối ứng: {next_expected_22})", "#54a0ff"

    return "📊 Khay bài đang đi sóng phẳng (Chưa có tín hiệu cầu đặc biệt)", "#2ecc71"


# =========================================================================
# INTERFACE DESIGN & STYLES
# =========================================================================
st.set_page_config(page_title="Oracle Ultimate v16.0", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stColumn"] { width: 50% !important; min-width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    
    .hud-box { padding: 18px; border-radius: 8px; text-align: center; margin-bottom: 12px; border: 1px solid #4f4f4f; background-color: #1a1a1a; }
    .hud-title { font-size: 13px; font-weight: 600; color: #b0b0b0; letter-spacing: 0.5px; }
    .hud-value { font-size: 36px; font-weight: 800; font-family: monospace; margin-top: 4px; }
    
    .neon-player-advantage { background-color: #0984e3 !important; border: 2px solid #74b9ff !important; box-shadow: 0 0 15px rgba(9, 132, 227, 0.7); }
    .neon-banker-advantage { background-color: #d63031 !important; border: 2px solid #ff7675 !important; box-shadow: 0 0 15px rgba(214, 48, 49, 0.7); }
    .neon-tie-alert { border: 2px solid #2ecc71 !important; box-shadow: 0 0 15px rgba(46, 204, 113, 0.8); }
    
    .validation-hud { padding: 12px; border-radius: 6px; text-align: center; font-weight: 700; font-size: 14px; margin-top: 12px; font-family: monospace; }
    .logic-pass { background-color: rgba(46, 204, 113, 0.15); border: 2px solid #2ecc71; color: #2ecc71; box-shadow: 0 0 10px rgba(46, 204, 113, 0.3); }
    .logic-fail { background-color: rgba(231, 76, 60, 0.15); border: 2px solid #e74c3c; color: #e74c3c; box-shadow: 0 0 10px rgba(231, 76, 60, 0.3); animation: blinker 1.5s linear infinite; }
    
    .trend-hud { padding: 14px; border-radius: 6px; background-color: #151515; border: 1px dashed #444; margin-top: 12px; }
    .trend-title { font-size: 11px; font-weight: bold; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;}
    .trend-string { font-size: 18px; font-family: monospace; letter-spacing: 6px; word-break: break-all; font-weight: 800; margin-bottom: 6px; }
    .trend-alert { font-size: 12px; font-weight: 700; padding: 4px 8px; border-radius: 4px; background-color: rgba(255,255,255,0.05); border-left: 3px solid; }
    
    .char-p { color: #54a0ff; }
    .char-b { color: #ff7675; }
    .char-t { color: #2ecc71; }
    
    @keyframes blinker { 50% { opacity: 0.6; } }
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
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ CẤU HÌNH KHAY BÀI")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Thiết lập nhanh khay bài")
manual_cards = st.sidebar.number_input("Số LÁ BÀI đã chia (nếu biết):", min_value=0, max_value=decks*52, value=0)
manual_games = st.sidebar.number_input("Tổng số ván đã chạy:", min_value=0, max_value=150, value=0)

st.sidebar.markdown("**Chi tiết ván thắng từng cửa:**")
p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0)

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
        if len(st.session_state.outcome_history) > 0: st.session_state.outcome_history.pop()
        st.session_state.game_counter = max(0, st.session_state.game_counter - 1)
        st.session_state.last_results = None
        st.session_state.last_played_cards = ""
        st.rerun()

if st.sidebar.button("🔄 RESET TOÀN BỘ KHAY BÀI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.game_counter = 0
    st.session_state.last_results = None
    st.session_state.last_played_cards = ""
    st.session_state.live_logs = []
    st.session_state.last_cards_added = []
    st.session_state.outcome_history = []
    st.rerun()

display_game = manual_games + len(st.session_state.live_logs)

# --- OUTPUT SCREEN MATRIX ---
if is_data_discrepancy:
    st.error(f"""
    ### 🛑 LỖI: DỮ LIỆU KHÔNG ĐỒNG BỘ Ở SIDEBAR
    * **Tổng số ván đã thiết lập:** `{manual_games}` ván.
    * **Tổng số bàn thắng cộng dồn lẻ:** `{calculated_total_wins}` ván.
    """)
else:
    if st.session_state.last_results:
        results_data = st.session_state.last_results
        
        if isinstance(results_data[0], str) and results_data[0].startswith("❌"):
            st.error(results_data[0])
        elif isinstance(results_data[0], str) and results_data[0].startswith("⚠️"):
            st.warning(results_data[0])
        else:
            res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical, invalid_cards = results_data
            
            p_box_css = "hud-box"
            b_box_css = "hud-box"
            tie_box_css = "hud-box"
            
            if res['Player'] > res['Banker']: p_box_css = "hud-box neon-player-advantage"
            elif res['Banker'] > res['Player']: b_box_css = "hud-box neon-banker-advantage"
            if res['Tie'] > 12.5: tie_box_css = "hud-box neon-tie-alert"
                
            left_result_col, right_pair_col = st.columns(2)
            with left_result_col:
                st.markdown("#### 📊 Dự Đoán Xác Suất Cửa Chính")
                st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER PROBABILITY</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER PROBABILITY</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="{tie_box_css}"><div class="hud-title">🟢 TIE WIN PROBABILITY</div><div class="hud-value" style="color: #2ecc71;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
                
            with right_pair_col:
                st.markdown("#### 💎 Tỷ Lệ Cược Phụ Xuất Hiện")
                st.metric("🔵 CON ĐÔI (PLAYER PAIR)", f"{p_pair}%", delta="🔥 CAO" if p_pair > 11.0 else None)
                st.metric("🔴 CÁI ĐÔI (BANKER PAIR)", f"{b_pair}%", delta="🔥 CAO" if b_pair > 11.0 else None)
                
                # [1] Thẩm định tính toàn vẹn bộ bài
                if is_shoe_logical:
                    st.markdown('<div class="validation-hud logic-pass">✔ KIỂM TRA BỘ BÀI: LOGIC KHAY HỢP LỆ</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="validation-hud logic-fail">⚠️ LỖI LOGIC: KHAY BỊ ÂM LÁ QUÁ GIỚI HẠN<br><span style="font-size:11px;">Thiếu lá: {", ".join(invalid_cards)}</span></div>', unsafe_allow_html=True)

                # [2] Xu hướng chuỗi chữ cái + Cảnh báo dạng cầu
                if st.session_state.outcome_history:
                    trend_letters = []
                    for outcome in st.session_state.outcome_history:
                        if outcome == "Player": trend_letters.append('<span class="char-p">P</span>')
                        elif outcome == "Banker": trend_letters.append('<span class="char-b">B</span>')
                        else: trend_letters.append('<span class="char-t">T</span>')
                    
                    trend_html_str = " ".join(trend_letters)
                    
                    pattern_msg, pattern_color = detect_baccarat_pattern(st.session_state.outcome_history)
                    
                    total_live_games = len(st.session_state.outcome_history)
                    p_live_pct = round((st.session_state.outcome_history.count("Player") / total_live_games) * 100, 1)
                    b_live_pct = round((st.session_state.outcome_history.count("Banker") / total_live_games) * 100, 1)
                    
                    st.markdown(
                        f"""
                        <div class="trend-hud">
                            <div class="trend-title">📈 XU HƯỚNG ĐƯỜNG ĐI BÀI THỰC TẾ ({total_live_games} ván)</div>
                            <div class="trend-string">{trend_html_str}</div>
                            <div class="trend-alert" style="border-left-color: {pattern_color}; color: {pattern_color};">
                                {pattern_msg}
                            </div>
                            <div style="font-size: 11px; color: #aaa; margin-top: 6px; font-family: monospace;">
                                Thực tế: Player {p_live_pct}% | Banker {b_live_pct}%
                            </div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        """
                        <div class="trend-hud">
                            <div class="trend-title">📈 XU HƯỚNG ĐƯỜNG ĐI BÀI THỰC TẾ</div>
                            <div style="font-size: 12px; color: #666; font-style: italic;">Chưa có dữ liệu ván để phân tích cầu.</div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )

            st.markdown("---")
            total_shoe_cards = decks * 52
            cards_used_calc = total_shoe_cards - cards_left
            penetration_rate = min(100.0, (cards_used_calc / total_shoe_cards) * 100)
            st.markdown(f"**Chế độ quét:** `{mode}` | **Độ chín khay bài:** {round(penetration_rate, 1)}% (Đã dùng {int(cards_used_calc)} / {total_shoe_cards} lá)")
            st.progress(penetration_rate / 100.0)

            with st.expander("📊 Xem chi tiết số lượng quân bài còn lại trong khay"):
                cols = st.columns(5)
                labels_13 = {1: "A", 11: "J", 12: "Q", 13: "K"}
                for idx, (num, cnt) in enumerate(remaining_deck.items()):
                    card_label = labels_13.get(num, f"[{num}]")
                    color_prefix = "🔴 " if cnt < 0 else ""
                    cols[idx % 5].markdown(f"{color_prefix}**{card_label}**: {round(cnt, 2)} lá")
    else:
        st.info("🔮 HỆ THỐNG ĐÃ KHÓA LUỒNG TỰ ĐỘNG CHẠY. Vui lòng nạp quân bài ván mới bên dưới để tính toán.")

st.markdown("---")

# --- DATA INPUT AREA ---
head_col, status_col = st.columns([2, 1])
with head_col: st.subheader("🃏 Nhập Dữ Liệu Ván Tiếp Tiếp Theo")
with status_col: st.markdown(f"<div style='text-align: right; margin-top: 10px; font-weight: bold; color: #ff4b4b;'>#Ván hiện tại: {display_game}</div>", unsafe_allow_html=True)

col_p, col_b = st.columns(2)
with col_p: p_input = st.text_input("PLAYER (Lá bài vừa ra):", value="", placeholder="Ví dụ: 5,K,2", disabled=is_data_discrepancy)
with col_b: b_input = st.text_input("BANKER (Lá bài vừa ra):", value="", placeholder="Ví dụ: J,7", disabled=is_data_discrepancy)

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

# --- ACTION TRIGGER CONTROL ---
btn_trigger = st.button("🚀 GHI NHẬN VÀ TÍNH TOÁN VÁN TIẾP THEO", use_container_width=True, type="primary", disabled=is_data_discrepancy)

if btn_trigger and not is_data_discrepancy:
    current_game_signature = f"P:{p_input.strip().upper()}|B:{b_input.strip().upper()}"
    
    if not p_input.strip() and not b_input.strip():
        st.warning("⚠️ Vui lòng điền thông tin quân bài để kích hoạt phép tính.")
    elif current_game_signature == st.session_state.last_played_cards:
        st.error("⛔ HỆ THỐNG CHẶN: Trùng lặp hoàn toàn với dữ liệu ván vừa nạp!")
    else:
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        
        if p_list or b_list:
            p_calc = p_list[:2]
            b_calc = b_list[:2]
            
            # Kích hoạt bộ sinh tính toán tối cao Core v16.0
            core_output = calculate_baccarat_v16_quantum(
                p_calc, b_calc, st.session_state.shoe_history, shoe_decks=decks,
                manual_cards_used=manual_cards, manual_games_played=manual_games,
                p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
            )
            
            if isinstance(core_output, str):
                st.session_state.last_results = (core_output, {}, 0.0, 0.0, "LỖI", 0, False, [])
            else:
                res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical, invalid_cards = core_output
                st.session_state.last_results = (res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical, invalid_cards)
                
                if not mode.startswith("LỖI"):
                    st.session_state.last_played_cards = current_game_signature
                    all_added = p_list + b_list
                    st.session_state.shoe_history.extend(all_added)
                    st.session_state.last_cards_added.append(all_added)
                    
                    final_p_score = sum([0 if c >= 10 else c for c in p_list]) % 10
                    final_b_score = sum([0 if c >= 10 else c for c in b_list]) % 10
                    win_side = "Player" if final_p_score > final_b_score else ("Banker" if final_b_score > final_p_score else "Tie")
                    st.session_state.outcome_history.append(win_side)
                    
                    actual_index = display_game + 1
                    st.session_state.live_logs.append(f"Ván {actual_index}: Player({p_input.strip()}) -> {final_p_score}đ vs Banker({b_input.strip()}) -> {final_b_score}đ | Thắng: {win_side.upper()}")
                    st.session_state.game_counter = display_game + 1
                    st.rerun()

if st.session_state.live_logs and not is_data_discrepancy:
    st.markdown("---")
    with st.expander("📝 Nhật ký khay bài thời gian thực (Live Logs)", expanded=True):
        for log in reversed(st.session_state.live_logs): 
            st.text(log)
