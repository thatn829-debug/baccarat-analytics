import streamlit as st
import numpy as np
import math

# =========================================================================
# ⚙️ MODULE 1: CARD COUNTING ANALYTICS CORE (Lõi đếm bài phi tuyến tính)
# =========================================================================
class CardCountingEngine:
    @staticmethod
    def get_remaining_cards(all_rounds_log, shoe_decks):
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        return exact_cards_left

    @staticmethod
    def calculate_eor_bias(exact_cards_left, shoe_decks):
        counting_effect = {
            1: -0.0050, 2: -0.0058, 3: -0.0060, 4: -0.0132, 5: -0.0094, 
            6: +0.0120, 7: +0.0140, 8: +0.0092,                        
            9: -0.0025, 10: +0.0042, 11: +0.0042, 12: +0.0042, 13: +0.0042
        }
        total_bias = 0.0
        for card_num, left in exact_cards_left.items():
            cards_removed = (4 * shoe_decks) - left
            total_bias += cards_removed * counting_effect[card_num]
        return total_bias


# =========================================================================
# 📊 MODULE 2: MARKOV TREND MATRIX ENGINE (Ma trận xu hướng & Tỷ lệ lịch sử)
# =========================================================================
class TrendMatrixEngine:
    @staticmethod
    def evaluate_road_bias(total_p_wins, total_b_wins):
        total_decisive = total_p_wins + total_b_wins
        if total_decisive <= 0:
            return 0.0
        p_win_rate = total_p_wins / total_decisive
        if p_win_rate > 0.53: return 1.8
        if p_win_rate < 0.47: return -1.8
        return 0.0


# =========================================================================
# 🚨 MODULE 3: DYNAMIC TREND BREAK DETECTOR (Mô-đun định vị & Bẻ cầu siêu nhạy)
# =========================================================================
class TrendBreakDetector:
    @staticmethod
    def analyze_trend_state(all_rounds_log):
        if len(all_rounds_log) < 2:
            return "CHƯA ĐỦ DỮ LIỆU ĐỊNH VỊ CẦU", None, 0

        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        
        if len(decisive_outcomes) < 2:
            return "ĐANG TÍCH LŨY CẦU NỀN", None, 0

        is_pingpong = True
        for i in range(1, min(5, len(decisive_outcomes))):
            if decisive_outcomes[-i] == decisive_outcomes[-(i+1)]:
                is_pingpong = False
                break
        if is_pingpong and len(decisive_outcomes) >= 3:
            return "CẦU NHẢY 1-1 (PING-PONG) ĐANG CHẠY", None, 0

        current_streak_side = decisive_outcomes[-1]
        current_streak_count = 0
        for outcome in reversed(decisive_outcomes):
            if outcome == current_streak_side:
                current_streak_count += 1
            else:
                break

        if current_streak_count >= 2:
            side_symbol = "🔵 PLAYER" if current_streak_side == "Player" else "🔴 BANKER"
            return f"CẦU BỆT {side_symbol} ({current_streak_count} VÁN)", current_streak_side, current_streak_count
        
        return "CẦU ĐANG BIẾN ĐỘNG TỰ DO", None, 0

    @staticmethod
    def calculate_break_force(streak_side, streak_count, total_decisive):
        if not streak_side or streak_count < 3:
            return 0.0, False

        fib_scale = {3: 2.5, 4: 5.5, 5: 7.5, 6: 10.5, 7: 14.0}
        base_force = fib_scale.get(streak_count, 18.0 + (streak_count - 7) * 4.5)

        entropy_multiplier = 1.0 + min(0.6, total_decisive / 40.0)
        final_break_bias = base_force * entropy_multiplier

        if streak_side == "Banker":
            return final_break_bias, True   
        else:
            return -final_break_bias, True  


# =========================================================================
# 🧠 MODULE 4: FUSION PREDICTION CORE (Bộ hội tụ dữ liệu & Tính toán xác suất)
# =========================================================================
def calculate_v67_3_ultimate_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t):
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r['outcome'] == "Tie")
    total_decisive = total_p_wins + total_b_wins
    
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, shoe_decks * 52, 0, 0, 0, False, None, 0, "HỆ THỐNG TRỐNG"

    cards_left_dict = CardCountingEngine.get_remaining_cards(all_rounds_log, shoe_decks)
    cards_remaining = max(1.0, sum(cards_left_dict.values()))
    eor_bias = CardCountingEngine.calculate_eor_bias(cards_left_dict, shoe_decks)
    
    road_bias = TrendMatrixEngine.evaluate_road_bias(total_p_wins, total_b_wins)
    
    trend_desc, streak_side, streak_count = TrendBreakDetector.analyze_trend_state(all_rounds_log)
    break_bias, is_critical = TrendBreakDetector.calculate_break_force(streak_side, streak_count, total_decisive)
    
    p_0 = sum([cards_left_dict[i] for i in [10, 11, 12, 13]]) / cards_remaining

    base_p = 44.62 + (eor_bias * 2.6) + road_bias + break_bias
    base_b = 45.86 - (eor_bias * 2.6) - road_bias - break_bias
    base_t = 9.52 + (p_0 * 3.2)

    base_p = max(20.0, min(80.0, base_p))
    base_b = max(20.0, min(80.0, base_b))
    base_t = max(4.0, min(22.0, base_t))
    
    total_sum = base_p + base_b + base_t
    return (base_p / total_sum) * 100, (base_b / total_sum) * 100, (base_t / total_sum) * 100, int(cards_remaining), total_p_wins, total_b_wins, total_ties, is_critical, streak_side, streak_count, trend_desc


# =========================================================================
# 🛰️ MODULE 5: DECISION ADAPTIVE CORTEX (Bộ chỉ huy và phát lệnh)
# =========================================================================
def get_ultimate_directive(p_val, b_val, is_critical, streak_side, streak_count, trend_desc, log, m_p, m_b):
    if not log and (m_p == 0 and m_b == 0):
        return {
            "status": "🛰️ SYSTEM ZERO-START READY",
            "msg": "Vui lòng cấu hình dữ liệu ở thanh Sidebar trái hoặc tiến hành nhập quân bài trực tiếp để kích hoạt lõi phân tích.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%"
        }
    
    diff = abs(p_val - b_val)
    
    if is_critical and streak_side and streak_count >= 3:
        target = "PLAYER" if streak_side == "Banker" else "BANKER"
        urgency = "⚠️ ĐIỂM SỚM (VÁN 3)" if streak_count == 3 else f"🚨 TỚI HẠN (VÁN {streak_count})"
        return {
            "status": f"{urgency} BẺ CẦU ➡️ {target}",
            "msg": f"Định vị hiện tại: {trend_desc}. Mô-đun Bẻ Cầu phát hiện áp lực Entropy suy giảm đạt ngưỡng cảnh giới. Thuật toán phát tín hiệu tấn công đảo chiều cửa {target}.",
            "color": "#06d6a0", "bg": "rgba(6, 214, 160, 0.2)", "size": "3% - 5% (Siêu nhạy)"
        }
        
    matrix_threshold = 1.2
    if diff < matrix_threshold:
        return {
            "status": "🛑 CHỜ (WAIT) - GIẰNG CO",
            "msg": f"Trạng thái: {trend_desc}. Biên độ lợi thế hai cửa đang tiệm cận mức cân bằng ({diff:.2f}%). Tạm thời không vào lệnh.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 VÀO LỆNH: PLAYER",
            "msg": f"Trạng thái: {trend_desc}. Tổ hợp dữ liệu đếm bài phối hợp dòng chảy xu hướng ủng hộ Player vượt màng lọc an toàn (+{diff:.2f}%).",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "2% - 3%"
        }
    else:
        return {
            "status": "🔴 VÀO LỆNH: BANKER",
            "msg": f"Trạng thái: {trend_desc}. Ma trận toán học xác nhận lợi thế dòng chảy tự nhiên của khay bài đang nghiêng mạnh về phía Banker (+{diff:.2f}%).",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "2% - 3%"
        }

def parse_baccarat_input_v67_3(raw_str):
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
# 📱 MODULE 6: BACCARAT INTERFACE SYSTEM (Giao diện lưới độc lập tách rời)
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
            
            .header-hud-bar { background: linear-gradient(90deg, #0f172a, #1e293b); border: 1px solid #334155; border-radius: 10px; padding: 10px; margin: 10px 0px 20px 0px; text-align: center; font-family: monospace; font-size: 13px; color: #cbd5e1; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
            
            .action-panel { border-radius: 14px; padding: 20px; margin: 15px 0px; text-align: center; box-shadow: 0px 5px 25px rgba(0,0,0,0.8); }
            .action-status { font-size: 21px; font-weight: 900; letter-spacing: 0.5px; margin-bottom: 6px; }
            .action-msg { font-size: 13.5px; opacity: 0.9; margin-bottom: 12px; line-height: 1.4; text-align: justify; }
            .action-vol { font-size: 16px; font-weight: 900; font-family: monospace; border-top: 1px dashed rgba(255,255,255,0.2); padding-top: 10px; }
            
            .mobile-metric-box { background: #0b132b; border: 1px solid #1c2541; border-radius: 10px; padding: 12px 6px; margin-bottom: 5px; display: flex; flex-direction: column; text-align: center; justify-content: center; }
            .metric-tag { font-size: 10.5px; font-weight: 800; color: #64748b; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 0.5px; }
            .metric-num { font-size: 19px; font-weight: 900; font-family: monospace; }
            
            .score-log-hud { padding: 12px; border-radius: 10px; background-color: #0b132b; border: 1px dashed #3a506b; margin-top: 12px; font-family: monospace; font-size: 12px; color: #cbd5e1; }
            
            div.stButton > button { background-color: #1c2541 !important; color: #cbd5e1 !important; border: 1px solid #3a506b !important; border-radius: 10px; font-weight: 800; width: 100% !important; padding: 12px 0px !important; font-size: 14px !important; }
            div.stButton > button:hover { background-color: #3a506b !important; color: #ffffff !important; }
            
            .submit-btn-box div.stButton > button { background-color: #00f5d4 !important; color: #010206 !important; border: none !important; box-shadow: 0 0 15px rgba(0,245,212,0.4); }
            .submit-btn-box div.stButton > button:hover { background-color: #57ffeb !important; }
            
            div[data-testid="stNumberInput"] label { font-size: 11px !important; color: #cbd5e1 !important; }
            .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
            </style>
            """, 
            unsafe_allow_html=True
        )

    @staticmethod
    def render_sidebar():
        st.sidebar.markdown("### ⚙️ CẤU HÌNH HỆ THỐNG")
        decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 LỊCH SỬ BẢNG ĐIỂM SÒNG BÀI")
        hist_p = st.sidebar.number_input("🔵 PLAYER WINS:", min_value=0, value=0, step=1)
        hist_b = st.sidebar.number_input("🔴 BANKER WINS:", min_value=0, value=0, step=1)
        hist_t = st.sidebar.number_input("🟢 TIE WINS:", min_value=0, value=0, step=1)
        return decks, hist_p, hist_b, hist_t

    @staticmethod
    def render_header_hud(total_rounds, cards_left, decks_count):
        st.markdown(
            f'<div class="header-hud-bar">'
            f'🎰 TỔNG SỐ VÁN ĐÃ CHẠY: <b>{total_rounds}</b> ván &nbsp;|&nbsp; '
            f'🎴 QUÂN BÀI CÒN LẠI TRONG KHAY: <b>{cards_left}</b> / {decks_count * 52}'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_input_form():
        st.markdown("##### 🎴 NHẬP QUÂN BÀI CHI TIẾT HIỆN TẠI:")
        with st.form(key="baccarat_modular_interface_form", clear_on_submit=True):
            input_grid = st.columns(2)
            with input_grid[0]:
                p_str = st.text_input("🔵 PLAYER CARD:", placeholder="Ví dụ: 8 K 2")
            with input_grid[1]:
                b_str = st.text_input("🔴 BANKER CARD:", placeholder="Ví dụ: 7 J")
            st.write("")
            st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
            triggered = st.form_submit_button("🔥 PHÂN TÍCH THỜI GIAN THỰC")
            st.markdown('</div>', unsafe_allow_html=True)
        return triggered, p_str, b_str

    @staticmethod
    def render_directive_panel(cmd):
        st.markdown(
            f'<div class="action-panel" style="background-color: {cmd["bg"]}; border: 2px solid {cmd["color"]}; color: {cmd["color"]};">'
            f'<div class="action-status">{cmd["status"]}</div>'
            f'<div class="action-msg" style="color: #f1f5f9;">{cmd["msg"]}</div>'
            f'<div class="action-vol">MỨC CƯỢC ĐỀ XUẤT: {cmd["size"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_probabilities_grid(p_pct, b_pct, t_pct, p_cnt, b_cnt, t_cnt):
        prob_grid = st.columns(3)
        with prob_grid[0]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER TOTAL</span><span class="metric-num" style="color:#00afb9;">{p_pct:.1f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {p_cnt}</span></div>', unsafe_allow_html=True)
        with prob_grid[1]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER TOTAL</span><span class="metric-num" style="color:#ff4757;">{b_pct:.1f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {b_cnt}</span></div>', unsafe_allow_html=True)
        with prob_grid[2]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE TOTAL</span><span class="metric-num" style="color:#2ecc71;">{t_pct:.1f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {t_cnt}</span></div>', unsafe_allow_html=True)

    @staticmethod
    def render_history_hud(log):
        if log:
            st.markdown('<div class="score-log-hud"><b>📊 LỊCH SỬ QUÂN BÀI ĐÃ NẠP QUA APP:</b><br>', unsafe_allow_html=True)
            for idx, r in enumerate(log):
                st.markdown(f"• Ván {idx+1}: [P] {r['p_score']}đ vs {r['b_score']}đ [B] ➡️ **{r['outcome'].upper()}**")
            st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def render_utilities():
        util_grid = st.columns(2)
        undo_triggered = util_grid[0].button("⏪ HOÀN TÁC BÀI")
        clear_triggered = util_grid[1].button("🔄 LÀM TRỐNG TOÀN BỘ")
        return undo_triggered, clear_triggered


# =========================================================================
# 🎮 RUNTIME EXECUTION CONTROLLER (Lõi điều hướng ứng dụng chính)
# =========================================================================
st.set_page_config(page_title="Oracle Pure Modular v67.3", page_icon="⚡", layout="centered")

# Khởi chạy nạp giao diện CSS tách biệt
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

# Vẽ Sidebar và lấy tham số cấu hình bài
decks, hist_p, hist_b, hist_t = BaccaratInterfaceSystem.render_sidebar()

st.markdown("### ⚡ ORACLE TREND TRACKING v67.3")
st.caption("Kiến trúc Module hóa hoàn chỉnh | Giao diện và Thuật toán tách rời độc lập.")

# Thực hiện tính toán toán học nền tảng trước để lấy dữ liệu cấp cho HUD đầu trang
final_p, final_b, final_t, cards_left, total_p, total_b, total_t, is_critical, streak_side, streak_count, trend_desc = calculate_v67_3_ultimate_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t
)
cmd = get_ultimate_directive(final_p, final_b, is_critical, streak_side, streak_count, trend_desc, st.session_state.round_detailed_log, hist_p, hist_b)

# Vẽ HUD hiển thị tổng số ván đầu trang
BaccaratInterfaceSystem.render_header_hud(total_rounds=(total_p + total_b + total_t), cards_left=cards_left, decks_count=decks)

# Vẽ Biểu mẫu nhập quân bài đầu vào
calc_triggered, p_input, b_input = BaccaratInterfaceSystem.render_input_form()

if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v67_3(p_input.strip())
    b_list = parse_baccarat_input_v67_3(b_input.strip())
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    st.session_state.round_detailed_log.append({'p_cards': p_list, 'b_cards': b_list, 'p_score': p_score, 'b_score': b_score, 'outcome': outcome})
    st.rerun()

st.markdown("---")

# Vẽ Bảng chỉ thị hành động chiến thuật
BaccaratInterfaceSystem.render_directive_panel(cmd)

# Vẽ Lưới hiển thị 3 phần trăm xác suất đối xứng Mobile
BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t, total_p, total_b, total_t)

# Vẽ Log lịch sử nạp quân bài chi tiết
BaccaratInterfaceSystem.render_history_hud(st.session_state.round_detailed_log)

st.markdown("<br>", unsafe_allow_html=True)

# Vẽ các nút Tiện ích cuối màn hình (Hoàn tác / Làm trống) và xử lý Logic State
undo_btn, clear_btn = BaccaratInterfaceSystem.render_utilities()
if undo_btn:
    if st.session_state.round_detailed_log:
        st.session_state.round_detailed_log.pop()
        st.rerun()
if clear_btn:
    st.session_state.round_detailed_log = []
    st.rerun()
