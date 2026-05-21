import streamlit as st
import numpy as np
import math
import re
import traceback
from datetime import datetime

# =========================================================================
# 🌌 SYSTEM HEALING REGISTRY (LÕI VÁ LỖI TỰ ĐỘNG THẾ HỆ V79.3)
# =========================================================================
if 'cyber_healing_logs' not in st.session_state:
    st.session_state.cyber_healing_logs = []

class CyberSelfHealingDaemon:
    @staticmethod
    def execute_and_heal(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError:
            CyberSelfHealingDaemon._register_fault("ZERO_DIV", "Hệ thống tự động bù sai số 1e-15.")
            return 1e-15 
        except TypeError as te:
            CyberSelfHealingDaemon._register_fault("TYPE_ERR", f"Chuẩn hóa chuỗi bài: {str(te)}")
            return 0.0
        except ValueError as ve:
            CyberSelfHealingDaemon._register_fault("VALUE_ERR", f"Vượt giới hạn tính toán tổ hợp: {str(ve)}")
            return 0.0
        except Exception as e:
            tb = traceback.format_exc()
            CyberSelfHealingDaemon._register_fault("FATAL_RUNTIME", f"Ngoại lệ phát sinh: {str(e)} \n{tb[:50]}")
            return None

    @staticmethod
    def _register_fault(fault_type, description):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "time": timestamp, "type": fault_type, "desc": description,
            "action": "🛠️ AI V79.3: Đã sửa đổi xung nhịp đồng bộ giao diện di động."
        }
        st.session_state.cyber_healing_logs.insert(0, log_entry)
        if len(st.session_state.cyber_healing_logs) > 3: st.session_state.cyber_healing_logs.pop()

    @staticmethod
    def render_warning_hud():
        if not st.session_state.cyber_healing_logs: return
        latest_fault = st.session_state.cyber_healing_logs[0]
        st.markdown(
            f'<div style="background: rgba(0, 245, 212, 0.04); border: 1px solid #00f5d4; border-radius: 8px; padding: 10px; margin: 8px 0px;">'
            f'<div style="font-size: 11px; font-weight: 900; color: #00f5d4; display: flex; justify-content: space-between;">'
            f'<span>⚡ MOBILE HEALING DAEMON v79.3</span><span>[{latest_fault["time"]}]</span></div>'
            f'<div style="font-size: 11px; color: #cbd5e1; margin-top: 2px; font-family: monospace;"><b>Lỗi:</b> {latest_fault["type"]} | {latest_fault["desc"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

# =========================================================================
# ⚙️ ULTRA-PRECISION CARD TRACKER ENGINE
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
                
    for i in range(1, 14):
        exact_cards_left[i] = round(min(max_total_cards, max(0.0, exact_cards_left[i])), 4)
            
    return exact_cards_left

# =========================================================================
# 🔮 PATTERN SYNCHRO MATRIX
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

        if len(full_seq) >= 4 and len(set(seq_tokens[-4:])) == 1:
            current_streak = seq_tokens[-1]
            next_pred = "PLAYER" if current_streak == "P" else "BANKER"
            return {"match": True, "type": f"CẦU BỆT DÀI {current_streak}", "suggest": next_pred, "confidence": 94.5}

        if len(seq_tokens) >= 4 and any(s4.endswith(x) for x in ["PBPB", "BPBP"]):
            next_pred = "PLAYER" if s4[-1] == "B" else "BANKER"
            return {"match": True, "type": "CẦU NHẢY ĐƠN 1:1", "suggest": next_pred, "confidence": 91.0}

        if len(seq_tokens) >= 4:
            if any(s4.endswith(x) for x in ["PPBB", "BBPP"]):
                next_pred = "PLAYER" if s4[-1] == "B" else "BANKER"
                return {"match": True, "type": "CẦU ĐÔI BIÊN ĐỘ 2:2", "suggest": next_pred, "confidence": 89.0}
            if any(s4.endswith(x) for x in ["PPB", "BBP"]):
                next_pred = "BANKER" if s4[-1] == "B" else "PLAYER"
                return {"match": True, "type": "CẦU ĐÔI ĐỦ CẶP", "suggest": next_pred, "confidence": 92.0}

        if len(seq_tokens) >= 6:
            if s6.endswith("PBBPPP"): return {"match": True, "type": "CẦU TIẾN 1-2-3", "suggest": "BANKER", "confidence": 88.5}
            if s6.endswith("BPPBBB"): return {"match": True, "type": "CẦU TIẾN 1-2-3", "suggest": "PLAYER", "confidence": 88.5}

        if len(seq_tokens) >= 5:
            s5_check = "".join(seq_tokens[-5:])
            if s5_check == "PBBBP": return {"match": True, "type": "CẦU TÁCH 1-3-1", "suggest": "BANKER", "confidence": 85.0}
            if s5_check == "BPPPB": return {"match": True, "type": "CẦU TÁCH 1-3-1", "suggest": "PLAYER", "confidence": 85.0}

        return {"match": False, "type": "NONE", "suggest": "WAIT", "confidence": 0.0}

# =========================================================================
# CORE AI AGENTS
# =========================================================================
class PlayerQuantumAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        p_eor_weights = {1: -0.0055, 2: -0.0063, 3: -0.0068, 4: -0.0142, 5: -0.0102, 6: +0.0128, 7: +0.0152, 8: +0.0105, 9: -0.0030, 10: +0.0047, 11: +0.0047, 12: +0.0047, 13: +0.0047}
        eor_shift = sum(((4 * shoe_decks) - left) * p_eor_weights.get(c, 0.0) for c, left in exact_cards_left.items())
        low_density = sum([exact_cards_left.get(i, 0.0) for i in [1, 2, 3, 4, 5]]) / total_cards_remaining
        return 44.6247 + (eor_shift * 5.45) + (low_density - 0.3846) * 19.25

class BankerMarkovAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
        exact_cards_left = get_exact_remaining_cards(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
        total_cards_remaining = max(1.0, sum(exact_cards_left.values()))
        b_eor_weights = {1: +0.0055, 2: +0.0063, 3: +0.0068, 4: +0.0142, 5: +0.0102, 6: -0.0128, 7: -0.0152, 8: -0.0105, 9: +0.0030, 10: -0.0047, 11: -0.0047, 12: -0.0047, 13: -0.0047}
        eor_shift = sum(((4 * shoe_decks) - left) * b_eor_weights.get(c, 0.0) for c, left in exact_cards_left.items())
        choke_density = sum([exact_cards_left.get(i, 0.0) for i in [1, 8, 9, 10, 11, 12, 13]]) / total_cards_remaining
        return 45.8597 + (eor_shift * 5.45) + (0.5384 - choke_density) * 13.15

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
# FUSION & DIRECTIVE
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

    trend_desc = "CẦU ỔN ĐỊNH"
    streak_side, streak_count = None, 0
    decisive = [r.get('outcome') for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
    if len(decisive) >= 2:
        current_streak_side = decisive[-1]
        for outcome in reversed(decisive):
            if outcome == current_streak_side: streak_count += 1
            else: break
        if streak_count >= 2:
            streak_side = current_streak_side
            trend_desc = f"BỆT {streak_side.upper()} ({streak_count}v)"
            
    pattern_status = PatternSynchroAgent.analyze_micro_patterns(all_rounds_log)
    if pattern_status["match"]: trend_desc = f"{pattern_status['type']}"

    return p_pct, b_pct, t_pct, cards_remaining, total_p_wins, total_b_wins, total_ties, trend_desc, streak_side, streak_count

def get_ultimate_directive_v79(p_val, b_val, trend_desc, log, shoe_decks, cards_left, pattern_info):
    if not log:
        return {"status": "🛰️ SYSTEM READY v79.3", "msg": "Hệ thống đã sẵn sàng quét sảnh bài.", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%", "raw_target": "WAIT"}

    diff = abs(p_val - b_val)
    min_rounds = 6 if pattern_info["match"] else 10
    if len(log) < min_rounds:
        return {"status": "🛑 ĐỒNG BỘ SÓNG NỀN", "msg": f"Đang thu thập dữ liệu cấu trúc ngắn (Thiếu {min_rounds - len(log)} ván).", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.05)", "size": "0%", "raw_target": "WAIT"}

    required_delta = 1.0 if pattern_info["match"] else 2.2
    if diff < required_delta:
        return {"status": "🛑 LỌC NHIỄU BIÊN ĐỘ", "msg": f"Độ lệch vi sai ({diff:.2f}%) nằm dưới ngưỡng an toàn.", "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.08)", "size": "0%", "raw_target": "WAIT"}

    target = "PLAYER" if p_val > b_val else "BANKER"
    color = "#00afb9" if target == "PLAYER" else "#ff4757"
    bg = "rgba(0, 175, 185, 0.12)" if target == "PLAYER" else "rgba(255, 71, 87, 0.12)"
    
    msg = f"Lợi thế nghiêng về {target} (+{diff:.2f}%)."
    if pattern_info["match"]:
        msg = f"🔥 KHỚP HÌNH THÁI: {pattern_info['type']}. Chỉ định cửa {target} ({pattern_info['confidence']}%)."

    return {"status": f"⚡ LỆNH KHỚP: {target}", "msg": msg, "color": color, "bg": bg, "size": "1% - 2% Vốn Kỷ Luật", "raw_target": target}

class AISovereignOracle:
    @staticmethod
    def analyze_and_suggest(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, p_val, b_val, t_val, cards_left, trend_desc, streak_side, streak_count, total_rounds, burn_cards, pattern_info):
        if total_rounds == 0:
            return {"decision": "👁️ ORACLE CORE v79.3", "ai_insight": "Hệ thống tối ưu hiển thị di động đã nạp thành công.", "risk_level": "Calibration", "color": "#a855f7", "memory_hud": "Chưa có dữ liệu", "cyber_knowledge": "Bảo vệ chủ động", "raw_code": "EMPTY", "target": "WAIT", "capital_allocation": "0%"}

        decisive_log = [r for r in all_rounds_log if r.get('outcome') in ["Player", "Banker"]]
        wrong_count = 0
        if decisive_log:
            last_round = decisive_log[-1]
            pred = last_round.get('oracle_target') if last_round.get('oracle_target') else "WAIT"
            if pred != "WAIT" and pred != last_round.get('outcome').upper(): wrong_count = 1
        if len(decisive_log) >= 2:
            if all(r.get('oracle_target') != r.get('outcome').upper() for r in decisive_log[-2:]): wrong_count = 2

        total_initial_cards = max(1.0, shoe_decks * 52.0)
        shoe_progress = (total_initial_cards - cards_left) / total_initial_cards
        memory_hud = f"🧬 CHU KỲ KHAY: {shoe_progress*100:.1f}% | Xu hướng: {trend_desc}"
        cyber_knowledge = f"🔭 LỆCH: {wrong_count}/2"

        if len(all_rounds_log) < (6 if pattern_info["match"] else 10):
            return {"decision": "🛑 GIAI ĐOẠN ĐỒNG BỘ SÓNG", "capital_allocation": "0%", "strategy_type": "INITIAL LOCK", "ai_insight": "Đang chạy giai đoạn tích lũy chu kỳ ngắn.", "risk_level": "Safe", "color": "#94a3b8", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "INITIAL_LOCK", "target": "WAIT"}

        diff = abs(p_val - b_val)
        required_delta = 1.0 if pattern_info["match"] else 2.2
        intrinsic_target = "PLAYER" if p_val > b_val else "BANKER"

        if diff < required_delta:
            return {"decision": "🛑 LỌC NHIỄU BIÊN ĐỘ THẤP", "capital_allocation": "0%", "strategy_type": "LOW_DELTA_LOCK", "ai_insight": f"Biên độ lệch {diff:.2f}% quá hẹp.", "risk_level": "Nhiễu cao", "color": "#f1c40f", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "LOW_DELTA_LOCK", "target": "WAIT"}

        if wrong_count >= 2:
            return {"decision": "🚨 PHONG TỎA KHẨN CẤP", "capital_allocation": "0%", "strategy_type": "EMERGENCY LOCK", "ai_insight": "Lệch chuỗi 2 ván liên tiếp. Tạm dừng để bảo toàn tài khoản.", "risk_level": "Nguy hiểm", "color": "#ff4757", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "FORCE_EMERGENCY_LOCK", "target": "STOP"}

        final_alloc = max(1.0, min(6.0, (diff / 100.0) * 14.0 * (1.0 + shoe_progress)))
        if pattern_info["match"] and pattern_info["suggest"] == intrinsic_target:
            return {"decision": f"🔥 SÓNG TRÙNG: {pattern_info['type']}", "target": intrinsic_target, "capital_allocation": f"{final_alloc * 1.3:.1f}% Vốn", "ai_insight": "Thuật toán vi sai trùng khớp hoàn toàn với xu hướng chu kỳ hình thái.", "color": "#00f5d4", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "MATCH_PATTERN"}

        return {"decision": f"⚡ THẦN LỆNH: {intrinsic_target}", "target": intrinsic_target, "capital_allocation": f"{final_alloc:.1f}% Vốn", "ai_insight": f"Định vị lợi thế cấu trúc mật độ bài nghiêng về cửa {intrinsic_target}.", "color": "#38bdf8" if intrinsic_target == "PLAYER" else "#ff4757", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge, "raw_code": "NORMAL"}

class QuantumArbitrationMatrix:
    @staticmethod
    def render_arbitration_logic(oracle_cmd):
        o_code = oracle_cmd.get('raw_code', '')
        o_target = oracle_cmd.get('target', 'WAIT')
        if o_code in ["INITIAL_LOCK", "LOW_DELTA_LOCK", "FORCE_EMERGENCY_LOCK"] or "WAIT" in o_target or "STOP" in o_target:
            return "WAIT"
        return o_target

# =========================================================================
# 📦 GIẢI PHÁP CSS RESPONSIVE TOÀN DIỆN CHO DI ĐỘNG (MOBILE CSS CORRECTION)
# =========================================================================
class BaccaratInterfaceSystem:
    @staticmethod
    def inject_custom_css():
        st.markdown(
            """
            <style>
            /* Reset & Dark Mode Base */
            .stApp { background: #02040a !important; color: #f8fafc !important; }
            
            /* Sửa lỗi tràn block ngang trên Mobile */
            div[data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-wrap: wrap !important;
                width: 100% !important;
                gap: 6px !important;
            }
            div[data-testid="column"] {
                flex: 1 1 30% !important;
                min-width: 100px !important;
            }
            @media (max-width: 480px) {
                div[data-testid="column"] { flex: 1 1 100% !important; }
            }

            /* Header HUD */
            .header-hud-bar { 
                background: linear-gradient(90deg, #090d16, #111827); 
                border: 1px solid #1f2937; 
                border-radius: 8px; 
                padding: 10px; 
                margin: 5px 0px; 
                text-align: center; 
                font-family: monospace; 
                font-size: 11px; 
                color: #cbd5e1; 
            }
            
            /* Responsive Panels */
            .action-panel { border-radius: 10px; padding: 12px; margin: 8px 0px; border: 1px solid #334155; }
            .action-status { font-size: 15px; font-weight: 900; letter-spacing: 0.3px; }
            .action-msg { font-size: 12px; margin-top: 3px; }
            
            /* Mobile Metrics Grid (Hỗ trợ flex tự xuống hàng trên điện thoại) */
            .mobile-metric-container {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                width: 100%;
                margin: 8px 0px;
            }
            .mobile-metric-box { 
                flex: 1 1 calc(33.33% - 6px);
                background: #050b14; 
                border: 1px solid #1e293b; 
                border-radius: 6px; 
                padding: 8px 4px; 
                text-align: center;
                min-width: 90px;
            }
            @media (max-width: 480px) {
                .mobile-metric-box { flex: 1 1 100%; text-align: left; padding-left: 15px; }
                .metric-num { display: inline-block; float: right; padding-right: 15px; }
            }
            .metric-tag { font-size: 9px; font-weight: 800; color: #64748b; display: block; }
            .metric-num { font-size: 14px; font-weight: 900; font-family: monospace; }
            
            /* Bảng kiểm toán chống tràn màn hình cảm ứng */
            .audit-matrix-box { 
                padding: 10px; 
                border-radius: 8px; 
                background-color: #050b14; 
                border: 1px dashed #38bdf8; 
                margin-top: 12px; 
                overflow-x: auto; /* Tạo thanh cuộn ngang khi xem trên điện thoại */
                -webkit-overflow-scrolling: touch;
            }
            .audit-title { font-size: 11px; font-weight: 800; color: #38bdf8; margin-bottom: 6px; }
            .audit-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 11px; min-width: 320px; }
            .audit-table th { padding: 6px; background: #0f172a; border: 1px solid #1e293b; color: #94a3b8; }
            .audit-table td { padding: 6px; border: 1px solid #0f172a; text-align: center; color: #f1f5f9; }
            .status-dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%; vertical-align: middle; margin-right: 4px; }
            
            /* Tối ưu hóa Nút bấm trên thiết bị di động */
            div.stButton > button { 
                background-color: #0f172a !important; 
                color: #cbd5e1 !important; 
                border: 1px solid #1e293b !important; 
                border-radius: 8px; 
                width: 100% !important; 
                min-height: 42px !important; /* Đạt chuẩn kích thước nhấn ngón tay */
                font-size: 12px !important;
            }
            .submit-btn-box div.stButton > button { 
                background-color: #00f5d4 !important; 
                color: #010206 !important; 
                font-weight: 800; 
                border: none !important;
                box-shadow: 0 0 10px rgba(0, 245, 212, 0.2);
            }
            </style>
            """, unsafe_allow_html=True
        )

    @staticmethod
    def render_header_hud(total_rounds, cards_left, decks):
        st.markdown(
            f'<div class="header-hud-bar">'
            f'📊 QUÉT: <b>{total_rounds}v</b> | 🎴 KHAY CÒN: <b>{cards_left}/{decks*52} lá</b>'
            f'</div>', unsafe_allow_html=True
        )

    @staticmethod
    def render_directive_panel(cmd):
        st.markdown(
            f'<div class="action-panel" style="background: {cmd["bg"]}; border-color: {cmd["color"]};">'
            f'<div class="action-status" style="color: {cmd["color"]};">{cmd["status"]}</div>'
            f'<div class="action-msg">{cmd["msg"]}</div>'
            f'<div style="font-size: 11px; margin-top: 4px; color: #94a3b8;"><b>QUẢN LÝ VỐN:</b> {cmd["size"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

    @staticmethod
    def render_ai_oracle_panel(oracle):
        st.markdown(
            f'<div style="background: #090d16; border: 1px solid #a855f7; border-radius: 8px; padding: 10px; margin: 6px 0px;">'
            f'<div style="color: {oracle["color"]}; font-weight: bold; font-size: 13px;">{oracle["decision"]}</div>'
            f'<div style="font-size: 11px; margin-top: 2px;">{oracle["ai_insight"]}</div>'
            f'<div style="font-size: 10px; color: #64748b; margin-top: 3px;">{oracle["memory_hud"]} | {oracle["cyber_knowledge"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

    @staticmethod
    def render_probabilities_grid(p, b, t):
        st.markdown(
            f'<div class="mobile-metric-container">'
            f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER (QUANTUM)</span><span class="metric-num" style="color: #00afb9;">{p:.2f}%</span></div>'
            f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER (MARKOV)</span><span class="metric-num" style="color: #ff4757;">{b:.2f}%</span></div>'
            f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE (HYPER)</span><span class="metric-num" style="color: #2ecc71;">{t:.2f}%</span></div>'
            f'</div>', unsafe_allow_html=True
        )

class QuantumAuditMatrixController:
    @staticmethod
    def render_audit_table(log, start_round_index):
        if not log: return
        st.markdown('<div class="audit-matrix-box"><div class="audit-title">📊 BẢNG ĐỐI CHIẾU KIỂM TOÁN LƯỢNG TỬ (v79.3)</div>', unsafe_allow_html=True)
        table_rows = ""
        for idx, r in enumerate(log):
            real_round_num = start_round_index + idx + 1
            oracle_decision = r.get('oracle_decision', '🛑 CHỜ')
            active_target = str(r.get('oracle_target', 'WAIT')).upper()
            outcome = r.get('outcome', 'Tie').upper()
            
            if outcome == "TIE":
                dot_html, status_text = '<span class="status-dot" style="background-color: #2ecc71;"></span>', "<span style='color:#2ecc71; font-weight:bold;'>HÒA</span>"
            elif active_target == "WAIT" or "LOCK" in oracle_decision or "CHỜ" in oracle_decision:
                dot_html, status_text = '<span class="status-dot" style="background-color: #94a3b8;"></span>', "<span style='color:#94a3b8;'>KHÓA</span>"
            elif active_target in outcome or outcome in active_target:
                dot_html, status_text = '<span class="status-dot" style="background-color: #00f5d4; box-shadow: 0 0 5px #00f5d4;"></span>', "<span style='color:#00f5d4; font-weight:bold;'>WIN</span>"
            else:
                dot_html, status_text = '<span class="status-dot" style="background-color: #ff4757;"></span>', "<span style='color:#ff4757; font-weight:bold;'>LỆCH</span>"
            
            if "PLAYER" in active_target: oracle_display = "<span style='color:#00afb9; font-weight:bold;'>🔵 PLAYER</span>"
            elif "BANKER" in active_target: oracle_display = "<span style='color:#ff4757; font-weight:bold;'>🔴 BANKER</span>"
            else: oracle_display = "<span style='color:#64748b;'>🛑 BỎ LỆNH</span>"
                
            outcome_display = f"<span style='color:#00afb9; font-weight:bold;'>P ({r.get('p_score',0)})</span>" if outcome == "PLAYER" else (f"<span style='color:#ff4757; font-weight:bold;'>B ({r.get('b_score',0)})</span>" if outcome == "BANKER" else "<span style='color:#2ecc71;'>TIE</span>")
            table_rows += f"<tr><td>V{real_round_num}</td><td style='text-align: left;'>{oracle_display}</td><td>{outcome_display}</td><td>{dot_html}{status_text}</td></tr>"
            
        st.markdown(f"<table class='audit-table'><thead><tr><th>VÁN</th><th>KHUYẾN NGHỊ</th><th>SÀN THỰC TẾ</th><th>TRẠNG THÁI</th></tr></thead><tbody>{table_rows}</tbody></table></div>", unsafe_allow_html=True)

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

# =========================================================================
# RUNTIME ENGINE v79.3 RESPONSIVE
# =========================================================================
st.set_page_config(page_title="Cosmological Oracle v79.3", page_icon="🔮", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

# Sidebar cấu hình tham số khay bài
st.sidebar.markdown("### ⚙️ CÀI ĐẶT THAM SỐ KHAY v79.3")
decks = st.sidebar.selectbox("Tổng số bộ bài cấu thành:", [8, 6, 4], index=0)
burn_cards = st.sidebar.number_input("🎴 Số lá rút bỏ đầu khay (Burn):", min_value=0, value=7)
hist_p = st.sidebar.number_input("🔵 Tổng số ván Player đã ra trước đó:", min_value=0, value=0)
hist_b = st.sidebar.number_input("🔴 Tổng số ván Banker đã ra trước đó:", min_value=0, value=0)
hist_t = st.sidebar.number_input("🟢 Tổng số ván Tie đã ra trước đó:", min_value=0, value=0)

st.markdown("### 🔮 COSMOLOGICAL ORACLE v79.3")
CyberSelfHealingDaemon.render_warning_hud()

# Đồng bộ dữ liệu lõi
pattern_info = PatternSynchroAgent.analyze_micro_patterns(st.session_state.round_detailed_log)
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

if current_ai_oracle.get('raw_code') in ["INITIAL_LOCK", "LOW_DELTA_LOCK"]:
    cmd['status'], cmd['msg'], cmd['color'], cmd['bg'], cmd['size'] = current_ai_oracle['decision'], current_ai_oracle['ai_insight'], current_ai_oracle['color'], "rgba(148, 163, 184, 0.05)", "0%"
elif current_ai_oracle.get('raw_code') == "FORCE_EMERGENCY_LOCK":
    cmd['status'], cmd['msg'], cmd['color'], cmd['bg'], cmd['size'] = current_ai_oracle['decision'], current_ai_oracle['ai_insight'], current_ai_oracle['color'], "rgba(255, 71, 87, 0.08)", "0%"

arbitrator_verdict = QuantumArbitrationMatrix.render_arbitration_logic(current_ai_oracle)

# Form nhập liệu tối ưu hóa cột phản hồi di động
st.markdown("##### 🎴 CẬP NHẬT DỮ LIỆU LÁ BÀI:")
with st.form(key="v79_form", clear_on_submit=True):
    p_input = st.text_input("🔵 LÁ PLAYER (Ví dụ: 5,6,K hoặc a,10):")
    b_input = st.text_input("🔴 LÁ BANKER (Ví dụ: 8,7,2 hoặc 9,q):")
    st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
    calc_triggered = st.form_submit_button("🚀 ĐỒNG BỘ ĐA CỔNG ORACLE v79.3")
    st.markdown('</div>', unsafe_allow_html=True)

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

# Cụm công cụ điều khiển chân trang đạt kích thước chuẩn Mobile tap
st.markdown("<br>", unsafe_allow_html=True)
if st.button("⏪ HỦY VÁN VỪA NHẬP (UNDO)") and st.session_state.round_detailed_log:
    st.session_state.round_detailed_log.pop()
    st.rerun()
if st.button("🔄 LÀM TRỐNG KHAY BÀI (RESET)"):
    st.session_state.round_detailed_log.clear()
    st.rerun()
