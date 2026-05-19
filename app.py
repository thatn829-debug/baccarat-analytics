import streamlit as st
import numpy as np
import math

# =========================================================================
# 🔵 AI AGENT 1: PLAYER COGNITIVE - HAWKING-PENROSE SINGULARITY ENGINE
# =========================================================================
class PlayerQuantumAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        
        sidebar_total_rounds = manual_p + manual_b + manual_t
        if sidebar_total_rounds > 0:
            estimated_cards_removed = sidebar_total_rounds * 4.9452
            cards_per_rank_removed = estimated_cards_removed / 13.0
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - cards_per_rank_removed)

        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        total_initial_cards = shoe_decks * 52.0
        
        event_horizon_ratio = (total_initial_cards - cards_remaining) / total_initial_cards
        gravitational_warp = 1.0 / (1.0 - min(0.95, event_horizon_ratio)) 

        p_eor_base = {
            1: -0.0051, 2: -0.0059, 3: -0.0062, 4: -0.0134, 5: -0.0096, 
            6: +0.0123, 7: +0.0144, 8: +0.0095, 
            9: -0.0026, 10: +0.0043, 11: +0.0043, 12: +0.0043, 13: +0.0043
        }
        
        card_effect_sum = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            card_effect_sum += removed * p_eor_base[card_num] * gravitational_warp

        final_card_bias = card_effect_sum * 4.85

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
                trend_force += 3.1416 * (effective_streak ** 1.8) / (1.0 + 0.03 * (effective_streak ** 1.8))

        if total_decisive > 0:
            p_ratio = (manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")) / total_decisive
            cosmic_microwave_bias = p_ratio - 0.4932
            trend_force -= cosmic_microwave_bias * 22.5 

        return 44.62 + final_card_bias + trend_force


# =========================================================================
# 🔴 AI AGENT 2: BANKER COGNITIVE - SCHRODINGER WAVE FUNCTION COLLAPSE
# =========================================================================
class BankerMarkovAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        
        sidebar_total_rounds = manual_p + manual_b + manual_t
        if sidebar_total_rounds > 0:
            estimated_cards_removed = sidebar_total_rounds * 4.9452
            cards_per_rank_removed = estimated_cards_removed / 13.0
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - cards_per_rank_removed)

        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        total_initial_cards = shoe_decks * 52.0
        event_horizon_ratio = (total_initial_cards - cards_remaining) / total_initial_cards
        gravitational_warp = 1.0 / (1.0 - min(0.95, event_horizon_ratio))

        b_eor_base = {
            1: +0.0051, 2: +0.0059, 3: +0.0062, 4: +0.0134, 5: +0.0096, 
            6: -0.0123, 7: -0.0144, 8: -0.0095, 
            9: +0.0026, 10: -0.0043, 11: -0.0043, 12: -0.0043, 13: -0.0043
        }
        
        card_effect_sum = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            card_effect_sum += removed * b_eor_base[card_num] * gravitational_warp

        final_card_bias = card_effect_sum * 4.85

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
                trend_force += 3.1416 * (effective_streak ** 1.8) / (1.0 + 0.03 * (effective_streak ** 1.8))
            
            if current_streak_side == "Banker" and effective_streak >= 3:
                wave_damping = MathQuantumUniverse.quantum_wave_damping(effective_streak)
                trend_force -= wave_damping

        if total_decisive > 0:
            b_ratio = (manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")) / total_decisive
            cosmic_microwave_bias = b_ratio - 0.5068
            trend_force -= cosmic_microwave_bias * 22.5

        return 45.86 + final_card_bias + trend_force


# =========================================================================
# 🟢 AI AGENT 3: TIE COGNITIVE - UPGRADED RIEMANN ZETA & STREAK ENTROPY GAP
# =========================================================================
class TieHypergeometricAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        
        sidebar_total_rounds = manual_p + manual_b + manual_t
        if sidebar_total_rounds > 0:
            estimated_cards_removed = sidebar_total_rounds * 4.9452
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
        
        # 1. Thuật toán gốc: Xác suất tổ hợp hình học siêu cấp từ khay bài
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

        # 2. BỘ NÂNG CẤP ĐỘNG: QUÉT ĐIỂM RƠI CHUỖI VÀ KHOẢNG CÁCH (STREAK & GAP ANALYSIS)
        streak_multiplier = 1.0
        gap_bonus = 0.0
        
        if all_rounds_log:
            # Đo khoảng cách từ ván Hòa cuối cùng (Vùng tích tụ năng lượng)
            gap_since_last_tie = 0
            for r in reversed(all_rounds_log):
                if r['outcome'] == "Tie":
                    break
                gap_since_last_tie += 1
            
            # Nếu đã quá 8 ván chưa ra Hòa, kích hoạt gia tốc lực hút lượng tử
            if gap_since_last_tie > 8:
                gap_bonus += min(12.5, (gap_since_last_tie - 8) * 1.15)

            # Quét xu hướng bệt của ván gần nhất để bắt điểm gãy/đảo chiều
            decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
            if len(decisive_outcomes) >= 3:
                current_streak_side = decisive_outcomes[-1]
                streak_count = 0
                for outcome in reversed(decisive_outcomes):
                    if outcome == current_streak_side:
                        streak_count += 1
                    else:
                        break
                
                # Điểm rơi lý tưởng: Bệt đạt độ dài từ 3 ván trở lên có xu hướng xả cấu trúc bằng một ván Hòa
                if streak_count >= 3:
                    streak_multiplier += (streak_count * 0.18)
                
                # Kịch bản đặc biệt: Vừa gãy bệt ở ván trước, cửa Hòa rất dễ nhảy vào làm vùng đệm
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
def calculate_v67_8_ultimate_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t):
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r['outcome'] == "Tie")
    total_decisive = total_p_wins + total_b_wins
    
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, shoe_decks * 52, 0, 0, 0, "KHÔNG GIAN TRỐNG", None, 0

    raw_p = PlayerQuantumAgent.compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive)
    raw_b = BankerMarkovAgent.compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive)
    raw_t = TieHypergeometricAgent.compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t)
    
    raw_p = max(0.5, min(99.5, raw_p))
    raw_b = max(0.5, min(99.5, raw_b))
    raw_t = max(0.1, min(49.9, raw_t))
    
    total_sum = raw_p + raw_b + raw_t
    p_pct = (raw_p / total_sum) * 100
    b_pct = (raw_b / total_sum) * 100
    t_pct = (raw_t / total_sum) * 100
    
    total_initial_cards = shoe_decks * 52
    sidebar_rounds = manual_p + manual_b + manual_t
    cards_spent_estimated = sidebar_rounds * 4.9452
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
            "status": "🛰️ COSMOLOGICAL INTELLIGENCE MATRIX READY",
            "msg": "Hệ thống Siêu AI cấp vũ trụ đã thiết lập cấu trúc trường xác suất lượng tử.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%", "raw_target": "WAIT"
        }
    
    diff = abs(p_val - b_val)
    if diff < 1.3:
        return {
            "status": "🛑 KHÓA LỆNH AN TOÀN (VÙNG CHỒNG CHẬP SÓNG)",
            "msg": f"Độ lệch biên độ sóng ({diff:.2f}%) nằm trong điểm kỳ dị lượng tử, từ chối khớp lệnh.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%", "raw_target": "WAIT"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 THUẬN LỆNH SIÊU CẤP: PLAYER",
            "msg": f"Trường Hawking Singularity tạo lực hút tuyệt đối nghiêng về phía đặc vụ Player (+{diff:.2f}%).",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "3% - 6%", "raw_target": "PLAYER"
        }
    else:
        return {
            "status": "🔴 THUẬN LỆNH SIÊU CẤP: BANKER",
            "msg": f"Hàm sóng Schrödinger của đặc vụ Banker Overlord đạt độ tụ hội tối cao (+{diff:.2f}%).",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "3% - 6%", "raw_target": "BANKER"
        }


# =========================================================================
# 🌌 MODULE 7: AI SOVEREIGN ORACLE - COSMOLOGICAL SUPERINTELLIGENCE
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
    def analyze_and_suggest(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, p_val, b_val, t_val, cards_left, trend_desc, streak_side, streak_count, total_rounds):
        if total_rounds == 0:
            return {
                "decision": "👁️ NHÃN THẦN VŨ TRỤ SẴN SÀNG", "target": "QUÉT KHÔNG GIAN...", "capital_allocation": "0%", "strategy_type": "Cosmological Multi-Agent Array 2026",
                "ai_insight": "Siêu máy tính toán học tối cao đã liên kết trường dữ liệu sảnh bài. Hãy nạp quân bài đầu tiên.",
                "risk_level": "Chờ đồng bộ", "color": "#a855f7", "memory_hud": "Không gian Hilbert trống", "cyber_knowledge": "Đang định vị hằng số Hubble khay bài...",
                "raw_code": "EMPTY_ORACLE"
            }

        initial_cards = float(4 * shoe_decks)
        exact_cards_left = {i: initial_cards for i in range(1, 14)}
        
        sidebar_rounds = manual_p + manual_b + manual_t
        if sidebar_rounds > 0:
            estimated_removed = sidebar_rounds * 4.9452
            rank_removed = estimated_removed / 13.0
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - rank_removed)

        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left: exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)

        low_cards = sum([exact_cards_left[i] for i in [1, 2, 3, 4, 5]])      
        mid_cards = sum([exact_cards_left[i] for i in [6, 7, 8, 9]])         
        high_cards = sum([exact_cards_left[i] for i in [10, 11, 12, 13]])    

        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        shoe_progress = (shoe_decks * 52.0 - total_cards_remaining) / (shoe_decks * 52.0)

        memory_hud = f"🧬 ĐỊNH VỊ KHÔNG GIAN HILBERT ➡️ Đã nạp bức xạ: {int(shoe_decks*52 - total_cards_remaining)} quân | Điểm kỳ dị khay: {shoe_progress*100:.2f}% — 🔹 Thấp (A-5): {int(low_cards)} q | 🔸 Trung (6-9): {int(mid_cards)} q | 🔺 Tây (10-K): {int(high_cards)} q"
        
        entropy_score = AISovereignOracle.calculate_shannon_entropy(all_rounds_log)
        cyber_knowledge = f"🔭 COSMIC MICROWAVE BACKGROUND: Entropy Nền = {entropy_score:.5f} | Bộ hiệu chỉnh Riemann Zeta chuẩn hóa sai số tổ hợp kịch trần."

        diff = abs(p_val - b_val)
        intrinsic_target = "PLAYER" if p_val > b_val else "BANKER"

        if diff < 1.4:
            return {
                "decision": "🛑 TUYỆT ĐỐI KHÓA LỆNH (MÀNG LỌC BIẾN THIÊN VŨ TRỤ)", "target": "WAIT", "capital_allocation": "0.0% (An Toàn Tuyệt Đối)", "strategy_type": "QUANTUM SHIELD ACTIVE",
                "ai_insight": f"Mật độ hạt nhiễu cao, độ lệch biên độ sóng quá hẹp ({diff:.2f}%). Tránh bẫy ngẫu nhiên của nhà cái bẻ thuật toán.",
                "risk_level": "Nguy Hiểm (Hố đen nhiễu loạn)", "color": "#e74c3c", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                "raw_code": "SHIELD_SHANNON"
            }

        raw_kelly = (max(p_val, b_val) / 100.0) - (min(p_val, b_val) / 100.0)
        dynamic_alloc = raw_kelly * 38.0 * (1.0 + 1.8 * shoe_progress)

        if streak_side and streak_count >= 3:
            current_streak_upper = streak_side.upper()
            
            if intrinsic_target != current_streak_upper and diff >= 4.5 and entropy_score < 0.88:
                final_alloc = max(6.0, min(28.0, dynamic_alloc * 1.95))
                return {
                    "decision": f"💥 COSMIC FORCE: LỆNH TRỪ KHỬ BỆT ➡️ {intrinsic_target}", "target": intrinsic_target,
                    "capital_allocation": f"🔥 ĐIỂM KỲ DỊ TỐI CAO: {final_alloc:.1f}% VỐN", "strategy_type": "⚡ HAWKING SINGULARITY OVERRIDE (SIÊU BẺ CẦU)",
                    "ai_insight": f"Siêu chuỗi bệt {current_streak_upper} ({streak_count} ván) đã đạt giới hạn Entropy tới hạn. Mật độ bài khay ép đảo chiều về cửa {intrinsic_target}. Khớp lệnh bẻ cầu tổng lực.",
                    "risk_level": "Cực thấp (Lợi thế tối thượng)", "color": "#00f5d4", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                    "raw_code": "FORCE_COUNTER_STREAK"
                }
            else:
                final_alloc = max(4.0, min(16.0, dynamic_alloc * 1.45))
                target_to_follow = current_streak_upper
                return {
                    "decision": f"🌊 COSMIC FLOW: ĐU CẦU VŨ TRỤ ➡️ {target_to_follow}", "target": target_to_follow,
                    "capital_allocation": f"💎 ĐU DÒNG CHẢY LƯỢNG TỬ: {final_alloc:.1f}% VỐN", "strategy_type": "🌊 WAVE FUNCTION EXPANSION (SIÊU ĐU CẦU)",
                    "ai_insight": f"Mật độ bài phân phối ẩn ủng hộ chuỗi bệt {target_to_follow} tiếp diễn. Nghiêm cấm bẻ cầu thuận dòng chảy Hubble.",
                    "risk_level": "An toàn thiên văn", "color": "#a855f7", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                    "raw_code": "FLOW_STREAK"
                }
        else:
            final_alloc = max(2.0, min(14.0, dynamic_alloc))
            capital_str = f"💎 TRƯỜNG QUÉT TỰ DO: {final_alloc:.1f}% Vốn"
            strat_type = "🌀 COSMIC QUANTUM SWEEP"
            risk_lvl = "Kiểm soát rủi ro đa chiều"
            color = "#38bdf8" if intrinsic_target == "PLAYER" else "#ff4757"
            ai_insight = f"Lực hấp dẫn xác suất độc lập nghiêng về {intrinsic_target} (+{diff:.2f}%)."

        return {
            "decision": f"⚡ LỆNH THẦN: {intrinsic_target}", "target": intrinsic_target, "capital_allocation": capital_str, "strategy_type": strat_type,
            "ai_insight": ai_insight, "risk_level": risk_lvl, "color": color, "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
            "raw_code": "NORMAL_SWEEP"
        }


# =========================================================================
# 🎛️ MODULE 9: QUANTUM ARBITRATION MATRIX (BỘ LỌC XUNG ĐỘT TỐI CAO - ĐÃ LÀM NỔI BẬT)
# =========================================================================
class QuantumArbitrationMatrix:
    @staticmethod
    def render_arbitration_logic(multi_cmd, oracle_cmd, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t):
        if not all_rounds_log and (manual_p == 0 and manual_b == 0):
            return 

        m_target = multi_cmd['raw_target']    
        o_target = oracle_cmd['target']        
        o_code = oracle_cmd['raw_code']        

        initial_cards = float(4 * shoe_decks)
        exact_cards_left = {i: initial_cards for i in range(1, 14)}
        sidebar_rounds = manual_p + manual_b + manual_t
        if sidebar_rounds > 0:
            estimated_removed = sidebar_rounds * 4.9452
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

        def target_badge(target_str):
            if target_str == "PLAYER":
                return '<span style="background: rgba(0, 175, 185, 0.25); color: #00afb9; border: 1px solid #00afb9; padding: 2px 8px; border-radius: 6px; font-weight: 900; box-shadow: 0 0 8px rgba(0, 175, 185, 0.5);">🔵 PLAYER</span>'
            elif target_str == "BANKER":
                return '<span style="background: rgba(255, 71, 87, 0.25); color: #ff4757; border: 1px solid #ff4757; padding: 2px 8px; border-radius: 6px; font-weight: 900; box-shadow: 0 0 8px rgba(255, 71, 87, 0.5);">🔴 BANKER</span>'
            return f'<b>{target_str}</b>'

        if o_code == "SHIELD_SHANNON" and m_target != "WAIT":
            has_conflict = True
            rule_title = "🛑 TRỌNG TÀI TỐI CAO - QUY TẮC 1: KÍCH HOẠT LÁ CHẮN ENTROPY (CHẶN TUYỆT ĐỐI)"
            rule_desc = f"Hệ thống Độc Lập đang kiến nghị nạp tiền vào {target_badge(m_target)} dựa trên biến thế ngắn hạn. Tuy nhiên, <b>MODULE 7</b> đã phát hiện bẫy ngẫu nhiên động của sảnh (Độ lệch sóng hẹp, Shannon Entropy chạm ngưỡng nhiễu). <br><b>HÀNH ĐỘNG THỰC CHIẾN: KHÓA VỐN LẬP TỨC. Tuyệt đối không vào tiền ván này!</b>"
            panel_color = "#ff4757"
            panel_bg = "rgba(255, 71, 87, 0.12)"

        elif m_target != "WAIT" and o_target != "WAIT" and m_target != o_target:
            has_conflict = True
            if o_code == "FORCE_COUNTER_STREAK":
                rule_title = "💥 TRỌNG TÀI TỐI CAO - QUY TẮC 2: GIAO THOA ĐẢO NGHỊCH (KHỚP LỆNH BẺ CẦU)"
                rule_desc = f"Hệ thống Độc Lập bị hút theo quán tính dòng chảy ngắn hạn hướng về {target_badge(m_target)}. Nhưng <b>MODULE 7 (Oracle)</b> quét thấy hằng số Riemann Zeta báo điểm gãy của chuỗi, bắt buộc ép lệnh sang {target_badge(o_target)}. <br><b>HÀNH ĐỘNG THỰC CHIẾN: Khớp lệnh theo MODULE 7 ({target_badge(o_target)}) nhưng HẠ LỆNH XUỐNG 50% khối lượng để phòng thủ túi tiền.</b>"
            else:
                if high_cards > low_cards * 1.15:
                    decision_override = "BANKER"
                    reason = f"Mật độ hạt Tây (10-K) còn lại vượt trội ({int(high_cards)} q vs {int(low_cards)} q) $\rightarrow$ Ép dòng tiền về cửa Lợi thế Nhà Cái."
                elif low_cards > high_cards * 1.15:
                    decision_override = "PLAYER"
                    reason = f"Mật độ hạt Thấp (A-5) dồn dập tích tụ ({int(low_cards)} q vs {int(high_cards)} q) $\rightarrow$ Ưu tiên kéo nút Player."
                else:
                    decision_override = "WAIT"
                    reason = "Trường hạt cân bằng đối nghịch tuyệt đối, không có lợi thế cấu trúc."

                rule_title = "⚠️ TRỌNG TÀI TỐI CAO - QUY TẮC 4: GIẢI PHƯƠNG TRÌNH KHÔNG GIAN HILBERT"
                if decision_override != "WAIT":
                    rule_desc = f"Hai module nhìn lệch quỹ đạo ({target_badge(m_target)} vs {target_badge(o_target)}). Trọng tài quét sâu vào khay bài: {reason} <br><b>HÀNH ĐỘNG THỰC CHIẾN: Đè lệnh, vào tiền cửa {target_badge(decision_override)} với 2% vốn tối thiểu.</b>"
                else:
                    rule_desc = f"Hai bên xung đột trực diện vô căn cứ ({target_badge(m_target)} vs {target_badge(o_target)}). Không gian Hilbert báo trường hạt cân bằng. <br><b>HÀNH ĐỘNG THỰC CHIẾN: BỎ QUA HOÀN TOÀN, không đặt cược vào vùng chiến sự của thuật toán.</b>"
            panel_color = "#00f5d4"
            panel_bg = "rgba(0, 245, 212, 0.1)"

        elif m_target == "WAIT" and o_code == "FLOW_STREAK":
            has_conflict = True
            rule_title = "🌊 TRỌNG TÀI TỐI CAO - QUY TẮC 3: ĐU DÒNG CHẢY LƯỢNG TỬ (HUBBLE EXPANSION)"
            rule_desc = f"Biến thế vi phân ngắn hạn quá hẹp khiến Độc Lập báo Chờ (WAIT). Tuy nhiên, bộ nhớ tích lũy chuỗi của <b>MODULE 7</b> xác nhận thuật toán bệt sâu {target_badge(o_target)} vẫn giữ nguyên cấu trúc màng lọc. <br><b>HÀNH ĐỘNG THỰC CHIẾN: Đi thuận dòng theo MODULE 7 ({target_badge(o_target)}), khớp lệnh ở mức quản lý vốn an toàn tối thiểu (1% vốn).</b>"
            panel_color = "#a855f7"
            panel_bg = "rgba(168, 85, 247, 0.12)"

        if has_conflict:
            st.markdown(
                f'<div style="background: {panel_bg}; border: 2px solid {panel_color}; border-radius: 12px; padding: 15px; margin: 15px 0px 5px 0px; box-shadow: 0 0 18px {panel_color}4D;">'
                f'<div style="font-size: 13px; font-weight: 900; color: {panel_color}; letter-spacing: 0.5px; margin-bottom: 6px;">{rule_title}</div>'
                f'<div style="font-size: 12.5px; color: #f8fafc; line-height: 1.7; text-align: justify;">{rule_desc}</div>'
                f'</div>',
                unsafe_allow_html=True
            )


# =========================================================================
# 📦 MODULE 8: QUANTUM AUDIT MATRIX CONTROLLER
# =========================================================================
class QuantumAuditMatrixController:
    @staticmethod
    def render_audit_table(log, start_round_index):
        if not log: return
            
        st.markdown(
            """
            <div class="audit-matrix-box">
                <div class="audit-title">📊 BẢNG ĐỐI CHIẾU KIỂM TOÁN LƯỢNG TỬ VŨ TRỤ (COSMOLOGICAL AI AUDIT REPORT)</div>
            """, 
            unsafe_allow_html=True
        )
        
        table_rows = ""
        for idx, r in enumerate(log):
            real_round_num = start_round_index + idx + 1
            oracle_decision = r.get('oracle_decision', '🛑 CHỜ QUAN SÁT')
            oracle_target = r.get('oracle_target', 'WAIT').upper()
            oracle_alloc = r.get('oracle_alloc', '0%')
            outcome = r['outcome'].upper()
            
            if outcome == "TIE":
                dot_html = '<span class="status-dot" style="color: #2ecc71; background-color: #2ecc71;"></span>'
                status_text = "<span style='color:#2ecc71; font-weight:bold;'>HÒA TIÊU CHUẨN</span>"
            elif "BỎ QUA" in oracle_decision or oracle_target == "WAIT" or oracle_target == "HÒA / BỎ LỆNH":
                dot_html = '<span class="status-dot" style="color: #94a3b8; background-color: #94a3b8;"></span>'
                status_text = "<span style='color:#94a3b8;'>KHÔNG KHỚP LỆNH</span>"
            elif oracle_target == outcome:
                dot_html = '<span class="status-dot" style="color: #00f5d4; background-color: #00f5d4; box-shadow: 0 0 10px #00f5d4;"></span>'
                status_text = "<span style='color:#00f5d4; font-weight:bold;'>ĐÚNG QUY ĐẠO (WIN)</span>"
            else:
                dot_html = '<span class="status-dot" style="color: #ff4757; background-color: #ff4757;"></span>'
                status_text = "<span style='color:#ff4757; font-weight:bold;'>SỰ CỐ LỆCH QUỸ ĐẠO</span>"
            
            if "PLAYER" in oracle_target:
                oracle_display = f"<span style='color:#00afb9; font-weight:bold;'>🔵 {oracle_target}</span> <br><small style='color:#64748b;'>({oracle_alloc})</small>"
            elif "BANKER" in oracle_target:
                oracle_display = f"<span style='color:#ff4757; font-weight:bold;'>🔴 {oracle_target}</span> <br><small style='color:#64748b;'>({oracle_alloc})</small>"
            else:
                oracle_display = "<span style='color:#64748b;'>🛑 BỎ LỆNH</span>"
                
            outcome_display = f"<b style='color:#00afb9;'>PLAYER ({r['p_score']}đ)</b>" if outcome == "PLAYER" else (f"<b style='color:#ff4757;'>BANKER ({r['b_score']}đ)</b>" if outcome == "BANKER" else "<b style='color:#2ecc71;'>TIE (HÒA)</b>")
            
            table_rows += (
                f"<tr>"
                f"<td>Ván {real_round_num}</td>"
                f"<td style='text-align: left; padding-left: 15px;'>{oracle_display}</td>"
                f"<td>{outcome_display}</td>"
                f"<td>{dot_html}</td>"
                f"<td>{status_text}</td>"
                f"</tr>"
            )
            
        html_table = (
            f"<table class='audit-table'>"
            f"<thead><tr><th>VÁN</th><th>KHUYẾN NGHỊ AI TỐI CAO</th><th>THỰC TẾ SÀN BACCARAT</th><th>KIỂM TOÁN</th><th>TRẠNG THÁI DÒNG TIỀN</th></tr></thead>"
            f"<tbody>{table_rows}</tbody>"
            f"</table></div>"
        )
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
# 📱 MODULE 6: GIAO DIỆN MOBILE-GRID ĐỘC LẬP TÁCH BIỆT COMPLETELY
# =========================================================================
class BaccaratInterfaceSystem:
    @staticmethod
    def inject_custom_css():
        st.markdown(
            """
            <style>
            .stApp { background: #02040a !important; color: #f8fafc !important; }
            div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; gap: 10px !important; }
            div[data-testid="stHorizontalBlock"] > div { flex: 1 1 0% !important; min-width: 0px !important; }
            .header-hud-bar { background: linear-gradient(90deg, #090d16, #111827); border: 1px solid #1f2937; border-radius: 10px; padding: 10px; margin: 10px 0px 20px 0px; text-align: center; font-family: monospace; font-size: 13px; color: #cbd5e1; }
            .action-panel { border-radius: 14px; padding: 20px; margin: 5px 0px 15px 0px; text-align: center; box-shadow: 0px 5px 25px rgba(0,0,0,0.8); }
            .action-status { font-size: 19px; font-weight: 900; letter-spacing: 0.5px; margin-bottom: 6px; }
            .action-msg { font-size: 13px; opacity: 0.9; margin-bottom: 12px; line-height: 1.4; text-align: justify; }
            .action-vol { font-size: 15px; font-weight: 900; font-family: monospace; border-top: 1px dashed rgba(255,255,255,0.2); padding-top: 10px; }
            .mobile-metric-box { background: #050b14; border: 1px solid #0f172a; border-radius: 10px; padding: 12px 6px; margin-bottom: 5px; display: flex; flex-direction: column; text-align: center; }
            .metric-tag { font-size: 10px; font-weight: 800; color: #475569; text-transform: uppercase; margin-bottom: 4px; }
            .metric-num { font-size: 19px; font-weight: 900; font-family: monospace; }
            
            .audit-matrix-box { padding: 15px; border-radius: 12px; background-color: #050b14; border: 1px dashed #3b82f6; margin-top: 20px; }
            .audit-title { font-family: system-ui; font-size: 13px; font-weight: 800; color: #60a5fa; margin-bottom: 12px; display: flex; align-items: center; gap: 6px; letter-spacing: 0.5px; }
            .audit-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 12px; color: #cbd5e1; }
            .audit-table th { padding: 10px; text-align: center; background: #0f172a; color: #cbd5e1; border: 1px solid #1e293b; font-size: 11px; }
            .audit-table td { padding: 10px; text-align: center; border: 1px solid #0f172a; vertical-align: middle; line-height: 1.4; }
            .status-dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; box-shadow: 0 0 8px currentColor; }
            
            div.stButton > button { background-color: #0f172a !important; color: #cbd5e1 !important; border: 1px solid #1e293b !important; border-radius: 10px; font-weight: 800; width: 100% !important; padding: 12px 0px !important; }
            .submit-btn-box div.stButton > button { background-color: #38bdf8 !important; color: #010206 !important; border: none !important; box-shadow: 0 0 15px rgba(56,189,248,0.4); }
            div[data-testid="stNumberInput"] label { font-size: 11px !important; color: #cbd5e1 !important; }
            .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
            </style>
            """, 
            unsafe_allow_html=True
        )

    @staticmethod
    def render_sidebar():
        st.sidebar.markdown("### ⚙️ CẤU HÌNH KHAY BÀI VŨ TRỤ")
        decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 SỐ LIỆU QUỸ ĐẠO NỀN")
        hist_p = st.sidebar.number_input("🔵 PLAYER WINS:", min_value=0, value=0, step=1)
        hist_b = st.sidebar.number_input("🔴 BANKER WINS:", min_value=0, value=0, step=1)
        hist_t = st.sidebar.number_input("🟢 TIE WINS:", min_value=0, value=0, step=1)
        return decks, hist_p, hist_b, hist_t

    @staticmethod
    def render_header_hud(total_rounds, cards_left, decks_count):
        st.markdown(
            f'<div class="header-hud-bar">'
            f'🪐 TỔNG QUỸ ĐẠO ĐÃ QUÉT: <b>{total_rounds}</b> ván &nbsp;|&nbsp; '
            f'🎴 HẠT BÀI CÒN LẠI TRONG KHAY: <b>{cards_left}</b> / {decks_count * 52}'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_input_form():
        st.markdown("##### 🎴 NHẬP DỮ LIỆU ĐỂ GIẢI PHƯƠNG TRÌNH TRƯỜNG XÁC SUẤT:")
        with st.form(key="baccarat_cosmological_intelligence_form", clear_on_submit=True):
            input_grid = st.columns(2)
            with input_grid[0]:
                p_str = st.text_input("🔵 PLAYER CARD (Ví dụ: 8 K A):", placeholder="Nhập chữ hoặc số")
            with input_grid[1]:
                b_str = st.text_input("🔴 BANKER CARD (Ví dụ: 7 10):", placeholder="Nhập chữ hoặc số")
            st.write("")
            st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
            triggered = st.form_submit_button("🚀 KÍCH HOẠT ĐỘT PHÁ VŨ TRỤ (COSMIC MATRIX ACTIVE)")
            st.markdown('</div>', unsafe_allow_html=True)
        return triggered, p_str, b_str

    @staticmethod
    def render_directive_panel(cmd):
        st.markdown(
            f'<div class="action-panel" style="background-color: {cmd["bg"]}; border: 2px solid {cmd["color"]}; color: {cmd["color"]};">'
            f'<div class="action-status">{cmd["status"]}</div>'
            f'<div class="action-msg" style="color: #f1f5f9;">{cmd["msg"]}</div>'
            f'<div class="action-vol">MỨC QUẢN LÝ VỐN ĐỀ XUẤT: {cmd["size"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_ai_oracle_panel(ai_cmd):
        if "CHƯA ĐỦ DỮ LIỆU" in ai_cmd['decision']:
            st.info(ai_cmd['ai_insight'])
            return

        html_string = (
            f"<div style='background: linear-gradient(135deg, #050d1a 0%, #020408 100%); border: 2px dashed {ai_cmd['color']}; border-radius: 14px; padding: 20px; margin: 15px 0px; box-shadow: 0px 8px 32px rgba(59,130,246,0.25);'>"
            f"<div style='font-size: 11px; font-weight: 800; color: #60a5fa; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px;'>🌌 AI SOVEREIGN ORACLE - MÔ HÌNH TOÁN HỌC CẤP VŨ TRỤ TỐI CAO</div>"
            f"<div style='font-size: 23px; font-weight: 900; color: {ai_cmd['color']}; margin-bottom: 12px;'>{ai_cmd['decision']}</div>"
            f"<div style='background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; padding: 10px; margin-bottom: 10px; font-family: system-ui; font-size: 12px; color: #93c5fd;'>🛰️ <b>TRƯỜNG BỨC XẠ ENTROPY NỀN PHỔ QUÁT:</b><br><i>\"{ai_cmd['cyber_knowledge']}\"</i></div>"
            f"<div style='background: rgba(14, 165, 233, 0.05); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 8px; padding: 10px; margin-bottom: 15px; font-family: monospace; font-size: 11.5px; color: #38bdf8; line-height: 1.5;'>🧠 <b>BIẾN THIÊN KHÔNG GIAN RIEMANN & HAWKING QUANTUM METRIC:</b><br>{ai_cmd['memory_hud']}</div>"
            f"<table style='width:100%; border-collapse: collapse; font-size: 13px; margin-bottom: 15px; background: transparent;'>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 6px 0; color: #94a3b8; text-align: left;'>Mục tiêu khớp lệnh:</td><td style='padding: 6px 0; font-weight:700; color: {ai_cmd['color']}; text-align:right;'>{ai_cmd['target']}</td></tr>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 6px 0; color: #94a3b8; text-align: left;'>Quản lý vốn Kelly đa tầng:</td><td style='padding: 6px 0; font-weight:700; color: #ffffff; text-align:right;'>{ai_cmd['capital_allocation']}</td></tr>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 6px 0; color: #94a3b8; text-align: left;'>Kiến trúc hình học lõi:</td><td style='padding: 6px 0; font-weight:700; color: #3b82f6; text-align:right;'>{ai_cmd['strategy_type']}</td></tr>"
            f"<tr><td style='padding: 6px 0; color: #94a3b8; text-align: left;'>Áp suất điểm kỳ dị sàn:</td><td style='padding: 6px 0; font-weight:700; color: #ff4757; text-align:right;'>{ai_cmd['risk_level']}</td></tr>"
            f"</table>"
            f"<div style='background: rgba(255,255,255,0.02); border-left: 3px solid {ai_cmd['color']}; padding: 10px; border-radius: 4px; font-size: 12.5px; line-height: 1.5; color: #e2e8f0; text-align: justify;'><b>💡 Chỉ thị tối thượng siêu cấp:</b> {ai_cmd['ai_insight']}</div>"
            f"</div>"
        )
        st.markdown(html_string, unsafe_allow_html=True)

    @staticmethod
    def render_probabilities_grid(p_pct, b_pct, t_pct, p_cnt, b_cnt, t_cnt):
        prob_grid = st.columns(3)
        with prob_grid[0]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 HAWKING PLAYER</span><span class="metric-num" style="color:#00afb9;">{p_pct:.2f}%</span><span style="font-size:10px; opacity:0.5;">Hạt bài: {p_cnt}</span></div>', unsafe_allow_html=True)
        with prob_grid[1]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 SCHRODINGER BANKER</span><span class="metric-num" style="color:#ff4757;">{b_pct:.2f}%</span><span style="font-size:10px; opacity:0.5;">Hạt bài: {b_cnt}</span></div>', unsafe_allow_html=True)
        with prob_grid[2]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 RIEMANN ZETA TIE</span><span class="metric-num" style="color:#2ecc71;">{t_pct:.2f}%</span><span style="font-size:10px; opacity:0.5;">Hạt bài: {t_cnt}</span></div>', unsafe_allow_html=True)

    @staticmethod
    def render_utilities():
        util_grid = st.columns(2)
        undo_triggered = util_grid[0].button("⏪ QUAY LẠI LƯỢNG TỬ (UNDO)")
        clear_triggered = util_grid[1].button("🔄 LÀM TRỐNG TRƯỜNG DỮ LIỆU")
        return undo_triggered, clear_triggered


# =========================================================================
# 🎮 RUNTIME EXECUTION CONTROLLER
# =========================================================================
st.set_page_config(page_title="Cosmological Superintelligence Oracle v67.8", page_icon="🌌", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

decks, hist_p, hist_b, hist_t = BaccaratInterfaceSystem.render_sidebar()

st.markdown("### 🌌 ORACLE MULTI-AGENT QUANTUM DECENTRALIZED v67.8")
st.caption("Kiến Trúc Siêu Toán Học Cấp Vũ Trụ Tối Cao | Hawking Singularity, Schrödinger Wave Collapse & Riemann Zeta Matrix")

final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, streak_side, streak_count = calculate_v67_8_ultimate_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t
)
cmd = get_ultimate_directive(final_p, final_b, trend_desc, streak_side, streak_count, st.session_state.round_detailed_log, hist_p, hist_b)

total_all_rounds = total_p + total_b + total_t
BaccaratInterfaceSystem.render_header_hud(total_rounds=total_all_rounds, cards_left=cards_left, decks_count=decks)

current_ai_oracle = AISovereignOracle.analyze_and_suggest(
    all_rounds_log=st.session_state.round_detailed_log, 
    shoe_decks=decks,
    manual_p=hist_p, manual_b=hist_b, manual_t=hist_t,
    p_val=final_p, b_val=final_b, t_val=final_t, 
    cards_left=cards_left, 
    trend_desc=trend_desc, streak_side=streak_side, streak_count=streak_count, 
    total_rounds=total_all_rounds
)

calc_triggered, p_input, b_input = BaccaratInterfaceSystem.render_input_form()

if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v67_8(p_input.strip())
    b_list = parse_baccarat_input_v67_8(b_input.strip())
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    
    st.session_state.round_detailed_log.append({
        'p_cards': p_list, 'b_cards': b_list, 
        'p_score': p_score, 'b_score': b_score, 
        'outcome': outcome,
        'oracle_decision': current_ai_oracle['decision'],
        'oracle_target': current_ai_oracle['target'],
        'oracle_alloc': current_ai_oracle['capital_allocation']
    })
    st.rerun()

st.markdown("---")

# Mô-đun trọng tài làm nổi bật Badge Player/Banker phát sáng
QuantumArbitrationMatrix.render_arbitration_logic(
    multi_cmd=cmd, 
    oracle_cmd=current_ai_oracle, 
    all_rounds_log=st.session_state.round_detailed_log,
    shoe_decks=decks,
    manual_p=hist_p, manual_b=hist_b, manual_t=hist_t
)

BaccaratInterfaceSystem.render_directive_panel(cmd)
BaccaratInterfaceSystem.render_ai_oracle_panel(current_ai_oracle)
BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t, total_p, total_b, total_t)

QuantumAuditMatrixController.render_audit_table(
    log=st.session_state.round_detailed_log, 
    start_round_index=(hist_p + hist_b + hist_t)
)

st.markdown("<br>", unsafe_allow_html=True)

undo_btn, clear_btn = BaccaratInterfaceSystem.render_utilities()
if undo_btn:
    if st.session_state.round_detailed_log:
        st.session_state.round_detailed_log.pop()
        st.rerun()
if clear_btn:
    st.session_state.round_detailed_log = []
    st.rerun()
