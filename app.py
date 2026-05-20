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

    @staticmethod
    def render_warning_hud():
        if not st.session_state.cyber_healing_logs: return
        latest_fault = st.session_state.cyber_healing_logs[0]
        st.markdown(f'<div style="background: rgba(255, 71, 87, 0.1); border: 1px solid #ff4757; padding: 8px; border-radius: 6px; font-size: 11px; color:#f8fafc;">🚨 {latest_fault["desc"]}</div>', unsafe_allow_html=True)

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
            return {"p_sim_win": 44.6, "b_sim_win": 45.8, "t_sim_win": 9.5}

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

# =========================================================================
# 🪐 FUSION MATRIX & DIRECTIVE HUB
# =========================================================================
def calculate_v79_ultimate_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards):
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, (shoe_decks * 52) - burn_cards, 0, 0, 0, "TRỐNG", None, 0, {"p_sim_win": 44.6, "b_sim_win": 45.8, "t_sim_win": 9.5}
    
    raw_p = CyberSelfHealingDaemon.execute_and_heal(PlayerQuantumAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    raw_b = CyberSelfHealingDaemon.execute_and_heal(BankerMarkovAgent.compute_sovereign_probability, all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, burn_cards)
    raw_t = 9.5
    
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
    pattern_status = PatternSynchroAgent.analyze_micro_patterns(all_rounds_log)
    if pattern_status["match"]: trend_desc = f"PHOM: {pattern_status['type']}"

    return p_pct, b_pct, t_pct, cards_remaining, total_p_wins, total_b_wins, total_ties, trend_desc, None, 0, sim_results

def get_ultimate_directive_v79(p_val, b_val, trend_desc, log, shoe_decks, cards_left, pattern_info, sim_results):
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
# GIAO DIỆN SIÊU PHẲNG - ÉP CỨNG ĐỒNG BỘ CHO ĐIỆN THOẠI (KHÔNG DÙNG ST.COLUMNS)
# =========================================================================
class BaccaratInterfaceSystem:
    @staticmethod
    def inject_custom_css():
        # Phá hủy hoàn toàn cơ chế bẻ hàng dọc của Streamlit trên điện thoại bằng cách can thiệp div con [data-testid="stHorizontalBlock"]
        st.markdown(
            """
            <style>
            .stApp { background: #030712 !important; color: #f9fafb !important; }
            
            /* ÉP BUỘC CÁC PHẦN TỬ LỚN KHÔNG ĐƯỢC PHÉP DỌC TRÊN MOBILE */
            div[data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                width: 100% !important;
                gap: 5px !important;
            }
            div[data-testid="stHorizontalBlock"] > div {
                width: 50% !important; /* Dành cho khung nhập liệu đôi */
                min-width: unset !important;
            }
            
            /* THIẾT KẾ GRID 3 CỘT KHÔNG BỊ PHÁ VỠ */
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
            
            .metric-tag { font-size: 9px; font-weight: 800; color: #94a3b8; display:block; }
            .metric-num { font-size: 13px; font-weight: 900; font-family: monospace; display:block; }
            .metric-sub { font-size: 8px; color: #64748b; display:block; }
            
            /* BẢNG KIỂM TOÁN DI ĐỘNG */
            .audit-matrix-box { padding: 8px; border-radius: 6px; background-color: #0b1329; border: 1px dashed #3b82f6; margin-top: 10px; overflow-x: auto; }
            .audit-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 10px; text-align: center; }
            .audit-table th { padding: 4px; background: #1f2937; color: #94a3b8; border: 1px solid #374151; }
            .audit-table td { padding: 4px; border: 1px solid #1f2937; }
            
            /* FIX NÚT BẤM STREAMLIT TRÊN MOBILE */
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
        st.markdown(f'<div class="header-hud-bar">📱 TRUE MOBILE CORE v79.2 | VÁN: <b>{total_rounds}</b> | BÀI CÒN: <b>{cards_left} Lá</b></div>', unsafe_allow_html=True)

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
    def render_probabilities_grid(p, b, t, sim_results):
        # SỬ DỤNG HTML THUẦN KHÔNG QUA ST.COLUMNS ĐỂ ÉP NẰM NGANG TRÊN ĐIỆN THOẠI
        sim_p = sim_results.get("p_sim_win", 44.6)
        sim_b = sim_results.get("b_sim_win", 45.8)
        sim_t = sim_results.get("t_sim_win", 9.5)
        
        st.markdown(
            f'<div class="true-mobile-grid">'
            f'<div class="true-mobile-box"><span class="metric-tag">🔵 PLAYER</span><span class="metric-num" style="color:#00afb9;">{p:.1f}%</span><span class="metric-sub">M.phỏng:{sim_p:.0f}%</span></div>'
            f'<div class="true-mobile-box"><span class="metric-tag">🔴 BANKER</span><span class="metric-num" style="color:#ff4757;">{b:.1f}%</span><span class="metric-sub">M.phỏng:{sim_b:.0f}%</span></div>'
            f'<div class="true-mobile-box"><span class="metric-tag">🟢 TIE</span><span class="metric-num" style="color:#2ecc71;">{t:.1f}%</span><span class="metric-sub">M.phỏng:{sim_t:.0f}%</span></div>'
            f'</div>', unsafe_allow_html=True
        )

class QuantumAuditMatrixController:
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
# RUNTIME ENGINE APPLICATION v79.2
# =========================================================================
st.set_page_config(page_title="Oracle v79.2 Mobile", page_icon="🌌", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []

with st.expander("⚙️ CẤU HÌNH KHAY BÀI"):
    decks = st.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)
    burn_cards = st.number_input("🎴 LÁ RÚT BỎ (BURN):", min_value=0, value=7)
    hist_p = st.number_input("🔵 Player Wins thô:", min_value=0, value=0)
    hist_b = st.number_input("🔴 Banker Wins thô:", min_value=0, value=0)
    hist_t = st.number_input("🟢 Tie Wins thô:", min_value=0, value=0)

pattern_info = PatternSynchroAgent.analyze_micro_patterns(st.session_state.round_detailed_log)

final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, _, _, sim_results = calculate_v79_ultimate_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t, burn_cards=burn_cards
)

cmd = get_ultimate_directive_v79(final_p, final_b, trend_desc, st.session_state.round_detailed_log, decks, cards_left, pattern_info, sim_results)
total_all_rounds = total_p + total_b + total_t

BaccaratInterfaceSystem.render_header_hud(total_all_rounds, cards_left)

# Ô NHẬP LIỆU ĐÔI - DÙNG DIV CỦA STREAMLIT NHƯNG ĐÃ ĐƯỢC ÉP LAYOUT HÀNG NGANG BẰNG CSS GỐC Ở TRÊN
with st.form(key="v79_fixed_form", clear_on_submit=True):
    in_cols = st.columns(2)
    p_input = in_cols[0].text_input("🔵 LÁ P:")
    b_input = in_cols[1].text_input("🔴 LÁ B:")
    st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
    calc_triggered = st.form_submit_button("🚀 ĐỒNG BỘ MÔ PHỎNG v79.2")
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
BaccaratInterfaceSystem.render_directive_panel(cmd)
BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t, sim_results)
QuantumAuditMatrixController.render_audit_table(st.session_state.round_detailed_log, (hist_p + hist_b + hist_t))

st.markdown("<br>", unsafe_allow_html=True)
# HAI NÚT TIỆN ÍCH ĐÃ ĐƯỢC FIX CỐ ĐỊNH NẰM NGANG KHÔNG BỊ RỚT DÒNG TỪNG NÚT LỚN
util_cols = st.columns(2)
if util_cols[0].button("⏪ UNDO"):
    if st.session_state.round_detailed_log:
        st.session_state.round_detailed_log.pop()
        st.rerun()
if util_cols[1].button("🔄 CLEAR KHAY"):
    st.session_state.round_detailed_log.clear()
    st.rerun()
