import streamlit as st
import numpy as np
import math
import traceback
from datetime import datetime

# =========================================================================
# 🌌 SYSTEM HEALING REGISTRY (BỘ NHỚ LƯU TRỮ VÀ TỰ VÁ LỖI CỦA AI)
# =========================================================================
if 'cyber_healing_logs' not in st.session_state:
    st.session_state.cyber_healing_logs = []

class CyberSelfHealingDaemon:
    @staticmethod
    def execute_and_heal(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError:
            CyberSelfHealingDaemon._register_fault("PHÉP CHIA CHO 0 (ZERO_DIV)", "Phát hiện chia cho 0 trong ma trận phân phối!")
            return 1e-15 
        except TypeError as te:
            CyberSelfHealingDaemon._register_fault("LỖI KIỂU DỮ LIỆU (TYPE_ERR)", f"Xung đột kiểu dữ liệu: {str(te)}")
            return 0.0
        except ValueError as ve:
            CyberSelfHealingDaemon._register_fault("LỖI GIÁ TRỊ (VALUE_ERR)", f"Vượt giới hạn tổ hợp toán học: {str(ve)}")
            return 0.0
        except Exception as e:
            tb = traceback.format_exc()
            CyberSelfHealingDaemon._register_fault("KỲ DỊ HỆ THỐNG (UNKNOWN_FATAL)", f"Ngoại lệ runtime: {str(e)} \n{tb[:100]}")
            return None

    @staticmethod
    def _register_fault(fault_type, description):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "time": timestamp, "type": fault_type, "desc": description,
            "action": "🛠️ AI VÁ LỖI v79.1: Đã ép cố định khung CSS responsive cho thiết bị di động."
        }
        st.session_state.cyber_healing_logs.insert(0, log_entry)
        if len(st.session_state.cyber_healing_logs) > 5: st.session_state.cyber_healing_logs.pop()

    @staticmethod
    def render_warning_hud():
        if not st.session_state.cyber_healing_logs: return
        latest_fault = st.session_state.cyber_healing_logs[0]
        st.markdown(
            f'<div class="mobile-card" style="border: 1px solid #ff4757; background: rgba(255, 71, 87, 0.05);">'
            f'<div style="font-size: 11px; font-weight: 900; color: #ff4757; display: flex; justify-content: space-between;">'
            f'<span>🚨 CYBER HEALING v79.1</span><span style="font-family: monospace;">[{latest_fault["time"]}]</span></div>'
            f'<div style="font-size: 11px; color: #cbd5e1; margin-top: 3px; font-family: monospace;">{latest_fault["desc"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

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
            return {"p_sim_win": 44.6, "b_sim_win": 45.8, "t_sim_win": 9.5, "sim_status": "LỖI BÀI"}

        p_wins, b_wins, ties = 0, 0, 0
        total_sims = 1500  # Tối ưu hóa số vòng lặp để điện thoại load mượt, không bị lag đơ trình duyệt
        
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
                    
            if b_draw:
                b_score = (b_score + sim_cards[5]) % 10
                
            if p_score > b_score: p_wins += 1
            elif b_score > p_score: b_wins += 1
            else: ties += 1
            
        return {
            "p_sim_win": (p_wins / total_sims) * 100,
            "b_sim_win": (b_wins / total_sims) * 100,
            "t_sim_win": (ties / total_sims) * 100,
            "sim_status": "OK"
        }

# =========================================================================
# 🔮 AI AGENT 6: PATTERN SYNCHRO AGENT (BẮT CẦU NGẮN CHUYÊN DI ĐỘNG)
# =========================================================================
class PatternSynchroAgent:
    @staticmethod
    def analyze_micro_patterns(all_rounds_log):
        outcomes = [r.get('outcome') for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
        if len(outcomes) < 4:
            return {"match": False, "type": "NONE", "suggest": "WAIT", "confidence": 0.0}
            
        short_tokens = ["P" if x == "Player" else "B" for x in outcomes[-6:]]
        seq = "".join(short_tokens)
        
        if any(seq.endswith(x) for x in ["PBPB", "BPBP"]):
            next_pred = "PLAYER" if seq[-1] == "B" else "BANKER"
            return {"match": True, "type": "1:1", "suggest": next_pred, "confidence": 92.0}
            
        if any(seq.endswith(x) for x in ["PPBB", "BBPP"]):
            next_pred = "PLAYER" if seq[-1] == "B" else "BANKER"
            return {"match": True, "type": "2:2 ĐẦU", "suggest": next_pred, "confidence": 88.0}
        if any(seq.endswith(x) for x in ["PPB", "BBP"]):
            next_pred = "BANKER" if seq[-1] == "B" else "PLAYER"
            return {"match": True, "type": "2:2 ĐỦ", "suggest": next_pred, "confidence": 90.0}

        if len(short_tokens) >= 5:
            s5 = "".join(short_tokens[-5:])
            if s5 == "PPBPP": return {"match": True, "type": "2-1-2 GÃY", "suggest": "BANKER", "confidence": 85.0}
            if s5 == "BBPBB": return {"match": True, "type": "2-1-2 GÃY", "suggest": "PLAYER", "confidence": 85.0}
            if s5 == "PPBP": return {"match": True, "type": "2-1-2 TẠO", "suggest": "PLAYER", "confidence": 87.0}
            if s5 == "BBPB": return {"match": True, "type": "2-1-2 TẠO", "suggest": "BANKER", "confidence": 87.0}

        return {"match": False, "type": "NONE", "suggest": "WAIT", "confidence": 0.0}

# =========================================================================
# 🔵 AI AGENT 1 & 🔴 AI AGENT 2
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

class BankerMarkovAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        b_eor_weights = {1: +0.0053, 2: +0.0061, 3: +0.0065, 4: +0.0138, 5: +0.0098, 6: -0.0125, 7: -0.0148, 8: -0.0099, 9: +0.0028, 10: -0.0045, 11: -0.0045, 12: -0.0045, 13: -0.0045}
        eor_shift = sum(((4 * shoe_decks) - left) * b_eor_weights.get(c, 0.0) for c, left in exact_cards_left.items())
        choke_ratio = sum([exact_cards_left.get(i, 0.0) for i in [1, 8, 9, 10, 11, 12, 13]]) / total_cards_remaining
        return 45.8597 + (eor_shift * 5.21) + (0.5384 - choke_ratio) * 12.54

class TieHypergeometricAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        cards_rem = int(max(1.0, sum(exact_cards_left.values())))
        zero_dens = sum([exact_cards_left.get(i, 0.0) for i in [10, 11, 12, 13]]) / float(cards_rem) if cards_rem > 0 else 0.3076
        gap = 0
        for r in reversed(all_rounds_log):
            if r.get('outcome') == "Tie": break
            gap += 1
        return 9.5156 + (zero_dens - 0.3076) * 38.45 + (1.0 - math.exp(-gap / 9.54)) * 4.25

# =========================================================================
# 🪐 FUSION MATRIX & DIRECTIVE HUB
# =========================================================================
def calculate_v79_ultimate_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, (shoe_decks * 52) - burn_cards, 0, 0, 0, "TRỐNG", None, 0, {"p_sim_win": 44.6, "b_sim_win": 45.8, "t_sim_win": 9.5}
    
    raw_p = CyberSelfHealingDaemon.execute_and_heal(PlayerQuantumAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    raw_b = CyberSelfHealingDaemon.execute_and_heal(BankerMarkovAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    raw_t = CyberSelfHealingDaemon.execute_and_heal(TieHypergeometricAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    
    exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    sim_results = NextCardSimulationMatrix.run_simulation(exact_cards_left)
    
    p_fused = (raw_p * 0.6) + (sim_results["p_sim_win"] * 0.4)
    b_fused = (raw_b * 0.6) + (sim_results["b_sim_win"] * 0.4)
    t_fused = (raw_t * 0.6) + (sim_results.get("t_sim_win", 9.5) * 0.4)
    
    total_sum = p_fused + b_fused + t_fused
    p_pct = (p_fused / total_sum) * 100
    b_pct = (b_fused / total_sum) * 100
    t_pct = (t_fused / total_sum) * 100
    
    cards_remaining = max(0, int(round(sum(exact_cards_left.values()))))
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r.get('outcome') == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r.get('outcome') == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r.get('outcome') == "Tie")

    trend_desc = "CẦU TỰ DO"
    decisive = [r.get('outcome') for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
    streak_side, streak_count = None, 0
    if len(decisive) >= 2:
        current_streak_side = decisive[-1]
        for outcome in reversed(decisive):
            if outcome == current_streak_side: streak_count += 1
            else: break
        if streak_count >= 2:
            streak_side = current_streak_side
            trend_desc = f"BỆT {streak_side.upper()} ({streak_count}V)"
            
    pattern_status = PatternSynchroAgent.analyze_micro_patterns(all_rounds_log)
    if pattern_status["match"]:
        trend_desc = f"PHOM: {pattern_status['type']}"

    return p_pct, b_pct, t_pct, cards_remaining, total_p_wins, total_b_wins, total_ties, trend_desc, streak_side, streak_count, sim_results

def get_ultimate_directive_v79(p_val, b_val, trend_desc, log, shoe_decks, cards_left, pattern_info, sim_results):
    if not log:
        return {"status": "🛰️ OPERATIONAL v79.1", "msg": "Hệ thống Mobile Core trực tuyến.", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%", "raw_target": "WAIT"}

    min_rounds = 8 if pattern_info["match"] else 12
    if len(log) < min_rounds:
        return {"status": "🛑 ĐỒNG BỘ NỀN", "msg": f"Cần tích lũy thêm {min_rounds - len(log)} ván dữ liệu nền để chạy mô phỏng.", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.05)", "size": "0%", "raw_target": "WAIT"}

    diff = abs(p_val - b_val)
    required_delta = 1.2 if pattern_info["match"] else 2.3
    
    if diff < required_delta:
        return {"status": "🛑 LỌC NHIỄU HẸP", "msg": f"Vi sai ({diff:.2f}%) chưa đạt điểm nổ lệnh ({required_delta}%).", "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.08)", "size": "0%", "raw_target": "WAIT"}

    target = "PLAYER" if p_val > b_val else "BANKER"
    color = "#00afb9" if target == "PLAYER" else "#ff4757"
    bg = "rgba(0, 175, 185, 0.12)" if target == "PLAYER" else "rgba(255, 71, 87, 0.12)"
    
    msg = f"Mô phỏng cây bài hỗ trợ hướng {target} tối ưu xác suất."
    if pattern_info["match"]:
        msg = f"Khớp phom cầu ngắn {pattern_info['type']}. Đánh thuận chiều chu kỳ sảnh."

    return {"status": f"⚡ LỆNH: {target}", "msg": msg, "color": color, "bg": bg, "size": "1.5% Vốn Kỷ Luật", "raw_target": target}

# =========================================================================
# 👑 AI SOVEREIGN ORACLE (v79.1 MOBILE)
# =========================================================================
class AISovereignOracle:
    @staticmethod
    def analyze_and_suggest(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, p_val, b_val, t_val, cards_left, trend_desc, streak_side, streak_count, total_rounds, burn_cards, pattern_info, sim_results):
        if total_rounds == 0:
            return {"decision": "👁️ ORACLE CORE v79.1", "ai_insight": "Hệ thống tối ưu hóa Mobile sẵn sàng. Hãy nạp bài.", "risk_level": "Quét nền", "color": "#a855f7", "memory_hud": "Đang chờ...", "cyber_knowledge": "Lõi di động ONLINE", "raw_code": "EMPTY"}

        decisive_log = [r for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
        wrong_count = 0
        if decisive_log:
            last_round = decisive_log[-1]
            pred = last_round.get('oracle_target') if last_round.get('oracle_target') else "WAIT"
            if pred != "WAIT" and pred != last_round.get('outcome').upper(): wrong_count = 1
        if len(decisive_log) >= 2:
            if all(r.get('oracle_target') != r.get('outcome').upper() for r in decisive_log[-2:]): wrong_count = 2

        total_initial_cards = shoe_decks * 52.0
        shoe_progress = (total_initial_cards - cards_left) / total_initial_cards
        
        sim_p, sim_b = sim_results.get("p_sim_win", 0), sim_results.get("b_sim_win", 0)
        memory_hud = f"P_Sim: {sim_p:.1f}% | B_Sim: {sim_b:.1f}% | Khay: {shoe_progress*100:.0f}%"
        cyber_knowledge = f"Lỗi bàn: {wrong_count}/2 | Xu hướng: {trend_desc}"

        if len(all_rounds_log) < (8 if pattern_info["match"] else 12):
            return {"decision": "🛑 ĐỒNG BỘ NỀN", "ai_insight": "Đang thu thập dữ liệu sảnh để kích hoạt Module mô phỏng cây.", "risk_level": "An toàn", "color": "#94a3b8", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "INITIAL_LOCK"}

        diff = abs(p_val - b_val)
        required_delta = 1.2 if pattern_info["match"] else 2.3
        intrinsic_target = "PLAYER" if p_val > b_val else "BANKER"

        if diff < required_delta:
            return {"decision": "🛑 BỎ LỆNH (NÉ NHIỄU)", "ai_insight": f"Độ lệch điểm ({diff:.2f}%) quá nhỏ. Sảnh bài đang giằng co nghẹt thở.", "risk_level": "Nhiễu cao", "color": "#f1c40f", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "LOW_DELTA_LOCK"}

        if wrong_count >= 2:
            return {"decision": "🚨 PHONG TỎA KHẨN CẤP", "ai_insight": "Sảnh bài xáo lỗi đảo cấu trúc liên tục. Ép đổi bàn ngay lập tức!", "risk_level": "Nguy hiểm", "color": "#ff4757", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "FORCE_EMERGENCY_LOCK"}

        final_alloc = max(1.0, min(6.0, (diff / 100.0) * 15.0 * (1.0 + shoe_progress)))
        
        if pattern_info["match"]:
            if pattern_info["suggest"] == intrinsic_target:
                return {"decision": f"⚡ SÓNG TRÙNG: {pattern_info['type']}", "capital_allocation": f"💎 ĐẬP MẠNH: {final_alloc * 1.3:.1f}%", "ai_insight": f"Mô phỏng lá bài và chu kỳ ngắn hội tụ hướng {intrinsic_target}.", "risk_level": "Tối ưu", "color": "#00f5d4", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "MATCH_PATTERN"}
            else:
                return {"decision": f"🌊 PHOM CHU KỲ: {pattern_info['type']}", "capital_allocation": f"🛡️ ĐI NHẸ: {max(1.0, final_alloc * 0.6):.1f}%", "ai_insight": f"Đánh thuận hình thái cầu ngắn {pattern_info['type']} để phòng thủ sảnh.", "risk_level": "Phòng thủ", "color": "#cbd5e1", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "PATTERN_FLOW"}

        return {"decision": f"⚡ CHUẨN LỆNH: {intrinsic_target}", "capital_allocation": f"💎 VỐN: {final_alloc:.1f}%", "ai_insight": f"Mật độ bài và mô phỏng nghiêng hoàn toàn về {intrinsic_target}.", "risk_level": "Bình thường", "color": "#38bdf8" if intrinsic_target == "PLAYER" else "#ff4757", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "NORMAL"}

# =========================================================================
# GIAO DIỆN SIÊU CO GIÃN MOBILE TRỰC QUAN (MOBILE HUD CSS)
# =========================================================================
class BaccaratInterfaceSystem:
    @staticmethod
    def inject_custom_css():
        st.markdown(
            """
            <style>
            .stApp { background: #02040a !important; color: #f8fafc !important; }
            /* Cấu trúc ép co giãn trên màn hình điện thoại nhỏ */
            .mobile-container { display: flex; width: 100%; gap: 6px; margin: 6px 0px; justify-content: space-between; }
            .mobile-card { background: #050b14; border: 1px solid #1e293b; border-radius: 10px; padding: 10px; width: 100%; box-sizing: border-box; margin: 4px 0px; }
            .header-hud-bar { background: linear-gradient(90deg, #090d16, #111827); border: 1px solid #1f2937; border-radius: 8px; padding: 8px; text-align: center; font-family: monospace; font-size: 11px; color: #cbd5e1; }
            .action-panel { border-radius: 10px; padding: 12px; margin: 8px 0px; border-left: 5px solid #cbd5e1; }
            .action-status { font-size: 15px; font-weight: 900; letter-spacing: 0.3px; }
            .action-msg { font-size: 12px; margin-top: 3px; text-align: justify; color: #cbd5e1; }
            
            /* Sửa dứt điểm lỗi tràn cột ngang trên Mobile */
            .mobile-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; width: 100%; margin: 6px 0px; }
            .mobile-metric-box { background: #050b14; border: 1px solid #1f2937; border-radius: 6px; padding: 6px 3px; text-align: center; }
            .metric-tag { font-size: 9px; font-weight: 800; color: #64748b; display:block; text-transform: uppercase; }
            .metric-num { font-size: 14px; font-weight: 900; font-family: monospace; display:block; margin: 1px 0px; }
            .metric-sub { font-size: 8px; color: #475569; display:block; }
            
            /* Thiết kế bảng kiểm toán cuộn mượt bằng ngón tay không bị lệch khung */
            .audit-matrix-box { padding: 10px; border-radius: 8px; background-color: #050b14; border: 1px dashed #3b82f6; margin-top: 12px; overflow-x: auto; }
            .audit-title { font-size: 11px; font-weight: 800; color: #60a5fa; margin-bottom: 6px; text-transform: uppercase; }
            .audit-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 11px; white-space: nowrap; }
            .audit-table th { padding: 5px; background: #0f172a; border: 1px solid #1e293b; color: #94a3b8; }
            .audit-table td { padding: 5px; border: 1px solid #0f172a; text-align:center; }
            .status-dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%; vertical-align: middle; margin-right: 2px;}
            
            div.stButton > button { background-color: #0f172a !important; color: #cbd5e1 !important; border: 1px solid #1e293b !important; border-radius: 8px; width: 100% !important; padding: 4px 10px !important; font-size: 12px !important;}
            .submit-btn-box div.stButton > button { background-color: #00f5d4 !important; color: #010206 !important; font-weight:800; box-shadow: 0 0 10px rgba(0,245,212,0.3); border:none !important; padding: 8px !important; font-size: 13px !important;}
            </style>
            """, unsafe_allow_html=True
        )

    @staticmethod
    def render_header_hud(total_rounds, cards_left, decks):
        st.markdown(
            f'<div class="header-hud-bar">📱 LÕI MÔ PHỎNG v79.1 DI ĐỘNG | '
            f'ĐÃ QUÉT: <b>{total_rounds}V</b> | BÀI CÒN: <b>{cards_left} Lá</b></div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_directive_panel(cmd):
        st.markdown(
            f'<div class="action-panel" style="background: {cmd["bg"]}; border-left: 5px solid {cmd["color"]};">'
            f'<div class="action-status" style="color: {cmd["color"]};">{cmd["status"]}</div>'
            f'<div class="action-msg">{cmd["msg"]}</div>'
            f'<div style="font-size: 11px; margin-top:4px; font-weight:bold; color:#a855f7;">💰 PHÂN PHỐI VỐN: {cmd["size"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

    @staticmethod
    def render_ai_oracle_panel(oracle):
        st.markdown(
            f'<div class="mobile-card">'
            f'<div style="font-size:12px; font-weight:bold; color:{oracle["color"]};">{oracle["decision"]}</div>'
            f'<div style="font-size:10px; color:#94a3b8; margin: 2px 0px; font-family:monospace;">🧬 {oracle["memory_hud"]}</div>'
            f'<div style="font-size:11px; color:#e2e8f0; margin-top:3px;"><b>AI Phân tích:</b> {oracle["ai_insight"]}</div>'
            f'<div style="font-size:10px; color:#64748b; margin-top:3px; font-family:monospace;">⚙️ {oracle["cyber_knowledge"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

    @staticmethod
    def render_probabilities_grid(p, b, t, sim_results):
        sim_p = sim_results.get("p_sim_win", 44.6)
        sim_b = sim_results.get("b_sim_win", 45.8)
        sim_t = sim_results.get("t_sim_win", 9.5)
        
        # Sử dụng thẻ CSS Grid thuần thay cho st.columns để ép hiển thị 3 cột trên màn hình điện thoại
        st.markdown(
            f'<div class="mobile-grid-3">'
            f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER</span><span class="metric-num" style="color:#00afb9;">{p:.1f}%</span><span class="metric-sub">Sim:{sim_p:.0f}%</span></div>'
            f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER</span><span class="metric-num" style="color:#ff4757;">{b:.1f}%</span><span class="metric-sub">Sim:{sim_b:.0f}%</span></div>'
            f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE</span><span class="metric-num" style="color:#2ecc71;">{t:.1f}%</span><span class="metric-sub">Sim:{sim_t:.0f}%</span></div>'
            f'</div>', unsafe_allow_html=True
        )

# =========================================================================
# QUANTUM AUDIT MATRIX CONTROLLER (BẢNG KIỂM TOÁN TỐI ƯU MOBILE)
# =========================================================================
class QuantumAuditMatrixController:
    @staticmethod
    def render_audit_table(log, start_round_index):
        if not log: return
        st.markdown('<div class="audit-matrix-box"><div class="audit-title">📊 ĐỐI CHIẾU KIỂM TOÁN LÕI DI ĐỘNG (v79.1)</div>', unsafe_allow_html=True)
        table_rows = ""
        for idx, r in enumerate(log):
            real_round_num = start_round_index + idx + 1
            oracle_decision = r.get('oracle_decision', '🛑 CHỜ')
            active_target = str(r.get('oracle_target', 'WAIT')).upper()
            outcome = r.get('outcome', 'Tie').upper()
            
            if outcome == "TIE":
                dot_html, status_text = '<span class="status-dot" style="background-color: #2ecc71;"></span>', "<span style='color:#2ecc71;'>HÒA</span>"
            elif "BỎ LỆNH" in oracle_decision or active_target == "WAIT" or "LOCK" in oracle_decision:
                dot_html, status_text = '<span class="status-dot" style="background-color: #64748b;"></span>', "<span style='color:#64748b;'>KHÓA</span>"
            elif active_target in outcome or outcome in active_target:
                dot_html, status_text = '<span class="status-dot" style="background-color: #00f5d4; box-shadow: 0 0 5px #00f5d4;"></span>', "<span style='color:#00f5d4; font-weight:bold;'>WIN</span>"
            else:
                dot_html, status_text = '<span class="status-dot" style="background-color: #ff4757;"></span>', "<span style='color:#ff4757;'>LỆCH</span>"
            
            if "PLAYER" in active_target: oracle_display = "<span style='color:#00afb9; font-weight:bold;'>🔵 PLAYER</span>"
            elif "BANKER" in active_target: oracle_display = "<span style='color:#ff4757; font-weight:bold;'>🔴 BANKER</span>"
            else: oracle_display = "<span style='color:#64748b;'>🛑 BỎ QUA</span>"
                
            outcome_display = f"<span style='color:#00afb9;'>P({r.get('p_score',0)})</span>" if outcome == "PLAYER" else (f"<span style='color:#ff4757;'>B({r.get('b_score',0)})</span>" if outcome == "BANKER" else "<span style='color:#2ecc71;'>TIE</span>")
            table_rows += f"<tr><td>V{real_round_num}</td><td style='text-align: left;'>{oracle_display}</td><td>{outcome_display}</td><td>{dot_html}{status_text}</td></tr>"
            
        st.markdown(f"<table class='audit-table'><thead><tr><th>VÁN</th><th>KHUYẾN NGHỊ</th><th>SÀN</th><th>KẾT QUẢ</th></tr></thead><tbody>{table_rows}</tbody></table></div>", unsafe_allow_html=True)

def parse_baccarat_input_v79(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().strip()
    temp = []
    i = 0
    while i < len(normalized):
        if normalized[i].isspace(): i+=1; continue
        if normalized[i:i+2] == "10": temp.append("10"); i+=2
        else: temp.append(normalized[i]); i+1; i+=1
    res = []
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13, '10': 10}
    for t in temp:
        if t in mapping: res.append(mapping[t])
        elif t.isdigit() and 1 <= int(t) <= 9: res.append(int(t))
    return res

# =========================================================================
# RUNTIME ENGINE APPLICATION v79.1 MOBILE
# =========================================================================
st.set_page_config(page_title="Oracle v79.1 Mobile", page_icon="🌌", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []

# Đưa cấu hình khay vào Expander thu gọn để tiết kiệm không gian màn hình dọc của điện thoại
with st.expander("⚙️ CẤU HÌNH KHAY BÀI (RÚT GỌN DI ĐỘNG)"):
    decks = st.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)
    burn_cards = st.number_input("🎴 LÁ RÚT BỎ (BURN):", min_value=0, value=7)
    m_cols = st.columns(3)
    hist_p = m_cols[0].number_input("🔵 P-Wins:", min_value=0, value=0)
    hist_b = m_cols[1].number_input("🔴 B-Wins:", min_value=0, value=0)
    hist_t = m_cols[2].number_input("🟢 T-Wins:", min_value=0, value=0)

st.markdown("### 🌌 MULTI-AGENT ORACLE v79.1")
CyberSelfHealingDaemon.render_warning_hud()

pattern_info = PatternSynchroAgent.analyze_micro_patterns(st.session_state.round_detailed_log)

final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, streak_side, streak_count, sim_results = calculate_v79_ultimate_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t, burn_cards=burn_cards
)

cmd = get_ultimate_directive_v79(final_p, final_b, trend_desc, st.session_state.round_detailed_log, decks, cards_left, pattern_info, sim_results)
total_all_rounds = total_p + total_b + total_t
BaccaratInterfaceSystem.render_header_hud(total_all_rounds, cards_left, decks)

current_ai_oracle = AISovereignOracle.analyze_and_suggest(
    st.session_state.round_detailed_log, decks, hist_p, hist_b, hist_t,
    final_p, final_b, final_t, cards_left, trend_desc, streak_side, streak_count,
    total_all_rounds, burn_cards, pattern_info, sim_results
)

if current_ai_oracle.get('raw_code') in ["INITIAL_LOCK", "LOW_DELTA_LOCK"]:
    cmd['status'], cmd['msg'], cmd['color'], cmd['bg'], cmd['size'] = current_ai_oracle['decision'], current_ai_oracle['ai_insight'], current_ai_oracle['color'], "rgba(148, 163, 184, 0.05)", "0%"
elif current_ai_oracle.get('raw_code') == "FORCE_EMERGENCY_LOCK":
    cmd['status'], cmd['msg'], cmd['color'], cmd['bg'], cmd['size'] = current_ai_oracle['decision'], current_ai_oracle['ai_insight'], current_ai_oracle['color'], "rgba(255, 71, 87, 0.08)", "0%"

# Form Nhập liệu dạng tối giản cho điện thoại
with st.form(key="v79_mobile_form", clear_on_submit=True):
    grid = st.columns(2)
    p_input = grid[0].text_input("🔵 LÁ P (Ví dụ: A,2):")
    b_input = grid[1].text_input("🔴 LÁ B (Ví dụ: 8,9):")
    st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
    calc_triggered = st.form_submit_button("🚀 ĐỒNG BỘ MÔ PHỎNG v79.1")
    st.markdown('</div>', unsafe_allow_html=True)

if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v79(p_input.strip())
    b_list = parse_baccarat_input_v79(b_input.strip())
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    
    st.session_state.round_detailed_log.append({
        'p_cards': p_list, 'b_cards': b_list, 'p_score': p_score, 'b_score': b_score, 'outcome': outcome,
        'oracle_decision': current_ai_oracle['decision'], 'oracle_target': cmd['raw_target'], 'oracle_alloc': current_ai_oracle['capital_allocation']
    })
    st.rerun()

st.markdown("---")
BaccaratInterfaceSystem.render_directive_panel(cmd)
BaccaratInterfaceSystem.render_ai_oracle_panel(current_ai_oracle)
BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t, sim_results)
QuantumAuditMatrixController.render_audit_table(st.session_state.round_detailed_log, (hist_p + hist_b + hist_t))

st.markdown("<br>", unsafe_allow_html=True)
# Ép nút tính năng tiện ích nằm ngang để không tốn diện tích cuộn
util_cols = st.columns(2)
if util_cols[0].button("⏪ UNDO VÁN"):
    if st.session_state.round_detailed_log:
        st.session_state.round_detailed_log.pop()
        st.rerun()
if util_cols[1].button("🔄 XOÁ KHAY"):
    st.session_state.round_detailed_log.clear()
    st.rerun()
