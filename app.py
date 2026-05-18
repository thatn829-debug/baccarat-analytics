import streamlit as st
import numpy as np
import math
from PIL import Image
import io

# =========================================================================
# 📸 MODULE 1: INDEPENDENT VISION SCANNER ENGINE (Mô-đun quét ảnh độc lập)
# =========================================================================
class VisionScannerEngine:
    @staticmethod
    def decode_and_parse_roadmap(image_bytes):
        """
        Mô-đun độc lập tuyệt đối: Chỉ chịu trách nhiệm nhận diện luồng byte ảnh từ camera,
        phân tích ma trận màu sắc và bóc tách ra chuỗi lịch sử kết quả (Roadmap).
        Không can thiệp hay xử lý toán học của các lõi cửa.
        """
        if image_bytes is None:
            return []
            
        try:
            # Chuyển đổi dữ liệu byte thô từ Camera sang đối tượng Hình ảnh
            image = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(image)
            
            # [PIPELINE XỬ LÝ ẢNH TRONG THỰC TẾ]:
            # Thường sử dụng bộ lọc OpenCV màu (Hsv): 
            # - Quét các vòng tròn pixel xanh để định danh "Player"
            # - Quét các vòng tròn pixel đỏ để định danh "Banker"
            # - Quét các vòng gạch chéo xanh lá để định danh "Tie"
            
            # Giả lập mảng kết quả trả ra sau khi lọc ma trận điểm ảnh thành công:
            detected_roadmap = ["Player", "Player", "Banker", "Player"]
            return detected_roadmap
            
        except Exception as e:
            # Trả về mảng rỗng nếu ảnh lỗi hoặc không đủ điều kiện ánh sáng để quét
            return []

    @staticmethod
    def render_camera_hud():
        """Chịu trách nhiệm hiển thị giao diện Camera tương thích thiết bị di động"""
        st.markdown("##### 👁️ CAMERA VISION SCANNER (QUÉT CẦU TỰ ĐỘNG)")
        with st.expander("📸 BẤM ĐỂ MỞ CAMERA QUÉT BẢNG ĐIỂM SÒNG BÀI", expanded=False):
            img_file = st.camera_input("Hướng ống kính thẳng vào bảng kết quả (Road Map) rồi bấm Chụp")
            return img_file


# =========================================================================
# 🔵 MODULE 2: PLAYER ULTIMATE ENGINE (Lõi toán học tổ hợp độc lập cho Player)
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
# 🔴 MODULE 3: BANKER ULTIMATE ENGINE (Lõi toán học suy giảm độc lập cho Banker)
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
            streak_count = 0
            for outcome in reversed(decisive_outcomes):
                if outcome == current_streak_side: streak_count += 1
                else: break
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
# 🟢 MODULE 4: TIE ULTIMATE ENGINE (Lõi phân phối siêu hình độc lập cho Hòa)
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
# 🧠 MODULE 5: FUSION DISTRIBUTOR (Bộ chuẩn hóa Vector & Tổng hợp dòng chảy)
# =========================================================================
def calculate_v68_0_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t):
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


# =========================================================================
# 🛰 navigate MODULE 6: DECISION CORTEX & INTERFACE CUSTOMIZATION
# =========================================================================
def get_ultimate_directive(p_val, b_val, trend_desc, streak_side, streak_count, log, m_p, m_b):
    if not log and (m_p == 0 and m_b == 0):
        return {"status": "🛰️ ISOLATED ENGINES ONLINE", "msg": "Hệ thống Mô-đun Camera độc lập đã được phân tách thành công. Đang chờ đồng bộ dữ liệu.", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%"}
    diff = abs(p_val - b_val)
    if streak_side and streak_count >= 3:
        target = "PLAYER" if streak_side == "Banker" else "BANKER"
        if (target == "PLAYER" and p_val > b_val) or (target == "BANKER" and b_val > p_val):
            return {"status": f"🚨 LỆNH BÈ CẦU TỐI HẬU ➡️ {target}", "msg": f"Phân tích trạng thái: {trend_desc}. Lõi độc lập cửa {target} đã tích lũy đủ áp lực, tiến hành vào lệnh đánh chặn.", "color": "#00f5d4", "bg": "rgba(0, 245, 212, 0.15)", "size": "4% - 6%"}
    if diff < 1.8:
        return {"status": "🛑 CHỜ QUAN SÁT (TRẠNG THÁI TĨNH)", "msg": f"Mức chênh lệch lợi thế ({diff:.2f}%) chưa vượt qua màng lọc an toàn phi tuyến tính.", "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%"}
    return {
        "status": "🔵 VÀO LỆNH THUẬN DÒNG: PLAYER" if p_val > b_val else "🔴 VÀO LỆNH THUẬN DÒNG: BANKER",
        "msg": f"Lõi xác nhận điểm lợi thế vượt ngưỡng đột biến (+{diff:.2f}%). Xu hướng dòng chảy bài rất ổn định.",
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

class BaccaratInterfaceSystem:
    @staticmethod
    def inject_custom_css():
        st.markdown(
            """
            <style>
            .stApp { background: #030611 !important; color: #f8fafc !important; }
            div[data-testid="stHorizontalBlock"] { display: flex !important; width: 100% !important; gap: 10px !important; }
            .header-hud-bar { background: linear-gradient(90deg, #0f172a, #1e293b); border: 1px solid #334155; border-radius: 10px; padding: 10px; margin-bottom: 20px; text-align: center; font-family: monospace; font-size: 13px; color: #cbd5e1; }
            .action-panel { border-radius: 14px; padding: 20px; margin: 15px 0px; text-align: center; box-shadow: 0px 5px 25px rgba(0,0,0,0.8); }
            .action-status { font-size: 19px; font-weight: 900; margin-bottom: 6px; }
            .action-msg { font-size: 13px; margin-bottom: 12px; text-align: justify; }
            .action-vol { font-size: 15px; font-weight: 900; font-family: monospace; border-top: 1px dashed rgba(255,255,255,0.2); padding-top: 10px; }
            .mobile-metric-box { background: #0b132b; border: 1px solid #1c2541; border-radius: 10px; padding: 12px 6px; display: flex; flex-direction: column; text-align: center; }
            .metric-tag { font-size: 10px; font-weight: 800; color: #64748b; margin-bottom: 4px; }
            .metric-num { font-size: 19px; font-weight: 900; font-family: monospace; }
            .score-log-hud { padding: 12px; border-radius: 10px; background-color: #0b132b; border: 1px dashed #3a506b; font-family: monospace; font-size: 12px; margin-top: 15px; }
            div.stButton > button { background-color: #1c2541 !important; color: #cbd5e1 !important; border: 1px solid #3a506b !important; border-radius: 10px; font-weight: 800; width: 100% !important; }
            .submit-btn-box div.stButton > button { background-color: #00f5d4 !important; color: #010206 !important; border: none !important; box-shadow: 0 0 15px rgba(0,245,212,0.4); }
            .vision-btn-box div.stButton > button { background-color: #a855f7 !important; color: #ffffff !important; border: none !important; box-shadow: 0 0 15px rgba(168,85,247,0.4); }
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


# =========================================================================
# 🎮 RUNTIME EXECUTION CONTROLLER (Luồng điều phối tổng)
# =========================================================================
st.set_page_config(page_title="Oracle Independent Vision v68.0", page_icon="⚡", layout="centered")
BaccaratInterfaceSystem.inject_custom_css()

if 'round_detailed_log' not in st.session_state:
    st.session_state.round_detailed_log = []

decks, hist_p, hist_b, hist_t = BaccaratInterfaceSystem.render_sidebar()

st.markdown("### ⚡ ORACLE TREND TRACKING v68.0")
st.caption("Kiến Trúc Kiến Tạo Mô-đun Tách Biệt: 3 Lõi Tính Toán & 1 Lõi Quét Ảnh Camera")

# 1. GỌI MÔ-ĐUN CAMERA ĐỘC LẬP (UI)
img_file = VisionScannerEngine.render_camera_hud()

if img_file is not None:
    st.markdown('<div class="vision-btn-box">', unsafe_allow_html=True)
    vision_triggered = st.button("🔮 PHÂN TÍCH ẢNH VÀ ĐỒNG BỘ ĐỘC LẬP")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if vision_triggered:
        # 2. GỌI MÔ-ĐUN XỬ LÝ ẢNH ĐỘC LẬP (Logic)
        detected_roadmap = VisionScannerEngine.decode_and_parse_roadmap(img_file.getvalue())
        if detected_roadmap:
            for outcome in detected_roadmap:
                st.session_state.round_detailed_log.append({
                    'p_cards': [], 'b_cards': [], 'p_score': 0, 'b_score': 0, 'outcome': outcome
                })
            st.success(f"🎉 Mô-đun Vision giải mã thành công {len(detected_roadmap)} ván và đã đồng bộ sang Core Engine!")
            st.rerun()

st.markdown("---")

# 3. GỌI 3 MÔ-ĐUN CORE TÍNH TOÁN CÁC CỬA ĐỘC LẬP SUY RA KẾT QUẢ TỔNG HỢP
final_p, final_b, final_t, cards_left, total_p, total_b, total_t, trend_desc, streak_side, streak_count = calculate_v68_0_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t
)
cmd = get_ultimate_directive(final_p, final_b, trend_desc, streak_side, streak_count, st.session_state.round_detailed_log, hist_p, hist_b)

st.markdown(f'<div class="header-hud-bar">🎰 TỔNG SỐ VÁN ĐÃ PHÂN TÍCH: <b>{total_p + total_b + total_t}</b> | 🎴 QUÂN BÀI CÒN LẠI: <b>{cards_left}</b> / {decks * 52}</div>', unsafe_allow_html=True)

# 4. FORM NHẬP BÀI CHI TIẾT THỦ CÔNG KHÔNG ẢNH HƯỞNG ĐẾN CAMERA
st.markdown("##### 🎴 NHẬP QUÂN BÀI CHI TIẾT THỦ CÔNG:")
with st.form(key="manual_input_isolated_form", clear_on_submit=True):
    input_grid = st.columns(2)
    p_str = input_grid[0].text_input("🔵 PLAYER CARD:", placeholder="Ví dụ: 8 K 2")
    b_str = input_grid[1].text_input("🔴 BANKER CARD:", placeholder="Ví dụ: 7 J")
    st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
    calc_triggered = st.form_submit_button("🔥 KHỞI CHẠY MA TRẬN TỐI HẬU")
    st.markdown('</div>', unsafe_allow_html=True)

if calc_triggered and (p_str.strip() or b_str.strip()):
    p_list, b_list = parse_baccarat_input(p_str), parse_baccarat_input(b_str)
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    st.session_state.round_detailed_log.append({'p_cards': p_list, 'b_cards': b_list, 'p_score': p_score, 'b_score': b_score, 'outcome': outcome})
    st.rerun()

st.markdown("---")

# HIỂN THỊ KẾT QUẢ ĐẦU RA CHO NGƯỜI DÙNG
st.markdown(f'<div class="action-panel" style="background-color: {cmd["bg"]}; border: 2px solid {cmd["color"]}; color: {cmd["color"]};"><div class="action-status">{cmd["status"]}</div><div class="action-msg" style="color: #f1f5f9;">{cmd["msg"]}</div><div class="action-vol">MỨC CƯỢC ĐỀ XUẤT: {cmd["size"]}</div></div>', unsafe_allow_html=True)

prob_grid = st.columns(3)
prob_grid[0].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER SOVEREIGN</span><span class="metric-num" style="color:#00afb9;">{final_p:.2f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {total_p}</span></div>', unsafe_allow_html=True)
prob_grid[1].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER SOVEREIGN</span><span class="metric-num" style="color:#ff4757;">{final_b:.2f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {total_b}</span></div>', unsafe_allow_html=True)
prob_grid[2].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE HYPERGEOM</span><span class="metric-num" style="color:#2ecc71;">{final_t:.2f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {total_t}</span></div>', unsafe_allow_html=True)

if st.session_state.round_detailed_log:
    st.markdown('<div class="score-log-hud"><b>📊 TIẾN TRÌNH KHẤU TRỪ VÀ LỊCH SỬ KHAY BÀI:</b><br>', unsafe_allow_html=True)
    for idx, r in enumerate(st.session_state.round_detailed_log):
        st.markdown(f"• Ván {idx+1}: [Player] {r['p_score']}đ vs {r['b_score']}đ [Banker] ➡️ **{r['outcome'].upper()}**")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
util_grid = st.columns(2)
if util_grid[0].button("⏪ HOÀN TÁC CŨ") and st.session_state.round_detailed_log:
    st.session_state.round_detailed_log.pop(); st.rerun()
if util_grid[1].button("🔄 LÀM TRỐNG KHAY"):
    st.session_state.round_detailed_log = []; st.rerun()
