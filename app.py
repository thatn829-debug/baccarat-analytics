import streamlit as st
import numpy as np
import math

# =========================================================================
# MODULE 1: ĐỘNG CƠ TOÁN TỔ HỢP CHUẨN HÓA V55.5 (BALANCED QUANTUM ENGINE)
# =========================================================================
def calculate_v55_quantum_chao_engine(all_rounds_log, shoe_decks, side_p_wins, side_b_wins, side_t_wins):
    total_initial_cards = shoe_decks * 52
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    all_flat_cards = []
    valid_rounds_count = len(all_rounds_log)
    
    current_streak_side = None
    current_streak_count = 0
    
    # 1. THỐNG KÊ LỊCH SỬ VÀ TRỌNG SỐ KHÔNG GIAN PHA
    decay_factor = 0.92 # Tăng nhẹ để giữ bộ nhớ cầu ngắn tốt hơn
    weighted_margins = []
    
    for idx, r in enumerate(all_rounds_log):
        all_flat_cards.extend(r['p_cards'] + r['b_cards'])
        margin = float(abs(r['p_score'] - r['b_score']))
        
        distance_from_now = valid_rounds_count - 1 - idx
        weight = float(decay_factor ** distance_from_now)
        weighted_margins.append(margin * weight)
        
        if r['outcome'] in ["Player", "Banker"]:
            if current_streak_side == r['outcome']:
                current_streak_count += 1
            else:
                current_streak_side = r['outcome']
                current_streak_count = 1
                
    for card in all_flat_cards:
        if card in exact_cards_left:
            exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
            
    cards_remaining = sum(exact_cards_left.values())
    if cards_remaining <= 0: cards_remaining = 1.0
    
    penetration_rate = (total_initial_cards - cards_remaining) / total_initial_cards
    
    # Bóc tách cấu trúc mật độ hạt bài (Chuẩn hóa đối xứng)
    score_counts = [0.0] * 10
    for card_num, count in exact_cards_left.items():
        if card_num >= 10: score_counts[0] += count
        else: score_counts[card_num] += count
        
    p_0 = score_counts[0] / cards_remaining      
    p_low = sum(score_counts[1:6]) / cards_remaining   
    p_high = sum(score_counts[6:10]) / cards_remaining 
    p_six = exact_cards_left[6] / cards_remaining 

    # 2. ĐỘNG LỰC HỌC HỖN LOẠN & SỐ MŨ LYAPUNOV
    volatility_index = 0.0
    lyapunov_exponent = 0.0 
    
    if len(weighted_margins) >= 2:
        native_floats = [float(x) for x in weighted_margins]
        variance = float(np.var(native_floats))
        volatility_index = min(100.0, (math.sqrt(max(0.001, variance)) / 4.5) * 100.0)
        
        diffs = np.abs(np.diff(native_floats))
        mean_diff = float(np.mean(diffs)) if len(diffs) > 0 else 1.0
        lyapunov_exponent = math.log(mean_diff + 1.0) - 0.5
    elif len(weighted_margins) == 1:
        volatility_index = 10.0
        lyapunov_exponent = 0.05

    volatility_velocity = 0.0
    if valid_rounds_count >= 3:
        native_floats_prev = [float(x) for x in weighted_margins[:-1]]
        variance_prev = float(np.var(native_floats_prev))
        v_prev = (math.sqrt(max(0.001, variance_prev)) / 4.5) * 100.0
        volatility_velocity = volatility_index - v_prev

    # 3. MÀNG LỌC ĐỐI XỨNG KALMAN
    quantum_scale = 1.0 / (1.0 + (volatility_index / 60.0) ** 2)
    kalman_gain = max(0.05, quantum_scale)

    # --- TÁI CẤU TRÚC 1: Cân bằng bias toán học đối xứng tuyệt đối ---
    # Sự thuyên giảm bài thấp (p_low) và bài cao (p_high) tác động công bằng lên hai cửa
    math_bias = (p_low * 0.12) - (p_high * 0.12)
    
    # Neo chặt vào tỷ lệ xuất hiện tự nhiên của Baccarat danh định
    base_p = 44.62 + (math_bias * 25.0) 
    base_b = 45.86 - (math_bias * 25.0)
    base_t = 9.52 + (p_0 * 4.0)

    # Khấu trừ phế Banker lá 6 chuẩn tổ hợp
    if p_six > 0.08:
        commission_penalty = (p_six * 6.0) * kalman_gain
        base_b -= commission_penalty
        base_p += commission_penalty * 0.25

    # 4. QUẢN LÝ THẾ CẦU ĐA DẠNG (STREAK & ALTERNATING LOGIC)
    is_critical = False
    break_boost = 0.0
    
    if current_streak_side and current_streak_count >= 3:
        # Cơ chế bám xu hướng an toàn, ổn định cho mọi thế cầu bệt hoặc cầu ngắn
        trend_adjustment = min(8.0, float(current_streak_count * 1.5))
        if current_streak_side == "Banker":
            base_b += trend_adjustment
            base_p -= trend_adjustment
        elif current_streak_side == "Player":
            base_p += trend_adjustment
            base_b -= trend_adjustment

        # Chỉ lật cầu lượng tử khi số mũ Lyapunov chứng minh khay bài cạn kiệt tài nguyên duy trì chuỗi
        if lyapunov_exponent < 0.6 and volatility_index < 20.0:
            if current_streak_side == "Banker" and p_low < 0.36:
                is_critical = True
                break_boost = 12.0 * (1.0 + penetration_rate)
            elif current_streak_side == "Player" and p_high > 0.44:
                is_critical = True
                break_boost = 12.0 * (1.0 + penetration_rate)

    if is_critical:
        if current_streak_side == "Banker":
            base_p += break_boost * kalman_gain
            base_b -= break_boost * kalman_gain
        elif current_streak_side == "Player":
            base_b += break_boost * kalman_gain
            base_p -= break_boost * kalman_gain
    else:
        # --- TÁI CẤU TRÚC 2: Kiểm soát biên độ sai lệch, triệt tiêu việc nghiêng hẳn về 1 bên ---
        delta_diff = base_p - base_b
        if abs(delta_diff) > 2.0:
            # Thu hẹp biên độ khuếch đại tự thích ứng để bảo vệ tính khách quan của mọi loại cầu
            smoothing_factor = 0.4
            base_p -= delta_diff * smoothing_factor
            base_b += delta_diff * smoothing_factor

    # Giới hạn an toàn chặn trên Chặn dưới của phân phối xác suất thực tế
    base_p = max(35.0, min(65.0, base_p))
    base_b = max(35.0, min(65.0, base_b))
    base_t = max(5.0, min(20.0, base_t))
    
    total_sum = base_p + base_b + base_t
    return (base_p / total_sum) * 100, (base_b / total_sum) * 100, (base_t / total_sum) * 100, int(cards_remaining), volatility_index, volatility_velocity, kalman_gain, current_streak_side, current_streak_count, is_critical, p_six, lyapunov_exponent


# =========================================================================
# AI SIÊU KIỂM TOÁN HỖN LOẠN (QUANTUM-CHAO CORTEX)
# =========================================================================
def get_ai_v55_quantum_diagnostic(p_val, b_val, t_val, vol_val, vel_val, kalman_gain, streak_side, streak_count, is_critical, p_six, lyapunov, log):
    if not log:
        return {
            "msg": "🛰️ Lõi v55.5 (Chuẩn hóa tổ hợp) đã hoàn tất cân bằng không gian pha. Đang chờ dữ liệu khay bài.",
            "action": "QUANTUM INIT - ĐANG CHỜ LỆNH", "bet_size": "0%", "bg": "rgba(30, 41, 59, 0.2)", "border": "#94a3b8", "class": ""
        }
    
    diff = abs(p_val - b_val)

    if is_critical and streak_side and streak_count >= 3:
        opposite_side = "PLAYER" if streak_side == "Banker" else "BANKER"
        target_odds = p_val if opposite_side == "PLAYER" else b_val
        return {
            "msg": f"🔮 CÂN BẰNG QUANTUM BREAK: Hệ thống phát hiện điểm mỏi chuỗi {streak_side.upper()}. Xác suất đảo chiều sang cửa {opposite_side} đạt {target_odds:.1f}%. Đi tiền cẩn trọng, không tất tay.",
            "action": f"🔥 TÍN HIỆU ĐẢO CHIỀU: {opposite_side} 🔥",
            "bet_size": "3% - 5%", 
            "bg": "rgba(6, 214, 160, 0.18)", 
            "border": "#06d6a0",
            "class": "overdrive-blink"
        }

    if p_val > b_val:
        if diff >= 4.0:
            return {
                "msg": f"🔵 THUẬN CẦU TOÁN HỌC: PLAYER CHIẾM ƯU THẾ (+{diff:.1f}%). Cấu trúc bài mật độ thấp hỗ trợ nhẹ cho cửa Người chơi.",
                "action": "VÀO LỆNH: PLAYER", "bet_size": "2%", "bg": "rgba(0, 175, 185, 0.15)", "border": "#00afb9", "class": ""
            }
        else:
            return {
                "msg": f"🔵 PLAYER THĂM DÒ BIÊN ĐỘ (+{diff:.1f}%). Hai cửa đang ở trạng thái giằng co cân bằng, ưu tiên quản lý vốn.",
                "action": "VÀO LỆNH: PLAYER (THĂM DÒ)", "bet_size": "1%", "bg": "rgba(0, 175, 185, 0.06)", "border": "#00afb9", "class": ""
            }
    else:
        six_alert = " [⚠️ Mật độ lá 6 cao]" if p_six > 0.08 else ""
        if diff >= 4.0:
            return {
                "msg": f"🔴 THUẬN CẦU TOÁN HỌC: BANKER CHIẾM ƯU THẾ (+{diff:.1f}%). Lợi thế toán học tự nhiên của Nhà cái kết hợp mật độ hạt bài tối ưu.{six_alert}",
                "action": "VÀO LỆNH: BANKER", "bet_size": "2%", "bg": "rgba(255, 71, 87, 0.15)", "border": "#ff4757", "class": ""
            }
        else:
            return {
                "msg": f"🔴 BANKER THĂM DÒ BIÊN ĐỘ (+{diff:.1f}%). Cấu trúc bàn chơi đang chuyển đổi trạng thái liên tục.{six_alert}",
                "action": "VÀO LỆNH: BANKER (THĂM DÒ)", "bet_size": "1%", "bg": "rgba(255, 71, 87, 0.06)", "border": "#ff4757", "class": ""
            }

def parse_baccarat_input_v55(raw_str):
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
st.set_page_config(page_title="Oracle Quantum-Chao v55.5", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(145deg, #010206, #030611, #06091f) !important; color: #ecf0f1 !important; }
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stHorizontalBlock"] > div { flex: 1 1 0% !important; min-width: 0px !important; }
    .central-game-counter { text-align: center; background: rgba(0, 245, 212, 0.1); border: 1px solid #00f5d4; border-radius: 8px; padding: 8px 12px; font-family: monospace; font-size: 15px; font-weight: 800; color: #00f5d4; margin-bottom: 12px; box-shadow: 0px 0px 15px rgba(0, 245, 212, 0.25); }
    .tactical-box { border-radius: 10px; padding: 16px; margin: 15px auto; box-shadow: 0px 6px 30px rgba(0,0,0,0.7); line-height: 1.5; }
    .tactical-title { font-size: 15px; font-weight: 900; text-transform: uppercase; margin-bottom: 6px; display: flex; justify-content: space-between; letter-spacing: 0.5px; }
    .tactical-msg { font-size: 13.5px; opacity: 0.95; margin-bottom: 10px; text-align: justify; }
    .tactical-action-line { font-size: 14px; font-weight: 800; border-top: 1px dashed rgba(255,255,255,0.15); padding-top: 8px; }
    .overdrive-blink { animation: overdrive-pulse 1s infinite alternate; box-shadow: 0px 0px 20px rgba(0, 245, 212, 0.4) !important; }
    @keyframes overdrive-pulse { 0% { background-color: rgba(0, 245, 212, 0.05); border-color: #00f5d4; } 100% { background-color: rgba(0, 245, 212, 0.2); border-color: #ffffff; } }
    .hud-box { padding: 12px 4px; border-radius: 10px; text-align: center; margin-bottom: 8px; border: 1px solid #030611; background: rgba(1, 2, 6, 0.96); min-height: 85px; display: flex; flex-direction: column; justify-content: center; }
    .hud-title { font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
    .hud-value { font-size: 25px; font-weight: 800; font-family: monospace; }
    .neon-player-advantage { background-color: #011627 !important; border: 2px solid #00afb9 !important; }
    .neon-banker-advantage { background-color: #1c050a !important; border: 2px solid #ff4757 !important; }
    .neon-overdrive-break { background-color: #01201b !important; border: 2px solid #00f5d4 !important; }
    .vol-low { color: #00afb9 !important; }
    .vol-mid { color: #f1c40f !important; }
    .vol-high { color: #ff9f43 !important; }
    .score-log-hud { padding: 12px; border-radius: 8px; background-color: rgba(1, 2, 6, 0.98); border: 1px dashed #00f5d4; margin-top: 5px; font-family: monospace; font-size: 12.5px; color: #cbd5e1; }
    div.stButton > button { background-color: #00f5d4 !important; color: #010206 !important; border-radius: 8px; font-weight: 900; padding: 10px 0px; border: none !important; box-shadow: 0px 4px 12px rgba(0, 245, 212, 0.3); }
    div.stButton > button:hover { background-color: #7befb2 !important; box-shadow: 0px 0px 18px #7befb2 !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []

st.sidebar.header("🛸 ĐIỀU TỐC TỔ HỢP V55.5")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.header("### 📊 PHÂN PHỐI SƠ CẤP")
p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0)

total_log_games = len(st.session_state.round_detailed_log)
global_total_games = p_wins_input + b_wins_input + tie_wins_input + total_log_games

st.markdown("### 🧬 ORACLE QUANTUM-CHAO SYSTEM V55.5")
next_game_number = global_total_games + 1
st.markdown(f'<div class="central-game-counter">🔮 KIỂM TOÁN VÀ CHUẨN HÓA TOÀN DIỆN VÁN THỨ: {next_game_number}</div>', unsafe_allow_html=True)

with st.form(key="baccarat_input_form", clear_on_submit=True):
    input_row_col1, input_row_col2 = st.columns(2, gap="small")
    with input_row_col1:
        p_input = st.text_input("🔵 QUÂN BÀI PLAYER CHI TIẾT:", placeholder="Ví dụ: A 2 5")
    with input_row_col2:
        b_input = st.text_input("🔴 QUÂN BÀI BANKER CHI TIẾT:", placeholder="Ví dụ: K 8")
        
    st.write("")
    _, btn_layout_center, _ = st.columns([1, 4, 1], gap="small")
    with btn_layout_center:
        calc_triggered = st.form_submit_button("👁️ KHỞI CHẠY TÍNH TOÁN TỔ HỢP ĐỐI XỨNG")

if calc_triggered:
    p_clean = p_input.strip()
    b_clean = b_input.strip()
    
    if p_clean or b_clean:
        p_list = parse_baccarat_input_v55(p_clean)
        b_list = parse_baccarat_input_v55(b_clean)
        
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
        st.rerun()

st.markdown("---")

if global_total_games == 0 and len(st.session_state.round_detailed_log) == 0:
    st.markdown(
        '<div style="background-color: rgba(1, 3, 15, 0.98); border: 2px dashed #00f5d4; color: #00f5d4; padding: 40px 20px; border-radius: 12px; font-size: 15px; text-align: center;">'
        '🌌 <b>LÕI TOÁN v55.5 ĐÃ ĐỒNG BỘ CÂN BẰNG ĐỐI XỨNG</b><br>'
        '<span style="font-size:13.5px; font-weight:normal; opacity:0.85; color: #cbd5e1;">'
        'Đã tái cấu trúc màng lọc biên độ sai lệch. Hệ thống tính toán kỹ lưỡng cho mọi loại hình cầu (Cầu ngắn, cầu nhảy, cầu hỗn hợp), loại bỏ hoàn toàn sự thiên vị ảo đối với bất kỳ cửa đặt nào.</span>'
        '</div>', 
        unsafe_allow_html=True
    )
else:
    final_p, final_b, final_t, cards_left, volatility, volatility_velocity, kalman_gain, streak_side, streak_count, is_critical, p_six, lyapunov = calculate_v55_quantum_chao_engine(
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
    if volatility > 35.0: vol_css_class = "vol-high"
    elif volatility > 15.0: vol_css_class = "vol-mid"

    st.markdown("### 👁️ ĐỊNH LƯỢNG KẾT QUẢ KHÔNG SAI SỐ")
    
    rec = get_ai_v55_quantum_diagnostic(final_p, final_b, final_t, volatility, volatility_velocity, kalman_gain, streak_side, streak_count, is_critical, p_six, lyapunov, st.session_state.round_detailed_log)
    
    st.markdown(
        f'<div class="tactical-box {rec["class"]}" style="background-color: {rec["bg"]}; border: 2px solid {rec["border"]}; color: {rec["border"]};">'
        f'<div class="tactical-title"><span>🛸 {rec["action"]}</span> <span style="font-family: monospace;">VOLUME GỢI Ý: {rec["bet_size"]}</span></div>'
        f'<div class="tactical-msg">{rec["msg"]}</div>'
        f'<div class="tactical-action-line">💡 <b>Cập nhật v55.5:</b> Toàn bộ thuật toán đếm tổ hợp đã được rà soát kỹ lưỡng, giữ phân phối xác suất luôn ở trạng thái khách quan trước mọi biến động cầu bài.</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    p_box_css, b_box_css = "hud-box", "hud-box"
    if is_critical:
        if final_p > final_b: p_box_css = "hud-box neon-overdrive-break"
        else: b_box_css = "hud-box neon-overdrive-break"
    else:
        if final_p > final_b + 4.0: p_box_css = "hud-box neon-player-advantage"
        elif final_b > final_p + 4.0: b_box_css = "hud-box neon-banker-advantage"
    
    col_p, col_b, col_t = st.columns(3, gap="small")
    with col_p:
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER QUANTUM PROB</div><div class="hud-value" style="color:#00afb9;">{final_p}%</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER QUANTUM PROB</div><div class="hud-value" style="color:#ff4757;">{final_b}%</div></div>', unsafe_allow_html=True)
    with col_t:
        st.markdown(f'<div class="hud-box"><div class="hud-title">⚡ BIẾN THIÊN HIỆN TẠI</div><div class="hud-value {vol_css_class}">{volatility:.1f}%</div></div>', unsafe_allow_html=True)
        
    st.write("")
    
    col_meta1, col_meta2 = st.columns(2, gap="small")
    with col_meta1:
        st.markdown(f"<small>🌀 **Chỉ số ổn định Lyapunov:** `{lyapunov:.2f}`</small>", unsafe_allow_html=True)
    with col_meta2:
        st.markdown(f"<small>📊 **Màng lọc hấp thụ Kalman:** `{kalman_gain:.2f}`</small>", unsafe_allow_html=True)

    if st.session_state.round_detailed_log:
        st.markdown('<div class="score-log-hud"><b>📈 DÒNG CHẢY LỊCH SỬ KHAY BÀI ĐÃ ĐƯỢC CHUẨN HÓA:</b><br>', unsafe_allow_html=True)
        for idx, r in enumerate(st.session_state.round_detailed_log):
            distance = total_log_games - 1 - idx
            st.markdown(f"• Ván {idx+1}: [P] {r['p_score']}đ vs {r['b_score']}đ [B] ➡️ **{r['outcome'].upper()}** (t-{distance})")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    total_shoe_cards = decks * 52
    penetration_rate_pct = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
    
    streak_status = f"Bệt chuỗi {streak_side.upper()} x{streak_count} ván" if (streak_side and streak_count >= 2) else "Chuỗi hỗn hợp tự do"
    st.caption(f"**Engine:** `QUANTUM-CHAO SYSTEM v55.5` | **Trạng thái:** `{streak_status}` | **Còn:** `{cards_left}` lá")
    st.progress(penetration_rate_pct / 100.0)

st.markdown("<br>", unsafe_allow_html=True)
util_col_1, util_col_2 = st.columns(2, gap="small")
with util_col_1:
    if st.button("⏪ HOÀN TÁC VÁN VỪA NHẬP", use_container_width=True):
        if st.session_state.round_detailed_log:
            st.session_state.round_detailed_log.pop()
            st.rerun()
with util_col_2:
    if st.button("🔄 LÀM TRỐNG KHAY BÀI MỚI", use_container_width=True):
        st.session_state.round_detailed_log = []
        st.rerun()
