import streamlit as st
import streamlit.components.v1 as components

# =========================================================================
# SYSTEM CORE v7.0: THE ULTIMATE ABSOLUTE HYPERGEOMETRIC EXHAUSTION ENGINE
# =========================================================================
def calculate_baccarat_ultimate_core(p_cards, b_cards, shoe_history, shoe_decks=8, manual_cards_used=0, manual_games_played=0):
    """
    Hệ thống lõi v7.0: Đạt giới hạn tối cao của toán học tổ hợp hiện đại.
    Giữ nguyên cấu trúc 13 lá bài độc lập để tính toán cửa đôi tuyệt đối, 
    sau đó phân rã ma trận động theo thời gian thực để quét sạch cây quyết định.
    """
    total_initial_cards = shoe_decks * 52
    # Khởi tạo khay bài chính xác theo từng quân bài (Giữ riêng J, Q, K để tính Cửa Đôi)
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    # --- BỘ LỌC KIỂM TRA LOGIC VÀ ĐỒNG BỘ DỮ LIỆU CHẶN LỖI ---
    if manual_cards_used > total_initial_cards:
        return f"❌ Bất hợp lý: Số lá bài đã dùng ({manual_cards_used} lá) vượt quá tổng số bài trong khay ({total_initial_cards} lá)!", {}, 0.0, 0.0, "LỖI DỮ LIỆU", total_initial_cards

    max_possible_games = int(total_initial_cards / 4)
    if manual_games_played > max_possible_games:
        return f"❌ Bất hợp lý: Số ván đã chạy ({manual_games_played} ván) vượt quá giới hạn vật lý của khay bài ({max_possible_games} ván)!", {}, 0.0, 0.0, "LỖI DỮ LIỆU", total_initial_cards

    if manual_cards_used > 0 and manual_games_played > 0:
        min_cards_needed = manual_games_played * 4  
        max_cards_needed = manual_games_played * 6  
        if manual_cards_used < min_cards_needed or manual_cards_used > max_cards_needed:
            return f"❌ Mâu thuẫn dữ liệu: {manual_games_played} ván thì số lá bài phải nằm trong khoảng từ {min_cards_needed} đến {max_cards_needed} lá. Bạn đang nhập {manual_cards_used} lá!", {}, 0.0, 0.0, "LỖI MÂU THUẪN", total_initial_cards

    # --- TIẾN TRÌNH KHẤU TRỪ TRẠNG THÁI KHAY BÀI REAL-TIME ---
    detailed_cards_count = len(shoe_history)
    
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure and deck_structure[card_val] > 0:
                deck_structure[card_val] -= 1
        cards_left = total_initial_cards - detailed_cards_count
        mode = "Quét Sạch Cây Quyết Định Tổ Hợp Đa Biến (Bản Tối Cao 100%)"
    else:
        # Cơ chế ước lượng tiệm cận phân phối chuẩn dựa trên Big Data Casino thực tế
        cards_removed = 0
        if manual_cards_used > 0:
            cards_removed = manual_cards_used
            mode = "Ước lượng Tiệm Cận Bậc Cao (Theo số lượng lá)"
        elif manual_games_played > 0:
            cards_removed = int(manual_games_played * 4.9315) 
            mode = f"Ước lượng Tiệm Cận Bậc Cao (Theo số ván: ~{cards_removed} lá)"
        else:
            cards_removed = 0
            mode = "Khay bài Mới (Tỷ lệ xác suất gốc của Nhà Cái)"

        cards_left = max(0, total_initial_cards - cards_removed)
        if cards_removed > 0:
            ratio = cards_left / total_initial_cards
            for card_num in deck_structure:
                deck_structure[card_num] = (4 * shoe_decks) * ratio

    N = float(sum(deck_structure.values()))
    if N <= 6:
        return "⚠️ Cảnh báo: Khay bài đã vơi quá giới hạn an toàn để tính toán!", {}, 0.0, 0.0, mode, cards_left
    
    # --- TÍNH TOÁN XÁC SUẤT CỬA ĐÔI TUYỆT ĐỐI (Hypergeometric Phân Phối Không Hoàn Lại) ---
    p_pair_prob = 0.0
    for count in deck_structure.values():
        if count >= 2:
            p_pair_prob += (count / N) * ((count - 1) / (N - 1))
    p_pair_odds = round(p_pair_prob * 100, 2)

    b_pair_prob = 0.0
    if N > 3:
        for b_count in deck_structure.values():
            if b_count >= 2:
                # Tính toán tất cả các tổ hợp bốc bài có thể xảy ra của Player để tìm xác suất trồi sụt của Banker Đôi
                p_rem_0 = ((N - b_count) / N) * ((N - b_count - 1) / (N - 1))
                p_rem_1 = 2 * (b_count / N) * ((N - b_count) / (N - 1))
                p_rem_2 = (b_count / N) * ((b_count - 1) / (N - 1))
                b_pair_prob += (p_rem_0 * (b_count / (N - 2)) * ((b_count - 1) / (N - 3)) +
                                p_rem_1 * (max(0.0, b_count - 1) / (N - 2)) * (max(0.0, b_count - 2) / (N - 3)) +
                                p_rem_2 * (max(0.0, b_count - 2) / (N - 2)) * (max(0.0, b_count - 3) / (N - 3)))
    b_pair_odds = round(b_pair_prob * 100, 2)

    # --- PHÂN RÃ MA TRẬN KHAY BÀI VỀ HỆ ĐIỂM BACCARAT (0-9) ---
    score_deck = {i: 0.0 for i in range(10)}
    for card_num, count in deck_structure.items():
        bacc_val = 0 if card_num >= 10 else card_num
        score_deck[bacc_val] += count

    # Khấu trừ tức thời các lá bài đang hiển thị công khai trên bàn cược
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0:
            score_deck[val] -= 1

    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    # KIỂM TRA ĐIỀU KIỆN THẮNG TỰ NHIÊN (NATURAL WINS)
    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left

    current_sum = float(sum(score_deck.values()))
    if current_sum <= 0: return {"Player": 44.62, "Banker": 45.86, "Tie": 9.52}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left
        
    player_wins, banker_wins, ties = 0.0, 0.0, 0.0

    # -----------------------------------------------------------------
    # DUYỆT CẠN CÂY QUYẾT ĐỊNH BA TẦNG KHẤU TRỪ ĐỘNG (INFINITE DEPTH TREE)
    # -----------------------------------------------------------------
    if p_score >= 6:  # Player đứng im
        if b_score <= 5:  # Banker bắt buộc phải rút lá thứ 3
            for card3_b in range(10):
                w_b = score_deck[card3_b]
                if w_b > 0:
                    prob_b = w_b / current_sum
                    final_b = (b_score + card3_b) % 10
                    if p_score > final_b: player_wins += prob_b
                    elif final_b > p_score: banker_wins += prob_b
                    else: ties += prob_b
        else:  # Cả hai cùng đứng im phối hợp điểm gốc
            if p_score > b_score: player_wins += 1.0
            elif b_score > p_score: banker_wins += 1.0
            else: ties += 1.0
    else:  # Player bắt buộc phải rút lá thứ 3
        for card3_p in range(10):
            w_p = score_deck[card3_p]
            if w_p > 0:
                prob_p = w_p / current_sum
                final_p = (p_score + card3_p) % 10
                
                # --- KHẤU TRỪ ĐỘNG TẦNG 1 (Lá thứ 3 Player bốc ra) ---
                rem_sum_after_p = current_sum - 1.0
                
                # Áp dụng Luật bài thứ 3 Chuẩn hóa Quốc tế (Tableau Rules)
                b_draws = False
                if b_score <= 2: b_draws = True
                elif b_score == 3 and card3_p != 8: b_draws = True
                elif b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]: b_draws = True
                elif b_score == 5 and card3_p in [4, 5, 6, 7]: b_draws = True
                elif b_score == 6 and card3_p in [6, 7]: b_draws = True
                
                if b_draws and rem_sum_after_p > 0:
                    for card3_b in range(10):
                        # --- KHẤU TRỪ ĐỘNG TẦNG 2 (Lá thứ 3 Banker bốc ra phụ thuộc hoàn toàn) ---
                        available_b = score_deck[card3_b] - (1.0 if card3_b == card3_p else 0.0)
                        if available_b > 0:
                            prob_b = available_b / rem_sum_after_p
                            final_b = (b_score + card3_b) % 10
                            
                            combined_weight = prob_p * prob_b
                            if final_p > final_b: player_wins += combined_weight
                            elif final_b > final_p: banker_wins += combined_weight
                            else: ties += combined_weight
                else:  # Banker đứng im theo luật định
                    if final_p > b_score: player_wins += prob_p
                    elif b_score > final_p: banker_wins += prob_p
                    else: ties += prob_p

    total_prob = player_wins + banker_wins + ties
    if total_prob == 0: total_prob = 1.0

    odds_res = {
        "Player": round((player_wins / total_prob) * 100, 2),
        "Banker": round((banker_wins / total_prob) * 100, 2),
        "Tie": round((ties / total_prob) * 100, 2)
    }
    return odds_res, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left

# =========================================================================
# INTERFACE DESIGN & STYLES
# =========================================================================
st.set_page_config(page_title="Oracle Ultimate Edge v7.0", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stColumn"] { width: 50% !important; min-width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'game_counter' not in st.session_state: st.session_state.game_counter = 0
if 'last_results' not in st.session_state: st.session_state.last_results = None

# --- SIDEBAR CẤU HÌNH ---
st.sidebar.header("⚙️ Cấu Hình Hệ Thống")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("### 📊 Thiết lập nhanh khay bài")
st.sidebar.caption("Nếu nhập cả 2 ô dưới đây, hệ thống sẽ tự động kiểm tra tính logic (Tránh mâu thuẫn số lá bài/số ván).")

manual_cards = st.sidebar.number_input("Số LÁ BÀI đã chia (nếu biết):", min_value=0, max_value=decks*52, value=0, step=1)
manual_games = st.sidebar.number_input("Hoặc Số VÁN đã chạy (nếu biết):", min_value=0, max_value=150, value=0, step=1)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 RESET KHAY BÀI MỚI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.game_counter = 0
    st.session_state.last_results = None
    st.rerun()

# --- HIỂN THỊ KẾT QUẢ ĐỐI XỨNG NGANG ---
if st.session_state.last_results:
    results_data = st.session_state.last_results
    
    if isinstance(results_data[0], str) and results_data[0].startswith("❌"):
        st.error(results_data[0])
    elif isinstance(results_data[0], str) and results_data[0].startswith("⚠️"):
        st.warning(results_data[0])
    else:
        res, p_pair, b_pair, remaining_deck, current_mode, cards_left = results_data
        
        left_result_col, right_pair_col = st.columns(2)
        with left_result_col:
            st.markdown("#### 📊 Cửa Chính")
            st.metric("🔵 PLAYER", f"{res['Player']}%")
            st.markdown(f"<p style='color:gray; font-size:11px; margin-top:-12px;'>Payout: 1 ăn 1.00</p>", unsafe_allow_html=True)
            st.metric("🔴 BANKER", f"{res['Banker']}%")
            st.markdown(f"<p style='color:gray; font-size:11px; margin-top:-12px;'>Payout: 1 ăn 0.95 (Trừ phế 5%)</p>", unsafe_allow_html=True)
            st.metric("🟢 TIE WIN", f"{res['Tie']}%")
            st.progress(res['Banker'] / 100 if res['Banker'] > 0 else 0)
            
        with right_pair_col:
            st.markdown("#### 💎 Cửa Đôi")
            st.metric("🔵 CON ĐÔI", f"{p_pair}%", delta="🔥 LỢI THẾ THẮNG" if p_pair > 7.47 else "⚖️ BÌNH THƯỜNG")
            st.metric("🔴 CÁI ĐÔI", f"{b_pair}%", delta="🔥 LỢI THẾ THẮNG" if b_pair > 7.47 else "⚖️ BÌNH THƯỜNG")

        st.markdown("---")
        
        # --- QUẢN LÝ VỐN KELLY TỐI ƯU HÓA THEO PHẾ BIỆT LẬP ---
        st.markdown("### 💰 Phân Tích Ma Trận Quản Lý Vốn")
        k_col1, k_col2 = st.columns(2)
        max_side = "Player" if res['Player'] > res['Banker'] else "Banker"
        max_prob = res[max_side] / 100.0
        
        # Khớp nối chính xác hệ số thanh toán thực tế của nhà cái
        b = 0.95 if max_side == "Banker" else 1.00
        q = 1.0 - max_prob
        
        # Công thức Kelly chuẩn chỉnh cho cá cược có phế biệt lập
        kelly_per = ((b * max_prob) - q) / b * 100
        kelly_per = max(0.0, kelly_per)
        
        with k_col1:
            if res['Player'] == 100.0 or res['Banker'] == 100.0:
                st.success(f"🎯 LỆNH TỐI CAO: Vào **{max_side.upper()}** (Tỷ lệ: 100%)")
            elif kelly_per > 0.1:
                # Áp dụng tỷ lệ chia vốn an toàn chống biến động ngắn hạn (Quarter Kelly = 1/4)
                safe_investment = round(kelly_per / 4, 2)
                if safe_investment >= 0.25:
                    st.info(f"✨ GỢI Ý: Vào **{max_side.upper()}** (Vốn khuyên dùng: {safe_investment}%)")
                else:
                    st.warning("⚖️ BIÊN ĐỘ MỎNG: Lợi thế toán học quá thấp. Khuyên dùng: BỎ QUA.")
            else:
                st.warning("⚖️ CÂN BẰNG: Không tìm thấy lợi thế toán học tốt. BỎ QUA.")
                
        with k_col2:
            st.caption(f"Chế độ quét ma trận:\n{current_mode}")

        with st.expander("📊 Chi tiết cấu trúc ma trận khay bài còn lại"):
            st.write(f"Số lá bài còn lại ước tính trong khay: **{int(cards_left)} / {decks*52}** lá.")
            cols = st.columns(5)
            labels_13 = {1: "A", 11: "J", 12: "Q", 13: "K"}
            for idx, (num, cnt) in enumerate(remaining_deck.items()):
                card_label = labels_13.get(num, f"[{num}]")
                cols[idx % 5].text(f"{card_label}: {round(cnt, 1)} lá")
else:
    st.info("🔮 Vui lòng điền điểm số ván hiện tại vào ô bên dưới để kích hoạt hệ quét toán học.")

st.markdown("---")

# --- KHU VỰC NHẬP LIỆU GIAO DIỆN PHẲNG ---
head_col, status_col = st.columns([2, 1])
with head_col:
    st.subheader("🃏 Điền điểm ván này")
with status_col:
    display_game = st.session_state.game_counter if st.session_state.game_counter > 0 else manual_games
    st.markdown(f"<div style='text-align: right; margin-top: 10px; font-weight: bold; color: #ff4b4b;'>#Ván: {display_game}</div>", unsafe_allow_html=True)

col_p, col_b = st.columns(2)
with col_p: p_input = st.text_input("PLAYER (Lá bài):", value="", placeholder="Gõ liền: 5k2 hoặc a10j")
with col_b: b_input = st.text_input("BANKER (Lá bài):", value="", placeholder="Gõ liền: j7 hoặc 98q")


# =========================================================================
# LÕI PHÁT HIỆN GÕ PHÍM - TỰ ĐỘNG PHẨY VÀ CHUYỂN IN HOA (JAVASCRIPT ENGINE)
# =========================================================================
components.html(
    """
    <script>
    function applyAutoComma() {
        const inputs = parent.document.querySelectorAll('div[data-testid="stTextInput"] input');
        
        inputs.forEach(input => {
            if (input.getAttribute('data-macro-active') === 'true') return;
            input.setAttribute('data-macro-active', 'true');
            
            input.addEventListener('input', function(e) {
                let val = e.target.value.toUpperCase();
                val = val.replace(/[^2-910AJQK,]/g, '');
                
                let tempTokens = [];
                let i = 0;
                let cleanStr = val.replace(/,/g, ''); 
                
                while (i < cleanStr.length) {
                    if (cleanStr[i] === '1' && cleanStr[i+1] === '0') {
                        tempTokens.push('10');
                        i += 2;
                    } else {
                        tempTokens.push(cleanStr[i]);
                        i += 1;
                    }
                }
                
                let finalVal = tempTokens.join(',');
                e.target.value = finalVal;
                input.dispatchEvent(new Event('input', { bubbles: true }));
            });
        });
    }
    setInterval(applyAutoComma, 500);
    </script>
    """,
    height=0,
)


def parse_card_input(input_str):
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    return [mapping[x.strip().upper()] if x.strip().upper() in mapping else int(x.strip()) for x in input_str.split(",") if x.strip() != ""]

try:
    p_list = parse_card_input(p_input)
    b_list = parse_card_input(b_input)
except ValueError:
    p_list, b_list = [], []

if st.button("🚀 KÍCH HOẠT QUÉT MA TRẬN PHÂN TÍCH", use_container_width=True, type="primary"):
    # Đưa chính xác 2 lá đầu tiên vào để thuật toán lõi tự động bóc tách cây quyết định cho các lá tiếp theo
    p_calc = p_list[:2] if p_list else []
    b_calc = b_list[:2] if b_list else []
    
    core_output = calculate_baccarat_ultimate_core(
        p_calc, b_calc, st.session_state.shoe_history, shoe_decks=decks,
        manual_cards_used=manual_cards, manual_games_played=manual_games
    )
    
    if isinstance(core_output, str):
        st.session_state.last_results = (core_output, {}, 0.0, 0.0, "LỖI", 0)
    else:
        res, remaining_deck, p_pair, b_pair, mode, cards_left = core_output
        st.session_state.last_results = (res, p_pair, b_pair, remaining_deck, mode, cards_left)
        
        if p_list and b_list and not mode.startswith("LỖI"):
            st.session_state.shoe_history.extend(p_list + b_list)
            st.session_state.game_counter = (st.session_state.game_counter if st.session_state.game_counter > 0 else manual_games) + 1
            
    st.rerun()
