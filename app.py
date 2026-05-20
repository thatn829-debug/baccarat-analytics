import streamlit as st
import numpy as np
import math

# =========================================================================
# 🧬 HỆ THỐNG TOÁN HỌC LƯỢNG TỬ VÀ KHÔNG GIAN XÁC SUẤT (COMBINATORIAL UTILITIES)
# =========================================================================
class MathQuantumUniverse:
    @staticmethod
    def lgamma_comb(n, k):
        """Tính tổ hợp C(n, k) bằng hàm Log-Gamma để tránh tràn số với độ chính xác tuyệt đối"""
        if k < 0 or k > n or n < 0: return 0.0
        if k == 0 or k == n: return 1.0
        return math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1))

    @staticmethod
    def exact_hypergeometric_prob(k_success_req, n_sample, total_success_pool, total_cards):
        """Phân phối siêu hình để tính xác suất rút chính xác tập hợp lá bài mong muốn"""
        if total_cards <= 0 or n_sample > total_cards: return 0.0
        num = MathQuantumUniverse.lgamma_comb(total_success_pool, k_success_req) * \
              MathQuantumUniverse.lgamma_comb(total_cards - total_success_pool, n_sample - k_success_req)
        den = MathQuantumUniverse.lgamma_comb(total_cards, n_sample)
        return num / max(1e-12, den)


# =========================================================================
# 🔵 AI AGENT 1: PLAYER COGNITIVE - HYPERGEOMETRIC & EOR DYNAMICS (v75)
# =========================================================================
class PlayerQuantumAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        # 1. Trích xuất cấu trúc bài thực tế (Real-time Deck Composition Analysis)
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)} # 1-9, 10,11,12,13 (Hình)
        
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
        
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        
        # 2. Thuật toán EOR (Effect of Removal) phi tuyến tính tối ưu cho Player
        # Lá bài nhỏ (1-5) có lợi cho Banker khi bị rút mất => tăng tỷ lệ Player
        # Lá bài lớn (6-9) có lợi cho Player khi bị rút mất => giảm tỷ lệ Player
        p_eor_weights = {
            1: -0.0053, 2: -0.0061, 3: -0.0065, 4: -0.0138, 5: -0.0098, 
            6: +0.0125, 7: +0.0148, 8: +0.0099, 9: -0.0028,
            10: +0.0045, 11: +0.0045, 12: +0.0045, 13: +0.0045
        }
        
        eor_shift = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            eor_shift += removed * p_eor_weights[card_num]

        # 3. Tính toán xác suất bốc lá thứ 3 dựa trên mật độ bài thấp (Low Cards Density)
        # Nếu khay còn nhiều bài nhỏ (1-5), Player rất dễ tối ưu hóa điểm số khi bị ép rút lá thứ 3
        low_cards_pool = sum([exact_cards_left[i] for i in [1, 2, 3, 4, 5]])
        low_cards_ratio = low_cards_pool / total_cards_remaining
        density_bias = (low_cards_ratio - (20.0 / 52.0)) * 18.5

        # 4. Tích hợp Động lượng Chuỗi (Bayesian Trend Momentum)
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        trend_force = 0.0
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = sum(1 for x in reversed(decisive_outcomes) if x == current_streak_side)
            if current_streak_side == "Banker" and streak_count >= 2:
                # Cầu bệt Banker làm suy giảm tạm thời xác suất Player tự nhiên (Luật hấp dẫn chuỗi)
                trend_force += min(4.5, 0.85 * streak_count)

        base_player_prob = 44.62
        return base_player_prob + (eor_shift * 5.2) + density_bias - trend_force


# =========================================================================
# 🔴 AI AGENT 2: BANKER COGNITIVE - MARKOV CHAIN & ADVANTAGE LAW (v75)
# =========================================================================
class BankerMarkovAgent:
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
        
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))

        # 1. Thuật toán EOR phi tuyến tính dành riêng cho cửa Banker
        b_eor_weights = {
            1: +0.0053, 2: +0.0061, 3: +0.0065, 4: +0.0138, 5: +0.0098, 
            6: -0.0125, 7: -0.0148, 8: -0.0099, 9: +0.0028,
            10: -0.0045, 11: -0.0045, 12: -0.0045, 13: -0.0045
        }
        
        eor_shift = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            eor_shift += removed * b_eor_weights[card_num]

        # 2. Trạng thái Xích Markov (Ưu thế đi sau và ma trận rút lá thứ 3)
        # Banker được quyền rút lá thứ 3 dựa vào lá thứ 3 của Player. 
        # Nếu khay bài đang dư thừa các lá [0, 1, 8, 9] (Lá triệt tiêu thế bốc của Banker), lợi thế Banker giảm đi.
        choke_cards_pool = sum([exact_cards_left[i] for i in [1, 8, 9, 10, 11, 12, 13]])
        choke_ratio = choke_cards_pool / total_cards_remaining
        markov_advantage_shift = ((16.0 + 12.0) / 52.0 - choke_ratio) * 12.5

        # 3. Xử lý giảm chấn chuỗi (Damping Factor) để tránh đu đỉnh cầu bệt quá sâu
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        trend_force = 0.0
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
            if current_streak_side == "Player" and streak_count >= 2:
                trend_force += min(5.0, 1.1 * (streak_count ** 1.2))

        base_banker_prob = 45.86
        return base_banker_prob + (eor_shift * 5.2) + markov_advantage_shift - trend_force


# =========================================================================
# 🟢 AI AGENT 3: TIE COGNITIVE - POISSON GAP DISTRIBUTION (v75)
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
        
        # 1. Toán học tổ hợp cặp trùng (Pair Matching Combinatorics)
        # Cửa Hòa xuất hiện cao nhất khi các lá bài có giá trị 0 (10, J, Q, K) có mật độ cực dày đặc
        zero_cards = int(sum([exact_cards_left[i] for i in [10, 11, 12, 13]]))
        actual_zero_density = zero_cards / float(cards_remaining)
        standard_zero_density = 16.0 / 52.0
        
        # 2. Phân phối Poisson tìm điểm rơi khoảng cách (Gap Probability Decay)
        # Xác suất xuất hiện ván Hòa tuân theo phân phối Poisson tích lũy qua số ván chưa về Hòa
        gap_since_last_tie = 0
        if all_rounds_log:
            for r in reversed(all_rounds_log):
                if r['outcome'] == "Tie": break
                gap_since_last_tie += 1
        
        # Định luật Poisson: P(X=0) = e^(-λ). Khi khoảng cách vượt quá λ (Trung bình 9.5 ván có 1 ván Hòa)
        lambda_tie = 9.5
        poisson_intensity = 1.0 - math.exp(-max(0, gap_since_last_tie) / lambda_tie)
        gap_bonus = poisson_intensity * 4.2

        base_tie_prob = 9.52
        density_delta = (actual_zero_density - standard_zero_density) * 38.0
        
        final_tie_prob = base_tie_prob + density_delta + gap_bonus
        return max(1.0, min(45.0, final_tie_prob))


# =========================================================================
# 🪐 MODULE 4: FUSION DISTRIBUTOR & QUANTUM WAVE COALITION
# =========================================================================
def calculate_v75_ultimate_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r['outcome'] == "Tie")
    total_decisive = total_p_wins + total_b_wins
    
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, (shoe_decks * 52) - burn_cards, 0, 0, 0, "KHÔNG GIAN TRỐNG", None, 0

    # Khởi chạy 3 Agent chuyên biệt độc lập
    raw_p = PlayerQuantumAgent.compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    raw_b = BankerMarkovAgent.compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    raw_t = TieHypergeometricAgent.compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    
    # Chuẩn hóa chuẩn xác tổng xác suất (Normalizing to 100%)
    total_sum = raw_p + raw_b + raw_t
    p_pct = (raw_p / total_sum) * 100
    b_pct = (raw_b / total_sum) * 100
    t_pct = (raw_t / total_sum) * 100
    
    total_initial_cards = shoe_decks * 52
    sidebar_rounds = manual_p + manual_b + manual_t
    cards_spent_estimated = (sidebar_rounds * 4.9452) + burn_cards
    cards_spent_actual = sum(len(r['p_cards'] + r['b_cards']) for r in all_rounds_log)
    cards_remaining = max(0, int(total_initial_cards - (cards_spent_estimated + cards_spent_actual)))
    
    trend_desc = "CẦU KHÔNG GIAN BÌNH THƯỜNG"
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
            "status": "🛰️ SYSTEM OPERATIONAL",
            "msg": "Hệ thống toán học xác suất lượng tử v75 sẵn sàng. Chờ nạp chuỗi dữ liệu.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%", "raw_target": "WAIT"
        }

    diff = abs(p_val - b_val)
    if diff < 1.4:
        return {
            "status": "🛑 LỆNH KHÓA AN TOÀN",
            "msg": f"Biên độ sóng phân tách quá hẹp ({diff:.2f}%), từ chối rủi ro ngẫu nhiên.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%", "raw_target": "WAIT"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 THUẬN LỆNH: PLAYER",
            "msg": f"Mô hình tổ hợp Hypergeometric phân tách lệch về hướng Player (+{diff:.2f}%).",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "2% - 4% Vốn", "raw_target": "PLAYER"
        }
    else:
        return {
            "status": "🔴 THUẬN LỆNH: BANKER",
            "msg": f"Chuỗi xích Markov hội tụ lợi thế toán học về hướng Banker (+{diff:.2f}%).",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "2% - 4% Vốn", "raw_target": "BANKER"
        }


# =========================================================================
# 👑 AI SOVEREIGN ORACLE - SIÊU MÔ HÌNH THẦN BÀI TỐI CAO BACCARAT (v75)
# =========================================================================
class AISovereignOracle:
    @staticmethod
    def calculate_shannon_entropy(all_rounds_log):
        """Tính toán độ hỗn loạn (Entropy) của sảnh để phát hiện cầu ngẫu nhiên hoặc cầu bệt"""
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
                "decision": "👁️ ORACLE CORE ONLINE", "target": "ĐANG TÍNH TOÁN NỀN...", "capital_allocation": "0%", "strategy_type": "Bayesian Calibration v75",
                "ai_insight": "Siêu toán học Thần Bài đã nạp toàn bộ lý thuyết Baccarat học (Kelly, Markov, Poisson, EOR). Đang đợi dữ liệu đầu tiên.",
                "risk_level": "Đồng bộ hóa", "color": "#a855f7", "memory_hud": "Trống", "cyber_knowledge": "Nạp lõi v75 thành công",
                "raw_code": "EMPTY_ORACLE"
            }

        # Kiểm tra lịch sử lệch pha (Anti-Whipsaw Mechanism)
        wrong_count = 0
        decisive_log = [r for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        
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

        # Tính toán tiến độ khay bài phục vụ Kelly tiêu chuẩn
        total_initial_cards = shoe_decks * 52.0
        shoe_progress = (total_initial_cards - cards_left) / total_initial_cards

        memory_hud = f"🧬 MAP LƯỢNG TỬ ➡️ Đã quét: {int(total_initial_cards - cards_left)} lá | Tiến độ khay: {shoe_progress*100:.1f}%"
        entropy_score = AISovereignOracle.calculate_shannon_entropy(all_rounds_log)
        cyber_knowledge = f"🔭 THẦN BÀI CORE: Entropy = {entropy_score:.4f} | Sai lệch pha: {wrong_count}/2"

        diff = abs(p_val - b_val)
        intrinsic_target = "PLAYER" if p_val > b_val else "BANKER"

        # CƠ CHẾ ĐỒNG BỘ THEO DÕI NĂNG ĐỘNG (Bảo toàn tiền khi sai 1 ván nhưng không mù thông tin)
        if wrong_count == 1:
            return {
                "decision": f"⚠️ THEO DÕI PHA (SAI 1 VÁN)", "target": f"{intrinsic_target} (DỰ KIẾN)", "capital_allocation": "0.0% (QUAN SÁT)", "strategy_type": "ANTI-WHIPSAW FILTER",
                "ai_insight": f"Ghi nhận ván trước lệch pha toán học. Thần bài tạm hạ dòng vốn về 0% để bạn theo dõi nhịp sảnh, tránh bão quay xe. Hướng tính toán dự kiến ván này là {intrinsic_target}.",
                "risk_level": "Lệch pha cục bộ", "color": "#f1c40f", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                "raw_code": "SINGLE_ERROR_LOCK"
            }
        elif wrong_count >= 2:
            return {
                "decision": "🚨 PHONG TỎA KHẨN CẤP (SAI 2 VÁN)", "target": "STOP & WAIT", "capital_allocation": "0.0% (BẢO TOÀN)", "strategy_type": "EMERGENCY COLD SYSTEM",
                "ai_insight": "Sảnh bài rơi vào vùng biến dị toán học liên tiếp. Thuật toán mất dấu pha, lệnh phong tỏa được kích hoạt vô điều kiện. Hãy đổi bàn hoặc reset khay bài ngay lập tức!",
                "risk_level": "Rủi ro cực đại", "color": "#ff4757", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                "raw_code": "FORCE_EMERGENCY_LOCK"
            }

        # Áp dụng Định lý Tiêu chuẩn Kelly tối ưu quản lý vốn (Fractional Kelly Criterion)
        # Giới hạn phân bổ tối đa 10% vốn để bảo vệ tài khoản đường dài theo đúng toán học quản trị rủi ro Baccarat học
        advantage = (max(p_val, b_val) - min(p_val, b_val)) / 100.0
        fractional_kelly = advantage * 22.0 * (1.0 + 1.5 * shoe_progress)
        final_alloc = max(2.0, min(10.0, fractional_kelly))

        # Phân tích chiến thuật bệt/bẻ bài chuyên sâu của Oracle
        if streak_side and streak_count >= 3:
            current_streak_upper = streak_side.upper()
            if intrinsic_target != current_streak_upper:
                # Điều kiện bẻ cầu nghiêm ngặt (Chỉ bẻ khi biên độ sóng hoặc Entropy đạt điểm tới hạn tuyệt đối)
                if diff >= 10.5 or (entropy_score < 0.65 and streak_count >= 6):
                    return {
                        "decision": f"💥 FORCE: BẺ CẦU KỲ DỊ ➡️ {intrinsic_target}", "target": intrinsic_target,
                        "capital_allocation": f"🔥 KÍCH HOẠT: {final_alloc * 1.3:.1f}% VỐN", "strategy_type": "⚡ BAYESIAN OVERRIDE",
                        "ai_insight": f"Động năng chuỗi bệt {current_streak_upper} đã đạt điểm bão hòa cực hạn. Xác suất độc lập hội tụ điểm rơi đảo chiều, cho phép lệnh bẻ cầu.",
                        "risk_level": "Kiểm soát điểm rơi rủi ro", "color": "#00f5d4", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                        "raw_code": "FORCE_COUNTER_STREAK"
                    }
                else:
                    # Chống bẻ non (Luật Baccarat học cốt lõi: Đu chuỗi nhẹ nhàng bảo toàn vốn)
                    return {
                        "decision": f"🌊 FLOW: THUẬN CHUỖI BỆT ➡️ {current_streak_upper}", "target": current_streak_upper,
                        "capital_allocation": f"💎 ĐU DÒNG: {max(1.5, final_alloc * 0.7):.1f}% VỐN", "strategy_type": "🛡️ ANTI-PREMATURE LAW",
                        "ai_insight": f"Dù xác suất độc lập lệch nhẹ sang {intrinsic_target}, nhưng chưa đủ lực phá vỡ gia tốc chuỗi bệt {current_streak_upper}. Tuyệt đối không bẻ non, bám nhẹ dòng chảy.",
                        "risk_level": "An toàn ổn định", "color": "#cbd5e1", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                        "raw_code": "FLOW_STREAK_PREVENT_PREMATURE"
                    }
            else:
                return {
                    "decision": f"🌊 FLOW: ĐU CHUỖI ĐỒNG PHA ➡️ {current_streak_upper}", "target": current_streak_upper,
                    "capital_allocation": f"💎 ĐU DÒNG: {min(12.0, final_alloc * 1.2):.1f}% VỐN", "strategy_type": "🌊 WAVE AMPLIFICATION",
                    "ai_insight": f"Xác suất độc lập cộng hưởng tuyệt đối với xu thế sảnh bài. Lệnh đu chuỗi {current_streak_upper} được khuếch đại dòng tiền.",
                    "risk_level": "Tối ưu hóa lợi nhuận", "color": "#a855f7", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                    "raw_code": "FLOW_STREAK"
                }

        # Trạng thái thị trường chuẩn
        capital_str = f"💎 LỆNH CHUẨN: {final_alloc:.1f}% Vốn"
        return {
            "decision": f"⚡ THẦN LỆNH KHỚP: {intrinsic_target}", "target": intrinsic_target, "capital_allocation": capital_str, "strategy_type": "🌀 QUANTUM SWEEP",
            "ai_insight": f"Mật độ bài thực tế và toán học tổ hợp định vị cửa {intrinsic_target} sở hữu lợi thế toán học vượt trội (+{diff:.2f}%).",
            "risk_level": "Quản trị rủi ro đa chiều", "color": "#38bdf8" if intrinsic_target == "PLAYER" else "#ff4757",
            "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "NORMAL_SWEEP"
        }


# =========================================================================
# 🎛️ MODULE 5: QUANTUM ARBITRATION MATRIX (BỘ LỌC TRỌNG TÀI ĐỒNG BỘ V75)
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
            if "PLAYER" in target_str:
                return '<span style="background: rgba(0, 175, 185, 0.25); color: #00afb9; border: 1px solid #00afb9; padding: 2px 6px; border-radius: 4px; font-weight: 800;">🔵 PLAYER</span>'
            elif "BANKER" in target_str:
                return '<span style="background: rgba(255, 71, 87, 0.25); color: #ff4757; border: 1px solid #ff4757; padding: 2px 6px; border-radius: 4px; font-weight: 800;">🔴 BANKER</span>'
            return f'<b>{target_str}</b>'

        if o_code == "SINGLE_ERROR_LOCK":
            has_conflict = True
            arbitrator_final_verdict = o_target.replace(" (DỰ KIẾN)", "")
            rule_title = "⚖️ TRỌNG TÀI TOÁN HỌC - CẢNH BÁO LỆCH PHA HẠ LỆNH VỐN"
            rule_desc = f"Nhận diện ván trước đoán lệch hướng sảnh bài. Trọng tài ép dòng vốn về <b>0% (NGHỈ XEM)</b>, khuyến nghị bám sát hướng đi dự kiến để kiểm tra độ khớp pha: {target_badge(arbitrator_final_verdict)}."
            panel_color = "#f1c40f"
            panel_bg = "rgba(241, 196, 15, 0.12)"

        elif o_code == "FORCE_EMERGENCY_LOCK":
            has_conflict = True
            arbitrator_final_verdict = "WAIT"
            rule_title = "🚨 TRỌNG TÀI TỐI CAO - KHÓA PHONG TỎA TOÀN KHAY"
            rule_desc = "Sảnh bài mất pha toán học liên tiếp 2 ván. Phong tỏa lệnh khớp tiền vô điều kiện bảo toàn tài khoản. Hãy đổi bàn hoặc làm mới khay bài!"
            panel_color = "#ff4757"
            panel_bg = "rgba(255, 71, 87, 0.15)"

        elif o_code == "SHIELD_SHANNON" and m_target != "WAIT":
            has_conflict = True
            arbitrator_final_verdict = "WAIT"
            rule_title = "⚖️ TRỌNG TÀI TỐI CAO - LÁ CHẮN ĐIỂM KỲ DỊ ENTROPY"
            rule_desc = f"Vùng nhiễu loạn ngẫu nhiên cao, biên độ sóng mỏng dưới ngưỡng an toàn tối thiểu 1.4%. Đóng lệnh."
            panel_color = "#ff4757"
            panel_bg = "rgba(255, 71, 87, 0.12)"

        elif m_target != "WAIT" and o_target != "WAIT" and m_target != o_target:
            has_conflict = True
            if o_code == "FORCE_COUNTER_STREAK":
                arbitrator_final_verdict = o_target
                rule_title = "⚖️ TRỌNG TÀI TỐI CAO - CHUẨN KHỚP LỆNH BẺ CẦU LƯỢNG TỬ"
                rule_desc = f"Động năng bẻ cầu đạt điểm kích nổ toán học. Khớp lệnh bẻ theo Thần Bài ({target_badge(o_target)}) với khối lượng an toàn."
            else:
                if high_cards > low_cards * 1.15: decision_override = "BANKER"
                elif low_cards > high_cards * 1.15: decision_override = "PLAYER"
                else: decision_override = "WAIT"

                arbitrator_final_verdict = decision_override
                rule_title = "⚖️ TRỌNG TÀI TỐI CAO - XỬ LÝ ĐỘ LỆCH TƯ DUY AGENT"
                if decision_override != "WAIT":
                    rule_desc = f"Xung đột giữa các Agent. Trọng tài dùng tỷ trọng mật độ bài lớn/nhỏ thực tế can thiệp: Đánh {target_badge(decision_override)} (Min vốn tối thiểu)."
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
# 📦 MODULE 6: QUANTUM AUDIT MATRIX CONTROLLER (BẢNG KIỂM TOÁN CHÍNH XÁC CAO)
# =========================================================================
class QuantumAuditMatrixController:
    @staticmethod
    def render_audit_table(log, start_round_index):
        if not log: return
            
        st.markdown('<div class="audit-matrix-box"><div class="audit-title">📊 BẢNG ĐỐI CHIẾU KIỂM TOÁN LƯỢNG TỬ (v75 ULTRA-PRECISION)</div>', unsafe_allow_html=True)
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
            elif active_target in outcome or outcome in active_target:
                dot_html = '<span class="status-dot" style="color: #00f5d4; background-color: #00f5d4; box-shadow: 0 0 10px #00f5d4;"></span>'
                status_text = "<span style='color:#00f5d4; font-weight:bold;'>WIN</span>"
            else:
                dot_html = '<span class="status-dot" style="color: #ff4757; background-color: #ff4757;"></span>'
                status_text = "<span style='color:#ff4757; font-weight:bold;'>LỆCH KO</span>"
            
            if is_arbitrated:
                if "PLAYER" in active_target: oracle_display = f"<span style='color:#00f5d4; font-weight:bold;'>⚖️ T.TÀI: PLAYER</span>"
                elif "BANKER" in active_target: oracle_display = f"<span style='color:#00f5d4; font-weight:bold;'>⚖️ T.TÀI: BANKER</span>"
                else: oracle_display = "<span style='color:#ff4757; font-weight:bold;'>⚖️ T.TÀI: KHÓA</span>"
            else:
                if "PLAYER" in active_target: oracle_display = f"<span style='color:#00afb9; font-weight:bold;'>🔵 {active_target}</span> <small style='color:#64748b;'>({oracle_alloc})</small>"
                elif "BANKER" in active_target: oracle_display = f"<span style='color:#ff4757; font-weight:bold;'>🔴 {active_target}</span> <small style='color:#64748b;'>({oracle_alloc})</small>"
                else: oracle_display = "<span style='color:#64748b;'>🛑 BỎ LỆNH</span>"
                
            outcome_display = f"<b style='color:#00afb9;'>P ({r['p_score']}đ)</b>" if outcome == "PLAYER" else (f"<b style='color:#ff4757;'>B ({r['b_score']}đ)</b>" if outcome == "BANKER" else "<b style='color:#2ecc71;'>TIE</b>")
            
            table_rows += f"<tr><td>V{real_round_num}</td><td style='text-align: left;'>{oracle_display}</td><td>{outcome_display}</td><td>{dot_html}</td><td>{status_text}</td></tr>"
            
        html_table = f"<table class='audit-table'><thead><tr><th>VÁN</th><th>KHUYẾN NGHỊ</th><th>SÀN ACT</th><th>MÃ</th><th>TRẠNG THÁI</th></tr></thead><tbody>{table_rows}</tbody></table></div>"
        st.markdown(html_table, unsafe_allow_html=True)


def parse_baccarat_input_v75(raw_str):
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
# 📱 MODULE 7: INTERFACE COGNITIVE
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
        st.markdown("##### 🎴 NHẬP LÁ BÀI THỰC TẾ XUẤT HIỆN:")
        with st.form(key="baccarat_cosmological_intelligence_form", clear_on_submit=True):
            input_grid = st.columns(2)
            with input_grid[0]: p_str = st.text_input("🔵 PLAYER CARD (Ví dụ: A,2,K):", placeholder="Nhập bài")
            with input_grid[1]: b_str = st.text_input("🔴 BANKER CARD (Ví dụ: 7,9):", placeholder="Nhập bài")
            st.write("")
            st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
            triggered = st.form_submit_button("🚀 KHỚP PHƯƠNG TRÌNH THẦN BÀI")
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
            f"<div style='font-size: 10px; font-weight: 800; color: #60a5fa; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 2px;'>🌌 AI SOVEREIGN ORACLE - VERSION v75 MATHEMATICAL MASTER</div>"
            f"<div style='font-size: 18px; font-weight: 900; color: {ai_cmd['color']}; margin-bottom: 8px;'>{ai_cmd['decision']}</div>"
            f"<div style='background: rgba(59, 130, 246, 0.06); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; padding: 8px; margin-bottom: 8px; font-size: 11px; color: #93c5fd;'>🛰️ <b>MẠCH TRÍ TUỆ ĐA TẦNG:</b> <i>{ai_cmd['cyber_knowledge']}</i></div>"
            f"<table style='width:100%; border-collapse: collapse; font-size: 12px; margin-bottom: 12px; background: transparent;'>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 5px 0; color: #94a3b8; text-align: left;'>Mục tiêu tối ưu:</td><td style='padding: 5px 0; font-weight:700; color: {ai_cmd['color']}; text-align:right;'>{ai_cmd['target']}</td></tr>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 5px 0; color: #94a3b8; text-align: left;'>Quản lý rủi ro (Kelly):</td><td style='padding: 5px 0; font-weight:700; color: #ffffff; text-align:right;'>{ai_cmd['capital_allocation']}</td></tr>"
            f"</table>"
            f"<div style='background: rgba(255,255,255,0.02); border-left: 3px solid {ai_cmd['color']}; padding: 8px; border-radius: 4px; font-size: 12px; color: #e2e8f0; text-align: justify;'><b>💡 Phân tích chiến thuật Thần Bài:</b> {ai_cmd['ai_insight']}</div>"
            f"</div>"
        )
        st.markdown(html_string, unsafe_allow_html=True)

    @staticmethod
    def render_probabilities_grid(p_pct, b_pct, t_pct):
        prob_grid = st.columns(3)
        with prob_grid[0]: st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER (Hypergeo)</span><span class="metric-num" style="color:#00afb9;">{p_pct:.1f}%</span></div>', unsafe_allow_html=True)
        with prob_grid[1]: st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER (Markov)</span><span class="metric-num" style="color:#ff4757;">{b_pct:.1f}%</span></div>', unsafe_allow_html=True)
        with prob_grid[2]: st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE (Poisson)</span><span class="metric-num" style="color:#2ecc71;">{t_pct:.1f}%</span></div>', unsafe_allow_html=True)

    @staticmethod
    def render_utilities():
        util_grid = st.columns(2)
        undo_triggered = util_grid[0].button("⏪ QUAY LẠI (UNDO)")
        clear_triggered = util_grid[1].button("🔄 LÀM TRỐNG KHAY BÀI")
        return undo_triggered, clear_triggered


# =========================================================================
# 🎮 CHƯƠNG TRÌNH ĐIỀU HÀNH CHÍNH (RUNTIME EXECUTION CONTROLLER)
# =========================================================================
st.set_page_config(page_title="Cosmological Oracle v75", page_icon="🌌", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

decks, hist_p, hist_b, hist_t, burn_cards = BaccaratInterfaceSystem.render_sidebar()

st.markdown("### 🌌 ORACLE MULTI-AGENT PRECISION SYSTEM v75")

final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, streak_side, streak_count = calculate_v75_ultimate_fusion(
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

# Đồng bộ hiển thị động thái sửa lỗi khóa khi sai 1 ván: Vẫn chỉ hướng đi dự tính
if current_ai_oracle['raw_code'] == "SINGLE_ERROR_LOCK":
    cmd['status'] = "⚠️ " + current_ai_oracle['decision']
    cmd['msg'] = current_ai_oracle['ai_insight']
    cmd['color'] = current_ai_oracle['color']
    cmd['bg'] = "rgba(241, 196, 15, 0.06)"
    cmd['action_vol'] = "QUẢN LÝ VỐN: 0.0% (CHỈ XEM PHA MẪU)"
elif current_ai_oracle['raw_code'] == "FORCE_EMERGENCY_LOCK":
    cmd['status'] = current_ai_oracle['decision']
    cmd['msg'] = current_ai_oracle['ai_insight']
    cmd['color'] = current_ai_oracle['color']
    cmd['bg'] = "rgba(255, 71, 87, 0.08)"
    cmd['action_vol'] = "QUẢN LÝ VỐN: 0.0% (PHONG TỎA KHAY)"

calc_triggered, p_input, b_input = BaccaratInterfaceSystem.render_input_form()

current_arbitrator_verdict = QuantumArbitrationMatrix.render_arbitration_logic(
    multi_cmd=cmd, oracle_cmd=current_ai_oracle, all_rounds_log=st.session_state.round_detailed_log,
    shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t, burn_cards=burn_cards
)

if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v75(p_input.strip())
    b_list = parse_baccarat_input_v75(b_input.strip())
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
BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t)

QuantumAuditMatrixController.render_audit_table(log=st.session_state.round_detailed_log, start_round_index=(hist_p + hist_b + hist_t))

st.markdown("<br>", unsafe_allow_html=True)
undo_btn, clear_btn = BaccaratInterfaceSystem.render_utilities()

if undo_btn and st.session_state.round_detailed_log:
    st.session_state.round_detailed_log.pop()
    st.rerun()

if clear_btn:
    st.session_state.round_detailed_log.clear()
    st.rerun()
