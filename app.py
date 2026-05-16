import streamlit as st

# =========================================================================
# ENGINE TOÁN HỌC - MAXIMUM ORACLE PRECISION MATRIX
# =========================================================================
def calculate_baccarat_maximum_oracle(p_cards, b_cards, shoe_matrix, total_games, shoe_decks=8):
    deck_structure = {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 0: 16}
    total_shoe = {k: v * shoe_decks for k, v in deck_structure.items()}
    
    for card_val in shoe_matrix:
        val = 0 if card_val >= 10 else card_val
        if val in total_shoe and total_shoe[val] > 0:
            total_shoe[val] -= 1
            
    cards_logged = len(shoe_matrix)
    estimated_cards_played = int(total_games * 4.95)
    hidden_cards_count = max(0, estimated_cards_played - cards_logged)
    
    if hidden_cards_count > 0:
        current_rem = sum(total_shoe.values())
        if current_rem > 0:
            for k in total_shoe.keys():
                weight = total_shoe[k] / current_rem
                total_shoe[k] = max(0.0, total_shoe[k] - (hidden_cards_count * weight))

    remaining_total = sum(total_shoe.values())
    if remaining_total <= 6:
        return "Hộp bài đã hết ván an toàn!", {}, 0.0, 0.0

    # Tính Đôi (Pair)
    N = remaining_total
    derived_13_decks = {k: total_shoe[k] for k in range(1, 10)}
    for k in [10, 11, 12, 13]:
        derived_13_decks[k] = total_shoe[0] / 4.0

    p_pair_odds = round((sum([(count / N) * ((count - 1) / (N - 1)) for count in derived_13_decks.values() if count >= 2]) * 100) if N > 1 else 0.0, 2)
    
    b_pair_prob = 0.0
    if N > 3:
        for b_count in derived_13_decks.values():
            if b_count >= 2:
                p_rem_0 = ((N - b_count) / N) * ((N - b_count - 1) / (N - 1))
                p_rem_1 = 2 * (b_count / N) * ((N - b_count) / (N - 1))
                p_rem_2 = (b_count / N) * ((b_count - 1) / (N - 1))
                b_pair_prob += (p_rem_0 * (b_count / (N - 2)) * ((b_count - 1) / (N - 3)) +
                                p_rem_1 * (max(0.0, b_count - 1) / (N - 2)) * (max(0.0, b_count - 2) / (N - 3)) +
                                p_rem_2 * (max(0.0, b_count - 2) / (N - 2)) * (max(0.0, b_count - 3) / (N - 3)))
    b_pair_odds = round(b_pair_prob * 100, 2)

    # Khấu trừ ván hiện tại để tính lá thứ 3
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if total_shoe[val] > 0:
            total_shoe[val] -= 1
            remaining_total -= 1

    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, total_shoe, p_pair_odds, b_pair_odds
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, total_shoe, p_pair_odds, b_pair_odds
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, total_shoe, p_pair_odds, b_pair_odds

    current_sum = sum(total_shoe.values())
    if current_sum == 0: return "Lỗi ma trận!", total_shoe, p_pair_odds, b_pair_odds
        
    prob_dict = {k: v / current_sum for k, v in total_shoe.items()}
    player_wins, banker_wins, ties = 0.0, 0.0, 0.0

    if not (p_score <= 5):
        if b_score <= 5:
            for card3_b, p_b in prob_dict.items():
                final_b = (b_score + card3_b) % 10
                if p_score > final_b: player_wins += p_b
                elif final_b > p_score: banker_wins += p_b
                else: ties += p_b
        else:
            if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, total_shoe, p_pair_odds, b_pair_odds
            elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, total_shoe, p_pair_odds, b_pair_odds
            else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, total_shoe, p_pair_odds, b_pair_odds
    else:
        for card3_p, p_p in prob_dict.items():
            final_p = (p_score + card3_p) % 10
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
    return {"Player": round((player_wins / total_prob) * 100, 2), "Banker": round((banker_wins / total_prob) * 100, 2), "Tie": round((ties / total_prob) * 100, 2)}, total_shoe, p_pair_odds, b_pair_odds

# =========================================================================
# GIAO DIỆN SIÊU TINH GỌN (COMPACT UI/UX)
# =========================================================================
st.set_page_config(page_title="Oracle Max v4", page_icon="🔮", layout="centered")

# Khởi tạo bộ nhớ tạm
if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'game_counter' not in st.session_state: st.session_state.game_counter = 0
if 'last_results' not in st.session_state: st.session_state.last_results = None

# --- SIDEBAR: CẤU HÌNH VÀ BỘ ĐIỀU KHIỂN ĐẨY SANG TRÁI ---
st.sidebar.header("⚙️ Cấu Hình")
decks = st.sidebar.selectbox("Số bộ bài:", [8, 6, 4], index=0)
st.sidebar.markdown("---")
st.session_state.game_counter = st.sidebar.number_input("Game Number (Số ván sòng bài):", min_value=0, max_value=150, value=st.session_state.game_counter)

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

# --- MÀN HÌNH CHÍNH ---
# 1. PHẦN KẾT QUẢ ĐẨY LÊN TRÊN CÙNG
if st.session_state.last_results:
    res, p_pair, b_pair, remaining_deck = st.session_state.last_results
    
    # Thanh hiển thị tỷ lệ nhanh
    c_p, c_b, c_t = st.columns(3)
    c_p.metric("🔵 PLAYER", f"{res['Player']}%")
    c_b.metric("🔴 BANKER", f"{res['Banker']}%")
    c_t.metric("🟢 TIE", f"{res['Tie']}%")
    
    # Progress bar trực quan
    st.progress(res['Banker'] / 100 if res['Banker'] > 0 else 0)
    
    # Tỷ lệ Đôi
    cp_p, cp_b = st.columns(2)
    cp_p.caption(f"Cặp Player: **{p_pair}%** " + ("🔥" if p_pair > 7.47 else ""))
    cp_b.caption(f"Cặp Banker: **{b_pair}%** " + ("🔥" if b_pair > 7.47 else ""))
    
    # Info phụ dạng ẩn gọn
    with st.expander("📊 Chi tiết khay bài"):
        st.write(f"Ván hiện tại: **{st.session_state.game_counter}** | Đã quét: {len(st.session_state.shoe_history)} lá.")
        cols = st.columns(5)
        for idx, (num, cnt) in enumerate(remaining_deck.items()):
            label = "10,J,Q,K" if num == 0 else f"[{num}]"
            cols[idx % 5].text(f"{label}: {int(cnt)} lá")
else:
    st.info("🔮 Nhập điểm phía dưới và bấm quét để nhận tỷ lệ xác suất ván kế tiếp.")

st.markdown("---")

# 2. PHẦN NHẬP ĐIỂM ĐẨY XUỐNG DƯỚI (Vừa tay bấm điện thoại)
st.subheader("🃏 Nhập bài ván này")
col_p, col_b = st.columns(2)
with col_p:
    p_input = st.text_input("PLAYER:", value="0", placeholder="Ví dụ: 5,1 hoặc 9,0,2")
with col_b:
    b_input = st.text_input("BANKER:", value="0", placeholder="Ví dụ: 4,11")

try:
    p_list = [int(x.strip()) for x in p_input.split(",") if x.strip() != ""]
    b_list = [int(x.strip()) for x in b_input.split(",") if x.strip() != ""]
except ValueError:
    st.error("Chỉ nhập số (0-13) cách nhau dấu phẩy!")
    p_list, b_list = [], []

# NÚT XỬ LÝ LỚN ĐẬM
if st.button("🚀 PHÂN TÍCH MA TRẬN", use_container_width=True, type="primary"):
    if p_list and b_list:
        p_calc = p_list[:2]
        b_calc = b_list[:2]
        
        res, remaining_deck, p_pair, b_pair = calculate_baccarat_maximum_oracle(
            p_calc, b_calc, st.session_state.shoe_history, st.session_state.game_counter, shoe_decks=decks
        )
        
        if isinstance(res, dict):
            # Lưu lại kết quả để hiển thị lên trên cùng
            st.session_state.last_results = (res, p_pair, b_pair, remaining_deck)
            # Lưu lịch sử và nhảy ván tự động
            st.session_state.shoe_history.extend(p_list + b_list)
            st.session_state.game_counter += 1
            st.rerun()
        else:
            st.warning(res)
