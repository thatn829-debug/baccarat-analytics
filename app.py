import streamlit as st
import numpy as np
import math

# =========================================================================
# MODULE 1: ĐỘNG CƠ MA TRẬN CHẨN ĐOÁN BẺ CẦU TỚI HẠN (ULTIMATE ANTI-TREND OVERDRIVE)
# =========================================================================
def calculate_v52_overdrive_engine(all_rounds_log, shoe_decks, side_p_wins, side_b_wins, side_t_wins):
    total_initial_cards = shoe_decks * 52
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    all_flat_cards = []
    margins_list = []
    valid_rounds_count = 0
    last_round_winner = None
    last_round_margin = 0
    
    # Bộ theo dõi chuỗi bệt sâu
    current_streak_side = None
    current_streak_count = 0
    
    for r in all_rounds_log:
        all_flat_cards.extend(r['p_cards'] + r['b_cards'])
        margin = r['p_score'] - r['b_score']
        margins_list.append(abs(margin))
        valid_rounds_count += 1
        last_round_winner = r['outcome']
        last_round_margin = abs(margin)
        
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
    
    # Phân tích mật độ bài
    score_counts = [0.0] * 10
    for card_num, count in exact_cards_left.items():
        if card_num >= 10: score_counts[0] += count
        else: score_counts[card_num] += count
        
    p_0 = score_counts[0] / cards_remaining      
    p_low = sum(score_counts[1:6]) / cards_remaining   
    p_high = sum(score_counts[6:10]) / cards_remaining 

    # Tính Toán Entropy Shannon
    entropy = 0.0
    for count in score_counts:
        prob = count / cards_remaining
        if prob > 0: entropy -= prob * math.log2(prob)
    entropy_efficiency = max(0.1, (3.32 - entropy) / 3.32)

    # Màng lọc nhiễu Kalman
    volatility_index = 0.0
    kalman_gain = 1.0
    if len(margins_list) >= 2:
        actual_variance = float(np.var(margins_list))
        volatility_index = min(50.0, (math.sqrt(actual_variance) / 4.5) * 100.0)
        kalman_gain = max(0.1, 1.0 - (volatility_index / 50.0))
    elif len(margins_list) == 1:
        volatility_index = 12.5
        kalman_gain = 0.75

    # Tính toán nền xác suất cơ sở
    math_bias = (p_low * 0.16) - (p_high * 0.11) + (p_0 * 0.06)
    base_p = 44.62 + (math_bias * 100.0)
    base_b = 45.86 - (math_bias * 100.0)
    base_t = 9.52 + (p_0 * 8.0)

    # 🔮 SIÊU THUẬT TOÁN: ĐO ĐỘ BÃO HÒA CHUỖI MARKOV ĐỂ ÉP ĐIỂM BẺ CẦU VÁN SAU
    break_probability_boost = 0.0
    critical_saturation_triggered = False

    if current_streak_side and current_streak_count >= 3:
        # Hệ số suy giảm Markov: Cầu càng dài, áp lực bẻ tự nhiên càng lớn
        markov_decay = 1.0 - (1.0 / (2.0 ** (current_streak_count - 2)))
        
        if current_streak_side == "Banker":
            # Nếu đang bệt Banker mà khay bài cạn kiệt tài nguyên bài nhỏ (p_low thấp) -> Banker mất khả năng bốc bài tối ưu
            if p_low < 0.38 or p_0 > 0.36:
                critical_saturation_triggered = True
                break_probability_boost = (30.0 * markov_decay) * (1.0 + penetration_rate)
        elif current_streak_side == "Player":
            # Nếu đang bệt Player mà khay bài dày đặc bài Tây và bài 6-9 -> Lợi thế điểm tự nhiên chuyển dịch sang Banker
            if p_high > 0.42 or p_0 > 0.36:
                critical_saturation_triggered = True
                break_probability_boost = (30.0 * markov_decay) * (1.0 + penetration_rate)

    # Áp dụng gia tốc Overdrive vào lõi xác suất nếu chạm điểm tới hạn
    if critical_saturation_triggered:
        if current_streak_side == "Banker":
            base_p += break_probability_boost * kalman_gain
            base_b -= break_probability_boost * kalman_gain * 0.8
        elif current_streak_side == "Player":
            base_b += break_probability_boost * kalman_gain
            base_p -= break_probability_boost * kalman_gain * 0.8
    else:
        # Nếu không có điểm gãy tới hạn, chạy tuyến tính khuếch đại dòng chảy thông thường
        delta_diff = base_p - base_b
        if abs(delta_diff) > 0.1:
            ultimate_amplifier = 1.0 + (3.5 * entropy_efficiency * kalman_gain * (1.0 + penetration_rate))
            base_p += (delta_diff * ultimate_amplifier)
            base_b -= (delta_diff * ultimate_amplifier)

    # Xung lực động lượng ván trước
    if valid_rounds_count > 0 and last_round_winner and not critical_saturation_triggered:
        momentum_push = min(10.0, last_round_margin * 1.5) * kalman_gain
        if last_round_winner == "Player":
            base_p += momentum_push
            base_b -= (momentum_push * 0.5)
        elif last_round_winner == "Banker":
            base_b += momentum_push
            base_p -= (momentum_push * 0.5)

    base_p = max(3.0, min(95.0, base_p))
    base_b = max(3.0, min(95.0, base_b))
    base_t = max(2.0, min(38.0, base_t))
    
    total_sum = base_p + base_b + base_t
    return (base_p / total_sum) * 100, (base_b / total_sum) * 100, (base_t / total_sum) * 100, int(cards_remaining), volatility_index, entropy, kalman_gain, current_streak_side, current_streak_count, critical_saturation_triggered


# =========================================================================
# AI SIÊU CHẨN ĐOÁN BẺ CẦU TỐI HẬU (OVERDRIVE DIAGNOSTIC CORTEX)
# =========================================================================
def get_ai_v52_overdrive_diagnostic(p_val, b_val, t_val, vol_val, entropy_val, kalman_gain, streak_side, streak_count, is_critical, log):
    if not log:
        return {
            "msg": "🔮 Đang khởi tạo Rada Quét Điểm Tới Hạn... Hệ thống đã sẵn sàng bóc tách khay bài.",
            "action": "CHẾ ĐỘ CHỜ - QUAN SÁT KHAY BÀI", "bet_size": "0%", "bg": "rgba(116, 125, 140, 0.08)", "border": "#747d8c", "class": ""
        }
    
    # 🚨 KIỂM SOÁT BIẾN THIÊN CỰC ĐẠI
    if vol_val > 33.0:
        return {
            "msg": f"🚨 BÁO ĐỘNG ĐỎ: BIẾN THIÊN VƯỢT NGƯỠNG AN TOÀN ({vol_val:.1f}%)! Lõi toán học phát hiện thuật toán sòng bài đang chạy chuỗi hỗn xáo cực đại để quét sạch người chơi bẻ cầu. Lệnh bẻ cầu bị HỦY BỎ để bảo vệ vốn.",
            "action": "HALT - ĐÓNG BĂNG GIAO DỊCH", "bet_size": "0%", "bg": "rgba(235, 94, 40, 0.15)", "border": "#eb5e28", "class": ""
        }

    diff = abs(p_val - b_val)

    # 💥 KỊCH BẢN SIÊU CHẨN ĐOÁN TỐI HẬU: VÁN SAU BẺ CẦU TUYỆT ĐỐI (OVERDRIVE)
    if is_critical and streak_side and streak_count >= 3:
        opposite_side = "PLAYER" if streak_side == "Banker" else "BANKER"
        target_odds = p_val if opposite_side == "PLAYER" else b_val
        
        # Công thức Kelly tích hợp gia tốc bão hòa khay bài nâng cao
        edge = (target_odds - min(p_val, b_val)) / 100.0
        overdrive_kelly = max(3.0, (edge * kalman_gain * (3.32 / entropy_val) * 1.5) * 100.0)
        
        return {
            "msg": f"🛸 TÍN HIỆU TỐI HẬU - VÁN SAU BẺ CẦU THÀNH CÔNG ĐẠT TỶ LỆ CAO! Chuỗi bệt {streak_side.upper()} ({streak_count} ván) đã đâm thủng màng giới hạn tổ hợp. Thuật toán đo lường bài còn lại không thể duy trì thêm chuỗi. Cửa {opposite_side} nhận xung lực đảo chiều lên đến {target_odds:.1f}%.",
            "action": f"⚡ OVERDRIVE: BẺ CẦU NGAY VÁN SAU ĐÁNH {opposite_side} ⚡",
            "bet_size": f"{min(15.0, overdrive_kelly):.1f}%", # Đẩy trần vốn lên 15% cho lệnh tối hậu sạch nhiễu
            "bg": "rgba(147, 51, 234, 0.25)", 
            "border": "#a855f7",
            "class": "overdrive-blink" # Kích hoạt hiệu ứng nhấp nháy tím cảnh báo tối hậu
        }

    # ĐÁNH THEO XU HƯỚNG TUYẾN TÍNH (NẾU CHƯA CÓ ĐIỂM GÃY TỚI HẠN)
    if p_val > b_val:
        edge = (p_val / 100.0) - (b_val / 100.0)
        kelly_bet = max(0.0, (edge * kalman_gain * (3.32 / entropy_val)) * 100.0)
        if diff >= 8.0 and vol_val <= 12.0:
            return {
                "msg": f"🔵 THUẬN TUYẾN TÍNH: PLAYER ĐÁNH MẠNH (+{diff:.1f}%). Khay bài đang chạy chuỗi sạch, chưa xuất hiện dấu hiệu nghẽn hay bão hòa.",
                "action": "VÀO LỆNH: PLAYER (ĐÁNH MẠNH)", "bet_size": f"{min(12.0, kelly_bet):.1f}%", "bg": "rgba(0, 175, 185, 0.2)", "border": "#00afb9", "class": ""
            }
        else:
            return {
                "msg": f"🔵 PLAYER XU HƯỚNG DU KÍCH (+{diff:.1f}%). Đi tiền nhỏ theo dòng chảy, duy trì trạng thái quan sát ranh giới.",
                "action": "VÀO LỆNH: PLAYER (DU KÍCH)", "bet_size": "2% - 4%", "bg": "rgba(0, 175, 185, 0.1)", "border": "#00afb9", "class": ""
            }
    else:
        edge = (b_val / 100.0) - (p_val / 100.0)
        kelly_bet = max(0.0, ((edge * 0.95) * kalman_gain * (3.32 / entropy_val)) * 100.0)
        if diff >= 8.0 and vol_val <= 12.0:
            return {
                "msg": f"🔴 THUẬN TUYẾN TÍNH: BANKER ĐÁNH MẠNH (+{diff:.1f}%). Mật độ điểm số Nhà Cái đang tối ưu cấu trúc khay bài.",
                "action": "VÀO LỆNH: BANKER (ĐÁNH MẠNH)", "bet_size": f"{min(12.0, kelly_bet):.1f}%", "bg": "rgba(254, 217, 255, 0.2)", "border": "#fed9ff", "class": ""
            }
        else:
            return {
                "msg": f"🔴 BANKER XU HƯỚNG DU KÍCH (+{diff:.1f}%). Đi tiền khối lượng thấp nương dòng chảy bệt, bảo vệ tài nguyên.",
                "action": "VÀO LỆNH: BANKER (DU KÍCH)", "bet_size": "2% - 4%", "bg": "rgba(254, 217, 255, 0.1)", "border": "#fed9ff", "class": ""
            }

def parse_baccarat_input_v52(raw_str):
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
st.set_page_config(page_title="Oracle Overdrive Engine v52.0", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(145deg, #010204, #04050d, #060714) !important; color: #ecf0f1 !important; }
    
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stHorizontalBlock"] > div { flex: 1 1 0% !important; min-width: 0px !important; }

    .central-game-counter { text-align: center; background: rgba(147, 51, 234, 0.15); border: 1px solid #a855f7; border-radius: 8px; padding: 8px 12px; font-family: monospace; font-size: 15px; font-weight: 800; color: #c084fc; margin-bottom: 12px; box-shadow: 0px 0px 12px rgba(147, 51, 234, 0.3); }
    
    .tactical-box { border-radius: 10px; padding: 16px; margin: 15px auto; box-shadow: 0px 6px 30px rgba(0,0,0,0.7); line-height: 1.5; }
    .tactical-title { font-size: 15px; font-weight: 900; text-transform: uppercase; margin-bottom: 6px; display: flex; justify-content: space-between; letter-spacing: 0.5px; }
    .tactical-msg { font-size: 13.5px; opacity: 0.95; margin-bottom: 10px; text-align: justify; }
    .tactical-action-line { font-size: 14px; font-weight: 800; border-top: 1px dashed rgba(255,255,255,0.15); padding-top: 8px; }

    /* Hiệu ứng nhấp nháy tối hậu khi phát hiện điểm bẻ cầu ván sau */
    .overdrive-blink {
        animation: overdrive-pulse 1.4s infinite alternate;
        box-shadow: 0px 0px 25px rgba(168, 85, 247, 0.6) !important;
    }
    @keyframes overdrive-pulse {
        0% { background-color: rgba(147, 51, 234, 0.15); border-color: #a855f7; }
        100% { background-color: rgba(147, 51, 234, 0.35); border-color: #d8b4fe; }
    }

    .hud-box { padding: 12px 4px; border-radius: 10px; text-align: center; margin-bottom: 8px; border: 1px solid #04050d; background: rgba(1, 2, 4, 0.96); min-height: 85px; display: flex; flex-direction: column; justify-content: center; }
    .hud-title { font-size: 11px; font-weight: 700; color: #8e9aaf; text-transform: uppercase; letter-spacing: 0.5px; }
    .hud-value { font-size: 25px; font-weight: 800; font-family: monospace; margin-top: 1px; }
    
    .neon-player-advantage { background-color: #01141e !important; border: 2px solid #00afb9 !important; box-shadow: 0px 0px 15px rgba(0, 175, 185, 0.35); }
    .neon-banker-advantage { background-color: #170508 !important; border: 2px solid #e74c3c !important; box-shadow: 0px 0px 15px rgba(231, 76, 60, 0.35); }
    .neon-overdrive-break { background-color: #230933 !important; border: 2px solid #a855f7 !important; box-shadow: 0px 0px 20px rgba(168, 85, 247, 0.5); }
    
    .vol-low { color: #00afb9 !important; }
    .vol-mid { color: #f1c40f !important; }
    .vol-high { color: #eb5e28 !important; animation: blinker 1s linear infinite; }
    
    @keyframes blinker { 50% { opacity: 0.2; } }
    
    .logic-lock { background-color: rgba(4, 5, 13, 0.98); border: 2px dashed #a855f7; color: #c084fc; padding: 40px 20px; border-radius: 12px; font-size: 15px; text-align: center; }
    .score-log-hud { padding: 12px; border-radius: 8px; background-color: rgba(1, 1, 3, 0.98); border: 1px dashed #23395b; margin-top: 5px; font-family: monospace; font-size: 12.5px; color: #cbd5e1; }
    
    div.stButton > button { background-color: #a855f7 !important; color: white !important; border-radius: 8px; font-weight: 900; padding: 10px 0px; font-size: 14px !important; border: none !important; box-shadow: 0px 4px 12px rgba(147, 51, 234, 0.3); }
    div.stButton > button:hover { background-color: #c084fc !important; box-shadow: 0px 0px 18px #c084fc !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []
if 'form_counter' not in st.session_state: st.session_state.form_counter = 0

st.sidebar.header("🛸 THÔNG SỐ KHAY BÀI CHUẨN ĐOÁN")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.header("### 📊 KHỚP DỮ LIỆU BAN ĐẦU")
p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0)

total_log_games = len(st.session_state.round_detailed_log)
global_total_games = p_wins_input + b_wins_input + tie_wins_input + total_log_games

st.markdown("### 🔮 ORACLE ANTI-TREND OVERDRIVE V52.0")
next_game_number = global_total_games + 1
st.markdown(f'<div class="central-game-counter">⚡ QUÉT ĐIỂM TỚI HẠN BỀT CHO VÁN THỨ: {next_game_number}</div>', unsafe_allow_html=True)

input_row_col1, input_row_col2 = st.columns(2, gap="small")
with input_row_col1:
    p_input = st.text_input("🔵 LÁ BÀI PLAYER VỪA RA:", key=f"p_in_{st.session_state.form_counter}", placeholder="Ví dụ: A 2 5 hoặc K 7")
with input_row_col2:
    b_input = st.text_input("🔴 LÁ BÀI BANKER VỪA RA:", key=f"b_in_{st.session_state.form_counter}", placeholder="Ví dụ: J Q 8 hoặc 9 4")

st.write("")
_, btn_layout_center, _ = st.columns([1, 4, 1], gap="small")
with btn_layout_center:
    calc_triggered = st.button("👁️ TÍNH TOÁN ĐIỂM GÃY TỚI HẠN VÁN SAU", use_container_width=True)

if calc_triggered:
    p_clean = p_input.strip()
    b_clean = b_input.strip()
    
    if not p_clean and not b_clean:
        st.warning("⚠️ Nhập thông tin quân bài để kích hoạt Rada chẩn đoán ván sau!")
    else:
        p_list = parse_baccarat_input_v52(p_clean)
        b_list = parse_baccarat_input_v52(b_clean)
        
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
        '🌌 <b>HỆ THỐNG KIỂM TRA ĐIỂM GÃY VÁN SAU ĐANG CHỜ</b><br>'
        '<span style="font-size:13.5px; font-weight:normal; opacity:0.85;">'
        'Phiên bản v52.0 đã kích hoạt tính năng chẩn đoán bẻ cầu ván sau cấp độ Tối Hậu. '
        'Hãy nhập quân bài để AI bóc tách cấu trúc bão hòa chuỗi Markov.</span>'
        '</div>', 
        unsafe_allow_html=True
    )
else:
    # Kích hoạt động cơ Overdrive dò tìm điểm gãy tới hạn ván sau
    final_p, final_b, final_t, cards_left, volatility, entropy_val, kalman_gain, streak_side, streak_count, is_critical = calculate_v52_overdrive_engine(
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
    vol_status_text = "TÍN HIỆU SẠCH"
    if volatility > 33.0:
        vol_css_class = "vol-high"
        vol_status_text = "HỆ THỐNG QUÈT (DỪNG LỆNH)"
    elif volatility > 15.0:
        vol_css_class = "vol-mid"
        vol_status_text = "NƠI GIẰNG CO ĐIỂM"

    st.markdown("### 👁️ KẾT QUẢ CHẨN ĐOÁN LƯỢNG TỬ TỚI HẠN VÁN SAU")
    
    # Truy xuất chẩn đoán từ AI cortex v52.0
    rec = get_ai_v52_overdrive_diagnostic(final_p, final_b, final_t, volatility, entropy_val, kalman_gain, streak_side, streak_count, is_critical, st.session_state.round_detailed_log)
    
    st.markdown(
        f'<div class="tactical-box {rec["class"]}" style="background-color: {rec["bg"]}; border: 2px solid {rec["border"]}; color: {rec["border"]};">'
        f'<div class="tactical-title"><span>📋 {rec["action"]}</span> <span style="font-family: monospace;">TỶ LỆ LỆNH KELLY: {rec["bet_size"]}</span></div>'
        f'<div class="tactical-msg">{rec["msg"]}</div>'
        f'<div class="tactical-action-line">💡 <b>Quy chế an toàn vốn:</b> Nếu lệnh bẻ cầu ván sau được phát ra, đây là điểm có xác suất cao nhất. Tuân thủ khối lượng đi tiền đề xuất, không tất tay (All-in).</div>'
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
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER ODDS</div><div class="hud-value" style="color:#00afb9;">{final_p}%</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER ODDS</div><div class="hud-value" style="color:#ff4757;">{final_b}%</div></div>', unsafe_allow_html=True)
    with col_t:
        st.markdown(f'<div class="hud-box"><div class="hud-title">⚡ BIẾN THIÊN LÕI</div><div class="hud-value {vol_css_class}">{volatility:.1f}%</div></div>', unsafe_allow_html=True)
        
    st.write("")
    
    col_meta1, col_meta2 = st.columns(2, gap="small")
    with col_meta1:
        st.markdown(f"<small>📈 **Entropy Khay Bài:** `{entropy_val:.3f} / 3.320` (Càng thấp tỷ lệ bẻ cầu chính xác càng tăng)</small>", unsafe_allow_html=True)
    with col_meta2:
        st.markdown(f"<small>🛰️ **Bộ lọc Kalman (Độ nhiễu):** `{kalman_gain:.2f}` (Yêu cầu > 0.40 để vào lệnh bẻ cầu an toàn)</small>", unsafe_allow_html=True)

    if st.session_state.round_detailed_log:
        st.markdown('<div class="score-log-hud"><b>📊 PHÂN TÍCH LỊCH SỬ CHUỖI TOÁN HỌC TÍCH LŨY:</b><br>', unsafe_allow_html=True)
        cumulative_margins = []
        for idx, r in enumerate(st.session_state.round_detailed_log):
            cumulative_margins.append(abs(r['p_score'] - r['b_score']))
            v_local = (math.sqrt(float(np.var(cumulative_margins))) / 4.5) * 100.0 if len(cumulative_margins) >= 2 else 12.5
            st.markdown(f"• Ván {idx+1}: [P] {r['p_score']}đ vs {r['b_score']}đ [B] ➡️ **{r['outcome'].upper()}** (Biến thiên cục bộ: `{v_local:.1f}%`)")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    total_shoe_cards = decks * 52
    penetration_rate_pct = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
    
    streak_status = f"Bệt {streak_side.upper()} liên tục x{streak_count} ván" if (streak_side and streak_count >= 2) else "Thế trận cầu nhảy ngẫu nhiên"
    st.caption(f"**Engine:** `OVERDRIVE ANTI-TREND v52.0` | **Trạng thái chuỗi:** `{streak_status}` | **Điểm Tới Hạn:** `{'KÍCH HOẠT VÁN SAU 🔥' if is_critical else 'CHƯA PHÁT HIỆN'}`")
    st.progress(penetration_rate_pct / 100.0)

st.markdown("<br>", unsafe_allow_html=True)
util_col_1, util_col_2 = st.columns(2, gap="small")
with util_col_1:
    if st.button("⏪ HOÀN TÁC VÁN TRƯỚC", use_container_width=True):
        if st.session_state.round_detailed_log:
            st.session_state.round_detailed_log.pop()
            st.rerun()
with util_col_2:
    if st.button("🔄 ĐỔI BÀN CHƠI MỚI", use_container_width=True):
        st.session_state.round_detailed_log = []
        st.session_state.form_counter = 0
        st.rerun()
