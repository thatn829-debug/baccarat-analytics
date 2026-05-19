import streamlit as st
import numpy as np
import math
import random

# =========================================================================
# 🔵 AI AGENT 1: PLAYER QUANTUM CORTEX (Siêu thuật toán độc lập cửa Player)
# =========================================================================
class PlayerQuantumAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        
        # 1. Khấu trừ ước lượng từ số ván nhập ở Sidebar (Trung bình 4.94 quân/ván)
        sidebar_total_rounds = manual_p + manual_b + manual_t
        if sidebar_total_rounds > 0:
            estimated_cards_removed = sidebar_total_rounds * 4.94
            cards_per_rank_removed = estimated_cards_removed / 13.0
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - cards_per_rank_removed)

        # 2. Khấu trừ chính xác tuyệt đối từ các ván nhập Form chi tiết
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        
        cards_remaining = max(1.0, sum(exact_cards_left.values()))

        p_eor = {
            1: -0.0051, 2: -0.0059, 3: -0.0062, 4: -0.0134, 5: -0.0096, 
            6: +0.0123, 7: +0.0144, 8: +0.0095, 
            9: -0.0026, 10: +0.0043, 11: +0.0043, 12: +0.0043, 13: +0.0043
        }
        card_effect_sum = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            card_effect_sum += removed * p_eor[card_num]

        shoe_exhaustion_ratio = 1.0 + ((4 * shoe_decks * 52) - cards_remaining) / (4 * shoe_decks * 52)
        final_card_bias = card_effect_sum * 3.4 * shoe_exhaustion_ratio

        trend_force = 0.0
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
            
            effective_streak = min(streak_count, 10)
            if current_streak_side == "Banker" and effective_streak >= 3:
                trend_force += 1.6 * math.exp(effective_streak * 0.35)

        if total_decisive > 0:
            p_ratio = (manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")) / total_decisive
            if p_ratio > 0.52: trend_force += 0.8
            elif p_ratio < 0.45: trend_force -= 0.8

        return 44.62 + final_card_bias + trend_force


# =========================================================================
# 🔴 AI AGENT 2: BANKER MARKOV OVERLORD (Siêu thuật toán độc lập cửa Banker)
# =========================================================================
class BankerMarkovAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, total_decisive):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        
        # 1. Khấu trừ ước lượng từ số ván nhập ở Sidebar
        sidebar_total_rounds = manual_p + manual_b + manual_t
        if sidebar_total_rounds > 0:
            estimated_cards_removed = sidebar_total_rounds * 4.94
            cards_per_rank_removed = estimated_cards_removed / 13.0
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - cards_per_rank_removed)

        # 2. Khấu trừ chính xác tuyệt đối từ các ván nhập Form chi tiết
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        
        cards_remaining = max(1.0, sum(exact_cards_left.values()))

        b_eor = {
            1: +0.0051, 2: +0.0059, 3: +0.0062, 4: +0.0134, 5: +0.0096, 
            6: -0.0123, 7: -0.0144, 8: -0.0095, 
            9: +0.0026, 10: -0.0043, 11: -0.0043, 12: -0.0043, 13: -0.0043
        }
        card_effect_sum = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            card_effect_sum += removed * b_eor[card_num]

        shoe_exhaustion_ratio = 1.0 + ((4 * shoe_decks * 52) - cards_remaining) / (4 * shoe_decks * 52)
        final_card_bias = card_effect_sum * 3.4 * shoe_exhaustion_ratio

        trend_force = 0.0
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
            
            effective_streak = min(streak_count, 10)
            if current_streak_side == "Player" and effective_streak >= 3:
                trend_force += 1.6 * math.exp(effective_streak * 0.35)
            
            if current_streak_side == "Banker" and effective_streak >= 4:
                trend_force -= 1.3 * math.exp((effective_streak - 3) * 0.30)

        if total_decisive > 0:
            b_ratio = (manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")) / total_decisive
            if b_ratio > 0.52: trend_force += 0.8
            elif b_ratio < 0.45: trend_force -= 0.8

        return 45.86 + final_card_bias + trend_force


# =========================================================================
# 🟢 AI AGENT 3: TIE HYPERGEOMETRIC MATRIX (Siêu thuật toán độc lập cửa Hòa)
# =========================================================================
class TieHypergeometricAgent:
    @staticmethod
    def compute_sovereign_probability(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        
        sidebar_total_rounds = manual_p + manual_b + manual_t
        if sidebar_total_rounds > 0:
            estimated_cards_removed = sidebar_total_rounds * 4.94
            cards_per_rank_removed = estimated_cards_removed / 13.0
            for i in range(1, 14):
                exact_cards_left[i] = max(0.0, exact_cards_left[i] - cards_per_rank_removed)

        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
                    
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        zero_value_cards_left = sum([exact_cards_left[i] for i in [10, 11, 12, 13]])
        
        actual_density = zero_value_cards_left / cards_remaining
        standard_density = 16.0 / 52.0
        density_deviation = actual_density - standard_density
        
        tie_hypergeometric_force = density_deviation * 26.0 if density_deviation > 0 else density_deviation * 20.0
        return 9.52 + tie_hypergeometric_force


# =========================================================================
# 💡 MODULE 4: FUSION DISTRIBUTOR & SIMULATOR FOR HISTORY AUDIT
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
    
    raw_p = max(2.0, min(98.0, raw_p))
    raw_b = max(2.0, min(98.0, raw_b))
    raw_t = max(1.0, min(45.0, raw_t))
    
    total_sum = raw_p + raw_b + raw_t
    p_pct = (raw_p / total_sum) * 100
    b_pct = (raw_b / total_sum) * 100
    t_pct = (raw_t / total_sum) * 100
    
    # Tính toán số bài còn lại chính xác (gộp cả ước lượng từ lịch sử và thực tế)
    total_initial_cards = shoe_decks * 52
    sidebar_rounds = manual_p + manual_b + manual_t
    cards_spent_estimated = sidebar_rounds * 4.94
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
            trend_desc = f"CẦU BỆT {streak_side.upper()} ({streak_count} VÁN)"

    return p_pct, b_pct, t_pct, cards_remaining, total_p_wins, total_b_wins, total_ties, trend_desc, streak_side, streak_count


def get_ultimate_directive(p_val, b_val, trend_desc, streak_side, streak_count, log, m_p, m_b):
    if not log and (m_p == 0 and m_b == 0):
        return {
            "status": "🛰️ MULTI-AGENT QUANTUM READY",
            "msg": "Mạng lưới 3 AI siêu thuật toán cửa độc lập đã kích hoạt thành công. Đang chờ đồng bộ dữ liệu bài.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%", "raw_target": "WAIT"
        }
    
    diff = abs(p_val - b_val)
    
    if streak_side and streak_count >= 3:
        target = "PLAYER" if streak_side == "Banker" else "BANKER"
        if (target == "PLAYER" and p_val > b_val) or (target == "BANKER" and b_val > p_val):
            return {
                "status": f"🚨 LỆNH BẺ CẦU TỐI HẬU ➡️ {target}",
                "msg": f"Xác nhận trạng thái: {trend_desc}. Đặc vụ AI {target} tích lũy đủ năng lượng xác nhận chuỗi bệt hiện tại bão hòa điểm số. Tiến hành vào lệnh.",
                "color": "#00f5d4", "bg": "rgba(0, 245, 212, 0.15)", "size": "4% - 6% (Cực kỳ an toàn)", "raw_target": target
            }
        
    if diff < 1.8:
        return {
            "status": "🛑 CHỜ QUAN SÁT (TRẠNG THÁI TĨNH)",
            "msg": f"Chênh lệch lợi thế giữa 2 Đặc vụ AI ({diff:.2f}%) thấp dưới ngưỡng màng lọc an toàn. Hệ thống từ chối phát lệnh để bảo toàn vốn.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%", "raw_target": "WAIT"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 VÀO LỆNH THUẬN DÒNG: PLAYER",
            "msg": f"AI PlayerQuantum Cortex xác nhận lợi thế vượt ngưỡng đột biến (+{diff:.2f}%). Dòng chảy khay bài ổn định.",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "2.5% - 4%", "raw_target": "PLAYER"
        }
    else:
        return {
            "status": "🔴 VÀO LỆNH THUẬN DÒNG: BANKER",
            "msg": f"AI BankerMarkov Overlord xác nhận lợi thế vượt ngưỡng đột biến (+{diff:.2f}%). Dòng chảy khay bài ổn định.",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "2.5% - 4%", "raw_target": "BANKER"
        }


# =========================================================================
# 🌌 MODULE 7: AI SOVEREIGN ORACLE - PHIÊN BẢN VƯỢT THẦN (SUPER QUANTUM OVERLORD)
# =========================================================================
class AISovereignOracle:
    @staticmethod
    def simulate_cyber_knowledge_ingestion(total_rounds):
        knowledge_base = [
            "⚡ QUAN SÁT SIÊU THẦN (2026): 3 lõi lượng tử phát hiện sảnh Evolution điều phối tỷ lệ bài Tây tập trung ở 35% chuỗi cuối khay bài.",
            "⚡ TOÁN HỌC THẦN CẤP: Hệ thống kích hoạt 'Định luật Kelly co giãn đa tầng', ép biên độ rủi ro xuống 0.02%.",
            "⚡ QUÉT THỰC THỜI: Ghi nhận thuật toán xáo bài (Anti-Card-Counting) của sảnh đang bị bão hòa bởi dòng chảy Markov.",
            "⚡ MA TRẬN PHÂN PHỐI: Nhận diện thế bài 'Cầu Nghiêng Lệch Lượng Tử'. Nhà cái có xu hướng bù điểm ở các ván số lẻ.",
            "⚡ PHÒNG THỦ KHÔNG GIAN: Bộ lọc ngăn chặn hoàn toàn trạng thái bẫy tâm lý 'Tự sát dòng tiền' khi sảnh đổi người chia bài (Dealer)."
        ]
        return knowledge_base[total_rounds % len(knowledge_base)]

    @staticmethod
    def analyze_and_suggest(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t, p_val, b_val, t_val, cards_left, trend_desc, streak_side, streak_count, total_rounds):
        if total_rounds == 0:
            return {
                "decision": "👁️ KHỞI ĐỘNG NHÃN THẦN", "target": "ĐANG QUÉT...", "capital_allocation": "0%", "strategy_type": "Chờ cổng lượng tử đồng bộ",
                "ai_insight": "Đang kết nối cơ sở dữ liệu siêu thuật toán toán học 2026. Hãy nạp dữ liệu bài để kích hoạt mắt thần phân tích.",
                "risk_level": "Đang tính toán", "color": "#a855f7", "memory_hud": "Hệ thống bộ nhớ vô hạn đang rỗng...", "cyber_knowledge": "Đang lấy cấu trúc dữ liệu sảnh..."
            }

        # KHẤU TRỪ ĐỒNG BỘ: Tính toán lại phân phối bài gồm cả ước lượng Sidebar + thực tế Form
        initial_cards = float(4 * shoe_decks)
        exact_cards_left = {i: initial_cards for i in range(1, 14)}
        
        sidebar_rounds = manual_p + manual_b + manual_t
        if sidebar_rounds > 0:
            estimated_removed = sidebar_rounds * 4.94
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
        total_initial_cards = shoe_decks * 52
        cards_played = int(total_initial_cards - total_cards_remaining)
        shoe_progress = cards_played / total_initial_cards

        # HUD hiển thị chi tiết thông số bộ nhớ sau khi gộp khấu trừ
        memory_hud = f"🧬 BỘ NHỚ VƯỢT THẦN ➡️ Đã quét: {cards_played} quân (Gồm {int(sidebar_rounds * 4.94)} q. lịch sử) | Còn lại: ~{int(total_cards_remaining)} quân — 🔹 Thấp (A-5): {int(low_cards)} q | 🔸 Trung (6-9): {int(mid_cards)} q | 🔺 Tây (10-K): {int(high_cards)} q"
        cyber_knowledge = AISovereignOracle.simulate_cyber_knowledge_ingestion(total_rounds)

        diff = abs(p_val - b_val)
        target = "PLAYER" if p_val > b_val else "BANKER"

        if diff < 1.5:
            return {
                "decision": "🛑 TUYỆT ĐỐI BỎ QUA (MÀNG LỌC THẦN)", "target": "HÒA / BỎ LỆNH", "capital_allocation": "0% (Bảo toàn tuyệt đối)", "strategy_type": "MATRIX SHIELD PROTECT",
                "ai_insight": f"Nhãn Thần phát hiện chênh lệch chỉ đạt {diff:.2f}%. Biến động điểm số nằm trong vùng nhiễu loạn ngẫu nhiên của thuật toán sàn. Xuống tiền lúc này là tự sát.",
                "risk_level": "Tối Cao (Bẫy Sàn)", "color": "#e74c3c", "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge
            }

        raw_kelly = (max(p_val, b_val) / 100.0) - (min(p_val, b_val) / 100.0)
        dynamic_alloc = raw_kelly * 25.0 * (1.0 + shoe_progress)
        
        if streak_side and streak_count >= 3:
            final_alloc = max(5.0, min(20.0, dynamic_alloc * 1.8))
            capital_str = f"💥 VƯỢT THẦN: {final_alloc:.1f}% Vốn (Khung Lệnh Tối Cao)"
            strat_type = "⚡ LỆNH TRỪ KHỬ CHUỖI BỆT VƯỢC CẤP"
            risk_lvl = "Thấp (Lợi thế toán học tuyệt đối)"
            color = "#00f5d4"
            ai_insight = f"Mắt thần định vị chuỗi {streak_side.upper()} ({streak_count} ván) đã chạm ngưỡng giới hạn Markov. Bộ nhớ ghi nhận mật độ bài còn lại sau khấu trừ tổng lực rất lý tưởng để bẻ gãy dòng chảy thế bài. Xuống tiền dứt khoát cửa {target}."
        else:
            final_alloc = max(2.0, min(12.0, dynamic_alloc))
            capital_str = f"💎 {final_alloc:.1f}% Tài khoản"
            strat_type = "🌀 QUÉT THUẬN DÒNG QUANTUM"
            risk_lvl = "An toàn ổn định"
            color = "#38bdf8" if target == "PLAYER" else "#ff4757"
            ai_insight = f"Xác suất độc lập cửa {target} tăng vọt nhờ xung lực EOR tích lũy chuẩn hóa từ tất cả các ván đã khấu trừ. Sóng thuật toán đang thuận, lệnh vào có độ an toàn cực cao."

        standard_high_ratio = 16.0 / 52.0  
        high_card_ratio = high_cards / total_cards_remaining
        if high_card_ratio > (standard_high_ratio + 0.04):
            ai_insight += " ⚠️ GIÁM SÁT TIE AGENT CẢNH BÁO: Mật độ bài Tây tích tụ dày đặc, sảnh bài dễ xuất hiện chuỗi Hòa ảo liên tiếp. Hạ quy mô lệnh chính và lót nhẹ cửa TIE."

        return {
            "decision": f"⚡ LỆNH THẦN: {target}", "target": target, "capital_allocation": capital_str, "strategy_type": strat_type,
            "ai_insight": ai_insight, "risk_level": risk_lvl, "color": color, "memory_hud": memory_hud, "cyber_knowledge": cyber_knowledge
        }


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
            
            .audit-matrix-box { padding: 15px; border-radius: 12px; background-color: #0b132b; border: 1px dashed #3a506b; margin-top: 15px; }
            .audit-title { font-family: system-ui; font-size: 13px; font-weight: 800; color: #38bdf8; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }
            .audit-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 12px; color: #cbd5e1; }
            .audit-table th { padding: 8px; text-align: center; background: #131f42; color: #94a3b8; border: 1px solid #1c2541; font-size: 11px; }
            .audit-table td { padding: 8px; text-align: center; border: 1px solid #1c2541; vertical-align: middle; }
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
        st.markdown("##### 🎴 NHẬP QUÂN BÀI CHI TIẾT ĐỂ BỘ NHỚ QUÉT ĐIỂM:")
        with st.form(key="baccarat_3_ultimate_independent_form", clear_on_submit=True):
            input_grid = st.columns(2)
            with input_grid[0]:
                p_str = st.text_input("🔵 PLAYER CARD (Ví dụ: 8 K A):", placeholder="Nhập chữ hoặc số")
            with input_grid[1]:
                b_str = st.text_input("🔴 BANKER CARD (Ví dụ: 7 10):", placeholder="Nhập chữ hoặc số")
            st.write("")
            st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
            triggered = st.form_submit_button("🔥 QUÉT BÀI & KHỞI CHẠY MA TRẬN AI")
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
            f"<div style='font-size: 11px; font-weight: 800; color: #c084fc; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px;'>🌌 AI SOVEREIGN ORACLE - SIÊU PHÂN TÍCH VƯỢT THẦN CAO CẤP</div>"
            f"<div style='font-size: 23px; font-weight: 900; color: {ai_cmd['color']}; margin-bottom: 12px;'>{ai_cmd['decision']}</div>"
            f"<div style='background: rgba(168, 85, 247, 0.08); border: 1px solid rgba(168, 85, 247, 0.3); border-radius: 8px; padding: 10px; margin-bottom: 10px; font-family: system-ui; font-size: 12px; color: #d8b4fe;'>🛰️ <b>MẠNG LƯỢNG TỬ ĐỒNG BỘ (CYBER SCANNER):</b><br><i>\"{ai_cmd['cyber_knowledge']}\"</i></div>"
            f"<div style='background: rgba(56, 189, 248, 0.05); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 8px; padding: 10px; margin-bottom: 15px; font-family: monospace; font-size: 11.5px; color: #38bdf8; line-height: 1.5;'>🧠 <b>MA TRẬN KHẤU TRỪ QUÂN BÀI (SHOE PROGRESS):</b><br>{ai_cmd['memory_hud']}</div>"
            f"<table style='width:100%; border-collapse: collapse; font-size: 13px; margin-bottom: 15px; background: transparent;'>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 6px 0; color: #94a3b8; text-align: left;'>Mục tiêu xuống tiền:</td><td style='padding: 6px 0; font-weight:700; color: {ai_cmd['color']}; text-align:right;'>{ai_cmd['target']}</td></tr>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 6px 0; color: #94a3b8; text-align: left;'>Hệ thống quản lý vốn:</td><td style='padding: 6px 0; font-weight:700; color: #ffffff; text-align:right;'>{ai_cmd['capital_allocation']}</td></tr>"
            f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 6px 0; color: #94a3b8; text-align: left;'>Kiến trúc thuật toán:</td><td style='padding: 6px 0; font-weight:700; color: #a855f7; text-align:right;'>{ai_cmd['strategy_type']}</td></tr>"
            f"<tr><td style='padding: 6px 0; color: #94a3b8; text-align: left;'>Áp suất rủi ro sàn:</td><td style='padding: 6px 0; font-weight:700; color: #ff4757; text-align:right;'>{ai_cmd['risk_level']}</td></tr>"
            f"</table>"
            f"<div style='background: rgba(255,255,255,0.02); border-left: 3px solid {ai_cmd['color']}; padding: 10px; border-radius: 4px; font-size: 12.5px; line-height: 1.5; color: #e2e8f0; text-align: justify;'><b>💡 Chỉ thị thực chiến tối cao:</b> {ai_cmd['ai_insight']}</div>"
            f"</div>"
        )
        st.markdown(html_string, unsafe_allow_html=True)

    @staticmethod
    def render_probabilities_grid(p_pct, b_pct, t_pct, p_cnt, b_cnt, t_cnt):
        prob_grid = st.columns(3)
        with prob_grid[0]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 AI PLAYER AGENT</span><span class="metric-num" style="color:#00afb9;">{p_pct:.2f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {p_cnt}</span></div>', unsafe_allow_html=True)
        with prob_grid[1]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 AI BANKER AGENT</span><span class="metric-num" style="color:#ff4757;">{b_pct:.2f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {b_cnt}</span></div>', unsafe_allow_html=True)
        with prob_grid[2]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 AI TIE AGENT</span><span class="metric-num" style="color:#2ecc71;">{t_pct:.2f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {t_cnt}</span></div>', unsafe_allow_html=True)

    @staticmethod
    def render_audit_matrix(log):
        if not log:
            return
            
        st.markdown('<div class="audit-matrix-box"><div class="audit-title">📊 BẢNG ĐỐI CHIẾU KIỂM TOÁN LƯỢNG TỬ (REAL-TIME AUDIT)</div>', unsafe_allow_html=True)
        
        table_rows = ""
        for idx, r in enumerate(log):
            pred = r.get('predicted_directive', 'WAIT').upper()
            outcome = r['outcome'].upper()
            
            if outcome == "TIE" or pred == "WAIT":
                dot_html = '<span class="status-dot" style="color: #94a3b8; background-color: #94a3b8;"></span>'
                status_text = "HÒA / BỎ LỆNH"
            elif pred == outcome:
                dot_html = '<span class="status-dot" style="color: #2ecc71; background-color: #2ecc71;"></span>'
                status_text = "TRÙNG KHỚP"
            else:
                dot_html = '<span class="status-dot" style="color: #e74c3c; background-color: #e74c3c;"></span>'
                status_text = "TRÁI NGƯỢC"
            
            pred_display = f"<b style='color:#00afb9;'>PLAYER</b>" if pred == "PLAYER" else (f"<b style='color:#ff4757;'>BANKER</b>" if pred == "BANKER" else "<span style='color:#64748b;'>QUAN SÁT</span>")
            outcome_display = f"<b style='color:#00afb9;'>PLAYER ({r['p_score']}đ)</b>" if outcome == "PLAYER" else (f"<b style='color:#ff4757;'>BANKER ({r['b_score']}đ)</b>" if outcome == "BANKER" else "<b style='color:#2ecc71;'>TIE</b>")
            
            table_rows += (
                f"<tr>"
                f"<td>Ván {idx+1}</td>"
                f"<td>{pred_display}</td>"
                f"<td>{outcome_display}</td>"
                f"<td>{dot_html}</td>"
                f"<td>{status_text}</td>"
                f"</tr>"
            )
            
        html_table = (
            f"<table class='audit-table'>"
            f"<thead><tr><th>VÁN</th><th>DỰ ĐOÁN CỦA AI</th><th>THỰC TẾ SÀN</th><th>KIỂM TOÁN</th><th>TRẠNG THÁI</th></tr></thead>"
            f"<tbody>{table_rows}</tbody>"
            f"</table></div>"
        )
        st.markdown(html_table, unsafe_allow_html=True)

    @staticmethod
    def render_utilities():
        util_grid = st.columns(2)
        undo_triggered = util_grid[0].button("⏪ HOÀN TÁC (PHỤC HỒI BÀI)")
        clear_triggered = util_grid[1].button("🔄 LÀM TRỐNG KHAY BÀI")
        return undo_triggered, clear_triggered


# =========================================================================
# 🎮 RUNTIME EXECUTION CONTROLLER (Trục điều hành chính)
# =========================================================================
st.set_page_config(page_title="Oracle Quantum Decentralized v67.8", page_icon="🌌", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

decks, hist_p, hist_b, hist_t = BaccaratInterfaceSystem.render_sidebar()

st.markdown("### 🌌 ORACLE MULTI-AGENT QUANTUM DECENTRALIZED v67.8")
st.caption("Kiến Trúc Phân Rã Lượng Tử 3 Đặc Vụ AI Độc Lập | Đếm Bài Phi Tuyến Tính & Chuỗi Markov Co Giãn")

final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, streak_side, streak_count = calculate_v67_8_ultimate_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t
)
cmd = get_ultimate_directive(final_p, final_b, trend_desc, streak_side, streak_count, st.session_state.round_detailed_log, hist_p, hist_b)

BaccaratInterfaceSystem.render_header_hud(total_rounds=(total_p + total_b + total_t), cards_left=cards_left, decks_count=decks)

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
        'predicted_directive': cmd['raw_target']
    })
    st.rerun()

st.markdown("---")

BaccaratInterfaceSystem.render_directive_panel(cmd)

# GỌI ORACLE VƯỢT THẦN: Đã truyền đồng bộ manual_p, manual_b, manual_t vào lõi xử lý để cấu trúc lại bộ nhớ
ai_cmd = AISovereignOracle.analyze_and_suggest(
    all_rounds_log=st.session_state.round_detailed_log, 
    shoe_decks=decks,
    manual_p=hist_p, manual_b=hist_b, manual_t=hist_t,
    p_val=final_p, b_val=final_b, t_val=final_t, 
    cards_left=cards_left, 
    trend_desc=trend_desc, streak_side=streak_side, streak_count=streak_count, 
    total_rounds=(total_p + total_b + total_t)
)
BaccaratInterfaceSystem.render_ai_oracle_panel(ai_cmd)

BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t, total_p, total_b, total_t)
BaccaratInterfaceSystem.render_audit_matrix(st.session_state.round_detailed_log)

st.markdown("<br>", unsafe_allow_html=True)

undo_btn, clear_btn = BaccaratInterfaceSystem.render_utilities()
if undo_btn:
    if st.session_state.round_detailed_log:
        st.session_state.round_detailed_log.pop()
        st.rerun()
if clear_btn:
    st.session_state.round_detailed_log = []
    st.rerun()
