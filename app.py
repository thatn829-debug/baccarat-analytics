import streamlit as st

def calculate_baccarat_odds(player_cards, banker_cards, cards_played, shoe_decks=8):
    deck_structure = {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 0: 16}
    total_shoe = {k: v * shoe_decks for k, v in deck_structure.items()}
    used_cards_count = cards_played + len(player_cards) + len(banker_cards)
    remaining_cards_total = (shoe_decks * 52) - used_cards_count
    
    if remaining_cards_total <= 6:
        return "Hộp bài đã hết bài!"

    for card in player_cards + banker_cards:
        val = 0 if card >= 10 else card
        if total_shoe[val] > 0:
            total_shoe[val] -= 1

    p_score = sum([0 if c >= 10 else c for c in player_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in banker_cards]) % 10

    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}

    pool = []
    for card_val, count in total_shoe.items():
        pool.extend([card_val] * int(count * (remaining_cards_total / sum(total_shoe.values()))))

    total_cases = 0
    player_wins = 0
    banker_wins = 0
    ties = 0
    p_draws = p_score <= 5

    if not p_draws:
        if b_score <= 5:
            for card3_b in set(pool):
                prob_b = pool.count(card3_b) / len(pool)
                final_b = (b_score + card3_b) % 10
                total_cases += prob_b
                if p_score > final_b: player_wins += prob_b
                elif final_b > p_score: banker_wins += prob_b
                else: ties += prob_b
        else:
            if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}
            elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}
            else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}
    else:
        for card3_p in set(pool):
            prob_p = pool.count(card3_p) / len(pool)
            final_p = (p_score + card3_p) % 10
            b_draws = False
            if b_score <= 2: b_draws = True
            elif b_score == 3 and card3_p != 8: b_draws = True
            elif b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]: b_draws = True
            elif b_score == 5 and card3_p in [4, 5, 6, 7]: b_draws = True
            elif b_score == 6 and card3_p in [6, 7]: b_draws = True
            
            if b_draws:
                for card3_b in set(pool):
                    prob_b = pool.count(card3_b) / len(pool)
                    final_b = (b_score + card3_b) % 10
                    weight = prob_p * prob_b
                    total_cases += weight
                    if final_p > final_b: player_wins += weight
                    elif final_b > final_p: banker_wins += weight
                    else: ties += weight
            else:
                weight = prob_p
                total_cases += weight
                if final_p > b_score: player_wins += weight
                elif b_score > final_p: banker_wins += weight
                else: ties += weight

    return {
        "Player": round((player_wins / total_cases) * 100, 2) if total_cases > 0 else 0,
        "Banker": round((banker_wins / total_cases) * 100, 2) if total_cases > 0 else 0,
        "Tie": round((ties / total_cases) * 100, 2) if total_cases > 0 else 0
    }

# --- GIAO DIỆN STREAMLIT CHO THIẾT BỊ DI ĐỘNG ---
st.set_page_config(page_title="Baccarat Analytics", page_icon="📊", layout="centered")
st.title("📊 Baccarat Odds Pro")

# Khởi tạo bộ nhớ đếm bài nếu chưa có
if 'cards' not in st.session_state:
    st.session_state.cards = 0

# Khối 1: Quản lý số bài đã rút
st.subheader("1. Bộ đếm bài trong hộp (Shoe)")
st.session_state.cards = st.number_input(
    "Tổng số lá bài đã rút từ đầu hộp bài:", 
    min_value=0, max_value=416, value=st.session_state.cards
)

# Khối 2: Nhập bài hiện tại
st.subheader("2. Nhập bài ván này")
st.caption("Quy ước: Điền số từ 1-9. Các lá 10, J, Q, K thì nhập số 0. Mỗi lá cách nhau bằng dấu phẩy.")
col1, col2 = st.columns(2)
with col1:
    p_in = st.text_input("Bài Player (Ví dụ: 5,0):", "0")
with col2:
    b_in = st.text_input("Bài Banker (Ví dụ: 4,3):", "0")

# Chuyển đổi dữ liệu chuỗi thành mảng số
try:
    p_list = [int(x.strip()) for x in p_in.split(",") if x.strip() != ""]
    b_list = [int(x.strip()) for x in b_in.split(",") if x.strip() != ""]
except ValueError:
    st.error("Lỗi cấu trúc: Vui lòng chỉ nhập số và dấu phẩy!")
    p_list, b_list = [], []

# Nút xử lý tính toán
if st.button("📊 TÍNH XÁC SUẤT", use_container_width=True):
    if p_list and b_list:
        res = calculate_baccarat_odds(p_list, b_list, st.session_state.cards)
        
        if isinstance(res, dict):
            st.markdown("### 📈 Xác suất chiến thắng:")
            
            # Hiển thị thanh tiến trình trực quan
            st.write(f"🔵 **PLAYER WIN**: {res['Player']}%")
            st.progress(res['Player']/100)
            
            st.write(f"🔴 **BANKER WIN**: {res['Banker']}%")
            st.progress(res['Banker']/100)
            
            st.write(f"🟢 **TIE (HÒA)**: {res['Tie']}%")
            st.progress(res['Tie']/100)
            
            # Tự động cộng dồn số bài lật trên bàn vào bộ đếm hệ thống
            st.session_state.cards += (len(p_list) + len(b_list))
            st.info(f"Hệ thống đã tự động cộng dồn bài. Ván sau sẽ tính từ lá thứ: **{st.session_state.cards}**")
        else:
            st.warning(res)
