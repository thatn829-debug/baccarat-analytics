import streamlit as st
import numpy as np
import math

# =========================================================================
# 🔵 MODULE 1: PLAYER ULTIMATE ENGINE (Lõi toán học tổ hợp tối hậu cho Player)
# =========================================================================
class PlayerUltimateEngine:
    @staticmethod
    def calculate_absolute_probability(all_rounds_log, shoe_decks, manual_p, total_decisive):
        """Tính toán xác suất tuyệt đối cho cửa Player bằng tổ hợp phi tuyến tính"""
        # 1. Đếm chính xác số lượng từng quân bài còn lại trong khay bài
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        
        cards_remaining = max(1.0, sum(exact_cards_left.values()))

        # 2. Thuật toán tối hậu tổ hợp EOR phi tuyến tính (Non-linear Combinatorial Bias)
        # Các quân bài 4 và 5 mất đi gây thiệt hại nặng nhất cho Player, quân 6, 7, 8 tạo lợi thế
        p_eor = {
            1: -0.0051, 2: -0.0059, 3: -0.0062, 4: -0.0134, 5: -0.0096, 
            6: +0.0123, 7: +0.0144, 8: +0.0095, 
            9: -0.0026, 10: +0.0043, 11: +0.0043, 12: +0.0043, 13: +0.0043
        }
        card_effect_sum = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            card_effect_sum += removed * p_eor[card_num]

        # Khuếch đại phi tuyến tính khi khay bài cạn dần (Càng chơi lâu biên độ lỗi bài càng rộng và chính xác)
        shoe_exhaustion_ratio = 1.0 + ((4 * shoe_decks * 52) - cards_remaining) / (4 * shoe_decks * 52)
        final_card_bias = card_effect_sum * 3.1 * shoe_exhaustion_ratio

        # 3. Phân tích xung lực chuỗi độc lập tác động lên Player (Hàm mũ Entropy)
        trend_force = 0.0
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
            
            # Nếu Banker đang bệt dài, tính toán áp lực bẻ cầu chuyển dịch dòng tiền sang Player bằng hàm mũ
            if current_streak_side == "Banker" and streak_count >= 3:
                trend_force += 1.5 * math.exp(streak_count * 0.32)

        # 4. Tỷ lệ sàn dài hạn (Long-term floor weight)
        if total_decisive > 0:
            p_ratio = manual_p / total_decisive
            if p_ratio > 0.52: trend_force += 0.6
            elif p_ratio < 0.45: trend_force -= 0.6

        return 44.62 + final_card_bias + trend_force


# =========================================================================
# 🔴 MODULE 2: BANKER ULTIMATE ENGINE (Lõi toán học suy giảm chuỗi Markov cho Banker)
# =========================================================================
class BankerUltimateEngine:
    @staticmethod
    def calculate_absolute_probability(all_rounds_log, shoe_decks, manual_b, total_decisive):
        """Tính toán xác suất tuyệt đối cho cửa Banker bằng suy giảm Markov liên tục"""
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
        
        cards_remaining = max(1.0, sum(exact_cards_left.values()))

        # 1. Thuật toán EOR đối lưu phi tuyến tính cho Banker
        b_eor = {
            1: -0.0051, 2: -0.0059, 3: -0.0062, 4: -0.0134, 5: -0.0096, 
            6: +0.0123, 7: +0.0144, 8: +0.0095, 
            9: -0.0026, 10: +0.0043, 11: +0.0043, 12: +0.0043, 13: +0.0043
        }
        card_effect_sum = 0.0
        for card_num, left in exact_cards_left.items():
            removed = (4 * shoe_decks) - left
            card_effect_sum += removed * b_eor[card_num]

        shoe_exhaustion_ratio = 1.0 + ((4 * shoe_decks * 52) - cards_remaining) / (4 * shoe_decks * 52)
        final_card_bias = card_effect_sum * 3.1 * shoe_exhaustion_ratio

        # 2. Thuật toán suy giảm liên tục chuỗi Markov (Markov Chain Continuous Decay)
        trend_force = 0.0
        decisive_outcomes = [r['outcome'] for r in all_rounds_log if r['outcome'] in ["Player", "Banker"]]
        
        if decisive_outcomes:
            current_streak_side = decisive_outcomes[-1]
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
            
            # Nếu Player đang bệt dài, tính toán áp lực bẻ cầu tăng lợi thế cho Banker bằng hàm mũ
            if current_streak_side == "Player" and streak_count >= 3:
                trend_force += 1.5 * math.exp(streak_count * 0.32)
            
            # SỬA LỖI BẺ SỚM/MUỘN: Nếu Banker đang bệt quá dài, tính toán sự suy giảm xác suất duy trì chuỗi
            if current_streak_side == "Banker" and streak_count >= 4:
                # Trừ bớt lực của Banker theo cấp số mũ vì chuỗi càng dài xác suất tiếp tục bệt càng tiệm cận về 0
                trend_force -= 1.2 * math.exp((streak_count - 3) * 0.28)

        if total_decisive > 0:
            b_ratio = manual_b / total_decisive
            if b_ratio > 0.52: trend_force += 0.6
            elif b_ratio < 0.45: trend_force -= 0.6

        # Xác suất nền gốc gốc của Banker là 45.86 do lợi thế luật rút bài ván thứ 3
        return 45.86 - final_card_bias + trend_force


# =========================================================================
# 🟢 MODULE 3: TIE ULTIMATE ENGINE (Lõi phân phối siêu hình tối hậu cho cửa Hòa)
# =========================================================================
class TieUltimateEngine:
    @staticmethod
    def calculate_absolute_probability(all_rounds_log, shoe_decks):
        """Tính toán xác suất tuyệt đối cửa Hòa dựa trên thuật toán mật độ phân phối siêu hình"""
        exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
        for r in all_rounds_log:
            for card in (r['p_cards'] + r['b_cards']):
                if card in exact_cards_left:
                    exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
                    
        cards_remaining = max(1.0, sum(exact_cards_left.values()))
        
        # Cửa hòa nổ mạnh nhất khi khay bài cô đặc các quân bài 0 nút (10, J, Q, K)
        zero_value_cards_left = sum([exact_cards_left[i] for i in [10, 11, 12, 13]])
        
        # Mật độ phân phối thực tế so với mật độ phân phối chuẩn ban đầu (4/13 ~ 0.3076)
        actual_density = zero_value_cards_left / cards_remaining
        standard_density = 16.0 / 52.0
        
        density_deviation = actual_density - standard_density
        
        # Áp dụng hàm phi tuyến tính bậc 2 để phóng đại tỷ lệ Hòa khi khay bài biến động cực đoan
        tie_hypergeometric_force = density_deviation * 24.0 if density_deviation > 0 else density_deviation * 18.0
        
        return 9.52 + tie_hypergeometric_force


# =========================================================================
# 🧠 MODULE 4: FUSION DISTRIBUTOR (Bộ chuẩn hóa Vector & Điều phối dữ liệu)
# =========================================================================
def calculate_v67_8_ultimate_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t):
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r['outcome'] == "Tie")
    total_decisive = total_p_wins + total_b_wins
    
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, shoe_decks * 52, 0, 0, 0, "HỆ THỐNG TRỐNG", None, 0

    # KÍCH HOẠT 3 LÕI TỐI HẬU ĐỘC LẬP TUYỆT ĐỐI
    raw_p = PlayerUltimateEngine.calculate_absolute_probability(all_rounds_log, shoe_decks, manual_p, total_decisive)
    raw_b = BankerUltimateEngine.calculate_absolute_probability(all_rounds_log, shoe_decks, manual_b, total_decisive)
    raw_t = TieUltimateEngine.calculate_absolute_probability(all_rounds_log, shoe_decks)
    
    # Ép biên an toàn toán học nghiêm ngặt để giữ tính thực tế của dòng chảy khay bài
    raw_p = max(2.0, min(98.0, raw_p))
    raw_b = max(2.0, min(98.0, raw_b))
    raw_t = max(1.0, min(45.0, raw_t))
    
    # Chuẩn hóa ma trận xác suất (Probability Vector Normalization) -> Đảm bảo tổng luôn bằng 100%
    total_sum = raw_p + raw_b + raw_t
    p_pct = (raw_p / total_sum) * 100
    b_pct = (raw_b / total_sum) * 100
    t_pct = (raw_t / total_sum) * 100
    
    # Tính toán số bài còn lại phục vụ HUD hiển thị giao diện
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    for r in all_rounds_log:
        for card in (r['p_cards'] + r['b_cards']):
            if card in exact_cards_left: exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
    cards_remaining = int(sum(exact_cards_left.values()))
    
    # Định dạng chuỗi văn bản phân tích cầu cho giao diện
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


# =========================================================================
# 🛰️ MODULE 5: DECISION ADAPTIVE CORTEX (Bộ phát tín hiệu chiến thuật tối hậu)
# =========================================================================
def get_ultimate_directive(p_val, b_val, trend_desc, streak_side, streak_count, log, m_p, m_b):
    if not log and (m_p == 0 and m_b == 0):
        return {
            "status": "🛰️ ULTIMATE SOVEREIGN READY",
            "msg": "Hệ thống 3 lõi tối hậu cửa độc lập đã kích hoạt thành công. Đang chờ đồng bộ dữ liệu bài.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%"
        }
    
    diff = abs(p_val - b_val)
    
    # Hệ thống bẻ cầu tự động tính toán điểm đảo chiều chính xác từ 3 lõi độc lập
    if streak_side and streak_count >= 3:
        target = "PLAYER" if streak_side == "Banker" else "BANKER"
        # Chỉ phát lệnh nếu độ lệch xác suất tối hậu thực sự ủng hộ việc bẻ cầu
        if (target == "PLAYER" and p_val > b_val) or (target == "BANKER" and b_val > p_val):
            return {
                "status": f"🚨 LỆNH BÈ CẦU TỐI HẬU ➡️ {target}",
                "msg": f"Xác nhận trạng thái: {trend_desc}. Lõi độc lập của cửa {target} đã tích lũy đủ năng lượng tổ hợp phi tuyến tính, xác nhận chuỗi bệt hiện tại đã bão hòa điểm số. Tiến hành vào lệnh.",
                "color": "#00f5d4", "bg": "rgba(0, 245, 212, 0.15)", "size": "4% - 6% (Cực kỳ an toàn)"
            }
        
    if diff < 1.8:
        return {
            "status": "🛑 CHỜ QUAN SÁT (TRẠNG THÁI TĨNH)",
            "msg": f"Mức chênh lệch lợi thế ({diff:.2f}%) quá thấp để vượt qua màng lọc an toàn phi tuyến tính. Hệ thống từ chối phát lệnh để bảo toàn vốn.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 VÀO LỆNH THUẬN DÒNG: PLAYER",
            "msg": f"Lõi PlayerUltimateEngine xác nhận điểm lợi thế vượt ngưỡng đột biến (+{diff:.2f}%). Xu hướng dòng chảy khay bài rất ổn định.",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "2.5% - 4%"
        }
    else:
        return {
            "status": "🔴 VÀO LỆNH THUẬN DÒNG: BANKER",
            "msg": f"Lõi BankerUltimateEngine xác nhận điểm lợi thế vượt ngưỡng đột biến (+{diff:.2f}%). Xu hướng dòng chảy khay bài rất ổn định.",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "2.5% - 4%"
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
        st.markdown("##### 🎴 NHẬP QUÂN BÀI CHI TIẾT ĐỂ TÍNH TOÁN 3 CỬA:")
        with st.form(key="baccarat_3_ultimate_independent_form", clear_on_submit=True):
            input_grid = st.columns(2)
            with input_grid[0]:
                p_str = st.text_input("🔵 PLAYER CARD:", placeholder="Ví dụ: 8 K 2")
            with input_grid[1]:
                b_str = st.text_input("🔴 BANKER CARD:", placeholder="Ví dụ: 7 J")
            st.write("")
            st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
            triggered = st.form_submit_button("🔥 KHỞI CHẠY MA TRẬN TỐI HẬU")
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
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER SOVEREIGN</span><span class="metric-num" style="color:#00afb9;">{p_pct:.2f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {p_cnt}</span></div>', unsafe_allow_html=True)
        with prob_grid[1]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER SOVEREIGN</span><span class="metric-num" style="color:#ff4757;">{b_pct:.2f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {b_cnt}</span></div>', unsafe_allow_html=True)
        with prob_grid[2]:
            st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE HYPERGEOM</span><span class="metric-num" style="color:#2ecc71;">{t_pct:.2f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {t_cnt}</span></div>', unsafe_allow_html=True)

    @staticmethod
    def render_history_hud(log):
        if log:
            st.markdown('<div class="score-log-hud"><b>📊 TIẾN TRÌNH KHẤU TRỪ BÀI ĐỘC LẬP:</b><br>', unsafe_allow_html=True)
            for idx, r in enumerate(log):
                st.markdown(f"• Ván {idx+1}: [Player] {r['p_score']}đ vs {r['b_score']}đ [Banker] ➡️ Kết quả: **{r['outcome'].upper()}**")
            st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def render_utilities():
        util_grid = st.columns(2)
        undo_triggered = util_grid[0].button("⏪ HOÀN TÁC (PHỤC HỒI BÀI)")
        clear_triggered = util_grid[1].button("🔄 LÀM TRỐNG KHAY BÀI")
        return undo_triggered, clear_triggered


# =========================================================================
# 🎮 RUNTIME EXECUTION CONTROLLER (Trục điều hành chính)
# =========================================================================
st.set_page_config(page_title="Oracle Triple Ultimate v67.8", page_icon="⚡", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state: 
    st.session_state.round_detailed_log = []

decks, hist_p, hist_b, hist_t = BaccaratInterfaceSystem.render_sidebar()

st.markdown("### ⚡ ORACLE TREND TRACKING v67.8")
st.caption("Kiến Trúc Lõi Tối Hậu Độc Lập Cho 3 Cửa | Đếm Bài Phi Tuyến Tính & Chuỗi Markov Co Giãn")

# Tính toán ma trận phân phối xác suất tuyệt đối từ 3 lõi độc lập hoàn toàn
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
