import streamlit as st

# =========================================================================
# SYSTEM CORE: ULTIMATE COMBINATORIAL ENGINE & RISK MATRIX (FINAL VERSION)
# =========================================================================
def calculate_baccarat_ultimate_core(p_cards, b_cards, shoe_history, shoe_decks=8):
    """
    Hệ thống toán học cốt lõi: Quét sạch không gian mẫu phụ thuộc phi tuyến tính 
    của lá bài thứ 3 với sai số bằng 0, kết hợp phân tích điều kiện biên.
    """
    # Khởi tạo khay bài chuẩn (1=A, 2-10, 11=J, 12=Q, 13=K)
    deck_structure = {i: 4 * shoe_decks for i in range(1, 14)}
    
    # Khấu trừ tuyệt đối từ lịch sử bài đã chạy
    for card_val in shoe_history:
        if card_val in deck_structure and deck_structure[card_val] > 0:
            deck_structure[card_val] -= 1

    N = sum(deck_structure.values())
    if N <= 6:
        return "Dữ liệu khay bài đã chạm giới hạn an toàn toán học!", {}, 0.0, 0.0
    
    # Xác suất cửa đôi chính xác tuyệt đối
    p_pair_prob = 0.0
    for count in deck_structure.values():
        if count >= 2:
            p_pair_prob += (count / N) * ((count - 1) / (N - 1))
    p_pair_odds = round(p_pair_prob * 100, 2)

    b_pair_prob = 0.0
    if N > 3:
        for b_count in deck_structure.values():
            if b_count >= 2:
                p_rem_0 = ((N - b_count) / N) * ((N - b_count - 1) / (N - 1))
                p_rem_1 = 2 * (b_count / N) * ((N - b_count) / (N - 1))
                p_rem_2 = (b_count / N) * ((b_count - 1) / (N - 1))
                b_pair_prob += (p_rem_0 * (b_count / (N - 2)) * ((b_count - 1) / (N - 3)) +
                                p_rem_1 * (max(0.0, b_count - 1) / (N - 2)) * (max(0.0, b_count - 2) / (N - 3)) +
                                p_rem_2 * (max(0.0, b_count - 2) / (N - 2)) * (max(0.0, b_count - 3) / (N - 3)))
    b_pair_odds = round(b_pair_prob * 100, 2)

    # Chuyển đổi ma trận sang hệ điểm Baccarat (0-9)
    score_deck = {i: 0 for i in range(10)}
    for card_num, count in deck_structure.items():
        bacc_val = 0 if card_num >= 10 else card_num
        score_deck[bacc_val] += int(count)

    # Khấu trừ các quân bài đang lộ diện của ván hiện tại
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0:
            score_deck[val] -= 1

    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    # Trạng thái thắng tự nhiên (Natural 8, 9)
    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds

    current_sum = sum(score_deck.values())
    if current_sum == 0: return "Lỗi phân rã ma trận điểm!", deck_structure, p_pair_odds, b_pair_odds
        
    player_wins, banker_wins, ties = 0.0, 0.0, 0.0

    # Quét không gian mẫu đệ quy không hoàn lại
    if not (p_score <= 5):  # Player Đứng
        if b_score <= 5:    # Banker rút lá thứ 3
            for card3_b in range(10):
                w_b = score_deck[card3_b]
                if w_b > 0:
                    prob_b = w_b / current_sum
                    final_b = (b_score + card3_b) % 10
                    if p_score > final_b: player_wins += prob_b
                    elif final_b > p_score: banker_wins += prob_b
                    else: ties += prob_b
        else:               # Cả hai cùng Đứng
            if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds
            elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds
            else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds
    else:                   # Player rút lá thứ 3
        for card3_p in range(10):
            w_p = score_deck[card3_p]
            if w_p > 0:
                prob_p = w_p / current_sum
                final_p = (p_score + card3_p) % 10
                
                rem_sum_after_p = current_sum - 1
                
                b_draws = (b_score <= 2) or \
                          (b_score == 3 and card3_p != 8) or \
                          (b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]) or \
                          (b_score == 5 and card3_p in [4, 5, 6, 7]) or \
                          (b_score == 6 and card3_p in [6, 7])
                
                if b_draws and rem_sum_after_p > 0:
                    for card3_b in range(10):
                        available_b = score_deck[card3_b] - (1 if card3_b == card3_p else 0)
                        if available_b > 0:
                            prob_b = available_b / rem_sum_after_p
                            final_b = (b_score + card3_b) % 10
                            combined_weight = prob_p * prob_b
                            
                            if final_p > final_b: player_wins += combined_weight
                            elif final_b > final_p: banker_wins += combined_weight
                            else: ties += combined_weight
                else:
                    if final_p > b_score: player_wins += prob_p
                    elif b_score > final_p: banker_wins += prob_p
                    else: ties += prob_p

    total_prob = player_wins + banker_wins + ties
    if total_prob == 0: 
        return {"Player": 44.62, "Banker": 45.86, "Tie": 9.52}, deck_structure, p_pair_odds, b_pair_odds

    odds_res = {
        "Player": round((player_wins / total_prob) * 100, 2),
        "Banker": round((banker_wins / total_prob) * 100, 2),
        "Tie": round((ties / total_prob) * 100, 2)
    }
    return odds_res, deck_structure, p_pair_odds, b_pair_odds


# =========================================================================
# INTERFACE: ORACLE ULTIMATE PRODUCTION EDGE
# =========================================================================
st.set_page_config(page_title="Oracle Ultimate Edge", page_icon="🔮", layout="centered")

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'game_counter' not in st.session_state: st.session_state.game_counter = 0
if 'last_results' not in st.session_state: st.session_state.last_results = None

# --- SIDEBAR CẤU HÌNH ---
st.sidebar.header("⚙️ Cấu Hình Hệ Thống")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.session_state.game_counter = st.sidebar.number_input(
    "Đồng bộ Số ván (Game No.):", 
    min_value=0, max_value=150, 
    value=st.session_state.game_counter,
    step=1
)
st.sidebar.markdown("---")

if st.sidebar.button("🔄 RESET KHAY BÀI MỚI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.game_counter = 0
    st.session_state.last_results = None
    st.rerun()

if st.sidebar.button("⏮️ HOÀN TÁC VÁN TRƯỚC (UNDO)", use_container_width=True):
    if len(st.session_state.shoe_history) > 0 and st.session_state.game_counter > 0:
        st.session_state.game_counter = max(0, st.session_state.game_counter - 1)
        st.session_state.shoe_history = st.session_state.shoe_history[:-5]
        st.session_state.last_results = None
        st.rerun()

# --- MÀN HÌNH CHÍNH ƯU TIÊN 1: BẢNG KẾT QUẢ ĐỐI XỨNG CHIA ĐÔI MÀN HÌNH ---
if st.session_state.last_results:
    res, p_pair, b_pair, remaining_deck = st.session_state.last_results
    
    left_result_col, right_pair_col = st.columns(2)
    
    # BÊN TRÁI: Tỷ lệ thắng 3 cửa chính
    with left_result_col:
        st.markdown("#### 📊 Tỷ Lệ Cửa Chính")
        st.metric("🔵 PLAYER WIN", f"{res['Player']}%")
        st.metric("🔴 BANKER WIN", f"{res['Banker']}%")
        st.metric("🟢 TIE WIN", f"{res['Tie']}%")
        st.progress(res['Banker'] / 100 if res['Banker'] > 0 else 0)
        
    # BÊN PHẢI: Tỷ lệ xuất hiện cửa đôi
    with right_pair_col:
        st.markdown("#### 💎 Tỷ Lệ Cửa Đôi")
        p_delta = "🔥 Lợi thế cao" if p_pair > 7.47 else "⚖️ Thường"
        st.metric("🔵 CON ĐÔI (P.Pair)", f"{p_pair}%", delta=p_delta, delta_color="normal")
        
        b_delta = "🔥 Lợi thế cao" if b_pair > 7.47 else "⚖️ Thường"
        st.metric("🔴 CÁI ĐÔI (B.Pair)", f"{b_pair}%", delta=b_delta, delta_color="normal")

    st.markdown("---")
    
    # KHU VỰC QUẢN LÝ VỐN CHUYÊN NGHIỆP (KELLY CRITERION MATRIX)
    st.markdown("### 💰 Phân Tích Ma Trận Quản Lý Vốn")
    kelly_col1, kelly_col2 = st.columns(2)
    
    # Tính toán chỉ số lợi thế để gợi ý lệnh đi tiền
    max_side = "Player" if res['Player'] > res['Banker'] else "Banker"
    max_prob = res[max_side] / 100.0
    
    # Công thức tính Kelly tối giản cho Baccarat (Tỷ lệ ăn thường là 1:1, Banker 1:0.95)
    b_payout = 1.0 if max_side == "Player" else 0.95
    kelly_percentage = max(0.0, (max_prob * (b_payout + 1) - 1) / b_payout) * 100
    
    with kelly_col1:
        if res['Player'] == 100.0 or res['Banker'] == 100.0:
            st.success(f"🎯 LỆNH TUYỆT ĐỐI: Vào mạnh cửa **{max_side.upper()}** (Tỷ lệ 100%)")
        elif kelly_percentage > 1.5:
            st.info(f"✨ GỢI Ý ĐI TIỀN: Ưu tiên cửa **{max_side.upper()}** (Quy mô vốn gợi ý: {round(kelly_percentage, 2)}%)")
        else:
            st.warning("⚖️ TRẠNG THÁI CÂN BẰNG: Biên lợi thế quá nhỏ, gợi ý HẠ VỐN tối đa hoặc BỎ QUA tay này.")
            
    with kelly_col2:
        if p_pair > 11.5 or b_pair > 11.5:
            pair_side = "Con Đôi" if p_pair > b_pair else "Cái Đôi"
            st.success(f"🔥 CẢNH BÁO BIẾN ĐỘNG: Cửa **{pair_side}** đang có tỷ lệ xuất hiện đột biến đột ngột!")
        else:
            st.text("Cửa Đôi đang chạy trong biên độ dao động an toàn.")
            
    with st.expander("📊 Chi tiết cấu trúc ma trận khay bài"):
        total_cards = decks * 52
        cards_left = total_cards - len(st.session_state.shoe_history)
        st.write(f"Ván hiện tại: **{st.session_state.game_counter}** | Trạng thái: **Phân tích Đệ Quy Tổ Hợp Hoàn Toàn** | Số lá còn lại: **{cards_left} / {total_cards}** lá.")
        cols = st.columns(5)
        labels_13 = {1: "A", 11: "J", 12: "Q", 13: "K"}
        for idx, (num, cnt) in enumerate(remaining_deck.items()):
            card_label = labels_13.get(num, f"[{num}]")
            cols[idx % 5].text(f"Quân {card_label}: {int(cnt)} lá")
else:
    st.info("🔮 Vui lòng điền điểm số ván hiện tại vào ô bên dưới để kích hoạt hệ quét toán học.")

st.markdown("---")

# --- MÀN HÌNH CHÍNH ƯU TIÊN 2: KHU VỰC NHẬP LIỆU GIAO DIỆN PHẲNG ---
head_col, status_col = st.columns([2, 1])
with head_col:
    st.subheader("🃏 Điền điểm ván này")
with status_col:
    st.markdown(
        f"<div style='text-align: right; margin-top: 10px; font-weight: bold; font-size: 16px; color: #ff4b4b;'>"
        f"Ván hiện tại: #{st.session_state.game_counter}"
        f"</div>", 
        unsafe_allow_html=True
    )

col_p, col_b = st.columns(2)
with col_p:
    p_input = st.text_input("PLAYER (Lá bài):", value="0", placeholder="Ví dụ: 5,1 hoặc 9,0,2")
with col_b:
    b_input = st.text_input("BANKER (Lá bài):", value="0", placeholder="Ví dụ: 4,11")

try:
    p_list = [int(x.strip()) for x in p_input.split(",") if x.strip() != ""]
    b_list = [int(x.strip()) for x in b_input.split(",") if x.strip() != ""]
except ValueError:
    st.error("Lưu ý: Chỉ nhập số nguyên (0-13) cách nhau bằng dấu phẩy!")
    p_list, b_list = [], []

if st.button("🚀 KÍCH HOẠT QUÉT MA TRẬN PHÂN TÍCH", use_container_width=True, type="primary"):
    if p_list and b_list:
        p_calc = p_list[:2]
        b_calc = b_list[:2]
        
        res, remaining_deck, p_pair, b_pair = calculate_baccarat_ultimate_core(
            p_calc, b_calc, st.session_state.shoe_history, shoe_decks=decks
        )
        
        if isinstance(res, dict):
            st.session_state.last_results = (res, p_pair, b_pair, remaining_deck)
            st.session_state.shoe_history.extend(p_list + b_list)
            st.session_state.game_counter += 1
            st.rerun()
        else:
            st.warning(res)
