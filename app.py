import streamlit as st
import numpy as np
import math

# =========================================================================
# 🔵 AI AGENT 1: PLAYER COGNITIVE - ULTRA-PRECISION HAWKING SINGULARITY
# =========================================================================
class PlayerQuantumAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive, burn_cards):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        
        sidebar_total_rounds = manual_p + manual_b + manual_t
        estimated_cards_removed = (sidebar_total_rounds * 4.9452) + burn_cards
        
        if estimated_cards_removed > 0:
            cards_per_rank_removed = estimated_cards_removed / 13.0
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - cards_per_rank_removed)

        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        total_initial_cards = shoe_decks * 52.0
        
        shoe_exhaustion_ratio = (total_initial_cards - cards_remaining) / total_initial_cards
        # v70.0: Phóng đại phi tuyến tính động lực EOR khi khay bài dần cạn
        dynamic_eor_multiplier = 4.85 * (1.0 + 0.65 * (shoe_exhaustion_ratio ** 2))
        gravitational_warp = 1.0 / (1.0 - min(0.96, shoe_exhaustion_ratio)) 

        p_eor_base = {
            1: -0.0051, 2: -0.0059, 3: -0.0062, 4: -0.0134, 5: -0.0096, 
            6: +0.0123, 7: +0.0144, 8: +0.0095, 
            9: -0.0026, 10: +0.0043, 11: +0.0043, 12: +0.0043, 13: +0.0043
        }
        
        card_effect_sum = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            card_effect_sum += removed * p_eor_base[card_num] * gravitational_warp

        final_card_bias = card_effect_sum * dynamic_eor_multiplier

        trend_force = 0.0
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
            
            effective_streak = min(streak_count, 18)
            if current_streak_side == "Banker" and effective_streak >= 2:
                trend_force += 3.1416 * (effective_streak ** 1.95) / (1.0 + 0.025 * (effective_streak ** 1.95))

        if total_decisive > 0:
            p_ratio = (manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")) / total_decisive
            cosmic_microwave_bias = p_ratio - 0.4932
            # Hồi quy tiệm cận tuyến tính động để tránh việc lệch tỉ số kéo dài làm nhiễu công thức tính ván ngắn hạn
            trend_force -= cosmic_microwave_bias * (22.5 / (1.0 + 0.01 * total_decisive)) 

        return 44.62 + final_card_bias + trend_force


# =========================================================================
# 🔴 AI AGENT 2: BANKER COGNITIVE - HIGH-PRECISION SCHRODINGER WAVE
# =========================================================================
class BankerMarkovAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive, burn_cards):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        
        sidebar_total_rounds = manual_p + manual_b + manual_t
        estimated_cards_removed = (sidebar_total_rounds * 4.9452) + burn_cards
        
        if estimated_cards_removed > 0:
            cards_per_rank_removed = estimated_cards_removed / 13.0
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - cards_per_rank_removed)

        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        total_initial_cards = shoe_decks * 52.0
        shoe_exhaustion_ratio = (total_initial_cards - cards_remaining) / total_initial_cards
        dynamic_eor_multiplier = 4.85 * (1.0 + 0.65 * (shoe_exhaustion_ratio ** 2))
        gravitational_warp = 1.0 / (1.0 - min(0.96, shoe_exhaustion_ratio))

        b_eor_base = {
            1: +0.0051, 2: +0.0059, 3: +0.0062, 4: +0.0134, 5: +0.0096, 
            6: -0.0123, 7: -0.0144, 8: -0.0095, 
            9: +0.0026, 10: -0.0043, 11: -0.0043, 12: -0.0043, 13: -0.0043
        }
        
        card_effect_sum = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            card_effect_sum += removed * b_eor_base[card_num] * gravitational_warp

        final_card_bias = card_effect_sum * dynamic_eor_multiplier

        trend_force = 0.0
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
            
            effective_streak = min(streak_count, 18)
            if current_streak_side == "Player" and effective_streak >= 2:
                trend_force += 3.1416 * (effective_streak ** 1.95) / (1.0 + 0.025 * (effective_streak ** 1.95))
            
            if current_streak_side == "Banker" and effective_streak >= 3:
                wave_damping = MathQuantumUniverse.quantum_wave_damping(effective_streak)
                trend_force -= wave_damping

        if total_decisive > 0:
            b_ratio = (manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")) / total_decisive
            cosmic_microwave_bias = b_ratio - 0.5068
            trend_force -= cosmic_microwave_bias * (22.5 / (1.0 + 0.01 * total_decisive))

        return 45.86 + final_card_bias + trend_force


# =========================================================================
# 🟢 AI AGENT 3: TIE COGNITIVE - RIEMANN ZETA EXTENDED
# =========================================================================
class TieHypergeometricAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        
        sidebar_total_rounds = manual_p + manual_b + manual_t
        estimated_cards_removed = (sidebar_total_rounds * 4.9452) + burn_cards
        
        if estimated_cards_removed > 0:
            cards_per_rank_removed = estimated_cards_removed / 13.0
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - cards_per_rank_removed)

        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
                    
        cards_remaining = int(max(1.0, sum(exact_cards_left.values())))
        zero_cards = int(sum([exact_cards_left[i] for i in [10, 11, 12, 13]]))
        non_zero_cards = cards_remaining - zero_cards
        
        if cards_remaining >= 6:
            c1 = MathQuantumUniverse.lgamma_comb(zero_cards, 3)
            c2 = MathQuantumUniverse.lgamma_comb(non_zero_cards, 3)
            c3 = MathQuantumUniverse.lgamma_comb(cards_remaining, 6)
            prob_zero_tie = (c1 * c2) / max(1.0, c3)
        else:
            prob_zero_tie = 0.0

        actual_density = zero_cards / float(cards_remaining)
        standard_density = 16.0 / 52.0
        density_deviation = actual_density - standard_density
        
        riemann_zeta_factor = 1.64493 
        base_probability = 9.52 + (density_deviation * 45.0) + (prob_zero_tie * 150.0 * riemann_zeta_factor)

        streak_multiplier = 1.0
        gap_bonus = 0.0
        
        if all_rounds_log:
            gap_since_last_tie = 0
            for r in reversed(all_rounds_log):
                if r['outcome'] == "Tie":
                    break
                gap_since_last_tie += 1
            
            if gap_since_last_tie > 8:
                gap_bonus += min(12.5, (gap_since_last_tie - 8) * 1.15)

            decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
            if len(decisive_outcomes) >= 3:
                current_streak_side = decisive_outcomes[-1]
                streak_count = 0
                for outcome in reversed(decisive_outcomes):
                    if outcome == current_streak_side:
                        streak_count += 1
                    else:
                        break
                
                if streak_count >= 3:
                    streak_multiplier += (streak_count * 0.18)
                
                if len(decisive_outcomes) >= 4 and decisive_outcomes[-2] != decisive_outcomes[-1]:
                    prev_streak_side = decisive_outcomes[-2]
                    prev_streak_count = 0
                    for outcome in reversed(decisive_outcomes[:-1]):
                        if outcome == prev_streak_side:
                            prev_streak_count += 1
                        else:
                            break
                    if prev_streak_count >= 3:
                        gap_bonus += 5.5

        final_tie_prob = (base_probability * streak_multiplier) + gap_bonus
        return max(0.5, min(55.0, final_tie_prob))


# =========================================================================
# 🪐 MATH QUANTUM UNIVERSE UTILITIES
# =========================================================================
class MathQuantumUniverse:
    @staticmethod
    def lgamma_comb(n, k):
        if k < 0 or k > n: return 0.0
        if k == 0 or k == n: return 1.0
        return math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1))

    @staticmethod
    def quantum_wave_damping(streak):
        return 2.0 * (streak ** 1.35) / (1.0 + 0.06 * (streak ** 1.35))


# =========================================================================
# 💡 MODULE 4: FUSION DISTRIBUTOR & SIMULATOR
# =========================================================================
def calculate_v67_8_ultimate_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r['outcome'] == "Tie")
    total_decisive = total_p_wins + total_b_wins
    
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, (shoe_decks * 52) - burn_cards, 0, 0, 0, "KHÔNG GIAN TRỐNG", None, 0

    raw_p = PlayerQuantumAgent.compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive, burn_cards)
    raw_b = BankerMarkovAgent.compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive, burn_cards)
    raw_t = TieHypergeometricAgent.compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    
    raw_p = max(0.5, min(99.5, raw_p))
    raw_b = max(0.5, min(99.5, raw_b))
    raw_t = max(0.1, min(49.9, raw_t))
    
    total_sum = raw_p + raw_b + raw_t
    p_pct = (raw_p / total_sum) * 100
    b_pct = (raw_b / total_sum) * 100
    t_pct = (raw_t / total_sum) * 100
    
    total_initial_cards = shoe_decks * 52
    sidebar_rounds = manual_p + manual_b + manual_t
    cards_spent_estimated = (sidebar_rounds * 4.9452) + burn_cards
    cards_spent_actual = sum(len(r['p_cards'] + r['b_cards']) for r in all_rounds_log)
    
    cards_remaining = max(0, int(total_initial_cards - (cards_spent_estimated + cards_spent_actual)))
    
    trend_desc = "CẦU BIẾN ĐỘNG TỰ DO TRONG KHÔNG GIAN METRIC"
    streak_side = None
    streak_count = 0
    decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
    if len(decisive_outcomes) >= 2:
        current_streak_side = decisive_outcomes[-1]
        for outcome in reversed(decisive_outcomes):
            if outcome == current_streak_side: streak_count += 1
            else: break
        if streak_count >= 2:
            streak_side = current_streak_side
            trend_desc = f"SIÊU CHUỖI BỆT {streak_side.upper()} ({streak_count} ván)"

    return p_pct, b_pct, t_pct, cards_remaining, total_p_wins, total_b_wins, total_ties, trend_desc, streak_side, streak_count


def get_ultimate_directive(p_val, b_val, trend_desc, streak_side, streak_count, log, m_p, m_b):
    if not log and (m_p == 0 and m_b == 0):
        return {
            "status": "🛰️ SYSTEM READY",
            "msg": "Hệ thống toán học xác suất lượng tử đã thiết lập. Chờ nạp bài khay mới.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%", "raw_target": "WAIT"
        }
    
    # v70.0: ANTI-CASCADE LOCK - Tự động phát hiện lệch chuỗi ngắn hạn để phanh bảo vệ
    decisive_log = [r for r in log if r.get('arbitrator_target') != "WAIT" and r['outcome'] in ["Player", "Banker"]]
    if decisive_log:
        last_round = decisive_log[-1]
        pred = last_round.get('arbitrator_target') if last_round.get('arbitrator_target') else last_round.get('oracle_target')
        if pred and pred != "WAIT" and pred != last_round['outcome']:
            return {
                "status": "🛑 TRẠNG THÁI CHỜ PHANH BẢO VỆ",
                "msg": "Phát hiện sảnh bài vừa khớp lệnh lệch hướng. Ngắt nhịp bắt buộc để ổn định lại pha sóng toán học.",
                "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0% (QUAN SÁT)", "raw_target": "WAIT"
            }

    diff = abs(p_val - b_val)
    # v70.0: Tăng biên độ lọc nhiễu lên 1.5% để cô lập các ván có tỉ lệ tiệm cận cân bằng rủi ro cao
    if diff < 1.5:
        return {
            "status": "🛑 KHÓA LỆNH AN TOÀN",
            "msg": f"Độ lệch biên độ sóng quá hẹp ({diff:.2f}%), từ chối khớp lệnh rủi ro cao.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%", "raw_target": "WAIT"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 THUẬN LỆNH: PLAYER",
            "msg": f"Trường Hawking Singularity nghiêng về phía Player (+{diff:.2f}%).",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "2% - 4% Vốn", "raw_target": "PLAYER"
        }
    else:
        return {
            "status": "🔴 THUẬN LỆNH: BANKER",
            "msg": f"Hàm sóng Schrödinger hội tụ cao về phía Banker (+{diff:.2f}%).",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "2% - 4% Vốn", "raw_target": "BANKER"
        }


# =========================================================================
# 👑 AI SOVEREIGN ORACLE - SIÊU MÔ HÌNH KIỂM SOÁT SAI SỐ KÉP (v70.0)
# =========================================================================
class AISovereignOracle:
    @staticmethod
    def calculate_shannon_entropy(all_rounds_log):
        outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        if len(outcomes) < 4: return 1.0
        p_count = outcomes.count("Player") / len(outcomes)
        b_count = outcomes.count("Banker") / len(outcomes)
        entropy = 0.0
        for p in [p_count, b_count]:
            if p > 0: entropy -= p * math.log2(p)
        return entropy

    @staticmethod
    def analyze_and_suggest(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, p_val, b_val, t_val, cards_left, trend_desc, streak_side, streak_count, total_rounds, burn_cards):
        if total_rounds == 0 and burn_cards == 0:
            return {
                "decision": "👁️ ORACLE v70.0 READY", "target": "QUÉT KHÔNG GIAN...", "capital_allocation": "0%", "strategy_type": "Quantum Calibration 2026",
                "ai_insight": "Siêu máy tính tối cao đã liên kết và chuẩn hóa trường dữ liệu khay bài.",
                "risk_level": "Chờ đồng bộ", "color": "#a855f7", "memory_hud": "Không gian Hilbert trống", "cyber_knowledge": "Đang định vị hằng số...",
                "raw_code": "EMPTY_ORACLE"
            }

        # 🛑 v70.0: THEO DÕI ĐỘ LỆCH CHUỖI TÍCH LŨY (CUMULATIVE DISTORTION)
        wrong_count = 0
        decisive_log = [r for r in all_rounds_log if r.get('arbitrator_target') != "WAIT" and r['outcome'] in ["Player", "Banker"]]
        
        if decisive_log:
            last_round = decisive_log[-1]
            pred = last_round.get('arbitrator_target') if last_round.get('arbitrator_target') else last_round.get('oracle_target')
            if pred and pred != "WAIT" and pred != last_round['outcome']:
                wrong_count = 1  

        if len(decisive_log) >= 2:
            temp_wrong = 0
            for r in reversed(decisive_log[-2:]):
                p_check = r.get('arbitrator_target') if r.get('arbitrator_target') else r.get('oracle_target')
                if p_check and p_check != "WAIT" and p_check != r['outcome']:
                    temp_wrong += 1
            if temp_wrong >= 2:
                wrong_count = 2

        initial_cards = float(4 * shoe_decks)
        exact_cards_left = {i: initial_cards for i in range(1, 14)}
        
        sidebar_rounds = manual_p + manual_b + manual_t
        estimated_removed = (sidebar_rounds * 4.9452) + burn_cards
        if estimated_removed > 0:
            rank_removed = estimated_removed / 13.0
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - rank_removed)

        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left: exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)

        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        shoe_progress = (shoe_decks * 52.0 - total_cards_remaining) / (shoe_decks * 52.0)

        memory_hud = f"🧬 HILBERT MAP ➡️ Đã quét: {int(shoe_decks*52 - total_cards_remaining)} lá | Tiến độ khay: {shoe_progress*100:.1f}%"
        entropy_score = AISovereignOracle.calculate_shannon_entropy(all_rounds_log)
        cyber_knowledge = f"🔭 BACKGROUND: Entropy = {entropy_score:.4f} | Sai lệch tích lũy: {wrong_count}/2"

        # KÍCH HOẠT LÁ CHẮN CHỐNG CHUỖI THUA SAI LIÊN TIẾP LẬP TỨC TRONG v70.0
        if wrong_count == 1:
            return {
                "decision": "🛑 PHANH CHỐNG CHUỖI SAI (v70.0)", "target": "WAIT (KHÔNG VÀO LỆNH)", "capital_allocation": "0.0% (An Toàn)", "strategy_type": "ANTI-WHIPSAW SHIELD",
                "ai_insight": "Ván vừa rồi ghi nhận dự đoán bị lệch pha với sảnh. Để bẻ gãy chuỗi sai dây chuyền do quán tính sảnh bài biến dị, hệ thống ép trạng thái nghỉ quan sát 1 ván nhằm đồng bộ hóa dữ liệu.",
                "risk_level": "Nguy cơ lệch pha cao", "color": "#f1c40f", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                "raw_code": "SINGLE_ERROR_LOCK"
            }
        elif wrong_count >= 2:
            return {
                "decision": "🚨 KHÓA HỆ THỐNG KHẨN CẤP (BÁO ĐỘNG ĐỎ)", "target": "STOP & WAIT", "capital_allocation": "0.0% (Phong Tỏa Quỹ)", "strategy_type": "EMERGENCY COLD SYSTEM",
                "ai_insight": "Cảnh báo nghiêm trọng: Sảnh bài đang chạy chuỗi kết quả dị biệt cực đoan, mô hình toán học đã mất đồng bộ pha liên tiếp. Yêu cầu dừng chơi ngay, thoát bàn hoặc làm mới khay bài khác.",
                "risk_level": "Nguy Hiểm Cực Đại", "color": "#ff4757", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                "raw_code": "FORCE_EMERGENCY_LOCK"
            }

        diff = abs(p_val - b_val)
        intrinsic_target = "PLAYER" if p_val > b_val else "BANKER"

        if diff < 1.5:
            return {
                "decision": "🛑 TUYỆT ĐỐI KHÓA LỆNH", "target": "WAIT", "capital_allocation": "0.0%", "strategy_type": "QUANTUM SHIELD",
                "ai_insight": f"Biên độ phân tách sóng quá hẹp ({diff:.2f}%). Chỉ số ngẫu nhiên lấn át xung lực xác suất, bảo toàn vốn.",
                "risk_level": "Nhiễu loạn cao", "color": "#e74c3c", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                "raw_code": "SHIELD_SHANNON"
            }

        # Kiểm soát phân bổ vốn Kelly chặt chẽ và chính xác hơn trong v70.0
        raw_kelly = (max(p_val, b_val) / 100.0) - (min(p_val, b_val) / 100.0)
        dynamic_alloc = raw_kelly * 26.0 * (1.0 + 1.2 * shoe_progress)

        if streak_side and streak_count >= 3:
            current_streak_upper = streak_side.upper()
            if intrinsic_target != current_streak_upper:
                is_fibonacci_node = streak_count in [3, 5, 8, 13, 21]
                is_extreme_entropy = (entropy_score < 0.70) and (streak_count >= 6)
                is_powerful_bias = (diff >= 9.5)  
                
                # Nâng cao độ kiểm chuẩn điều kiện bẻ cầu để tránh bẻ cầu non chết dây bệt
                if not (is_powerful_bias or is_extreme_entropy or (is_fibonacci_node and diff >= 6.5)):
                    final_alloc = max(1.5, min(6.0, dynamic_alloc * 0.8))
                    return {
                        "decision": f"🌊 FLOW: NƯƠNG CHUỖI BỆT ➡️ THUẬN {current_streak_upper}", "target": current_streak_upper,
                        "capital_allocation": f"💎 ĐU DÒNG: {final_alloc:.1f}% VỐN", "strategy_type": "🛡️ ANTI-PREMATURE DAMPING v70",
                        "ai_insight": "Ghi nhận dòng bệt dài mạnh. Tuyệt đối không bẻ cầu khi chưa hội tụ đủ động năng toán học, tiếp tục ôm dòng nhẹ nhàng.",
                        "risk_level": "An toàn ổn định", "color": "#cbd5e1", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                        "raw_code": "FLOW_STREAK_PREVENT_PREMATURE"
                    }
                else:
                    final_alloc = max(4.0, min(16.0, dynamic_alloc * 1.5))
                    return {
                        "decision": f"💥 FORCE: BẺ CẦU TỐI CAO ➡️ {intrinsic_target}", "target": intrinsic_target,
                        "capital_allocation": f"🔥 KÝ DỊ: {final_alloc:.1f}% VỐN", "strategy_type": "⚡ HAWKING OVERRIDE",
                        "ai_insight": "Xác suất độc lập độc bản đạt điểm đảo chiều toán học tối cao. Cho phép lệnh kích hoạt bẻ cầu.",
                        "risk_level": "Kiểm soát rủi ro điểm rơi", "color": "#00f5d4", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                        "raw_code": "FORCE_COUNTER_STREAK"
                    }
            else:
                final_alloc = max(3.0, min(12.0, dynamic_alloc * 1.3))
                return {
                    "decision": f"🌊 FLOW: ĐU THEO CHUỖI ➡️ {current_streak_upper}", "target": current_streak_upper,
                    "capital_allocation": f"💎 ĐU DÒNG: {final_alloc:.1f}% VỐN", "strategy_type": "🌊 WAVE EXPANSION",
                    "ai_insight": f"Xác suất độc lập đồng điệu xu thế sảnh. Tiếp tục đẩy lệnh bám sát chuỗi {current_streak_upper}.",
                    "risk_level": "An toàn cao", "color": "#a855f7", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                    "raw_code": "FLOW_STREAK"
                }
        else:
            final_alloc = max(2.0, min(10.0, dynamic_alloc))
            capital_str = f"💎 LỆNH CHUẨN: {final_alloc:.1f}% Vốn"
            strat_type = "🌀 QUANTUM SWEEP"
            risk_lvl = "Kiểm soát đa chiều"
            color = "#38bdf8" if intrinsic_target == "PLAYER" else "#ff4757"
            ai_insight = f"Lực hấp dẫn xác suất độc lập nghiêng về {intrinsic_target} (+{diff:.2f}%)."

        return {
            "decision": f"⚡ LỆNH THẦN: {intrinsic_target}", "target": intrinsic_target, "capital_allocation": capital_str, "strategy_type": strat_type,
            "ai_insight": ai_insight, "risk_level": risk_lvl, "color": color, "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
            "raw_code": "NORMAL_SWEEP"
        }


# =========================================================================
# 🎛️ MODULE 9: QUANTUM ARBITRATION MATRIX (BỘ LỌC TRỌNG TÀI TỐI CAO)
# =========================================================================
class QuantumArbitrationMatrix:
    @staticmethod
    def render_arbitration_logic(multi_cmd, oracle_cmd, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        if not all_rounds_log and (manual_p == 0 and manual_b == 0):
            return "WAIT"

        m_target = multi_cmd['raw_target']    
        o_target = oracle_cmd['target']        
        o_code = oracle_cmd['raw_code']        

        initial_cards = float(4 * shoe_decks)
        exact_cards_left = {i: initial_cards for i in range(1, 14)}
        sidebar_rounds = manual_p + manual_b + manual_t
        estimated_removed = (sidebar_rounds * 4.9452) + burn_cards
        if estimated_removed > 0:
            rank_removed = estimated_removed / 13.0
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - rank_removed)
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left: exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)

        low_cards = sum([exact_cards_left[i] for i in [1, 2, 3, 4, 5]])      
        high_cards = sum([exact_cards_left[i] for i in [10, 11, 12, 13]])    

        has_conflict = False
        rule_title = ""
        rule_desc = ""
        panel_color = "#f1c40f"
        panel_bg = "rgba(241, 196, 15, 0.08)"
        arbitrator_final_verdict = None 

        def target_badge(target_str):
            if target_str == "PLAYER":
                return '<span style="background: rgba(0, 175, 185, 0.25); color: #00afb9; border: 1px solid #00afb9; padding: 2px 6px; border-radius: 4px; font-weight: 800;">🔵 PLAYER</span>'
            elif target_str == "BANKER":
                return '<span style="background: rgba(255, 71, 87, 0.25); color: #ff4757; border: 1px solid #ff4757; padding: 2px 6px; border-radius: 4px; font-weight: 800;">🔴 BANKER</span>'
            return f'<b>{target_str}</b>'

        if o_code == "SINGLE_ERROR_LOCK" or m_target == "WAIT":
            has_conflict = True
            arbitrator_final_verdict = "WAIT"
            rule_title = "⚖️ TRỌNG TÀI - CHẶN CHUỖI SAI LŨY TIẾN KHÁCH QUAN (v70.0)"
            rule_desc = "Phát hiện ván trước hệ thống đoán lệch hướng sảnh bài. Trọng tài kích hoạt lá chắn bảo vệ, <b>HỦY BỎ KHỚP LỆNH TOÀN DIỆN VÁN NÀY</b>. Hãy nhập kết quả ván này để mô hình tái cân bằng pha!"
            panel_color = "#f1c40f"
            panel_bg = "rgba(241, 196, 15, 0.15)"

        elif o_code == "FORCE_EMERGENCY_LOCK":
            has_conflict = True
            arbitrator_final_verdict = "WAIT"
            rule_title = "🚨 TRỌNG TÀI TỐI CAO - KHÓA TÀI KHOẢN KHẨN CẤP"
            rule_desc = "Sảnh bài mất pha toán học liên tiếp. Trọng tài phong tỏa lệnh khớp tiền vô điều kiện nhằm bảo vệ vốn tối đa!"
            panel_color = "#ff4757"
            panel_bg = "rgba(255, 71, 87, 0.15)"

        elif o_code == "SHIELD_SHANNON" and m_target != "WAIT":
            has_conflict = True
            arbitrator_final_verdict = "WAIT"
            rule_title = "⚖️ TRỌNG TÀI TỐI CAO - LÁ CHẮN ĐIỂM KỲ DỊ ENTROPY"
            rule_desc = f"Vùng nhiễu loạn ngẫu nhiên cao, biên độ sóng mỏng dưới ngưỡng an toàn tối thiểu 1.5%. Đóng lệnh."
            panel_color = "#ff4757"
            panel_bg = "rgba(255, 71, 87, 0.12)"

        elif m_target != "WAIT" and o_target != "WAIT" and m_target != o_target:
            has_conflict = True
            if o_code == "FORCE_COUNTER_STREAK":
                arbitrator_final_verdict = o_target
                rule_title = "⚖️ TRỌNG TÀI TỐI CAO - CHUẨN KHỚP LỆNH BẺ CẦU GIỚI HẠN"
                rule_desc = f"Động năng bẻ cầu đạt điểm kích nổ. Khớp lệnh theo Oracle ({target_badge(o_target)}) nhưng **HẠ 50% KHỐI LƯỢNG LỆNH ĐÁNH** để phòng vệ rủi ro."
            else:
                if high_cards > low_cards * 1.15: decision_override = "BANKER"
                elif low_cards > high_cards * 1.15: decision_override = "PLAYER"
                else: decision_override = "WAIT"

                arbitrator_final_verdict = decision_override
                rule_title = "⚖️ TRỌNG TÀI TỐI CAO - XỬ LÝ ĐỘ LỆCH KHÔNG GIAN HILBERT"
                if decision_override != "WAIT":
                    rule_desc = f"Xung đột Agent hệ thống. Trọng tài dùng tỷ trọng mật độ bài thực tế can thiệp: Đánh {target_badge(decision_override)} (Min vốn tối thiểu)."
                else:
                    rule_desc = f"Trường hạt mật độ cân bằng tuyệt đối không rõ xu hướng. BỎ QUA TOÀN DIỆN."
            panel_color = "#00f5d4"
            panel_bg = "rgba(0, 245, 212, 0.1)"

        if has_conflict:
            st.markdown(
                f'<div style="background: {panel_bg}; border: 2px solid {panel_color}; border-radius: 10px; padding: 12px; margin: 10px 0px; box-shadow: 0 0 12px {panel_color}4D;">'
                f'<div style="font-size: 13px; font-weight: 900; color: {panel_color}; letter-spacing: 0.3px; margin-bottom: 4px;">{rule_title}</div>'
                f'<div style="font-size: 12px; color: #f8fafc; line-height: 1.5; text-align: left;">{rule_desc}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            return arbitrator_final_verdict
        return None 


# =========================================================================
# 📦 MODULE 8: QUANTUM AUDIT MATRIX CONTROLLER
# =========================================================================
class QuantumAuditMatrixController:
    @staticmethod
    def render_audit_table(log, start_round_index):
        if not log: return
            
        st.markdown('<div class="audit-matrix-box"><div class="audit-title">📊 BẢNG ĐỐI CHIẾU KIỂM TOÁN LƯỢNG TỬ (v70.0 ULTRA-PRECISION)</div>', unsafe_allow_html=True)
        table_rows = ""
        for idx, r in enumerate(log):
            real_round_num = start_round_index + idx + 1
            oracle_decision = r.get('oracle_decision', '🛑 CHỜ')
            oracle_target = r.get('oracle_target', 'WAIT').upper()
            oracle_alloc = r.get('oracle_alloc', '0%')
            arbitrator_target = r.get('arbitrator_target', None)
            outcome = r['outcome'].upper()
            
            if arbitrator_target is not None:
                active_target = arbitrator_target.upper()
                is_arbitrated = True
            else:
                active_target = oracle_target
                is_arbitrated = False

            if outcome == "TIE":
                dot_html = '<span class="status-dot" style="color: #2ecc71; background-color: #2ecc71;"></span>'
                status_text = "<span style='color:#2ecc71; font-weight:bold;'>HÒA</span>"
            elif "BỎ QUA" in oracle_decision or active_target == "WAIT" or "CHỜ" in oracle_decision:
                dot_html = '<span class="status-dot" style="color: #94a3b8; background-color: #94a3b8;"></span>'
                status_text = "<span style='color:#94a3b8;'>KHÓA</span>"
            elif active_target == outcome:
                dot_html = '<span class="status-dot" style="color: #00f5d4; background-color: #00f5d4; box-shadow: 0 0 10px #00f5d4;"></span>'
                status_text = "<span style='color:#00f5d4; font-weight:bold;'>WIN</span>"
            else:
                dot_html = '<span class="status-dot" style="color: #ff4757; background-color: #ff4757;"></span>'
                status_text = "<span style='color:#ff4757; font-weight:bold;'>LỆCH KO</span>"
            
            if is_arbitrated:
                if active_target == "PLAYER": oracle_display = f"<span style='color:#00f5d4; font-weight:bold;'>⚖️ T.TÀI: PLAYER</span>"
                elif active_target == "BANKER": oracle_display = f"<span style='color:#00f5d4; font-weight:bold;'>⚖️ T.TÀI: BANKER</span>"
                else: oracle_display = "<span style='color:#ff4757; font-weight:bold;'>⚖️ T.TÀI: KHÓA</span>"
            else:
                if "PLAYER" in active_target: oracle_display = f"<span style='color:#00afb9; font-weight:bold;'>🔵 {active_target}</span> <small style='color:#64748b;'>({oracle_alloc})</small>"
                elif "BANKER" in active_target: oracle_display = f"<span style='color:#ff4757; font-weight:bold;'>🔴 {active_target}</span> <small style='color:#64748b;'>({oracle_alloc})</small>"
                else: oracle_display = "<span style='color:#64748b;'>🛑 BỎ LỆNH</span>"
                
            outcome_display = f"<b style='color:#00afb9;'>P ({r['p_score']}đ)</b>" if outcome == "PLAYER" else (f"<b style='color:#ff4757;'>B ({r['b_score']}đ)</b>" if outcome == "BANKER" else "<b style='color:#2ecc71;'>TIE</b>")
            
            table_rows += f"<tr><td>V{real_round_num}</td><td style='text-align: left;'>{oracle_display}</td><td>{outcome_display}</td><td>{dot_html}</td><td>{status_text}</td></tr>"
            
        html_table = f"<table class='audit-table'><thead><tr><th>VÁN</th><th>KHUYẾN NGHỊ</th><th>SÀN ACT</th><th>MÃ</th><th>TRẠNG THÁI</th></tr></thead><tbody>{table_rows}</tbody></table></div>"
        st.markdown(html_table, unsafe_allow_html=True)


def parse_baccarat_input_v67_8(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().strip().replace(",", " ").replace(";", " ")
    temp_tokens = []
    i = 0
    while i < len(normalized):
        if normalized[i].isspace(): i += 1; continue
        if normalized[i:i+2] == "10": temp_tokens.append("10"); i += 2
        else: temp_tokens.append(normalized[i]); i += 1
    result_list = []
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13, '10': 10}
    for token in temp_tokens:
        if token in mapping: result_list.append(mapping[token])
        elif token.isdigit():
            val = int(token)
            if 1 <= val <= 9: result_list.append(val)
    return result_list


# =========================================================================
# 📱 MODULE 6: INTERFACE COGNITIVE
# =========================================================================
class BaccaratInterfaceSystem:
    @staticmethod
    def inject_custom_css():
        st.markdown(
            """
            <style>
            .stApp { background: #02040a !important; color: #f8fafc !important; }
            div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; gap: 8px !important; }
            div[data-testid="stHorizontalBlock"] > div { flex: 1 1 0% !important; min-width: 0px !important; }
            .header-hud-bar { background: linear-gradient(90deg, #090d16, #111827); border: 1px solid #1f2937; border-radius: 10px; padding: 10px; margin: 10px 0px 15px 0px; text-align: center; font-family: monospace; font-size: 12px; color: #cbd5e1; }
            .action-panel { border-radius: 12px; padding: 15px; margin: 5px 0px 15px 0px; text-align: center; box-shadow: 0px 5px 20px rgba(0,0,0,0.8); }
            .action-status { font-size: 16px; font-weight: 900; letter-spacing: 0.3px; margin-bottom: 4px; }
            .action-msg { font-size: 12px; opacity: 0.9; margin-bottom: 10px; line-height: 1.4; text-align: justify; }
            .action-vol { font-size: 14px; font-weight: 900; font-family: monospace; border-top: 1px dashed rgba(255,255,255,0.2); padding-top: 8px; }
            .mobile-metric-box { background: #050b14; border: 1px solid #0f172a; border-radius: 8px; padding: 10px 4px; margin-bottom: 5px; display: flex; flex-direction: column; text-align: center; }
            .metric-tag { font-size: 9px; font-weight: 800; color: #475569; text-transform: uppercase; margin-bottom: 2px; }
            .metric-num { font-size: 16px; font-weight: 900; font-family: monospace; }
            
            .audit-matrix-box { padding: 12px; border-radius: 10px; background-color: #050b14; border: 1px dashed #3b82f6; margin-top: 15px; box-sizing: border-box; width: 100%; overflow: hidden; }
            .audit-title { font-family: system-ui; font-size: 12px; font-weight: 800; color: #60a5fa; margin-bottom: 10px; letter-spacing: 0.3px; }
            .audit-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 11px; color: #cbd5e1; table-layout: fixed; }
            .audit-table th { padding: 8px 4px; text-align: center; background: #0f172a; color: #cbd5e1; border: 1px solid #1e293b; font-size: 10px; }
            .audit-table td { padding: 8px 4px; text-align: center; border: 1px solid #0f172a; vertical-align: middle; line-height: 1.3; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
            
            .audit-table th:nth-child(1), .audit-table td:nth-child(1) { width: 12%; }
            .audit-table th:nth-child(2), .audit-table td:nth-child(2) { width: 43%; text-align: left; white-space: normal; }
            .audit-table th:nth-child(3), .audit-table td:nth-child(3) { width: 18%; }
            .audit-table th:nth-child(4), .audit-table td:nth-child(4) { width: 10%; }
            .audit-table th:nth-child(5), .audit-table td:nth-child(5) { width: 17%; font-size: 10px; white-space: normal; }
            
            .status-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; }
            
            div.stButton > button { background-color: #0f172a !important; color: #cbd5e1 !important; border: 1px solid #1e293b !important; border-radius: 8px; font-weight: 800; width: 100% !important; padding: 10px 0px !important; }
            .submit-btn-box div.stButton > button { background-color: #38bdf8 !important; color: #010206 !important; border: none !important; box-shadow: 0 0 12px rgba(56,189,248,0.3); }
            div[data-testid="stNumberInput"] label { font-size: 11px !important; color: #cbd5e1 !important; }
            .block-container { padding-top: 0.8rem !important; padding-bottom: 0.8rem !important; }
            </style>
            """, 
            unsafe_allow_html=True
        )

    @staticmethod
    def render_sidebar():
        st.sidebar.markdown("### ⚙️ CẤU HÌNH KHAY BÀI VŨ TRỤ")
        decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)
        burn_cards = st.sidebar.number_input("🎴 SỐ LÁ RÚT BỎ (BURN CARDS):", min_value=0, max_value=50, value=7, step=1)
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 SỐ LIỆU QUỸ ĐẠO NỀN")
        hist_p = st.sidebar.number_input("🔵 PLAYER WINS:", min_value=0, value=0, step=1)
        hist_b = st.sidebar.number_input("🔴 BANKER WINS:", min_value=0, value=0, step=1)
        hist_t = st.sidebar.number_input("🟢 TIE WINS:", min_value=0, value=0, step=1)
        return decks, hist_p, hist_b, hist_t, burn_cards

    @staticmethod
    def render_header_hud(total_rounds, cards_left, decks_count):
        st.markdown(
            f'<div class="header-hud-bar">'
            f'🪐 TỔNG QUỸ ĐẠO: <b>{total_rounds}</b> ván &nbsp;|&nbsp; '
            f'🎴 CÒN LẠI: <b>{cards_left}</b> / {decks_count * 52}'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_input_form():
        st.markdown("##### 🎴 NHẬP DỮ LIỆU ĐỂ GIẢI PHƯƠNG TRÌNH:")
        with st.form(key="baccarat_cosmological_intelligence_form", clear_on_submit=True):
            input_grid = st.columns(2)
            with input_grid[0]: p_str = st.text_input("🔵 PLAYER CARD:", placeholder="Nhập bài")
            with input_grid[1]: b_str = st.text_input("🔴 BANKER CARD:", placeholder="Nhập bài")
            st.write("")
            st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
            triggered = st.form_submit_button("🚀 KÍCH HOẠT HỆ THỐNG ĐỘ CHÍNH XÁC CAO")
            st.markdown('</div>', unsafe_allow_html=True)
        return triggered, p_str, b_str

    @staticmethod
    def render_directive_panel(cmd):
        st.markdown(
            f'<div class="action-panel" style="background-color: {cmd["bg"]}; border: 2px solid {cmd["color"]}; color: {cmd["color"]};">'
            f'<div class="action-status">{cmd["status"]}</div>'
            f'<div class="action-msg" style="color: #f1f5f9;">{cmd["msg"]}</div>'
            f'<div class="action-vol">{cmd["action_vol"] if "action_vol" in cmd else "QUẢN LÝ VỐN: " + cmd["size"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_ai_oracle_panel(ai_cmd):
        if "CHƯA ĐỦ DỮ LIỆU" in ai_cmd['decision']:
            st.info(ai_cmd['ai_insight'])
            return

        html_string = (
            f"<div style='background: linear-gradient(135deg, #050d1a 0%, #020408 100%); border: 2px dashed {ai_cmd['color']}; border-radius: 12px; padding: 15px; margin: 12px 0px; box-shadow: 0px 6px 20px rgba(59,130,246,0.15); max-width:100%; overflow:hidden; word-wrap:break-word;'>"
            f"<div style='font-size: 10px; font-weight: 800; color: #60a5fa; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 2px;'>🌌 AI SOVEREIGN ORACLE - VERSION v70.0 ULTRA-PRECISION</div>"
            f"<div style='font-size: 18px; font-weight: 900; color: {ai_cmd['color']}; margin-bottom: 8px;'>{ai_cmd['decision']}</div>"
            f"<div style='background: rgba(59, 130, 246, 0.06); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; padding: 8px; margin-bottom: 8px; font-size: 11px; color: #93c5fd;'>🛰️ <b>MẠCH KIỂM SOÁT SAI SỐ KÉP:</b> <i>{ai_cmd['cyber_knowledge']}</i></div>"
            f"<table style='width:100%; border-collapse: collapse; font-size: 12px; margin-bottom: 12px; background: transparent;'>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 5px 0; color: #94a3b8; text-align: left;'>Mục tiêu:</td><td style='padding: 5px 0; font-weight:700; color: {ai_cmd['color']}; text-align:right;'>{ai_cmd['target']}</td></tr>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 5px 0; color: #94a3b8; text-align: left;'>Khối lượng Kelly:</td><td style='padding: 5px 0; font-weight:700; color: #ffffff; text-align:right;'>{ai_cmd['capital_allocation']}</td></tr>"
            f"</table>"
            f"<div style='background: rgba(255,255,255,0.02); border-left: 3px solid {ai_cmd['color']}; padding: 8px; border-radius: 4px; font-size: 12px; color: #e2e8f0; text-align: justify;'><b>💡 Phân tích chiến thuật chuyên sâu:</b> {ai_cmd['ai_insight']}</div>"
            f"</div>"
        )
        st.markdown(html_string, unsafe_allow_html=True)

    @staticmethod
    def render_probabilities_grid(p_pct, b_pct, t_pct, p_cnt, b_cnt, t_cnt):
        prob_grid = st.columns(3)
        with prob_grid[0]: st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER</span><span class="metric-num" style="color:#00afb9;">{p_pct:.1f}%</span></div>', unsafe_allow_html=True)
        with prob_grid[1]: st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER</span><span class="metric-num" style="color:#ff4757;">{b_pct:.1f}%</span></div>', unsafe_allow_html=True)
        with prob_grid[2]: st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE ZETA</span><span class="metric-num" style="color:#2ecc71;">{t_pct:.1f}%</span></div>', unsafe_allow_html=True)

    @staticmethod
    def render_utilities():
        util_grid = st.columns(2)
        undo_triggered = util_grid[0].button("⏪ QUAY LẠI (UNDO)")
        clear_triggered = util_grid[1].button("🔄 LÀM TRỐNG KHAY BÀI")
        return undo_triggered, clear_triggered


# =========================================================================
# 🎮 RUNTIME EXECUTION CONTROLLER
# =========================================================================
st.set_page_config(page_title="Cosmological Oracle v70.0", page_icon="🌌", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

decks, hist_p, hist_b, hist_t, burn_cards = BaccaratInterfaceSystem.render_sidebar()

st.markdown("### 🌌 ORACLE MULTI-AGENT PRECISION SYSTEM v70.0")

final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, streak_side, streak_count = calculate_v67_8_ultimate_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t, burn_cards=burn_cards
)
cmd = get_ultimate_directive(final_p, final_b, trend_desc, streak_side, streak_count, st.session_state.round_detailed_log, hist_p, hist_b)

total_all_rounds = total_p + total_b + total_t
BaccaratInterfaceSystem.render_header_hud(total_rounds=total_all_rounds, cards_left=cards_left, decks_count=decks)

current_ai_oracle = AISovereignOracle.analyze_and_suggest(
    all_rounds_log=st.session_state.round_detailed_log, shoe_decks=decks,
    manual_p=hist_p, manual_b=hist_b, manual_t=hist_t,
    p_val=final_p, b_val=final_b, t_val=final_t, cards_left=cards_left, 
    trend_desc=trend_desc, streak_side=streak_side, streak_count=streak_count, 
    total_rounds=total_all_rounds, burn_cards=burn_cards
)

# Đồng bộ hiển thị bảng điều khiển lệnh chính khi có trạng thái ngắt phanh bảo vệ v70.0
if current_ai_oracle['raw_code'] in ["SINGLE_ERROR_LOCK", "FORCE_EMERGENCY_LOCK"]:
    cmd['status'] = current_ai_oracle['decision']
    cmd['msg'] = current_ai_oracle['ai_insight']
    cmd['color'] = current_ai_oracle['color']
    cmd['bg'] = "rgba(241, 196, 15, 0.08)" if current_ai_oracle['raw_code'] == "SINGLE_ERROR_LOCK" else "rgba(255, 71, 87, 0.08)"
    cmd['action_vol'] = f"QUẢN LÝ VỐN: 0.0% (TẠM NGHỈ CHỜ ĐỒNG BỘ)"

calc_triggered, p_input, b_input = BaccaratInterfaceSystem.render_input_form()

current_arbitrator_verdict = QuantumArbitrationMatrix.render_arbitration_logic(
    multi_cmd=cmd, oracle_cmd=current_ai_oracle, all_rounds_log=st.session_state.round_detailed_log,
    shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t, burn_cards=burn_cards
)

if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v67_8(p_input.strip())
    b_list = parse_baccarat_input_v67_8(b_input.strip())
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    
    st.session_state.round_detailed_log.append({
        'p_cards': p_list, 'b_cards': b_list, 'p_score': p_score, 'b_score': b_score, 'outcome': outcome,
        'oracle_decision': current_ai_oracle['decision'], 'oracle_target': current_ai_oracle['target'],
        'oracle_alloc': current_ai_oracle['capital_allocation'], 'arbitrator_target': current_arbitrator_verdict 
    })
    st.rerun()

st.markdown("---")

BaccaratInterfaceSystem.render_directive_panel(cmd)
BaccaratInterfaceSystem.render_ai_oracle_panel(current_ai_oracle)
BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t, total_p, total_b, total_t)

QuantumAuditMatrixController.render_audit_table(log=st.session_state.round_detailed_log, start_round_index=(hist_p + hist_b + hist_t))

st.markdown("<br>", unsafe_allow_html=True)
undo_btn, clear_btn = BaccaratInterfaceSystem.render_utilities()

if undo_btn and st.session_state.round_detailed_log:
    st.session_state.round_detailed_log.pop()
    st.rerun()

if clear_btn:
    st.session_state.round_detailed_log.clear()
    st.rerun()
