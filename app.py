import streamlit as st

# ==========================================
# THUẬT TOÁN TÍNH TOÁN XÁC SUẤT MA TRẬN NÂNG CẤP
# ==========================================
def calculate_baccarat_matrix(p_cards, b_cards, cards_played, shoe_decks=8):
    # Khởi tạo cấu trúc 1 bộ bài từ 1 đến 13 (A đến K) để tính ĐÔI chính xác
    # (Vì tính Đôi thì J-J là đôi, K-K là đôi, không gộp chung thành số 0 như tính điểm)
    deck_structure = {i: 4 for i in range(1, 14)} # 1=A, 11=J, 12=Q, 13=K
    total_shoe = {k: v * shoe_decks for k, v in deck_structure.items()}
    
    total_cards = shoe_decks * 52
    remaining_total = total_cards - cards_played
    
    if remaining_total <= 6:
        return "Hộp bài đã hết bài!", {}, 0.0, 0.0

    # Khấu trừ bài dựa trên số liệu tiêu thụ tích lũy tổng quan
    for k in total_shoe.keys():
        ratio = total_shoe[k] / total_cards
        total_shoe[k] = max(0.0, total_shoe[k] - (cards_played * ratio))

    # --- THUẬT TOÁN TÍNH XÁC SUẤT ĐÔI CHO VÁN TIẾP THEO ---
    # Công thức: Tổng xắc suất bốc lá thứ 1 (còn lại) * bốc lá thứ 2 trùng loại với lá thứ 1
    total_pair_prob = 0.0
    N = sum(total_shoe.values())
    
    if N > 1:
        for card_type, count in total_shoe.items():
            if count >= 2:
                # Xác suất lá 1 là card_type: count / N
                # Xác suất lá 2 cũng là card_type: (count - 1) / (N - 1)
                prob_this_pair = (count / N) * ((count - 1) / (N - 1))
                total_pair_prob += prob_this_pair
    
    # Do khay bài chưa chia, xác suất nền ban đầu của Player Pair và Banker Pair là như nhau
    pair_odds = round(total_pair_prob * 100, 2)

    # --- KHẤU TRỪ BÀI HIỆN TẠI ĐỂ TÍNH ĐIỂM (Quy về hệ 0-9) ---
    # Chuyển đổi mảng bài nhập vào sang dạng điểm Baccarat (10,J,Q,K = 0)
    p_calc_values = [0 if c >= 10 or c == 0 else c for c in p_cards]
    b_calc_values = [0 if c >= 10 or c == 0 else c for c in b_cards]

    # Trừ các lá bài đang lộ diện khỏi khay bài dùng để tính điểm
    shoe_for_score = {k: v * shoe_decks for k, v in {0: 16, 1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4}.items()}
    for k in shoe_for_score.keys():
        ratio = shoe_for_score[k] / total_cards
        shoe_for_score[k] = max(0.0, shoe_for_score[k] - (cards_played * ratio))
        
    for card in p_cards + b_cards:
        val = 0 if card >= 10 or card == 0 else card
        if shoe_for_score[val] > 0:
            shoe_for_score[val] -= 1

    p_score = sum(p_calc_values) % 10
    b_score = sum(b_calc_values) % 10

    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, total_shoe, pair_odds, pair_odds
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, total_shoe, pair_odds, pair_odds
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, total_shoe, pair_odds, pair_odds

    current_sum = sum(shoe_for_score.values())
    prob_dict = {k: v / current_sum for k, v in shoe_for_score.items()} if current_sum > 0 else {}

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
                if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, total_shoe, pair_odds, pair_odds
                elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, total_shoe, pair_odds, pair_odds
                else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, total_shoe, pair_odds, pair_odds
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
                        elif final_b > final_p: banker_wins += weight
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
    
    return odds_res, total_shoe, pair_odds, pair_odds

# ==========================================
# GIAO DIỆN ĐIỀU KHIỂN TRỰC QUAN (UI/UX)
# ==========================================
st.set_page_config(page_title="Baccarat Quantum Pro", page_icon="🎯", layout="centered")
st.title("🎯 Baccarat Quantum Pro")
st.caption("Phiên bản tối ưu phân tích xác suất Thắng, Hòa và Cặp Đôi (Pairs)")
st.markdown("---")

if 'total_cards_played' not in st.session_state:
    st.session_state.total_cards_played = 0

# THIẾT LẬP SÀN
st.subheader("⚙️ 1. Thiết lập cấu hình sàn")
c1, c2 = st.columns(2)
with c1:
    decks = st.selectbox("Số bộ bài trong khay (Shoe):", [8, 6, 4], index=0)
with c2:
    st.session_state.total_cards_played = st.number_input(
        "Số lá bài ĐÃ TIÊU THỤ tổng cộng:", 
        min_value=0, max_value=(decks * 52), value=st.session_state.total_cards_played
    )

# NHẬP LIỆU BÀI VÁN HIỆN TẠI
st.subheader("🃏 2. Nhập dữ liệu ván này")
st.caption("⚠️ Lưu ý nhập ĐÔI chính xác: Các quân J nhập 11, Q nhập 12, K nhập 13. Lá 10 nhập số 10. (Chỉ khi tính điểm máy mới tự quy về 0).")
col_p, col_b = st.columns(2)
with col_p:
    p_input = st.text_input("Bài PLAYER (Ví dụ: 5,11 hoặc 10,10,2):", "0")
with col_b:
    b_input = st.text_input("Bài BANKER (Ví dụ: 4,13 hoặc 3,1,12):", "0")

try:
    p_list = [int(x.strip()) for x in p_input.split(",") if x.strip() != ""]
    b_list = [int(x.strip()) for x in b_input.split(",") if x.strip() != ""]
except ValueError:
    st.error("⚠️ Vui lòng chỉ nhập số và phân tách bằng dấu phẩy!")
    p_list, b_list = [], []

# XỬ LÝ PHÂN TÍCH
if st.button("🚀 KHỞI CHẠY PHÂN TÍCH LỆNH", use_container_width=True):
    if p_list and b_list:
        p_calc = p_list[:2]
        b_calc = b_list[:2]
        
        res, remaining_deck, p_pair, b_pair = calculate_baccarat_matrix(
            p_calc, b_calc, st.session_state.total_cards_played, shoe_decks=decks
        )
        
        if isinstance(res, dict):
            # HIỂN THỊ CÁC CỬA CƯỢC CHÍNH
            st.markdown("### 📊 1. Xác suất các cửa cược chính:")
            col_res1, col_res2, col_res3 = st.columns(3)
            col_res1.metric(label="🔵 PLAYER WIN", value=f"{res['Player']}%")
            col_res2.metric(label="🔴 BANKER WIN", value=f"{res['Banker']}%")
            col_res3.metric(label="🟢 TIE (HÒA)", value=f"{res['Tie']}%")
            
            # HIỂN THỊ CÁC CỬA ĐÔI (MỚI)
            st.markdown("### 💎 2. Xác suất xuất hiện Cặp Đôi ván kế tiếp:")
            st.caption("Tỷ lệ toán học lý thuyết cho cửa Đôi là **7.47%** (Đền 1 ăn 11). Nên cân nhắc vào lệnh khi chỉ số vượt ngưỡng trung bình.")
            col_p_pair, col_b_pair = st.columns(2)
            
            # Đánh giá độ khả thi bằng màu sắc dựa trên toán học xác suất
            p_status = "🔥 Cao" if p_pair > 7.47 else "⚖️ Bình thường"
            b_status = "🔥 Cao" if b_pair > 7.47 else "⚖️ Bình thường"
            
            col_p_pair.metric(label="🔵 PLAYER PAIR (Con Đôi)", value=f"{p_pair}%", delta=p_status)
            col_b_pair.metric(label="🔴 BANKER PAIR (Cái Đôi)", value=f"{b_pair}%", delta=b_status)
            
            # CẬP NHẬT BỘ ĐẾM
            current_turn_cards = len(p_list) + len(b_list)
            st.session_state.total_cards_played += current_turn_cards
            st.success(f" Ghi nhận ván này tiêu thụ: **{current_turn_cards} lá**. Tổng tích lũy khay bài: **{st.session_state.total_cards_played} / {decks * 52} lá**.")
            
            # THỐNG KÊ CHI TIẾT
            with st.expander("🔍 Chi tiết số lượng 13 loại lá bài còn lại"):
                display_cols = st.columns(5)
                labels = {1:"A", 11:"J", 12:"Q", 13:"K"}
                for index, (card_num, rem_count) in enumerate(remaining_deck.items()):
                    card_label = labels.get(card_num, f"Lá [{card_num}]")
                    display_cols[index % 5].metric(label=f"Quân {card_label}", value=f"{int(rem_count)} lá")
        else:
            st.warning(res)
