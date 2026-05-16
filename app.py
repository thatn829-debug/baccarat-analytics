import streamlit as st

# ==========================================
# THUẬT TOÁN TÍNH TOÁN XÁC SUẤT THEO SỐ VÁN
# ==========================================
def get_exact_odds_with_games(p_cards, b_cards, shoe_matrix, total_games, shoe_decks=8):
    # Khởi tạo cấu trúc 1 bộ bài (0 đại diện cho 10, J, Q, K - chiếm 16 lá)
    deck_structure = {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 0: 16}
    
    # Tổng số bài ban đầu theo số bộ bài cấu hình
    total_shoe = {k: v * shoe_decks for k, v in deck_structure.items()}
    total_initial_cards = shoe_decks * 52
    
    # 1. Trừ chính xác các lá bài đã được ghi nhớ từ lịch sử nhập liệu
    for card_val in shoe_matrix:
        val = 0 if card_val >= 10 else card_val
        if val in total_shoe and total_shoe[val] > 0:
            total_shoe[val] -= 1
            
    cards_logged = len(shoe_matrix)
    
    # 2. THUẬT TOÁN BÙ TRỪ SAI SỐ PHI TUYẾN TÍNH (Dựa trên Số Ván thực tế)
    # Trung bình một ván Baccarat tiêu thụ khoảng 4.95 lá bài.
    # Nếu Số Ván thực tế lớn hơn lượng bài đã nhập, hệ thống sẽ tự động khấu trừ "Lá bài ẩn" (Bài đốt / Ván bỏ qua)
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
        return f"Hộp bài đã hết sau {total_games} ván!", total_shoe

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
st.set_page_config(page_title="Baccarat Game Matrix Pro", page_icon="🔢", layout="centered")
st.title("🔢 Baccarat Game Matrix Pro")
st.caption("Hệ thống quản lý tích lũy theo số ván - Đồng bộ toán học thực tế")
st.markdown("---")

# Lưu trữ trạng thái bộ đếm và lịch sử bằng Session State
if 'shoe_history' not in st.session_state:
    st.session_state.shoe_history = []
if 'game_counter' not in st.session_state:
    st.session_state.game_counter = 0

# --- CẤU HÌNH SIDEBAR ĐIỀU KHIỂN CHỈ SỐ ---
st.sidebar.header("⚙️ Cấu hình hộp bài")
decks = st.sidebar.selectbox("Số bộ bài trong khay (Shoe):", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.subheader("🔢 Bộ điều khiển ván")

# Ô nhập số ván thông minh, có thể tự chỉnh tay theo bảng điện tử của sòng bài
st.session_state.game_counter = st.sidebar.number_input(
    "VÁN SỐ (Game Number trên bảng đèn):", 
    min_value=0, max_value=120, value=st.session_state.game_counter
)

if st.sidebar.button("🔄 ĐỔI HỘP BÀI MỚI (RESET)", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.game_counter = 0
    st.rerun()

if st.sidebar.button("⏮️ HOÀN TÁC VÁN VỪA RỒI", use_container_width=True):
    if len(st.session_state.shoe_history) > 0 and st.session_state.game_counter > 0:
        # Giảm số ván và ước tính xóa bớt số bài ván cuối (trung bình 4 đến 6 lá)
        st.session_state.game_counter = max(0, st.session_state.game_counter - 1)
        st.session_state.shoe_history = st.session_state.shoe_history[:-5]
        st.sidebar.success("Đã hoàn tác dữ liệu ván trước!")
        st.rerun()

# --- KHỐI THÔNG SỐ GIAO DIỆN CHÍNH ---
c_metric1, c_metric2 = st.columns(2)
with c_metric1:
    st.metric(label="🚩 VÁN HIỆN TẠI (Round):", value=f"Ván thứ {st.session_state.game_counter}")
with c_metric2:
    total_cards = decks * 52
    # Ước tính số bài dựa trên số ván
    est_played = min(total_cards, int(st.session_state.game_counter * 4.95))
    st.metric(label="📊 Ước tính số lá bài đã tiêu thụ:", value=f"{est_played} / {total_cards} lá")

st.markdown("---")

# KHỐI NHẬP LIỆU DỮ LIỆU BÀI HIỆN TẠI
st.subheader("🃏 Nhập dữ liệu ván này")
st.caption("Quy ước: Át=1 | Các lá 2-10 giữ nguyên | J=11, Q=12, K=13. Cách nhau dấu phẩy.")

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
    st.error("⚠️ Vui lòng chỉ nhập số (0-13) và phân tách bằng dấu phẩy!")
    p_list, b_list = [], []

# NÚT PHÂN TÍCH TOÁN HỌC
if st.button("🚀 PHÂN TÍCH XÁC SUẤT MA TRẬN", use_container_width=True):
    if p_list and b_list:
        # Lấy 2 lá đầu tiên để phân tích kịch bản tương lai sắp diễn ra cho lá thứ 3
        p_calc = p_list[:2]
        b_calc = b_list[:2]
        
        # Truyền thêm tham số st.session_state.game_counter vào thuật toán
        res, remaining_deck = get_exact_odds_with_games(
            p_calc, b_calc, st.session_state.shoe_history, st.session_state.game_counter, shoe_decks=decks
        )
        
        if isinstance(res, dict):
            st.markdown("### 📊 Tỷ lệ lệnh ván kế tiếp:")
            
            # Thanh hiển thị thông minh
            st.write(f"🔵 **PLAYER WIN**: {res['Player']}%")
            st.progress(res['Player']/100)
            
            st.write(f"🔴 **BANKER WIN**: {res['Banker']}%")
            st.progress(res['Banker']/100)
            
            # Làm mượt kết quả Tie tránh lỗi hiển thị khi xác suất dồn về một phía
            st.write(f"🟢 **TIE (HÒA)**: {res['Tie']}%")
            st.progress(res['Tie']/100)
            
            # CẬP NHẬT TRẠNG THÁI TỰ ĐỘNG
            st.session_state.shoe_history.extend(p_list + b_list)
            st.session_state.game_counter += 1
            
            st.success(f" Ghi nhận xong ván {st.session_state.game_counter - 1}. Hệ thống tự động chuyển sang ván {st.session_state.game_counter}.")
            
            # HIỂN THỊ ĐỘ BIẾN THIÊN BÀI CÒN LẠI (Radar hiển thị số lá còn trong khay)
            with st.expander("🔍 Xem chi tiết số lượng các lá bài còn lại trong khay"):
                st.write("Dữ liệu phân phối ma trận bài nền (đã đồng bộ bù trừ số ván):")
                display_cols = st.columns(5)
                for index, (card_num, rem_count) in enumerate(remaining_deck.items()):
                    card_label = "10,J,Q,K" if card_num == 0 else f"Lá [{card_num}]"
                    display_cols[index % 5].metric(label=card_label, value=f"{int(rem_count)} lá")
        else:
            st.warning(res)

