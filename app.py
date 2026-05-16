import streamlit as st

# =========================================================================
# THUẬT TOÁN MA TRẬN TOÁN HỌC CAO CẤP - MAXIMUM ORACLE PRECISION MATRIX
# =========================================================================
def calculate_baccarat_maximum_oracle(p_cards, b_cards, shoe_matrix, total_games, shoe_decks=8):
    # Cấu trúc ma trận bài gốc: 1-9 giữ nguyên. 0 đại diện cho (10, J, Q, K) có 16 lá/bộ
    deck_structure = {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 0: 16}
    
    # Nhân bản theo cấu hình số bộ bài (Decks) của bàn chơi
    total_shoe = {k: v * shoe_decks for k, v in deck_structure.items()}
    total_initial_cards = shoe_decks * 52
    
    # 1. Khấu trừ chính xác tuyệt đối các lá bài đã lưu trong lịch sử nhập liệu
    for card_val in shoe_matrix:
        val = 0 if card_val >= 10 else card_val
        if val in total_shoe and total_shoe[val] > 0:
            total_shoe[val] -= 1
            
    cards_logged = len(shoe_matrix)
    
    # 2. THUẬT TOÁN BÙ TRỪ SAI SỐ BÀI ẨN PHI TUYẾN TÍNH (BURN-CARDS & MISSING ROUNDS)
    # Trung bình một ván tiêu thụ ~4.95 lá. Số ván thực tế (total_games) quyết định lượng bài đã chạy.
    estimated_cards_played = int(total_games * 4.95)
    hidden_cards_count = max(0, estimated_cards_played - cards_logged)
    
    if hidden_cards_count > 0:
        current_rem = sum(total_shoe.values())
        if current_rem > 0:
            for k in total_shoe.keys():
                weight = total_shoe[k] / current_rem
                total_shoe[k] = max(0.0, total_shoe[k] - (hidden_cards_count * weight))

    remaining_total = sum(total_shoe.values())
    
    # Nếu khay bài còn quá ít, dừng tính toán để bảo toàn vốn
    if remaining_total <= 6:
        return "Hộp bài đã cạn kiệt dữ liệu an toàn!", {}, 0.0, 0.0

    # 3. THUẬT TOÁN TÍNH XÁC SUẤT ĐÔI (PAIR) CHUỖI THỜI GIAN THỰC
    # Phải quy đổi ngược cấu trúc 13 lá từ ma trận 10 nhóm để tính tổ hợp cặp trùng lặp
    N = remaining_total
    
    # Tạo vector giả lập 13 loại lá bài từ hệ phân rã total_shoe để tính Đôi chính xác
    derived_13_decks = {}
    for k in range(1, 10):
        derived_13_decks[k] = total_shoe[k]
    # Nhóm bài số 0 (10, J, Q, K) chia đều làm 4 phần bằng nhau
    for k in [10, 11, 12, 13]:
        derived_13_decks[k] = total_shoe[0] / 4.0

    # Xác suất Player Pair ván tiếp theo
    p_pair_prob = 0.0
    if N > 1:
        for card_type, count in derived_13_decks.items():
            if count >= 2:
                p_pair_prob += (count / N) * ((count - 1) / (N - 1))
    p_pair_odds = round(p_pair_prob * 100, 2)

    # Xác suất Banker Pair ván tiếp theo (Tính toán ma trận có điều kiện chiều sâu)
    b_pair_prob = 0.0
    if N > 3:
        for b_card_type, b_count in derived_13_decks.items():
            if b_count >= 2:
                p_rem_0 = ((N - b_count) / N) * ((N - b_count - 1) / (N - 1))
                b_count_case0 = b_count
                
                p_rem_1 = 2 * (b_count / N) * ((N - b_count) / (N - 1))
                b_count_case1 = b_count - 1
                
                p_rem_2 = (b_count / N) * ((b_count - 1) / (N - 1))
                b_count_case2 = b_count - 2
                
                prob_b_pair = (
                    p_rem_0 * (b_count_case0 / (N - 2)) * ((b_count_case0 - 1) / (N - 3)) +
                    p_rem_1 * (max(0.0, b_count_case1) / (N - 2)) * (max(0.0, b_count_case1 - 1) / (N - 3)) +
                    p_rem_2 * (max(0.0, b_count_case2) / (N - 2)) * (max(0.0, b_count_case2 - 1) / (N - 3))
                )
                b_pair_prob += prob_b_pair
    b_pair_odds = round(b_pair_prob * 100, 2)

    # 4. KHẤU TRỪ TIẾP CÁC LÁ BÀI ĐANG LỘ DIỆN VÁN HIỆN TẠI ĐỂ XÉT LÁ THỨ 3
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if total_shoe[val] > 0:
            total_shoe[val] -= 1
            remaining_total -= 1

    p_calc_values = [0 if c >= 10 else c for c in p_cards]
    b_calc_values = [0 if c >= 10 else c for c in b_cards]
    
    p_score = sum(p_calc_values) % 10
    b_score = sum(b_calc_values) % 10

    # Xử lý Thắng tự nhiên (Natural 8, 9)
    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, total_shoe, p_pair_odds, b_pair_odds
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, total_shoe, p_pair_odds, b_pair_odds
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, total_shoe, p_pair_odds, b_pair_odds

    current_sum = sum(total_shoe.values())
    if current_sum == 0:
        return "Lỗi phân phối ma trận!", total_shoe, p_pair_odds, b_pair_odds
        
    prob_dict = {k: v / current_sum for k, v in total_shoe.items()}

    player_wins, banker_wins, ties = 0.0, 0.0, 0.0
    p_draws = p_score <= 5

    # Phân tích kịch bản lá thứ 3
    if not p_draws:  # Player đứng (6, 7 điểm)
        if b_score <= 5:  # Banker bắt buộc rút
            for card3_b, p_b in prob_dict.items():
                final_b = (b_score + card3_b) % 10
                if p_score > final_b: player_wins += p_b
                elif final_b > p_score: banker_wins += p_b
                else: ties += p_b
        else:  # Cả hai cùng đứng
            if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, total_shoe, p_pair_odds, b_pair_odds
            elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, total_shoe, p_pair_odds, b_pair_odds
            else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, total_shoe, p_pair_odds, b_pair_odds
    else:  # Player rút lá thứ 3
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
    if total_prob == 0: 
        return "Tổ hợp phân phối bằng rỗng!", total_shoe, p_pair_odds, b_pair_odds

    odds_res = {
        "Player": round((player_wins / total_prob) * 100, 2),
        "Banker": round((banker_wins / total_prob) * 100, 2),
        "Tie": round((ties / total_prob) * 100, 2)
    }
    
    return odds_res, total_shoe, p_pair_odds, b_pair_odds

# =========================================================================
# GIAO DIỆN PHÂN TÍCH TOÁN HỌC CAO CẤP (SUPREME UI/UX)
# =========================================================================
st.set_page_config(page_title="Baccarat Oracle Matrix Max v3", page_icon="🔮", layout="centered")
st.title("🔮 Oracle Matrix Max v3")
st.caption("Thuật toán phân rã ma trận tối đa kết hợp đồng bộ hóa Số Ván")
st.markdown("---")

# Cấu trúc lưu trữ thông minh thông qua Streamlit Session State
if 'shoe_history' not in st.session_state:
    st.session_state.shoe_history = []
if 'game_counter' not in st.session_state:
    st.session_state.game_counter = 0

# --- THANH ĐIỀU HƯỚNG BÊN (SIDEBAR CẤU HÌNH) ---
st.sidebar.header("⚙️ CẤU HÌNH HỘP BÀI NỀN")
decks = st.sidebar.selectbox("Tổng số bộ bài (Decks):", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.subheader("🔢 ĐỒNG BỘ SỐ VÁN THỰC TẾ")

# Ô nhập số ván trực tiếp tương tác đồng bộ với bảng đèn sòng bài
st.session_state.game_counter = st.sidebar.number_input(
    "GAME NUMBER (Số ván hiện tại):", 
    min_value=0, max_value=150, value=st.session_state.game_counter
)

if st.sidebar.button("🔄 LÀM MỚI TOÀN BỘ (RESET KHAY)", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.game_counter = 0
    st.rerun()

if st.sidebar.button("⏮️ HOÀN TÁC VÁN TRƯỚC (UNDO)", use_container_width=True):
    if len(st.session_state.shoe_history) > 0 and st.session_state.game_counter > 0:
        st.session_state.game_counter = max(0, st.session_state.game_counter - 1)
        st.session_state.shoe_history = st.session_state.shoe_history[:-5]  # Xoá ước lượng ván trước
        st.sidebar.success("Đã lùi lại dữ liệu ván trước thành công!")
        st.rerun()

# --- HIỂN THỊ CHỈ SỐ MONITOR TRÊN GIAO DIỆN CHÍNH ---
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.metric(label="🚩 TRẠNG THÁI VÁN CHƠI:", value=f"Ván thứ {st.session_state.game_counter}")
with col_m2:
    total_cards = decks * 52
    est_played = min(total_cards, int(st.session_state.game_counter * 4.95))
    st.metric(label="📊 ƯỚC TÍNH BÀI ĐÃ CHẠY:", value=f"{est_played} / {total_cards} lá")

st.markdown("---")

# --- KHỐI ĐẦU VÀO DỮ LIỆU BÀI VÁN HIỆN TẠI ---
st.subheader("🃏 Nhập dữ liệu phân tích ván này")
st.caption("Nhập toàn bộ các lá bài xuất hiện (Át=1 | 2->10 giữ nguyên | J=11, Q=12, K=13), cách nhau bằng dấu phẩy.")

col_p, col_b = st.columns(2)
with col_p:
    p_input = st.text_input("Bài PLAYER (Ví dụ: 1,5 hoặc 10,2,3):", "0")
with col_b:
    b_input = st.text_input("Bài BANKER (Ví dụ: 7,10 hoặc 4,5,0):", "0")

try:
    p_list = [int(x.strip()) for x in p_input.split(",") if x.strip() != ""]
    b_list = [int(x.strip()) for x in b_input.split(",") if x.strip() != ""]
except ValueError:
    st.error("⚠️ Định dạng lỗi! Bạn chỉ được phép nhập số (0-13) phân tách bằng dấu phẩy.")
    p_list, b_list = [], []

# --- KÍCH HOẠT ENGINE TÍNH TOÁN TOÁN HỌC ---
if st.button("🚀 KÍCH HOẠT MÁY QUÉT ORACLE TOÁN HỌC", use_container_width=True):
    if p_list and b_list:
        # Tách lấy 2 lá bài đầu tiên phục vụ tính toán kịch bản kéo bài lá thứ 3
        p_calc = p_list[:2]
        b_calc = b_list[:2]
        
        # Thực thi hàm toán học cốt lõi
        res, remaining_deck, p_pair, b_pair = calculate_baccarat_maximum_oracle(
            p_calc, b_calc, st.session_state.shoe_history, st.session_state.game_counter, shoe_decks=decks
        )
        
        if isinstance(res, dict):
            # 1. KẾT QUẢ CỬA CHÍNH (XÁC SUẤT ĐỘC LẬP VÁN TIẾP THEO)
            st.markdown("### 📊 Tỷ lệ lệnh ván kế tiếp:")
            
            st.write(f"🔵 **PLAYER WIN**: {res['Player']}%")
            st.progress(res['Player']/100)
            
            st.write(f"🔴 **BANKER WIN**: {res['Banker']}%")
            st.progress(res['Banker']/100)
            
            st.write(f"🟢 **TIE (HÒA)**: {res['Tie']}%")
            st.progress(res['Tie']/100)
            
            # 2. KẾT QUẢ CỬA PHỤ ĐÔI (Đã khôi phục dựa trên phân rã cấu trúc bài nền)
            st.markdown("### 💎 Xác suất xuất hiện Cặp Đôi ván kế tiếp:")
            col_p_pair, col_b_pair = st.columns(2)
            
            p_delta = f"🔥 Tốt (+{(p_pair-7.47):.2f}%)" if p_pair > 7.47 else "⚖️ Bình thường"
            b_delta = f"🔥 Tốt (+{(b_pair-7.47):.2f}%)" if b_pair > 7.47 else "⚖️ Bình thường"
            
            col_p_pair.metric(label="🔵 PLAYER PAIR", value=f"{p_pair}%", delta=p_delta)
            col_b_pair.metric(label="🔴 BANKER PAIR", value=f"{b_pair}%", delta=b_delta)
            
            # 3. TỰ ĐỘNG LƯU TRỮ VÀ TĂNG CHỈ SỐ ĐỒNG BỘ
            st.session_state.shoe_history.extend(p_list + b_list)
            st.session_state.game_counter += 1
            
            st.success(f" Ghi nhận hoàn tất dữ liệu ván {st.session_state.game_counter - 1}. Hệ thống tự động nhảy sang ván {st.session_state.game_counter}.")
            
            # 4. CHI TIẾT VECTOR KHAY BÀI CÒN LẠI (Sử dụng hệ metric scannable)
            with st.expander("🔍 Chi tiết số lượng các loại lá bài còn lại trong khay nền"):
                st.markdown("> Dữ liệu phân phối thực tế sau khi xử lý bù trừ số ván và trừ bài lộ diện:")
                display_cols = st.columns(5)
                for index, (card_num, rem_count) in enumerate(remaining_deck.items()):
                    card_label = "10,J,Q,K" if card_num == 0 else f"Lá [{card_num}]"
                    display_cols[index % 5].metric(label=card_label, value=f"{int(rem_count)} lá")
        else:
            st.warning(res)
