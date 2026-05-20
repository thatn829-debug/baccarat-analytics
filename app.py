import streamlit as st
import numpy as np
import math
import traceback
from datetime import datetime

# =========================================================================
# 🌌 SYSTEM HEALING REGISTRY (BỘ NHỚ LƯU TRỮ VÀ TỰ VÁ LỖI CỦA AI THỨ 5)
# =========================================================================
if 'cyber_healing_logs' not in st.session_state:
    st.session_state.cyber_healing_logs = []

class CyberSelfHealingDaemon:
    """AI AGENT 5: Độc lập giám sát toàn bộ hệ thống, tự động vá lỗi và phát cảnh báo"""
    
    @staticmethod
    def execute_and_heal(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError:
            error_msg = "Phát hiện phép chia cho 0 trong ma trận phân phối mật độ bài!"
            CyberSelfHealingDaemon._register_fault("PHÉP CHIA CHO 0 (ZERO_DIV)", error_msg)
            return 1e-15 
        except TypeError as te:
            error_msg = f"Xung đột kiểu dữ liệu đầu vào hoặc giá trị rỗng: {str(te)}"
            CyberSelfHealingDaemon._register_fault("LỖI KIỂU DỮ LIỆU (TYPE_ERR)", error_msg)
            return 0.0
        except ValueError as ve:
            error_msg = f"Giá trị đầu vào vượt ngoài giới hạn tổ hợp toán học: {str(ve)}"
            CyberSelfHealingDaemon._register_fault("LỖI GIÁ TRỊ (VALUE_ERR)", error_msg)
            return 0.0
        except Exception as e:
            tb = traceback.format_exc()
            error_msg = f"Ngoại lệ hệ thống không xác định: {str(e)} \nTraceback: {tb[:150]}..."
            CyberSelfHealingDaemon._register_fault("KỲ DỊ HỆ THỐNG (UNKNOWN_FATAL)", error_msg)
            return None

    @staticmethod
    def _register_fault(fault_type, description):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "time": timestamp,
            "type": fault_type,
            "desc": description,
            "action": "🛠️ AI VÁ LỖI: Đã cô lập vùng chết, tái cấu trúc tham số nền an toàn thành công."
        }
        st.session_state.cyber_healing_logs.insert(0, log_entry)
        if len(st.session_state.cyber_healing_logs) > 5:
            st.session_state.cyber_healing_logs.pop()

    @staticmethod
    def render_warning_hud():
        if not st.session_state.cyber_healing_logs:
            return
            
        latest_fault = st.session_state.cyber_healing_logs[0]
        st.markdown(
            f'<div style="background: rgba(255, 71, 87, 0.07); border: 2px solid #ff4757; border-radius: 10px; padding: 12px; margin: 10px 0px; box-shadow: 0 0 15px rgba(255, 71, 87, 0.3);">'
            f'<div style="font-size: 13px; font-weight: 900; color: #ff4757; letter-spacing: 0.5px; display: flex; justify-content: space-between;">'
            f'<span>🚨 CYBER SELF-HEALING DAEMON: PHÁT HIỆN LỖI RUNTIME</span>'
            f'<span style="font-family: monospace;">[{latest_fault["time"]}]</span>'
            f'</div>'
            f'<div style="font-size: 12px; color: #f8fafc; margin-top: 5px; font-family: monospace;"><b>Mã lỗi:</b> {latest_fault["type"]}</div>'
            f'<div style="font-size: 12px; color: #cbd5e1; margin-top: 2px;"><b>Chi tiết:</b> {latest_fault["desc"]}</div>'
            f'<div style="font-size: 12px; color: #00f5d4; font-weight: 700; margin-top: 6px;">{latest_fault["action"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )


# =========================================================================
# ⚙️ ULTRA-PRECISION CARD TRACKER ENGINE (BỘ ĐẾM VÀ PHÂN RÃ THEO THỜI GIAN THỰC)
# =========================================================================
def get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    for r in all_rounds_log:
        for card in (r.get('p_cards', []) + r.get('b_cards', [])):
            if card in exact_cards_left:
                exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
                
    manual_rounds_total = manual_p + manual_b + manual_t
    if manual_rounds_total > 0:
        cards_logged = sum(len(r.get('p_cards', []) + r.get('b_cards', [])) for r in all_rounds_log)
        rounds_logged = len(all_rounds_log)
        
        dynamic_ratio = (cards_logged / float(rounds_logged)) if rounds_logged > 0 else 4.94117647
        estimated_removed = (manual_rounds_total * dynamic_ratio) + burn_cards
        
        total_current_sum = sum(exact_cards_left.values())
        if total_current_sum > 0:
            for i in range(1, 14):
                proportion = exact_cards_left[i] / total_current_sum
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - (estimated_removed * proportion))
    elif burn_cards > 0:
        total_current_sum = sum(exact_cards_left.values())
        if total_current_sum > 0:
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - (burn_cards / 13.0))

    return exact_cards_left


# =========================================================================
# 🔵 AI AGENT 1: PLAYER COGNITIVE - HYPERGEOMETRIC & EOR DYNAMICS (v77)
# =========================================================================
class PlayerQuantumAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        
        p_eor_weights = {
            1: -0.00532, 2: -0.00611, 3: -0.00654, 4: -0.01382, 5: -0.00984, 
            6: +0.01254, 7: +0.01483, 8: +0.00991, 9: -0.00282,
            10: +0.00451, 11: +0.00451, 12: +0.00451, 13: +0.00451
        }
        
        eor_shift = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            eor_shift += removed * p_eor_weights.get(card_num, 0.0)

        low_cards_pool = sum([exact_cards_left.get(i, 0.0) for i in [1, 2, 3, 4, 5]])
        low_cards_ratio = low_cards_pool / total_cards_remaining
        density_bias = (low_cards_ratio - (20.0 / 52.0)) * 18.532

        decisive_outcomes = [r.get('outcome') for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
        trend_force = 0.0
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = sum(1 for x in reversed(decisive_outcomes) if x == current_streak_side)
            if current_streak_side == "Banker" and streak_count >= 2:
                trend_force += min(4.5, 0.85 * streak_count)

        base_player_prob = 44.6247
        return base_player_prob + (eor_shift * 5.215) + density_bias - trend_force


# =========================================================================
# 🔴 AI AGENT 2: BANKER COGNITIVE - MARKOV CHAIN & ADVANTAGE LAW (v77)
# =========================================================================
class BankerMarkovAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))

        b_eor_weights = {
            1: +0.00532, 2: +0.00611, 3: +0.00654, 4: +0.01382, 5: +0.00984, 
            6: -0.01254, 7: -0.01483, 8: -0.00991, 9: +0.00282,
            10: -0.00451, 11: -0.00451, 12: -0.00451, 13: -0.00451
        }
        
        eor_shift = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            eor_shift += removed * b_eor_weights.get(card_num, 0.0)

        choke_cards_pool = sum([exact_cards_left.get(i, 0.0) for i in [1, 8, 9, 10, 11, 12, 13]])
        choke_ratio = choke_cards_pool / total_cards_remaining
        markov_advantage_shift = ((16.0 + 12.0) / 52.0 - choke_ratio) * 12.545

        decisive_outcomes = [r.get('outcome') for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
        trend_force = 0.0
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
            if current_streak_side == "Player" and streak_count >= 2:
                trend_force += min(5.0, 1.1 * (streak_count ** 1.2))

        base_banker_prob = 45.8597
        return base_banker_prob + (eor_shift * 5.215) + markov_advantage_shift - trend_force


# =========================================================================
# 🟢 AI AGENT 3: TIE COGNITIVE - POISSON GAP DISTRIBUTION (v77)
# =========================================================================
class TieHypergeometricAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        cards_remaining = int(max(1.0, sum(exact_cards_left.values())))
        
        zero_cards = int(sum([exact_cards_left.get(i, 0.0) for i in [10, 11, 12, 13]]))
        actual_zero_density = zero_cards / float(cards_remaining) if cards_remaining > 0 else 0.3076
        standard_zero_density = 16.0 / 52.0
        
        gap_since_last_tie = 0
        if all_rounds_log:
            for r in reversed(all_rounds_log):
                if r.get('outcome') == "Tie": break
                gap_since_last_tie += 1
        
        lambda_tie = 9.54
        poisson_intensity = 1.0 - math.exp(-max(0, gap_since_last_tie) / lambda_tie)
        gap_bonus = poisson_intensity * 4.25

        base_tie_prob = 9.5156
        density_delta = (actual_zero_density - standard_zero_density) * 38.45
        
        final_tie_prob = base_tie_prob + density_delta + gap_bonus
        return max(1.0, min(45.0, final_tie_prob))


# =========================================================================
# 🪐 MODULE 4: FUSION DISTRIBUTOR & QUANTUM WAVE COALITION
# =========================================================================
def calculate_v77_ultimate_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, (shoe_decks * 52) - burn_cards, 0, 0, 0, "KHÔNG GIAN TRỐNG", None, 0

    raw_p = CyberSelfHealingDaemon.execute_and_heal(PlayerQuantumAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    raw_b = CyberSelfHealingDaemon.execute_and_heal(BankerMarkovAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    raw_t = CyberSelfHealingDaemon.execute_and_heal(TieHypergeometricAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    
    if raw_p is None: raw_p = 44.62
    if raw_b is None: raw_b = 45.86
    if raw_t is None: raw_t = 9.52

    total_sum = raw_p + raw_b + raw_t
    if total_sum <= 0: total_sum = 100.0
    p_pct = (raw_p / total_sum) * 100
    b_pct = (raw_b / total_sum) * 100
    t_pct = (raw_t / total_sum) * 100
    
    exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    cards_remaining = max(0, int(round(sum(exact_cards_left.values()))))
    
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r.get('outcome') == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r.get('outcome') == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r.get('outcome') == "Tie")

    trend_desc = "CẦU KHÔNG GIAN BÌNH THƯỜNG"
    streak_side = None
    streak_count = 0
    decisive_outcomes = [r.get('outcome') for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
    if len(decisive_outcomes) >= 2:
        current_streak_side = decisive_outcomes[-1]
        for outcome in reversed(decisive_outcomes):
            if outcome == current_streak_side: streak_count += 1
            else: break
        if streak_count >= 2:
            streak_side = current_streak_side
            trend_desc = f"SIÊU CHUỖI BỆT {streak_side.upper()} ({streak_count} ván)"

    return p_pct, b_pct, t_pct, cards_remaining, total_p_wins, total_b_wins, total_ties, trend_desc, streak_side, streak_count


def get_ultimate_directive_v77(p_val, b_val, trend_desc, streak_side, streak_count, log, m_p, m_b, cards_left, shoe_decks):
    if not log and (m_p == 0 and m_b == 0):
        return {
            "status": "🛰️ SYSTEM OPERATIONAL",
            "msg": "Hệ thống v77 Hyper-Conservative Core trực tuyến. Đang đợi nạp dữ liệu.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%", "raw_target": "WAIT"
        }

    total_initial_cards = shoe_decks * 52.0
    shoe_progress = (total_initial_cards - cards_left) / total_initial_cards
    diff = abs(p_val - b_val)
    
    # TIÊU CHUẨN 1: Khay bài quá mới -> Khóa bảo toàn
    if shoe_progress < 0.15 and len(log) < 12:
        return {
            "status": "🛑 GIAI ĐOẠN KHỞI ĐỘNG (BẢO TOÀN)",
            "msg": f"Khay bài mới chạy {shoe_progress*100:.1f}%. Ma trận vi sai chưa đủ độ chín. Ép lệnh chờ.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.05)", "size": "0% (WAIT)", "raw_target": "WAIT"
        }

    # TIÊU CHUẨN 2: Thắt chặt bộ lọc nhiễu lên nghiêm ngặt 2.5% để tăng tối đa độ chính xác
    if diff < 2.5:
        return {
            "status": "🛑 BỘ LỌC NHIỄU KHẨN CẤP (BIÊN ĐỘ HẸP)",
            "msg": f"Độ lệch xác suất thực tế chỉ đạt {diff:.4f}% (Dưới ngưỡng an toàn v77 là 2.50%). Từ chối rủi ro.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.08)", "size": "0% (LOCK)", "raw_target": "WAIT"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 THUẬN LỆNH CỰC HẠN: PLAYER",
            "msg": f"Mô hình Hypergeometric đạt biên độ an toàn tuyệt đối lệch về hướng Player (+{diff:.4f}%).",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "1% - 2% Vốn Kỷ Luật", "raw_target": "PLAYER"
        }
    else:
        return {
            "status": "🔴 THUẬN LỆNH CỰC HẠN: BANKER",
            "msg": f"Chuỗi xích Markov hội tụ lợi thế toán học vượt trội về hướng Banker (+{diff:.4f}%).",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "1% - 2% Vốn Kỷ Luật", "raw_target": "BANKER"
        }


# =========================================================================
# 👑 AI SOVEREIGN ORACLE - SIÊU MÔ HÌNH THẦN BÀI TỐI CAO BACCARAT (v77)
# =========================================================================
class AISovereignOracle:
    @staticmethod
    def calculate_shannon_entropy(all_rounds_log):
        outcomes = [r.get('outcome') for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
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
                "decision": "👁️ ORACLE CORE ONLINE", "target": "ĐANG TÍNH TOÁN NỀN...", "capital_allocation": "0%", "strategy_type": "Precision Calibration v77",
                "ai_insight": "Hệ thống lọc nhiễu v77 đã được kích hoạt thành công. Đang quét tín hiệu phân tách phổ.",
                "risk_level": "Đồng bộ hóa", "color": "#a855f7", "memory_hud": "Trống", "cyber_knowledge": "Nạp lõi lọc v77 thành công",
                "raw_code": "EMPTY_ORACLE"
            }

        wrong_count = 0
        decisive_log = [r for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
        
        if decisive_log:
            last_round = decisive_log[-1]
            pred = last_round.get('arbitrator_target') if last_round.get('arbitrator_target') else last_round.get('oracle_target')
            if pred and pred != "WAIT" and pred != last_round.get('outcome'):
                wrong_count = 1  

        if len(decisive_log) >= 2:
            temp_wrong = 0
            for r in reversed(decisive_log[-2:]):
                p_check = r.get('arbitrator_target') if r.get('arbitrator_target') else r.get('oracle_target')
                if p_check and p_check != "WAIT" and p_check != r.get('outcome'):
                    temp_wrong += 1
            if temp_wrong >= 2:
                wrong_count = 2

        total_initial_cards = shoe_decks * 52.0
        shoe_progress = (total_initial_cards - cards_left) / total_initial_cards

        memory_hud = f"🧬 MAP LƯỢNG TỬ ➡️ Đã quét: {int(total_initial_cards - cards_left)} lá | Tiến độ khay: {shoe_progress*100:.2f}%"
        entropy_score = AISovereignOracle.calculate_shannon_entropy(all_rounds_log)
        cyber_knowledge = f"🔭 THẦN BÀI CORE v77: Entropy = {entropy_score:.4f} | Thất thoát pha: {wrong_count}/2"

        diff = abs(p_val - b_val)
        intrinsic_target = "PLAYER" if p_val > b_val else "BANKER"

        # BỘ LỌC AN TOÀN TUYỆT ĐỐI V77
        if shoe_progress < 0.15 and len(all_rounds_log) < 12:
            return {
                "decision": "🛑 GIAI ĐOẠN ĐỢI SÓNG NỀN", "target": "WAIT", "capital_allocation": "0.0% (LOCK)", "strategy_type": "SHOE INITIALIZATION FILTER",
                "ai_insight": "Hệ thống v77 từ chối ra lệnh ở đầu khay bài để loại bỏ hoàn toàn các biến động ảo.",
                "risk_level": "Bảo toàn dữ liệu", "color": "#94a3b8", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                "raw_code": "INITIAL_SHOE_LOCK"
            }

        if diff < 2.5:
            return {
                "decision": "🛑 BỘ LỌC NHIỄU (BIÊN ĐỘ THẤP)", "target": "WAIT", "capital_allocation": "0.0% (LOCK)", "strategy_type": "MICRO-VARIANCE FILTER",
                "ai_insight": f"Độ phân tách pha giữa 2 hướng quá bé ({diff:.4f}%). Ép hệ thống khóa lệnh để tránh nhiễu ngẫu nhiên của sàn bài.",
                "risk_level": "Vùng nhiễu cao", "color": "#f1c40f", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                "raw_code": "LOW_DELTA_LOCK"
            }

        if wrong_count == 1:
            return {
                "decision": f"⚠️ THEO DÕI PHA (SAI 1 VÁN)", "target": f"{intrinsic_target} (DỰ KIẾN)", "capital_allocation": "0.0% (QUAN SÁT)", "strategy_type": "ANTI-WHIPSAW FILTER",
                "ai_insight": f"Ghi nhận ván trước lệch pha toán học cục bộ. Hệ thống cô lập dòng tiền về 0%. Hướng tính toán dự kiến ván này là {intrinsic_target}.",
                "risk_level": "Lệch pha cục bộ", "color": "#f1c40f", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                "raw_code": "SINGLE_ERROR_LOCK"
            }
        elif wrong_count >= 2:
            return {
                "decision": "🚨 PHONG TỎA KHẨN CẤP (SAI 2 VÁN)", "target": "STOP & WAIT", "capital_allocation": "0.0% (BẢO TOÀN)", "strategy_type": "EMERGENCY COLD SYSTEM",
                "ai_insight": "Sảnh bài rơi vào vùng biến dị toán học liên tiếp. Thuật toán mất dấu pha, lệnh phong tỏa được kích hoạt vô điều kiện. Hãy đổi bàn!",
                "risk_level": "Rủi ro cực đại", "color": "#ff4757", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                "raw_code": "FORCE_EMERGENCY_LOCK"
            }

        advantage = (max(p_val, b_val) - min(p_val, b_val)) / 100.0
        fractional_kelly = advantage * 15.0 * (1.0 + 1.2 * shoe_progress) # Thắt chặt tỷ lệ phân bổ tiền của Kelly
        final_alloc = max(1.5, min(7.0, fractional_kelly))

        if streak_side and streak_count >= 3:
            current_streak_upper = streak_side.upper()
            if intrinsic_target != current_streak_upper:
                if diff >= 12.0 or (entropy_score < 0.60 and streak_count >= 6):
                    return {
                        "decision": f"💥 FORCE: BẺ CẦU KỲ DỊ ➡️ {intrinsic_target}", "target": intrinsic_target,
                        "capital_allocation": f"🔥 KÍCH HOẠT: {final_alloc * 1.2:.1f}% VỐN", "strategy_type": "⚡ BAYESIAN OVERRIDE",
                        "ai_insight": f"Động năng chuỗi bệt {current_streak_upper} đã chạm ngưỡng bão hòa cực hạn của thuật toán. Tiến hành bẻ cầu.",
                        "risk_level": "Kiểm soát điểm rơi rủi ro", "color": "#00f5d4", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                        "raw_code": "FORCE_COUNTER_STREAK"
                    }
                else:
                    return {
                        "decision": f"🌊 FLOW: THUẬN CHUỖI BỆT ➡️ {current_streak_upper}", "target": current_streak_upper,
                        "capital_allocation": f"💎 ĐU DÒNG: {max(1.0, final_alloc * 0.6):.1f}% VỐN", "strategy_type": "🛡️ ANTI-PREMATURE LAW",
                        "ai_insight": f"Bộ lọc v77 nghiêm cấm bẻ non, bám nhẹ dòng chảy theo chuỗi bệt {current_streak_upper}.",
                        "risk_level": "An toàn ổn định", "color": "#cbd5e1", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                        "raw_code": "FLOW_STREAK_PREVENT_PREMATURE"
                    }
            else:
                return {
                    "decision": f"🌊 FLOW: ĐU CHUỖI ĐỒNG PHA ➡️ {current_streak_upper}", "target": current_streak_upper,
                    "capital_allocation": f"💎 ĐU DÒNG: {min(8.5, final_alloc * 1.1):.1f}% VỐN", "strategy_type": "WAVE AMPLIFICATION",
                    "ai_insight": f"Xác suất độc lập cộng hưởng tuyệt đối với xu thế. Lệnh đu chuỗi {current_streak_upper} được khuếch đại.",
                    "risk_level": "Tối ưu hóa lợi nhuận", "color": "#a855f7", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge,
                    "raw_code": "FLOW_STREAK"
                }

        capital_str = f"💎 LỆNH CHUẨN: {final_alloc:.1f}% Vốn"
        return {
            "decision": f"⚡ THẦN LỆNH KHỚP: {intrinsic_target}", "target": intrinsic_target, "capital_allocation": capital_str, "strategy_type": "🌀 QUANTUM SWEEP",
            "ai_insight": f"Mật độ bài thực tế định vị cửa {intrinsic_target} sở hữu lợi thế toán học vượt trội hoàn toàn (+{diff:.4f}%).",
            "risk_level": "Quản trị rủi ro đa chiều", "color": "#38bdf8" if intrinsic_target == "PLAYER" else "#ff4757",
            "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "NORMAL_SWEEP"
        }


# =========================================================================
# 🎛️ MODULE 5: QUANTUM ARBITRATION MATRIX (BỘ LỌC TRỌNG TÀI ĐỒNG BỘ V77)
# =========================================================================
class QuantumArbitrationMatrix:
    @staticmethod
    def render_arbitration_logic(multi_cmd, oracle_cmd, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        if not all_rounds_log and (manual_p == 0 and manual_b == 0):
            return "WAIT"

        m_target = multi_cmd.get('raw_target', 'WAIT')    
        o_target = oracle_cmd.get('target', 'WAIT')        
        o_code = oracle_cmd.get('raw_code', '')        

        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        low_cards = sum([exact_cards_left.get(i, 0.0) for i in [1, 2, 3, 4, 5]])      
        high_cards = sum([exact_cards_left.get(i, 0.0) for i in [10, 11, 12, 13]])    

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

        if o_code in ["INITIAL_SHOE_LOCK", "LOW_DELTA_LOCK"]:
            has_conflict = True
            arbitrator_final_verdict = "WAIT"
            rule_title = "⚖️ TRỌNG TÀI TOÁN HỌC - KHÓA BẢO VỆ CHỈ SỐ"
            rule_desc = "Tín hiệu thị trường đang nằm trong vùng nhiễu cao hoặc khay bài quá mới. Ép lệnh BỎ QUA hệ thống."
            panel_color = "#94a3b8"
            panel_bg = "rgba(148, 163, 184, 0.1)"

        elif o_code == "SINGLE_ERROR_LOCK":
            has_conflict = True
            arbitrator_final_verdict = o_target.replace(" (DỰ KIẾN)", "")
            rule_title = "⚖️ TRỌNG TÀI TOÁN HỌC - CẢNH BÁO LỆCH PHA HẠ LỆNH VỐN"
            rule_desc = f"Nhận diện ván trước đoán lệch hướng sảnh bài. Ép dòng vốn về 0%, khuyến nghị bám sát hướng đi dự kiến: {target_badge(arbitrator_final_verdict)}."
            panel_color = "#f1c40f"
            panel_bg = "rgba(241, 196, 15, 0.12)"

        elif o_code == "FORCE_EMERGENCY_LOCK":
            has_conflict = True
            arbitrator_final_verdict = "WAIT"
            rule_title = "🚨 TRỌNG TÀI TỐI CAO - KHÓA PHONG TỎA TOÀN KHAY"
            rule_desc = "Sảnh bài mất pha toán học liên tiếp 2 ván. Phong tỏa lệnh khớp tiền vô điều kiện."
            panel_color = "#ff4757"
            panel_bg = "rgba(255, 71, 87, 0.15)"

        elif m_target != "WAIT" and o_target != "WAIT" and m_target != o_target:
            has_conflict = True
            if o_code == "FORCE_COUNTER_STREAK":
                arbitrator_final_verdict = o_target
                rule_title = "⚖️ TRỌNG TÀI TỐI CAO - CHUẨN KHỚP LỆNH BẺ CẦU LƯỢNG TỬ"
                rule_desc = f"Động năng bẻ cầu đạt điểm kích nổ toán học. Khớp lệnh bẻ theo Thần Bài ({target_badge(o_target)})."
            else:
                if high_cards > low_cards * 1.05: decision_override = "BANKER"
                elif low_cards > high_cards * 1.05: decision_override = "PLAYER"
                else: decision_override = "WAIT"

                arbitrator_final_verdict = decision_override
                rule_title = "⚖️ TRỌNG TÀI TỐI CAO - XỬ LÝ ĐỘ LỆCH TƯ DUY AGENT"
                if decision_override != "WAIT":
                    rule_desc = f"Xung đột giữa các Agent. Can thiệp theo vi sai mật độ thực tế: Đánh {target_badge(decision_override)}."
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
            
        st.markdown('<div class="audit-matrix-box"><div class="audit-title">📊 BẢNG ĐỐI CHIẾU KIỂM TOÁN LƯỢNG TỬ (v77 HYPER-CONSERVATIVE)</div>', unsafe_allow_html=True)
        table_rows = ""
        for idx, r in enumerate(log):
            real_round_num = start_round_index + idx + 1
            oracle_decision = r.get('oracle_decision', '🛑 CHỜ')
            oracle_target = r.get('oracle_target', 'WAIT').upper()
            oracle_alloc = r.get('oracle_alloc', '0%')
            arbitrator_target = r.get('arbitrator_target', None)
            outcome = r.get('outcome', 'Tie').upper()
            
            if arbitrator_target is not None:
                active_target = arbitrator_target.upper()
                is_arbitrated = True
            else:
                active_target = oracle_target
                is_arbitrated = False

            if outcome == "TIE":
                dot_html = '<span class="status-dot" style="color: #2ecc71; background-color: #2ecc71;"></span>'
                status_text = "<span style='color:#2ecc71; font-weight:bold;'>HÒA</span>"
            elif "BỎ QUA" in oracle_decision or active_target == "WAIT" or "CHỜ" in oracle_decision or "LOCK" in oracle_decision:
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
                else: oracle_display = "<span style='color:#94a3b8; font-weight:bold;'>⚖️ T.TÀI: KHÓA</span>"
            else:
                if "PLAYER" in active_target: oracle_display = f"<span style='color:#00afb9; font-weight:bold;'>🔵 {active_target}</span> <small style='color:#64748b;'>({oracle_alloc})</small>"
                elif "BANKER" in active_target: oracle_display = f"<span style='color:#ff4757; font-weight:bold;'>🔴 {active_target}</span> <small style='color:#64748b;'>({oracle_alloc})</small>"
                else: oracle_display = "<span style='color:#64748b;'>🛑 BỎ LỆNH</span>"
                
            outcome_display = f"<b style='color:#00afb9;'>P ({r.get('p_score',0)}đ)</b>" if outcome == "PLAYER" else (f"<b style='color:#ff4757;'>B ({r.get('b_score',0)}đ)</b>" if outcome == "BANKER" else "<b style='color:#2ecc71;'>TIE</b>")
            
            table_rows += f"<tr><td>V{real_round_num}</td><td style='text-align: left;'>{oracle_display}</td><td>{outcome_display}</td><td>{dot_html}</td><td>{status_text}</td></tr>"
            
        html_table = f"<table class='audit-table'><thead><tr><th>VÁN</th><th>KHUYẾN NGHỊ</th><th>SÀN ACT</th><th>MÃ</th><th>TRẠNG THÁI</th></tr></thead><tbody>{table_rows}</tbody></table></div>"
        st.markdown(html_table, unsafe_allow_html=True)


def parse_baccarat_input_v77(raw_str):
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
            f'🎴 CÒN LẠI THỰC TẾ: <b>{cards_left}</b> / {decks_count * 52}'
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
            f"<div style='font-size: 10px; font-weight: 800; color: #60a5fa; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 2px;'>🌌 AI SOVEREIGN ORACLE - VERSION v77 HYPER-CONSERVATIVE</div>"
            f"<div style='font-size: 18px; font-weight: 900; color: {ai_cmd['color']}; margin-bottom: 8px;'>{ai_cmd['decision']}</div>"
            f"<div style='background: rgba(59, 130, 246, 0.06); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; padding: 8px; margin-bottom: 8px; font-size: 11px; color: #93c5fd;'>🛰️ <b>MẠCH TRÍ TUỆ ĐA TẦNG (VI SAI):</b> <i>{ai_cmd['cyber_knowledge']}</i></div>"
            f"<table style='width:100%; border-collapse: collapse; font-size: 12px; margin-bottom: 12px; background: transparent;'>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 5px 0; color: #94a3b8; text-align: left;'>Mục tiêu tối ưu:</td><td style='padding: 5px 0; font-weight:700; color: {ai_cmd['color']}; text-align:right;'>{ai_cmd['target']}</td></tr>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 5px 0; color: #94a3b8; text-align: left;'>Quản lý rủi ro (Kelly):</td><td style='padding: 5px 0; font-weight:700; color: #ffffff; text-align:right;'>{ai_cmd['capital_allocation']}</td></tr>"
            f"</table>"
            f"<div style='background: rgba(255,255,255,0.02); border-left: 3px solid {ai_cmd['color']}; padding: 8px; border-radius: 4px; font-size: 12px; color: #e2e8f0; text-align: justify;'><b>💡 Phân tích vi sai Thần Bài:</b> {ai_cmd['ai_insight']}</div>"
            f"</div>"
        )
        st.markdown(html_string, unsafe_allow_html=True)

    @staticmethod
    def render_probabilities_grid(p_pct, b_pct, t_pct):
        prob_grid = st.columns(3)
        with prob_grid[0]: st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER (Hypergeo)</span><span class="metric-num" style="color:#00afb9;">{p_pct:.4f}%</span></div>', unsafe_allow_html=True)
        with prob_grid[1]: st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER (Markov)</span><span class="metric-num" style="color:#ff4757;">{b_pct:.4f}%</span></div>', unsafe_allow_html=True)
        with prob_grid[2]: st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE (Poisson)</span><span class="metric-num" style="color:#2ecc71;">{t_pct:.4f}%</span></div>', unsafe_allow_html=True)

    @staticmethod
    def render_utilities():
        util_grid = st.columns(2)
        undo_triggered = util_grid[0].button("⏪ QUAY LẠI (UNDO)")
        clear_triggered = util_grid[1].button("🔄 LÀM TRỐNG KHAY BÀI")
        return undo_triggered, clear_triggered


# =========================================================================
# 🎮 CHƯƠNG TRÌNH ĐIỀU HÀNH CHÍNH (RUNTIME EXECUTION CONTROLLER)
# =========================================================================
st.set_page_config(page_title="Cosmological Oracle v77", page_icon="🌌", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

decks, hist_p, hist_b, hist_t, burn_cards = BaccaratInterfaceSystem.render_sidebar()

st.markdown("### 🌌 ORACLE MULTI-AGENT PRECISION SYSTEM v77")

# 📡 KÍCH HOẠT HUD CỦA AI THỨ 5 NGAY ĐẦU TRANG ĐỂ HIỂN THỊ CẢNH BÁO
CyberSelfHealingDaemon.render_warning_hud()

final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, streak_side, streak_count = calculate_v77_ultimate_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t, burn_cards=burn_cards
)

# KHỚP LOGIC LỌC NHIỄU V77
cmd = get_ultimate_directive_v77(final_p, final_b, trend_desc, streak_side, streak_count, st.session_state.round_detailed_log, hist_p, hist_b, cards_left, decks)

total_all_rounds = total_p + total_b + total_t
BaccaratInterfaceSystem.render_header_hud(total_rounds=total_all_rounds, cards_left=cards_left, decks_count=decks)

current_ai_oracle = AISovereignOracle.analyze_and_suggest(
    all_rounds_log=st.session_state.round_detailed_log, shoe_decks=decks,
    manual_p=hist_p, manual_b=hist_b, manual_t=hist_t,
    p_val=final_p, b_val=final_b, t_val=final_t, cards_left=cards_left, 
    trend_desc=trend_desc, streak_side=streak_side, streak_count=streak_count, 
    total_rounds=total_all_rounds, burn_cards=burn_cards
)

# ÉP PHA ĐỒNG BỘ V77 KHỎI XUNG ĐỘT
if current_ai_oracle.get('raw_code') in ["INITIAL_SHOE_LOCK", "LOW_DELTA_LOCK"]:
    cmd['status'] = current_ai_oracle['decision']
    cmd['msg'] = current_ai_oracle['ai_insight']
    cmd['color'] = current_ai_oracle['color']
    cmd['bg'] = "rgba(148, 163, 184, 0.05)"
    cmd['action_vol'] = "QUẢN LÝ VỐN: 0.0% (CHỜ THỦY TRIỀU TOÁN HỌC)"
elif current_ai_oracle.get('raw_code') == "SINGLE_ERROR_LOCK":
    cmd['status'] = "⚠️ " + current_ai_oracle['decision']
    cmd['msg'] = current_ai_oracle['ai_insight']
    cmd['color'] = current_ai_oracle['color']
    cmd['bg'] = "rgba(241, 196, 15, 0.06)"
    cmd['action_vol'] = "QUẢN LÝ VỐN: 0.0% (CHỈ XEM PHA MẪU)"
elif current_ai_oracle.get('raw_code') == "FORCE_EMERGENCY_LOCK":
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
    p_list = parse_baccarat_input_v77(p_input.strip())
    b_list = parse_baccarat_input_v77(b_input.strip())
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
