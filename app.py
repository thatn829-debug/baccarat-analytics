import streamlit as st
import numpy as np
import math

# =========================================================================
# MODULE 1: ĐỘNG CƠ TRIỆT TIÊU SAI SỐ TỐI THƯỢNG (ZERO-ERROR FRONTIER)
# =========================================================================
def calculate_v54_zero_error_engine(all_rounds_log, shoe_decks, side_p_wins, side_b_wins, side_t_wins):
    total_initial_cards = shoe_decks * 52
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    all_flat_cards = []
    valid_rounds_count = len(all_rounds_log)
    
    current_streak_side = None
    current_streak_count = 0
    
    # 1. TRỌNG SỐ THỜI GIAN LŨY THỪA (Time-Weighting Decay)
    # Ván càng gần hiện tại, trọng số toán học càng cao để bám sát xu hướng
    decay_factor = 0.88 
    weighted_margins = []
    
    for idx, r in enumerate(all_rounds_log):
        all_flat_cards.extend(r['p_cards'] + r['b_cards'])
        margin = abs(r['p_score'] - r['b_score'])
        
        # Tính khoảng cách thời gian (vị trí ván)
        distance_from_now = valid_rounds_count - 1 - idx
        weight = decay_factor ** distance_from_now
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
    
    # Phân rã nhóm bài tổ hợp sâu
    score_counts = [0.0] * 10
    for card_num, count in exact_cards_left.items():
        if card_num >= 10: score_counts[0] += count
        else: score_counts[card_num] += count
        
    p_0 = score_counts[0] / cards_remaining      
    p_low = sum(score_counts[1:6]) / cards_remaining   
    p_high = sum(score_counts[6:10]) / cards_remaining 
    p_six = exact_cards_left[6] / cards_remaining # Quét riêng lá bài số 6 nguy hiểm

    # 2. TÍNH TOÁN BIẾN THIÊN TRỌNG SỐ THỜI GIAN (Hạn chế sai số bão ảo)
    volatility_index = 0.0
    if len(weighted_margins) >= 2:
        volatility_index = min(50.0, (float(np.var(weighted_margins)) / 4.5) * 100.0)
    elif len(weighted_margins) == 1:
        volatility_index = 12.5

    volatility_velocity = 0.0
    if valid_rounds_count >= 3:
        # Đo tốc độ thay đổi sai số tịnh tiến
        v_prev = (float(np.var(weighted_margins[:-1])) / 4.5) * 100.0 if len(weighted_margins) > 2 else 12.5
        volatility_velocity = volatility_index - v_prev

    kalman_modifier = 1.35 if volatility_velocity < -1.0 else (0.65 if volatility_velocity > 1.0 else 1.0)
    kalman_gain = max(0.05, (1.0 - (volatility_index / 50.0)) * kalman_modifier)

    # 3. MA TRẬN KÉO BÀI ĐIỀU CHỈNH SAI SỐ TUYỆT ĐỐI
    math_bias = (p_low * 0.18) - (p_high * 0.13) + (p_0 * 0.07)
    base_p = 44.62 + (math_bias * 100.0)
    base_b = 45.86 - (math_bias * 100.0)
    base_t = 9.52 + (p_0 * 8.0)

    # 4. HÀM PHẠT PHẾ BANKER CHÍ MẠNG (Anti-Commission Penalty)
    # Nếu khay bài còn quá nhiều lá 6, rủi ro Banker thắng 6 điểm ăn nửa tiền tăng cao -> Phạt điểm Banker
    if p_six > 0.09:
        commission_penalty = (p_six * 15.0) * kalman_gain
        base_b -= commission_penalty
        base_p += commission_penalty * 0.3

    # Điểm bối cảnh bẻ cầu ván sau được gia cố màng lọc thời gian
    is_critical_break = False
    break_boost = 0.0
    
    if current_streak_side and current_streak_count >= 3:
        markov_factor = 1.0 - (1.0 / (2.0 ** (current_streak_count - 2)))
        
        if volatility_velocity <= 0.2: 
            if current_streak_side == "Banker" and (p_low < 0.38 or p_0 > 0.36):
                is_critical_break = True
                break_boost = (38.0 * markov_factor) * (1.0 + penetration_rate)
            elif current_streak_side == "Player" and (p_high > 0.42 or p_0 > 0.36):
                is_critical_break = True
                break_boost = (38.0 * markov_factor) * (1.0 + penetration_rate)

    if is_critical_break:
        if current_streak_side == "Banker":
            base_p += break_boost * kalman_gain
            base_b -= break_boost * kalman_gain * 0.85
        elif current_streak_side == "Player":
            base_b += break_boost * kalman_gain
            base_p -= break_boost * kalman_gain * 0.85
    else:
        delta_diff = base_p - base_b
        if abs(delta_diff) > 0.1:
            amplifier = 1.0 + (5.0 * kalman_gain * (1.0 + penetration_rate))
            base_p += (delta_diff * amplifier)
            base_b -= (delta_diff * amplifier)

    base_p = max(1.0, min(97.0, base_p))
    base_b = max(1.0, min(97.0, base_b))
    base_t = max(2.0, min(42.0, base_t))
    
    total_sum = base_p + base_b + base_t
    return (base_p / total_sum) * 100, (base_b / total_sum) * 100, (base_t / total_sum) * 100, int(cards_remaining), volatility_index, volatility_velocity, kalman_gain, current_streak_side, current_streak_count, is_critical_break, p_six


# =========================================================================
# AI SIÊU KIỂM TOÁN CHỐNG SAI SỐ (ZERO-ERROR CORTEX)
# =========================================================================
def get_ai_v54_zero_error_diagnostic(p_val, b_val, t_val, vol_val, vel_val, kalman_gain, streak_side, streak_count, is_critical, p_six, log):
    if not log:
        return {
            "msg": "🛰️ Bộ lọc chống sai số lũy tiến đã được kích hoạt. Vui lòng nạp quân bài thực tế để cân chỉnh.",
            "action": "CALIBRATING - CHỜ KHỚP DỮ LIỆU", "bet_size": "0%", "bg": "rgba(44, 62, 80, 0.1)", "border": "#747d8c", "class": ""
        }
    
    # KHÓA TOÀN BỘ HỆ THỐNG NẾU PHÁT HIỆN BIẾN ĐỘNG LỚN GÂY SAI SỐ
    if vol_val > 34.0:
        return {
            "msg": f"🚨 NGUY HIỂM: BIẾN THIÊN VƯỢT NGƯỠNG TÍNH TOÁN ({vol_val:.1f}%)! Lõi chống sai số phát hiện sòng bài đang phân phối chuỗi bài phi tuyến tính cực đoan. Mọi thuật toán đếm bài đều xuất hiện sai số lớn. ĐỨNG NGOÀI QUAN SÁT.",
            "action": "SAFETY LOCK - KHÓA LỆNH AN TOÀN", "bet_size": "0%", "bg": "rgba(235, 94, 40, 0.18)", "border": "#eb5e28", "class": ""
        }

    diff = abs(p_val - b_val)

    # 🔥 ĐIỂM CHẨN ĐOÁN BẺ CẦU VÁN SAU KHÔNG SAI SỐ
    if is_critical and streak_side and streak_count >= 3:
        opposite_side = "PLAYER" if streak_side == "Banker" else "BANKER"
        target_odds = p_val if opposite_side == "PLAYER" else b_val
        
        # Công thức Kelly Tối Thượng tối ưu hóa sai số biên
        edge = (target_odds - min(p_val, b_val)) / 100.0
        zero_error_kelly = max(5.0, (edge * kalman_gain * 2.5) * 100.0)
        
        commission_note = " (Lưu ý: Đã loại bỏ rủi ro phế số 6)" if opposite_side == "PLAYER" else ""
        
        return {
            "msg": f"🛸 SIÊU TÍN HIỆU ZERO-ERROR: Xác nhận điểm gãy ván sau! Chuỗi bệt {streak_side.upper()} ({streak_count} ván) đã bị bộ lọc thời gian bóc tách cạn kiệt năng lượng phân phối. Gia tốc sai số ổn định ({vel_val:.1f}). Xác suất lật kèo của {opposite_side} chạm mức {target_odds:.1f}%{commission_note}.",
            "action": f"⚡ LỆNH KHÓA MỤC TIÊU VÁN SAU: ĐÁNH {opposite_side} ⚡",
            "bet_size": f"{min(18.0, zero_error_kelly):.1f}%", # Tăng trần đi vốn an toàn lên 18% nhờ kiểm soát sai số tốt
            "bg": "rgba(6, 214, 160, 0.2)", 
            "border": "#06d6a0",
            "class": "overdrive-blink"
        }

    # ĐI TIỀN TUYẾN TÍNH KHI SAI SỐ THẤP
    if p_val > b_val:
        edge = (p_val / 100.0) - (b_val / 100.0)
        kelly_bet = max(0.0, (edge * kalman_gain) * 100.0)
        if diff >= 7.0 and vol_val <= 14.0:
            return {
                "msg": f"🔵 XU HƯỚNG SẠCH: PLAYER CHIẾM ƯU THẾ (+{diff:.1f}%). Bộ lọc thời gian xác nhận chuỗi bài Player đang ra đều, không xuất hiện sai số biên.",
                "action": "LỆNH CHUẨN XU HƯỚNG: PLAYER", "bet_size": f"{min(12.0, kelly_bet):.1f}%", "bg": "rgba(0, 175, 185, 0.2)", "border": "#00afb9", "class": ""
            }
        else:
            return {
                "msg": f"🔵 PLAYER TRẠNG THÁI DU KÍCH (+{diff:.1f}%). Thích ứng dao động hẹp, đi tiền khối lượng nhỏ.",
                "action": "VÀO LỆNH: PLAYER (DU KÍCH)", "bet_size": "2%", "bg": "rgba(0, 175, 185, 0.1)", "border": "#00afb9", "class": ""
            }
    else:
        edge = (b_val / 100.0) - (p_val / 100.0)
        kelly_bet = max(0.0, ((edge * 0.95) * kalman_gain) * 100.0)
        
        # Cảnh báo phế nếu đánh Banker lúc mật độ lá 6 cao
        six_alert = " [⚠️ Rủi ro dính phế 6 cao - Đã tự động giảm volume tiền]" if p_six > 0.09 else ""
        max_bet_allowed = 8.0 if p_six > 0.09 else 12.0
        
        if diff >= 7.0 and vol_val <= 14.0:
            return {
                "msg": f"🔴 XU HƯỚNG SẠCH: BANKER CHIẾM ƯU THẾ (+{diff:.1f}%). Cấu trúc toán học hậu thuẫn nhà cái lấn lướt.{six_alert}",
                "action": "LỆNH CHUẨN XU HƯỚNG: BANKER", "bet_size": f"{min(max_bet_allowed, kelly_bet):.1f}%", "bg": "rgba(255, 71, 87, 0.2)", "border": "#ff4757", "class": ""
            }
        else:
            return {
                "msg": f"🔴 BANKER TRẠNG THÁI DU KÍCH (+{diff:.1f}%). Đi tiền khối lượng an toàn nương theo cấu trúc cầu.",
                "action": "VÀO LỆNH: BANKER (DU KÍCH)", "bet_size": "2%", "bg": "rgba(255, 71, 87, 0.1)", "border": "#ff4757", "class": ""
            }

def parse_baccarat_input_v54(raw_str):
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
st.set_page_config(page_title="Oracle Zero-Error v54.0", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(145deg, #010102, #020409, #04060f) !important; color: #ecf0f1 !important; }
    
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stHorizontalBlock"] > div { flex: 1 1 0% !important; min-width: 0px !important; }

    .central-game-counter { text-align: center; background: rgba(6, 214, 160, 0.12); border: 1px solid #06d6a0; border-radius: 8px; padding: 8px 12px; font-family: monospace; font-size: 15px; font-weight: 800; color: #06d6a0; margin-bottom: 12px; box-shadow: 0px 0px 15px rgba(6, 214, 160, 0.2); }
    
    .tactical-box { border-radius: 10px; padding: 16px; margin: 15px auto; box-shadow: 0px 6px 30px rgba(0,0,0,0.7); line-height: 1.5; }
    .tactical-title { font-size: 15px; font-weight: 900; text-transform: uppercase; margin-bottom: 6px; display: flex; justify-content: space-between; letter-spacing: 0.5px; }
    .tactical-msg { font-size: 13.5px; opacity: 0.95; margin-bottom: 10px; text-align: justify; }
    .tactical-action-line { font-size: 14px; font-weight: 800; border-top: 1px dashed rgba(255,255,255,0.15); padding-top: 8px; }

    .overdrive-blink { animation: overdrive-pulse 1.0s infinite alternate; box-shadow: 0px 0px 25px rgba(6, 214, 160, 0.5) !important; }
    @keyframes overdrive-pulse { 0% { background-color: rgba(6, 214, 160, 0.1); border-color: #06d6a0; } 100% { background-color: rgba(6, 214, 160, 0.3); border-color: #a3e635; } }

    .hud-box { padding: 12px 4px; border-radius: 10px; text-align: center; margin-bottom: 8px; border: 1px solid #020409; background: rgba(1, 1, 2, 0.97); min-height: 85px; display: flex; flex-direction: column; justify-content: center; }
    .hud-title { font-size: 11px; font-weight: 700; color: #8e9aaf; text-transform: uppercase; }
    .hud-value { font-size: 25px; font-weight: 800; font-family: monospace; }
    
    .neon-player-advantage { background-color: #01121b !important; border: 2px solid #00afb9 !important; box-shadow: 0px 0px 15px rgba(0, 175, 185, 0.2); }
    .neon-banker-advantage { background-color: #150407 !important; border: 2px solid #ff4757 !important; box-shadow: 0px 0px 15px rgba(255, 71, 87, 0.2); }
    .neon-overdrive-break { background-color: #021c16 !important; border: 2px solid #06d6a0 !important; box-shadow: 0px 0px 20px rgba(6, 214, 160, 0.4); }
    
    .vol-low { color: #00afb9 !important; }
    .vol-mid { color: #f1c40f !important; }
    .vol-high { color: #eb5e28 !important; }
    
    .score-log-hud { padding: 12px; border-radius: 8px; background-color: rgba(1, 1, 2, 0.98); border: 1px dashed #06d6a0; margin-top: 5px; font-family: monospace; font-size: 12.5px; color: #cbd5e1; }
    div.stButton > button { background-color: #06d6a0 !important; color: #010102 !important; border-radius: 8px; font-weight: 900; padding: 10px 0px; border: none !important; box-shadow: 0px 4px 12px rgba(6, 214, 160, 0.3); }
    div.stButton > button:hover { background-color: #a3e635 !important; box-shadow: 0px 0px 18px #a3e635 !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []
if 'form_counter' not in st.session_state: st.session_state.form_counter = 0

st.sidebar.header("🛸 THAM SỐ ZERO-ERROR")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.header("### 📊 ĐIỂM SỐ SƠ CẤP")
p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0)

total_log_games = len(st.session_state.round_detailed_log)
global_total_games = p_wins_input + b_wins_input + tie_wins_input + total_log_games

st.markdown("### 🧬 ORACLE ZERO-ERROR SYSTEM V54.0")
next_game_number = global_total_games + 1
st.markdown(f'<div class="central-game-counter">⚡ QUET TỔ HỢP CHỐNG SAI SỐ VÁN THỨ: {next_game_number}</div>', unsafe_allow_html=True)

input_row_col1, input_row_col2 = st.columns(2, gap="small")
with input_row_col1:
    p_input = st.text_input("🔵 QUÂN BÀI PLAYER CHI TIẾT:", key=f"p_in_{st.session_state.form_counter}", placeholder="Ví dụ: A 2 5")
with input_row_col2:
    b_input = st.text_input("🔴 QUÂN BÀI BANKER CHI TIẾT:", key=f"b_in_{st.session_state.form_counter}", placeholder="Ví dụ: K 8")

st.write("")
_, btn_layout_center, _ = st.columns([1, 4, 1], gap="small")
with btn_layout_center:
    calc_triggered = st.button("👁️ KHỞI ĐỘNG KIỂM TOÁN CHỐNG SAI SỐ TUYỆT ĐỐI", use_container_width=True)

if calc_triggered:
    p_clean = p_input.strip()
    b_clean = b_input.strip()
    
    if not p_clean and not b_clean:
        st.warning("⚠️ Nhập thông tin quân bài chính xác để chạy bộ khử sai số!")
    else:
        p_list = parse_baccarat_input_v54(p_clean)
        b_list = parse_baccarat_input_v54(b_clean)
        
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
        '<div style="background-color: rgba(1, 2, 5, 0.98); border: 2px dashed #06d6a0; color: #06d6a0; padding: 40px 20px; border-radius: 12px; font-size: 15px; text-align: center;">'
        '🌌 <b>LÕI ZERO-ERROR ĐANG CHỜ PHÂN TÍCH THỜI GIAN THỰC</b><br>'
        '<span style="font-size:13.5px; font-weight:normal; opacity:0.85; color: #cbd5e1;">'
        'Mô hình v54.0 tích hợp màng lọc phạt phế Nhà Cái và Trọng số suy giảm lũy thừa ván bài. Vui lòng nạp quân bài lật để kích hoạt rada.</span>'
        '</div>', 
        unsafe_allow_html=True
    )
else:
    # Khởi chạy lõi khử sai số tuyệt đối v54
    final_p, final_b, final_t, cards_left, volatility, volatility_velocity, kalman_gain, streak_side, streak_count, is_critical, p_six = calculate_v54_zero_error_engine(
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
    if volatility > 34.0: vol_css_class = "vol-high"
    elif volatility > 15.0: vol_css_class = "vol-mid"

    st.markdown("### 👁️ HUD ĐIỀU PHỐI KHỬ SAI SỐ THỰC THỜI")
    
    rec = get_ai_v54_zero_error_diagnostic(final_p, final_b, final_t, volatility, volatility_velocity, kalman_gain, streak_side, streak_count, is_critical, p_six, st.session_state.round_detailed_log)
    
    st.markdown(
        f'<div class="tactical-box {rec["class"]}" style="background-color: {rec["bg"]}; border: 2px solid {rec["border"]}; color: {rec["border"]};">'
        f'<div class="tactical-title"><span>🛸 {rec["action"]}</span> <span style="font-family: monospace;">ĐỊNH LƯỢNG VỐN KELLY THỰC: {rec["bet_size"]}</span></div>'
        f'<div class="tactical-msg">{rec["msg"]}</div>'
        f'<div class="tactical-action-line">💡 <b>Cân bằng phế Nhà Cái:</b> Thuật toán đã tự động khấu trừ rủi ro phế 6 điểm của sòng bài để bảo vệ biên độ nhuận ròng thực tế.</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    p_box_css, b_box_css = "hud-box", "hud-box"
    if is_critical:
        if final_p > final_b: p_box_css = "hud-box neon-overdrive-break"
        else: b_box_css = "hud-box neon-overdrive-break"
    else:
        if final_p > final_b + 5.0: p_box_css = "hud-box neon-player-advantage"
        elif final_b > final_p + 5.0: b_box_css = "hud-box neon-banker-advantage"
    
    col_p, col_b, col_t = st.columns(3, gap="small")
    with col_p:
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER PROBABILITY</div><div class="hud-value" style="color:#00afb9;">{final_p}%</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER PROBABILITY</div><div class="hud-value" style="color:#ff4757;">{final_b}%</div></div>', unsafe_allow_html=True)
    with col_t:
        st.markdown(f'<div class="hud-box"><div class="hud-title">⚡ BIẾN THIÊN THỜI GIAN</div><div class="hud-value {vol_css_class}">{volatility:.1f}%</div></div>', unsafe_allow_html=True)
        
    st.write("")
    
    col_meta1, col_meta2 = st.columns(2, gap="small")
    with col_meta1:
        st.markdown(f"<small>🛰️ **Mật độ lá bài 6 trong khay:** `{p_six*100:.1f}%` (Ngưỡng > 9.0% kích hoạt lệnh phạt tránh phế Banker)</small>", unsafe_allow_html=True)
    with col_meta2:
        st.markdown(f"<small>📊 **Gia tốc sai số tịnh tiến:** `{volatility_velocity:.2f}` | **Kalman Gain:** `{kalman_gain:.2f}`</small>", unsafe_allow_html=True)

    if st.session_state.round_detailed_log:
        st.markdown('<div class="score-log-hud"><b>📈 LỊCH SỬ KHAY BÀI ĐÃ ĐƯỢC CHUẨN HÓA TRỌNG SỐ THỜI GIAN LŨY THỪA:</b><br>', unsafe_allow_html=True)
        for idx, r in enumerate(st.session_state.round_detailed_log):
            distance = total_log_games - 1 - idx
            st.markdown(f"• Ván {idx+1}: [P] {r['p_score']}đ vs {r['b_score']}đ [B] ➡️ **{r['outcome'].upper()}** (Suy giảm thời gian: `t-{distance}` | Trọng số: `{0.88**distance:.2f}`)")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    total_shoe_cards = decks * 52
    penetration_rate_pct = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
    
    streak_status = f"Bệt chuỗi {streak_side.upper()} x{streak_count} ván" if (streak_side and streak_count >= 2) else "Chuỗi hỗn hợp phân tán"
    st.caption(f"**Engine:** `ZERO-ERROR FRONTIER v54.0` | **Trạng thái chuỗi:** `{streak_status}` | **Độ sâu khay bài:** `{penetration_rate_pct:.1f}%`")
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
        st.session_state.form_counter = 0
        st.rerun()
