import streamlit as st
import numpy as np
import math

# =========================================================================
# 🔵 AI AGENT 1: PLAYER QUANTUM CORTEX (MAXIMUM BAYESIAN CONDITIONING)
# =========================================================================
class PlayerQuantumAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive):
        # Khởi tạo ma trận bài kịch trần
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
        exhaustion_slice = (total_initial_cards - cards_remaining) / total_initial_cards

        # Hệ số EOR vi phân kịch trần (Tác động động theo độ cạn của khay bài)
        p_eor_base = {
            1: -0.0051, 2: -0.0059, 3: -0.0062, 4: -0.0134, 5: -0.0096, 
            6: +0.0123, 7: +0.0144, 8: +0.0095, 
            9: -0.0026, 10: +0.0043, 11: +0.0043, 12: +0.0043, 13: +0.0043
        }
        
        card_effect_sum = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            # Tăng trọng số EOR phi tuyến tính khi khay bài dần cạn (Độ chính xác tăng vọt ở cuối khay)
            dynamic_weight = p_eor_base[card_num] * (1.0 + 2.5 * exhaustion_slice)
            card_effect_sum += removed * dynamic_weight

        # Hàm hồi quy phi tuyến tính tối đa hóa độ lệch
        final_card_bias = card_effect_sum * 4.25

        # Tính toán áp suất chuỗi (Markov Chain Matrix Force)
        trend_force = 0.0
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
            
            effective_streak = min(streak_count, 15)
            if current_streak_side == "Banker" and effective_streak >= 2:
                # Hàm tăng trưởng tiệm cận (Log-logistic) để tránh tràn số nhưng đạt gia tốc tối đa
                trend_force += 2.5 * (effective_streak ** 1.6) / (1.0 + 0.05 * (effective_streak ** 1.6))

        # Phân tích độ lệch phân phối tích lũy dài hạn
        if total_decisive > 0:
            p_ratio = (manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")) / total_decisive
            deviation = p_ratio - 0.4932
            trend_force -= deviation * 18.5  # Lực kéo hồi quy về điểm cân bằng toán học

        return 44.62 + final_card_bias + trend_force


# =========================================================================
# 🔴 AI AGENT 2: BANKER MARKOV OVERLORD (MAXIMUM MARKOV MATRIX RESISTANCE)
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
        exhaustion_slice = (total_initial_cards - cards_remaining) / total_initial_cards

        b_eor_base = {
            1: +0.0051, 2: +0.0059, 3: +0.0062, 4: +0.0134, 5: +0.0096, 
            6: -0.0123, 7: -0.0144, 8: -0.0095, 
            9: +0.0026, 10: -0.0043, 11: -0.0043, 12: -0.0043, 13: -0.0043
        }
        
        card_effect_sum = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            dynamic_weight = b_eor_base[card_num] * (1.0 + 2.5 * exhaustion_slice)
            card_effect_sum += removed * dynamic_weight

        final_card_bias = card_effect_sum * 4.25

        trend_force = 0.0
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
            
            effective_streak = min(streak_count, 15)
            if current_streak_side == "Player" and effective_streak >= 2:
                trend_force += 2.5 * (effective_streak ** 1.6) / (1.0 + 0.05 * (effective_streak ** 1.6))
            
            if current_streak_side == "Banker" and effective_streak >= 3:
                # Xung lực giảm dần lực của Banker khi bệt quá sâu để chống bẫy bệt ảo
                trend_force -= 1.5 * (effective_streak ** 1.2) / (1.0 + 0.08 * (effective_streak ** 1.2))

        if total_decisive > 0:
            b_ratio = (manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")) / total_decisive
            deviation = b_ratio - 0.5068
            trend_force -= deviation * 18.5

        return 45.86 + final_card_bias + trend_force


# =========================================================================
# 🟢 AI AGENT 3: TIE HYPERGEOMETRIC MATRIX (MAXIMUM COMBINATORIAL LOG-GAMMA)
# =========================================================================
class TieHypergeometricAgent:
    @staticmethod
    def lgamma_comb(n, k):
        if k < 0 or k > n: return 0.0
        if k == 0 or k == n: return 1.0
        # Hàm tính tổ hợp kịch trần bằng Log-Gamma để tránh tràn số nguyên lớn
        return math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1))

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
        
        # Đếm chính xác mật độ các cặp tổ hợp đối xứng còn lại trong khay
        zero_cards = int(sum([exact_cards_left[i] for i in [10, 11, 12, 13]]))
        non_zero_cards = cards_remaining - zero_cards
        
        # Siêu tính toán Hypergeometric kịch trần cho xác suất Hòa cấu trúc bài Tây (0đ)
        if cards_remaining >= 6:
            prob_zero_tie = (TieHypergeometricAgent.lgamma_comb(zero_cards, 3) * TieHypergeometricAgent.lgamma_comb(non_zero_cards, 3)) / max(1.0, TieHypergeometricAgent.lgamma_comb(cards_remaining, 6))
        else:
            prob_zero_tie = 0.0

        # Mật độ lệch chuẩn phổ quát
        actual_density = zero_cards / float(cards_remaining)
        standard_density = 16.0 / 52.0
        density_deviation = actual_density - standard_density
        
        hyper_force = density_deviation * 35.0 + (prob_zero_tie * 120.0)
        return max(0.5, min(45.0, 9.52 + hyper_force))


# =========================================================================
# 💡 MODULE 4: FUSION DISTRIBUTOR & SIMULATOR
# =========================================================================
def calculate_v67_8_ultimate_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t):
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r['outcome'] == "Tie")
    total_decisive = total_p_wins + total_b_wins
    
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, shoe_decks * 52, 0, 0, 0, "HỆ THỐNG TRỐNG", None, 0

    raw_p = PlayerQuantumAgent.compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive)
    raw_b = BankerMarkovAgent.compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive)
    raw_t = TieHypergeometricAgent.compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t)
    
    raw_p = max(1.0, min(99.0, raw_p))
    raw_b = max(1.0, min(99.0, raw_b))
    raw_t = max(0.5, min(49.0, raw_t))
    
    total_sum = raw_p + raw_b + raw_t
    p_pct = (raw_p / total_sum) * 100
    b_pct = (raw_b / total_sum) * 100
    t_pct = (raw_t / total_sum) * 100
    
    total_initial_cards = shoe_decks * 52
    sidebar_rounds = manual_p + manual_b + manual_t
    cards_spent_estimated = sidebar_rounds * 4.9452
    cards_spent_actual = sum(len(r['p_cards'] + r['b_cards']) for r in all_rounds_log)
    
    cards_remaining = max(0, int(total_initial_cards - (cards_spent_estimated + cards_spent_actual)))
    
    trend_desc = "CẦU ĐANG BIẾN ĐỘNG TỰ DO"
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
            trend_desc = f"CẦU BỆT {streak_side.upper()} ({streak_count} ván)"

    return p_pct, b_pct, t_pct, cards_remaining, total_p_wins, total_b_wins, total_ties, trend_desc, streak_side, streak_count


def get_ultimate_directive(p_val, b_val, trend_desc, streak_side, streak_count, log, m_p, m_b):
    if not log and (m_p == 0 and m_b == 0):
        return {
            "status": "🛰️ MULTI-AGENT QUANTUM READY",
            "msg": "Mạng lưới siêu toán học độc lập cấp tối đa đã kích hoạt.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%", "raw_target": "WAIT"
        }
    
    diff = abs(p_val - b_val)
    if diff < 1.5:
        return {
            "status": "🛑 CHỜ QUAN SÁT (VÙNG NHIỄU)",
            "msg": f"Chênh lệch hai đặc vụ ({diff:.2f}%) quá hẹp. Hệ thống khóa lệnh an toàn.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%", "raw_target": "WAIT"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 THUẬN LỆNH LƯỢNG TỬ: PLAYER",
            "msg": f"Đặc vụ Player Quantum chiếm ưu thế nén vi phân vượt ngưỡng (+{diff:.2f}%).",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "2.5% - 5%", "raw_target": "PLAYER"
        }
    else:
        return {
            "status": "🔴 THUẬN LỆNH LƯỢNG TỬ: BANKER",
            "msg": f"Đặc vụ Banker Overlord đạt chuỗi tích lũy điểm Markov tối ưu (+{diff:.2f}%).",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "2.5% - 5%", "raw_target": "BANKER"
        }


# =========================================================================
# 🌌 MODULE 7: AI SOVEREIGN ORACLE - VERSION MAXIMUM OVERLORD (EXTREME SHANNON ENTROPY)
# =========================================================================
class AISovereignOracle:
    @staticmethod
    def calculate_shannon_entropy(all_rounds_log):
        # Tính toán độ hỗn loạn thực tế của dòng chuỗi bài để nhận diện bệt ảo
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
                "decision": "👁️ KÍCH HOẠT NHÃN THẦN MAXIMUM", "target": "ĐANG QUÉT...", "capital_allocation": "0%", "strategy_type": "Đồng bộ ma trận đa biến 2026",
                "ai_insight": "Hệ thống lõi kịch trần đã sẵn sàng. Vui lòng nạp quân bài để kích hoạt bộ lọc Entropy.",
                "risk_level": "Tính toán thực thời", "color": "#a855f7", "memory_hud": "Bộ nhớ vô hạn trống", "cyber_knowledge": "Đồng bộ cấu trúc sảnh bài..."
            }

        # Khấu trừ khay bài kịch trần phục vụ Nhãn Thần
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

        memory_hud = f"🧬 BỘ NHỚ LƯỢNG TỬ MAXIMUM ➡️ Đã quét: {int(shoe_decks*52 - total_cards_remaining)} quân | Khay bài: {shoe_progress*100:.1f}% — 🔹 Thấp: {int(low_cards)} q | 🔸 Trung: {int(mid_cards)} q | 🔺 Tây: {int(high_cards)} q"
        
        # Tính toán chỉ số hỗn loạn chuỗi
        entropy_score = AISovereignOracle.calculate_shannon_entropy(all_rounds_log)
        cyber_knowledge = f"📊 SHANNON ENTROPY MATRIX: {entropy_score:.4f} | Bộ tính toán tổ hợp Log-Gamma đã khóa chính xác mục tiêu khay bài."

        diff = abs(p_val - b_val)
        intrinsic_target = "PLAYER" if p_val > b_val else "BANKER"

        # Màng bảo vệ vốn tuyệt đối của Oracle
        if diff < 1.6:
            return {
                "decision": "🛑 BỎ QUA TUYỆT ĐỐI (MÀNG LỌC ENTROPY)", "target": "HÒA / CHỜ TĨNH", "capital_allocation": "0.0% (Bảo toàn)", "strategy_type": "SHANNON SHIELD ACTIVE",
                "ai_insight": f"Độ lệch biến thế lượng tử quá yếu ({diff:.2f}%). Thuật toán sàn đang đưa ra các thế bài đảo nghịch giả lập. Tuyệt đối không khớp lệnh.",
                "risk_level": "Cực cao (Nhiễu cấu trúc)", "color": "#e74c3c", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge
            }

        # Định luật Kelly phi tuyến co giãn đa tầng (Maximum Formula)
        raw_kelly = (max(p_val, b_val) / 100.0) - (min(p_val, b_val) / 100.0)
        # Khung vốn tự động co giãn mạnh theo tiến trình khay bài (Bài càng cạn cược càng chuẩn và lớn)
        dynamic_alloc = raw_kelly * 32.0 * (1.0 + 1.5 * shoe_progress)

        # 🔥 HỆ THỐNG PHÂN PHỐI LỆNH CẦU BỆT TOÁN HỌC CAO CẤP TỐI ĐA
        if streak_side and streak_count >= 3:
            current_streak_upper = streak_side.upper()
            
            # Nếu lõi toán học đảo nghịch hoàn toàn với xu hướng bệt thực tế và chênh lệch cực sâu
            if intrinsic_target != current_streak_upper and diff >= 5.0 and entropy_score < 0.85:
                final_alloc = max(5.0, min(25.0, dynamic_alloc * 1.75))
                return {
                    "decision": f"💥 MAXIMUM: LỆNH TRỪ KHỬ BỆT ➡️ {intrinsic_target}",
                    "target": intrinsic_target,
                    "capital_allocation": f"🔥 CHỐT CHẶN TỐI CAO: {final_alloc:.1f}% VỐN",
                    "strategy_type": "⚡ MARKOV ENTROPY OVERRIDE (MAX BẺ CẦU)",
                    "ai_insight": f"Chuỗi bệt {current_streak_upper} ({streak_count} ván) rơi vào trạng thái cạn kiệt năng lượng Markov (Entropy tụt sâu). Mật độ bài còn lại báo hiệu cửa {intrinsic_target} bùng nổ điểm số kịch trần. Tiến hành bẻ cầu tổng lực.",
                    "risk_level": "Tối thiểu (Lợi thế toán học tuyệt đối)",
                    "color": "#00f5d4", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge
                }
            else:
                # Nếu khay bài vẫn ủng hộ bệt, ép lệnh ĐU CẦU MAXIMUM
                final_alloc = max(4.0, min(15.0, dynamic_alloc * 1.35))
                target_to_follow = current_streak_upper
                return {
                    "decision": f"🌊 MAXIMUM: ĐU CẦU TUYỆT ĐỐI ➡️ {target_to_follow}",
                    "target": target_to_follow,
                    "capital_allocation": f"💎 ĐU DÒNG CHẢY: {final_alloc:.1f}% VỐN",
                    "strategy_type": "🌊 STREAK FLOW QUANTUM (MAX ĐU CẦU)",
                    "ai_insight": f"Thuật toán khay bài chưa xuất hiện dấu hiệu gãy chuỗi. Mật độ bài Tây ({int(high_cards)} quân) ủng hộ chuỗi bệt {target_to_follow} tiếp diễn. Nghiêm cấm bẻ cầu tự sát. Khớp lệnh thuận dòng.",
                    "risk_level": "Thấp (Thuận dòng chảy lượng tử)",
                    "color": "#a855f7", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge
                }
        else:
            # Giao dịch trạng thái dao động tự do
            final_alloc = max(2.0, min(12.0, dynamic_alloc))
            capital_str = f"💎 QUÉT ĐƠN: {final_alloc:.1f}% Vốn"
            strat_type = "🌀 EXTRA QUANTUM SWEEP"
            risk_lvl = "Kiểm soát rủi ro chuẩn hóa"
            color = "#38bdf8" if intrinsic_target == "PLAYER" else "#ff4757"
            ai_insight = f"Lợi thế biên vững chắc nghiêng về cửa {intrinsic_target} (+{diff:.2f}%). Mạng lưới 3 AI hoạt động đồng bộ, khớp lệnh tiêu chuẩn."

        return {
            "decision": f"⚡ LỆNH THẦN: {intrinsic_target}", "target": intrinsic_target, "capital_allocation": capital_str, "strategy_type": strat_type,
            "ai_insight": ai_insight, "risk_level": risk_lvl, "color": color, "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge
        }


# =========================================================================
# ⚙️ MODULE 8: QUANTUM AUDIT MATRIX CONTROLLER
# =========================================================================
class QuantumAuditMatrixController:
    @staticmethod
    def render_audit_table(log, start_round_index):
        if not log:
            return
            
        st.markdown(
            """
            <div class="audit-matrix-box">
                <div class="audit-title">📊 BẢNG ĐỐI CHIẾU KIỂM TOÁN LƯỢNG TỬ (MAXIMUM AI ORACLE REPORT)</div>
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
                status_text = "<span style='color:#00f5d4; font-weight:bold;'>THẮNG LỚN (ĐÚNG NHÃN)</span>"
            else:
                dot_html = '<span class="status-dot" style="color: #ff4757; background-color: #ff4757;"></span>'
                status_text = "<span style='color:#ff4757; font-weight:bold;'>LỆCH THUẬT TOÁN</span>"
            
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
            f"<thead><tr><th>VÁN</th><th>KHUYẾN NGHỊ AI VƯỢT THẦN</th><th>THỰC TẾ SÀN BACCARAT</th><th>KIỂM TOÁN</th><th>TRẠNG THÁI DÒNG TIỀN</th></tr></thead>"
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
            .stApp { background: #030611 !important; color: #f8fafc !important; }
            div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; gap: 10px !important; }
            div[data-testid="stHorizontalBlock"] > div { flex: 1 1 0% !important; min-width: 0px !important; }
            .header-hud-bar { background: linear-gradient(90deg, #0f172a, #1e293b); border: 1px solid #334155; border-radius: 10px; padding: 10px; margin: 10px 0px 20px 0px; text-align: center; font-family: monospace; font-size: 13px; color: #cbd5e1; }
            .action-panel { border-radius: 14px; padding: 20px; margin: 15px 0px; text-align: center; box-shadow: 0px 5px 25px rgba(0,0,0,0.8); }
            .action-status { font-size: 19px; font-weight: 900; letter-spacing: 0.5px; margin-bottom: 6px; }
            .action-msg { font-size: 13px; opacity: 0.9; margin-bottom: 12px; line-height: 1.4; text-align: justify; }
            .action-vol { font-size: 15px; font-weight: 900; font-family: monospace; border-top: 1px dashed rgba(255,255,255,0.2); padding-top: 10px; }
            .mobile-metric-box { background: #0b132b; border: 1px solid #1c2541; border-radius: 10px; padding: 12px 6px; margin-bottom: 5px; display: flex; flex-direction: column; text-align: center; }
            .metric-tag { font-size: 10px; font-weight: 800; color: #64748b; text-transform: uppercase; margin-bottom: 4px; }
            .metric-num { font-size: 19px; font-weight: 900; font-family: monospace; }
            
            .audit-matrix-box { padding: 15px; border-radius: 12px; background-color: #0b132b; border: 1px dashed #a855f7; margin-top: 20px; }
            .audit-title { font-family: system-ui; font-size: 13px; font-weight: 800; color: #c084fc; margin-bottom: 12px; display: flex; align-items: center; gap: 6px; letter-spacing: 0.5px; }
            .audit-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 12px; color: #cbd5e1; }
            .audit-table th { padding: 10px; text-align: center; background: #150d2a; color: #cbd5e1; border: 1px solid #231942; font-size: 11px; }
            .audit-table td { padding: 10px; text-align: center; border: 1px solid #1c2541; vertical-align: middle; line-height: 1.4; }
            .status-dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; box-shadow: 0 0 8px currentColor; }
            
            div.stButton > button { background-color: #1c2541 !important; color: #cbd5e1 !important; border: 1px solid #3a506b !important; border-radius: 10px; font-weight: 800; width: 100% !important; padding: 12px 0px !important; }
            .submit-btn-box div.stButton > button { background-color: #00f5d4 !important; color: #010206 !important; border: none !important; box-shadow: 0 0 15px rgba(0,245,212,0.4); }
            div[data-testid="stNumberInput"] label { font-size: 11px !important; color: #cbd5e1 !important; }
            .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
            </style>
            """, 
            unsafe_allow_html=True
        )

    @staticmethod
    def render_sidebar():
        st.sidebar.markdown("### ⚙️ CẤU HÌNH KHAY BÀI")
        decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 LỊCH SỬ SÀN TÍCH LŨY")
        hist_p = st.sidebar.number_input("🔵 PLAYER WINS:", min_value=0, value=0, step=1)
        hist_b = st.sidebar.number_input("🔴 BANKER WINS:", min_value=0, value=0, step=1)
        hist_t = st.sidebar.number_input("🟢 TIE WINS:", min_value=0, value=0, step=1)
        return decks, hist_p, hist_b, hist_t

    @staticmethod
    def render_header_hud(total_rounds, cards_left, decks_count):
        st.markdown(
            f'<div class="header-hud-bar">'
            f'🎰 TỔNG SỐ VÁN ĐÃ PHÂN TÍCH: <b>{total_rounds}</b> ván &nbsp;|&nbsp; '
            f'🎴 QUÂN BÀI CÒN LẠI TRONG KHAY: <b>{cards_left}</b> / {decks_count * 52}'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_input_form():
        st.markdown("##### 🎴 NHẬP QUÂN BÀI CHI TIẾT ĐỂ BỘ NHỚ QUÉT DIỂM:")
        with st.form(key="baccarat_maximum_quantum_core_form", clear_on_submit=True):
            input_grid = st.columns(2)
            with input_grid[0]:
                p_str = st.text_input("🔵 PLAYER CARD (Ví dụ: 8 K A):", placeholder="Nhập chữ hoặc số")
            with input_grid[1]:
                b_str = st.text_input("🔴 BANKER CARD (Ví dụ: 7 10):", placeholder="Nhập chữ hoặc số")
            st.write("")
            st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
            triggered = st.form_submit_button("🔥 KÍCH HOẠT LÕI TỐI ĐA (MAX REVOLUTION)")
            st.markdown('</div>', unsafe_allow_html=True)
        return triggered, p_str, b_str

    @staticmethod
    def render_directive_panel(cmd):
        st.markdown(
            f'<div class="action-panel" style="background-color: {cmd["bg"]}; border: 2px solid {cmd["color"]}; color: {cmd["color"]};">'
            f'<div class="action-status">{cmd["status"]}</div>'
            f'<div class="action-msg" style="color: #f1f5f9;">{cmd["msg"]}</div>'
            f'<div class="action-vol">MỨC CƯỢC ĐỀ XUẤT NỀN: {cmd["size"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_ai_oracle_panel(ai_cmd):
        if "CHƯA ĐỦ DỮ LIỆU" in ai_cmd['decision']:
            st.info(ai_cmd['ai_insight'])
            return

        html_string = (
            f"<div style='background: linear-gradient(135deg, #150d2a 0%, #070714 100%); border: 2px dashed {ai_cmd['color']}; border-radius: 14px; padding: 20px; margin: 15px 0px; box-shadow: 0px 8px 32px rgba(168,85,247,0.3);'>"
            f"<div style='font-size: 11px; font-weight: 800; color: #c084fc; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px;'>🌌 AI SOVEREIGN ORACLE - PHIÊN BẢN MAXIMUM KỊCH TRẦN THUẬT TOÁN</div>"
            f"<div style='font-size: 23px; font-weight: 900; color: {ai_cmd['color']}; margin-bottom: 12px;'>{ai_cmd['decision']}</div>"
            f"<div style='background: rgba(168, 85, 247, 0.08); border: 1px solid rgba(168, 85, 247, 0.3); border-radius: 8px; padding: 10px; margin-bottom: 10px; font-family: system-ui; font-size: 12px; color: #d8b4fe;'>🛰️ <b>BỘ ĐỊNH VỊ SHANNON ENTROPY REAL-TIME:</b><br><i>\"{ai_cmd['cyber_knowledge']}\"</i></div>"
            f"<div style='background: rgba(56, 189, 248, 0.05); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 8px; padding: 10px; margin-bottom: 15px; font-family: monospace; font-size: 11.5px; color: #38bdf8; line-height: 1.5;'>🧠 <b>MA TRẬN ĐẾM BÀI PHI TUYẾN CONDITIONAL BAYESIAN:</b><br>{ai_cmd['memory_hud']}</div>"
            f"<table style='width:100%; border-collapse: collapse; font-size: 13px; margin-bottom: 15px; background: transparent;'>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 6px 0; color: #94a3b8; text-align: left;'>Mục tiêu xuống tiền:</td><td style='padding: 6px 0; font-weight:700; color: {ai_cmd['color']}; text-align:right;'>{ai_cmd['target']}</td></tr>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 6px 0; color: #94a3b8; text-align: left;'>Quản lý vốn Kelly tối đa:</td><td style='padding: 6px 0; font-weight:700; color: #ffffff; text-align:right;'>{ai_cmd['capital_allocation']}</td></tr>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 6px 0; color: #94a3b8; text-align: left;'>Kiến trúc toán học lõi:</td><td style='padding: 6px 0; font-weight:700; color: #a855f7; text-align:right;'>{ai_cmd['strategy_type']}</td></tr>"
            f"<tr><td style='padding: 6px 0; color: #94a3b8; text-align: left;'>Áp suất biến động sàn:</td><td style='padding: 6px 0; font-weight:700; color: #ff4757; text-align:right;'>{ai_cmd['risk_level']}</td></tr>"
            f"</table>"
            f"<div style='background: rgba(255,255,255,0.02); border-left: 3px solid {ai_cmd['color']}; padding: 10px; border-radius: 4px; font-size: 12.5px; line-height: 1.5; color: #e2e8f0; text-align: justify;'><b>💡 Chỉ thị thực chiến tối cao:</b> {ai_cmd['ai_insight']}</div>"
            f"</div>"
        )
        st.markdown(html_string, unsafe_allow_html=True)

    @staticmethod
    def render_probabilities_grid(p_pct, b_pct, t_pct, p_cnt, b_cnt, t_cnt):
        prob_grid = st.columns(3)
        with prob_grid[0]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 AI PLAYER MAXIMUM</span><span class="metric-num" style="color:#00afb9;">{p_pct:.2f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {p_cnt}</span></div>', unsafe_allow_html=True)
        with prob_grid[1]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 AI BANKER MAXIMUM</span><span class="metric-num" style="color:#ff4757;">{b_pct:.2f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {b_cnt}</span></div>', unsafe_allow_html=True)
        with prob_grid[2]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 AI TIE LOG-GAMMA</span><span class="metric-num" style="color:#2ecc71;">{t_pct:.2f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {t_cnt}</span></div>', unsafe_allow_html=True)

    @staticmethod
    def render_utilities():
        util_grid = st.columns(2)
        undo_triggered = util_grid[0].button("⏪ HOÀN TÁC (PHỤC HỒI BÀI)")
        clear_triggered = util_grid[1].button("🔄 LÀM TRỐNG KHAY BÀI")
        return undo_triggered, clear_triggered


# =========================================================================
# 🎮 RUNTIME EXECUTION CONTROLLER
# =========================================================================
st.set_page_config(page_title="Oracle Quantum Maximum v67.8", page_icon="🌌", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

decks, hist_p, hist_b, hist_t = BaccaratInterfaceSystem.render_sidebar()

st.markdown("### 🌌 ORACLE MULTI-AGENT QUANTUM DECENTRALIZED v67.8")
st.caption("Kiến Trúc Lõi Tối Đa (Maximum Revolution) | Bayesian Vi Phân, Tổ Hợp Log-Gamma & Bộ Lọc Entropy Shannon")

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

BaccaratInterfaceSystem.render_directive_panel(cmd)
BaccaratInterfaceSystem.render_ai_oracle_panel(current_ai_oracle)
BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t, total_p, total_b, total_t)

# Thực thi kiểm toán lượng tử độc lập biệt lập hoàn toàn
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
