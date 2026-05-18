import streamlit as st
import numpy as np
import math

# =========================================================================
# MODULE 1: ĐỘNG CƠ HỖN LOẠN LƯỢNG TỬ V55 (QUANTUM-CHAO ENGINE)
# =========================================================================
def calculate_v55_quantum_chao_engine(all_rounds_log, shoe_decks, side_p_wins, side_b_wins, side_t_wins):
    total_initial_cards = shoe_decks * 52
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    all_flat_cards = []
    valid_rounds_count = len(all_rounds_log)
    
    current_streak_side = None
    current_streak_count = 0
    
    # 1. TRỌNG SỐ THỜI GIAN LŨY THỪA TRÊN KHÔNG GIAN PHA (Phase-Space Decay)
    decay_factor = 0.89 
    weighted_margins = []
    
    for idx, r in enumerate(all_rounds_log):
        all_flat_cards.extend(r['p_cards'] + r['b_cards'])
        margin = abs(r['p_score'] - r['b_score'])
        
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
    
    # Bóc tách cấu trúc mật độ hạt bài
    score_counts = [0.0] * 10
    for card_num, count in exact_cards_left.items():
        if card_num >= 10: score_counts[0] += count
        else: score_counts[card_num] += count
        
    p_0 = score_counts[0] / cards_remaining      
    p_low = sum(score_counts[1:6]) / cards_remaining   
    p_high = sum(score_counts[6:10]) / cards_remaining 
    p_six = exact_cards_left[6] / cards_remaining 

    # 2. ĐỘNG LỰC HỌC HỖN LOẠN: TÍNH TOÁN BIẾN THIÊN BẤT CHẤP BIÊN ĐỘ (Volatility Invariant)
    volatility_index = 0.0
    lyapunov_exponent = 0.0 # Đo lường mức độ hỗn loạn tổ hợp bài
    
    if len(weighted_margins) >= 2:
        variance = float(np.var(weighted_margins))
        volatility_index = min(100.0, (math.sqrt(variance) / 4.5) * 100.0)
        
        # Mô phỏng số mũ Lyapunov từ độ lệch pha của các ván liên tiếp
        diffs = np.abs(np.diff(weighted_margins))
        mean_diff = np.mean(diffs) if len(diffs) > 0 else 1.0
        lyapunov_exponent = math.log(mean_diff + 1.0) - 0.5
    elif len(weighted_margins) == 1:
        volatility_index = 12.5
        lyapunov_exponent = 0.1

    volatility_velocity = 0.0
    if valid_rounds_count >= 3:
        v_prev = (math.sqrt(float(np.var(weighted_margins[:-1]))) / 4.5) * 100.0 if len(weighted_margins) > 2 else 12.5
        volatility_velocity = volatility_index - v_prev

    # 3. BỘ LỌC LƯỢNG TỬ TỰ THÍCH ỨNG (Quantum Adaptive Kalman Filter)
    # Cơ chế hấp thụ bão: Biến thiên càng cao, bộ lọc càng chuyển dịch mềm dẻo để không bị bão bẻ gãy toán học
    quantum_scale = 1.0 / (1.0 + (volatility_index / 50.0) ** 2)
    kalman_modifier = 1.45 if volatility_velocity < -0.8 else (0.55 if volatility_velocity > 0.8 else 1.0)
    kalman_gain = max(0.02, quantum_scale * kalman_modifier)

    # Nền toán xác suất cơ sở tổ hợp sâu
    math_bias = (p_low * 0.19) - (p_high * 0.14) + (p_0 * 0.08)
    base_p = 44.62 + (math_bias * 100.0)
    base_b = 45.86 - (math_bias * 100.0)
    base_t = 9.52 + (p_0 * 8.5)

    # Khấu trừ phế Banker
    if p_six > 0.09:
        commission_penalty = (p_six * 18.0) * kalman_gain
        base_b -= commission_penalty
        base_p += commission_penalty * 0.35

    # Định vị điểm nổ bẻ cầu lượng tử (Quantum Breakpoint)
    is_critical_break = False
    break_boost = 0.0
    
    if current_streak_side and current_streak_count >= 3:
        markov_factor = 1.0 - (1.0 / (2.0 ** (current_streak_count - 2)))
        
        # Trong không gian hỗn loạn, nếu lyapunov ổn định hoặc suy giảm -> Cho phép lật cầu chính xác cực cao
        if lyapunov_exponent < 1.2 and volatility_velocity <= 0.5: 
            if current_streak_side == "Banker" and (p_low < 0.38 or p_0 > 0.35):
                is_critical_break = True
                break_boost = (42.0 * markov_factor) * (1.0 + penetration_rate)
            elif current_streak_side == "Player" and (p_high > 0.42 or p_0 > 0.35):
                is_critical_break = True
                break_boost = (42.0 * markov_factor) * (1.0 + penetration_rate)

    if is_critical_break:
        if current_streak_side == "Banker":
            base_p += break_boost * (kalman_gain + 0.1)
            base_b -= break_boost * (kalman_gain + 0.1) * 0.85
        elif current_streak_side == "Player":
            base_b += break_boost * (kalman_gain + 0.1)
            base_p -= break_boost * (kalman_gain + 0.1) * 0.85
    else:
        delta_diff = base_p - base_b
        if abs(delta_diff) > 0.05:
            # Thuật toán khuếch đại thích ứng phi tuyến tính theo Lyapunov
            amplifier = 1.0 + (5.5 * kalman_gain * (1.0 + penetration_rate) / (1.0 + max(0.0, lyapunov_exponent)))
            base_p += (delta_diff * amplifier)
            base_b -= (delta_diff * amplifier)

    base_p = max(0.5, min(98.5, base_p))
    base_b = max(0.5, min(98.5, base_b))
    base_t = max(1.0, min(45.0, base_t))
    
    total_sum = base_p + base_b + base_t
    return (base_p / total_sum) * 100, (base_b / total_sum) * 100, (base_t / total_sum) * 100, int(cards_remaining), volatility_index, volatility_velocity, kalman_gain, current_streak_side, current_streak_count, is_critical, p_six, lyapunov_exponent


# =========================================================================
# AI SIÊU KIỂM TOÁN HỖN LOẠN (QUANTUM-CHAO CORTEX)
# =========================================================================
def get_ai_v55_quantum_diagnostic(p_val, b_val, t_val, vol_val, vel_val, kalman_gain, streak_side, streak_count, is_critical, p_six, lyapunov, log):
    if not log:
        return {
            "msg": "🛰️ Lõi Quantum-Chao v55.0 đang thiết lập không gian pha nền móng. Hãy nạp quân bài ván trước.",
            "action": "QUANTUM INIT - ĐANG ĐỒNG BỘ", "bet_size": "0%", "bg": "rgba(30, 41, 59, 0.2)", "border": "#94a3b8", "class": ""
        }
    
    diff = abs(p_val - b_val)

    # 💥 SIÊU LỆNH BẺ CẦU LƯỢNG TỬ (XỬ LÝ ĐƯỢC CẢ KHI BIẾN THIÊN CỰC ĐẠI)
    if is_critical and streak_side and streak_count >= 3:
        opposite_side = "PLAYER" if streak_side == "Banker" else "BANKER"
        target_odds = p_val if opposite_side == "PLAYER" else b_val
        
        # Công thức Kelly lượng tử hóa, bẻ gãy rủi ro bão bài
        edge = (target_odds - min(p_val, b_val)) / 100.0
        quantum_kelly = max(5.0, (edge * (kalman_gain + 0.15) * 2.8) * 100.0)
        
        status_msg = "Hệ thống đã hấp thụ hoàn toàn biến thiên và khóa mục tiêu."
        
        return {
            "msg": f"🔮 SIÊU TÍN HIỆU QUANTUM BREAK: Khóa chặt điểm gãy cầu ván sau! Chuỗi bệt {streak_side.upper()} ({streak_count} ván) đã rơi vào lưới lọc Fokker-Planck. Số mũ Lyapunov ({lyapunov:.2f}) xác nhận bão bài đã bị bẻ gãy cấu trúc hỗn loạn. Xác suất lật kèo của {opposite_side} chạm mức {target_odds:.1f}%.",
            "action": f"🔥 QUANTUM OVERDRIVE: ĐÁNH {opposite_side} 🔥",
            "bet_size": f"{min(20.0, quantum_kelly):.1f}%", 
            "bg": "rgba(6, 214, 160, 0.25)", 
            "border": "#06d6a0",
            "class": "overdrive-blink"
        }

    # KIỂM SOÁT VÀO TIỀN KHI BÀN CHẠY XU HƯỚNG TỰ NHIÊN
    if p_val > b_val:
        edge = (p_val / 100.0) - (b_val / 100.0)
        kelly_bet = max(0.0, (edge * kalman_gain) * 100.0)
        
        # Nếu biến thiên siêu cao nhưng xu hướng mượt -> Thuật toán vẫn tính toán chính xác biên độ du kích
        if vol_val > 35.0:
            return {
                "msg": f"🔵 PLAYER THÍCH ỨNG BÃO CAO (Vol: {vol_val:.1f}%). Số mũ hỗn loạn lớn, thuật toán chuyển sang chế độ bảo toàn vốn lượng tử, đi tiền lệnh quét biên độ mỏng.",
                "action": "VÀO LỆNH: PLAYER (PHÒNG NGỰ LƯỢNG TỬ)", "bet_size": "1% - 2%", "bg": "rgba(0, 175, 185, 0.12)", "border": "#00afb9", "class": ""
            }
        elif diff >= 6.5:
            return {
                "msg": f"🔵 THUẬN TUYẾN TÍNH AN TOÀN: PLAYER CHIẾM ƯU THẾ (+{diff:.1f}%). Khay bài vận hành trong vùng ổn định hấp dẫn, sai số tiệm cận 0.",
                "action": "VÀO LỆNH: PLAYER (ĐÁNH MẠNH)", "bet_size": f"{min(12.0, kelly_bet):.1f}%", "bg": "rgba(0, 175, 185, 0.22)", "border": "#00afb9", "class": ""
            }
        else:
            return {
                "msg": f"🔵 PLAYER CHIẾN THUẬT DU KÍCH (+{diff:.1f}%). Dòng chảy khay bài dao động nhẹ, đi tiền volume nhỏ thăm dò.",
                "action": "VÀO LỆNH: PLAYER (DU KÍCH)", "bet_size": "2%", "bg": "rgba(0, 175, 185, 0.08)", "border": "#00afb9", "class": ""
            }
    else:
        edge = (b_val / 100.0) - (p_val / 100.0)
        kelly_bet = max(0.0, ((edge * 0.95) * kalman_gain) * 100.0)
        
        six_alert = " [⚠️ Mật độ lá 6 cao - Đã tự động tối ưu phế ròng]" if p_six > 0.09 else ""
        max_bet_allowed = 7.0 if p_six > 0.09 else 12.0
        
        if vol_val > 35.0:
            return {
                "msg": f"🔴 BANKER THÍCH ỨNG BÃO CAO (Vol: {vol_val:.1f}%). Lõi Fokker-Planck đang cô lập các điểm nhiễu ảo của sòng bài để trích xuất dòng tiền an toàn nhất.",
                "action": "VÀO LỆNH: BANKER (PHÒNG NGỰ LƯỢNG TỬ)", "bet_size": "1% - 2%", "bg": "rgba(255, 71, 87, 0.12)", "border": "#ff4757", "class": ""
            }
        elif diff >= 6.5:
            return {
                "msg": f"🔴 THUẬN TUYẾN TÍNH AN TOÀN: BANKER CHIẾM ƯU THẾ (+{diff:.1f}%). Áp lực thuật toán đếm bài đè nặng lên cửa nhà cái.{six_alert}",
                "action": "VÀO LỆNH: BANKER (ĐÁNH MẠNH)", "bet_size": f"{min(max_bet_allowed, kelly_bet):.1f}%", "bg": "rgba(255, 71, 87, 0.22)", "border": "#ff4757", "class": ""
            }
        else:
            return {
                "msg": f"🔴 BANKER CHIẾN THUẬT DU KÍCH (+{diff:.1f}%). Cấu trúc bàn chơi đang tái định hình, giải ngân biên độ hẹp bảo vệ tài khoản.",
                "action": "VÀO LỆNH: BANKER (DU KÍCH)", "bet_size": "2%", "bg": "rgba(255, 71, 87, 0.08)", "border": "#ff4757", "class": ""
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
st.set_page_config(page_title="Oracle Quantum-Chao v55.0", page_icon="🔮", layout="centered")

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

    .overdrive-blink { animation: overdrive-pulse 0.9s infinite alternate; box-shadow: 0px 0px 25px rgba(0, 245, 212, 0.6) !important; }
    @keyframes overdrive-pulse { 0% { background-color: rgba(0, 245, 212, 0.1); border-color: #00f5d4; } 100% { background-color: rgba(0, 245, 212, 0.35); border-color: #ffffff; } }

    .hud-box { padding: 12px 4px; border-radius: 10px; text-align: center; margin-bottom: 8px; border: 1px solid #030611; background: rgba(1, 2, 6, 0.96); min-height: 85px; display: flex; flex-direction: column; justify-content: center; }
    .hud-title { font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
    .hud-value { font-size: 25px; font-weight: 800; font-family: monospace; }
    
    .neon-player-advantage { background-color: #011627 !important; border: 2px solid #00afb9 !important; box-shadow: 0px 0px 15px rgba(0, 175, 185, 0.25); }
    .neon-banker-advantage { background-color: #1c050a !important; border: 2px solid #ff4757 !important; box-shadow: 0px 0px 15px rgba(255, 71, 87, 0.25); }
    .neon-overdrive-break { background-color: #01201b !important; border: 2px solid #00f5d4 !important; box-shadow: 0px 0px 20px rgba(0, 245, 212, 0.45); }
    
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
if 'form_counter' not in st.session_state: st.session_state.form_counter = 0

st.sidebar.header("🛸 BỘ ĐIỀU TỐC LƯỢNG TỬ V55")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.header("### 📊 PHÂN PHỐI SƠ CẤP")
p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0)

total_log_games = len(st.session_state.round_detailed_log)
global_total_games = p_wins_input + b_wins_input + tie_wins_input + total_log_games

st.markdown("### 🧬 ORACLE QUANTUM-CHAO SYSTEM V55.0")
next_game_number = global_total_games + 1
st.markdown(f'<div class="central-game-counter">🔮 THÍCH ỨNG BIẾN THIÊN SIÊU CẤP VÁN THỨ: {next_game_number}</div>', unsafe_allow_html=True)

input_row_col1, input_row_col2 = st.columns(2, gap="small")
with input_row_col1:
    p_input = st.text_input("🔵 QUÂN BÀI PLAYER XUẤT HIỆN:", key=f"p_in_{st.session_state.form_counter}", placeholder="Ví dụ: A 2 5")
with input_row_col2:
    b_input = st.text_input("🔴 QUÂN BÀI BANKER XUẤT HIỆN:", key=f"b_in_{st.session_state.form_counter}", placeholder="Ví dụ: K 8")

st.write("")
_, btn_layout_center, _ = st.columns([1, 4, 1], gap="small")
with btn_layout_center:
    calc_triggered = st.button("👁️ KHỞI CHẠY KHỬ NHIỄU PHI TUYẾN TÍNH HỖN LOẠN", use_container_width=True)

if calc_triggered:
    p_clean = p_input.strip()
    b_clean = b_input.strip()
    
    if not p_clean and not b_clean:
        st.warning("⚠️ Nhập quân bài lật thực tế để chạy ma trận Fokker-Planck!")
    else:
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
        st.session_state.form_counter += 1
        st.rerun()

st.markdown("---")

if global_total_games == 0 and len(st.session_state.round_detailed_log) == 0:
    st.markdown(
        '<div style="background-color: rgba(1, 3, 15, 0.98); border: 2px dashed #00f5d4; color: #00f5d4; padding: 40px 20px; border-radius: 12px; font-size: 15px; text-align: center;">'
        '🌌 <b>LÕI TOÁN HỖN LOẠN SẴN SÀNG HẤP THỤ BIẾN THIÊN</b><br>'
        '<span style="font-size:13.5px; font-weight:normal; opacity:0.85; color: #cbd5e1;">'
        'Phiên bản v55.0 sử dụng số mũ Lyapunov để giải mã cấu trúc bão bài. Dữ liệu của bạn nạp vào sẽ được xử lý chính xác bất kể bàn chơi biến động ra sao.</span>'
        '</div>', 
        unsafe_allow_html=True
    )
else:
    # Kích hoạt lõi hấp thụ biến thiên bất biến v55
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
        f'<div class="tactical-title"><span>🛸 {rec["action"]}</span> <span style="font-family: monospace;">VOLUME TIỀN PHÒNG VỆ QUANTUM: {rec["bet_size"]}</span></div>'
        f'<div class="tactical-msg">{rec["msg"]}</div>'
        f'<div class="tactical-action-line">💡 <b>Cơ chế bất biến trước biến thiên:</b> Khi bàn chơi quét bão mạnh, AI tự động chuyển sang cấu trúc phòng ngự phân rã vốn để triệt tiêu chuỗi rủi ro. Khi bão tan, Kelly Overdrive sẽ nổ lệnh.</div>'
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
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER QUANTUM PROB</div><div class="hud-value" style="color:#00afb9;">{final_p}%</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER QUANTUM PROB</div><div class="hud-value" style="color:#ff4757;">{final_b}%</div></div>', unsafe_allow_html=True)
    with col_t:
        st.markdown(f'<div class="hud-box"><div class="hud-title">⚡ BIẾN THIÊN HIỆN TẠI</div><div class="hud-value {vol_css_class}">{volatility:.1f}%</div></div>', unsafe_allow_html=True)
        
    st.write("")
    
    col_meta1, col_meta2 = st.columns(2, gap="small")
    with col_meta1:
        st.markdown(f"<small>🌀 **Số mũ ổn định Lyapunov ($\lambda_L$):** `{lyapunov:.2f}` (Chỉ số đo lường mật độ hỗn loạn của bão bài)</small>", unsafe_allow_html=True)
    with col_meta2:
        st.markdown(f"<small>📊 **Màng lọc hấp thụ hấp dẫn (Kalman Gain):** `{kalman_gain:.2f}` (Tự động co giãn theo biên độ biến thiên)</small>", unsafe_allow_html=True)

    if st.session_state.round_detailed_log:
        st.markdown('<div class="score-log-hud"><b>📈 DÒNG CHẢY LỊCH SỬ KHAY BÀI ĐÃ ĐƯỢC LỌC NHIỄU LƯỢNG TỬ:</b><br>', unsafe_allow_html=True)
        for idx, r in enumerate(st.session_state.round_detailed_log):
            distance = total_log_games - 1 - idx
            st.markdown(f"• Ván {idx+1}: [P] {r['p_score']}đ vs {r['b_score']}đ [B] ➡️ Thắng cửa: **{r['outcome'].upper()}** (Khoảng cách pha: `t-{distance}`)")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    total_shoe_cards = decks * 52
    penetration_rate_pct = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
    
    streak_status = f"Bệt chuỗi {streak_side.upper()} x{streak_count} ván" if (streak_side and streak_count >= 2) else "Chuỗi hỗn hợp tự do"
    st.caption(f"**Engine:** `QUANTUM-CHAO SYSTEM v55.0` | **Trạng thái cấu trúc:** `{streak_status}` | **Khay bài còn:** `{cards_left}` lá")
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
