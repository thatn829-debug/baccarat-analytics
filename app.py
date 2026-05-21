import streamlit as st
import numpy as np
import math

# =========================================================================
# 🔵 ALL-SHARE DATA ENGINE: CARD TRACKER CORE (UPGRADED WITH BAYESIAN DRIFT)
# =========================================================================
class ShoeCardTracker:
    @staticmethod
    def get_exact_cards_left(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        """Tính toán chính xác số lượng từng quân bài còn lại với hiệu chỉnh Bayes"""
        # Khởi tạo khay bài ban đầu (mỗi rank từ 1-13 có 4 * số bộ bài)
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        
        # Tổng số ván nhập tay ở Sidebar + Burn Cards
        sidebar_total_rounds = manual_p + manual_b + manual_t
        estimated_cards_removed = (sidebar_total_rounds * 4.9452) + burn_cards
        
        if estimated_cards_removed > 0:
            # Thuật toán Bayes: Điều chỉnh tỷ lệ bài dựa trên kết quả thắng thua ở Sidebar
            # Nếu Player thắng nhiều hơn -> Xu hướng các lá bài có lợi cho Player (bài nhỏ) đã ra nhiều hơn
            total_decisive = max(1, manual_p + manual_b)
            p_win_ratio = manual_p / total_decisive
            b_win_ratio = manual_b / total_decisive
            drift_factor = p_win_ratio - b_win_ratio # Dương nếu Player áp đảo, Âm nếu Banker áp đảo
            
            for i in range(1, 14):
                # Bài nhỏ (1-5) ảnh hưởng Player, bài lớn (6-9) ảnh hưởng Banker
                bias = 0.0
                if i <= 5: bias = 0.05 * drift_factor  # Tăng xác suất đã rút nếu Player thắng nhiều
                elif 6 <= i <= 9: bias = -0.05 * drift_factor
                
                cards_per_rank_removed = (estimated_cards_removed / 13.0) * (1.0 + bias)
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - cards_per_rank_removed)

        # Khấu trừ chính xác tuyệt đối từ log thực tế (Real-time Scan)
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
                    
        return exact_cards_left


# =========================================================================
# 🧠 AI AGENT 1: PLAYER DYNAMIC COMBINATORIAL ENGINE (UPGRADED V69.0)
# =========================================================================
class PlayerExactProbabilityAgent:
    @staticmethod
    def compute_player_probability(exact_cards_left, shoe_decks):
        """Mô hình tổ hợp tuyến tính động (Dynamic EOR) dành riêng cho PLAYER"""
        total_initial_cards = shoe_decks * 52.0
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        shoe_progress = (total_initial_cards - cards_remaining) / total_initial_cards

        # Hệ số EOR nền bản v69.0 tối ưu động
        p_eor_base = {
            1: -0.0045, 2: -0.0058, 3: -0.0062, 4: -0.0124, 5: -0.0085, 
            6: 0.0115, 7: 0.0138, 8: 0.0088, 9: -0.0018, 
            10: 0.0036, 11: 0.0036, 12: 0.0036, 13: 0.0036
        }
        
        # Khếch đại phi tuyến tính khi khay bài đi về cuối (Shoe Depth Amplification)
        dynamic_multiplier = 1.0 / (1.0 - min(0.85, shoe_progress))

        p_bias = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            p_bias += removed * p_eor_base[card_num] * dynamic_multiplier

        # Hàm kích hoạt xác suất Gauss tiệm cận biên
        final_p_base = 44.62 + (p_bias * 2.8)
        return final_p_base


# =========================================================================
# 🧠 AI AGENT 2: BANKER DYNAMIC COMBINATORIAL ENGINE (UPGRADED V69.0)
# =========================================================================
class BankerExactProbabilityAgent:
    @staticmethod
    def compute_banker_probability(exact_cards_left, shoe_decks):
        """Mô hình tổ hợp tuyến tính động (Dynamic EOR) dành riêng cho BANKER"""
        total_initial_cards = shoe_decks * 52.0
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        shoe_progress = (total_initial_cards - cards_remaining) / total_initial_cards

        # Hệ số EOR nền bản v69.0 tối ưu động (Đối xứng phi tuyến)
        b_eor_base = {
            1: 0.0045, 2: 0.0058, 3: 0.0062, 4: 0.0124, 5: 0.0085, 
            6: -0.0115, 7: -0.0138, 8: -0.0088, 9: 0.0018, 
            10: -0.0036, 11: -0.0036, 12: -0.0036, 13: -0.0036
        }
        
        # Khếch đại phi tuyến tính khi khay bài đi về cuối (Shoe Depth Amplification)
        dynamic_multiplier = 1.0 / (1.0 - min(0.85, shoe_progress))

        b_bias = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            b_bias += removed * b_eor_base[card_num] * dynamic_multiplier

        final_b_base = 45.86 + (b_bias * 2.8)
        return final_b_base


# =========================================================================
# 🟢 AI AGENT 3: TIE HYPERGEOMETRIC MATRIX ENGINE
# =========================================================================
class TieHypergeometricAgent:
    @staticmethod
    def compute_tie_probability(exact_cards_left):
        """Tính toán mật độ phân bố mớ cấu trúc tổ hợp Hòa (Tie)"""
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        
        zero_cards = sum([exact_cards_left[i] for i in [10, 11, 12, 13]])
        non_zero_cards = max(0.0, cards_remaining - zero_cards)
        
        z_cards_i = max(0, int(zero_cards))
        nz_cards_i = max(0, int(non_zero_cards))
        rem_cards_i = max(0, int(cards_remaining))

        if rem_cards_i >= 6 and z_cards_i >= 3 and nz_cards_i >= 3:
            c1 = MathQuantumUniverse.lgamma_comb(z_cards_i, 3)
            c2 = MathQuantumUniverse.lgamma_comb(nz_cards_i, 3)
            c3 = MathQuantumUniverse.lgamma_comb(rem_cards_i, 6)
            prob_zero_tie = (c1 * c2) / max(1.0, c3)
        else:
            prob_zero_tie = 0.0

        actual_density = zero_cards / cards_remaining
        standard_density = 16.0 / 52.0
        density_deviation = actual_density - standard_density
        
        base_probability = 9.52 + (density_deviation * 42.0) + (prob_zero_tie * 15.0)
        return max(0.5, min(45.0, base_probability))


# =========================================================================
# 🪐 MATH CORE UTILITIES
# =========================================================================
class MathQuantumUniverse:
    @staticmethod
    def lgamma_comb(n, k):
        if k < 0 or k > n or n < 0: return 0.0
        if k == 0 or k == n: return 1.0
        return math.exp(math.lgamma(float(n) + 1.0) - math.lgamma(float(k) + 1.0) - math.lgamma(float(n - k) + 1.0))


# =========================================================================
# 💡 MODULE 4: FUSION DISTRIBUTOR & SIMULATOR
# =========================================================================
def calculate_v69_0_quantum_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r['outcome'] == "Tie")
    
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, (shoe_decks * 52) - burn_cards, 0, 0, 0, "KHÔNG GIAN TRỐNG", None, 0

    exact_cards_left = ShoeCardTracker.get_exact_cards_left(
        all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards
    )

    # ĐỌC ĐỘC LẬP TỪ CÁC MODULE AI AGENT ĐÃ NÂNG CẤP
    raw_p = PlayerExactProbabilityAgent.compute_player_probability(exact_cards_left, shoe_decks)
    raw_b = BankerExactProbabilityAgent.compute_banker_probability(exact_cards_left, shoe_decks)
    raw_t = TieHypergeometricAgent.compute_tie_probability(exact_cards_left)
    
    total_sum = raw_p + raw_b + raw_t
    p_pct = (raw_p / total_sum) * 100
    b_pct = (raw_b / total_sum) * 100
    t_pct = (raw_t / total_sum) * 100
    
    total_initial_cards = shoe_decks * 52
    sidebar_rounds = manual_p + manual_b + manual_t
    cards_spent_estimated = (sidebar_rounds * 4.9452) + burn_cards
    cards_spent_actual = sum(len(r['p_cards'] + r['b_cards']) for r in all_rounds_log)
    cards_remaining = max(0, int(total_initial_cards - (cards_spent_estimated + cards_spent_actual)))
    
    trend_desc = "TRƯỜNG TỔ HỢP BIẾN ĐỘNG QUY CHUẨN"
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
            trend_desc = f"MÔ HÌNH BỆT CHUỖI {streak_side.upper()} ({streak_count} ván)"

    return p_pct, b_pct, t_pct, cards_remaining, total_p_wins, total_b_wins, total_ties, trend_desc, streak_side, streak_count


def get_ultimate_directive(p_val, b_val, trend_desc, streak_side, streak_count, log, m_p, m_b):
    if not log and (m_p == 0 and m_b == 0):
        return {
            "status": "🛰️ SYSTEM READY V69.0",
            "msg": "Hệ thống ma trận Tensor đã thiết lập trạng thái cân bằng.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%", "raw_target": "WAIT"
        }
    
    diff = abs(p_val - b_val)
    if diff < 0.4:  # Thu hẹp vùng khóa từ 0.5 xuống 0.4 nhờ độ chính xác toán học tăng cao
        return {
            "status": "🛑 KHÓA LỆNH AN TOÀN",
            "msg": f"Biên độ lệch xác suất quá nhỏ ({diff:.2f}%), hệ thống kích hoạt tường lửa phòng vệ.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%", "raw_target": "WAIT"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 THUẬN LỆNH: PLAYER",
            "msg": f"Cấu trúc hạt tổ hợp nghiêng mạnh về Player với biên độ lợi thế +{diff:.2f}%.",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "Phụ thuộc Kelly", "raw_target": "PLAYER"
        }
    else:
        return {
            "status": "🔴 THUẬN LỆNH: BANKER",
            "msg": f"Mật độ khay bài hội tụ áp đảo về phía Banker với biên độ lợi thế +{diff:.2f}%.",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "Phụ thuộc Kelly", "raw_target": "BANKER"
        }


# =========================================================================
# 🪐 AI SOVEREIGN ORACLE - KELLY RISK ADAPTIVE ALLOCATION MANAGEMENT
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
                "decision": "👁️ ORACLE MATRIX V69", "target": "QUÉT ĐỊNH VỊ...", "capital_allocation": "0%", "strategy_type": "Quantum Tensor Matrix 2026",
                "ai_insight": "Hệ thống hấp dẫn toán học liên kết thành công trường dữ liệu sảnh.",
                "risk_level": "Đang đồng bộ", "color": "#a855f7", "memory_hud": "Khay bài trống", "cyber_knowledge": "Đang đồng bộ...",
                "raw_code": "EMPTY_ORACLE"
            }

        exact_cards_left = ShoeCardTracker.get_exact_cards_left(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        low_cards = sum([exact_cards_left[i] for i in [1, 2, 3, 4, 5]])      
        mid_cards = sum([exact_cards_left[i] for i in [6, 7, 8, 9]])         
        high_cards = sum([exact_cards_left[i] for i in [10, 11, 12, 13]])    

        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        shoe_progress = (shoe_decks * 52.0 - total_cards_remaining) / (shoe_decks * 52.0)

        memory_hud = f"🧬 TENSOR MAP ➡️ Đã quét: {int(shoe_decks*52 - total_cards_remaining)} lá | Tiến độ khay: {shoe_progress*100:.1f}% — Thấp(A-5): {int(low_cards)} | Trung(6-9): {int(mid_cards)} | Tây(10-K): {int(high_cards)}"
        entropy_score = AISovereignOracle.calculate_shannon_entropy(all_rounds_log)
        cyber_knowledge = f"🔭 BACKGROUND: Entropy = {entropy_score:.4f} | Bộ hiệu chỉnh Bayes đã áp chế sai số."

        diff = abs(p_val - b_val)
        intrinsic_target = "PLAYER" if p_val > b_val else "BANKER"

        if diff < 0.5:
            return {
                "decision": "🛑 KHÓA VỐN CHỦ ĐỘNG", "target": "WAIT", "capital_allocation": "0.0% (Phòng ngự)", "strategy_type": "QUANTUM SHIELD",
                "ai_insight": f"Độ nhiễu thông tin cao, biên độ lệch mục tiêu quá mỏng ({diff:.2f}%). Kích hoạt chế độ quan sát bảo toàn.",
                "risk_level": "Bất ổn định cao", "color": "#e74c3c", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                "raw_code": "SHIELD_SHANNON"
            }

        win_prob = max(p_val, b_val) / 100.0
        loss_prob = 1.0 - win_prob
        payout_ratio = 0.95 if intrinsic_target == "BANKER" else 1.0
        
        # Công thức Kelly gốc
        raw_kelly = (win_prob * payout_ratio - loss_prob) / payout_ratio
        
        # NÂNG CẤP V69: Fractional Kelly thích ứng dựa theo Entropy (Entropy càng cao, rủi ro càng lớn -> Đi tiền nhỏ lại để an toàn)
        adaptive_fraction = 0.15 * (1.1 - entropy_score) 
        fractional_kelly = max(0.0, raw_kelly * max(0.05, adaptive_fraction)) * 100 
        
        if fractional_kelly <= 0:
            fractional_kelly = 1.0

        final_alloc = min(12.0, fractional_kelly) # Nâng trần vốn tối đa an toàn lên 12% khi bài đẹp tuyệt đối

        capital_str = f"💎 TENSOR ALLOC: {final_alloc:.1f}% Vốn"
        strat_type = "🌀 DYNAMIC KELLY SWEEP"
        risk_lvl = "Kiểm soát rủi ro Bayes"
        color = "#38bdf8" if intrinsic_target == "PLAYER" else "#ff4757"
        ai_insight = f"Lực hấp dẫn ma trận Tensor phân rã độc lập hội tụ tại cửa {intrinsic_target} (+{diff:.2f}%). Thích ứng dòng tiền tối ưu."

        return {
            "decision": f"⚡ THẦN LỆNH V69: {intrinsic_target}", "target": intrinsic_target, "capital_allocation": capital_str, "strategy_type": strat_type,
            "ai_insight": ai_insight, "risk_level": risk_lvl, "color": color, "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
            "raw_code": "NORMAL_SWEEP"
        }


# =========================================================================
# 🎛️ MODULE 9: QUANTUM ARBITRATION MATRIX (BỘ LỌC TRỌNG TÀI RỦI RO)
# =========================================================================
class QuantumArbitrationMatrix:
    @staticmethod
    def calculate_arbitration(multi_cmd, oracle_cmd, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        if not all_rounds_log and (manual_p == 0 and manual_b == 0):
            return None, "WAIT"

        m_target = multi_cmd['raw_target']    
        o_target = oracle_cmd['target']        
        o_code = oracle_cmd['raw_code']        

        exact_cards_left = ShoeCardTracker.get_exact_cards_left(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
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

        if o_code == "SHIELD_SHANNON" and m_target != "WAIT":
            has_conflict = True
            arbitrator_final_verdict = "WAIT"
            rule_title = "⚖️ TRỌNG TÀI TỐI CAO - LÁ CHẮN TENSOR"
            rule_desc = f"Phát hiện biên độ rủi ro tiềm ẩn lớn hơn lợi thế tính toán thực tế. <br><b>HÀNH ĐỘNG: ĐÓNG VỐN AN TOÀN, KHÔNG VÀO LỆNH TẠI VÙNG NHIỄU!</b>"
            panel_color = "#ff4757"
            panel_bg = "rgba(255, 71, 87, 0.12)"

        elif m_target != "WAIT" and o_target != "WAIT" and m_target != o_target:
            has_conflict = True
            if high_cards > low_cards * 1.08: # Siết chặt biên độ trọng tài từ 1.10 xuống 1.08 bảo đảm nhạy bén
                decision_override = "BANKER"
                reason = "Mật độ bài lớn (Hình K-10) còn dầy trong khay ủng hộ cấu trúc kéo thế Banker."
            elif low_cards > high_cards * 1.08:
                decision_override = "PLAYER"
                reason = "Mật độ bài nhỏ nút (A-5) dồn dập tối ưu hóa điểm số tự nhiên của Player."
            else:
                decision_override = "WAIT"
                reason = "Xung đột trường thông tin cân bằng tĩnh, không đạt tiêu chuẩn an toàn xác suất."

            arbitrator_final_verdict = decision_override
            rule_title = "⚖️ TRỌNG TÀI TỐI CAO - ĐỘT PHÁ MATRIX KHAY BÀI"
            if decision_override != "WAIT":
                rule_desc = f"Xung đột thuật toán Agent. Bộ lọc mật độ Tensor xác nhận: {reason} <br><b>HÀNH ĐỘNG: Vào lệnh cửa {target_badge(decision_override)} (Tối thiểu Vốn).</b>"
            else:
                rule_desc = f"Xung đột trực diện, trường hạt cân bằng hệ số an toàn thấp. <br><b>HÀNH ĐỘNG: BỎ QUA HOÀN TOÀN, chờ bước sóng khay bài định hình lại.</b>"
            panel_color = "#00f5d4"
            panel_bg = "rgba(0, 245, 212, 0.1)"

        if has_conflict:
            ui_html = (
                f'<div style="background: {panel_bg}; border: 2px solid {panel_color}; border-radius: 10px; padding: 12px; margin: 10px 0px; box-shadow: 0 0 12px {panel_color}4D; max-width: 100%; box-sizing: border-box; overflow: hidden; word-wrap: break-word;">'
                f'<div style="font-size: 13px; font-weight: 900; color: {panel_color}; letter-spacing: 0.3px; margin-bottom: 4px;">{rule_title}</div>'
                f'<div style="font-size: 12px; color: #f8fafc; line-height: 1.5; text-align: left; overflow: hidden;">{rule_desc}</div>'
                f'</div>'
            )
            return ui_html, arbitrator_final_verdict
        return None, None


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
                <div class="audit-title">📊 BẢNG ĐỐI CHIẾU KIỂM TOÁN TỔ HỢP KHAY BÀI V69.0</div>
            """, 
            unsafe_allow_html=True
        )
        
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
                status_text = "<span style='color:#2ecc71; font-weight:bold;'>HÒA CHUẨN</span>"
            elif "BỎ QUA" in oracle_decision or active_target == "WAIT":
                dot_html = '<span class="status-dot" style="color: #94a3b8; background-color: #94a3b8;"></span>'
                status_text = "<span style='color:#94a3b8;'>BỎ QUA</span>"
            elif active_target == outcome:
                dot_html = '<span class="status-dot" style="color: #00f5d4; background-color: #00f5d4; box-shadow: 0 0 10px #00f5d4;"></span>'
                status_text = "<span style='color:#00f5d4; font-weight:bold;'>WIN</span>"
            else:
                dot_html = '<span class="status-dot" style="color: #ff4757; background-color: #ff4757;"></span>'
                status_text = "<span style='color:#ff4757; font-weight:bold;'>LỆCH KO</span>"
            
            if is_arbitrated:
                if active_target == "PLAYER":
                    oracle_display = f"<span style='color:#00f5d4; font-weight:bold;'>⚖️ T.TÀI: PLAYER</span>"
                elif active_target == "BANKER":
                    oracle_display = f"<span style='color:#00f5d4; font-weight:bold;'>⚖️ T.TÀI: BANKER</span>"
                else:
                    oracle_display = "<span style='color:#ff4757; font-weight:bold;'>⚖️ T.TÀI: KHÓA</span>"
            else:
                if "PLAYER" in active_target:
                    oracle_display = f"<span style='color:#00afb9; font-weight:bold;'>🔵 {active_target}</span> <small style='color:#64748b;'>({oracle_alloc})</small>"
                elif "BANKER" in active_target:
                    oracle_display = f"<span style='color:#ff4757; font-weight:bold;'>🔴 {active_target}</span> <small style='color:#64748b;'>({oracle_alloc})</small>"
                else:
                    oracle_display = "<span style='color:#64748b;'>🛑 BỎ LỆNH</span>"
                
            outcome_display = f"<b style='color:#00afb9;'>P ({r['p_score']}đ)</b>" if outcome == "PLAYER" else (f"<b style='color:#ff4757;'>B ({r['b_score']}đ)</b>" if outcome == "BANKER" else "<b style='color:#2ecc71;'>TIE</b>")
            
            table_rows += (
                f"<tr>"
                f"<td>V{real_round_num}</td>"
                f"<td style='text-align: left;'>{oracle_display}</td>"
                f"<td>{outcome_display}</td>"
                f"<td>{dot_html}</td>"
                f"<td>{status_text}</td>"
                f"</tr>"
            )
            
        html_table = (
            f"<table class='audit-table'>"
            f"<thead><tr><th>VÁN</th><th>KHUYẾN NGHỊ</th><th>SÀN ACT</th><th>MÃ</th><th>TRẠNG THÁI</th></tr></thead>"
            f"<tbody>{table_rows}</tbody>"
            f"</table></div>"
        )
        st.markdown(html_table, unsafe_allow_html=True)


def parse_baccarat_input_v69_0(raw_str):
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
# 📱 MODULE 6: GIAO DIỆN INTERFACE SYSTEM
# =========================================================================
class BaccaratInterfaceSystem:
    @staticmethod
    def inject_custom_css():
        st.markdown(
            """
            <style>
            .stApp { background: #010409 !important; color: #e6edf3 !important; }
            .metrics-container div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; gap: 8px !important; }
            .metrics-container div[data-testid="stHorizontalBlock"] > div { flex: 1 1 0% !important; min-width: 0px !important; }
            
            .header-hud-bar { background: linear-gradient(90deg, #0d1117, #161b22); border: 1px solid #30363d; border-radius: 10px; padding: 10px; margin: 10px 0px 15px 0px; text-align: center; font-family: monospace; font-size: 12px; color: #c9d1d9; }
            .action-panel { border-radius: 12px; padding: 15px; margin: 5px 0px 15px 0px; text-align: center; box-shadow: 0px 5px 20px rgba(0,0,0,0.8); }
            .action-status { font-size: 17px; font-weight: 900; letter-spacing: 0.3px; margin-bottom: 4px; }
            .action-msg { font-size: 12px; opacity: 0.9; margin-bottom: 10px; line-height: 1.4; text-align: justify; }
            .action-vol { font-size: 14px; font-weight: 900; font-family: monospace; border-top: 1px dashed rgba(255,255,255,0.2); padding-top: 8px; }
            .mobile-metric-box { background: #0d1117; border: 1px solid #21262d; border-radius: 8px; padding: 10px 4px; margin-bottom: 5px; display: flex; flex-direction: column; text-align: center; overflow: hidden; }
            .metric-tag { font-size: 9px; font-weight: 800; color: #8b949e; text-transform: uppercase; margin-bottom: 2px; }
            .metric-num { font-size: 16px; font-weight: 900; font-family: monospace; }
            
            .audit-matrix-box { padding: 12px; border-radius: 10px; background-color: #0d1117; border: 1px dashed #58a6ff; margin-top: 15px; box-sizing: border-box; width: 100%; overflow: hidden; }
            .audit-title { font-family: system-ui; font-size: 12px; font-weight: 800; color: #58a6ff; margin-bottom: 10px; letter-spacing: 0.3px; }
            .audit-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 11px; color: #c9d1d9; table-layout: fixed; }
            .audit-table th { padding: 8px 4px; text-align: center; background: #161b22; color: #c9d1d9; border: 1px solid #30363d; font-size: 10px; overflow: hidden; }
            .audit-table td { padding: 8px 4px; text-align: center; border: 1px solid #21262d; vertical-align: middle; line-height: 1.3; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
            
            .audit-table th:nth-child(1), .audit-table td:nth-child(1) { width: 12%; }
            .audit-table th:nth-child(2), .audit-table td:nth-child(2) { width: 43%; text-align: left; white-space: normal; }
            .audit-table th:nth-child(3), .audit-table td:nth-child(3) { width: 18%; }
            .audit-table th:nth-child(4), .audit-table td:nth-child(4) { width: 10%; }
            .audit-table th:nth-child(5), .audit-table td:nth-child(5) { width: 17%; font-size: 10px; white-space: normal; }
            
            .status-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 6px currentColor; }
            
            div.stButton > button { background-color: #21262d !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; border-radius: 8px; font-weight: 800; width: 100% !important; padding: 10px 0px !important; }
            .submit-btn-box div.stButton > button { background-color: #238636 !important; color: #ffffff !important; border: none !important; box-shadow: 0 0 12px rgba(35,134,54,0.4); }
            div[data-testid="stNumberInput"] label { font-size: 11px !important; color: #c9d1d9 !important; }
            .block-container { padding-top: 0.8rem !important; padding-bottom: 0.8rem !important; }
            </style>
            """, 
            unsafe_allow_html=True
        )

    @staticmethod
    def render_sidebar():
        st.sidebar.markdown("### ⚙️ CẤU HÌNH KHAY BÀI TENSOR")
        decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)
        burn_cards = st.sidebar.number_input("🎴 SỐ LÁ RÚT BỎ (BURN CARDS):", min_value=0, max_value=50, value=7, step=1)
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 KHỞI TẠO MA TRẬN BAYES (SIDEBAR)")
        hist_p = st.sidebar.number_input("🔵 PLAYER WINS:", min_value=0, value=0, step=1)
        hist_b = st.sidebar.number_input("🔴 BANKER WINS:", min_value=0, value=0, step=1)
        hist_t = st.sidebar.number_input("🟢 TIE WINS:", min_value=0, value=0, step=1)
        return decks, hist_p, hist_b, hist_t, burn_cards

    @staticmethod
    def render_header_hud(total_rounds, cards_left, decks_count):
        st.markdown(
            f'<div class="header-hud-bar">'
            f'🪐 TỔNG SỐ VÁN: <b>{total_rounds}</b> &nbsp;|&nbsp; '
            f'🎴 BÀI CÒN LẠI: <b>{cards_left}</b> / {decks_count * 52}'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_input_form():
        st.markdown("##### 🎴 NHẬP CHỈ SỐ LÁ BÀI RÚT THỰC TẾ:")
        with st.form(key="baccarat_combinatorial_intelligence_form", clear_on_submit=True):
            input_grid = st.columns(2)
            with input_grid[0]:
                p_str = st.text_input("🔵 PLAYER CARD (Ví dụ: 8 K A):", placeholder="Nhập bài")
            with input_grid[1]:
                b_str = st.text_input("🔴 BANKER CARD (Ví dụ: 7 10):", placeholder="Nhập bài")
            st.write("")
            st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
            triggered = st.form_submit_button("🚀 KÍCH HOẠT QUAN SÁT TỔ HỢP TENSOR")
            st.markdown('</div>', unsafe_allow_html=True)
        return triggered, p_str, b_str

    @staticmethod
    def render_directive_panel(cmd):
        st.markdown(
            f'<div class="action-panel" style="background-color: {cmd["bg"]}; border: 2px solid {cmd["color"]}; color: {cmd["color"]};">'
            f'<div class="action-status">{cmd["status"]}</div>'
            f'<div class="action-msg" style="color: #f1f5f9;">{cmd["msg"]}</div>'
            f'<div class="action-vol font-monospace">HỆ THỐNG QUẢN LÝ RỦI RO: CHỈ THỊ THEO KELLY THÍCH ỨNG CHẶT CHẼ</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_ai_oracle_panel(ai_cmd):
        if "CHƯA ĐỦ DỮ LIỆU" in ai_cmd['decision']:
            st.info(ai_cmd['ai_insight'])
            return

        html_string = (
            f"<div style='background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); border: 2px dashed {ai_cmd['color']}; border-radius: 12px; padding: 15px; margin: 12px 0px; box-shadow: 0px 6px 20px rgba(88,166,255,0.1); max-width:100%; overflow:hidden; word-wrap:break-word;'>"
            f"<div style='font-size: 10px; font-weight: 800; color: #58a6ff; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 2px;'>🌌 AI SOVEREIGN ORACLE - TENSOR MATRIX ENGINE V69.0</div>"
            f"<div style='font-size: 18px; font-weight: 900; color: {ai_cmd['color']}; margin-bottom: 8px;'>{ai_cmd['decision']}</div>"
            f"<div style='background: rgba(88, 166, 255, 0.05); border: 1px solid rgba(88, 166, 255, 0.15); border-radius: 6px; padding: 8px; margin-bottom: 8px; font-size: 11px; color: #a5d6ff;'>🛰️ <b>BỨC XẠ ENTROPY:</b> <i>{ai_cmd['cyber_knowledge']}</i></div>"
            f"<div style='background: rgba(56, 189, 248, 0.04); border: 1px solid rgba(56, 189, 248, 0.15); border-radius: 6px; padding: 8px; margin-bottom: 12px; font-family: monospace; font-size: 11px; color: #79c0ff; line-height: 1.4;'>🧠 <b>BẢN ĐỒ MẬT ĐỘ TENSOR:</b> {ai_cmd['memory_hud']}</div>"
            f"<table style='width:100%; border-collapse: collapse; font-size: 12px; margin-bottom: 12px; background: transparent;'>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 5px 0; color: #8b949e; text-align: left;'>Mục tiêu toán học:</td><td style='padding: 5px 0; font-weight:700; color: {ai_cmd['color']}; text-align:right;'>{ai_cmd['target']}</td></tr>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 5px 0; color: #8b949e; text-align: left;'>Phân bổ dòng vốn tối ưu:</td><td style='padding: 5px 0; font-weight:700; color: #ffffff; text-align:right;'>{ai_cmd['capital_allocation']}</td></tr>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 5px 0; color: #8b949e; text-align: left;'>Hình học lõi:</td><td style='padding: 5px 0; font-weight:700; color: #58a6ff; text-align:right;'>{ai_cmd['strategy_type']}</td></tr>"
            f"<tr><td style='padding: 5px 0; color: #8b949e; text-align: left;'>Mức độ bảo toàn:</td><td style='padding: 5px 0; font-weight:700; color: #ff7b72; text-align:right;'>{ai_cmd['risk_level']}</td></tr>"
            f"</table>"
            f"<div style='background: rgba(255,255,255,0.02); border-left: 3px solid {ai_cmd['color']}; padding: 8px; border-radius: 4px; font-size: 12px; line-height: 1.4; color: #e6edf3; text-align: justify;'><b>💡 Khuyến nghị chiến lược:</b> {ai_cmd['ai_insight']}</div>"
            f"</div>"
        )
        st.markdown(html_string, unsafe_allow_html=True)

    @staticmethod
    def render_probabilities_grid(p_pct, b_pct, t_pct, p_cnt, b_cnt, t_cnt):
        st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
        prob_grid = st.columns(3)
        with prob_grid[0]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER</span><span class="metric-num" style="color:#58a6ff;">{p_pct:.1f}%</span><span style="font-size:9px; opacity:0.5;">Tổng thắng: {p_cnt}</span></div>', unsafe_allow_html=True)
        with prob_grid[1]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER</span><span class="metric-num" style="color:#ff7b72;">{b_pct:.1f}%</span><span style="font-size:9px; opacity:0.5;">Tổng thắng: {b_cnt}</span></div>', unsafe_allow_html=True)
        with prob_grid[2]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE DATA</span><span class="metric-num" style="color:#3fb950;">{t_pct:.1f}%</span><span style="font-size:9px; opacity:0.5;">Tổng thắng: {t_cnt}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def render_utilities():
        util_grid = st.columns(2)
        undo_triggered = util_grid[0].button("⏪ QUAY LẠI (UNDO)")
        clear_triggered = util_grid[1].button("🔄 LÀM TRỐNG KHAY BÀI")
        return undo_triggered, clear_triggered


# =========================================================================
# 🎮 RUNTIME EXECUTION CONTROLLER
# =========================================================================
st.set_page_config(page_title="Quantum Tensor Oracle v69.0", page_icon="🌌", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

decks, hist_p, hist_b, hist_t, burn_cards = BaccaratInterfaceSystem.render_sidebar()

st.markdown("### 🌌 ORACLE QUANTUM TENSOR ENGINE v69.0")

calc_triggered, p_input, b_input = BaccaratInterfaceSystem.render_input_form()

# LUỒNG SỰ KIỆN KHI CẬP NHẬT VÁN BÀI MỚI
if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v69_0(p_input.strip())
    b_list = parse_baccarat_input_v69_0(b_input.strip())
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    
    # Tính toán trạng thái ảo trước khi đẩy dữ liệu vào bộ nhớ log
    temp_p, temp_b, temp_t, _, _, _, _, temp_trend, temp_side, temp_count = calculate_v69_0_quantum_fusion(
        st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t, burn_cards=burn_cards
    )
    temp_ai = AISovereignOracle.analyze_and_suggest(
        st.session_state.round_detailed_log, decks, hist_p, hist_b, hist_t, temp_p, temp_b, temp_t, 0, temp_trend, temp_side, temp_count, 1, burn_cards
    )
    temp_cmd = get_ultimate_directive(temp_p, temp_b, temp_trend, temp_side, temp_count, st.session_state.round_detailed_log, hist_p, hist_b)
    
    # Phân tích Trọng tài tối cao
    _, temp_arb = QuantumArbitrationMatrix.calculate_arbitration(temp_cmd, temp_ai, st.session_state.round_detailed_log, decks, hist_p, hist_b, hist_t, burn_cards)

    # Đẩy dữ liệu đồng bộ
    st.session_state.round_detailed_log.append({
        'p_cards': p_list, 'b_cards': b_list, 
        'p_score': p_score, 'b_score': b_score, 
        'outcome': outcome,
        'oracle_decision': temp_ai['decision'],
        'oracle_target': temp_ai['target'],
        'oracle_alloc': temp_ai['capital_allocation'],
        'arbitrator_target': temp_arb
    })
    st.rerun()

# RENDERING GIAO DIỆN CHÍNH THỨC
final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, streak_side, streak_count = calculate_v69_0_quantum_fusion(
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

arb_html_panel, current_arbitrator_verdict = QuantumArbitrationMatrix.calculate_arbitration(
    multi_cmd=cmd, oracle_cmd=current_ai_oracle, all_rounds_log=st.session_state.round_detailed_log,
    shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t, burn_cards=burn_cards
)

st.markdown("---")

# Render Panel chỉ thị
BaccaratInterfaceSystem.render_directive_panel(cmd)

# Nếu kích hoạt trọng tài phân xử rủi ro -> Hiển thị panel trọng tài
if arb_html_panel:
    st.markdown(arb_html_panel, unsafe_allow_html=True)

BaccaratInterfaceSystem.render_ai_oracle_panel(current_ai_oracle)
BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t, total_p, total_b, total_t)

# Bảng đối chiếu kiểm toán
QuantumAuditMatrixController.render_audit_table(
    log=st.session_state.round_detailed_log, 
    start_round_index=(hist_p + hist_b + hist_t)
)

st.markdown("<br>", unsafe_allow_html=True)

# Công cụ điều khiển bộ nhớ khay bài nhanh
undo_btn, clear_btn = BaccaratInterfaceSystem.render_utilities()
if undo_btn:
    if st.session_state.round_detailed_log:
        st.session_state.round_detailed_log.pop()
        st.rerun()
if clear_btn:
    st.session_state.round_detailed_log = []
    st.rerun()
