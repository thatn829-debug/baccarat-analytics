# =========================================================================
# LÕI CẬP NHẬT v54.1: THÊM BỘ BÙ SAI SỐ KHI THIẾU DỮ LIỆU ĐẦU KHAY
# =========================================================================
def calculate_v54_zero_error_engine(all_rounds_log, shoe_decks, side_p_wins, side_b_wins, side_t_wins):
    total_initial_cards = shoe_decks * 52
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    all_flat_cards = []
    valid_rounds_count = len(all_rounds_log)
    
    current_streak_side = None
    current_streak_count = 0
    decay_factor = 0.88 
    weighted_margins = []
    
    for idx, r in enumerate(all_rounds_log):
        all_flat_cards.extend(r['p_cards'] + r['b_cards'])
        margin = abs(r['p_score'] - r['b_score'])
        distance = valid_rounds_count - 1 - idx
        weight = decay_factor ** distance
        weighted_margins.append(margin * weight)
        
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
    
    score_counts = [0.0] * 10
    for card_num, count in exact_cards_left.items():
        if card_num >= 10: score_counts[0] += count
        else: score_counts[card_num] += count
        
    p_0 = score_counts[0] / cards_remaining      
    p_low = sum(score_counts[1:6]) / cards_remaining   
    p_high = sum(score_counts[6:10]) / cards_remaining 
    p_six = exact_cards_left[6] / cards_remaining 

    # 🔥 ĐIỀU CHỈNH CHÍ MẠNG: Khử nhiễu biến thiên khi số ván nhập vào quá ít (< 3 ván)
    if valid_rounds_count < 3:
        volatility_index = 12.5 # Đưa về mức ổn định mặc định, không cho vọt lên 50%
        volatility_velocity = 0.0
        kalman_gain = 0.70 # Mở khóa bộ lọc để cho phép tính toán sớm
    else:
        # Khi đã đủ dữ liệu, quay lại tính toán toán học nghiêm ngặt
        if len(weighted_margins) >= 2:
            volatility_index = min(50.0, (float(np.var(weighted_margins)) / 4.5) * 100.0)
        else:
            volatility_index = 12.5

        v_prev = (float(np.var(weighted_margins[:-1])) / 4.5) * 100.0 if len(weighted_margins) > 2 else 12.5
        volatility_velocity = volatility_index - v_prev
        
        kalman_modifier = 1.35 if volatility_velocity < -1.0 else (0.65 if volatility_velocity > 1.0 else 1.0)
        kalman_gain = max(0.05, (1.0 - (volatility_index / 50.0)) * kalman_modifier)

    # Phần tính toán nền xác suất giữ nguyên
    math_bias = (p_low * 0.18) - (p_high * 0.13) + (p_0 * 0.07)
    base_p = 44.62 + (math_bias * 100.0)
    base_b = 45.86 - (math_bias * 100.0)
    base_t = 9.52 + (p_0 * 8.0)

    if p_six > 0.09:
        commission_penalty = (p_six * 15.0) * kalman_gain
        base_b -= commission_penalty
        base_p += commission_penalty * 0.3

    is_critical_break = False
    break_boost = 0.0
    
    if current_streak_side and current_streak_count >= 3:
        markov_factor = 1.0 - (1.0 / (2.0 ** (current_streak_count - 2)))
        if volatility_velocity <= 0.5: # Nới rộng biên độ chấp nhận gia tốc bão để bắt bẻ cầu nhạy hơn
            if current_streak_side == "Banker" and (p_low < 0.38 or p_0 > 0.36):
                is_critical_break = True
                break_boost = (40.0 * markov_factor) * (1.0 + penetration_rate)
            elif current_streak_side == "Player" and (p_high > 0.42 or p_0 > 0.36):
                is_critical_break = True
                break_boost = (40.0 * markov_factor) * (1.0 + penetration_rate)

    if is_critical_break:
        if current_streak_side == "Banker":
            base_p += break_boost * kalman_gain
            base_b -= break_boost * kalman_gain * 0.85
        elif current_streak_side == "Player":
            base_b += break_boost * kalman_gain
            base_p -= break_boost * kalman_gain * 0.85
    else:
        delta_diff = base_p - base_b
        if abs(delta_diff) > 0.1:
            amplifier = 1.0 + (5.5 * kalman_gain * (1.0 + penetration_rate))
            base_p += (delta_diff * amplifier)
            base_b -= (delta_diff * amplifier)

    base_p = max(1.0, min(97.0, base_p))
    base_b = max(1.0, min(97.0, base_b))
    base_t = max(2.0, min(42.0, base_t))
    
    total_sum = base_p + base_b + base_t
    return (base_p / total_sum) * 100, (base_b / total_sum) * 100, (base_t / total_sum) * 100, int(cards_remaining), volatility_index, volatility_velocity, kalman_gain, current_streak_side, current_streak_count, is_critical_break, p_six
