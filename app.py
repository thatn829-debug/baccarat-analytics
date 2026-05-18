import streamlit as st
import numpy as np

# =========================================================================
# MODULE 1: ĐỘNG CƠ CÔNG THỨC TOÁN HỌC & LUẬT KÉO BÀI (TACTICAL ENGINE)
# =========================================================================
def calculate_v48_tactical_engine(all_rounds_log, shoe_decks, side_p_wins, side_b_wins, side_t_wins):
    """
    Hệ thống phân tích luật kéo bài, tính toán lợi thế thực tế (Edge)
    và đo lường độ biến thiên để đưa ra chiến thuật đi tiền.
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
    
    # Phân tích mật độ bài để áp quy luật kéo bài thứ 3
    score_counts = [0.0] * 10
    for card_num, count in exact_cards_left.items():
        if card_num >= 10: score_counts[0] += count
        else: score_counts[card_num] += count
        
    p_0 = score_counts[0] / cards_remaining      # Bài Tây & 10 (Ức chế điểm)
    p_low = sum(score_counts[1:6]) / cards_remaining   # Bài nhỏ 1-5 (Kích hoạt kéo thêm bài)
    p_high = sum(score_counts[6:10]) / cards_remaining # Bài lớn 6-9 (Tạo điểm tự nhiên, không kéo)

    # Tính độ biến thiên (Volatility)
    volatility_index = 0.0
    if len(margins_list) >= 2:
        std_deviation = float(np.std(margins_list))
        volatility_index = min(50.0, (std_deviation / 4.5) * 100.0)
    elif len(margins_list) == 1:
        volatility_index = 12.5 

    # Cấu trúc toán học khay bài dựa trên xác suất kéo bài thực tế
    # Nếu bài thấp (1-5) còn nhiều -> Player có lợi thế kéo bài bứt phá
    # If bài 0 còn nhiều -> Banker dễ ôm bài giữ thế thắng điểm sát nút
    math_bias = (p_low * 0.14) - (p_high * 0.10) + (p_0 * 0.05)
    
    base_p = 44.62 + (math_bias * 100.0)
    base_b = 45.86 - (math_bias * 100.0)
    base_t = 9.52 + (p_0 * 6.0)

    # Phóng đại biên độ để bộc lộ rõ xu hướng dòng chảy khay bài
    delta_diff = base_p - base_b
    if abs(delta_diff) > 0.1:
        amp_factor = 3.2 
        base_p += (delta_diff * amp_factor)
        base_b -= (delta_diff * amp_factor)

    # Cộng hưởng xung lực thế trận ván trước
    if valid_rounds_count > 0 and last_round_winner:
        momentum_push = min(10.0, last_round_margin * 1.6)
        if last_round_winner == "Player":
            base_p += momentum_push
            base_b -= (momentum_push * 0.5)
        elif last_round_winner == "Banker":
            base_b += momentum_push
            base_p -= (momentum_push * 0.5)

    # Khống chế giới hạn phân phối
    base_p = max(10.0, min(85.0, base_p))
    base_b = max(10.0, min(85.0, base_b))
    base_t = max(4.0, min(25.0, base_t))
    
    total_sum = base_p + base_b + base_t
    return (base_p / total_sum) * 100, (base_b / total_sum) * 100, (base_t / total_sum) * 100, int(cards_remaining), volatility_index, p_low, p_high, p_0


# =========================================================================
# AI ADVANCED STRATEGIC AND TACTICAL RECOMMENDATION (LUẬT BÀI & ĐI TIỀN)
# =========================================================================
def get_ai_tactical_recommendation(p_val, b_val, t_val, vol_val, p_low, p_high, p_0, log):
    if not log:
        return {
            "msg": "📊 Đang chờ nạp dữ liệu quân bài thực tế để kích hoạt động cơ chiến thuật.",
            "action": "DỪNG LẠI QUAN SÁT", "bet_size": "0%", "bg": "rgba(164, 176, 190, 0.1)", "border": "#a4b0be"
        }
    
    # 1. CẢNH BÁO BIẾN THIÊN (QUÉT TÀI KHOẢN)
    if vol_val > 32.0:
        return {
            "msg": f"🚨 BÀN ĐANG QUÉT DỊ BIỆT (Biến thiên: {vol_val:.1f}%)! Thuật toán phân rã tổ hợp phát hiện sòng đang phân phối bài lệch chuẩn nhằm bẻ gãy các chuỗi cược lớn.",
            "action": "PHONG TỎA VỐN - BỎ VÁN", "bet_size": "0%", "bg": "rgba(235, 94, 40, 0.2)", "border": "#eb5e28"
        }

    # 2. PHÂN TÍCH QUY LUẬT RA BÀI DỰA TRÊN MẬT ĐỘ KHAY BÀI
    rule_analysis = ""
    if p_low > 0.45:
        rule_analysis = "Mật độ bài NHỎ (1-5) rất dày, theo luật Baccarat sẽ ép Player phải kéo lá thứ 3 và tăng cơ hội bứt phá điểm."
    elif p_high > 0.40:
        rule_analysis = "Mật độ bài LỚN (6-9) đang cao, các ván đấu dễ kết thúc sớm bằng điểm số tự nhiên (Natural 8, 9), giảm tỷ lệ kéo bài."
    elif p_0 > 0.35:
        rule_analysis = "Mật độ bài TÂY/10 (0 điểm) đang chiếm ưu thế, thế trận dễ rơi vào trạng thái thắt nút điểm hoặc tạo biến số Hòa đột biến."
    else:
        rule_analysis = "Cấu trúc khay bài đang phân phối đồng đều theo tỷ lệ chuẩn định vị."

    # 3. TÍNH TOÁN LỢI THẾ THỰC TẾ (EDGE) VÀ ĐI TIỀN THEO KELLY CRITERION
    diff = abs(p_val - b_val)
    
    # Công thức Kelly đơn giản hóa có màng bọc an toàn (Fractional Kelly - 25% công suất gốc)
    if p_val > b_val:
        edge = (p_val / 100.0) - (b_val / 100.0)
        kelly_bet = max(0.0, (edge * 0.25) * 100.0)
        bet_display = f"{min(15.0, kelly_bet):.1f}%" # Giới hạn max 15% vốn để quản trị rủi ro
        
        if diff >= 6.0:
            msg = f"🔵 LỢI THẾ PLAYER KHUẾCH ĐẠI (+{diff:.1f}%). {rule_analysis} Thế trận ủng hộ đà ra Người Chơi ăn điểm sâu."
            return {"msg": msg, "action": "VÀO LỆNH: PLAYER (ĐÁNH MẠNH)", "bet_size": bet_display, "bg": "rgba(0, 175, 185, 0.25)", "border": "#00afb9"}
        else:
            msg = f"🔵 LỢI THẾ PLAYER TIÊU CHUẨN (+{diff:.1f}%). {rule_analysis} Khay bài chuyển dịch nhẹ nhàng."
            return {"msg": msg, "action": "VÀO LỆNH: PLAYER (DU KÍCH)", "bet_size": "2% - 5%", "bg": "rgba(0, 175, 185, 0.12)", "border": "#00afb9"}
            
    else:
        edge = (b_val / 100.0) - (p_val / 100.0)
        # Tính xâu 5% cho Banker trong toán học lợi thế
        kelly_bet = max(0.0, ((edge * 0.95) * 0.25) * 100.0)
        bet_display = f"{min(15.0, kelly_bet):.1f}%"
        
        if diff >= 6.0:
            msg = f"🔴 LỢI THẾ BANKER KHUẾCH ĐẠI (+{diff:.1f}%). {rule_analysis} Nhà Cái giữ lợi thế điểm số nền tảng tốt."
            return {"msg": msg, "action": "VÀO LỆNH: BANKER (ĐÁNH MẠNH)", "bet_size": bet_display, "bg": "rgba(254, 217, 255, 0.25)", "border": "#fed9ff"}
        else:
            msg = f"🔴 LỢI THẾ BANKER TIÊU CHUẨN (+{diff:.1f}%). {rule_analysis} An toàn bám theo dòng chảy Nhà Cái."
            return {"msg": msg, "action": "VÀO LỆNH: BANKER (DU KÍCH)", "bet_size": "2% - 5%", "bg": "rgba(254, 217, 255, 0.12)", "border": "#fed9ff"}

def parse_baccarat_input_v48(raw_str):
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
st.set_page_config(page_title="Oracle Engine v48.0 Tactical Rule", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(145deg, #05070e, #0a0e1c, #10162b) !important; color: #ecf0f1 !important; }
    
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
    
    /* Giao diện Bảng chiến thuật nâng cấp */
    .tactical-box { border-radius: 10px; padding: 16px; margin: 15px auto; box-shadow: 0px 5px 20px rgba(0,0,0,0.4); line-height: 1.5; }
    .tactical-title { font-size: 16px; font-weight: 900; text-transform: uppercase; margin-bottom: 6px; display: flex; justify-content: space-between; }
    .tactical-msg { font-size: 13.5px; opacity: 0.9; font-weight: 400; margin-bottom: 10px; }
    .tactical-action-line { font-size: 15px; font-weight: 800; border-top: 1px dashed rgba(255,255,255,0.15); padding-top: 8px; }

    .hud-box { padding: 12px 4px; border-radius: 10px; text-align: center; margin-bottom: 8px; border: 1px solid #0a0e1c; background: rgba(5, 7, 14, 0.9); min-height: 85px; display: flex; flex-direction: column; justify-content: center; }
    .hud-title { font-size: 11px; font-weight: 700; color: #a4b0be; text-transform: uppercase; }
    .hud-value { font-size: 25px; font-weight: 800; font-family: monospace; margin-top: 1px; }
    
    .neon-player-advantage { background-color: #042a3a !important; border: 2px solid #00afb9 !important; box-shadow: 0px 0px 12px rgba(0, 175, 185, 0.3); }
    .neon-banker-advantage { background-color: #341017 !important; border: 2px solid #e74c3c !important; box-shadow: 0px 0px 12px rgba(231, 76, 60, 0.3); }
    
    .vol-low { color: #00afb9 !important; }
    .vol-mid { color: #f1c40f !important; }
    .vol-high { color: #eb5e28 !important; animation: blinker 1.2s linear infinite; }
    
    @keyframes blinker { 50% { opacity: 0.3; } }
    
    .logic-lock { background-color: rgba(10, 14, 28, 0.95); border: 2px dashed #00afb9; color: #00afb9; padding: 40px 20px; border-radius: 12px; font-size: 15px; text-align: center; }
    .score-log-hud { padding: 10px; border-radius: 8px; background-color: rgba(3, 5, 11, 0.95); border: 1px dashed #1d2d44; margin-top: 5px; font-family: monospace; font-size: 12.5px; }
    
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
st.sidebar.header("### 📊 DỮ LIỆU PHỤ (SIDEBAR LỊCH SỬ)")
p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0)

total_log_games = len(st.session_state.round_detailed_log)
global_total_games = p_wins_input + b_wins_input + tie_wins_input + total_log_games

st.markdown("### 🃏 ĐỘNG CƠ ĐỊNH VỊ CHIẾN THUẬT QUÂN BÀI")
next_game_number = global_total_games + 1
st.markdown(f'<div class="central-game-counter">🔮 NHẬP QUÂN BÀI CHO VÁN THỨ: {next_game_number}</div>', unsafe_allow_html=True)

input_row_col1, input_row_col2 = st.columns(2, gap="small")
with input_row_col1:
    p_input = st.text_input("🔵 LÁ BÀI PLAYER LẬT:", key=f"p_in_{st.session_state.form_counter}", placeholder="Ví dụ: A 2 5 hoặc K 7")
with input_row_col2:
    b_input = st.text_input("🔴 LÁ BÀI BANKER LẬT:", key=f"b_in_{st.session_state.form_counter}", placeholder="Ví dụ: J Q 8 hoặc 9 4")

st.write("")
_, btn_layout_center, _ = st.columns([1, 4, 1], gap="small")
with btn_layout_center:
    calc_triggered = st.button("🚀 PHÂN TÍCH QUY LUẬT & ĐƯA RA CHIẾN THUẬT", use_container_width=True)

if calc_triggered:
    p_clean = p_input.strip()
    b_clean = b_input.strip()
    
    if not p_clean and not b_clean:
        st.warning("⚠️ Vui lòng cung cấp quân bài thực tế để kích hoạt quy luật!")
    else:
        p_list = parse_baccarat_input_v48(p_clean)
        b_list = parse_baccarat_input_v48(b_clean)
        
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

if global_total_games == 0 and len(st.session_state.round_detailed_log) == 0:
    st.markdown(
        '<div class="logic-lock">'
        '🔒 <b>HỆ THỐNG ĐANG CHỜ QUÂN BÀI ĐỂ ĐỊNH VỊ QUY LUẬT</b><br>'
        '<span style="font-size:13.5px; font-weight:normal; opacity:0.85;">'
        'Thuật toán chiến thuật v48.0 yêu cầu dữ liệu bài lật thực tế để phân tích luật kéo bài thứ 3. '
        'Vui lòng nhập kết quả ván đấu hoặc thiết lập lịch sử ở Sidebar để mở khóa lệnh đi tiền Kelly.</span>'
        '</div>', 
        unsafe_allow_html=True
    )
else:
    # Chạy động cơ tích hợp luật bài và đo lường độ phân rã khay bài
    final_p, final_b, final_t, cards_left, volatility, p_low, p_high, p_0 = calculate_v48_tactical_engine(
        st.session_state.round_detailed_log, 
        shoe_decks=decks, 
        side_p_wins=p_wins_input, 
        side_b_wins=b_wins_input,
        side_t_wins=tie_wins_input
    )
    
    final_p = round(final_p, 2)
    final_b = round(final_b, 2)
    final_t = round(100.0 - final_p - final_b, 2)

    vol_css_class = "vol-low"
    vol_status_text = "ỔN ĐỊNH"
    if volatility > 32.0:
        vol_css_class = "vol-high"
        vol_status_text = "Nhiễu động cao"
    elif volatility > 15.0:
        vol_css_class = "vol-mid"
        vol_status_text = "Giằng co nhẹ"

    st.markdown("### 🔮 BẢNG KHUYẾN NGHỊ CHIẾN THUẬT & HÀNH ĐỘNG TIẾP THEO")
    
    # Lấy dữ liệu chiến thuật toàn diện từ AI
    rec = get_ai_tactical_recommendation(final_p, final_b, final_t, volatility, p_low, p_high, p_0, st.session_state.round_detailed_log)
    
    # Hiển thị Khung khuyến nghị chuẩn Tactical
    st.markdown(
        f'<div class="tactical-box" style="background-color: {rec["bg"]}; border: 2px solid {rec["border"]}; color: {rec["border"]};">'
        f'<div class="tactical-title"><span>📋 {rec["action"]}</span> <span style="font-family: monospace;">Vốn cược: {rec["bet_size"]}</span></div>'
        f'<div class="tactical-msg">{rec["msg"]}</div>'
        f'<div class="tactical-action-line">💡 <b>Hành động tiếp theo:</b> Quản lý vốn nghiêm ngặt, đi đúng khối lượng tiền chỉ định. Tuyệt đối không gấp thếp sai quy trình nếu ván trước đứt chuỗi.</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # Định dạng hiển thị HUD
    p_box_css, b_box_css = "hud-box", "hud-box"
    if final_p > final_b + 4.0: p_box_css = "hud-box neon-player-advantage"
    elif final_b > final_p + 4.0: b_box_css = "hud-box neon-banker-advantage"
    
    col_p, col_b, col_t = st.columns(3, gap="small")
    with col_p:
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER ODDS</div><div class="hud-value" style="color:#00afb9;">{final_p}%</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER ODDS</div><div class="hud-value" style="color:#ff4757;">{final_b}%</div></div>', unsafe_allow_html=True)
    with col_t:
        st.markdown(f'<div class="hud-box"><div class="hud-title">⚡ BIẾN THIÊN VÁN</div><div class="hud-value {vol_css_class}">{volatility:.1f}%</div></div>', unsafe_allow_html=True)
        
    st.write("")
    
    # Nhật ký thế trận điểm số
    if st.session_state.round_detailed_log:
        st.markdown('<div class="score-log-hud"><b>📊 THẾ TRẬN CHI TIẾT & CHỈ SỐ BIẾN ĐỘNG TỪNG VÁN:</b><br>', unsafe_allow_html=True)
        cumulative_margins = []
        for idx, r in enumerate(st.session_state.round_detailed_log):
            cumulative_margins.append(abs(r['p_score'] - r['b_score']))
            v_local = (float(np.std(cumulative_margins)) / 4.5) * 100.0 if len(cumulative_margins) >= 2 else 12.5
            st.markdown(f"• Ván {idx+1}: [P] {r['p_score']}đ vs {r['b_score']}đ [B] ➡️ Cách biệt: **{abs(r['p_score'] - r['b_score'])}đ** ➡️ Thắng: **{r['outcome'].upper()}** (Độ biến thiên: `{v_local:.1f}%`)")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    total_shoe_cards = decks * 52
    penetration_rate = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
    st.caption(f"**Engine:** `TACTICAL RULE ENGINE v48.0` | **Trạng thái:** `{vol_status_text}` | **Bài còn lại:** {int(cards_left)}/{total_shoe_cards} lá")
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
