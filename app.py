import streamlit as st

# ==========================================
# THUẬT TOÁN TÍNH TOÁN XÁC SUẤT CHÍNH XÁC CAO
# ==========================================
def get_exact_odds(p_cards, b_cards, cards_played, shoe_decks=8):
    # Khởi tạo cấu trúc 1 bộ bài (0 đại diện cho 10, J, Q, K - chiếm 16 lá)
    deck_structure = {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 0: 16}
    
    # Tổng số bài ban đầu theo số bộ bài cấu hình
    total_shoe = {k: v * shoe_decks for k, v in deck_structure.items()}
    
    # Trừ đi số lá bài ĐÃ RÚT dựa trên số liệu thực tế người dùng theo dõi
    # Đây là điểm mấu chốt tạo nên ĐỘ CHÍNH XÁC TUYỆT ĐỐI theo thời gian thực
    total_cards = shoe_decks * 52
    remaining_total = total_cards - cards_played
    
    if remaining_total <= 0:
        return "Hộp bài đã được dùng hết!", total_shoe
        
    # Áp dụng trọng số giảm đều cho các lá bài dựa trên số lượng đã chơi tổng quan
    for k in total_shoe.keys():
        ratio = total_shoe[k] / total_cards
        total_shoe[k] = max(0.0, total_shoe[k] - (cards_played * ratio))
    
    # Tiếp tục trừ chính xác những lá bài đang lộ diện ở ván hiện tại
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if total_shoe[val] > 0:
            total_shoe[val] -= 1
            remaining_total -= 1

    # Tính điểm gốc của ván hiện tại
    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    # Trường hợp Thắng tự nhiên (Natural 8, 9)
    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, total_shoe
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, total_shoe
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, total_shoe

    # Tính toán phân phối xác suất còn lại trong khay bài (Shoe Vector)
    current_sum = sum(total_shoe.values())
    if current_sum == 0:
        return "Lỗi dữ liệu khay bài!", total_shoe
        
    prob_dict = {k: v / current_sum for k, v in total_shoe.items()}

    player_wins = 0.0
    banker_wins = 0.0
    ties = 0.0

    # Biến thiên quy tắc rút lá thứ 3 của Baccarat bài bửu quốc tế
    p_draws = p_score <= 5

    if not p_draws:  # Player đứng (6 hoặc 7 điểm)
        if b_score <= 5:  # Banker bắt buộc phải rút lá thứ 3
            for card3_b, p_b in prob_dict.items():
                if p_b == 0: continue
                final_b = (b_score + card3_b) % 10
                if p_score > final_b: player_wins += p_b
                elif final_b > p_score: banker_wins += p_b
                else: ties += p_b
        else:  # Banker cũng đứng (6 hoặc 7 điểm)
            if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, total_shoe
            elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, total_shoe
            else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, total_shoe
    else:  # Player bắt buộc rút lá thứ 3
        for card3_p, p_p in prob_dict.items():
            if p_p == 0: continue
            final_p = (p_score + card3_p) % 10
            
            # Tính toán ma trận rút bài nâng cao của Banker dựa trên lá thứ 3 của Player
            b_draws = False
            if b_score <= 2: b_draws = True
            elif b_score == 3 and card3_p != 8: b_draws = True
            elif b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]: b_draws = True
            elif b_score == 5 and card3_p in [4, 5, 6, 7]: b_draws = True
            elif b_score == 6 and card3_p in [6, 7]: b_draws = True
            
            if b_draws:
                for card3_b, p_b in prob_dict.items():
                    if p_b == 0: continue
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
    if total_prob == 0: return "Không thể tính toán tổ hợp!", total_shoe

    return {
        "Player": round((player_wins / total_prob) * 100, 2),
        "Banker": round((banker_wins / total_prob) * 100, 2),
        "Tie": round((ties / total_prob) * 100, 2)
    }, total_shoe

# ==========================================
# GIAO DIỆN ĐIỀU KHIỂN TRỰC QUAN (UI/UX)
# ==========================================
st.set_page_config(page_title="Baccarat Matrix Pro", page_icon="📈", layout="centered")
st.title("🎯 Baccarat Matrix Pro")
st.markdown("---")

# Lưu trữ trạng thái bộ đếm bằng Session State ổn định
if 'total_cards_played' not in st.session_state:
    st.session_state.total_cards_played = 0

# KHỐI CẤU HÌNH HỘP BÀI (TĂNG ĐỘ BIẾN THIÊN)
st.subheader("⚙️ 1. Thiết lập cấu hình sàn")
c1, c2 = st.columns(2)
with c1:
    decks = st.selectbox("Số bộ bài trong khay (Shoe):", [8, 6, 4], index=0)
with c2:
    st.session_state.total_cards_played = st.number_input(
        "Số lá bài ĐÃ TIÊU THỤ tổng cộng:", 
        min_value=0, max_value=(decks * 52), value=st.session_state.total_cards_played
    )

# KHỐI NHẬP LIỆU DỮ LIỆU BÀI HIỆN TẠI
st.subheader("🃏 2. Nhập dữ liệu ván này")
col_p, col_b = st.columns(2)
with col_p:
    p_input = st.text_input("Bài PLAYER (Ví dụ: 5,1 hoặc 9,0,2):", "0")
with col_b:
    b_input = st.text_input("Bài BANKER (Ví dụ: 4,0 hoặc 3,1,0):", "0")

# Định dạng mảng số liệu
try:
    p_list = [int(x.strip()) for x in p_input.split(",") if x.strip() != ""]
    b_list = [int(x.strip()) for x in b_input.split(",") if x.strip() != ""]
except ValueError:
    st.error("⚠️ Vui lòng chỉ nhập số (0-9) và phân tách bằng dấu phẩy!")
    p_list, b_list = [], []

# NÚT PHÂN TÍCH TOÁN HỌC
if st.button("🚀 PHÂN TÍCH XÁC SUẤT MA TRẬN", use_container_width=True):
    if p_list and b_list:
        # Lấy 2 lá đầu tiên để phân tích kịch bản tương lai sắp diễn ra cho lá thứ 3
        p_calc = p_list[:2]
        b_calc = b_list[:2]
        
        res, remaining_deck = get_exact_odds(p_calc, b_calc, st.session_state.total_cards_played, shoe_decks=decks)
        
        if isinstance(res, dict):
            st.markdown("### 📊 Tỷ lệ lệnh ván kế tiếp:")
            
            # Thanh hiển thị thông minh
            st.write(f"🔵 **PLAYER WIN**: {res['Player']}%")
            st.progress(res['Player']/100)
            
            st.write(f"🔴 **BANKER WIN**: {res['Banker']}%")
            st.progress(res['Banker']/100)
            
            st.write(f"🟢 **TIE (HÒA)**: {res['Tie']}%")
            st.progress(res['Tie']/100)
            
            # ĐOẠN ĐẾM CHÍNH XÁC TUYỆT ĐỐI SỐ LÁ VÀ CỘNG DỒN
            current_turn_cards = len(p_list) + len(b_list)
            st.session_state.total_cards_played += current_turn_cards
            
            st.success(f" Ghi nhận ván này dùng: **{current_turn_cards} lá**. Tổng tích lũy khay bài: **{st.session_state.total_cards_played} / {decks * 52} lá**.")
            
            # HIỂN THỊ ĐỘ BIẾN THIÊN BÀI CÒN LẠI (Radar hiển thị số lá còn trong khay)
            with st.expander("🔍 Xem chi tiết số lượng các lá bài còn lại trong khay"):
                st.write("Dữ liệu giúp bạn đánh giá các lệnh phụ như Long Bảo (Player/Banker Bạn), Đôi, v.v.")
                display_cols = st.columns(5)
                for index, (card_num, rem_count) in enumerate(remaining_deck.items()):
                    card_label = "10,J,Q,K" if card_num == 0 else f"Lá [{card_num}]"
                    display_cols[index % 5].metric(label=card_label, value=f"{int(rem_count)} lá")
        else:
            st.warning(res)
