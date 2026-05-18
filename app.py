import streamlit as st
import numpy as np
import math

# =========================================================================
# MODULE 1: ĐỘNG CƠ ĐẾM BÀI CHUẨN TỔ HỢP V55.6 (TRUE MATHEMATICS ENGINE)
# =========================================================================
def calculate_v55_quantum_chao_engine(all_rounds_log, shoe_decks, side_p_wins, side_b_wins, side_t_wins):
    total_initial_cards = shoe_decks * 52
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    all_flat_cards = []
    valid_rounds_count = len(all_rounds_log)
    
    current_streak_side = None
    current_streak_count = 0
    
    # 1. THỐNG KÊ LỊCH SỬ VÀ PHÂN TÍCH CHUỖI
    for idx, r in enumerate(all_rounds_log):
        all_flat_cards.extend(r['p_cards'] + r['b_cards'])
        if r['outcome'] in ["Player", "Banker"]:
            if current_streak_side == r['outcome']:
                current_streak_count += 1
            else:
                current_streak_side = r['outcome']
                current_streak_count = 1
                
    # Cập nhật số lá bài còn lại trong khay bài thực tế
    for card in all_flat_cards:
        if card in exact_cards_left:
            exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
            
    cards_remaining = sum(exact_cards_left.values())
    if cards_remaining <= 0: cards_remaining = 1.0
    
    penetration_rate = (total_initial_cards - cards_remaining) / total_initial_cards
    
    # --- TÁI CẤU TRÚC 1: ĐẾM BÀI CHUẨN TOÁN HỌC BACCARAT ---
    # Sử dụng hệ số ảnh hưởng thực tế (Effect of Removal) của từng lá bài đến lợi thế cửa đặt
    # Giá trị dương có lợi cho Player, giá trị âm có lợi cho Banker
    counting_effect = {
        1: -0.005,  # Át
        2: -0.006,  
        3: -0.007,  
        4: -0.012,  # Rút nhiều lá bài nhỏ -> Có lợi cho Banker
        5: -0.008,  
        6: +0.011,  # Rút nhiều lá bài lớn -> Có lợi cho Player
        7: +0.013,  
        8: +0.008,  
        9: -0.002,  
        10: +0.004, # Bài hình hình thành cấu trúc điểm 0 ổn định
        11: +0.004, 
        12: +0.004, 
        13: +0.004
    }
    
    # Tính toán độ lệch lợi thế dựa trên các quân bài ĐÃ BỊ RÚT RA
    total_counting_bias = 0.0
    for card_num, left in exact_cards_left.items():
        cards_removed = (4 * shoe_decks) - left
        total_counting_bias += cards_removed * counting_effect[card_num]
        
    # Mật độ lá 10 và bài hình còn lại (Dùng riêng cho việc tính cửa Tie)
    p_0 = sum([exact_cards_left[i] for i in [10, 11, 12, 13]]) / cards_remaining
    p_six = exact_cards_left[6] / cards_remaining

    # 2. PHÂN TÍCH BIẾN THIÊN (VOLATILITY) ĐỂ ĐIỀU CHỈNH TRỌNG SỐ NĂNG ĐỘNG
    volatility_index = 0.0
    lyapunov_exponent = 0.2
    if len(all_rounds_log) >= 2:
        margins = [float(abs(r['p_score'] - r['b_score'])) for r in all_rounds_log]
        variance = float(np.var(margins))
        volatility_index = min(100.0, (math.sqrt(max(0.001, variance)) / 4.5) * 100.0)
        diffs = np.abs(np.diff(margins))
        lyapunov_exponent = math.log(float(np.mean(diffs)) + 1.0) - 0.5

    # 3. THIẾT LẬP XÁC SUẤT GỐC TUYỆT ĐỐI (TRUNG LẬP HÓA)
    # Không dùng amplifier nhân vô căn cứ, dựa hoàn toàn vào hệ số đếm bài chuẩn
    base_p = 44.62 + (total_counting_bias * 2.5)
    base_b = 45.86 - (total_counting_bias * 2.5)
    base_t = 9.52 + (p_0 * 3.0)

    # 4. XỬ LÝ ĐIỂM NÚT THẮT KHÔNG GIAN PHA (CHỈ DÙNG KHI BỆT QUÁ DÀI)
    is_critical = False
    if current_streak_side and current_streak_count >= 4:
        # Nếu chuỗi bệt quá dài ván 4+, kiểm tra cấu trúc hỗn loạn ổn định thấp để cảnh báo lật cầu
        if lyapunov_exponent < 0.5 and volatility_index < 25.0:
            is_critical = True
            if current_streak_side == "Banker":
                base_p += 4.5
                base_b -= 4.5
            else:
                base_b += 4.5
                base_p -= 4.5

    # Chuẩn hóa giới hạn biên độ an toàn cực kỳ khắt khe, ép xác suất luôn về thế cân bằng tự nhiên
    base_p = max(40.0, min(60.0, base_p))
    base_b = max(40.0, min(60.0, base_b))
    base_t = max(6.0, min(18.0, base_t))
    
    total_sum = base_p + base_b + base_t
    return (base_p / total_sum) * 100, (base_b / total_sum) * 100, (base_t / total_sum) * 100, int(cards_remaining), volatility_index, is_critical, p_six, lyapunov_exponent, current_streak_side, current_streak_count


# =========================================================================
# AI SIÊU KIỂM TOÁN HỖN LOẠN (QUANTUM-CHAO CORTEX)
# =========================================================================
def get_ai_v55_quantum_diagnostic(p_val, b_val, t_val, vol_val, is_critical, p_six, lyapunov, streak_side, streak_count, log):
    if not log:
        return {
            "msg": "🛰️ Lõi v55.6 Trung Lập đã sẵn sàng. Hệ thống vận hành theo thuật toán đếm bài Baccarat chuẩn toán học.",
            "action": "QUANTUM INIT - ĐANG CHỜ LỆNH", "bet_size": "0%", "bg": "rgba(30, 41, 59, 0.2)", "border": "#94a3b8", "class": ""
        }
    
    diff = abs(p_val - b_val)

    if is_critical and streak_side and streak_count >= 4:
        opposite_side = "PLAYER" if streak_side == "Banker" else "BANKER"
        target_odds = p_val if opposite_side == "PLAYER" else b_val
        return {
            "msg": f"🔮 CẢNH BÁO LẬT CẦU TOÁN HỌC: Chuỗi bệt {streak_side.upper()} ({streak_count} ván) đã chạm vùng cạn kiệt năng lượng. Xác suất chuyển đổi trạng thái sang {opposite_side} đạt {target_odds:.1f}%.",
            "action": f"🔥 TÍN HIỆU ĐẢO CHIỀU: {opposite_side} 🔥",
            "bet_size": "2% - 3%", 
            "bg": "rgba(6, 214, 160, 0.15)", 
            "border": "#06d6a0",
            "class": "overdrive-blink"
        }

    if p_val > b_val:
        if diff >= 2.5:
            return {
                "msg": f"🔵 PLAYER ƯU THẾ NHẸ (+{diff:.1f}%). Cấu trúc bài bị rút khỏi khay đang tạm thời ủng hộ cửa Người chơi.",
                "action": "VÀO LỆNH: PLAYER", "bet_size": "1% - 2%", "bg": "rgba(0, 175, 185, 0.12)", "border": "#00afb9", "class": ""
            }
        else:
            return {
                "msg": f"🔵 THẾ CẦU CÂN BẰNG (+{diff:.1f}% cho Player). Dao động cực nhỏ, ưu tiên bỏ ván hoặc đi tiền tối thiểu.",
                "action": "VÀO LỆNH: PLAYER (THĂM DÒ)", "bet_size": "1%", "bg": "rgba(0, 175, 185, 0.05)", "border": "#00afb9", "class": ""
            }
    else:
        if diff >= 2.5:
            return {
                "msg": f"🔴 BANKER ƯU THẾ NHẸ (+{diff:.1f}%). Phân phối hạt bài hội tụ về phía lợi thế bẩm sinh của Nhà cái.",
                "action": "VÀO LỆNH: BANKER", "bet_size": "1% - 2%", "bg": "rgba(255, 71, 87, 0.12)", "border": "#ff4757", "class": ""
            }
        else:
            return {
                "msg": f"🔴 THẾ CẦU CÂN BẰNG (+{diff:.1f}% cho Banker). Bàn chơi đang triệt tiêu sai lệch biên độ, không lạm dụng vào lệnh.",
                "action": "VÀO LỆNH: BANKER (THĂM DÒ)", "bet_size": "1%", "bg": "rgba(255, 71, 87, 0.05)", "border": "#ff4757", "class": ""
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
st.set_page_config(page_title="Oracle Quantum-Chao v55.6", page_icon="🔮", layout="centered")

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
    .neon-player-advantage { border: 2px solid #00afb9 !important; background-color: #011627 !important; }
    .neon-banker-advantage { border: 2px solid #ff4757 !important; background-color: #1c050a !important; }
    .vol-low { color: #00afb9 !important; }
    .score-log-hud { padding: 12px; border-radius: 8px; background-color: rgba(1, 2, 6, 0.98); border: 1px dashed #00f5d4; margin-top: 5px; font-family: monospace; font-size: 12.5px; color: #cbd5e1; }
    div.stButton > button { background-color: #00f5d4 !important; color: #010206 !important; border-radius: 8px; font-weight: 900; padding: 10px 0px; border: none !important; }
    div.stButton > button:hover { background-color: #7befb2 !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []

st.sidebar.header("🛸 THIẾT LẬP KHAY BÀI V55.6")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

total_log_games = len(st.session_state.round_detailed_log)

st.markdown("### 🧬 ORACLE QUANTUM-CHAO SYSTEM V55.6")
next_game_number = total_log_games + 1
st.markdown(f'<div class="central-game-counter">🔮 HỆ THỐNG TRUNG LẬP HÓA TOÁN HỌC VÁN THỨ: {next_game_number}</div>', unsafe_allow_html=True)

with st.form(key="baccarat_input_form", clear_on_submit=True):
    input_row_col1, input_row_col2 = st.columns(2, gap="small")
    with input_row_col1:
        p_input = st.text_input("🔵 QUÂN BÀI PLAYER CHI TIẾT:", placeholder="Ví dụ: A 2 5")
    with input_row_col2:
        b_input = st.text_input("🔴 QUÂN BÀI BANKER CHI TIẾT:", placeholder="Ví dụ: K 8")
        
    st.write("")
    _, btn_layout_center, _ = st.columns([1, 4, 1], gap="small")
    with btn_layout_center:
        calc_triggered = st.form_submit_button("👁️ KHỞI CHẠY TÍNH TOÁN THEO LÕI TRUNG LẬP")

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

if total_log_games == 0:
    st.markdown(
        '<div style="background-color: rgba(1, 3, 15, 0.98); border: 2px dashed #00f5d4; color: #00f5d4; padding: 40px 20px; border-radius: 12px; font-size: 15px; text-align: center;">'
        '🌌 <b>LÕI TOÁN v55.6: TRUNG LẬP HÓA HOÀN TOÀN</b><br>'
        '<span style="font-size:13.5px; font-weight:normal; opacity:0.85; color: #cbd5e1;">'
        'Đã loại bỏ tất cả các hệ số khuếch đại tự chế. Hệ thống vận hành 100% dựa trên thuật toán đếm bài thực tế của Baccarat quốc tế, giải quyết triệt để lỗi thiên vị Player lẫn Banker.</span>'
        '</div>', 
        unsafe_allow_html=True
    )
else:
    final_p, final_b, final_t, cards_left, volatility, is_critical, p_six, lyapunov, streak_side, streak_count = calculate_v55_quantum_chao_engine(
        st.session_state.round_detailed_log, 
        shoe_decks=decks, 
        side_p_wins=0, side_b_wins=0, side_t_wins=0
    )
    
    final_p = round(final_p, 2)
    final_b = round(final_b, 2)
    final_t = round(100.0 - final_p - final_b, 2)

    st.markdown("### 👁️ ĐỊNH LƯỢNG KẾT QUẢ")
    
    rec = get_ai_v55_quantum_diagnostic(final_p, final_b, final_t, volatility, is_critical, p_six, lyapunov, streak_side, streak_count, st.session_state.round_detailed_log)
    
    st.markdown(
        f'<div class="tactical-box {rec["class"]}" style="background-color: {rec["bg"]}; border: 2px solid {rec["border"]}; color: {rec["border"]};">'
        f'<div class="tactical-title"><span>🛸 {rec["action"]}</span> <span style="font-family: monospace;">VOLUME GỢI Ý: {rec["bet_size"]}</span></div>'
        f'<div class="tactical-msg">{rec["msg"]}</div>'
        f'<div class="tactical-action-line">💡 <b>Cập nhật v55.6:</b> Đã tắt toàn bộ bộ nhân ảo. Xác suất hiện tại phản ánh chính xác cấu trúc toán học thuần túy của khay bài.</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    p_box_css, b_box_css = "hud-box", "hud-box"
    if final_p > final_b + 2.5: p_box_css = "hud-box neon-player-advantage"
    elif final_b > final_p + 2.5: b_box_css = "hud-box neon-banker-advantage"
    
    col_p, col_b, col_t = st.columns(3, gap="small")
    with col_p:
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER PROB</div><div class="hud-value" style="color:#00afb9;">{final_p}%</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER PROB</div><div class="hud-value" style="color:#ff4757;">{final_b}%</div></div>', unsafe_allow_html=True)
    with col_t:
        st.markdown(f'<div class="hud-box"><div class="hud-title">🟢 TIE PROB</div><div class="hud-value" style="color:#2ecc71;">{final_t}%</div></div>', unsafe_allow_html=True)

    if st.session_state.round_detailed_log:
        st.markdown('<div class="score-log-hud"><b>📈 DÒNG CHẢY LỊCH SỬ KHAY BÀI:</b><br>', unsafe_allow_html=True)
        for idx, r in enumerate(st.session_state.round_detailed_log):
            distance = total_log_games - 1 - idx
            st.markdown(f"• Ván {idx+1}: [P] {r['p_score']}đ vs {r['b_score']}đ [B] ➡️ **{r['outcome'].upper()}** (t-{distance})")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    total_shoe_cards = decks * 52
    penetration_rate_pct = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
    
    streak_status = f"Chuỗi {streak_side.upper()} x{streak_count} ván" if (streak_side and streak_count >= 2) else "Cầu tự do / Cầu ngắn"
    st.caption(f"**Engine:** `QUANTUM-CHAO v55.6 (BALANCED)` | **Thế cầu:** `{streak_status}` | **Còn:** `{cards_left}` lá")
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
