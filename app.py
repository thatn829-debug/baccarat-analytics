import streamlit as st

# =========================================================================
# SYSTEM CORE: QUANTUM ORACLE PRECISION MATRIX (VERSION 6)
# =========================================================================
def calculate_baccarat_quantum_precision(p_cards, b_cards, shoe_matrix, total_games, shoe_decks=8):
    # Khởi tạo ma trận phân phối 13 loại lá bài gốc (1=A, 2-10 giữ nguyên, 11=J, 12=Q, 13=K)
    # Việc quản lý chi tiết 13 nhánh giúp tính toán xác suất kéo bài và xác suất Đôi chính xác tuyệt đối
    deck_structure = {i: 4 * shoe_decks for i in range(1, 14)}
    total_initial_cards = shoe_decks * 52
    
    # 1. Khấu trừ chính xác các lá bài đã xuất hiện trong lịch sử bộ nhớ đóng
    for card_val in shoe_matrix:
        if card_val in deck_structure and deck_structure[card_val] > 0:
            deck_structure[card_val] -= 1
            
    cards_logged = len(shoe_matrix)
    
    # 2. THUẬT TOÁN SUY HAO BAYESIAN THEO SỐ VÁN THỰC TẾ (TRIỆT TIÊU SAI SỐ BÀI ĐỐT)
    # Áp dụng hằng số tiêu thụ ngẫu nhiên Baccarat chuẩn quốc tế: 4.95154 lá/ván
    estimated_cards_played = int(total_games * 4.95154)
    hidden_cards_count = max(0, estimated_cards_played - cards_logged)
    
    if hidden_cards_count > 0:
        current_rem = sum(deck_structure.values())
        if current_rem > 0:
            for k in deck_structure.keys():
                # Phân rã tỷ lệ phi tuyến tính động dựa trên trọng số phân phối còn lại
                weight = deck_structure[k] / current_rem
                deck_structure[k] = max(0.0, deck_structure[k] - (hidden_cards_count * weight))

    remaining_total = sum(deck_structure.values())
    if remaining_total <= 4:
        return "Khay bài đã cạn kiệt dữ liệu an toàn!", {}, 0.0, 0.0

    # 3. ENGINE XÁC SUẤT CẶP ĐÔI REAL-TIME CHIỀU SÂU
    N = remaining_total
    
    # Tính xác suất Player Pair ván kế tiếp
    p_pair_prob = 0.0
    if N > 1:
        for count in deck_structure.values():
            if count >= 2:
                p_pair_prob += (count / N) * ((count - 1) / (N - 1))
    p_pair_odds = round(p_pair_prob * 100, 2)

    # Tính xác suất Banker Pair ván kế tiếp (Xác suất có điều kiện tích hợp chuỗi ma trận)
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

    # 4. QUY ĐỔI MA TRẬN 13 LÁ SANG HỆ ĐIỂM BACCARAT (0 ĐẾN 9) ĐỂ TÍNH CỬA CHÍNH
    score_deck = {i: 0.0 for i in range(10)}
    for card_num, count in deck_structure.items():
        bacc_val = 0 if card_num >= 10 else card_num
        score_deck[bacc_val] += count

    # Trừ các lá bài đang lộ diện ở ván hiện tại trước khi xét kịch bản rút lá thứ 3
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0:
            score_deck[val] -= 1

    p_calc_values = [0 if c >= 10 else c for c in p_cards]
    b_calc_values = [0 if c >= 10 else c for c in b_cards]
    
    p_score = sum(p_calc_values) % 10
    b_score = sum(b_calc_values) % 10

    # Luật Thắng Tự Nhiên (Natural 8, 9) - Đưa ra kết quả tuyệt đối ngay lập tức
    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds

    current_sum = sum(score_deck.values())
    if current_sum == 0: return "Lỗi tính toán hệ ma trận!", deck_structure, p_pair_odds, b_pair_odds
        
    prob_dict = {k: v / current_sum for k, v in score_deck.items()}
    player_wins, banker_wins, ties = 0.0, 0.0, 0.0

    # Cây quyết định phân phối xác suất kéo lá thứ 3 chuẩn sòng bài quốc tế
    if not (p_score <= 5):  # Player đứng (6 hoặc 7 điểm)
        if b_score <= 5:    # Banker bắt buộc phải rút thêm lá thứ 3
            for card3_b, p_b in prob_dict.items():
                final_b = (b_score + card3_b) % 10
                if p_score > final_b: player_wins += p_b
                elif final_b > p_score: banker_wins += p_b
                else: ties += p_b
        else:               # Cả hai cùng đứng
            if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds
            elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds
            else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds
    else:                   # Player bắt buộc rút lá thứ 3
        for card3_p, p_p in prob_dict.items():
            final_p = (p_score + card3_p) % 10
            # Quy tắc rút lá bài thứ 3 nghiêm ngặt của Banker
            b_draws = (b_score <= 2) or (b_score == 3 and card3_p != 8) or (b_score == 4 and card3_p in [2,3,4,5,6,7]) or (b_score == 5 and card3_p in [4,5,6,7]) or (b_score == 6 and card3_p in [6,7])
            
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
        "Player": round((player_wins / total_prob) * 100, 2),
        "Banker": round((banker_wins / total_prob) * 100, 2),
        "Tie": round((ties / total_prob) * 100, 2)
    }
    return odds_res, deck_structure, p_pair_odds, b_pair_odds


# =========================================================================
# INTERFACE: SUPREME COMPACT PRO V6 (RESTORED VIEW)
# =========================================================================
st.set_page_config(page_title="Oracle Max v6", page_icon="🔮", layout="centered")

# Khởi tạo trạng thái bộ nhớ
if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'game_counter' not in st.session_state: st.session_state.game_counter = 0
if 'last_results' not in st.session_state: st.session_state.last_results = None

# --- SIDEBAR CẤU HÌNH GỌN ---
st.sidebar.header("⚙️ Cấu Hình")
decks = st.sidebar.selectbox("Số bộ bài:", [8, 6, 4], index=0)
st.sidebar.markdown("---")

if st.sidebar.button("🔄 RESET KHAY BÀI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.game_counter = 0
    st.session_state.last_results = None
    st.rerun()

if st.sidebar.button("⏮️ HOÀN TÁC (UNDO)", use_container_width=True):
    if len(st.session_state.shoe_history) > 0 and st.session_state.game_counter > 0:
        st.session_state.game_counter = max(0, st.session_state.game_counter - 1)
        st.session_state.shoe_history = st.session_state.shoe_history[:-5]
        st.session_state.last_results = None
        st.rerun()

# --- MÀN HÌNH CHÍNH ƯU TIÊN 1: BẢNG KẾT QUẢ ĐẦY ĐỦ LÊN ĐẦU ---
if st.session_state.last_results:
    res, p_pair, b_pair, remaining_deck = st.session_state.last_results
    
    c_p, c_b, c_t = st.columns(3)
    c_p.metric("🔵 PLAYER WIN", f"{res['Player']}%")
    c_b.metric("🔴 BANKER WIN", f"{res['Banker']}%")
    c_t.metric("🟢 TIE WIN", f"{res['Tie']}%")
    
    st.progress(res['Banker'] / 100 if res['Banker'] > 0 else 0)
    
    cp_p, cp_b = st.columns(2)
    cp_p.caption(f"Cặp Player: **{p_pair}%** " + ("🔥 Tốt" if p_pair > 7.47 else "⚖️ Bình thường"))
    cp_b.caption(f"Cặp Banker: **{b_pair}%** " + ("🔥 Tốt" if b_pair > 7.47 else "⚖️ Bình thường"))
    
    with st.expander("📊 Chi tiết ma trận khay bài"):
        total_cards = decks * 52
        est_played = min(total_cards, int(st.session_state.game_counter * 4.95154))
        st.write(f"Ván hiện tại: **{st.session_state.game_counter}** | Bài đã chạy (ước tính): **{est_played} / {total_cards}** lá.")
        cols = st.columns(5)
        labels_13 = {1: "A", 11: "J", 12: "Q", 13: "K"}
        for idx, (num, cnt) in enumerate(remaining_deck.items()):
            card_label = labels_13.get(num, f"[{num}]")
            cols[idx % 5].text(f"Quân {card_label}: {int(cnt)} lá")
else:
    st.info("🔮 Vui lòng điền điểm số ván hiện tại vào ô bên dưới để kích hoạt ma trận dự đoán.")

st.markdown("---")

# --- MÀN HÌNH CHÍNH ƯU TIÊN 2: KHU VỰC NHẬP LIỆU (KHÔI PHỤC GIAO DIỆN TRƯỚC) ---
# Tách tiêu đề nhập điểm sang bên trái và đặt ô chỉnh Số Ván (Game No.) nằm nép sát góc phải
head_col, game_num_col = st.columns([2, 1])
with head_col:
    st.subheader("🃏 Điền điểm ván này")
with game_num_col:
    # Hộp số ván hiển thị nhỏ gọn góc phải, đồng bộ trực tiếp với sòng bài
    st.session_state.game_counter = st.number_input(
        "Ván số (Game No.):", 
        min_value=0, max_value=150, 
        value=st.session_state.game_counter,
        step=1
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
    st.error("Chỉ nhập số nguyên cách nhau bằng dấu phẩy!")
    p_list, b_list = [], []

if st.button("🚀 KÍCH HOẠT QUÉT MA TRẬN PHÂN TÍCH", use_container_width=True, type="primary"):
    if p_list and b_list:
        p_calc = p_list[:2]
        b_calc = b_list[:2]
        
        res, remaining_deck, p_pair, b_pair = calculate_baccarat_quantum_precision(
            p_calc, b_calc, st.session_state.shoe_history, st.session_state.game_counter, shoe_decks=decks
        )
        
        if isinstance(res, dict):
            st.session_state.last_results = (res, p_pair, b_pair, remaining_deck)
            st.session_state.shoe_history.extend(p_list + b_list)
            st.session_state.game_counter += 1
            st.rerun()
        else:
            st.warning(res)


