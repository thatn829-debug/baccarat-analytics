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

# --- GIAO DIỆN STREAMLIT CẢI TIẾN ---
st.set_page_config(page_title="Baccarat Analytics", page_icon="📊", layout="centered")
st.title("📊 Baccarat Odds Pro")

# Khởi tạo bộ đếm bài
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
st.caption("Quy ước: Điền các lá bài đã lật (gồm cả lá thứ 3 nếu có), cách nhau bằng dấu phẩy. Ví dụ: 5,0 hoặc 5,0,2. (10, J, Q, K nhập số 0)")

col1, col2 = st.columns(2)
with col1:
    p_in = st.text_input("Bài Player hiện tại:", "0")
with col2:
    b_in = st.text_input("Bài Banker hiện tại:", "0")

# Chuyển dữ liệu chuỗi nhập vào thành danh sách số
try:
    p_list = [int(x.strip()) for x in p_in.split(",") if x.strip() != ""]
    b_list = [int(x.strip()) for x in b_in.split(",") if x.strip() != ""]
except ValueError:
    st.error("Lỗi: Vui lòng chỉ nhập số và dấu phẩy!")
    p_list, b_list = [], []

# Nút tính toán
if st.button("📊 TÍNH XÁC SUẤT", use_container_width=True):
    if p_list and b_list:
        # Sử dụng 2 lá bài đầu tiên của mỗi bên để tính toán xác suất cho lá thứ 3 sắp ra
        p_calc = p_list[:2]
        b_calc = b_list[:2]
        
        res = calculate_baccarat_odds(p_calc, b_calc, st.session_state.cards)
        
        if isinstance(res, dict):
            st.markdown("### 📈 Xác suất chiến thắng:")
            
            st.write(f"🔵 **PLAYER WIN**: {res['Player']}%")
            st.progress(res['Player']/100)
            
            st.write(f"🔴 **BANKER WIN**: {res['Banker']}%")
            st.progress(res['Banker']/100)
            
            st.write(f"🟢 **TIE (HÒA)**: {res['Tie']}%")
            st.progress(res['Tie']/100)
            
            # --- TỰ ĐỘNG ĐẾM CHÍNH XÁC SỐ LÁ ĐÃ NHẬP ---
            # Đếm tổng số lượng phần tử thực tế bạn đã gõ vào (bao gồm cả lá thứ 3)
            actual_cards_played = len(p_list) + len(b_list)
            
            # Cộng dồn số lá thực tế này vào bộ đếm của hệ thống
            st.session_state.cards += actual_cards_played
            
            st.success(f" Ghi nhận ván này tiêu thụ: **{actual_cards_played} lá bài**.")
            st.info(f"Hộp bài ván sau sẽ tự động tính từ lá thứ: **{st.session_state.cards}**")
        else:
            st.warning(res)
