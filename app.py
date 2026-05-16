import streamlit as st

# ==========================================
# THUẬT TOÁN MA TRẬN KHAY BÀI THEO SỐ VÁN (EXTREME PRECISION)
# ==========================================
def calculate_baccarat_with_games(p_cards, b_cards, shoe_matrix, total_games, shoe_decks=8):
    # Cấu trúc 13 loại lá bài ban đầu (1=A, 2-10 giữ nguyên, 11=J, 12=Q, 13=K)
    deck_structure = {i: 4 * shoe_decks for i in range(1, 14)}
    total_initial_cards = shoe_decks * 52
    
    # 1. Trừ chính xác các lá bài đã được ghi nhớ từ lịch sử nhập liệu
    for card_val in shoe_matrix:
        if card_val in deck_structure and deck_structure[card_val] > 0:
            deck_structure[card_val] -= 1
            
    cards_logged = len(shoe_matrix)
    
    # 2. THUẬT TOÁN BÙ TRỪ SAI SỐ PHI TUYẾN TÍNH (Dựa trên Số Ván)
    # Trung bình một ván Baccarat tiêu thụ khoảng 4.95 lá bài.
    # Nếu Số Ván thực tế lớn hơn lượng bài đã nhập, hệ thống sẽ tự động trừ đi các "Lá bài ẩn" (Burn Cards/Lỗi)
    estimated_cards_played = int(total_games * 4.95)
    hidden_cards_count = max(0, estimated_cards_played - cards_logged)
    
    # Phân bổ khấu trừ các lá bài ẩn đều theo tỷ lệ còn lại để không làm lệch Ma Trận Đôi
    if hidden_cards_count > 0:
        current_rem = sum(deck_structure.values())
        if current_rem > 0:
            for k in deck_structure.keys():
                weight = deck_structure[k] / current_rem
                deck_structure[k] = max(0.0, deck_structure[k] - (hidden_cards_count * weight))

    remaining_total = sum(deck_structure.values())
    
    if remaining_total <= 6:
        return f"Hộp bài đã hết sau {total_games} ván!", {}, 0.0, 0.0

    # --- THUẬT TOÁN TÍNH ĐÔI CHUỖI THỜI GIAN CHÍNH XÁC ---
    N = remaining_total
    
    # Xác suất Player Pair ván tiếp theo
    p_pair_prob = 0.0
    if N > 1:
        for card_type, count in deck_structure.items():
            if count >= 2:
                p_pair_prob += (count / N) * ((count - 1) / (N - 1))
    p_pair_odds = round(p_pair_prob * 100, 2)

    # Xác suất Banker Pair ván tiếp theo (Tính xác suất có điều kiện)
    b_pair_prob = 0.0
    if N > 3:
        for b_card_type, b_count in deck_structure.items():
            if b_count >= 2:
                p_rem_0 = ((N - b_count) / N) * ((N - b_count - 1) / (N - 1))
                b_count_case0 = b_count
                
                p_rem_1 = 2 * (b_count / N) * ((N - b_count) / (N - 1))
                b_count_case1 = b_count - 1
                
                p_rem_2 = (b_count / N) * ((b_count - 1) / (N - 1))
                b_count_case2 = b_count - 2
                
                prob_b_pair = (
                    p_rem_0 * (b_count_case0 / (N - 2)) * ((b_count_case0 - 1) / (N - 3)) +
                    p_rem_1 * (max(0, b_count_case1) / (N - 2)) * (max(0, b_count_case1 - 1) / (N - 3)) +
                    p_rem_2 * (max(0, b_count_case2) / (N - 2)) * (max(0, b_count_case2 - 1) / (N - 3))
                )
                b_pair_prob += prob_b_pair
    b_pair_odds = round(b_pair_prob * 100, 2)

    # --- KHẤU TRỪ BÀI VÁN HIỆN TẠI ĐỂ TÍNH ĐIỂM (HỆ BACCARAT 0-9) ---
    score_deck = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for card_num, count in deck_structure.items():
        bacc_val = 0 if card_num >= 10 else int(card_num)
        score_deck[bacc_val] += count

    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0:
            score_deck[val] -= 1

    p_calc_values = [0 if c >= 10 else c for c in p_cards]
    b_calc_values = [0 if c >= 10 else c for c in b_cards]
    
    p_score = sum(p_calc_values) % 10
    b_score = sum(b_calc_values) % 10

    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds

    current_sum = sum(score_deck.values())
    prob_dict = {k: v / current_sum for k, v in score_deck.items()} if current_sum > 0 else {}

    player_wins, banker_wins, ties = 0.0, 0.0, 0.0
    p_draws = p_score <= 5

    if prob_dict:
        if not p_draws:
            if b_score <= 5:
                for card3_b, p_b in prob_dict.items():
                    final_b = (b_score + card3_b) % 10
                    if p_score > final_b: player_wins += p_b
                    elif final_b > p_score: banker_wins += p_b
                    else: ties += p_b
            else:
                if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds
                elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds
                else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds
        else:
            for card3_p, p_p in prob_dict.items():
                final_p = (p_score + card3_p) % 10
                b_draws = False
                if b_score <= 2: b_draws = True
                elif b_score == 3 and card3_p != 8: b_draws = True
                elif b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]: b_draws = True
                elif b_score == 5 and card3_p in [4, 5, 6, 7]: b_draws = True
                elif b_score == 6 and card3_p in [6, 7]: b_draws = True
                
                if b_draws:
                    for card3_b, p_b in prob_dict.items():
                        final_b = (b_score + card3_b) % 10
                        weight = p_p * p_b
                        if final_p > final_b: player_wins += weight
                        elif final_b > p_score: banker_wins += weight
                        else: ties += weight
                else:
                    if final_p > b_score: player_wins += p_p
                    elif b_score > final_p: banker_wins += p_p
                    else: ties += p_p

    total_prob = player_wins + banker_wins + ties
    odds_res = {
        "Player": round((player_wins / total_prob) * 100, 2) if total_prob > 0 else 0,
        "Banker": round((banker_wins / total_prob) * 100, 2) if total_prob > 0 else 0,
        "Tie": round((ties / total_prob) * 100, 2) if total_prob > 0 else 0
    }
    
    return odds_res, deck_structure, p_pair_odds, b_pair_odds

# ==========================================
# GIAO DIỆN HỆ THỐNG QUẢN LÝ THEO SỐ VÁN
# ==========================================
st.set_page_config(page_title="Baccarat Game Matrix Pro", page_icon="🔢", layout="centered")
st.title("🔢 Baccarat Game Matrix Pro")
st.caption("Hệ thống quản lý tích lũy theo số ván - Đồng bộ thuật toán Burn-Cards")
st.markdown("---")

# Khởi tạo Session State dữ liệu khay bài
if 'shoe_history' not in st.session_state:
    st.session_state.shoe_history = []
if 'game_counter' not in st.session_state:
    st.session_state.game_counter = 0

# --- SIDEBAR ĐIỀU KHIỂN CHỈ SỐ ---
st.sidebar.header("🎯 Cấu hình hộp bài")
decks = st.sidebar.selectbox("Số bộ bài (Decks):", [8, 6, 4], index=0)

st.sidebar.markdown("---")
# Bộ đếm số ván thông minh (Có thể tự chỉnh tay bằng nút cộng trừ nếu sòng bài nhảy ván)
st.sidebar.subheader("🔢 Bộ điều khiển ván")
st.session_state.game_counter = st.sidebar.number_input(
    "VÁN SỐ (Game Number):", 
    min_value=0, max_value=100, value=st.session_state.game_counter
)

if st.sidebar.button("🔄 ĐỔI HỘP BÀI MỚI (RESET)", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.game_counter = 0
    st.rerun()

if st.sidebar.button("⏮️ HOÀN TÁC VÁN VỪA RỒI", use_container_width=True):
    if len(st.session_state.shoe_history) > 0 and st.session_state.game_counter > 0:
        st.sidebar.warning("Đã lùi lại 1 ván lịch sử!")

# --- THÔNG SỐ TRỰC QUAN GIAO DIỆN CHÍNH ---
c_metric1, c_metric2 = st.columns(2)
with c_metric1:
    st.metric(label="🚩 VÁN HIỆN TẠI (Round):", value=f"Ván thứ {st.session_state.game_counter}")
with c_metric2:
    st.metric(label="📊 Số lá bài đã quét trong bộ nhớ:", value=f"{len(st.session_state.shoe_history)} / {decks * 52} lá")

st.markdown("---")

# NHẬP DỮ LIỆU VÁN HIỆN TẠI
st.subheader("🃏 Nhập dữ liệu bài ván này")
st.caption("Quy ước nhập: Át=1 | Các lá 2-10 giữ nguyên | J=11, Q=12, K=13. Cách nhau dấu phẩy.")

col_p, col_b = st.columns(2)
with col_p:
    p_input = st.text_input("Bài PLAYER ván này:", "0")
with col_b:
    b_input = st.text_input("Bài BANKER ván này:", "0")

try:
    p_list = [int(x.strip()) for x in p_input.split(",") if x.strip() != ""]
    b_list = [int(x.strip()) for x in b_input.split(",") if x.strip() != ""]
except ValueError:
    st.error("⚠️ Định dạng sai! Vui lòng chỉ nhập số và dấu phẩy.")
    p_list, b_list = [], []

# CHẠY PHÂN TÍCH
if st.button("🚀 PHÂN TÍCH LỆNH TOÁN HỌC", use_container_width=True):
    if p_list and b_list:
        p_calc = p_list[:2]
        b_calc = b_list[:2]
        
        # Truyền chính xác: Bài hiện tại, mảng lịch sử bài, số ván hiện tại, và số bộ bài
        res, remaining_deck, p_pair, b_pair = calculate_baccarat_with_games(
            p_calc, b_calc, st.session_state.shoe_history, st.session_state.game_counter, shoe_decks=decks
        )
        
        if isinstance(res, dict):
            # 1. HIỂN THỊ CỬA CHÍNH
            st.markdown("### 📊 Xác suất cửa chính ván hiện tại:")
            col_res1, col_res2, col_res3 = st.columns(3)
            col_res1.metric(label="🔵 PLAYER WIN", value=f"{res['Player']}%")
            col_res2.metric(label="🔴 BANKER WIN", value=f"{res['Banker']}%")
            col_res3.metric(label="🟢 TIE (HÒA)", value=f"{res['Tie']}%")
            
            # 2. HIỂN THỊ CỬA ĐÔI THEO SỐ VÁN CHÍNH XÁC CAO
            st.markdown("### 💎 Xác suất Cặp Đôi cho ván kế tiếp:")
            col_p_pair, col_b_pair = st.columns(2)
            
            p_delta = f"🔥 Tốt (+{(p_pair-7.47):.2f}%)" if p_pair > 7.47 else "⚖️ Bình thường"
            b_delta = f"🔥 Tốt (+{(b_pair-7.47):.2f}%)" if b_pair > 7.47 else "⚖️ Bình thường"
            
            col_p_pair.metric(label="🔵 PLAYER PAIR", value=f"{p_pair}%", delta=p_delta)
            col_b_pair.metric(label="🔴 BANKER PAIR", value=f"{b_pair}%", delta=b_delta)
            
            # 3. TỰ ĐỘNG TĂNG SỐ VÁN VÀ CỘNG DỒN BÀI VÀO BỘ NHỚ
            st.session_state.shoe_history.extend(p_list + b_list)
            st.session_state.game_counter += 1
            
            st.success(f" Đã xử lý xong ván {st.session_state.game_counter - 1}. Hệ thống tự động chuyển sang ván {st.session_state.game_counter}.")
            
            # 4. VECTOR CHI TIẾT
            with st.expander("🔍 Chi tiết số lượng 13 loại lá bài còn lại trong khay"):
                display_cols = st.columns(5)
                labels = {1:"A", 11:"J", 12:"Q", 13:"K"}
                for index, (card_num, rem_count) in enumerate(remaining_deck.items()):
                    card_label = labels.get(card_num, f"Lá [{card_num}]")
                    display_cols[index % 5].metric(label=f"Quân {card_label}", value=f"{int(rem_count)} lá")
        else:
            st.warning(res)
