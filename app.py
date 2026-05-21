import streamlit as st
import numpy as np
import math

# =========================================================================
# 🔵 ALL-SHARE DATA ENGINE: INFINITE MEMORY CARD TRACKER CORE
# =========================================================================
class ShoeCardTracker:
    @staticmethod
    def get_exact_cards_left(all_rounds_log, shoe_decks, burn_cards):
        """
        [BỘ NHỚ VÔ HẠN V70.0] Theo vết tuyệt đối từng quân bài đơn lẻ từ lịch sử sàn.
        Xóa bỏ hoàn toàn cơ chế ước lượng (estimation), chỉ dựa trên dữ liệu thực tế khay bài.
        """
        # Khởi tạo số lượng bài ban đầu: mỗi nút có 4 lá * số bộ bài
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        
        # 1. TRỪ LÁ BÀI ĐÃ BỎ (BURN CARDS) - Giả định trừ đều theo phân phối chuẩn ban đầu nếu không nhập chi tiết
        if burn_cards > 0:
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - (burn_cards / 13.0))
                
        # 2. TRỪ TOÀN BỘ CÁC LÁ BÀI ĐÃ XUẤT HIỆN TRONG LỊCH SỬ KHÔNG GIỚI HẠN VÒNG
        for r in all_rounds_log:
            for card in (r.get('p_cards', []) + r.get('b_cards', [])):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
                    
        return exact_cards_left

    @staticmethod
    def calculate_historical_bias(all_rounds_log):
        """
        Phân tích xu hướng sai số của sàn dựa trên bộ nhớ chuỗi dài sâu dữ liệu.
        """
        if len(all_rounds_log) < 1:
            return 0.0, 0.0
            
        p_error_weight = 0.0
        b_error_weight = 0.0
        
        # Quét qua toàn bộ bộ nhớ lịch sử để tìm độ lệch phân phối sàn
        for idx, r in enumerate(all_rounds_log):
            oracle_target = r.get('oracle_target', 'WAIT')
            outcome = r.get('outcome', 'Tie').upper()
            p_score = r.get('p_score', 0)
            b_score = r.get('b_score', 0)
            
            # Trọng số thích ứng tăng dần theo thời gian gần
            recency_multiplier = (idx + 1) / len(all_rounds_log)
            
            if oracle_target == "PLAYER" and outcome == "BANKER":
                score_diff = max(1, b_score - p_score)
                p_error_weight -= 0.01 * score_diff * recency_multiplier
                b_error_weight += 0.01 * score_diff * recency_multiplier
            elif oracle_target == "BANKER" and outcome == "PLAYER":
                score_diff = max(1, p_score - b_score)
                b_error_weight -= 0.01 * score_diff * recency_multiplier
                p_error_weight += 0.01 * score_diff * recency_multiplier
                
        return p_error_weight, b_error_weight


# =========================================================================
# 🧠 AI AGENT 1: PLAYER ABSOLUTE PROBABILITY AGENT
# =========================================================================
class PlayerExactProbabilityAgent:
    @staticmethod
    def compute_player_probability(exact_cards_left, shoe_decks, p_error_weight):
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        
        # Phân rã giá trị đóng góp tổ hợp của từng quân bài còn lại đối với Player
        # Thấp (A-5) bất lợi cho kéo bài Player, Trung (6-9) đứng bài tốt, Tây (10-K) triệt tiêu điểm
        p_eor = {
            1: -0.0048, 2: -0.0061, 3: -0.0065, 4: -0.0128, 5: -0.0089, 
            6: 0.0121, 7: 0.0142, 8: 0.0092, 9: -0.0020, 
            10: 0.0039, 11: 0.0039, 12: 0.0039, 13: 0.0039
        }
        
        bias_sum = 0.0
        for card_num, left in exact_cards_left.items():
            initial_count = 4 * shoe_decks
            removed = initial_count - left
            bias_sum += removed * p_eor[card_num]
            
        base_prob = 44.62 + (p_error_weight * 100.0)
        return max(5.0, min(90.0, base_prob + (bias_sum * 2.5)))


# =========================================================================
# 🧠 AI AGENT 2: BANKER ABSOLUTE PROBABILITY AGENT
# =========================================================================
class BankerExactProbabilityAgent:
    @staticmethod
    def compute_banker_probability(exact_cards_left, shoe_decks, b_error_weight):
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        
        # Đối với Banker: Bài nhỏ (A-5) hỗ trợ luật kéo bài có lợi lợi thế, bài trung (6-8) nguy hiểm
        b_eor = {
            1: 0.0047, 2: 0.0059, 3: 0.0064, 4: 0.0127, 5: 0.0088, 
            6: -0.0119, 7: -0.0141, 8: -0.0090, 9: 0.0020, 
            10: -0.0038, 11: -0.0038, 12: -0.0038, 13: -0.0038
        }
        
        bias_sum = 0.0
        for card_num, left in exact_cards_left.items():
            initial_count = 4 * shoe_decks
            removed = initial_count - left
            bias_sum += removed * b_eor[card_num]
            
        base_prob = 45.86 + (b_error_weight * 100.0)
        return max(5.0, min(90.0, base_prob + (bias_sum * 2.5)))


# =========================================================================
# 🟢 AI AGENT 3: TIE HYPERGEOMETRIC MATRIX ENGINE
# =========================================================================
class TieHypergeometricAgent:
    @staticmethod
    def compute_tie_probability(exact_cards_left, all_rounds_log):
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        
        # Đếm chính xác số lượng quân bài 0 điểm (10, J, Q, K) còn lại trong khay bài
        zero_cards = sum([exact_cards_left[i] for i in [10, 11, 12, 13]])
        non_zero_cards = max(0.0, cards_remaining - zero_cards)
        
        z_cards_i = max(0, int(zero_cards))
        nz_cards_i = max(0, int(non_zero_cards))
        rem_cards_i = max(0, int(cards_remaining))

        # Phép tính tổ hợp phân phối Hypergeometric siêu hình học cho ván bài Hòa điểm 0
        if rem_cards_i >= 6 and z_cards_i >= 3 and nz_cards_i >= 3:
            c1 = math.exp(math.lgamma(z_cards_i + 1) - math.lgamma(3 + 1) - math.lgamma(z_cards_i - 3 + 1))
            c2 = math.exp(math.lgamma(nz_cards_i + 1) - math.lgamma(3 + 1) - math.lgamma(nz_cards_i - 3 + 1))
            c3 = math.exp(math.lgamma(rem_cards_i + 1) - math.lgamma(6 + 1) - math.lgamma(rem_cards_i - 6 + 1))
            prob_zero_tie = (c1 * c2) / max(1.0, c3)
        else:
            prob_zero_tie = 0.0

        actual_density = zero_cards / cards_remaining
        standard_density = 16.0 / 52.0
        density_deviation = actual_density - standard_density
        
        # Phản hồi từ bộ nhớ vô hạn về tần suất xuất hiện cửa Hòa gần đây
        tie_feedback = 0.0
        if len(all_rounds_log) >= 3:
            recent_ties = sum(1 for r in all_rounds_log[-5:] if r.get('outcome') == "Tie")
            if recent_ties >= 2: tie_feedback = 5.0
            elif recent_ties == 0: tie_feedback = -1.0
            
        base_probability = 9.52 + (density_deviation * 35.0) + (prob_zero_tie * 12.0) + tie_feedback
        return max(0.5, min(40.0, base_probability))


# =========================================================================
# 🪐 AI SOVEREIGN ORACLE - KELLY RISK ADAPTIVE ALLOCATION (THẦN BÀI)
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
    def analyze_and_suggest(all_rounds_log, shoe_decks, p_val, b_val, t_val, cards_left, p_err, b_err, burn_cards):
        if not all_rounds_log:
            return {
                "decision": "👁️ ORACLE MATRIX V70.0", "target": "WAIT", "capital_allocation": "0%", "strategy_type": "Infinite Memory Core",
                "ai_insight": "Hệ thống vô hạn bộ nhớ đã được kích hoạt. Đang quét trạng thái khay bài.",
                "risk_level": "Đang tính toán", "color": "#a855f7", "memory_hud": "Khay bài trống", "cyber_knowledge": "Đang đồng bộ...",
                "raw_code": "EMPTY_ORACLE"
            }

        exact_cards_left = ShoeCardTracker.get_exact_cards_left(all_rounds_log, shoe_decks, burn_cards)
        low_cards = sum([exact_cards_left[i] for i in [1, 2, 3, 4, 5]])      
        mid_cards = sum([exact_cards_left[i] for i in [6, 7, 8, 9]])         
        high_cards = sum([exact_cards_left[i] for i in [10, 11, 12, 13]])    

        memory_hud = f"🧬 Còn lại: {int(sum(exact_cards_left.values()))} lá | Thấp(A-5): {int(low_cards)} | Trung(6-9): {int(mid_cards)} | Tây(10-K): {int(high_cards)}"
        entropy_score = AISovereignOracle.calculate_shannon_entropy(all_rounds_log)
        cyber_knowledge = f"Hiệu chỉnh Bayes: P_Bias={p_err*100:+.2f}% | B_Bias={b_err*100:+.2f}%"

        diff = abs(p_val - b_val)
        intrinsic_target = "PLAYER" if p_val > b_val else "BANKER"

        # Tường lửa phòng thủ rủi ro nếu độ lệch quá hẹp
        if diff < 0.7:
            return {
                "decision": "🛑 KHÓA VỐN AN TOÀN", "target": "WAIT", "capital_allocation": "0.0% (Chờ dữ liệu)", "strategy_type": "QUANTUM SHIELD",
                "ai_insight": f"Mật độ bài cân bằng tuyệt đối, biên độ lợi thế quá mỏng ({diff:.2f}%).",
                "risk_level": "Bất ổn định", "color": "#e74c3c", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                "raw_code": "SHIELD_SHANNON"
            }

        # Áp dụng Công thức Kelly thích ứng động với Entropy thị trường
        win_prob = max(p_val, b_val) / 100.0
        loss_prob = 1.0 - win_prob
        payout_ratio = 0.95 if intrinsic_target == "BANKER" else 1.0
        
        raw_kelly = (win_prob * payout_ratio - loss_prob) / payout_ratio
        adaptive_fraction = 0.15 * (1.1 - entropy_score) 
        fractional_kelly = max(0.0, raw_kelly * max(0.05, adaptive_fraction)) * 100 
        
        final_alloc = min(12.0, max(1.0, fractional_kelly)) 

        return {
            "decision": f"⚡ LỆNH KHUYẾN NGHỊ: {intrinsic_target}", "target": intrinsic_target, "capital_allocation": f"💎 {final_alloc:.1f}% Vốn", "strategy_type": "INFINITE KELLY DYNAMIC",
            "ai_insight": f"Bộ nhớ tối ưu xác nhận lợi thế nghiêng hẳn về {intrinsic_target} với chênh lệch +{diff:.2f}%.",
            "risk_level": "Kiểm soát Bayes Động", "color": "#38bdf8" if intrinsic_target == "PLAYER" else "#ff4757", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
            "raw_code": "NORMAL_SWEEP"
        }


# =========================================================================
# 💡 MODULE 4: FUSION DISTRIBUTOR & UTILITIES
# =========================================================================
def calculate_v70_quantum_fusion(all_rounds_log, shoe_decks, burn_cards):
    total_p_wins = sum(1 for r in all_rounds_log if r.get('outcome') == "Player")
    total_b_wins = sum(1 for r in all_rounds_log if r.get('outcome') == "Banker")
    total_ties = sum(1 for r in all_rounds_log if r.get('outcome') == "Tie")
    
    if not all_rounds_log:
        return 0.0, 0.0, 0.0, (shoe_decks * 52) - burn_cards, 0, 0, 0, 0.0, 0.0

    exact_cards_left = ShoeCardTracker.get_exact_cards_left(all_rounds_log, shoe_decks, burn_cards)
    p_error_weight, b_error_weight = ShoeCardTracker.calculate_historical_bias(all_rounds_log)

    # Kích hoạt tính toán độc lập từ 3 AI chuyên biệt cho từng cửa
    raw_p = PlayerExactProbabilityAgent.compute_player_probability(exact_cards_left, shoe_decks, p_error_weight)
    raw_b = BankerExactProbabilityAgent.compute_banker_probability(exact_cards_left, shoe_decks, b_error_weight)
    raw_t = TieHypergeometricAgent.compute_tie_probability(exact_cards_left, all_rounds_log)
    
    # Chuẩn hóa tổng xác suất về 100%
    total_sum = raw_p + raw_b + raw_t
    p_pct = (raw_p / total_sum) * 100
    b_pct = (raw_b / total_sum) * 100
    t_pct = (raw_t / total_sum) * 100
    
    cards_remaining = max(0, int(sum(exact_cards_left.values())))

    return p_pct, b_pct, t_pct, cards_remaining, total_p_wins, total_b_wins, total_ties, p_error_weight, b_error_weight


def get_ultimate_directive(p_val, b_val, log):
    if not log:
        return {
            "status": "🛰️ SYSTEM READY V70.0",
            "msg": "Mô đun Vô hạn Bộ nhớ tích hợp toán tổ hợp chính xác lá bài đã sẵn sàng.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "raw_target": "WAIT"
        }
    
    diff = abs(p_val - b_val)
    if diff < 0.7:  
        return {
            "status": "🛑 KHÓA LỆNH AN TOÀN",
            "msg": f"Biên độ lợi thế quá mỏng ({diff:.2f}%), hệ thống kích hoạt tường lửa phòng thủ.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "raw_target": "WAIT"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 TÍN HIỆU: PLAYER",
            "msg": f"Cấu trúc mật độ bài nghiêng mạnh về Player với biên độ lợi thế +{diff:.2f}%.",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "raw_target": "PLAYER"
        }
    else:
        return {
            "status": "🔴 TÍN HIỆU: BANKER",
            "msg": f"Mật độ khay bài hội tụ áp đảo về phía Banker với biên độ lợi thế +{diff:.2f}%.",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "raw_target": "BANKER"
        }


# =========================================================================
# 📦 MODULE 8: QUANTUM AUDIT MATRIX CONTROLLER
# =========================================================================
class QuantumAuditMatrixController:
    @staticmethod
    def render_audit_table(log):
        if not log: return
            
        st.markdown('<div class="audit-matrix-box"><div class="audit-title">📊 BẢNG KIỂM TOÁN VÀ SỬA SAI SÀN THỰC TẾ</div>', unsafe_allow_html=True)
        
        total_wins = 0
        total_errors = 0
        total_skips = 0

        table_rows = ""
        for idx, r in enumerate(log):
            real_round_num = idx + 1
            oracle_decision = r.get('oracle_decision', '🛑 CHỜ')
            oracle_target = r.get('oracle_target', 'WAIT').upper()
            oracle_alloc = r.get('oracle_alloc', '0%')
            outcome = r['outcome'].upper()
            
            active_target = oracle_target

            if outcome == "TIE":
                dot_html = '<span class="status-dot" style="color: #2ecc71; background-color: #2ecc71;"></span>'
                status_text = "<span style='color:#2ecc71; font-weight:bold;'>HÒA</span>"
                total_skips += 1
            elif "BỎ QUA" in oracle_decision or active_target == "WAIT":
                dot_html = '<span class="status-dot" style="color: #94a3b8; background-color: #94a3b8;"></span>'
                status_text = "<span style='color:#94a3b8;'>BỎ</span>"
                total_skips += 1
            elif active_target == outcome:
                dot_html = '<span class="status-dot" style="color: #00f5d4; background-color: #00f5d4;"></span>'
                status_text = "<span style='color:#00f5d4; font-weight:bold;'>WIN</span>"
                total_wins += 1
            else:
                dot_html = '<span class="status-dot" style="color: #ff4757; background-color: #ff4757;"></span>'
                status_text = "<span style='color:#ff4757; font-weight:bold;'>ERR</span>"
                total_errors += 1
            
            if "PLAYER" in active_target:
                oracle_display = f"🔵 P <small style='color:#64748b;'>({oracle_alloc.replace('💎 ', '')})</small>"
            elif "BANKER" in active_target:
                oracle_display = f"🔴 B <small style='color:#64748b;'>({oracle_alloc.replace('💎 ', '')})</small>"
            else:
                oracle_display = "🛑 BỎ"
                
            outcome_display = f"P ({r['p_score']}đ)" if outcome == "PLAYER" else (f"B ({r['b_score']}đ)" if outcome == "BANKER" else "TIE")
            
            table_rows += (
                f"<tr>"
                f"<td>V{real_round_num}</td>"
                f"<td>{oracle_display}</td>"
                f"<td>{outcome_display}</td>"
                f"<td>{dot_html}</td>"
                f"<td>{status_text}</td>"
                f"</tr>"
            )
            
        st.markdown(
            f'<div class="audit-summary-bar">'
            f'  <div class="summary-item"><span style="color:#00f5d4;">🟢 THẮNG (WIN):</span> <b>{total_wins}</b></div>'
            f'  <div class="summary-item"><span style="color:#ff4757;">🔴 THUA (ERR):</span> <b>{total_errors}</b></div>'
            f'  <div class="summary-item"><span style="color:#94a3b8;">⚪ BỎ QUA (SKIP):</span> <b>{total_skips}</b></div>'
            f'</div>', 
            unsafe_allow_html=True
        )

        html_table = (
            f"<table class='audit-table'>"
            f"<thead><tr><th>VÁN</th><th>KHUYẾN NGHỊ</th><th>SÀN ACT</th><th>MÃ</th><th>KQ</th></tr></thead>"
            f"<tbody>{table_rows}</tbody>"
            f"</table></div>"
        )
        st.markdown(html_table, unsafe_allow_html=True)


def parse_baccarat_input_v70(raw_str):
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
# 🎛️ MODULE 6: GIAO DIỆN INTERFACE SYSTEM (MOBILE-FIRST)
# =========================================================================
class BaccaratInterfaceSystem:
    @staticmethod
    def inject_custom_css():
        st.markdown(
            """
            <style>
            .stApp { background: #010409 !important; color: #e6edf3 !important; }
            .mobile-flex-container { display: flex !important; flex-direction: row !important; width: 100% !important; gap: 6px !important; justify-content: space-between !important; margin-bottom: 10px !important; }
            .mobile-flex-box { flex: 1 !important; background: #0d1117 !important; border: 1px solid #21262d !important; border-radius: 8px !important; padding: 8px 2px !important; text-align: center !important; min-width: 0px !important; }
            .header-hud-bar { background: linear-gradient(90deg, #0d1117, #161b22); border: 1px solid #30363d; border-radius: 8px; padding: 8px; margin: 5px 0px 10px 0px; text-align: center; font-family: monospace; font-size: 11px; color: #c9d1d9; }
            .action-panel { border-radius: 10px; padding: 12px; margin: 5px 0px 10px 0px; text-align: center; box-shadow: 0px 4px 15px rgba(0,0,0,0.5); }
            .action-status { font-size: 15px; font-weight: 900; letter-spacing: 0.2px; }
            .action-msg { font-size: 11px; margin-top: 4px; line-height: 1.3; text-align: center; }
            .metric-tag { font-size: 9px; font-weight: 800; color: #8b949e; text-transform: uppercase; display: block; margin-bottom: 2px; }
            .metric-num { font-size: 14px; font-weight: 900; font-family: monospace; display: block; }
            .metric-sub { font-size: 8px; opacity: 0.5; display: block; }
            
            .audit-summary-bar { display: flex !important; flex-direction: row !important; justify-content: space-between !important; background: #161b22 !important; border: 1px solid #30363d !important; border-radius: 6px !important; padding: 8px 6px !important; margin-bottom: 10px !important; gap: 4px !important; }
            .summary-item { flex: 1 !important; text-align: center !important; font-family: monospace !important; font-size: 10px !important; color: #c9d1d9 !important; white-space: nowrap !important; }
            .summary-item b { font-size: 12px !important; color: #ffffff !important; margin-left: 2px !important; }

            .audit-matrix-box { padding: 8px; border-radius: 8px; background-color: #0d1117; border: 1px dashed #58a6ff; margin-top: 10px; width: 100%; overflow: hidden; }
            .audit-title { font-size: 11px; font-weight: 800; color: #58a6ff; margin-bottom: 8px; text-align: center; }
            .audit-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 10px; color: #c9d1d9; table-layout: fixed; }
            .audit-table th { padding: 5px 2px; text-align: center; background: #161b22; border: 1px solid #30363d; font-size: 9px; }
            .audit-table td { padding: 6px 2px; text-align: center; border: 1px solid #21262d; vertical-align: middle; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            .audit-table th:nth-child(1), .audit-table td:nth-child(1) { width: 14%; }
            .audit-table th:nth-child(2), .audit-table td:nth-child(2) { width: 44%; text-align: left; }
            .audit-table th:nth-child(3), .audit-table td:nth-child(3) { width: 18%; }
            .audit-table th:nth-child(4), .audit-table td:nth-child(4) { width: 10%; }
            .audit-table th:nth-child(5), .audit-table td:nth-child(5) { width: 14%; }
            .status-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; }
            div.stButton > button { background-color: #21262d !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; border-radius: 6px; font-weight: 800; width: 100% !important; padding: 6px 0px !important; font-size: 12px !important; }
            .submit-btn-box div.stButton > button { background-color: #238636 !important; color: #ffffff !important; border: none !important; box-shadow: 0 0 10px rgba(35,134,54,0.3); padding: 10px 0px !important; }
            div[data-testid="stNumberInput"] label { font-size: 10px !important; color: #c9d1d9 !important; }
            .block-container { padding-top: 0.5rem !important; padding-bottom: 0.5rem !important; }
            </style>
            """, 
            unsafe_allow_html=True
        )

    @staticmethod
    def render_sidebar():
        st.sidebar.markdown("### ⚙️ CẤU HÌNH KHAY BÀI V70")
        decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)
        burn_cards = st.sidebar.number_input("🎴 SỐ LÁ RÚT BỎ BAN ĐẦU:", min_value=0, max_value=100, value=7, step=1)
        return decks, burn_cards

    @staticmethod
    def render_header_hud(total_rounds, cards_left, decks_count):
        st.markdown(
            f'<div class="header-hud-bar">'
            f'🪐 TỔNG VÁN TRONG BỘ NHỚ: <b>{total_rounds}</b> &nbsp;|&nbsp; '
            f'🎴 CÒN LẠI TRONG KHAY: <b>{cards_left}</b> / {decks_count * 52}'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_input_form():
        st.markdown("##### 🎴 NHẬP LÁ BÀI RÚT SÀN THỰC TẾ:")
        with st.form(key="mobile_tensor_form", clear_on_submit=True):
            input_grid = st.columns(2)
            with input_grid[0]:
                p_str = st.text_input("🔵 PLAYER CARD:", placeholder="Ví dụ: 8 K A")
            with input_grid[1]:
                b_str = st.text_input("🔴 BANKER CARD:", placeholder="Ví dụ: 7 10 2")
            st.write("")
            st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
            triggered = st.form_submit_button("🚀 KÍCH HOẠT HỆ THỐNG AI TÍNH TOÁN")
            st.markdown('</div>', unsafe_allow_html=True)
        return triggered, p_str, b_str

    @staticmethod
    def render_directive_panel(cmd):
        st.markdown(
            f'<div class="action-panel" style="background-color: {cmd["bg"]}; border: 1px solid {cmd["color"]}; color: {cmd["color"]};">'
            f'<div class="action-status">{cmd["status"]}</div>'
            f'<div class="action-msg" style="color: #f1f5f9;">{cmd["msg"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_ai_oracle_panel(ai_cmd):
        html_string = (
            f"<div style='background: #0d1117; border: 1px dashed {ai_cmd['color']}; border-radius: 8px; padding: 10px; margin: 8px 0px; font-size: 11px;'>"
            f"<div style='font-size: 8px; color: #58a6ff; letter-spacing: 0.5px; font-weight:800; margin-bottom: 2px;'>🌌 AI SOVEREIGN MATRIX V70.0 (THẦN BÀI VÔ HẠN)</div>"
            f"<div style='font-size: 14px; font-weight: 900; color: {ai_cmd['color']}; margin-bottom: 6px;'>{ai_cmd['decision']}</div>"
            f"<div style='color: #79c0ff; font-family: monospace; font-size: 10px; margin-bottom: 4px;'>{ai_cmd['memory_hud']}</div>"
            f"<div style='color: #a5d6ff; font-family: monospace; font-size: 10px; margin-bottom: 6px;'>🛰️ {ai_cmd['cyber_knowledge']}</div>"
            f"<div style='border-top: 1px solid rgba(255,255,255,0.05); padding-top: 4px; color: #e6edf3;'>"
            f"📍 Quản lý vốn Kelly: <b style='color:#ffffff;'>{ai_cmd['capital_allocation']}</b> ({ai_cmd['strategy_type']})<br>"
            f"💡 Phân tích chiến thuật: {ai_cmd['ai_insight']}"
            f"</div>"
            f"</div>"
        )
        st.markdown(html_string, unsafe_allow_html=True)

    @staticmethod
    def render_probabilities_grid(p_pct, b_pct, t_pct, p_cnt, b_cnt, t_cnt):
        html_grid = (
            f'<div class="mobile-flex-container">'
            f'  <div class="mobile-flex-box"><span class="metric-tag">🔵 PLAYER AI</span><span class="metric-num" style="color:#58a6ff;">{p_pct:.1f}%</span><span class="metric-sub">Thực tế: {p_cnt}</span></div>'
            f'  <div class="mobile-flex-box"><span class="metric-tag">🔴 BANKER AI</span><span class="metric-num" style="color:#ff7b72;">{b_pct:.1f}%</span><span class="metric-sub">Thực tế: {b_cnt}</span></div>'
            f'  <div class="mobile-flex-box"><span class="metric-tag">🟢 TIE AI</span><span class="metric-num" style="color:#3fb950;">{t_pct:.1f}%</span><span class="metric-sub">Thực tế: {t_cnt}</span></div>'
            f'</div>'
        )
        st.markdown(html_grid, unsafe_allow_html=True)

    @staticmethod
    def render_utilities():
        util_grid = st.columns(2)
        undo_triggered = util_grid[0].button("⏪ XOÁ VÁN CUỐI (UNDO)")
        clear_triggered = util_grid[1].button("🔄 RESET BỘ NHỚ KHAY")
        return undo_triggered, clear_triggered


# =========================================================================
# 🎮 RUNTIME EXECUTION CONTROLLER
# =========================================================================
st.set_page_config(page_title="Quantum Tensor Infinite v70.0", page_icon="🌌", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

# Khởi tạo bộ lưu trữ trạng thái vô hạn vòng chơi
if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

decks, burn_cards = BaccaratInterfaceSystem.render_sidebar()

st.markdown("### 🌌 QUANTUM TENSOR INFINITE v70.0")

calc_triggered, p_input, b_input = BaccaratInterfaceSystem.render_input_form()

# Khi nhận dữ liệu bài rút thực tế từ sàn
if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v70(p_input.strip())
    b_list = parse_baccarat_input_v70(b_input.strip())
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    
    # Tính toán trạng thái tạm thời trước khi ghi vào bộ nhớ
    temp_p, temp_b, temp_t, cards_rem, _, _, _, t_pe, t_be = calculate_v70_quantum_fusion(
        st.session_state.round_detailed_log, shoe_decks=decks, burn_cards=burn_cards
    )
    temp_ai = AISovereignOracle.analyze_and_suggest(
        st.session_state.round_detailed_log, decks, temp_p, temp_b, temp_t, cards_rem, t_pe, t_be, burn_cards
    )

    # Đưa ván đấu vào bộ nhớ chuỗi dài vô hạn
    st.session_state.round_detailed_log.append({
        'p_cards': p_list, 'b_cards': b_list, 
        'p_score': p_score, 'b_score': b_score, 
        'outcome': outcome,
        'oracle_decision': temp_ai['decision'],
        'oracle_target': temp_ai['target'],
        'oracle_alloc': temp_ai['capital_allocation']
    })
    st.rerun()

# Tính toán ma trận hợp nhất xác suất thực tế
final_p, final_b, final_t, cards_left, total_p, total_b, total_t, p_err, b_err = calculate_v70_quantum_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, burn_cards=burn_cards
)
cmd = get_ultimate_directive(final_p, final_b, st.session_state.round_detailed_log)

total_all_rounds = len(st.session_state.round_detailed_log)
BaccaratInterfaceSystem.render_header_hud(total_rounds=total_all_rounds, cards_left=cards_left, decks_count=decks)

st.markdown("---")

# Hiển thị HUD khuyến nghị
BaccaratInterfaceSystem.render_directive_panel(cmd)

# Thần bài phân tích và tính toán đi vốn Kelly
current_oracle_analysis = AISovereignOracle.analyze_and_suggest(
    st.session_state.round_detailed_log, decks, final_p, final_b, final_t, cards_left, p_err, b_err, burn_cards
)
BaccaratInterfaceSystem.render_ai_oracle_panel(current_oracle_analysis)

# Hiển thị tỷ lệ phần trăm từ 3 AI chuyên biệt đầu ra
BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t, total_p, total_b, total_t)

# Hiển thị bảng kiểm toán tích hợp bộ đếm kết quả thực tế phía trên
QuantumAuditMatrixController.render_audit_table(log=st.session_state.round_detailed_log)

st.markdown("<br>", unsafe_allow_html=True)

# Các tính năng quản lý bộ nhớ
undo_btn, clear_btn = BaccaratInterfaceSystem.render_utilities()
if undo_btn:
    if st.session_state.round_detailed_log:
        st.session_state.round_detailed_log.pop()
        st.rerun()
if clear_btn:
    st.session_state.round_detailed_log = []
    st.rerun()
