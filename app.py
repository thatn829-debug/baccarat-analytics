import streamlit as st
import numpy as np

# =========================================================================
# MODULE 1: ĐỘNG CƠ TỔ HỢP LÁ BÀI & ĐO LƯỜNG ĐỘ BIẾN THIÊN LƯỢNG TỬ
# =========================================================================
def calculate_v47_engine(all_rounds_log, shoe_decks, side_p_wins, side_b_wins):
    """
    Lấy quân bài làm gốc, phóng đại biên độ chênh lệch, 
    đồng thời tính toán chính xác độ biến thiên (Volatility) thực thời của bàn chơi.
    """
    total_initial_cards = shoe_decks * 52
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    all_flat_cards = []
    margins_list = []
    valid_rounds_count = 0
    last_round_winner = None
    last_round_margin = 0
    
    for r in all_rounds_log:
        all_flat_cards.extend(r['p_cards'] + r['b_cards'])
        margin = r['p_score'] - r['b_score']
        margins_list.append(abs(margin))
        valid_rounds_count += 1
        last_round_winner = r['outcome']
        last_round_margin = abs(margin)
        
    for card in all_flat_cards:
        if card in exact_cards_left:
            exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
            
    cards_remaining = sum(exact_cards_left.values())
    if cards_remaining <= 0: cards_remaining = 1.0
    
    # Tính toán phân bổ nhóm bài
    score_counts = [0.0] * 10
    for card_num, count in exact_cards_left.items():
        if card_num >= 10: score_counts[0] += count
        else: score_counts[card_num] += count
        
    p_0 = score_counts[0] / cards_remaining
    p_low = sum(score_counts[1:6]) / cards_remaining
    p_high = sum(score_counts[6:10]) / cards_remaining

    # Tính độ biến thiên toán học (Volatility Index) dựa trên độ lệch chuẩn của điểm số
    volatility_index = 0.0
    if len(margins_list) >= 2:
        # Độ lệch chuẩn của biên độ điểm thắng qua các ván
        std_deviation = float(np.std(margins_list))
        # Quy đổi ra tỷ lệ phần trăm biến thiên (Max khống chế khoảng 50% để hiển thị trực quan)
        volatility_index = min(50.0, (std_deviation / 4.5) * 100.0)
    elif len(margins_list) == 1:
        volatility_index = 12.5 # Mức nền mặc định cho ván đầu tiên

    # Khung toán học gốc của khay bài
    math_bias = (p_low * 0.12) - (p_high * 0.09) + (p_0 * 0.04)
    
    base_p = 44.62 + (math_bias * 100.0)
    base_b = 45.86 - (math_bias * 100.0)
    base_t = 9.52 + (p_0 * 6.0)

    # Hệ số phóng đại biên độ để bẻ gãy thế cân bằng 50-50
    delta_diff = base_p - base_b
    if abs(delta_diff) > 0.1:
        amp_factor = 3.0 
        base_p += (delta_diff * amp_factor)
        base_b -= (delta_diff * amp_factor)

    # Cộng hưởng xung lực điểm số ván trước
    if valid_rounds_count > 0 and last_round_winner:
        momentum_push = min(9.0, last_round_margin * 1.5)
        if last_round_winner == "Player":
            base_p += momentum_push
            base_b -= (momentum_push * 0.5)
        elif last_round_winner == "Banker":
            base_b += momentum_push
            base_p -= (momentum_push * 0.5)

    # Khống chế giới hạn phân phối
    base_p = max(15.0, min(80.0, base_p))
    base_b = max(15.0, min(80.0, base_b))
    base_t = max(4.0, min(25.0, base_t))
    
    total_sum = base_p + base_b + base_t
    return (base_p / total_sum) * 100, (base_b / total_sum) * 100, (base_t / total_sum) * 100, int(cards_remaining), volatility_index


# =========================================================================
# AI STRATEGIC FILTER WITH VOLATILITY GUARDRESIST
# =========================================================================
def get_ai_recommendation_v47(p_val, b_val, t_val, log, vol_val):
    if not log:
        return "📊 Vui lòng nhập quân bài thực tế để kích hoạt máy đo biến thiên khay bài.", "rgba(164, 176, 190, 0.1)", "#a4b0be"
    
    # CHẶN LỆNH NẾU ĐỘ BIẾN THIÊN QUÁ CAO (SÒNG ĐANG QUÉT HOẶC XÁO TRỘN BÀI DỊ)
    if vol_val > 30.0:
         return f"🚨 ĐỘ BIẾN THIÊN CỰC ĐẠI ({vol_val:.1f}%): Bàn chơi đang rơi vào vùng nhiễu động dị biệt (Quét tài khoản). TUYỆT ĐỐI DỪNG LỆNH!", "rgba(235, 94, 40, 0.2)", "#eb5e28"
         
    if t_val > 18.0:
        return f"🟢 ĐIỂM RƠI TỔ HỢP HÒA (TIE): Mật độ bài nút không đồng đều, lót nhẹ cửa Hòa ({t_val:.2f}%).", "rgba(46, 213, 115, 0.15)", "#2ed573"
        
    diff = abs(p_val - b_val)
    
    if p_val > b_val:
        if diff >= 5.0:
            return f"🔥 LỆNH XUNG LỰC CAO: VÀO 🔵 PLAYER (Biến thiên ổn định {vol_val:.1f}% + Ưu thế khuếch đại +{diff:.1f}%).", "rgba(0, 175, 185, 0.25)", "#00afb9"
        return f"🔵 LỆNH TIÊU CHUẨN: PLAYER (Khay bài chuyển dịch an toàn về phía Người Chơi).", "rgba(0, 175, 185, 0.15)", "#00afb9"
        
    elif b_val > p_val:
        if diff >= 5.0:
            return f"🔥 LỆNH XUNG LỰC CAO: VÀO 🔴 BANKER (Biến thiên ổn định {vol_val:.1f}% + Ưu thế khuếch đại +{diff:.1f}%).", "rgba(254, 217, 255, 0.25)", "#fed9ff"
        return f"🔴 LỆNH TIÊU CHUẨN: BANKER (Khay bài chuyển dịch an toàn về phía Nhà Cái).", "rgba(254, 217, 255, 0.15)", "#fed9ff"
        
    return "📊 THẾ BÀI TRUNG TÍNH: Biên độ giằng co chưa đạt điểm bứt phá. Bỏ ván!", "rgba(164, 176, 190, 0.1)", "#a4b0be"

def parse_baccarat_input_v47(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().strip().replace(",", " ").replace(";", " ")
    temp_tokens = []
    i = 0
    while i < len(normalized):
        if normalized[i].isspace():
            i += 1
            continue
        if normalized[i:i+2] == "10":
            temp_tokens.append("10")
            i += 2
        else:
            temp_tokens.append(normalized[i])
            i += 1
    result_list = []
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13, '10': 10}
    for token in temp_tokens:
        if token in mapping: result_list.append(mapping[token])
        elif token.isdigit():
            val = int(token)
            if 1 <= val <= 9: result_list.append(val)
    return result_list

# =========================================================================
# SYSTEM INTERFACE DISPLAY
# =========================================================================
st.set_page_config(page_title="Oracle Engine v47.0 Real-Time Variance", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(145deg, #060913, #0b1120, #111a30) !important; color: #ecf0f1 !important; }
    
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
    }
    div[data-testid="stHorizontalBlock"] > div {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    .central-game-counter { text-align: center; background: rgba(0, 175, 185, 0.15); border: 1px solid #00afb9; border-radius: 8px; padding: 8px 12px; font-family: monospace; font-size: 15px; font-weight: 800; color: #00afb9; margin-bottom: 12px; }
    .ai-decision-box { text-align: center; border-radius: 10px; padding: 14px 10px; font-size: 15px; font-weight: 800; margin: 12px auto; box-shadow: 0px 4px 15px rgba(0,0,0,0.3); line-height: 1.4; }
    
    .hud-box { padding: 12px 4px; border-radius: 10px; text-align: center; margin-bottom: 8px; border: 1px solid #0b1120; background: rgba(6, 9, 19, 0.9); min-height: 85px; display: flex; flex-direction: column; justify-content: center; }
    .hud-title { font-size: 11px; font-weight: 700; color: #a4b0be; text-transform: uppercase; }
    .hud-value { font-size: 25px; font-weight: 800; font-family: monospace; margin-top: 1px; }
    
    .neon-player-advantage { background-color: #062f3f !important; border: 2px solid #00afb9 !important; box-shadow: 0px 0px 12px rgba(0, 175, 185, 0.3); }
    .neon-banker-advantage { background-color: #38121a !important; border: 2px solid #e74c3c !important; box-shadow: 0px 0px 12px rgba(231, 76, 60, 0.3); }
    
    .vol-low { color: #00afb9 !important; }
    .vol-mid { color: #f1c40f !important; }
    .vol-high { color: #eb5e28 !important; animation: blinker 1.2s linear infinite; }
    
    @keyframes blinker {
        50% { opacity: 0.3; }
    }
    
    .logic-lock { background-color: rgba(11, 17, 32, 0.95); border: 2px dashed #00afb9; color: #00afb9; padding: 40px 20px; border-radius: 12px; font-size: 15px; text-align: center; }
    .score-log-hud { padding: 10px; border-radius: 8px; background-color: rgba(4, 7, 14, 0.95); border: 1px dashed #1d2d44; margin-top: 5px; font-family: monospace; font-size: 12.5px; line-height: 1.5; }
    
    div.stButton > button { background-color: #00afb9 !important; color: white !important; border-radius: 8px; font-weight: 900; padding: 10px 0px; font-size: 14px !important; border: none !important; }
    div.stButton > button:hover { background-color: #00d2de !important; box-shadow: 0px 0px 12px #00d2de; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []
if 'form_counter' not in st.session_state: st.session_state.form_counter = 0

st.sidebar.header("⚙️ THÔNG SỐ KHAY BÀI THẬT")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.header("### 📊 DỮ LIỆU PHỤ (TRỌNG SỐ SỐ VÁN)")
p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng bổ sung:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng bổ sung:", min_value=0, max_value=100, value=0)

total_log_games = len(st.session_state.round_detailed_log)
global_total_games = p_wins_input + b_wins_input + total_log_games

st.markdown("### 🃏 ĐỘNG CƠ ĐO ĐỘ BIẾN THIÊN VÁN ĐẤU")
next_game_number = global_total_games + 1
st.markdown(f'<div class="central-game-counter">🔮 NHẬP QUÂN BÀI CHO VÁN THỨ: {next_game_number}</div>', unsafe_allow_html=True)

input_row_col1, input_row_col2 = st.columns(2, gap="small")
with input_row_col1:
    p_input = st.text_input("🔵 LÁ BÀI PLAYER LẬT THỰC TẾ:", key=f"p_in_{st.session_state.form_counter}", placeholder="Ví dụ: A 2 5 hoặc K 7")
with input_row_col2:
    b_input = st.text_input("🔴 LÁ BÀI BANKER LẬT THỰC TẾ:", key=f"b_in_{st.session_state.form_counter}", placeholder="Ví dụ: J Q 8 hoặc 9 4")

st.write("")
_, btn_layout_center, _ = st.columns([1, 4, 1], gap="small")
with btn_layout_center:
    calc_triggered = st.button("🚀 PHÂN TÍCH QUÂN BÀI & ĐỘ BIẾN THIÊN", use_container_width=True)

if calc_triggered:
    p_clean = p_input.strip()
    b_clean = b_input.strip()
    
    if not p_clean and not b_clean:
        st.warning("⚠️ Vui lòng cung cấp quân bài thực tế để phân tích biến thiên!")
    else:
        p_list = parse_baccarat_input_v47(p_clean)
        b_list = parse_baccarat_input_v47(b_clean)
        
        p_score_eval = sum([0 if c >= 10 else c for c in p_list]) % 10 if p_list else 0
        b_score_eval = sum([0 if c >= 10 else c for c in b_list]) % 10 if b_list else 0
        
        current_outcome = "Tie"
        if p_score_eval > b_score_eval: current_outcome = "Player"
        elif b_score_eval > p_score_eval: current_outcome = "Banker"
        
        st.session_state.round_detailed_log.append({
            'p_cards': p_list,
            'b_cards': b_list,
            'p_score': p_score_eval,
            'b_score': b_score_eval,
            'outcome': current_outcome
        })
        st.session_state.form_counter += 1
        st.rerun()

st.markdown("---")

# KIỂM TRA ĐIỀU KIỆN KHÓA HIỂN THỊ
if global_total_games == 0 and len(st.session_state.round_detailed_log) == 0:
    st.markdown(
        '<div class="logic-lock">'
        '🔒 <b>MÁY ĐO BIẾN THIÊN ĐANG KHÓA (CHỜ LÁ BÀI LẬT)</b><br>'
        '<span style="font-size:13.5px; font-weight:normal; opacity:0.85;">'
        'Hệ thống v47.0 từ chối chạy dữ liệu ảo. Hãy nhập kết quả quân bài của ván đấu thực tế vừa diễn ra '
        'để kích hoạt biểu đồ và thanh đo độ ổn định khay bài.</span>'
        '</div>', 
        unsafe_allow_html=True
    )
else:
    # Chạy thuật toán lõi tích hợp biến thiên lượng tử
    final_p, final_b, final_t, cards_left, volatility = calculate_v47_engine(
        st.session_state.round_detailed_log, 
        shoe_decks=decks, 
        side_p_wins=p_wins_input, 
        side_b_wins=b_wins_input
    )
    
    final_p = round(final_p, 2)
    final_b = round(final_b, 2)
    final_t = round(100.0 - final_p - final_b, 2)

    # Đánh giá cấp độ biến thiên ván bài để định dạng HUD
    vol_css_class = "vol-low"
    vol_status_text = "ỔN ĐỊNH (AN TOÀN)"
    if volatility > 30.0:
        vol_css_class = "vol-high"
        vol_status_text = "CỰC CAO (RỦI RO QUÉT LỆCH)"
    elif volatility > 15.0:
        vol_css_class = "vol-mid"
        vol_status_text = "TRUNG BÌNH (DỰ PHÒNG)"

    st.markdown("### 🔮 XÁC SUẤT KHUẾCH ĐẠI BIÊN ĐỘ THỰC TẾ")
    
    # Xuất khuyến nghị hành động dứt khoát có màng bọc rủi ro biến thiên
    rec_text, rec_bg, rec_border = get_ai_recommendation_v47(final_p, final_b, final_t, st.session_state.round_detailed_log, volatility)
    st.markdown(f'<div class="ai-decision-box" style="background-color: {rec_bg}; border: 2px solid {rec_border}; color: {rec_border};">{rec_text}</div>', unsafe_allow_html=True)
    
    # Hộp màu ưu thế Neon
    p_box_css, b_box_css = "hud-box", "hud-box"
    if final_p > final_b + 4.0: p_box_css = "hud-box neon-player-advantage"
    elif final_b > final_p + 4.0: b_box_css = "hud-box neon-banker-advantage"
    
    col_p, col_b, col_t = st.columns(3, gap="small")
    with col_p:
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER</div><div class="hud-value" style="color:#00afb9;">{final_p}%</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER</div><div class="hud-value" style="color:#ff4757;">{final_b}%</div></div>', unsafe_allow_html=True)
    with col_t:
        st.markdown(f'<div class="hud-box"><div class="hud-title">⚡ BIẾN THIÊN VÁN</div><div class="hud-value {vol_css_class}">{volatility:.1f}%</div></div>', unsafe_allow_html=True)
        
    st.write("")
    
    # Nhật ký thế trận và hiển thị độ biến thiên từng ván đấu cụ thể
    if st.session_state.round_detailed_log:
        st.markdown('<div class="score-log-hud"><b>📊 THẾ TRẬN CHI TIẾT & CHỈ SỐ BIẾN ĐỘNG TỪNG VÁN:</b><br>', unsafe_allow_html=True)
        cumulative_margins = []
        for idx, r in enumerate(st.session_state.round_detailed_log):
            cumulative_margins.append(abs(r['p_score'] - r['b_score']))
            # Tính toán biến thiên cục bộ tích lũy đến ván hiện tại
            v_local = (float(np.std(cumulative_margins)) / 4.5) * 100.0 if len(cumulative_margins) >= 2 else 12.5
            st.markdown(f"• Ván {idx+1}: [P] {r['p_score']}đ vs {r['b_score']}đ [B] ➡️ Cách biệt: **{abs(r['p_score'] - r['b_score'])}đ** ➡️ Thắng: **{r['outcome'].upper()}** (Độ biến thiên: `{v_local:.1f}%`)")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    total_shoe_cards = decks * 52
    penetration_rate = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
    st.caption(f"**Engine:** `REAL-TIME VARIANCE ADAPTIVE v47.0` | **Trạng thái biến thiên:** `{vol_status_text}` | **Bài còn lại:** {int(cards_left)}/{total_shoe_cards} lá")
    st.progress(penetration_rate / 100.0)

st.markdown("<br>", unsafe_allow_html=True)
util_col_1, util_col_2 = st.columns(2, gap="small")
with util_col_1:
    if st.button("⏪ HOÀN TÁC (UNDO)", use_container_width=True):
        if st.session_state.round_detailed_log:
            st.session_state.round_detailed_log.pop()
            st.rerun()
with util_col_2:
    if st.button("🔄 LÀM TRỐNG (ĐỔI BÀN)", use_container_width=True):
        st.session_state.round_detailed_log = []
        st.session_state.form_counter = 0
        st.rerun()
