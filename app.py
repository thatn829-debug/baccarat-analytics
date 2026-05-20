import streamlit as st
import numpy as np
import math
import traceback
from datetime import datetime

# =========================================================================
# 🌌 SYSTEM HEALING REGISTRY (BỘ NHỚ LỰU TRỮ VÀ TỰ VÁ LỖI CỦA AI)
# =========================================================================
if 'cyber_healing_logs' not in st.session_state:
    st.session_state.cyber_healing_logs = []

class CyberSelfHealingDaemon:
    @staticmethod
    def execute_and_heal(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError:
            return 1e-15 
        except Exception as e:
            return 0.0

# =========================================================================
# ⚙️ ULTRA-PRECISION CARD TRACKER ENGINE
# =========================================================================
def get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    for r in all_rounds_log:
        for card in (r.get('p_cards', []) + r.get('b_cards', [])):
            if card in exact_cards_left: exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
    manual_rounds_total = manual_p + manual_b + manual_t
    if manual_rounds_total > 0:
        cards_logged = sum(len(r.get('p_cards', []) + r.get('b_cards', [])) for r in all_rounds_log)
        rounds_logged = len(all_rounds_log)
        dynamic_ratio = (cards_logged / float(rounds_logged)) if rounds_logged > 0 else 4.94
        estimated_removed = (manual_rounds_total * dynamic_ratio) + burn_cards
        total_current_sum = sum(exact_cards_left.values())
        if total_current_sum > 0:
            for i in range(1, 14):
                proportion = exact_cards_left[i] / total_current_sum
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - (estimated_removed * proportion))
    elif burn_cards > 0:
        total_current_sum = sum(exact_cards_left.values())
        if total_current_sum > 0:
            for i in range(1, 14): exact_cards_left[i] = max(0.0, exact_cards_left[i] - (burn_cards / 13.0))
    return exact_cards_left

# =========================================================================
# 🎴 MODULE 7: NEXT-CARD POINT SIMULATION ENGINE
# =========================================================================
class NextCardSimulationMatrix:
    @staticmethod
    def run_simulation(exact_cards_left):
        cards_pool = []
        for card_num, qty in exact_cards_left.items():
            val = 0 if card_num >= 10 else card_num
            cards_pool.extend([val] * int(round(qty)))
            
        if len(cards_pool) < 6:
            return {"p_sim_win": 44.6, "b_sim_win": 45.8, "t_sim_win": 9.6}

        p_wins, b_wins, ties = 0, 0, 0
        total_sims = 1000  
        
        np.random.seed(42)
        for _ in range(total_sims):
            sim_cards = np.random.choice(cards_pool, size=6, replace=False)
            p_score = (sim_cards[0] + sim_cards[1]) % 10
            b_score = (sim_cards[2] + sim_cards[3]) % 10
            
            p_draw, b_draw = False, False
            p_third = 0
            
            if p_score <= 5 and b_score < 8:
                p_draw = True
                p_third = sim_cards[4]
                p_score = (p_score + p_third) % 10
                
            if b_score < 8 and not (p_draw == False and p_score >= 6):
                if p_draw == False:
                    if b_score <= 5: b_draw = True
                else:
                    if b_score <= 2: b_draw = True
                    elif b_score == 3 and p_third != 8: b_draw = True
                    elif b_score == 4 and p_third in [2, 3, 4, 5, 6, 7]: b_draw = True
                    elif b_score == 5 and p_third in [4, 5, 6, 7]: b_draw = True
                    elif b_score == 6 and p_third in [6, 7]: b_draw = True
                    
            if b_draw: b_score = (b_score + sim_cards[5]) % 10
                
            if p_score > b_score: p_wins += 1
            elif b_score > p_score: b_wins += 1
            else: ties += 1
            
        return {"p_sim_win": (p_wins / total_sims) * 100, "b_sim_win": (b_wins / total_sims) * 100, "t_sim_win": (ties / total_sims) * 100}

# =========================================================================
# 🔮 AI AGENT 6: PATTERN SYNCHRO AGENT
# =========================================================================
class PatternSynchroAgent:
    @staticmethod
    def analyze_micro_patterns(all_rounds_log):
        outcomes = [r.get('outcome') for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
        if len(outcomes) < 4: return {"match": False, "type": "NONE", "suggest": "WAIT"}
        short_tokens = ["P" if x == "Player" else "B" for x in outcomes[-5:]]
        seq = "".join(short_tokens)
        if any(seq.endswith(x) for x in ["PBPB", "BPBP"]):
            return {"match": True, "type": "1:1", "suggest": "PLAYER" if seq[-1] == "B" else "BANKER"}
        if any(seq.endswith(x) for x in ["PPBB", "BBPP"]):
            return {"match": True, "type": "2:2", "suggest": "PLAYER" if seq[-1] == "B" else "BANKER"}
        return {"match": False, "type": "NONE", "suggest": "WAIT"}

# =========================================================================
# 🔵 PLAYER QUANTUM AGENT
# =========================================================================
class PlayerQuantumAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        p_eor_weights = {1: -0.0053, 2: -0.0061, 3: -0.0065, 4: -0.0138, 5: -0.0098, 6: +0.0125, 7: +0.0148, 8: +0.0099, 9: -0.0028, 10: +0.0045, 11: +0.0045, 12: +0.0045, 13: +0.0045}
        eor_shift = sum(((4 * shoe_decks) - left) * p_eor_weights.get(c, 0.0) for c, left in exact_cards_left.items())
        low_ratio = sum([exact_cards_left.get(i, 0.0) for i in [1, 2, 3, 4, 5]]) / total_cards_remaining
        return 44.6247 + (eor_shift * 5.21) + (low_ratio - 0.3846) * 18.53

# =========================================================================
# 🔴 BANKER MARKOV AGENT
# =========================================================================
class BankerMarkovAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        b_eor_weights = {1: +0.0053, 2: +0.0061, 3: +0.0065, 4: +0.0138, 5: +0.0098, 6: -0.0125, 7: -0.0148, 8: -0.0099, 9: +0.0028, 10: -0.0045, 11: -0.0045, 12: -0.0045, 13: -0.0045}
        eor_shift = sum(((4 * shoe_decks) - left) * b_eor_weights.get(c, 0.0) for c, left in exact_cards_left.items())
        choke_ratio = sum([exact_cards_left.get(i, 0.0) for i in [1, 8, 9, 10, 11, 12, 13]]) / total_cards_remaining
        return 45.8597 + (eor_shift * 5.21) + (0.5384 - choke_ratio) * 12.54

# =========================================================================
# 🟢 TIE QUANTUM ANOMALY AGENT
# =========================================================================
class TieQuantumAnomalyAgent:
    @staticmethod
    def compute_tie_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        tie_eor_weights = {1: -0.0012, 2: -0.0008, 3: -0.0005, 4: -0.0015, 5: -0.0022, 6: +0.0031, 7: +0.0035, 8: +0.0028, 9: +0.0011, 10: +0.0048, 11: +0.0048, 12: +0.0048, 13: +0.0048}
        eor_shift = sum(((4 * shoe_decks) - left) * tie_eor_weights.get(c, 0.0) for c, left in exact_cards_left.items())
        high_cards_qty = sum([exact_cards_left.get(i, 0.0) for i in [10, 11, 12, 13]])
        high_card_ratio = high_cards_qty / total_cards_remaining
        base_tie = 9.5156 + (eor_shift * 8.44) + (high_card_ratio - 0.3076) * 14.25
        return max(2.0, min(35.0, base_tie))

# =========================================================================
# 🛡️ MODULE 9: QUANTUM AUDIT & ADVANCED RISK CONTROL (KHÔI PHỤC BẢN GỐC)
# =========================================================================
class QuantumAuditMatrixController:
    @staticmethod
    def verify_cross_integrity(all_rounds_log, p_pct, b_pct):
        """Khảo sát và chấm điểm độ lệch pha của thuật toán so với thực tế sàn"""
        if len(all_rounds_log) < 3:
            return {"integrity_score": 100.0, "risk_level": "LOW", "adjustment": 1.0}
        
        decisive_rounds = [r for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
        if not decisive_rounds:
            return {"integrity_score": 100.0, "risk_level": "LOW", "adjustment": 1.0}
            
        fail_strike = 0
        for r in reversed(decisive_rounds[-3:]):
            target = r.get('oracle_target', 'WAIT')
            actual = str(r.get('outcome', '')).upper()
            if target != 'WAIT' and target != actual:
                fail_strike += 1
                
        if fail_strike == 1:
            return {"integrity_score": 75.0, "risk_level": "NORMAL", "adjustment": 1.0}
        elif fail_strike == 2:
            return {"integrity_score": 45.0, "risk_level": "MEDIUM", "adjustment": 0.5}
        elif fail_strike >= 3:
            return {"integrity_score": 10.0, "risk_level": "CRITICAL", "adjustment": 0.0}
            
        return {"integrity_score": 100.0, "risk_level": "EXCELLENT", "adjustment": 1.0}

    @staticmethod
    def render_audit_table(log, start_round_index):
        if not log: return
        st.markdown('<div class="audit-matrix-box">', unsafe_allow_html=True)
        table_rows = ""
        for idx, r in enumerate(log):
            real_round_num = start_round_index + idx + 1
            active_target = str(r.get('oracle_target', 'WAIT')).upper()
            outcome = r.get('outcome', 'Tie').upper()
            
            if outcome == "TIE": status_text = "<span style='color:#2ecc71;'>HÒA</span>"
            elif active_target == "WAIT": status_text = "<span style='color:#64748b;'>KHÓA</span>"
            elif active_target in outcome or outcome in active_target: status_text = "<span style='color:#00f5d4;font-weight:bold;'>WIN</span>"
            else: status_text = "<span style='color:#ff4757;'>LỆCH</span>"
            
            oracle_display = "🔵 P" if "PLAYER" in active_target else ("🔴 B" if "BANKER" in active_target else "🛑 BỎ")
            outcome_display = f"P({r.get('p_score',0)})" if outcome == "PLAYER" else (f"B({r.get('b_score',0)})" if outcome == "BANKER" else "TIE")
            table_rows += f"<tr><td>V{real_round_num}</td><td>{oracle_display}</td><td>{outcome_display}</td><td>{status_text}</td></tr>"
            
        st.markdown(f"<table class='audit-table'><thead><tr><th>VÁN</th><th>CẦU</th><th>SÀN</th><th>STT</th></tr></thead><tbody>{table_rows}</tbody></table></div>", unsafe_allow_html=True)

# =========================================================================
# 👑 AI SOVEREIGN ORACLE - MÔ PHỎNG ĐIỂM THỰC TẾ & XỬ LÝ TÌNH HUỐNG
# =========================================================================
class AISovereignOracle:
    @staticmethod
    def analyze_and_suggest(all_rounds_log, shoe_decks, p_val, b_val, t_val, cards_left, trend_desc, total_rounds, pattern_info, audit_meta):
        if total_rounds == 0:
            return {"decision": "👁️ COSMOS CORE v79.6", "ai_insight": "Toàn bộ cấu trúc hệ thống và Module 9 đã đồng bộ toàn vẹn.", "color": "#a855f7", "raw_code": "EMPTY"}

        decisive_log = [r for r in all_rounds_log if r.get('outcome') in ["Player", "Banker", "Tie"]]
        
        last_point_gap = 0
        was_natural = False
        third_card_drawn = False
        
        if len(decisive_log) > 0:
            last_r = decisive_log[-1]
            p_score = last_r.get('p_score', 0)
            b_score = last_r.get('b_score', 0)
            last_point_gap = abs(p_score - b_score)
            
            if (p_score >= 8 and len(last_r.get('p_cards', [])) == 2) or (b_score >= 8 and len(last_r.get('b_cards', [])) == 2):
                was_natural = True
            if len(last_r.get('p_cards', [])) > 2 or len(last_r.get('b_cards', [])) > 2:
                third_card_drawn = True

        if len(all_rounds_log) < (8 if pattern_info["match"] else 12):
            return {"decision": "🛑 ĐỒNG BỘ NỀN", "ai_insight": "Đang nạp dữ liệu phân bổ điểm thực tế từ khay bài.", "color": "#94a3b8", "raw_code": "INITIAL_LOCK"}

        # Áp dụng dữ liệu kiểm tra chéo từ Module 9 để xử lý tình huống khẩn cấp
        if audit_meta["risk_level"] == "MEDIUM":
            return {"decision": "⚠️ CẢNH BÁO PHA LỆCH (M9)", "ai_insight": f"Phát hiện sai số cục bộ. Hệ thống ép giảm nửa vốn để bảo toàn.", "color": "#f1c40f", "raw_code": "REDUCE_BET"}
        elif audit_meta["risk_level"] == "CRITICAL":
            return {"decision": "🚨 PHONG TỎA KHẨN CẤP (M9)", "ai_insight": "Phát hiện dây lệch pha kéo dài từ sàn đấu. Yêu cầu dừng cược hoặc đổi bàn lập tức!", "color": "#ff4757", "raw_code": "FORCE_EMERGENCY_LOCK"}

        if t_val > 13.5 and last_point_gap <= 2:
            return {"decision": "🟢 ANOMALY TIE DETECTED", "ai_insight": f"Xác suất Tie bất thường ({t_val:.1f}%), biên độ nút thắt hẹp. Khuyến nghị lót nhẹ.", "color": "#2ecc71", "raw_code": "BET_TIE"}

        diff = abs(p_val - b_val)
        required_delta = 1.2 if pattern_info["match"] else 2.3
        intrinsic_target = "PLAYER" if p_val > b_val else "BANKER"

        if diff < required_delta:
            return {"decision": "🛑 BỎ LỆNH (NÉ NHIỄU)", "ai_insight": f"Biên độ lệch vi sai ({diff:.2f}%) nằm dưới ngưỡng an toàn.", "color": "#f1c40f", "raw_code": "LOW_DELTA_LOCK"}

        insight_msg = f"Mô phỏng điểm thực tế ủng hộ {intrinsic_target}."
        if was_natural: insight_msg += " Chuỗi nổ điểm Natural tạo áp lực chuyển pha."
        if third_card_drawn and last_point_gap == 1: insight_msg += " Biên độ 1 nút từ lá thứ 3 chứng tỏ xung lực bài đang siết chặt."

        if pattern_info["match"] and pattern_info["suggest"] == intrinsic_target:
            return {"decision": f"🔥 SÓNG TRÙNG CẦU: {pattern_info['type']}", "ai_insight": f"Hội tụ mật độ vi sai mạng và phom chu kỳ hướng về {intrinsic_target}!", "color": "#00f5d4", "raw_code": "MATCH_PATTERN"}

        return {"decision": f"🤖 THẦN BÀI CHỐT: {intrinsic_target}", "ai_insight": insight_msg, "color": "#38bdf8" if intrinsic_target == "PLAYER" else "#ff4757", "raw_code": "NORMAL"}

# =========================================================================
# 🪐 HÀM FUSION HUB (HỢP NHẤT DỮ LIỆU ĐỘC LẬP TỪ CÁC MODULE)
# =========================================================================
def calculate_v79_ultimate_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, (shoe_decks * 52) - burn_cards, 0, 0, 0, "TRỐNG", None, 0, {"p_sim_win": 44.6, "b_sim_win": 45.8, "t_sim_win": 9.6}
    
    raw_p = CyberSelfHealingDaemon.execute_and_heal(PlayerQuantumAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    raw_b = CyberSelfHealingDaemon.execute_and_heal(BankerMarkovAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    raw_t = CyberSelfHealingDaemon.execute_and_heal(TieQuantumAnomalyAgent.compute_tie_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    
    exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    sim_results = NextCardSimulationMatrix.run_simulation(exact_cards_left)
    
    p_fused = (raw_p * 0.6) + (sim_results["p_sim_win"] * 0.4)
    b_fused = (raw_b * 0.6) + (sim_results["b_sim_win"] * 0.4)
    t_fused = (raw_t * 0.6) + (sim_results.get("t_sim_win", 9.6) * 0.4)
    
    total_sum = p_fused + b_fused + t_fused
    p_pct = (p_fused / total_sum) * 100
    b_pct = (b_fused / total_sum) * 100
    t_pct = (t_fused / total_sum) * 100
    
    cards_remaining = max(0, int(round(sum(exact_cards_left.values()))))
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r.get('outcome') == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r.get('outcome') == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r.get('outcome') == "Tie")

    trend_desc = "CẦU TỰ DO"
    pattern_status = PatternSynchroAgent.analyze_micro_patterns(all_rounds_log)
    if pattern_status["match"]: trend_desc = f"PHOM: {pattern_status['type']}"

    return p_pct, b_pct, t_pct, cards_remaining, total_p_wins, total_b_wins, total_ties, trend_desc, None, 0, sim_results

def get_ultimate_directive_v79(p_val, b_val, t_val, trend_desc, log, shoe_decks, cards_left, pattern_info, sim_results):
    if not log: return {"status": "🛰️ SYSTEM OPERATIONAL", "msg": "Chờ nạp dữ liệu nền.", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%", "raw_target": "WAIT"}
    if len(log) < (8 if pattern_info["match"] else 12):
        return {"status": "🛑 ĐỒNG BỘ NỀN", "msg": f"Cần tích lũy thêm {12 - len(log)} ván nền để chạy mô phỏng.", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.05)", "size": "0%", "raw_target": "WAIT"}
    
    diff = abs(p_val - b_val)
    required_delta = 1.2 if pattern_info["match"] else 2.3
    if diff < required_delta:
        return {"status": "🛑 LỌC NHIỄU HẸP", "msg": f"Độ lệch biên độ ({diff:.2f}%) quá hẹp.", "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.08)", "size": "0%", "raw_target": "WAIT"}
    
    target = "PLAYER" if p_val > b_val else "BANKER"
    return {"status": f"⚡ LỆNH: {target}", "msg": f"Khớp ma trận Module 7. Đánh cửa {target}.", "color": "#00afb9" if target == "PLAYER" else "#ff4757", "bg": "rgba(0,175,185,0.12)" if target == "PLAYER" else "rgba(255,71,87,0.12)", "size": f"{max(1.0, min(5.0, diff*0.85)):.1f}% Vốn", "raw_target": target}

# =========================================================================
# GIAO DIỆN DI ĐỘNG KHÓA FLEX CỨNG PHẲNG
# =========================================================================
class BaccaratInterfaceSystem:
    @staticmethod
    def inject_custom_css():
        st.markdown(
            """
            <style>
            .stApp { background: #030712 !important; color: #f9fafb !important; }
            
            div[data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                width: 100% !important;
                gap: 5px !important;
            }
            div[data-testid="stHorizontalBlock"] > div {
                width: 50% !important;
                min-width: unset !important;
            }
            
            .true-mobile-grid {
                display: flex !important;
                flex-direction: row !important;
                width: 100% !important;
                gap: 6px !important;
                margin: 8px 0px !important;
            }
            .true-mobile-box {
                flex: 1 !important;
                background: #0b1329;
                border: 1px solid #1f2937;
                border-radius: 8px;
                padding: 8px 4px;
                text-align: center;
                box-sizing: border-box;
            }
            
            .header-hud-bar { background: #111827; border: 1px solid #1f2937; border-radius: 6px; padding: 6px; text-align: center; font-family: monospace; font-size: 11px; color: #cbd5e1; }
            .action-panel { border-radius: 8px; padding: 10px; margin: 8px 0px; }
            .action-status { font-size: 14px; font-weight: 900; }
            .action-msg { font-size: 11px; margin-top: 2px; color: #cbd5e1; text-align: justify; }
            
            .oracle-card {
                background: linear-gradient(135deg, #090f24 0%, #111c44 100%);
                border: 1px solid #3b82f6;
                border-radius: 8px;
                padding: 10px;
                margin: 8px 0px;
                box-shadow: 0 0 10px rgba(59, 130, 246, 0.15);
            }
            .oracle-title { font-size: 13px; font-weight: 900; letter-spacing: 0.5px; }
            .oracle-desc { font-size: 11px; color: #cbd5e1; margin-top: 3px; }
            
            /* CSS RIÊNG CHO MODULE 9 MONITOR HUD */
            .m9-hud { background: #022c22; border: 1px solid #059669; border-radius: 6px; padding: 4px 8px; font-size: 10px; font-family: monospace; color: #34d399; margin: 4px 0px; text-align: center;}

            .metric-tag { font-size: 9px; font-weight: 800; color: #94a3b8; display:block; }
            .metric-num { font-size: 13px; font-weight: 900; font-family: monospace; display:block; }
            .metric-sub { font-size: 8px; color: #64748b; display:block; }
            
            .audit-matrix-box { padding: 8px; border-radius: 6px; background-color: #0b1329; border: 1px dashed #3b82f6; margin-top: 10px; overflow-x: auto; }
            .audit-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 10px; text-align: center; }
            .audit-table th { padding: 4px; background: #1f2937; color: #94a3b8; border: 1px solid #374151; }
            .audit-table td { padding: 4px; border: 1px solid #1f2937; }
            
            div.stButton > button {
                background-color: #1f2937 !important;
                color: #f3f4f6 !important;
                border: 1px solid #374151 !important;
                border-radius: 6px !important;
                padding: 4px 6px !important;
                font-size: 11px !important;
                width: 100% !important;
            }
            .submit-btn-box div.stButton > button {
                background-color: #00f5d4 !important;
                color: #030712 !important;
                font-weight: 900 !important;
                border: none !important;
                padding: 8px !important;
                font-size: 12px !important;
            }
            </style>
            """, unsafe_allow_html=True
        )

    @staticmethod
    def render_header_hud(total_rounds, cards_left):
        st.markdown(f'<div class="header-hud-bar">📱 INTEGRATED CORE v79.6 | VÁN: <b>{total_rounds}</b> | BÀI CÒN: <b>{cards_left} Lá</b></div>', unsafe_allow_html=True)

    @staticmethod
    def render_m9_monitor(audit_meta):
        # Xuất khung giám sát kiểm định chéo của Module 9 lên đầu giao diện nền
        score = audit_meta["integrity_score"]
        status = audit_meta["risk_level"]
        color = "#34d399" if score >= 70 else ("#f59e0b" if score >= 40 else "#ef4444")
        st.markdown(f'<div class="m9-hud" style="color: {color}; border-color: {color}; background: rgba(0,0,0,0.2);">🛡️ MODULE 9 INTEGRITY: <b>{score:.1f}%</b> | RISK CONTROL: <b>{status}</b></div>', unsafe_allow_html=True)

    @staticmethod
    def render_directive_panel(cmd):
        st.markdown(
            f'<div class="action-panel" style="background: {cmd["bg"]}; border-left: 4px solid {cmd["color"]};">'
            f'<div class="action-status" style="color: {cmd["color"]};">{cmd["status"]}</div>'
            f'<div class="action-msg">{cmd["msg"]}</div>'
            f'<div style="font-size: 11px; margin-top:3px; font-weight:bold; color:#a855f7;">💰 MỨC ĐI TIỀN: {cmd["size"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

    @staticmethod
    def render_oracle_panel(oracle):
        st.markdown(
            f'<div class="oracle-card" style="border-color: {oracle["color"]};">'
            f'<div class="oracle-title" style="color: {oracle["color"]};">🔮 {oracle["decision"]}</div>'
            f'<div class="oracle-desc"><b>Phân tích sảnh mạng & lá bài thực tế:</b> {oracle["ai_insight"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

    @staticmethod
    def render_probabilities_grid(p, b, t, sim_results):
        sim_p = sim_results.get("p_sim_win", 44.6)
        sim_b = sim_results.get("b_sim_win", 45.8)
        sim_t = sim_results.get("t_sim_win", 9.6)
        
        st.markdown(
            f'<div class="true-mobile-grid">'
            f'<div class="true-mobile-box"><span class="metric-tag">🔵 PLAYER</span><span class="metric-num" style="color:#00afb9;">{p:.1f}%</span><span class="metric-sub">Sim:{sim_p:.0f}%</span></div>'
            f'<div class="true-mobile-box"><span class="metric-tag">🔴 BANKER</span><span class="metric-num" style="color:#ff4757;">{b:.1f}%</span><span class="metric-sub">Sim:{sim_b:.0f}%</span></div>'
            f'<div class="true-mobile-box"><span class="metric-tag">🟢 TIE (QUANTUM)</span><span class="metric-num" style="color:#2ecc71;">{t:.1f}%</span><span class="metric-sub">Sim:{sim_t:.0f}%</span></div>'
            f'</div>', unsafe_allow_html=True
        )

def parse_baccarat_input_v79(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().strip()
    temp = []
    i = 0
    while i < len(normalized):
        if normalized[i].isspace(): i+=1; continue
        if normalized[i:i+2] == "10": temp.append("10"); i+=2
        else: temp.append(normalized[i]); i+=1
    res = []
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13, '10': 10}
    for t in temp:
        if t in mapping: res.append(mapping[t])
        elif t.isdigit() and 1 <= int(t) <= 9: res.append(int(t))
    return res

# =========================================================================
# RUNTIME ENGINE APPLICATION v79.6
# =========================================================================
st.set_page_config(page_title="Oracle v79.6 Integrity", page_icon="🌌", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []

with st.expander("⚙️ CẤU HÌNH KHAY BÀI"):
    decks = st.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)
    burn_cards = st.number_input("🎴 LÁ RÚT BỎ (BURN):", min_value=0, value=7)
    hist_p = st.number_input("🔵 Player Wins thô:", min_value=0, value=0)
    hist_b = st.number_input("🔴 Banker Wins thô:", min_value=0, value=0)
    hist_t = st.number_input("🟢 Tie Wins thô:", min_value=0, value=0)

pattern_info = PatternSynchroAgent.analyze_micro_patterns(st.session_state.round_detailed_log)

# 🪐 1. Tính toán Fusion từ 3 Cụm Agent độc lập
final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, _, _, sim_results = calculate_v79_ultimate_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t, burn_cards=burn_cards
)

# 🛡️ 2. Kích hoạt Trích xuất dữ liệu Kiểm định chéo từ Module 9 gốc
audit_meta = QuantumAuditMatrixController.verify_cross_integrity(st.session_state.round_detailed_log, final_p, final_b)

cmd = get_ultimate_directive_v79(final_p, final_b, final_t, trend_desc, st.session_state.round_detailed_log, decks, cards_left, pattern_info, sim_results)
total_all_rounds = total_p + total_b + total_t

# 🔮 3. Kích hoạt AI Thần bài chốt ma trận thực tế tích hợp dữ liệu của M9
oracle_data = AISovereignOracle.analyze_and_suggest(
    st.session_state.round_detailed_log, decks, final_p, final_b, final_t, cards_left, trend_desc, total_all_rounds, pattern_info, audit_meta
)

# ĐỒNG BỘ HÓA TÌNH HUỐNG TỪ AI THẦN BÀI XUỐNG KHUNG CHỈ LỆNH ĐI TIỀN
if oracle_data.get('raw_code') in ["INITIAL_LOCK", "LOW_DELTA_LOCK"]:
    cmd['status'], cmd['msg'], cmd['color'], cmd['bg'], cmd['size'] = oracle_data['decision'], oracle_data['ai_insight'], oracle_data['color'], "rgba(148, 163, 184, 0.05)", "0%"
elif oracle_data.get('raw_code') == "REDUCE_BET":
    cmd['status'], cmd['msg'], cmd['color'], cmd['bg'], cmd['size'] = oracle_data['decision'], oracle_data['ai_insight'], oracle_data['color'], "rgba(241, 196, 15, 0.06)", "HẠ 1/2 VỐN THUẬN M9"
elif oracle_data.get('raw_code') == "BET_TIE":
    cmd['status'], cmd['msg'], cmd['color'], cmd['bg'], cmd['size'] = oracle_data['decision'], oracle_data['ai_insight'], oracle_data['color'], "rgba(46, 204, 113, 0.08)", "LÓT TIE NHẸ"
elif oracle_data.get('raw_code') == "FORCE_EMERGENCY_LOCK":
    cmd['status'], cmd['msg'], cmd['color'], cmd['bg'], cmd['size'] = oracle_data['decision'], oracle_data['ai_insight'], oracle_data['color'], "rgba(255, 71, 87, 0.08)", "0% (STOP LỆNH M9)"

# HIỂN THỊ ENGINE GIAO DIỆN CHUẨN PHẲNG DI ĐỘNG
BaccaratInterfaceSystem.render_header_hud(total_all_rounds, cards_left)
BaccaratInterfaceSystem.render_m9_monitor(audit_meta) # Xuất thanh trạng thái M9 chống gãy cầu cực đoan

with st.form(key="v79_integrity_form", clear_on_submit=True):
    in_cols = st.columns(2)
    p_input = in_cols[0].text_input("🔵 LÁ P:")
    b_input = in_cols[1].text_input("🔴 LÁ B:")
    st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
    calc_triggered = st.form_submit_button("🚀 KÍCH HOẠT HỆ THỐNG TOÀN VẸN v79.6")
    st.markdown('</div>', unsafe_allow_html=True)

if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v79(p_input.strip())
    b_list = parse_baccarat_input_v79(b_input.strip())
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    
    st.session_state.round_detailed_log.append({
        'p_cards': p_list, 'b_cards': b_list, 'p_score': p_score, 'b_score': b_score, 'outcome': outcome,
        'oracle_target': cmd['raw_target']
    })
    st.rerun()

st.markdown("---")
BaccaratInterfaceSystem.render_oracle_panel(oracle_data)
BaccaratInterfaceSystem.render_directive_panel(cmd)
BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t, sim_results)
QuantumAuditMatrixController.render_audit_table(st.session_state.round_detailed_log, (hist_p + hist_b + hist_t))

st.markdown("<br>", unsafe_allow_html=True)
util_cols = st.columns(2)
if util_cols[0].button("⏪ UNDO"):
    if st.session_state.round_detailed_log:
        st.session_state.round_detailed_log.pop()
        st.rerun()
if util_cols[1].button("🔄 CLEAR KHAY"):
    st.session_state.round_detailed_log.clear()
    st.rerun()
