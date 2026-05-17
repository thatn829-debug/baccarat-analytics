# =========================================================================
# --- ĐIỀU KHIỂN NHẬP TAY & QUẢN LÝ FORM BIẾN ĐỔI ---
# =========================================================================
st.markdown("---")
st.subheader("🃏 Nạp Quân Bài Vừa Ra & Dự Đoán Ván Kế Tiếp")
st.caption("Nhập các lá bài vừa xuất hiện ở ván trước để hệ thống ghi nhớ vào khay, sau đó tự động tính toán xác suất cho ván hoàn toàn mới tiếp theo.")

# Sử dụng form để kiểm soát hành vi submit và tránh trigger rerun thừa
with st.form(key="baccarat_input_form", clear_on_submit=True):
    col_p, col_b = st.columns(2)
    with col_p: 
        p_input = st.text_input("🔵 PLAYER (Các lá bài vừa ra):", value="", placeholder="Ví dụ: 5,K,2")
    with col_b: 
        b_input = st.text_input("🔴 BANKER (Các lá bài vừa ra):", value="", placeholder="Ví dụ: J,7")
        
    submit_btn = st.form_submit_button("🚀 GHI NHẬN & TÍNH TOÁN VÁN TIẾP THEO", use_container_width=True, type="primary")

def clean_and_parse_input(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().replace(" ", "")
    tokens = []
    i = 0
    if "," in normalized:
        parts = normalized.split(",")
        for p in parts:
            p_clean = "".join([c for c in p if c in "2345678910AJQK"])
            if p_clean: tokens.append(p_clean)
    else:
        while i < len(normalized):
            if normalized[i:i+2] == "10": tokens.append("10"); i += 2
            elif normalized[i] in "23456789AJQK": tokens.append(normalized[i]); i += 1
            else: i += 1
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    result_list = []
    for tok in tokens:
        if tok in mapping: result_list.append(mapping[tok])
        elif tok.isdigit():
            val = int(tok)
            if 2 <= val <= 10: result_list.append(val)
    return result_list

if submit_btn:
    current_game_signature = f"P:{p_input.strip().upper()}|B:{b_input.strip().upper()}"
    
    if not p_input.strip() and not b_input.strip():
        st.warning("⚠️ Vui lòng điền thông tin quân bài để kích hoạt phép tính.")
    elif current_game_signature == st.session_state.last_played_cards:
        st.error("⛔ Trùng lặp hoàn toàn với dữ liệu ván vừa nạp!")
    else:
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        
        if p_list or b_list:
            # Bước 1: Cập nhật lịch sử xúc xắc sàn (Xu hướng P - B - T) dựa trên kết quả ván ĐÃ QUA
            p_score_eval = sum([0 if c >= 10 else c for c in p_list]) % 10
            b_score_eval = sum([0 if c >= 10 else c for c in b_list]) % 10
            if p_score_eval > b_score_eval:
                st.session_state.outcome_history.append("Player")
            elif b_score_eval > p_score_eval:
                st.session_state.outcome_history.append("Banker")
            else:
                st.session_state.outcome_history.append("Tie")

            # Bước 2: Đẩy các quân bài cũ này vào khay bài tổng (Shoe History)
            st.session_state.shoe_history.extend(p_list + b_list)
            st.session_state.last_played_cards = current_game_signature
            
            # Bước 3: GỌI TOÁN ENGINE DỰ ĐOÁN CHO VÁN MỚI 
            # Truyền mảng rỗng [] vào p_cards và b_cards vì đây là dự đoán khi ván mới CHƯA CHIA LÁ NÀO.
            core_output = calculate_baccarat_v18_ultimate(
                [], [], st.session_state.shoe_history, shoe_decks=decks,
                manual_cards_used=manual_cards, manual_games_played=manual_games,
                p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
            )
            
            if isinstance(core_output, str):
                st.session_state.last_results = (core_output, {}, 0.0, 0.0, "LỖI", 0, False, [])
            else:
                st.session_state.last_results = core_output
                
            st.rerun()
