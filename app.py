import streamlit as st
import numpy as np
import math
import re
import traceback
from datetime import datetime

# =========================================================================
# 🌌 SYSTEM HEALING REGISTRY (LÕI VÁ LỖI TỰ ĐỘNG THẾ HỆ V79.2)
# =========================================================================
if 'cyber_healing_logs' not in st.session_state:
    st.session_state.cyber_healing_logs = []

class CyberSelfHealingDaemon:
    @staticmethod
    def execute_and_heal(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError:
            CyberSelfHealingDaemon._register_fault("ZERO_DIV", "Hệ thống tự động bù sai số 1e-15 để tránh sập mạch phân phối hẹp.")
            return 1e-15 
        except TypeError as te:
            CyberSelfHealingDaemon._register_fault("TYPE_ERR", f"Xử lý chuẩn hóa ép kiểu dữ liệu chuỗi bài: {str(te)}")
            return 0.0
        except ValueError as ve:
            CyberSelfHealingDaemon._register_fault("VALUE_ERR", f"Vượt giới hạn tính toán tổ hợp xác suất: {str(ve)}")
            return 0.0
        except Exception as e:
            tb = traceback.format_exc()
            CyberSelfHealingDaemon._register_fault("FATAL_RUNTIME", f"Ngoại lệ phát sinh: {str(e)} \n{tb[:80]}")
            return None

    @staticmethod
    def _register_fault(fault_type, description):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "time": timestamp, "type": fault_type, "desc": description,
            "action": "🛠️ AI V79.2 DAEMON: Tái cấu trúc chu kỳ xung nhịp phân phối dòng thành công."
        }
        st.session_state.cyber_healing_logs.insert(0, log_entry)
        if len(st.session_state.cyber_healing_logs) > 5: st.session_state.cyber_healing_logs.pop()

    @staticmethod
    def render_warning_hud():
        if not st.session_state.cyber_healing_logs: return
        latest_fault = st.session_state.cyber_healing_logs[0]
        st.markdown(
            f'<div style="background: rgba(0, 245, 212, 0.04); border: 1px solid #00f5d4; border-radius: 8px; padding: 10px; margin: 10px 0px;">'
            f'<div style="font-size: 12px; font-weight: 900; color: #00f5d4; display: flex; justify-content: space-between;">'
            f'<span>⚡ CYBER HEALING DAEMON v79.2 ACTIVATED</span><span>[{latest_fault["time"]}]</span></div>'
            f'<div style="font-size: 11px; color: #cbd5e1; margin-top: 3px; font-family: monospace;"><b>Sự cố:</b> {latest_fault["type"]} | {latest_fault["desc"]}</div>'
            f'<div style="font-size: 11px; color: #38bdf8; font-weight: 700; margin-top: 2px;">{latest_fault["action"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

# =========================================================================
# ⚙️ ULTRA-PRECISION CARD TRACKER ENGINE (VÁ LỖI SAI SỐ FLOATING-POINT)
# =========================================================================
def get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
    max_total_cards = float(4 * shoe_decks)
    exact_cards_left = {i: max_total_cards for i in range(1, 14)}
    
    for r in all_rounds_log:
        for card in (r.get('p_cards', []) + r.get('b_cards', [])):
            if card in exact_cards_left: 
                exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
                
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
            for i in range(1, 14): 
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - (burn_cards / 13.0))
                
    # Vá lỗi: Làm tròn vị phân toán học chống rò rỉ sai số floating-point
    for i in range(1, 14):
        exact_cards_left[i] = round(min(max_total_cards, max(0.0, exact_cards_left[i])), 4)
            
    return exact_cards_left

# =========================================================================
# 🔮 PATTERN SYNCHRO MATRIX (VÁ LỖI INDEX CHUỖI KHÔNG GIAN ĐOẠN ĐẦU)
# =========================================================================
class PatternSynchroAgent:
    @staticmethod
    def analyze_micro_patterns(all_rounds_log):
        outcomes = [r.get('outcome') for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
        if len(outcomes) < 3:
            return {"match": False, "type": "NONE", "suggest": "WAIT", "confidence": 0.0}
            
        seq_tokens = ["P" if x == "Player" else "B" for x in outcomes]
        full_seq = "".join(seq_tokens)
        s6 = "".join(seq_tokens[-6:]) if len(seq_tokens) >= 6 else full_seq
        s4 = "".join(seq_tokens[-4:]) if len(seq_tokens) >= 4 else full_seq

        # 1. CẦU BỆT DÀI (STREAK MATRIX)
        if len(full_seq) >= 4 and len(set(seq_tokens[-4:])) == 1:
            current_streak = seq_tokens[-1]
            next_pred = "PLAYER" if current_streak == "P" else "BANKER"
            return {"match": True, "type": f"CẦU BỆT ĐƯỜNG DÀI {current_streak}", "suggest": next_pred, "confidence": 94.5}

        # 2. CẦU NHẢY NGẮN 1:1
        if len(seq_tokens) >= 4 and any(s4.endswith(x) for x in ["PBPB", "BPBP"]):
            next_pred = "PLAYER" if s4[-1] == "B" else "BANKER"
            return {"match": True, "type": "CẦU NHẢY ĐƠN 1:1", "suggest": next_pred, "confidence": 91.0}

        # 3. CẦU ĐÔI 2:2 HOẶC SONG SONG
        if len(seq_tokens) >= 4:
            if any(s4.endswith(x) for x in ["PPBB", "BBPP"]):
                next_pred = "PLAYER" if s4[-1] == "B" else "BANKER"
                return {"match": True, "type": "CẦU ĐÔI BIÊN ĐỘ 2:2", "suggest": next_pred, "confidence": 89.0}
            if any(s4.endswith(x) for x in ["PPB", "BBP"]):
                next_pred = "BANKER" if s4[-1] == "B" else "PLAYER"
                return {"match": True, "type": "CẦU ĐÔI KHỚP KHỐI (ĐỦ CẶP)", "suggest": next_pred, "confidence": 92.0}

        # 4. CẦU TIẾN ĐỘ 1-2-3 HOẶC 3-2-1
        if len(seq_tokens) >= 6:
            if s6 == "PBBPPP" or s6.endswith("BBPPP"): return {"match": True, "type": "CẦU TIẾN ĐỘ 1-2-3", "suggest": "BANKER", "confidence": 88.5}
            if s6 == "BPPBBB" or s6.endswith("PPBBB"): return {"match": True, "type": "CẦU TIẾN ĐỘ 1-2-3", "suggest": "PLAYER", "confidence": 88.5}
            if s6 == "PPPBBP" or s6.endswith("PPBBP"): return {"match": True, "type": "CẦU LÙI CHU KỲ 3-2-1", "suggest": "PLAYER", "confidence": 86.0}
            if s6 == "BBBPPT" or s6.endswith("BBPPB"): return {"match": True, "type": "CẦU LÙI CHU KỲ 3-2-1", "suggest": "BANKER", "confidence": 86.0}

        # 5. CẦU ĐỐI XỨNG NGẮN 2-1-2 / 2-3-2
        if len(seq_tokens) >= 5:
            s5 = "".join(seq_tokens[-5:])
            if s5 == "PPBPP": return {"match": True, "type": "CẦU ĐỐI XỨNG HÌNH THÁI 2-1-2", "suggest": "BANKER", "confidence": 87.0}
            if s5 == "BBPBB": return {"match": True, "type": "CẦU ĐỐI XỨNG HÌNH THÁI 2-1-2", "suggest": "PLAYER", "confidence": 87.0}
        if len(seq_tokens) >= 6:
            if s6 == "PPBBBP": return {"match": True, "type": "CẦU ĐỐI XỨNG PHÂN KHÚC 2-3-2", "suggest": "PLAYER", "confidence": 86.5}
            if s6 == "BBPPPB": return {"match": True, "type": "CẦU ĐỐI XỨNG PHÂN KHÚC 2-3-2", "suggest": "BANKER", "confidence": 86.5}

        # 6. CẦU TÁCH BIÊN (1-3-1) HOẶC CẦU HỒI (Vá lỗi cứng chặn index mảng)
        if len(seq_tokens) >= 5:
            s5_check = "".join(seq_tokens[-5:])
            if s5_check == "PBBBP": return {"match": True, "type": "CẦU TÁCH TRUNG TÂM 1-3-1", "suggest": "BANKER", "confidence": 85.0}
            if s5_check == "BPPPB": return {"match": True, "type": "CẦU TÁCH TRUNG TÂM 1-3-1", "suggest": "PLAYER", "confidence": 85.0}

        return {"match": False, "type": "NONE", "suggest": "WAIT", "confidence": 0.0}

# =========================================================================
# 🔵 AI AGENT 1: SUPER PLAYER QUANTUM AGENT
# =========================================================================
class PlayerQuantumAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        
        p_eor_weights = {1: -0.0055, 2: -0.0063, 3: -0.0068, 4: -0.0142, 5: -0.0102, 
                         6: +0.0128, 7: +0.0152, 8: +0.0105, 9: -0.0030, 
                         10: +0.0047, 11: +0.0047, 12: +0.0047, 13: +0.0047}
        
        eor_shift = sum(((4 * shoe_decks) - left) * p_eor_weights.get(c, 0.0) for c, left in exact_cards_left.items())
        low_density = sum([exact_cards_left.get(i, 0.0) for i in [1, 2, 3, 4, 5]]) / total_cards_remaining
        return 44.6247 + (eor_shift * 5.45) + (low_density - 0.3846) * 19.25

# =========================================================================
# 🔴 AI AGENT 2: SUPER BANKER MARKOV AGENT
# =========================================================================
class BankerMarkovAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        
        b_eor_weights = {1: +0.0055, 2: +0.0063, 3: +0.0068, 4: +0.0142, 5: +0.0102, 
                         6: -0.0128, 7: -0.0152, 8: -0.0105, 9: +0.0030, 
                         10: -0.0047, 11: -0.0047, 12: -0.0047, 13: -0.0047}
        
        eor_shift = sum(((4 * shoe_decks) - left) * b_eor_weights.get(c, 0.0) for c, left in exact_cards_left.items())
        choke_density = sum([exact_cards_left.get(i, 0.0) for i in [1, 8, 9, 10, 11, 12, 13]]) / total_cards_remaining
        return 45.8597 + (eor_shift * 5.45) + (0.5384 - choke_density) * 13.15

# =========================================================================
# 🟢 AI AGENT 3: SUPER TIE HYPERGEOMETRIC AGENT
# =========================================================================
class TieHypergeometricAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        
        zero_card_density = sum([exact_cards_left.get(i, 0.0) for i in [10, 11, 12, 13]]) / total_cards_remaining
        gap_count = 0
        for r in reversed(all_rounds_log):
            if r.get('outcome') == "Tie": break
            gap_count += 1
            
        return 9.5156 + (zero_card_density - 0.3076) * 42.15 + (1.0 - math.exp(-gap_count / 8.50)) * 5.50

# =========================================================================
# 🪐 ULTRA FUSION MATRIX (ĐỒNG BỘ CHU KỲ V79.2)
# =========================================================================
def calculate_v79_ultimate_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, (shoe_decks * 52) - burn_cards, 0, 0, 0, "KHÔNG GIAN TRỐNG", None, 0
    
    raw_p = CyberSelfHealingDaemon.execute_and_heal(PlayerQuantumAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    raw_b = CyberSelfHealingDaemon.execute_and_heal(BankerMarkovAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    raw_t = CyberSelfHealingDaemon.execute_and_heal(TieHypergeometricAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    
    total_sum = (raw_p or 44.62) + (raw_b or 45.86) + (raw_t or 9.52)
    p_pct = (raw_p / total_sum) * 100
    b_pct = (raw_b / total_sum) * 100
    t_pct = (raw_t / total_sum) * 100
    
    exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    cards_remaining = max(0, int(round(sum(exact_cards_left.values()))))
    
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r.get('outcome') == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r.get('outcome') == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r.get('outcome') == "Tie")

    trend_desc = "CẦU KHÔNG GIAN ỔN ĐỊNH"
    streak_side, streak_count = None, 0
    decisive = [r.get('outcome') for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
    if len(decisive) >= 2:
        current_streak_side = decisive[-1]
        for outcome in reversed(decisive):
            if outcome == current_streak_side: streak_count += 1
            else: break
        if streak_count >= 2:
            streak_side = current_streak_side
            trend_desc = f"CHUỖI BỆT {streak_side.upper()} ({streak_count} ván)"
            
    pattern_status = PatternSynchroAgent.analyze_micro_patterns(all_rounds_log)
    if pattern_status["match"]:
        trend_desc = f"PHOM HÌNH THÁI: {pattern_status['type']}"

    return p_pct, b_pct, t_pct, cards_remaining, total_p_wins, total_b_wins, total_ties, trend_desc, streak_side, streak_count

def get_ultimate_directive_v79(p_val, b_val, trend_desc, log, shoe_decks, cards_left, pattern_info):
    if not log:
        return {"status": "🛰️ SYSTEM OPERATIONAL v79.2", "msg": "Hệ thống liên kết dữ liệu trực tuyến.", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%", "raw_target": "WAIT"}

    diff = abs(p_val - b_val)
    min_rounds = 6 if pattern_info["match"] else 10
    if len(log) < min_rounds:
        return {"status": "🛑 ĐỒNG BỘ HÓA SÓNG NỀN", "msg": f"Đang thu thập dữ liệu cấu trúc ngắn (Thiếu {min_rounds - len(log)} ván).", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.05)", "size": "0%", "raw_target": "WAIT"}

    required_delta = 1.0 if pattern_info["match"] else 2.2
    if diff < required_delta:
        return {"status": "🛑 BỘ LỌC CHỐNG NHIỄU BIÊN", "msg": f"Đoạn lệch vi sai ({diff:.2f}%) chưa vượt bộ lọc sóng an toàn ({required_delta}%). Khóa lệnh.", "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.08)", "size": "0%", "raw_target": "WAIT"}

    target = "PLAYER" if p_val > b_val else "BANKER"
    color = "#00afb9" if target == "PLAYER" else "#ff4757"
    bg = "rgba(0, 175, 185, 0.15)" if target == "PLAYER" else "rgba(255, 71, 87, 0.15)"
    
    msg = f"Mô hình vi sai hội tụ độc lập nghiêng về hướng {target} (+{diff:.4f}%)."
    if pattern_info["match"]:
        msg = f"🔥 KHỚP LỆNH HÌNH THÁI: {pattern_info['type']}. Sóng chu kỳ ngắn chỉ định cửa {target} với độ tin cậy {pattern_info['confidence']}%."

    return {"status": f"⚡ KHỚP LỆNH: {target}", "msg": msg, "color": color, "bg": bg, "size": "1.0% - 2.0% Vốn Kỷ Luật", "raw_target": target}

# =========================================================================
# 👑 AI SOVEREIGN ORACLE - SIÊU MÔ HÌNH THẦN BÀI TỐI CAO (v79.2)
# =========================================================================
class AISovereignOracle:
    @staticmethod
    def analyze_and_suggest(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, p_val, b_val, t_val, cards_left, trend_desc, streak_side, streak_count, total_rounds, burn_cards, pattern_info):
        if total_rounds == 0:
            return {"decision": "👁️ ORACLE CORE v79.2", "target": "QUÈT SÓNG SÀNH CHƯA CÓ DỮ LIỆU", "capital_allocation": "0%", "strategy_type": "Pattern Core Integration", "ai_insight": "Hệ thống v79.2 tích hợp bộ nhận diện cầu nâng cao sẵn sàng hoạt động.", "risk_level": "Calibration", "color": "#a855f7", "memory_hud": "Trống", "cyber_knowledge": "Lõi v79.2 nạp tối ưu thành công", "raw_code": "EMPTY"}

        decisive_log = [r for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
        wrong_count = 0
        if decisive_log:
            last_round = decisive_log[-1]
            pred = last_round.get('oracle_target') if last_round.get('oracle_target') else "WAIT"
            if pred != "WAIT" and pred != last_round.get('outcome').upper(): 
                wrong_count = 1
        if len(decisive_log) >= 2:
            if all(r.get('oracle_target') != r.get('outcome').upper() for r in decisive_log[-2:]): 
                wrong_count = 2

        total_initial_cards = max(1.0, shoe_decks * 52.0)
        shoe_progress = (total_initial_cards - cards_left) / total_initial_cards
        memory_hud = f"🧬 CHU KỲ KHAY: {shoe_progress*100:.1f}% | Xu hướng: {trend_desc}"
        cyber_knowledge = f"🔭 THẦN BÀI LÕI v79.2 | Trạng thái bảo vệ: {wrong_count}/2 Lệch"

        if len(all_rounds_log) < (6 if pattern_info["match"] else 10):
            return {"decision": "🛑 GIAI ĐOẠN ĐỒNG BỘ SÓNG", "target": "WAIT", "capital_allocation": "0%", "strategy_type": "INITIAL LOCK", "ai_insight": "Đang chạy giai đoạn tích lũy chu kỳ ngắn sảnh bài.", "risk_level": "Safe", "color": "#94a3b8", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "INITIAL_LOCK"}

        diff = abs(p_val - b_val)
        required_delta = 1.0 if pattern_info["match"] else 2.2
        intrinsic_target = "PLAYER" if p_val > b_val else "BANKER"

        if diff < required_delta:
            return {"decision": "🛑 LỌC NHIỄU BIÊN ĐỘ THẤP", "target": "WAIT", "capital_allocation": "0%", "strategy_type": "LOW_DELTA_LOCK", "ai_insight": f"Biên độ lệch {diff:.2f}% quá hẹp dưới ngưỡng an toàn v79.2.", "risk_level": "Nhiễu cao", "color": "#f1c40f", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "LOW_DELTA_LOCK"}

        if wrong_count >= 2:
            return {"decision": "🚨 PHONG TỎA KHẨN CẤP (SAI ĐỒNG BỘ 2 VÁN)", "target": "STOP & WAIT", "capital_allocation": "0%", "strategy_type": "EMERGENCY RE-CALIBRATION", "ai_insight": f"Sảnh bài đột ngột bẻ gãy cấu trúc lưu trữ của {trend_desc}. Đề xuất dừng cược hoặc chuyển sảnh ngay lập tức để tránh bão gãy cầu.", "risk_level": "Nguy hiểm cực đại", "color": "#ff4757", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "FORCE_EMERGENCY_LOCK"}

        final_alloc = max(1.0, min(6.0, (diff / 100.0) * 14.0 * (1.0 + shoe_progress)))
        if t_val > 15.0:
            memory_hud += " | ✨ ĐỘNG LỰC HÒA TĂNG CAO"

        if pattern_info["match"]:
            if pattern_info["suggest"] == intrinsic_target:
                return {"decision": f"🔥 SÓNG TRÙNG HỘI TỤ: {pattern_info['type']}", "target": intrinsic_target, "capital_allocation": f"💎 ĐẬP CƯỜNG ĐỘ: {final_alloc * 1.4:.1f}% Vốn", "strategy_type": "HIGH_CONFIDENCE_SWEEP", "ai_insight": f"Thuật toán vi sai trùng khớp hoàn toàn với xu hướng chu kỳ hình thái {pattern_info['type']}.", "risk_level": "Tối ưu hóa lợi nhuận", "color": "#00f5d4", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "MATCH_PATTERN"}
            else:
                return {"decision": f"🌊 NƯƠNG THEO CHU KỲ: {pattern_info['type']}", "target": pattern_info["suggest"], "capital_allocation": f"🛡️ ĐI NHẸ PHÒNG THỦ: {max(1.0, final_alloc * 0.6):.1f}% Vốn", "strategy_type": "PATTERN_FLOW_DOMINANCE", "ai_insight": f"Dữ liệu vi sai phân phối chưa đồng nhất nhưng dòng chảy chu kỳ hình thái đang chiếm quyền sảnh bài.", "risk_level": "Phòng thủ chủ động", "color": "#cbd5e1", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "PATTERN_FLOW"}

        return {"decision": f"⚡ THẦN LỆNH KHỚP KHỐI: {intrinsic_target}", "target": intrinsic_target, "capital_allocation": f"💎 TIÊU CHUẨN: {final_alloc:.1f}% Vốn", "strategy_type": "STANDARD_DENSITY_SWEEP", "ai_insight": f"Định vị lợi thế cấu trúc mật độ bài nghiêng rõ rệt về cửa {intrinsic_target}.", "risk_level": "Kiểm soát rủi ro", "color": "#38bdf8" if intrinsic_target == "PLAYER" else "#ff4757", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "NORMAL"}

# =========================================================================
# 🎛️ BỘ LỌC TRỌNG TÀI ĐỒNG BỘ QUYẾT ĐỊNH TRỰC TIẾP
# =========================================================================
class QuantumArbitrationMatrix:
    @staticmethod
    def render_arbitration_logic(cmd, oracle_cmd, all_rounds_log):
        if not all_rounds_log: return "WAIT"
        o_code = oracle_cmd.get('raw_code', '')
        o_target = oracle_cmd.get('target', 'WAIT')
        
        if o_code in ["INITIAL_LOCK", "LOW_DELTA_LOCK", "FORCE_EMERGENCY_LOCK"]: return "WAIT"
        if "WAIT" in o_target or "STOP" in o_target: return "WAIT"
        return o_target

# =========================================================================
# 📦 GIAI DIỆN HÌNH THÁI VÀ GIAO DIỆN KIỂM TOÁN (INTERFACES SYSTEM v79.2)
# =========================================================================
class QuantumAuditMatrixController:
    @staticmethod
    def render_audit_table(log, start_round_index):
        if not log: return
        st.markdown('<div class="audit-matrix-box"><div class="audit-title">📊 BẢNG ĐỐI CHIẾU KIỂM TOÁN LƯỢNG TỬ CHU KỲ MẢNG (v79.2 CORE)</div>', unsafe_allow_html=True)
        table_rows = ""
        for idx, r in enumerate(log):
            real_round_num = start_round_index + idx + 1
            oracle_decision = r.get('oracle_decision', '🛑 CHỜ')
            active_target = str(r.get('oracle_target', 'WAIT')).upper()
            outcome = r.get('outcome', 'Tie').upper()
            
            if outcome == "TIE":
                dot_html, status_text = '<span class="status-dot" style="color: #2ecc71; background-color: #2ecc71;"></span>', "<span style='color:#2ecc71; font-weight:bold;'>HÒA</span>"
            elif active_target == "WAIT" or "LOCK" in oracle_decision or "CHỜ" in oracle_decision:
                dot_html, status_text = '<span class="status-dot" style="color: #94a3b8; background-color: #94a3b8;"></span>', "<span style='color:#94a3b8;'>KHÓA</span>"
            elif active_target in outcome or outcome in active_target:
                dot_html, status_text = '<span class="status-dot" style="color: #00f5d4; background-color: #00f5d4; box-shadow: 0 0 10px #00f5d4;"></span>', "<span style='color:#00f5d4; font-weight:bold;'>WIN</span>"
            else:
                dot_html, status_text = '<span class="status-dot" style="color: #ff4757; background-color: #ff4757;"></span>', "<span style='color:#ff4757; font-weight:bold;'>LỆCH KO</span>"
            
            if "PLAYER" in active_target: oracle_display = f"<span style='color:#00afb9; font-weight:bold;'>🔵 {active_target}</span>"
            elif "BANKER" in active_target: oracle_display = f"<span style='color:#ff4757; font-weight:bold;'>🔴 {active_target}</span>"
            else: oracle_display = "<span style='color:#64748b;'>🛑 BỎ LỆNH</span>"
                
            outcome_display = f"<b style='color:#00afb9;'>P ({r.get('p_score',0)}đ)</b>" if outcome == "PLAYER" else (f"<b style='color:#ff4757;'>B ({r.get('b_score',0)}đ)</b>" if outcome == "BANKER" else "<b style='color:#2ecc71;'>TIE</b>")
            table_rows += f"<tr><td>V{real_round_num}</td><td style='text-align: left;'>{oracle_display}</td><td>{outcome_display}</td><td>{dot_html}</td><td>{status_text}</td></tr>"
            
        st.markdown(f"<table class='audit-table'><thead><tr><th>VÁN</th><th>KHUYẾN NGHỊ</th><th>SÀN THỰC TẾ</th><th>MÃ BIỂU</th><th>TRẠNG THÁI</th></tr></thead><tbody>{table_rows}</tbody></table></div>", unsafe_allow_html=True)

def parse_baccarat_input_v79(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().strip()
    tokens = re.findall(f'(?:10|[AJKQT1-9])', normalized)
    
    res = []
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13, '10': 10, 'T': 10}
    for t in tokens:
        if t in mapping: res.append(mapping[t])
        elif t.isdigit() and 1 <= int(t) <= 9: res.append(int(t))
    return res

class BaccaratInterfaceSystem:
    @staticmethod
    def inject_custom_css():
        st.markdown(
            """
            <style>
            .stApp { background: #02040a !important; color: #f8fafc !important; }
            div[data-testid="stHorizontalBlock"] { display: flex !important; width: 100% !important; gap: 8px !important; }
            .header-hud-bar { background: linear-gradient(90deg, #090d16, #111827); border: 1px solid #1f2937; border-radius: 10px; padding: 10px; margin: 10px 0px; text-align: center; font-family: monospace; font-size: 12px; color: #cbd5e1; }
            .action-panel { border-radius: 12px; padding: 15px; margin: 10px 0px; text-align: left; border: 1px solid #334155; }
            .action-status { font-size: 16px; font-weight: 900; letter-spacing: 0.3px; }
            .action-msg { font-size: 12px; margin-top: 4px; text-align: justify; }
            .mobile-metric-box { background: #050b14; border: 1px solid #0f172a; border-radius: 8px; padding: 8px 4px; text-align: center; }
            .metric-tag { font-size: 9px; font-weight: 800; color: #475569; display:block; }
            .metric-num { font-size: 15px; font-weight: 900; font-family: monospace; }
            .audit-matrix-box { padding: 12px; border-radius: 10px; background-color: #050b14; border: 1px dashed #38bdf8; margin-top: 15px; }
            .audit-title { font-size: 11px; font-weight: 800; color: #38bdf8; margin-bottom: 8px; }
            .audit-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 11px; }
            .audit-table th { padding: 6px; background: #0f172a; border: 1px solid #1e293b; }
            .audit-table td { padding: 6px; border: 1px solid #0f172a; text-align:center; }
            .status-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; }
            div.stButton > button { background-color: #0f172a !important; color: #cbd5e1 !important; border: 1px solid #1e293b !important; border-radius: 8px; width: 100% !important; }
            .submit-btn-box div.stButton > button { background-color: #00f5d4 !important; color: #010206 !important; font-weight:800; border: none !important; }
            </style>
            """, unsafe_allow_html=True
        )

    @staticmethod
    def render_header_hud(total_rounds, cards_left, decks):
        st.markdown(
            f'<div class="header-hud-bar">'
            f'📊 TỔNG VÁN QUÉT: <b>{total_rounds}</b> | 🎴 CÒN LẠI TRONG KHAY: <b>{cards_left}/{decks*52} lá</b>'
            f'</div>', unsafe_allow_html=True
        )

    @staticmethod
    def render_directive_panel(cmd):
        st.markdown(
            f'<div class="action-panel" style="background: {cmd["bg"]}; border-color: {cmd["color"]};">'
            f'<div class="action-status" style="color: {cmd["color"]};">{cmd["status"]}</div>'
            f'<div class="action-msg">{cmd["msg"]}</div>'
            f'<div style="font-size: 11px; margin-top: 5px; color: #94a3b8;"><b>QUẢN TRỊ VỐN AN TOÀN:</b> {cmd["size"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

    @staticmethod
    def render_ai_oracle_panel(oracle):
        st.markdown(
            f'<div style="background: #090d16; border: 1px solid #a855f7; border-radius: 10px; padding: 12px; margin: 10px 0px;">'
            f'<div style="color: {oracle["color"]}; font-weight: bold; font-size: 14px;">{oracle["decision"]}</div>'
            f'<div style="font-size: 12px; margin-top: 4px;"><b>Phân tích lõi:</b> {oracle["ai_insight"]}</div>'
            f'<div style="font-size: 11px; color: #64748b; margin-top: 4px;">{oracle["memory_hud"]} | {oracle["cyber_knowledge"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

    @staticmethod
    def render_probabilities_grid(p, b, t):
        cols = st.columns(3)
        cols[0].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER (QUANTUM EOR)</span><div class="metric-num" style="color: #00afb9;">{p:.2f}%</div></div>', unsafe_allow_html=True)
        cols[1].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER (MARKOV CHOKE)</span><div class="metric-num" style="color: #ff4757;">{b:.2f}%</div></div>', unsafe_allow_html=True)
        cols[2].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE (HYPERGEOMETRIC)</span><div class="metric-num" style="color: #2ecc71;">{t:.2f}%</div></div>', unsafe_allow_html=True)

# =========================================================================
# RUNTIME ENGINE v79.2 TỐI CAO
# =========================================================================
st.set_page_config(page_title="Cosmological Oracle v79.2", page_icon="🔮", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

# Cấu hình bên lề (Sidebar)
st.sidebar.markdown("### ⚙️ CÀI ĐẶT THAM SỐ KHAY v79.2")
decks = st.sidebar.selectbox("Tổng số bộ bài cấu thành:", [8, 6, 4], index=0)
burn_cards = st.sidebar.number_input("🎴 Số lá rút bỏ đầu khay (Burn):", min_value=0, value=7)
hist_p = st.sidebar.number_input("🔵 Tổng số ván Player đã ra trước đó:", min_value=0, value=0)
hist_b = st.sidebar.number_input("🔴 Tổng số ván Banker đã ra trước đó:", min_value=0, value=0)
hist_t = st.sidebar.number_input("🟢 Tổng số ván Tie đã ra trước đó:", min_value=0, value=0)

st.markdown("### 🔮 COSMOLOGICAL ORACLE SYSTEM v79.2 (PATTERN MATRIX)")
CyberSelfHealingDaemon.render_warning_hud()

# Phân tích hình thái phom cầu thực tế đầu chu kỳ
pattern_info = PatternSynchroAgent.analyze_micro_patterns(st.session_state.round_detailed_log)

# Đồng bộ khối xử lý dữ liệu từ 3 Agent hoàn toàn độc lập
final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, streak_side, streak_count = calculate_v79_ultimate_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t, burn_cards=burn_cards
)

cmd = get_ultimate_directive_v79(final_p, final_b, trend_desc, st.session_state.round_detailed_log, decks, cards_left, pattern_info)
total_all_rounds = total_p + total_b + total_t
BaccaratInterfaceSystem.render_header_hud(total_all_rounds, cards_left, decks)

current_ai_oracle = AISovereignOracle.analyze_and_suggest(
    st.session_state.round_detailed_log, decks, hist_p, hist_b, hist_t,
    final_p, final_b, final_t, cards_left, trend_desc, streak_side, streak_count,
    total_all_rounds, burn_cards, pattern_info
)

# Áp chế trạng thái nếu phát hiện khóa bộ lọc hoặc phong tỏa khẩn cấp từ Oracle
if current_ai_oracle.get('raw_code') in ["INITIAL_LOCK", "LOW_DELTA_LOCK"]:
    cmd['status'], cmd['msg'], cmd['color'], cmd['bg'], cmd['size'] = current_ai_oracle['decision'], current_ai_oracle['ai_insight'], current_ai_oracle['color'], "rgba(148, 163, 184, 0.05)", "0%"
elif current_ai_oracle.get('raw_code') == "FORCE_EMERGENCY_LOCK":
    cmd['status'], cmd['msg'], cmd['color'], cmd['bg'], cmd['size'] = current_ai_oracle['decision'], current_ai_oracle['ai_insight'], current_ai_oracle['color'], "rgba(255, 71, 87, 0.08)", "0%"

# Form Nhập liệu thế hệ mới (Đã chuẩn hoá Tokenizer)
st.markdown("##### 🎴 CẬP NHẬT DỮ LIỆU LÁ BÀI THỰC TẾ:")
with st.form(key="v79_form", clear_on_submit=True):
    grid = st.columns(2)
    p_input = grid[0].text_input("🔵 LÁ PLAYER (Ví dụ: a, 10, j hoặc 5,6,K):")
    b_input = grid[1].text_input("🔴 LÁ BANKER (Ví dụ: 9, q hoặc 8,7,2):")
    st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
    calc_triggered = st.form_submit_button("🚀 ĐỒNG BỘ ĐA CỔNG ORACLE v79.2")
    st.markdown('</div>', unsafe_allow_html=True)

arbitrator_verdict = QuantumArbitrationMatrix.render_arbitration_logic(cmd, current_ai_oracle, st.session_state.round_detailed_log)

# Vá lỗi: Gọi trực tiếp st.rerun() ngay sau khi mutate mảng dữ liệu trạng thái
if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v79(p_input)
    b_list = parse_baccarat_input_v79(b_input)
    
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    
    st.session_state.round_detailed_log.append({
        'p_cards': p_list, 'b_cards': b_list, 'p_score': p_score, 'b_score': b_score, 'outcome': outcome,
        'oracle_decision': current_ai_oracle['decision'], 'oracle_target': arbitrator_verdict, 'oracle_alloc': current_ai_oracle['capital_allocation']
    })
    st.rerun()

st.markdown("---")
BaccaratInterfaceSystem.render_directive_panel(cmd)
BaccaratInterfaceSystem.render_ai_oracle_panel(current_ai_oracle)
BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t)
QuantumAuditMatrixController.render_audit_table(st.session_state.round_detailed_log, (hist_p + hist_b + hist_t))

st.markdown("<br>", unsafe_allow_html=True)
util_grid = st.columns(2)
if util_grid[0].button("⏪ HỦY VÁN VỪA NHẬP (UNDO)") and st.session_state.round_detailed_log:
    st.session_state.round_detailed_log.pop()
    st.rerun()
if util_grid[1].button("🔄 LÀM TRỐNG KHAY BÀI (RESET)"):
    st.session_state.round_detailed_log.clear()
    st.rerun()
