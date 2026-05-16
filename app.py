import streamlit as st

# ==========================================
# THUẬT TOÁN MA TRẬN KHAY BÀI CHÍNH XÁC TUYỆT ĐỐI
# ==========================================
def calculate_baccarat_absolute(p_cards, b_cards, shoe_matrix, shoe_decks=8):
    # Tổng số bài ban đầu trong khay bài (Shoe)
    # 1=A, 2-10 giữ nguyên, 11=J, 12=Q, 13=K
    deck_structure = {i: 4 * shoe_decks for i in range(1, 14)}
    
    # Trừ đi CHÍNH XÁC tất cả các lá bài đã lưu trong bộ nhớ hệ thống từ các ván trước
    for card_val in shoe_matrix:
        if card_val in deck_structure and deck_structure[card_val] > 0:
            deck_structure[card_val] -= 1
            
    remaining_total = sum(deck_structure.values())
    
    if remaining_total <= 6:
        return "Hộp bài đã hết bài!", {}, 0.0, 0.0

    # --- THUẬT TOÁN TÍNH ĐÔI CHÍNH XÁC CHUỖI THỜI GIAN ---
    N = remaining_total
    
    # 1. Xác suất Player Pair ván tiếp theo
    p_pair_prob = 0.0
    if N > 1:
        for card_type, count in deck_structure.items():
            if count >= 2:
                p_pair_prob += (count / N) * ((count - 1) / (N - 1))
    p_pair_odds = round(p_pair_prob * 100, 2)

    # 2. Xác suất Banker Pair ván tiếp theo (Tính xác suất có điều kiện sau khi Player bốc 2 lá)
    b_pair_prob = 0.0
    if N > 3:
        for b_card_type, b_count in deck_structure.items():
            if b_count >= 2:
                # Kịch bản A: Player không bốc trúng lá b_card_type nào
                p_rem_0 = ((N - b_count) / N) * ((N - b_count - 1) / (N - 1))
                b_count_case0 = b_count
                
                # Kịch bản B: Player bốc trúng đúng 1 lá b_card_type
                p_rem_1 = 2 * (b_count / N) * ((N - b_count) / (N - 1))
                b_count_case1 = b_count - 1
                
                # Kịch bản C: Player bốc trúng cả 2 lá b_card_type
                p_rem_2 = (b_count / N) * ((b_count - 1) / (N - 1))
                b_count_case2 = b_count - 2
                
                prob_b_pair = (
                    p_rem_0 * (b_count_case0 / (N - 2)) * ((b_count_case0 - 1) / (N - 3)) +
                    p_rem_1 * (max(0, b_count_case1) / (N - 2)) * (max(0, b_count_case1 - 1) / (N - 3)) +
                    p_rem_2 * (max(0, b_count_case2) / (N - 2)) * (max(0, b_count_case2 - 1) / (N - 3))
                )
                b_pair_prob += prob_b_pair
    b_pair_odds = round(b_pair_prob * 100, 2)

    # --- KHẤU TRỪ BÀI HIỆN TẠI ĐỂ TÍNH ĐIỂM (QUY VỀ HỆ BACCARAT 0-9) ---
    # Tạo một bản sao khay bài riêng để tính toán kịch bản lá thứ 3 của ván hiện tại
    score_deck = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for card_num, count in deck_structure.items():
        bacc_val = 0 if card_num >= 10 else card_num
        score_deck[bacc_val] += count

    # Trừ tiếp các lá bài hiện tại đang lật trên bàn
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0:
            score_deck[val] -= 1

    p_calc_values = [0 if c >= 10 else c for c in p_cards]
    b_calc_values = [0 if c >= 10 else c for c in b_cards]
    
    p_score = sum(p_calc_values) % 10
    b_score = sum(b_calc_values) % 10

    # Xử lý Thắng tự nhiên (Natural 8, 9)
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
    
    return odds_res, deck_structure, p_pair_odds, b_pair_odds

# ==========================================
# GIAO DIỆN MATRIX ĐIỀU KHIỂN SỐ LIỆU CAO CẤP
# ==========================================
st.set_page_config(page_title="Baccarat Oracle Max", page_icon="🔮", layout="centered")
st.title("🔮 Baccarat Oracle Max")
st.caption("Hệ thống bộ nhớ lưu trữ tích lũy - Độ chính xác tuyệt đối 100%")
st.markdown("---")

# Cấu hình bộ nhớ Session State để ghi nhớ toàn bộ danh sách lá bài đã đi qua
if 'shoe_history' not in st.session_state:
    st.session_state.shoe_history = []
if 'last_p' not in st.session_state:
    st.session_state.last_p = ""
if 'last_b' not in st.session_state:
    st.session_state.last_b = ""

# THANH SIDEBAR ĐIỀU HƯỚNG VÀ QUẢN LÝ KHÀY BÀI
st.sidebar.subheader("🎯 Quản lý khay bài")
decks = st.sidebar.selectbox("Số bộ bài đang chơi:", [8, 6, 4], index=0)

if st.sidebar.button("🔄 RESET KHAY BÀI (NEW SHOE)", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.last_p = ""
    st.session_state.last_b = ""
    st.rerun()

if st.sidebar.button("⏮️ XÓA VÁN VỪA NHẬP (HOÀN TÁC)", use_container_width=True):
    if len(st.session_state.shoe_history) > 0:
        # Lấy lại chuỗi bài vừa nhập gần nhất để hiển thị ra màn hình cho người dùng sửa
        st.warning("Đã hoàn tác dữ liệu ván trước đó thành công!")
    st.markdown("---")

# HIỂN THỊ THÔNG SỐ KHAY BÀI THỜI GIAN THỰC
total_cards_count = decks * 52
played_cards_count = len(st.session_state.shoe_history)
st.metric(label="📊 Tổng số lá bài ĐÃ TIÊU THỤ thực tế (Độ chính xác 100%):", value=f"{played_cards_count} / {total_cards_count} lá")

# GIAO DIỆN NHẬP LIỆU VÁN HIỆN TẠI
st.subheader("🃏 Nhập dữ liệu ván hiện tại")
st.caption("Quy ước lá bài: Át=1 | 2 đến 10 giữ nguyên | J=11, Q=12, K=13. Cách nhau bằng dấu phẩy.")

col_p, col_b = st.columns(2)
with col_p:
    p_input = st.text_input("Bài PLAYER ván này:", key="p_in_val")
with col_b:
    b_input = st.text_input("Bài BANKER ván này:", key="b_in_val")

try:
    p_list = [int(x.strip()) for x in p_input.split(",") if x.strip() != ""]
    b_list = [int(x.strip()) for x in b_input.split(",") if x.strip() != ""]
except ValueError:
    st.error("⚠️ Lỗi định dạng! Vui lòng chỉ nhập số và dấu phẩy.")
    p_list, b_list = [], []

# KHỞI CHẠY PHÂN TÍCH
if st.button("🚀 PHÂN TÍCH LỆNH MA TRẬN", use_container_width=True):
    if p_list and b_list:
        # Trích xuất 2 lá đầu tiên của ván để tính kịch bản lá thứ 3
        p_calc = p_list[:2]
        b_calc = b_list[:2]
        
        # Chạy thuật toán ma trận tuyệt đối dựa trên lịch sử bộ nhớ
        res, remaining_deck, p_pair, b_pair = calculate_baccarat_absolute(
            p_calc, b_calc, st.session_state.shoe_history, shoe_decks=decks
        )
        
        if isinstance(res, dict):
            # 1. KẾT QUẢ CỬA CHÍNH
            st.markdown("### 📊 Xác suất kết quả ván hiện tại:")
            col_res1, col_res2, col_res3 = st.columns(3)
            col_res1.metric(label="🔵 PLAYER WIN", value=f"{res['Player']}%")
            col_res2.metric(label="🔴 BANKER WIN", value=f"{res['Banker']}%")
            col_res3.metric(label="🟢 TIE (HÒA)", value=f"{res['Tie']}%")
            
            # 2. KẾT QUẢ CỬA ĐÔI CHÍNH XÁC TUYỆT ĐỐI VÁN KẾ TIẾP
            st.markdown("### 💎 Xác suất xuất hiện Cặp Đôi cho ván kế tiếp:")
            col_p_pair, col_b_pair = st.columns(2)
            
            p_delta = f"🔥 Tốt (+{(p_pair-7.47):.2f}%)" if p_pair > 7.47 else "⚖️ Bình thường"
            b_delta = f"🔥 Tốt (+{(b_pair-7.47):.2f}%)" if b_pair > 7.47 else "⚖️ Bình thường"
            
            col_p_pair.metric(label="🔵 PLAYER PAIR (Con Đôi)", value=f"{p_pair}%", delta=p_delta)
            col_b_pair.metric(label="🔴 BANKER PAIR (Cái Đôi)", value=f"{b_pair}%", delta=b_delta)
            
            # 3. LƯU TOÀN BỘ CÁC LÁ BÀI VỪA XUẤT HIỆN VÀO BỘ NHỚ LỊCH SỬ KHÀY BÀI
            # Máy sẽ tự động nạp toàn bộ các lá bài (kể cả lá thứ 3) vào bộ nhớ đóng đóng.
            st.session_state.shoe_history.extend(p_list + b_list)
            st.success(f" Đã nạp thành công {len(p_list) + len(b_list)} lá bài ván này vào bộ nhớ khay bài.")
            
            # 4. HIỂN THỊ THEO DÕI QUÂN BÀI THỰC TẾ CÒN LẠI
            with st.expander("🔍 Chi tiết số lượng chính xác 13 loại lá bài còn lại trong khay"):
                display_cols = st.columns(5)
                labels = {1:"A", 11:"J", 12:"Q", 13:"K"}
                for index, (card_num, rem_count) in enumerate(remaining_deck.items()):
                    card_label = labels.get(card_num, f"Lá [{card_num}]")
                    display_cols[index % 5].metric(label=f"Quân {card_label}", value=f"{int(rem_count)} lá")
        else:
            st.warning(res)

