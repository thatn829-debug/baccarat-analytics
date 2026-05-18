import streamlit as st
import numpy as np
import math

# =========================================================================
# 🔵 MODULE 1: PLAYER SOVEREIGN ENGINE (Lõi tính toán riêng biệt cho Player)
# =========================================================================
class PlayerProbabilityEngine:
    @staticmethod
    def calculate_raw_probability(all_rounds_log, shoe_decks, manual_p, total_decisive):
        """Chỉ tính toán và trả về trọng số xác suất thô của cửa Player"""
        # 1. Trích xuất mật độ bài đếm phục vụ Player (Bài nhỏ 1-5 có lợi cho Player)
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        
        # Tính EOR ảnh hưởng trực tiếp đến Player
        player_eor_effect = {1: -0.0050, 2: -0.0058, 3: -0.0060, 4: -0.0132, 5: -0.0094, 6: 0.0120, 7: 0.0140, 8: 0.0092, 9: -0.0025, 10: 0.0042, 11: 0.0042, 12: 0.0042, 13: 0.0042}
        player_card_bias = 0.0
        for card_num, left in exact_cards_left.items():
            cards_removed = (4 * shoe_decks) - left
            player_card_bias += cards_removed * player_eor_effect[card_num]

        # 2. Phân tích chuỗi bệt / xu hướng của riêng Player
        player_trend_bias = 0.0
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        
        if decisive_outcomes:
            # Kiểm tra áp lực bẻ cầu nếu Banker đang bệt (Giúp tăng xác suất Player lên)
            current_streak_side = decisive_outcomes[-1]
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
            
            if current_streak_side == "Banker" and streak_count >= 3:
                step_scale = {3: 1.8, 4: 3.5, 5: 5.5, 6: 8.0}
                player_trend_bias += step_scale.get(streak_count, 10.0)

        # 3. Tính toán tỷ lệ sàn dài hạn cho Player
        if total_decisive > 0 and (manual_p / total_decisive) > 0.53:
            player_trend_bias += 0.5

        # Trả về điểm nền móng Player (Xác suất toán học chuẩn gốc: 44.62)
        return 44.62 + (player_card_bias * 3.0) + player_trend_bias


# =========================================================================
# 🔴 MODULE 2: BANKER SOVEREIGN ENGINE (Lõi tính toán riêng biệt cho Banker)
# =========================================================================
class BankerProbabilityEngine:
    @staticmethod
    def calculate_raw_probability(all_rounds_log, shoe_decks, manual_b, total_decisive):
        """Chỉ tính toán và trả về trọng số xác suất thô của cửa Banker"""
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        
        # Tính EOR ảnh hưởng ngược chiều đối với Banker
        banker_eor_effect = {1: -0.0050, 2: -0.0058, 3: -0.0060, 4: -0.0132, 5: -0.0094, 6: 0.0120, 7: 0.0140, 8: 0.0092, 9: -0.0025, 10: 0.0042, 11: 0.0042, 12: 0.0042, 13: 0.0042}
        banker_card_bias = 0.0
        for card_num, left in exact_cards_left.items():
            cards_removed = (4 * shoe_decks) - left
            banker_card_bias += cards_removed * banker_eor_effect[card_num]

        # Phân tích chuỗi bệt / xu hướng tác động lên riêng Banker
        banker_trend_bias = 0.0
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        
        if decisive_outcomes:
            # Kiểm tra áp lực bẻ cầu nếu Player đang bệt (Giúp tăng xác suất Banker lên)
            current_streak_side = decisive_outcomes[-1]
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
            
            if current_streak_side == "Player" and streak_count >= 3:
                step_scale = {3: 1.8, 4: 3.5, 5: 5.5, 6: 8.0}
                banker_trend_bias += step_scale.get(streak_count, 10.0)

        if total_decisive > 0 and (manual_b / total_decisive) > 0.53:
            banker_trend_bias += 0.5

        # Trả về điểm nền móng Banker (Xác suất toán học chuẩn gốc: 45.86)
        return 45.86 - (banker_card_bias * 3.0) + banker_trend_bias


# =========================================================================
# 🟢 MODULE 3: TIE SOVEREIGN ENGINE (Lõi tính toán riêng biệt cho Hòa)
# =========================================================================
class TieProbabilityEngine:
    @staticmethod
    def calculate_raw_probability(all_rounds_log, shoe_decks):
        """Chỉ chịu trách nhiệm tính toán xác suất độc lập cho cửa Hòa (Tie)"""
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
                    
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        # Cửa hòa phụ thuộc cực lớn vào mật độ quân bài có giá trị 0 nút (10, J, Q, K) còn lại
        tie_cards_left = sum([exact_cards_left[i] for i in [10, 11, 12, 13]])
        
        p_0 = tie_cards_left / cards_remaining
        
        # Trả về điểm nền móng cửa Hòa (Xác suất toán học chuẩn gốc: 9.52)
        return 9.52 + (p_0 * 3.5)


# =========================================================================
# 🧠 MODULE 4: FUSION DISTRIBUTOR (Bộ chuẩn hóa & Điều phối dữ liệu)
# =========================================================================
def calculate_v67_7_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t):
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r['outcome'] == "Tie")
    total_decisive = total_p_wins + total_b_wins
    
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, shoe_decks * 52, 0, 0, 0, "HỆ THỐNG TRỐNG", None, 0

    # Gọi 3 mô-đun chạy độc lập tính toán 3 cửa riêng biệt
    raw_p = PlayerProbabilityEngine.calculate_raw_probability(all_rounds_log, shoe_decks, manual_p, total_decisive)
    raw_b = BankerProbabilityEngine.calculate_raw_probability(all_rounds_log, shoe_decks, manual_b, total_decisive)
    raw_t = TieProbabilityEngine.calculate_raw_probability(all_rounds_log, shoe_decks)
    
    # Ép biên an toàn cho từng mô-đun
    raw_p = max(5.0, min(95.0, raw_p))
    raw_b = max(5.0, min(95.0, raw_b))
    raw_t = max(2.0, min(35.0, raw_t))
    
    # Chuẩn hóa tổng xác suất về định dạng 100% (Normalizing vector)
    total_sum = raw_p + raw_b + raw_t
    p_pct = (raw_p / total_sum) * 100
    b_pct = (raw_b / total_sum) * 100
    t_pct = (raw_t / total_sum) * 100
    
    # Tính toán thông số phụ hiển thị HUD giao diện
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    for r in all_rounds_log:
        for card in (r['p_cards'] + r['b_cards']):
            if card in exact_cards_left: exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
    cards_remaining = int(sum(exact_cards_left.values()))
    
    # Phát hiện trạng thái cầu phục vụ hiển thị văn bản HUD
    trend_desc = "CẦU BIẾN ĐỘNG TỰ DO"
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


# =========================================================================
# 🛰️ MODULE 5: DECISION ADAPTIVE CORTEX (Bộ phát lệnh hành động)
# =========================================================================
def get_ultimate_directive(p_val, b_val, trend_desc, streak_side, streak_count, log, m_p, m_b):
    if not log and (m_p == 0 and m_b == 0):
        return {
            "status": "🛰️ TRIPLE ENGINES READY",
            "msg": "Hệ thống 3 Mô-đun cửa độc lập đã kích hoạt hoàn chỉnh. Hãy nạp bài để so khớp xác suất.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%"
        }
    
    diff = abs(p_val - b_val)
    
    # Phát hiện điều kiện kích hoạt bẻ cầu từ dữ liệu độc lập của 3 cửa
    if streak_side and streak_count >= 3:
        target = "PLAYER" if streak_side == "Banker" else "BANKER"
        return {
            "status": f"🚨 TÍN HIỆU BÈ CẦU CỬA {target}",
            "msg": f"Phân tích trạng thái: {trend_desc}. Mô-đun cửa đối diện ghi nhận điểm số lợi thế tích lũy đột biến. Đề xuất đánh chặn đảo chiều.",
            "color": "#00f5d4", "bg": "rgba(0, 245, 212, 0.15)", "size": "3% - 5%"
        }
        
    if diff < 1.5:
        return {
            "status": "🛑 CHỜ XU HƯỚNG CÂN BẰNG",
            "msg": "Xác suất tính toán độc lập giữa Player và Banker đang giằng co nghẹt thở dưới màng lọc an toàn. Không vào lệnh.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 VÀO LỆNH: PLAYER",
            "msg": f"Mô-đun PlayerProbabilityEngine chấm điểm vượt trội so với Banker (+{diff:.2f}%). Vào lệnh thuận xu hướng bài.",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "2% - 3%"
        }
    else:
        return {
            "status": "🔴 VÀO LỆNH: BANKER",
            "msg": f"Mô-đun BankerProbabilityEngine chấm điểm vượt trội so với Player (+{diff:.2f}%). Vào lệnh thuận xu hướng bài.",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "2% - 3%"
        }

def parse_baccarat_input_v67_7(raw_str):
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
# 📱 MODULE 6: GIAO DIỆN STREAMLIT ĐỘC LẬP HOÀN TOÀN
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
            .score-log-hud { padding: 12px; border-radius: 10px; background-color: #0b132b; border: 1px dashed #3a506b; margin-top: 12px; font-family: monospace; font-size: 12px; color: #cbd5e1; }
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
            f'🎴 QUÂN BÀI CÒN LẠI TRONG KHAY BÀI: <b>{cards_left}</b> / {decks_count * 52}'
            f'</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_input_form():
        st.markdown("##### 🎴 NHẬP QUÂN BÀI CHI TIẾT HIỆN TẠI:")
        with st.form(key="baccarat_3_independent_modular_form", clear_on_submit=True):
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
            st.markdown('<div class="score-log-hud"><b>📊 LỊCH SỬ GHI NHỚ QUÂN BÀI QUA APP:</b><br>', unsafe_allow_html=True)
            for idx, r in enumerate(log):
                st.markdown(f"• Ván {idx+1}: [P] {r['p_score']}đ vs {r['b_score']}đ [B] ➡️ **{r['outcome'].upper()}**")
            st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def render_utilities():
        util_grid = st.columns(2)
        undo_triggered = util_grid[0].button("⏪ HOÀN TÁC BÀI")
        clear_triggered = util_grid[1].button("🔄 LÀM TRỐNG KHAY BÀI")
        return undo_triggered, clear_triggered


# =========================================================================
# 🎮 RUNTIME EXECUTION CONTROLLER
# =========================================================================
st.set_page_config(page_title="Oracle Triple Sovereign v67.7", page_icon="⚡", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

decks, hist_p, hist_b, hist_t = BaccaratInterfaceSystem.render_sidebar()

st.markdown("### ⚡ ORACLE TREND TRACKING v67.7")
st.caption("Kiến Trúc 3 Mô-đun Cửa Độc Lập Tuyệt Đối (`Player` | `Banker` | `Tie`)")

# Gọi xử lý điều phối từ 3 mô-đun cửa riêng biệt độc lập
final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, streak_side, streak_count = calculate_v67_7_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t
)
cmd = get_ultimate_directive(final_p, final_b, trend_desc, streak_side, streak_count, st.session_state.round_detailed_log, hist_p, hist_b)

BaccaratInterfaceSystem.render_header_hud(total_rounds=(total_p + total_b + total_t), cards_left=cards_left, decks_count=decks)

calc_triggered, p_input, b_input = BaccaratInterfaceSystem.render_input_form()

if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v67_7(p_input.strip())
    b_list = parse_baccarat_input_v67_7(b_input.strip())
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    st.session_state.round_detailed_log.append({'p_cards': p_list, 'b_cards': b_list, 'p_score': p_score, 'b_score': b_score, 'outcome': outcome})
    st.rerun()

st.markdown("---")

BaccaratInterfaceSystem.render_directive_panel(cmd)
BaccaratInterfaceSystem.render_probabilities_grid(final_p, final_b, final_t, total_p, total_b, total_t)
BaccaratInterfaceSystem.render_history_hud(st.session_state.round_detailed_log)

st.markdown("<br>", unsafe_allow_html=True)

undo_btn, clear_btn = BaccaratInterfaceSystem.render_utilities()
if undo_btn:
    if st.session_state.round_detailed_log:
        st.session_state.round_detailed_log.pop()
        st.rerun()
if clear_btn:
    st.session_state.round_detailed_log = []
    st.rerun()
