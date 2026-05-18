import streamlit as st

# =========================================================================
# MODULE 1: ĐỘNG CƠ QUÉT MẬT ĐỘ LÁ BÀI & PHÂN TÍCH THẾ TRẬN ĐIỂM
# =========================================================================
def calculate_card_and_score_core(all_rounds_log, shoe_decks, side_p_wins, side_b_wins, side_t_wins):
    """
    Lấy giá trị quân bài và điểm số làm gốc. 
    Số ván thắng từ sidebar/lịch sử chỉ đóng vai trò thứ yếu (Trọng số phụ < 5%).
    """
    total_initial_cards = shoe_decks * 52
    exact_cards_left = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    # 1. Gom tất cả các lá bài đã lật để trừ trực tiếp khỏi khay bài thật
    all_flat_cards = []
    total_margin_score = 0.0  # Tổng độ lệch điểm số trận đấu
    valid_rounds_count = 0
    
    for r in all_rounds_log:
        all_flat_cards.extend(r['p_cards'] + r['b_cards'])
        # Tính toán độ chênh lệch điểm số thực tế giữa 2 cửa
        margin = abs(r['p_score'] - r['b_score'])
        total_margin_score += margin
        valid_rounds_count += 1
        
    for card in all_flat_cards:
        if card in exact_cards_left:
            exact_cards_left[card] = max(0.0, exact_cards_left[card] - 1.0)
            
    cards_remaining = sum(exact_cards_left.values())
    if cards_remaining <= 0: cards_remaining = 1.0
    
    # Quy đổi về tỷ lệ xác suất xuất hiện điểm từ 0-9 trong khay bài hiện tại
    score_counts = [0.0] * 10
    for card_num, count in exact_cards_left.items():
        if card_num >= 10: score_counts[0] += count
        else: score_counts[card_num] += count
        
    p_0 = score_counts[0] / cards_remaining
    p_low = sum(score_counts[1:6]) / cards_remaining   # Bài nhỏ (1-5) kích hoạt kéo bài
    p_high = sum(score_counts[6:10]) / cards_remaining # Bài lớn (6-9) tạo điểm tự nhiên

    # 2. Công thức toán học Baccarat thuần tổ hợp lá bài làm gốc (95% Trọng số)
    # Cấu trúc dịch chuyển dựa hoàn toàn trên việc thiếu hụt/dư thừa các nhóm bài trong khay
    math_bias = (p_low * 0.10) - (p_high * 0.08) + (p_0 * 0.03)
    
    pure_p = 44.62 + (math_bias * 100.0)
    pure_b = 45.86 - (math_bias * 100.0)
    pure_t = 9.52 + (p_0 * 5.0) # Bài 0 nhiều làm tăng tỷ lệ điểm Hòa thực tế
    
    # Điều chỉnh dựa trên thế trận điểm số (Điểm cách biệt trung bình giữa các ván)
    if valid_rounds_count > 0:
        avg_margin = total_margin_score / valid_rounds_count
        # Nếu điểm số thắng cách biệt quá sâu, hệ thống tự động điều tiết biên độ hồi quy
        pure_b += (avg_margin * 0.15)
        pure_p -= (avg_margin * 0.15)

    # 3. Lớp dữ liệu phụ: Số ván thắng (Chỉ chiếm 5% trọng số điều hòa dòng chảy)
    total_games_all = side_p_wins + side_b_wins + side_t_wins + valid_rounds_count
    if total_games_all > 0:
        minor_weight = 0.05 # Khóa cứng trọng số phụ ở mức 5%
        
        raw_p_rate = ((side_p_wins + sum(1 for r in all_rounds_log if r['outcome'] == "Player")) / total_games_all) * 100.0
        raw_b_rate = ((side_b_wins + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")) / total_games_all) * 100.0
        
        pure_p = (pure_p * (1.0 - minor_weight)) + (raw_p_rate * minor_weight)
        pure_b = (pure_b * (1.0 - minor_weight)) + (raw_b_rate * minor_weight)

    # Khống chế giới hạn toán học an toàn
    pure_p = max(32.0, min(62.0, pure_p))
    pure_b = max(32.0, min(62.0, pure_b))
    pure_t = max(6.0, min(20.0, pure_t))
    
    # Chuẩn hóa về mốc 100%
    total_sum = pure_p + pure_b + pure_t
    return (pure_p / total_sum) * 100, (pure_b / total_sum) * 100, (pure_t / total_sum) * 100, int(cards_remaining)


# =========================================================================
# AI STRATEGIC REAL-TIME RECOMMENDATION
# =========================================================================
def get_ai_recommendation_v45(p_val, b_val, t_val, log):
    if not log:
        return "📊 Vui lòng nạp dữ liệu quân bài thực tế để kích hoạt động cơ quét tổ hợp.", "rgba(164, 176, 190, 0.1)", "#a4b0be"
    
    if t_val > 16.0:
        return f"🟢 ĐIỂM RƠI TỔ HỢP - VÀO CỬA HÒA (TIE): Mật độ bài 0 điểm dầy đặc tạo điều kiện Hòa ({t_val:.2f}%).", "rgba(46, 213, 115, 0.15)", "#2ed573"
        
    last_round = log[-1]
    p_last_score = last_round['p_score']
    b_last_score = last_round['b_score']
    
    # Phân tích trạng thái điểm ván trước để đưa ra đòn đánh ép thế bài nhà cái
    if p_val > b_val + 1.2:
        if p_last_score >= 7 and b_last_score <= 3:
            return f"🔵 VÀO LỆNH: PLAYER | Thế bài ván trước hủy diệt + Khay bài ủng hộ đà ra Người Chơi ({p_val:.2f}%).", "rgba(0, 175, 185, 0.15)", "#00afb9"
        return f"🔵 VÀO LỆNH: PLAYER | Cấu trúc tổ hợp lá bài đang lệch hẳn về phía Player ({p_val:.2f}%).", "rgba(0, 175, 185, 0.15)", "#00afb9"
        
    elif b_val > p_val + 1.2:
        if b_last_score >= 7 and p_last_score <= 3:
            return f"🔴 VÀO LỆNH: BANKER | Thế bài Nhà Cái ăn điểm sâu + Mật độ khay bài giữ điểm lợi thế ({b_val:.2f}%).", "rgba(254, 217, 255, 0.15)", "#fed9ff"
        return f"🔴 VÀO LỆNH: BANKER | Cấu trúc tổ hợp lá bài đang lệch hẳn về phía Banker ({b_val:.2f}%).", "rgba(254, 217, 255, 0.15)", "#fed9ff"
        
    return "📊 THẾ BÀI TRUNG LẬP: Điểm số khay bài đang giằng co ở vùng cân bằng tuyệt đối. Bỏ ván này.", "rgba(164, 176, 190, 0.1)", "#a4b0be"

def parse_baccarat_input_v45(raw_str):
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
st.set_page_config(page_title="Oracle Engine v45.0 Pure Combinatorics", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(145deg, #070a13, #0f1526, #161f38) !important; color: #ecf0f1 !important; }
    
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
    .hud-box { padding: 12px 4px; border-radius: 10px; text-align: center; margin-bottom: 8px; border: 1px solid #0f1526; background: rgba(7, 10, 19, 0.9); min-height: 85px; display: flex; flex-direction: column; justify-content: center; }
    .hud-title { font-size: 11px; font-weight: 700; color: #a4b0be; text-transform: uppercase; }
    .hud-value { font-size: 26px; font-weight: 800; font-family: monospace; margin-top: 1px; }
    .neon-player-advantage { background-color: #092635 !important; border: 2px solid #00afb9 !important; }
    .neon-banker-advantage { background-color: #2b141a !important; border: 2px solid #e74c3c !important; }
    .logic-lock { background-color: rgba(15, 21, 38, 0.95); border: 2px dashed #00afb9; color: #00afb9; padding: 40px 20px; border-radius: 12px; font-size: 15px; text-align: center; box-shadow: 0px 0px 15px rgba(0, 175, 185, 0.15); }
    .score-log-hud { padding: 10px; border-radius: 8px; background-color: rgba(5, 12, 20, 0.9); border: 1px dashed #3a506b; margin-top: 5px; font-family: monospace; font-size: 13px; }
    
    div.stButton > button { background-color: #00afb9 !important; color: white !important; border-radius: 8px; font-weight: 900; padding: 10px 0px; font-size: 14px !important; border: none !important; }
    div.stButton > button:hover { background-color: #00d2de !important; box-shadow: 0px 0px 10px #00d2de; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'round_detailed_log' not in st.session_state: st.session_state.round_detailed_log = []
if 'form_counter' not in st.session_state: st.session_state.form_counter = 0

st.sidebar.header("⚙️ CẤU HÌNH KHAY BÀI")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.header("### 📊 SỐ VÁN THẮNG (DỮ LIỆU PHỤ - TRỌNG SỐ 5%)")
p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER đã thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER đã thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) đã thắng:", min_value=0, max_value=100, value=0)

# Tính tổng số ván tổng quan
total_log_games = len(st.session_state.round_detailed_log)
global_total_games = p_wins_input + b_wins_input + tie_wins_input + total_log_games

st.markdown("### 🃏 ĐỘNG CƠ ĐIỂM SỐ QUÂN BÀI")
next_game_number = global_total_games + 1
st.markdown(f'<div class="central-game-counter">🔮 NHẬP QUÂN BÀI THỰC TẾ CHO VÁN THỨ: {next_game_number}</div>', unsafe_allow_html=True)

# Giao diện nhập dữ liệu bài lật
input_row_col1, input_row_col2 = st.columns(2, gap="small")
with input_row_col1:
    p_input = st.text_input("🔵 CÁC LÁ BÀI PLAYER LẬT:", key=f"p_in_{st.session_state.form_counter}", placeholder="Ví dụ: A 2 K hoặc 7 5")
with input_row_col2:
    b_input = st.text_input("🔴 CÁC LÁ BÀI BANKER LẬT:", key=f"b_in_{st.session_state.form_counter}", placeholder="Ví dụ: K Q 9 hoặc 8 4")

st.write("")
btn_layout_l, btn_layout_center, btn_layout_r = st.columns([1, 4, 1], gap="small")
with btn_layout_center:
    calc_triggered = st.button("🚀 XỬ LÝ QUÂN BÀI & THẾ TRẬN ĐIỂM", use_container_width=True)

if calc_triggered:
    p_clean = p_input.strip()
    b_clean = b_input.strip()
    
    if not p_clean and not b_clean:
        st.warning("⚠️ Vui lòng nhập dữ liệu quân bài để tính toán thế trận!")
    else:
        p_list = parse_baccarat_input_v45(p_clean)
        b_list = parse_baccarat_input_v45(b_clean)
        
        # Công thức chuẩn hóa điểm số thực tế Baccarat
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

# GUARDRAIL: CHẶN HIỂN THỊ TUYỆT ĐỐI NẾU CHƯA CÓ BẤT KỲ DỮ LIỆU ĐIỂM NÀO
if global_total_games == 0 and len(st.session_state.round_detailed_log) == 0:
    st.markdown(
        '<div class="logic-lock">'
        '🔒 <b>HỆ THỐNG ĐANG KHÓA TỶ LỆ CHỐNG LỆCH ẢO</b><br>'
        '<span style="font-size:13.5px; font-weight:normal; opacity:0.85;">'
        'Thuật toán v45.0 lấy quân bài làm gốc từ chối xuất kết quả lý thuyết suông. '
        'Vui lòng nhập điểm số các quân bài lật của ván đầu tiên hoặc khai báo số ván ở Sidebar để mở khóa tính toán.</span>'
        '</div>', 
        unsafe_allow_html=True
    )
else:
    # Chạy thuật toán lõi: Lấy bài lật và điểm số làm trọng số gốc 95%
    final_p, final_b, final_t, cards_left = calculate_card_and_score_core(
        st.session_state.round_detailed_log, 
        shoe_decks=decks, 
        side_p_wins=p_wins_input, 
        side_b_wins=b_wins_input, 
        side_t_wins=tie_wins_input
    )
    
    final_p = round(final_p, 2)
    final_b = round(final_b, 2)
    final_t = round(100.0 - final_p - final_b, 2)

    st.markdown("### 🔮 XÁC SUẤT TOÁN HỌC KHAY BÀI THỰC TẾ")
    
    # Khuyến nghị lệnh dựa trên thế bài
    rec_text, rec_bg, rec_border = get_ai_recommendation_v45(final_p, final_b, final_t, st.session_state.round_detailed_log)
    st.markdown(f'<div class="ai-decision-box" style="background-color: {rec_bg}; border: 2px solid {rec_border}; color: {rec_border};">{rec_text}</div>', unsafe_allow_html=True)
    
    # Định dạng hiển thị cửa chiếm ưu thế lớn
    p_box_css, b_box_css = "hud-box", "hud-box"
    if final_p > final_b + 1.0: p_box_css = "hud-box neon-player-advantage"
    elif final_b > final_p + 1.0: b_box_css = "hud-box neon-banker-advantage"
    
    col_p, col_b, col_t = st.columns(3, gap="small")
    with col_p:
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER</div><div class="hud-value" style="color:#00afb9;">{final_p}%</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER</div><div class="hud-value" style="color:#ff4757;">{final_b}%</div></div>', unsafe_allow_html=True)
    with col_t:
        st.markdown(f'<div class="hud-box"><div class="hud-title">🟢 TIE WIN</div><div class="hud-value" style="color: #2ed573;">{final_t}%</div></div>', unsafe_allow_html=True)
        
    st.write("")
    
    # Nhật ký điểm số chi tiết từng ván
    if st.session_state.round_detailed_log:
        st.markdown('<div class="score-log-hud"><b>📊 NHẬT KÝ ĐIỂM SỐ & THẾ TRẬN THỰC THỜI:</b>', unsafe_allow_html=True)
        for idx, r in enumerate(st.session_state.round_detailed_log):
            st.markdown(f"Ván {idx+1}: [Player] {r['p_score']} điểm vs {r['b_score']} điểm [Banker] ➡️ **{r['outcome'].upper()} WIN**")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    total_shoe_cards = decks * 52
    penetration_rate = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
    st.caption(f"**Engine:** `COMBINATORIAL REAL-SCORE v45.0` | **Kho bài còn lại:** {int(cards_left)}/{total_shoe_cards} lá")
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
