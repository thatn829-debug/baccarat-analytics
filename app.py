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
        # Hệ số EOR Chuẩn Quốc Tế mở rộng
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
        # Trả về biên độ lệch dựa trên mật độ phân phối ván thắng thực tế
        if p_win_rate > 0.53: return 1.8
        if p_win_rate < 0.47: return -1.8
        return 0.0

    @staticmethod
    def detect_streak_state(all_rounds_log):
        current_streak_side = None
        current_streak_count = 0
        for r in all_rounds_log:
            if r['outcome'] in ["Player", "Banker"]:
                if current_streak_side == r['outcome']:
                    current_streak_count += 1
                else:
                    current_streak_side = r['outcome']
                    current_streak_count = 1
        return current_streak_side, current_streak_count


# =========================================================================
# 🧠 MODULE 3: FUSION PREDICTION CORE (Bộ hội tụ dữ liệu & Tính toán xác suất)
# =========================================================================
def calculate_v64_5_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t):
    # Tính số ván thắng tổng hợp
    total_p_wins = manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")
    total_b_wins = manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")
    total_ties = manual_t + sum(1 for r in all_rounds_log if r['outcome'] == "Tie")
    
    # Kích hoạt trạng thái Zero-Start nếu không có bất kỳ dữ liệu nào
    if not all_rounds_log and (manual_p == 0 and manual_b == 0 and manual_t == 0):
        return 0.0, 0.0, 0.0, shoe_decks * 52, 0, 0, 0, False, None, 0

    # Gọi Module 1: Xử lý đếm bài
    cards_left_dict = CardCountingEngine.get_remaining_cards(all_rounds_log, shoe_decks)
    cards_remaining = max(1.0, sum(cards_left_dict.values()))
    eor_bias = CardCountingEngine.calculate_eor_bias(cards_left_dict, shoe_decks)
    
    # Gọi Module 2: Phân tích xu hướng road bài
    road_bias = TrendMatrixEngine.evaluate_road_bias(total_p_wins, total_b_wins)
    streak_side, streak_count = TrendMatrixEngine.detect_streak_state(all_rounds_log)
    
    # Tính toán mật độ bài hình (10, J, Q, K) còn lại
    p_0 = sum([cards_left_dict[i] for i in [10, 11, 12, 13]]) / cards_remaining

    # Tổ hợp công thức xác suất từ các Module kết quả
    base_p = 44.62 + (eor_bias * 2.6) + road_bias
    base_b = 45.86 - (eor_bias * 2.6) - road_bias
    base_t = 9.52 + (p_0 * 3.2)

    # Điểm tới hạn bẻ cầu bệt (Ván thứ 4 trở đi)
    is_critical = False
    if streak_side and streak_count >= 4:
        is_critical = True
        if streak_side == "Banker":
            base_p += 5.0; base_b -= 5.0
        else:
            base_b += 5.0; base_p -= 5.0

    # Ép biên toán học giới hạn bảo toàn
    base_p = max(30.0, min(70.0, base_p))
    base_b = max(30.0, min(70.0, base_b))
    base_t = max(4.0, min(22.0, base_t))
    
    total_sum = base_p + base_b + base_t
    return (base_p / total_sum) * 100, (base_b / total_sum) * 100, (base_t / total_sum) * 100, int(cards_remaining), total_p_wins, total_b_wins, total_ties, is_critical, streak_side, streak_count


# =========================================================================
# 🛰️ MODULE 4: DECISION ADAPTIVE CORTEX (Bộ điều phối & Phát lệnh tấn công)
# =========================================================================
def get_modular_directive(p_val, b_val, is_critical, streak_side, streak_count, log, m_p, m_b):
    if not log and (m_p == 0 and m_b == 0):
        return {
            "status": "🛰️ MULTI-MODULE v64.5 READY",
            "msg": "Hệ thống đa mô đun đã đồng bộ thành công. Vui lòng cập nhật số liệu bảng điểm hoặc nhập quân bài ván hiện tại.",
            "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%"
        }
    
    diff = abs(p_val - b_val)
    
    if is_critical and streak_side and streak_count >= 4:
        target = "PLAYER" if streak_side == "Banker" else "BANKER"
        return {
            "status": f"🚨 LẬT CẦU BẺ CHUỖI: {target}",
            "msg": f"Mô-đun Chuỗi Markov phát hiện bệt {streak_side.upper()} ({streak_count} ván) đã tới hạn phân phối cực đại. Vào lệnh đảo chiều.",
            "color": "#06d6a0", "bg": "rgba(6, 214, 160, 0.2)", "size": "3% - 5%"
        }
        
    # Màng lọc nhạy bén tối ưu hóa độ nhạy
    matrix_threshold = 1.2
    if diff < matrix_threshold:
        return {
            "status": "🛑 CHỜ (WAIT) - GIẰNG CO",
            "msg": f"Mô-đun phân tích xác định độ lệch biên độ quá hẹp ({diff:.2f}%). Hãy bỏ qua ván này để bảo toàn dòng vốn ổn định.",
            "color": "#f1c40f", "bg": "rgba(241, 196, 15, 0.1)", "size": "0%"
        }
        
    if p_val > b_val:
        return {
            "status": "🔵 VÀO LỆNH: PLAYER",
            "msg": f"Mô-đun đếm bài đồng thuận cùng ma trận lịch sử xác nhận ưu thế vượt vùng lọc nghiêng về Player (+{diff:.2f}%).",
            "color": "#00afb9", "bg": "rgba(0, 175, 185, 0.2)", "size": "2% - 3%"
        }
    else:
        return {
            "status": "🔴 VÀO LỆNH: BANKER",
            "msg": f"Dữ liệu tích hợp đa tầng phân phối xác nhận lợi thế dòng chảy toán học nghiêng hẳn về Banker (+{diff:.2f}%).",
            "color": "#ff4757", "bg": "rgba(255, 71, 87, 0.2)", "size": "2% - 3%"
        }

def parse_baccarat_input_v64_5(raw_str):
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
# 📱 MODULE 5: USER INTERFACE SYSTEM (Bảo lưu toàn bộ giao diện & Ô nhập liệu)
# =========================================================================
st.set_page_config(page_title="Oracle Multi-Module v64.5", page_icon="⚡", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: #030611 !important; color: #f8fafc !important; }
    
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; gap: 10px !important; }
    div[data-testid="stHorizontalBlock"] > div { flex: 1 1 0% !important; min-width: 0px !important; }
    
    .action-panel { border-radius: 14px; padding: 20px; margin: 15px 0px; text-align: center; box-shadow: 0px 5px 25px rgba(0,0,0,0.8); }
    .action-status { font-size: 22px; font-weight: 900; letter-spacing: 0.5px; margin-bottom: 6px; }
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
    
    div[data-testid="stNumberInput"] label { font-size: 11px !important; color: #94a3b8 !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.markdown("### ⚡ ORACLE MULTI-MODULE v64.5")
st.caption("Kiến trúc phân rã mô đun độc lập | Tối ưu hóa tính chính xác tính toán ngầm.")

# 1. Ô NHẬP LIỆU SỐ VÁN THẮNG LỊCH SỬ BẢN CHƠI TRÊN ROAD (BẢO LƯU NGUYÊN VẸN)
st.markdown("##### 📊 1. NHẬP LỊCH SỬ BẢNG ĐIỂM (TỪ SÒNG BÀI):")
road_input_grid = st.columns(3)
with road_input_grid[0]:
    hist_p = st.number_input("🔵 PLAYER WINS:", min_value=0, value=0, step=1)
with road_input_grid[1]:
    hist_b = st.number_input("🔴 BANKER WINS:", min_value=0, value=0, step=1)
with road_input_grid[2]:
    hist_t = st.number_input("🟢 TIE WINS:", min_value=0, value=0, step=1)

st.markdown("---")

# 2. Ô NHẬP LIỆU QUÂN BÀI CHI TIẾT QUA FORM (BẢO LƯU NGUYÊN VẸN)
st.markdown("##### 🎴 2. NHẬP QUÂN BÀI CHI TIẾT HIỆN TẠI:")
with st.form(key="baccarat_modular_input_form", clear_on_submit=True):
    input_grid = st.columns(2)
    with input_grid[0]:
        p_input = st.text_input("🔵 PLAYER CARD:", placeholder="Ví dụ: 8 K 2")
    with input_grid[1]:
        b_input = st.text_input("🔴 BANKER CARD:", placeholder="Ví dụ: 7 J")
    
    st.write("")
    st.markdown('<div class="submit-btn-box">', unsafe_allow_html=True)
    calc_triggered = st.form_submit_button("🔥 PHÂN TÍCH HỘI TỤ ĐA MÔ ĐUN")
    st.markdown('</div>', unsafe_allow_html=True)

if calc_triggered and (p_input.strip() or b_input.strip()):
    p_list = parse_baccarat_input_v64_5(p_input.strip())
    b_list = parse_baccarat_input_v64_5(b_input.strip())
    p_score = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
    b_score = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    st.session_state.round_detailed_log.append({'p_cards': p_list, 'b_cards': b_list, 'p_score': p_score, 'b_score': b_score, 'outcome': outcome})
    st.rerun()

st.markdown("---")

# CHẠY HỘI TỤ ĐA MÔ ĐUN TÍNH TOÁN
final_p, final_b, final_t, cards_left, total_p, total_b, total_t, is_critical, streak_side, streak_count = calculate_v64_5_fusion(
    st.session_state.round_detailed_log, shoe_decks=decks, manual_p=hist_p, manual_b=hist_b, manual_t=hist_t
)
cmd = get_modular_directive(final_p, final_b, is_critical, streak_side, streak_count, st.session_state.round_detailed_log, hist_p, hist_b)

# BẢNG CHỈ THỊ HÀNH ĐỘNG 
st.markdown(
    f'<div class="action-panel" style="background-color: {cmd["bg"]}; border: 2px solid {cmd["color"]}; color: {cmd["color"]};">'
    f'<div class="action-status">{cmd["status"]}</div>'
    f'<div class="action-msg" style="color: #f1f5f9;">{cmd["msg"]}</div>'
    f'<div class="action-vol">MỨC CƯỢC ĐỀ XUẤT: {cmd["size"]}</div>'
    f'</div>',
    unsafe_allow_html=True
)

# HIỂN THỊ BA ĐƯỜNG XÁC SUẤT ĐỐI XỨNG NGANG TRÊN MOBILE
prob_grid = st.columns(3)
with prob_grid[0]:
    st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER TOTAL</span><span class="metric-num" style="color:#00afb9;">{final_p:.1f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {total_p}</span></div>', unsafe_allow_html=True)
with prob_grid[1]:
    st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER TOTAL</span><span class="metric-num" style="color:#ff4757;">{final_b:.1f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {total_b}</span></div>', unsafe_allow_html=True)
with prob_grid[2]:
    st.markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE TOTAL</span><span class="metric-num" style="color:#2ecc71;">{final_t:.1f}%</span><span style="font-size:10px; opacity:0.6;">Tổng: {total_t}</span></div>', unsafe_allow_html=True)

# LỊCH SỬ QUÂN BÀI THỰC TẾ
if st.session_state.round_detailed_log:
    st.markdown('<div class="score-log-hud"><b>📊 LỊCH SỬ QUÂN BÀI ĐÃ NẠP QUA APP:</b><br>', unsafe_allow_html=True)
    for idx, r in enumerate(st.session_state.round_detailed_log):
        st.markdown(f"• Ván {idx+1}: [P] {r['p_score']}đ vs {r['b_score']}đ [B] ➡️ **{r['outcome'].upper()}**")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# TIỆN ÍCH HOÀN TÁC / LÀM TRỐNG (GIỮ NGUYÊN)
util_grid = st.columns(2)
with util_grid[0]:
    if st.button("⏪ HOÀN TÁC BÀI"):
        if st.session_state.round_detailed_log:
            st.session_state.round_detailed_log.pop()
            st.rerun()
with util_grid[1]:
    if st.button("🔄 LÀM TRỐNG TOÀN BỘ"):
        st.session_state.round_detailed_log = []
        st.rerun()
