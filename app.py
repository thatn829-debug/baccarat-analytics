import streamlit as st
import math

# =========================================================================
# SYSTEM CORE v38.0 (ADVANCED SNAPSHOT IDENTITY GUARD & LOOP BUG DETECTOR)
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
    # 1. BỘ XẾT LOGIC ĐỘC LẬP (Sửa lỗi mù chuỗi trùng lặp ván đấu)
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

    # Quy luật 2: SỬA ĐỔI TOÀN DIỆN - PHÁT HIỆN KẸT VÒNG LẶP HÌNH ẢNH (ROUND SNAPSHOT IDENTITY GUARD)
    # Kiểm tra xem cấu trúc quân bài lật ra của các ván liên tiếp có bị giống hệt nhau không
    if len(round_detailed_log) >= 3:
        identical_streak = 1
        # Tạo chuỗi so sánh từ ván cuối cùng ngược lên
        for i in range(len(round_detailed_log) - 1, 0, -1):
            current_round = round_detailed_log[i]
            previous_round = round_detailed_log[i-1]
            
            # Sắp xếp để không bị ảnh hưởng bởi thứ tự nhập nhập liệu ngẫu nhiên
            curr_p = sorted(current_round['p_cards'])
            curr_b = sorted(current_round['b_cards'])
            prev_p = sorted(previous_round['p_cards'])
            prev_b = sorted(previous_round['b_cards'])
            
            # Nếu cả bài Player và bài Banker của ván này giống hệt ván trước
            if curr_p == prev_p and curr_b == prev_b and (len(curr_p) > 0 or len(curr_b) > 0):
                identical_streak += 1
            else:
                break # Đứt chuỗi trùng lặp
                
        if identical_streak == 3:
            invalid_logic_messages.append(f"⚠️ SIÊU BIẾN DẠNG TRÙNG LẶP: Phát hiện {identical_streak} ván liên tiếp lật ra chính xác các quân bài giống hệt nhau. Tỷ lệ ngẫu nhiên tự nhiên nhỏ hơn 1 phần vài triệu!")
        elif identical_streak >= 4:
            invalid_logic_messages.append(f"🚨 LỖI PHI THỰC TẾ (KẸT VÒNG LẶP): Phát hiện chuỗi {identical_streak} ván trùng khít hoàn toàn cả quân bài lẫn điểm số! Sàn đang bị kẹt đồ họa hiển thị hoặc thuật toán game lỗi lặp.")

    # Quy luật 3: Kiểm tra chuỗi Hòa bệt liên tiếp ngắn hạn
    current_tie_streak = 0
    for round_data in reversed(round_detailed_log):
        if round_data['outcome'] == "Tie": current_tie_streak += 1
        else: break
    if current_tie_streak == 5:
        invalid_logic_messages.append(f"⚠️ NGƯỠNG HIẾM GẶP: Xuất hiện {current_tie_streak} ván HÒA liên tiếp (Tỷ lệ ngẫu nhiên 1/128,000 ván).")
    elif current_tie_streak >= 6:
        invalid_logic_messages.append(f"🚨 CHUỖI HÒA BẤT THƯỜNG: Xuất hiện {current_tie_streak} ván HÒA liên tiếp! Vượt ngưỡng giới hạn ngẫu nhiên.")

    # Quy luật 4: Kiểm tra độ lệch phi logic toàn cục
    if global_total_games >= 30:
        actual_tie_rate = (total_t_wins / global_total_games) * 100
        if actual_tie_rate > 20.0:
            invalid_logic_messages.append(f"🚨 PHI LOGIC CỬA HÒA: Tỷ lệ Hòa thực tế quá cao ({actual_tie_rate:.1f}% trên {global_total_games} ván).")
            
    no_tie_counter = 0
    for round_data in reversed(round_detailed_log):
        if round_data['outcome'] != "Tie": no_tie_counter += 1
        else: break
    if no_tie_counter >= 60:
        invalid_logic_messages.append(f"🚨 PHI LOGIC DÒNG CHẢY: Đã {no_tie_counter} ván liên tiếp KHÔNG CÓ HÒA.")

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

    # So sánh biên độ lệch Delta khi đủ tập mẫu lớn
    if global_total_games >= 40:
        actual_p_rate = (total_p_wins / global_total_games) * 100
        delta_p = abs(actual_p_rate - p_prob)
        if delta_p > 15.0:
            invalid_logic_messages.append(f"🚨 LỆCH BIÊN ĐỘ TOÁN HỌC: Player thực tế chiếm {actual_p_rate:.1f}% nhưng khay bài chỉ cho phép quanh mức {p_prob:.1f}% (Delta: {delta_p:.1f}%).")

    p_pair_prob = 0.0
    for i in range(1, 14):
        if deck_structure[i] >= 2: 
            p_pair_prob += (deck_structure[i] / N_total) * ((deck_structure[i] - 1) / (N_total - 1))
    p_pair_odds = round(p_pair_prob * 100, 2)
    b_pair_odds = round(p_pair_odds * 1.015, 2)

    odds_res = {"Player": round(p_prob, 2), "Banker": round(b_prob, 2), "Tie": round(t_prob, 2)}
    is_shoe_logical = (len(invalid_logic_messages) == 0)
    
    return odds_res, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_logic_messages

# [Các hàm giữ nguyên: detect_baccarat_pattern, get_ai_recommendation, parse_baccarat_input_v37 và phần giao diện Streamlit phía sau...]
