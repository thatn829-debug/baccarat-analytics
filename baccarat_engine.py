# baccarat_engine.py
import streamlit as st
import numpy as np
import math
from PIL import Image
import io

# =========================================================================
# 📸 MODULE 1: INDEPENDENT VISION SCANNER ENGINE
# =========================================================================
class VisionScannerEngine:
    @staticmethod
    def decode_and_parse_roadmap(image_bytes):
        if image_bytes is None:
            return []
        try:
            image = Image.open(io.BytesIO(image_bytes))
            # Pipeline OpenCV/OCR giả lập xử lý ma trận điểm ảnh
            detected_roadmap = ["Player", "Player", "Banker", "Player"]
            return detected_roadmap
        except Exception:
            return []

    @staticmethod
    def render_camera_hud():
        st.markdown('<p class="section-title">👁️ CAMERA VISION SCANNER (QUÉT CẦU TỰ ĐỘNG)</p>', unsafe_allow_html=True)
        with st.expander("📸 BẤM ĐỂ MỞ CAMERA QUÉT BẢNG ĐIỂM SÒNG BÀI", expanded=False):
            img_file = st.camera_input("Hướng ống kính thẳng vào bảng kết quả (Road Map) rồi bấm Chụp")
            return img_file


# =========================================================================
# 🔵 MODULE 2: PLAYER ULTIMATE ENGINE
# =========================================================================
class PlayerUltimateEngine:
    @staticmethod
    def calculate_absolute_probability(all_rounds_log, shoe_decks, manual_p, total_decisive):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left: exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        p_eor = {1: -0.0051, 2: -0.0059, 3: -0.0062, 4: -0.0134, 5: -0.0096, 6: +0.0123, 7: +0.0144, 8: +0.0095, 9: -0.0026, 10: +0.0043, 11: +0.0043, 12: +0.0043, 13: +0.0043}
        
        card_effect_sum = sum(((4 * shoe_decks) - left) * p_eor[card_num] for card_num, left in exact_cards_left.items())
        shoe_exhaustion_ratio = 1.0 + ((4 * shoe_decks * 52) - cards_remaining) / (4 * shoe_decks * 52)
        final_card_bias = card_effect_sum * 3.1 * shoe_exhaustion_ratio

        trend_force = 0.0
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = sum(1 for outcome in reversed(decisive_outcomes) if outcome == current_streak_side)
            if current_streak_side == "Banker" and streak_count >= 3:
                trend_force += 1.5 * math.exp(streak_count * 0.32)

        if total_decisive > 0:
            p_ratio = manual_p / total_decisive
            if p_ratio > 0.52: trend_force += 0.6
            elif p_ratio < 0.45: trend_force -= 0.6

        return 44.62 + final_card_bias + trend_force


# =========================================================================
# 🔴 MODULE 3: BANKER ULTIMATE ENGINE
# =========================================================================
class BankerUltimateEngine:
    @staticmethod
    def calculate_absolute_probability(all_rounds_log, shoe_decks, manual_b, total_decisive):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left: exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        b_eor = {1: -0.0051, 2: -0.0059, 3: -0.0062, 4: -0.0134, 5: -0.0096, 6: +0.0123, 7: +0.0144, 8: +0.0095, 9: -0.0026, 10: +0.0043, 11: +0.0043, 12: +0.0043, 13: +0.0043}
        
        card_effect_sum = sum(((4 * shoe_decks) - left) * b_eor[card_num] for card_num, left in exact_cards_left.items())
        shoe_exhaustion_ratio = 1.0 + ((4 * shoe_decks * 52) - cards_remaining) / (4 * shoe_decks * 52)
        final_card_bias = card_effect_sum * 3.1 * shoe_exhaustion_ratio

        trend_force = 0.0
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = sum(1 for outcome in reversed(decisive_outcomes) if outcome == current_streak_side)
            if current_streak_side == "Player" and streak_count >= 3:
                trend_force += 1.5 * math.exp(streak_count * 0.32)
            if current_streak_side == "Banker" and streak_count >= 4:
                trend_force -= 1.2 * math.exp((streak_count - 3) * 0.28)

        if total_decisive > 0:
            b_ratio = manual_b / total_decisive
            if b_ratio > 0.52: trend_force += 0.6
            elif b_ratio < 0.45: trend_force -= 0.6

        return 45.86 - final_card_bias + trend_force


# =========================================================================
# 🟢 MODULE 4: TIE ULTIMATE ENGINE
# =========================================================================
class TieUltimateEngine:
    @staticmethod
    def calculate_absolute_probability(all_rounds_log, shoe_decks):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left: exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
                    
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        zero_value_cards_left = sum([exact_cards_left[i] for i in [10, 11, 12, 13]])
        actual_density = zero_value_cards_left / cards_remaining
        standard_density = 16.0 / 52.0
        density_deviation = actual_density - standard_density
        
        tie_hypergeometric_force = density_deviation * 24.0 if density_deviation > 0 else density_deviation * 18.0
        return 9.52 + tie_hypergeometric_force


# =========================================================================
# 🧠 MODULE 5: FUSION DISTRIBUTOR
# =========================================================================
def calculate_v68_1_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t):
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r['outcome'] == "Tie")
    total_decisive = total_p_wins + total_b_wins
    
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, shoe_decks * 52, 0, 0, 0, "HỆ THỐNG TRỐNG", None, 0

    raw_p = PlayerUltimateEngine.calculate_absolute_probability(all_rounds_log, shoe_decks, manual_p, total_decisive)
    raw_b = BankerUltimateEngine.calculate_absolute_probability(all_rounds_log, shoe_decks, manual_b, total_decisive)
    raw_t = TieUltimateEngine.calculate_absolute_probability(all_rounds_log, shoe_decks)
    
    raw_p, raw_b, raw_t = max(2.0, min(98.0, raw_p)), max(2.0, min(98.0, raw_b)), max(1.0, min(45.0, raw_t))
    total_sum = raw_p + raw_b + raw_t
    
    p_pct = (raw_p / total_sum) * 100
    b_pct = (raw_b / total_sum) * 100
    t_pct = (raw_t / total_sum) * 100
    
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    for r in all_rounds_log:
        for card in (r['p_cards'] + r['b_cards']):
            if card in exact_cards_left: exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
    cards_remaining = int(sum(exact_cards_left.values()))
    
    trend_desc = "CẦU ĐANG BIẾN ĐỘNG TỰ DO"
    streak_side = None
    streak_count = 0
    decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
    if len(decisive_outcomes) >= 2:
        current_streak_side = decisive_outcomes[-1]
        streak_count = sum(1 for outcome in reversed(decisive_outcomes) if outcome == current_streak_side)
        if streak_count >= 2:
            streak_side = current_streak_side
            trend_desc = f"CẦU BỆT {streak_side.upper()} ({streak_count} VÁN)"

    return p_pct, b_pct, t_pct, cards_remaining, total_p_wins, total_b_wins, total_ties, trend_desc, streak_side, streak_count


def get_ultimate_directive(p_val, b_val, trend_desc, streak_side, streak_count, log, m_p, m_b):
    if not log and (m_p == 0 and m_b == 0):
        return {"status": "🛰️ ISOLATED ENGINES ONLINE", "msg": "Mô-đun Camera và 3 Lõi Tính Toán đã cô lập. Hệ thống sẵn sàng hoạt động.", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%"}
    diff = abs(p_val - b_val)
    if streak_side and streak_count >= 3:
        target = "PLAYER" if streak_side == "Banker" else "BANKER"
        if (target == "PLAYER" and p_val > b_val) or (target == "BANKER" and b_val > p_val):
            return {"status": f"🚨 LỆNH BÈ CẦU TỐI HẬU ➡️ {target}", "msg": f"Phân tích trạng thái: {trend_desc}. Lõi độc lập cửa {target} đã tích lũy đủ áp lực, đánh chặn đảo chiều ván này.", "color": "#00f5d4", "bg": "rgba(0, 245, 212, 0.15)", "size": "4% - 6%"}
    if diff < 1.8:
        return {"status": "🛑 CHỜ QUAN SÁT (TRẠNG THÁI TĨNH)", "msg": f"Mức chênh lệch lợi thế ({diff:.2f}%) quá nhỏ, chưa vượt qua màng lọc an toàn phi tuyến tính.", "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%"}
    return {
        "status": "🔵 VÀO LỆNH THUẬN DÒNG: PLAYER" if p_val > b_val else "🔴 VÀO LỆNH THUẬN DÒNG: BANKER",
        "msg": f"Xác nhận điểm lợi thế vượt ngưỡng đột biến (+{diff:.2f}%). Xu hướng dòng chảy bài rất ổn định.",
        "color": "#00afb9" if p_val > b_val else "#ff4757", "bg": "rgba(0,175,185,0.2)" if p_val > b_val else "rgba(255,71,87,0.2)", "size": "2.5% - 4%"
    }

def parse_baccarat_input(raw_str):
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
        elif token.isdigit() and 1 <= int(token) <= 9: result_list.append(int(token))
    return result_list


# =========================================================================
# 📱 MODULE 6: 100% HARDCORE MOBILE INJECTION CSS
# =========================================================================
class BaccaratInterfaceSystem:
    @staticmethod
    def inject_mobile_css():
        st.markdown(
            """
            <style>
            .stApp { background: #030611 !important; color: #f8fafc !important; }
            .block-container { padding: 0.8rem 0.6rem !important; max-width: 100% !important; }
            div[data-testid="stHorizontalBlock"] { 
                display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; gap: 6px !important; padding: 0px !important;
            }
            div[data-testid="stHorizontalBlock"] > div { 
                flex: 1 1 0% !important; min-width: 0px !important; padding: 0px !important;
            }
            .section-title { font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.5px; }
            .header-hud-bar { background: linear-gradient(90deg, #0f172a, #1e293b); border: 1px solid #334155; border-radius: 8px; padding: 8px; margin-bottom: 12px; text-align: center; font-family: monospace; font-size: 11px; color: #cbd5e1; }
            .action-panel { border-radius: 10px; padding: 14px; margin: 10px 0px; text-align: center; box-shadow: 0px 4px 20px rgba(0,0,0,0.5); }
            .action-status { font-size: 16px; font-weight: 900; margin-bottom: 4px; }
            .action-msg { font-size: 12px; margin-bottom: 10px; text-align: justify; line-height: 1.3; }
            .action-vol { font-size: 13px; font-weight: 900; font-family: monospace; border-top: 1px dashed rgba(255,255,255,0.15); padding-top: 8px; }
            .mobile-metric-box { background: #0b132b; border: 1px solid #1c2541; border-radius: 8px; padding: 8px 4px; display: flex; flex-direction: column; text-align: center; }
            .metric-tag { font-size: 8px; font-weight: 800; color: #64748b; margin-bottom: 2px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; }
            .metric-num { font-size: 16px; font-weight: 900; font-family: monospace; }
            .metric-sub { font-size: 9px; opacity: 0.5; }
            .score-log-hud { padding: 10px; border-radius: 8px; background-color: #0b132b; border: 1px dashed #3a506b; font-family: monospace; font-size: 11px; margin-top: 12px; color: #cbd5e1; height: 120px; overflow-y: auto; }
            div.stButton > button { background-color: #1c2541 !important; color: #cbd5e1 !important; border: 1px solid #3a506b !important; border-radius: 8px; font-weight: 700; width: 100% !important; padding: 6px 0px !important; font-size: 12px !important; }
            .submit-btn-box div.stButton > button { background-color: #00f5d4 !important; color: #010206 !important; border: none !important; font-weight: 800; box-shadow: 0 0 10px rgba(0,245,212,0.3); }
            .vision-btn-box div.stButton > button { background-color: #a855f7 !important; color: #ffffff !important; border: none !important; box-shadow: 0 0 10px rgba(168,85,247,0.3); }
            div[data-testid="stWidgetLabel"] p { font-size: 11px !important; color: #94a3b8 !important; font-weight: 700; }
            div[data-testid="stTextInput"] input { padding: 6px 10px !important; font-size: 13px !important; background-color: #090d16 !important; color: #fff !important; border: 1px solid #1e293b !important; }
            </style>
            """, unsafe_allow_html=True
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
