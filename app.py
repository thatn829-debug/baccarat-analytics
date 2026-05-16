import streamlit as st
import pandas as pd
import numpy as np

# =========================================================================
# SYSTEM CORE v12.0: VECTORIZED EXTREME COMPACT ENGINE & TRUE EV CALCULATOR
# =========================================================================
def calculate_baccarat_v12_core(p_cards, b_cards, shoe_history, shoe_decks=8, 
                                manual_cards_used=0, manual_games_played=0,
                                p_wins=0, b_wins=0, tie_wins=0, is_super6=False):
    total_initial_cards = shoe_decks * 52
    deck_structure = np.full(14, float(4 * shoe_decks))
    deck_structure[0] = 0.0 # Bỏ chỉ số 0 để đồng bộ với số thứ tự bài từ 1-13
    
    sum_wins_games = p_wins + b_wins + tie_wins

    if manual_cards_used > total_initial_cards or manual_games_played > int(total_initial_cards / 4):
        return "❌ LỖI RỦI RO: Dữ liệu cấu hình khay bài vượt giới hạn vật lý quy định!", {}, 0.0, 0.0, "ERROR", total_initial_cards

    detailed_cards_count = len(shoe_history)
    
    # KHẤU TRỪ VECTOR THỜI GIAN THỰC
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if 1 <= card_val <= 13 and deck_structure[card_val] > 0:
                deck_structure[card_val] -= 1
        cards_left = total_initial_cards - detailed_cards_count
        mode = "VECTORIZED 2D CONVOLUTION MATRIX (TRẦN VẬT LÝ v12.0)"
    else:
        cards_removed = 0
        if manual_cards_used > 0:
            cards_removed = manual_cards_used
            mode = "ƯỚC LƯỢNG TIỆM CẬN BẬC CAO"
        elif sum_wins_games > 0:
            cards_removed = int((p_wins * 4.8633) + (b_wins * 4.8118) + (tie_wins * 5.2312))
            mode = f"PHÂN RÃ TRỌNG SỐ THỜI GIAN THỰC (~{cards_removed} LÁ)"
        else:
            cards_removed = 0
            mode = "MA TRẬN GỐC KHỞI TẠO"

        cards_left = max(0, total_initial_cards - cards_removed)
        if cards_removed > 0:
            deck_structure[1:14] = (4 * shoe_decks) * (cards_left / total_initial_cards)

    N = float(np.sum(deck_structure))
    if N <= 6:
        return "⚠️ Cảnh báo: Khay bài đã vơi quá giới hạn an toàn để tính toán!", {}, 0.0, 0.0, mode, cards_left
    
    # TÍNH TOÁN CỬA ĐÔI QUA VECTOR HYPERGEOMETRIC TRUY HỒI
    p_pair_prob = np.sum([ (c/N)*((c-1)/(N-1)) for c in deck_structure[1:14] if c >= 2 ])
    p_pair_odds = round(p_pair_prob * 100, 2)

    b_pair_prob = 0.0
    if N > 3:
        for b_count in deck_structure[1:14]:
            if b_count >= 2:
                p_rem_0 = ((N - b_count) / N) * ((N - b_count - 1) / (N - 1))
                p_rem_1 = 2 * (b_count / N) * ((N - b_count) / (N - 1))
                p_rem_2 = (b_count / N) * ((b_count - 1) / (N - 1))
                b_pair_prob += (p_rem_0 * (b_count / (N - 2)) * ((b_count - 1) / (N - 3)) +
                                p_rem_1 * (max(0.0, b_count - 1) / (N - 2)) * (max(0.0, b_count - 2) / (N - 3)) +
                                p_rem_2 * (max(0.0, b_count - 2) / (N - 2)) * (max(0.0, b_count - 3) / (N - 3)))
    b_pair_odds = round(b_pair_prob * 100, 2)

    # ĐỒNG BỘ SANG HỆ ĐIỂM BACCARAT 10 NHÁNH (0-9)
    score_deck = np.zeros(10)
    for num in range(1, 14):
        val = 0 if num >= 10 else num
        score_deck[val] += deck_structure[num]

    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] -= 1

    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    # Ngắt điều kiện nếu dính Natural
    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, {i: score_deck[0 if i>=10 else i] for i in range(1,14)}, p_pair_odds, b_pair_odds, mode, cards_left
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, {i: score_deck[0 if i>=10 else i] for i in range(1,14)}, p_pair_odds, b_pair_odds, mode, cards_left
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, {i: score_deck[0 if i>=10 else i] for i in range(1,14)}, p_pair_odds, b_pair_odds, mode, cards_left

    current_sum = float(np.sum(score_deck))
    if current_sum <= 0: return {"Player": 44.62, "Banker": 45.86, "Tie": 9.52}, {}, p_pair_odds, b_pair_odds, mode, cards_left
        
    player_wins, banker_wins, ties = 0.0, 0.0, 0.0

    # CHẠY MA TRẬN TÍCH CHẬP SONG SONG (PARALLEL CONVOLUTION LÁ THỨ 3)
    if p_score >= 6: 
        if b_score <= 5: 
            for card3_b in range(10):
                w_b = score_deck[card3_b]
                if w_b > 0:
                    prob_b = w_b / current_sum
                    final_b = (b_score + card3_b) % 10
                    if p_score > final_b: player_wins += prob_b
                    elif final_b > p_score: banker_wins += prob_b
                    else: ties += prob_b
        else:
            if p_score > b_score: player_wins += 1.0
            elif b_score > p_score: banker_wins += 1.0
            else: ties += 1.0
    else: 
        for card3_p in range(10):
            w_p = score_deck[card3_p]
            if w_p <= 0: continue
            prob_p = w_p / current_sum
            final_p = (p_score + card3_p) % 10
            
            rem_sum_after_p = current_sum - 1.0
            if rem_sum_after_p <= 0: continue
            
            b_draws = False
            if b_score <= 2: b_draws = True
            elif b_score == 3 and card3_p != 8: b_draws = True
            elif b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]: b_draws = True
            elif b_score == 5 and card3_p in [4, 5, 6, 7]: b_draws = True
            elif b_score == 6 and card3_p in [6, 7]: b_draws = True
            
            if b_draws:
                for card3_b in range(10):
                    available_b = score_deck[card3_b] - (1.0 if card3_b == card3_p else 0.0)
                    if available_b > 0:
                        prob_b = available_b / rem_sum_after_p
                        final_b = (b_score + card3_b) % 10
                        combined_weight = prob_p * prob_b
                        
                        if final_p > final_b: player_wins += combined_weight
                        elif final_b > final_p: banker_wins += combined_weight
                        else: ties += combined_weight
            else: 
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
    
    # Chuyển đổi deck_structure dạng dict để phục vụ việc hiển thị ở giao diện
    out_deck = {i: float(deck_structure[i]) for i in range(1, 14)}
    return odds_res, out_deck, p_pair_odds, b_pair_odds, mode, cards_left

# =========================================================================
# LÕI PHÂN TÍCH CHUỖI VÀ QUÉT ĐỘ LỆCH (ADVANCED TREND PATTERN ENGINE)
# =========================================================================
def analyze_shoe_patterns(outcome_history):
    if len(outcome_history) < 2:
        return "⚖️ ỔN ĐỊNH LÝ THUYẾT", "Hệ thống đang tích lũy dữ liệu chuỗi ván bài.", "Normal"
        
    last_outcome = outcome_history[-1]
    streak_len = 0
    for out in reversed(outcome_history):
        if out == last_outcome: streak_len += 1
        else: break
            
    is_pingpong = True
    if len(outcome_history) >= 4:
        for i in range(-1, -5, -1):
            if outcome_history[i] == outcome_history[i-1] and outcome_history[i] != "Tie" and outcome_history[i-1] != "Tie":
                is_pingpong = False
                break
    else:
        is_pingpong = False

    if streak_len >= 4 and last_outcome != "Tie":
        return "⚠️ CẢNH BÁO BỆT DÂY CAO", f"Cửa **{last_outcome.upper()}** đang đi dây dài **{streak_len} ván**. Tuyệt đối không bẻ cầu dòng tiền.", "High_Streak"
    elif is_pingpong:
        return "🔄 DÂY NHẢY ĐƠN (PING-PONG)", "Cấu trúc bàn đang nhảy xen kẽ. Ưu tiên đánh thuận nhịp dòng tiền.", "PingPong"
    
    return "⚖️ KHAY BÀI ĐAN XEN ỔN ĐỊNH", "Biên độ dao động các cửa nằm trong khoảng cân bằng lý thuyết.", "Normal"

# =========================================================================
# STREAMLIT UI DESIGN MATRIX v12.0
# =========================================================================
st.set_page_config(page_title="Oracle Quantum Extreme v12.0", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stColumn"] { width: 50% !important; min-width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    .css-1kyx603 {font-size: 14px !important;}
    </style>
    """, 
    unsafe_allow_html=True
)

# Khởi tạo ma trận bộ nhớ cục bộ chống crash
if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'game_counter' not in st.session_state: st.session_state.game_counter = 0
if 'last_results' not in st.session_state: st.session_state.last_results = None
if 'last_played_cards' not in st.session_state: st.session_state.last_played_cards = ""
if 'live_logs' not in st.session_state: st.session_state.live_logs = []
if 'last_cards_added' not in st.session_state: st.session_state.last_cards_added = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'edge_history_df' not in st.session_state: st.session_state.edge_history_df = pd.DataFrame(columns=["Ván", "Player_Edge", "Banker_Edge"])
if 'fibo_index' not in st.session_state: st.session_state.fibo_index = 0
if 'martingale_step' not in st.session_state: st.session_state.martingale_step = 1

# --- SIDEBAR OPERATIONAL ---
st.sidebar.header("🔮 QUANTUM CORE CONFIG v12.0")
decks = st.sidebar.selectbox("Số bộ bài quy chuẩn:", [8, 6, 4], index=0)
is_super6_rule = st.sidebar.checkbox("Áp dụng luật bàn Super 6 (Không xâu, Banker 6 điểm ăn nửa)", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💰 ĐIỀU PHỐI VỐN CHIẾN THUẬT")
capital_strategy = st.sidebar.selectbox(
    "Chiến thuật phân bổ:",
    ["Kelly Criterion (Tối ưu EV)", "Fibonacci (Bảo toàn vốn)", "Martingale Sửa Đổi (Áp đảo)"]
)
base_bet = st.sidebar.number_input("Tiền cược cơ sở (1 Đơn vị):", min_value=10000, value=50000, step=10000)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 THIẾT LẬP NHANH TÌNH TRẠNG BÀN")
manual_cards = st.sidebar.number_input("Số lá đã chia:", min_value=0, max_value=decks*52, value=0, step=1)
manual_games = st.sidebar.number_input("Tổng số ván đã qua:", min_value=0, max_value=150, value=0, step=1)

st.sidebar.markdown("**Thống kê bảng điểm (Hàng dọc):**")
p_wins_input = st.sidebar.number_input("🔵 Cửa Player thắng:", min_value=0, max_value=100, value=0, step=1)
b_wins_input = st.sidebar.number_input("🔴 Cửa Banker thắng:", min_value=0, max_value=100, value=0, step=1)
tie_wins_input = st.sidebar.number_input("🟢 Cửa Hòa (Tie) thắng:", min_value=0, max_value=100, value=0, step=1)

calculated_total_wins = p_wins_input + b_wins_input + tie_wins_input
is_data_discrepancy = (manual_games != calculated_total_wins)

st.sidebar.markdown("---")
if st.session_state.live_logs:
    if st.sidebar.button("↩️ HOÀN TÁC VÁN VỪA NHẬP", use_container_width=True):
        if st.session_state.last_cards_added:
            num_to_remove = len(st.session_state.last_cards_added[-1])
            if num_to_remove <= len(st.session_state.shoe_history):
                st.session_state.shoe_history = st.session_state.shoe_history[:-num_to_remove]
            st.session_state.last_cards_added.pop()
        st.session_state.live_logs.pop()
        if len(st.session_state.outcome_history) > 0: st.session_state.outcome_history.pop()
        if not st.session_state.edge_history_df.empty: st.session_state.edge_history_df = st.session_state.edge_history_df.iloc[:-1]
        st.session_state.game_counter = max(0, st.session_state.game_counter - 1)
        st.session_state.last_results = None
        st.session_state.last_played_cards = ""
        st.rerun()

if st.sidebar.button("🔄 RESET TOÀN BỘ KHAY BÀI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.game_counter = 0
    st.session_state.last_results = None
    st.session_state.last_played_cards = ""
    st.session_state.live_logs = []
    st.session_state.last_cards_added = []
    st.session_state.outcome_history = []
    st.session_state.edge_history_df = pd.DataFrame(columns=["Ván", "Player_Edge", "Banker_Edge"])
    st.session_state.fibo_index = 0
    st.session_state.martingale_step = 1
    st.rerun()

display_game = manual_games + len(st.session_state.live_logs)

# --- DISPLAY INTERFACE INTERACTION ---
if is_data_discrepancy:
    st.error(f"🛑 ĐỒNG BỘ THẤT BẠI: Tổng số ván thiết lập ({manual_games}) không khớp với tổng số ván chi tiết từng cửa ({calculated_total_wins})!")
else:
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
                st.markdown("#### 📊 Ma Trận Cửa Chính")
                st.metric("🔵 PLAYER", f"{res['Player']}%")
                st.metric("🔴 BANKER", f"{res['Banker']}%")
                st.metric("🟢 TIE WIN", f"{res['Tie']}%")
                st.progress(res['Banker'] / 100 if res['Banker'] > 0 else 0)
                
            with right_pair_col:
                st.markdown("#### 💎 Ma Trận Cửa Đôi")
                st.metric("🔵 PLAYER PAIR", f"{p_pair}%", delta="🔥 CÓ LỢI THẾ" if p_pair > 7.47 else "⚖️ BÌNH THƯỜNG")
                st.metric("🔴 BANKER PAIR", f"{b_pair}%", delta="🔥 CÓ LỢI THẾ" if b_pair > 7.47 else "⚖️ BÌNH THƯỜNG")

            st.markdown("---")
            
            # XU HƯỚNG BỆT VÀ CHUỖI
            st.markdown("### 🧬 Hệ Thống Nhận Diện Xu Hướng Cầu Bài")
            trend_title, trend_desc, trend_level = analyze_shoe_patterns(st.session_state.outcome_history)
            if trend_level == "High_Streak": st.error(f"**{trend_title}** \n\n {trend_desc}")
            elif trend_level == "PingPong": st.info(f"**{trend_title}** \n\n {trend_desc}")
            else: st.success(f"**{trend_title}** \n\n {trend_desc}")

            st.markdown("---")
            
            # QUÂN BÀI ĐI TIỀN VẬT LÝ NÂNG CAO - TRỪ KHẤU HAO TIỀN XÂU (TRUE EV)
            st.markdown(f"### 💰 Phân Phối Dòng Tiền Tối Ưu Ròng ({capital_strategy})")
            k_col1, k_col2 = st.columns(2)
            max_side = "Player" if res['Player'] > res['Banker'] else "Banker"
            max_prob = res[max_side] / 100.0
            
            # Tính toán khấu trừ hoa hồng ròng (EV Real Deduction)
            if max_side == "Banker":
                b_factor = 1.00 if is_super6_rule else 0.95 
            else:
                b_factor = 1.00
                
            q_factor = 1.0 - max_prob
            kelly_per = ((b_factor * max_prob) - q_factor) / b_factor * 100
            kelly_per = max(0.0, kelly_per)
            
            fibo_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
            idx_fibo = min(st.session_state.fibo_index, len(fibo_sequence)-1)
            fibo_unit = fibo_sequence[idx_fibo]
            
            martingale_unit = 2 ** (st.session_state.martingale_step - 1)

            with k_col1:
                if res['Player'] == 100.0 or res['Banker'] == 100.0:
                    st.success(f"🎯 LỆNH TỐI CAO: Vào **{max_side.upper()}** (Đã khóa kết quả dừng bài)")
                elif "Kelly" in capital_strategy:
                    if kelly_per > 0.1:
                        safe_investment = round(kelly_per / 4, 2)
                        if safe_investment >= 0.25:
                            st.info(f"✨ LỆNH VÀO: Đặt **{max_side.upper()}**\n\n💵 Tỷ lệ chia quỹ: **{safe_investment}%** tổng vốn.")
                        else:
                            st.warning("⚖️ LỢI NHUẬN RÒNG QUÁ MỎNG (EV tiêu cực) -> BỎ QUA.")
                    else:
                        st.warning("⚖️ KHÔNG TÌM THẤY LỢI THẾ TOÁN HỌC -> BỎ QUA.")
                elif "Fibonacci" in capital_strategy:
                    st.info(f"✨ LỆNH VÀO: Đặt **{max_side.upper()}**\n\n💵 Mức cược ván này: **{fibo_unit} Đơn vị** ({fibo_unit * base_bet:,} VNĐ)")
                elif "Martingale" in capital_strategy:
                    st.info(f"✨ LỆNH VÀO: Đặt **{max_side.upper()}**\n\n💵 Mức cược ván này: **{martingale_unit} Đơn vị** ({martingale_unit * base_bet:,} VNĐ)")
                    
            with k_col2:
                st.caption(f"Hạ tầng tính toán:\n{current_mode}")
                if "Fibonacci" in capital_strategy or "Martingale" in capital_strategy:
                    st.markdown("**Xác nhận ván thực tế để nhảy bậc cược:**")
                    f_win, f_lose = st.columns(2)
                    if f_win.button("👍 THẮNG VÁN", use_container_width=True):
                        st.session_state.fibo_index = max(0, st.session_state.fibo_index - 2)
                        st.session_state.martingale_step = 1
                        st.rerun()
                    if f_lose.button("👎 THUA VÁN", use_container_width=True):
                        st.session_state.fibo_index += 1
                        st.session_state.martingale_step += 1
                        st.rerun()

            st.markdown("---")
            
            if not st.session_state.edge_history_df.empty:
                st.markdown("### 📈 Biểu Đồ Thực Thời Biên Độ Lợi Thế")
                st.line_chart(st.session_state.edge_history_df.set_index("Ván"))

            total_shoe_cards = decks * 52
            cards_used_calc = total_shoe_cards - cards_left
            penetration_rate = min(100.0, (cards_used_calc / total_shoe_cards) * 100)
            st.markdown(f"**Độ vơi khay bài thực tế (Shoe Penetration): {round(penetration_rate, 1)}%**")
            st.progress(penetration_rate / 100.0)

            with st.expander("📊 Kiểm toán chi tiết số lượng bài còn lại"):
                st.write(f"Tổng số bài còn lại trong máy chia: **{int(cards_left)} / {total_shoe_cards}** lá.")
                cols = st.columns(5)
                labels_13 = {1: "A", 11: "J", 12: "Q", 13: "K"}
                for idx, (num, cnt) in enumerate(remaining_deck.items()):
                    card_label = labels_13.get(num, f"[{num}]")
                    cols[idx % 5].text(f"{card_label}: {round(cnt, 1)} lá")
    else:
        st.info("🔮 Đang chờ nạp dữ liệu. Vui lòng nhập chi tiết quân bài bên dưới để kích hoạt lõi v12.0.")

st.markdown("---")

# --- DATA INPUT ENGINE ---
head_col, status_col = st.columns([2, 1])
with head_col: st.subheader("🃏 Nạp Dữ Liệu Phân Tích")
with status_col: st.markdown(f"<div style='text-align: right; margin-top: 10px; font-weight: bold; color: #ff4b4b;'>#Mã ván bài: {display_game}</div>", unsafe_allow_html=True)

col_p, col_b = st.columns(2)
with col_p: p_input = st.text_input("PLAYER CARDS (Lá bài):", value="", placeholder="Ví dụ: 5,K,2", disabled=is_data_discrepancy)
with col_b: b_input = st.text_input("BANKER CARDS (Lá bài):", value="", placeholder="Ví dụ: J,7", disabled=is_data_discrepancy)

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
            if normalized[i:i+2] == "10":
                tokens.append("10")
                i += 2
            elif normalized[i] in "23456789AJQK":
                tokens.append(normalized[i])
                i += 1
            else: i += 1
                
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    result_list = []
    for tok in tokens:
        if tok in mapping: result_list.append(mapping[tok])
        elif tok.isdigit():
            val = int(tok)
            if 2 <= val <= 10: result_list.append(val)
    return result_list

# --- ACTION TRIGGER ---
btn_trigger = st.button("🚀 KÍCH HOẠT HỆ THỐNG V12.0 QUANTUM ENGINE", use_container_width=True, type="primary", disabled=is_data_discrepancy)

if btn_trigger and not is_data_discrepancy:
    current_game_signature = f"P:{p_input.strip().upper()}|B:{b_input.strip().upper()}"
    
    if not p_input.strip() and not b_input.strip():
        st.warning("⚠️ Vui lòng nhập thông tin lá bài để chạy thuật toán.")
    elif current_game_signature == st.session_state.last_played_cards:
        st.error("⛔ PHÁT HIỆN TRÙNG LẶP: Dữ liệu ván bài này đã được nạp trước đó!")
    else:
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        
        if p_list or b_list:
            p_calc = p_list[:2]
            b_calc = b_list[:2]
            
            core_output = calculate_baccarat_v12_core(
                p_calc, b_calc, st.session_state.shoe_history, shoe_decks=decks,
                manual_cards_used=manual_cards, manual_games_played=manual_games,
                p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input,
                is_super6=is_super6_rule
            )
            
            if isinstance(core_output, str):
                st.session_state.last_results = (core_output, {}, 0.0, 0.0, "LỖI", 0)
            else:
                res, remaining_deck, p_pair, b_pair, mode, cards_left = core_output
                st.session_state.last_results = (res, p_pair, b_pair, remaining_deck, mode, cards_left)
                
                if not mode.startswith("LỖI"):
                    st.session_state.last_played_cards = current_game_signature
                    all_added = p_list + b_list
                    st.session_state.shoe_history.extend(all_added)
                    st.session_state.last_cards_added.append(all_added)
                    
                    final_p_score = sum([0 if c >= 10 else c for c in p_list]) % 10
                    final_b_score = sum([0 if c >= 10 else c for c in b_list]) % 10
                    win_side = "Player" if final_p_score > final_b_score else ("Banker" if final_b_score > final_p_score else "Tie")
                    st.session_state.outcome_history.append(win_side)
                    
                    actual_index = display_game + 1
                    new_edge_row = pd.DataFrame([{
                        "Ván": f"V{actual_index}",
                        "Player_Edge": res['Player'],
                        "Banker_Edge": res['Banker']
                    }])
                    st.session_state.edge_history_df = pd.concat([st.session_state.edge_history_df, new_edge_row], ignore_index=True)
                    
                    st.session_state.live_logs.append(f"Ván {actual_index}: Player({p_input.strip()}) -> {final_p_score}đ vs Banker({b_input.strip()}) -> {final_b_score}đ | Thắng: {win_side.upper()}")
                    st.session_state.game_counter = display_game + 1
                    st.rerun()

if st.session_state.live_logs and not is_data_discrepancy:
    st.markdown("---")
    with st.expander("📝 Nhật ký khay bài thời gian thực (Live Shoe Logs)", expanded=True):
        for log in reversed(st.session_state.live_logs): st.text(log)
