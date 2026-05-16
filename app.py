import streamlit as st
import pandas as pd
import numpy as np
import threading
from queue import Queue

# =========================================================================
# SYSTEM CORE v13.0: ASYNC MULTITHREADED MULTI-VARIABLE BAYESIAN CORE
# =========================================================================

# Sử dụng hàng đợi và đa luồng để cô lập hoàn toàn tác vụ tính toán nặng
def _async_calculation_worker(q_in, q_out):
    while True:
        data = q_in.get()
        if data is None: break
        
        p_cards, b_cards, shoe_history, shoe_decks, is_super6 = data
        total_initial_cards = shoe_decks * 52
        deck_structure = np.full(14, float(4 * shoe_decks))
        deck_structure[0] = 0.0
        
        # Khấu trừ đồng bộ hóa tốc độ cao
        for card_val in shoe_history:
            if 1 <= card_val <= 13 and deck_structure[card_val] > 0:
                deck_structure[card_val] -= 1
                
        cards_left = float(np.sum(deck_structure))
        
        if cards_left <= 6:
            q_out.put(("⚠️ Khay bài đã vơi quá giới hạn an toàn!", {}, 0.0, 0.0, "EXHAUSTED", cards_left))
            continue
            
        # Tính toán Hypergeometric nâng cao cho Cửa Đôi
        p_pair_prob = np.sum([(c / cards_left) * ((c - 1) / (cards_left - 1)) for c in deck_structure[1:14] if c >= 2])
        p_pair_odds = round(p_pair_prob * 100, 2)

        b_pair_prob = 0.0
        if cards_left > 3:
            for b_count in deck_structure[1:14]:
                if b_count >= 2:
                    p_rem_0 = ((cards_left - b_count) / cards_left) * ((cards_left - b_count - 1) / (cards_left - 1))
                    p_rem_1 = 2 * (b_count / cards_left) * ((cards_left - b_count) / (cards_left - 1))
                    p_rem_2 = (b_count / cards_left) * ((b_count - 1) / (cards_left - 1))
                    b_pair_prob += (p_rem_0 * (b_count / (cards_left - 2)) * ((b_count - 1) / (cards_left - 3)) +
                                    p_rem_1 * (max(0.0, b_count - 1) / (cards_left - 2)) * (max(0.0, b_count - 2) / (cards_left - 3)) +
                                    p_rem_2 * (max(0.0, b_count - 2) / (cards_left - 2)) * (max(0.0, b_count - 3) / (cards_left - 3)))
        b_pair_odds = round(b_pair_prob * 100, 2)

        # Chuyển đổi sang hệ điểm Baccarat (0-9)
        score_deck = np.zeros(10)
        for num in range(1, 14):
            score_deck[0 if num >= 10 else num] += deck_structure[num]

        # Khấu trừ bài trên bàn ngay lập tức
        for card in p_cards + b_cards:
            val = 0 if card >= 10 else card
            if score_deck[val] > 0: score_deck[val] -= 1

        p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
        b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

        # Kiểm tra Natural thắng trắng
        if p_score >= 8 or b_score >= 8:
            res = {"Player": 100.0, "Banker": 0.0, "Tie": 0.0} if p_score > b_score else ({"Player": 0.0, "Banker": 100.0, "Tie": 0.0} if b_score > p_score else {"Player": 0.0, "Banker": 0.0, "Tie": 100.0})
            q_out.put((res, {i: float(deck_structure[i]) for i in range(1, 14)}, p_pair_odds, b_pair_odds, "NATURAL_LOCK", cards_left))
            continue

        current_sum = float(np.sum(score_deck))
        player_wins, banker_wins, ties = 0.0, 0.0, 0.0

        # Khối Tích Chập Vector Phụ Thuộc Đồng Thời (Convolution Engine)
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
                
                b_draws = (b_score <= 2) or (b_score == 3 and card3_p != 8) or (b_score == 4 and card3_p in [2,3,4,5,6,7]) or (b_score == 5 and card3_p in [4,5,6,7]) or (b_score == 6 and card3_p in [6,7])
                
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
        out_deck = {i: float(deck_structure[i]) for i in range(1, 14)}
        q_out.put((odds_res, out_deck, p_pair_odds, b_pair_odds, "OMNISCIENT_THREAD_ACTIVE v13.0", cards_left))

# Khởi tạo Worker Thread chạy ngầm tránh xung đột CPU của UI
if 'worker_initialized' not in st.session_state:
    st.session_state.q_in = Queue()
    st.session_state.q_out = Queue()
    st.session_state.worker_thread = threading.Thread(
        target=_async_calculation_worker, 
        args=(st.session_state.q_in, st.session_state.q_out), 
        daemon=True
    )
    st.session_state.worker_thread.start()
    st.session_state.worker_initialized = True

# =========================================================================
# LÕI PHÂN TÍCH HIỆP BIẾN PHÂN PHỐI (BAYES COVARIANCE ENGINE)
# =========================================================================
def analyze_advanced_covariance(shoe_history, outcome_history):
    if len(shoe_history) < 10:
        return "⚖️ KHỞI TẠO MA TRẬN", "Đang tích lũy mật độ phân phối bài để quét Hiệp Biến Biến Động.", "Normal"
        
    # Tính toán độ lệch phân phối (Biên độ lệch khối bài lớn/nhỏ)
    cards_np = np.array(shoe_history)
    low_cards_ratio = np.sum((cards_np >= 1) & (cards_np <= 5)) / len(shoe_history)
    
    last_outcome = outcome_history[-1] if outcome_history else "Normal"
    streak_len = 0
    for out in reversed(outcome_history):
        if out == last_outcome: streak_len += 1
        else: break

    if low_cards_ratio > 0.45:
        return "💥 HIỆP BIẾN LỆCH KHỐI (BÀI NHỎ TỤ TẬP)", "Khay bài đang bị bão hòa bởi các quân bài từ 1-5. Xu hướng kéo lá thứ 3 có lợi thế cực lớn cho các thế bài lội ngược dòng.", "Warning"
    if streak_len >= 4:
        return "⚠️ CẢNH BÁO BỆT DÂY VẬT LÝ", f"Cửa **{last_outcome.upper()}** đang dính bệt chuỗi dài **{streak_len} ván**. Không thực hiện hành vi bẻ dòng tiền.", "High_Streak"
        
    return "⚖️ KHAY BÀI CÂN BẰNG ĐA BIẾN", "Mật độ phân bổ bài đồng đều, sai số ngẫu nhiên nằm trong tầm kiểm soát lý thuyết.", "Normal"

# =========================================================================
# STREAMLIT UI ARCHITECTURE DESIGN
# =========================================================================
st.set_page_config(page_title="Oracle Omniscient Singularity v13.0", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stColumn"] { width: 50% !important; min-width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

# Hệ thống lưu trữ dữ liệu State an toàn tuyệt đối chống F5 Crash
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

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("🔮 SINGULARITY CONTROL PANEL")
decks = st.sidebar.selectbox("Số bộ bài quy chuẩn của sòng:", [8, 6, 4], index=0)
is_super6_rule = st.sidebar.checkbox("Bàn Super 6 (Không hoa hồng - Banker 6 điểm ăn nửa)", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💰 LÕI QUẢN TRỊ DÒNG VỐN THÍCH ỨNG")
capital_strategy = st.sidebar.selectbox(
    "Thuật toán quản lý vốn thích ứng:",
    ["Kelly Thích Ứng (Tối ưu EV Ròng)", "Fibonacci Động (An toàn cao)", "Martingale Tuyệt Đối"]
)
base_bet = st.sidebar.number_input("Giá trị cược gốc (1 Đơn vị - VNĐ):", min_value=10000, value=50000, step=10000)

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

if st.sidebar.button("🔄 RESET KHAY BÀI TOÀN PHẦN", use_container_width=True):
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

display_game = len(st.session_state.live_logs)

# --- PANEL DISPLAY SCREEN ---
if st.session_state.last_results:
    results_data = st.session_state.last_results
    
    if isinstance(results_data[0], str) and results_data[0].startswith("⚠️"):
        st.warning(results_data[0])
    else:
        res, p_pair, b_pair, remaining_deck, current_mode, cards_left = results_data
        
        left_result_col, right_pair_col = st.columns(2)
        with left_result_col:
            st.markdown("#### 📊 Phân Tích Cửa Chính")
            st.metric("🔵 PLAYER WIN", f"{res['Player']}%")
            st.metric("🔴 BANKER WIN", f"{res['Banker']}%")
            st.metric("🟢 TIE WIN", f"{res['Tie']}%")
            st.progress(res['Banker'] / 100 if res['Banker'] > 0 else 0)
            
        with right_pair_col:
            st.markdown("#### 💎 Phân Tích Cửa Đôi")
            st.metric("🔵 CON ĐÔI (P PAIR)", f"{p_pair}%", delta="🔥 LỢI THẾ LỚN" if p_pair > 7.47 else "⚖️ BÌNH THƯỜNG")
            st.metric("🔴 CÁI ĐÔI (B PAIR)", f"{b_pair}%", delta="🔥 LỢI THẾ LỚN" if b_pair > 7.47 else "⚖️ BÌNH THƯỜNG")

        st.markdown("---")
        
        # Phân tích Hiệp biến Bayes nâng cao
        st.markdown("### 🧬 Quét Trạng Thái Hiệp Biến Hệ Thống")
        trend_title, trend_desc, trend_level = analyze_advanced_covariance(st.session_state.shoe_history, st.session_state.outcome_history)
        if trend_level == "Warning": st.warning(f"**{trend_title}** \n\n {trend_desc}")
        elif trend_level == "High_Streak": st.error(f"**{trend_title}** \n\n {trend_desc}")
        else: st.success(f"**{trend_title}** \n\n {trend_desc}")

        st.markdown("---")
        
        # Quản lý dòng tiền thông minh tích hợp trừ hao hụt hoa hồng thực tế (True Net EV)
        st.markdown(f"### 💰 Phân Phối Lệnh Vào Tiền Thích Ứng ({capital_strategy})")
        k_col1, k_col2 = st.columns(2)
        max_side = "Player" if res['Player'] > res['Banker'] else "Banker"
        max_prob = res[max_side] / 100.0
        
        b_factor = 1.00 if is_super6_rule else (0.95 if max_side == "Banker" else 1.00)
        q_factor = 1.0 - max_prob
        kelly_per = ((b_factor * max_prob) - q_factor) / b_factor * 100
        kelly_per = max(0.0, kelly_per)
        
        fibo_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        idx_fibo = min(st.session_state.fibo_index, len(fibo_sequence)-1)
        fibo_unit = fibo_sequence[idx_fibo]
        
        martingale_unit = 2 ** (st.session_state.martingale_step - 1)

        with k_col1:
            if res['Player'] == 100.0 or res['Banker'] == 100.0:
                st.success(f"🎯 LỆNH TUYỆT ĐỐI: Vào thẳng cửa **{max_side.upper()}**")
            elif "Kelly" in capital_strategy:
                if kelly_per > 0.1:
                    safe_investment = round(kelly_per / 4, 2)
                    if safe_investment >= 0.25:
                        st.info(f"✨ ĐỀ XUẤT VÀO: Đặt **{max_side.upper()}**\n\n💵 Quy mô quỹ: **{safe_investment}%**")
                    else:
                        st.warning("⚖️ LỢI NHUẬN RÒNG QUÁ THẤP -> BỎ QUA VÁN NÀY.")
                else:
                    st.warning("⚖️ TRẠNG THÁI KHÔNG LỢI THẾ (EV ÂM) -> BỎ QUA VÁN NÀY.")
            elif "Fibonacci" in capital_strategy:
                st.info(f"✨ ĐỀ XUẤT VÀO: Đặt **{max_side.upper()}**\n\n💵 Cược: **{fibo_unit} Đơn vị** ({fibo_unit * base_bet:,} VNĐ)")
            elif "Martingale" in capital_strategy:
                st.info(f"✨ ĐỀ XUẤT VÀO: Đặt **{max_side.upper()}**\n\n💵 Cược: **{martingale_unit} Đơn vị** ({martingale_unit * base_bet:,} VNĐ)")
                
        with k_col2:
            st.caption(f"Engine xử lý độc lập:\n{current_mode}")
            if "Fibonacci" in capital_strategy or "Martingale" in capital_strategy:
                st.markdown("**Xác nhận kết quả ván thực tế:**")
                f_win, f_lose = st.columns(2)
                if f_win.button("👍 THẮNG VÁN VỪA RỒI", use_container_width=True):
                    st.session_state.fibo_index = max(0, st.session_state.fibo_index - 2)
                    st.session_state.martingale_step = 1
                    st.rerun()
                if f_lose.button("👎 THUA VÁN VỪA RỒI", use_container_width=True):
                    st.session_state.fibo_index += 1
                    st.session_state.martingale_step += 1
                    st.rerun()

        st.markdown("---")
        
        if not st.session_state.edge_history_df.empty:
            st.markdown("### 📈 Biểu Đồ Diễn Biến Biên Độ Lợi Thế Thực Thời")
            st.line_chart(st.session_state.edge_history_df.set_index("Ván"))

        total_shoe_cards = decks * 52
        cards_used_calc = total_shoe_cards - cards_left
        penetration_rate = min(100.0, (cards_used_calc / total_shoe_cards) * 100)
        st.markdown(f"**Độ chín khay bài hiện tại (Shoe Penetration): {round(penetration_rate, 1)}%**")
        st.progress(penetration_rate / 100.0)

        with st.expander("📊 Kiểm toán chi tiết số lượng bài còn lại"):
            st.write(f"Số lượng quân bài vật lý còn lại trong khay: **{int(cards_left)} / {total_shoe_cards}** lá.")
            cols = st.columns(5)
            labels_13 = {1: "A", 11: "J", 12: "Q", 13: "K"}
            for idx, (num, cnt) in enumerate(remaining_deck.items()):
                card_label = labels_13.get(num, f"[{num}]")
                cols[idx % 5].text(f"{card_label}: {round(cnt, 1)} lá")
else:
    st.info("🔮 Đang chờ nạp tín hiệu. Nhập dữ liệu chi tiết các quân bài bên dưới để kích hoạt lõi v13.0.")

st.markdown("---")

# --- DATA INPUT ROW ---
head_col, status_col = st.columns([2, 1])
with head_col: st.subheader("🃏 Nạp Dữ Liệu Phân Tích Ván")
with status_col: st.markdown(f"<div style='text-align: right; margin-top: 10px; font-weight: bold; color: #ff4b4b;'>#Mã ván: {display_game}</div>", unsafe_allow_html=True)

col_p, col_b = st.columns(2)
with col_p: p_input = st.text_input("PLAYER CARDS (Điểm):", value="", placeholder="Ví dụ: 5,K,2")
with col_b: b_input = st.text_input("BANKER CARDS (Điểm):", value="", placeholder="Ví dụ: J,7")

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
btn_trigger = st.button("🚀 KÍCH HOẠT LÕI TỐI HẬU V13.0 SINGULARITY CORE", use_container_width=True, type="primary")

if btn_trigger:
    current_game_signature = f"P:{p_input.strip().upper()}|B:{b_input.strip().upper()}"
    
    if not p_input.strip() and not b_input.strip():
        st.warning("⚠️ Hệ thống yêu cầu nạp quân bài để thực hiện phép toán tính chập.")
    elif current_game_signature == st.session_state.last_played_cards:
        st.error("⛔ ĐÃ CHẶN: Dữ liệu ván này trùng lặp với ván vừa tính!")
    else:
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        
        if p_list or b_list:
            p_calc = p_list[:2]
            b_calc = b_list[:2]
            
            # Gửi dữ liệu vào luồng tính toán ngầm tránh gây treo UI ứng dụng
            st.session_state.q_in.put((p_calc, b_calc, st.session_state.shoe_history, decks, is_super6_rule))
            
            # Chờ lấy kết quả từ luồng tính toán độc lập
            core_output = st.session_state.q_out.get()
            
            if isinstance(core_output[0], str) and "⚠️" in core_output[0]:
                st.session_state.last_results = (core_output[0], {}, 0.0, 0.0, "EXHAUSTED", 0)
            else:
                res, remaining_deck, p_pair, b_pair, mode, cards_left = core_output
                st.session_state.last_results = (res, p_pair, b_pair, remaining_deck, mode, cards_left)
                
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

if st.session_state.live_logs:
    st.markdown("---")
    with st.expander("📝 Nhật ký khay bài thời gian thực (Live Shoe Logs)", expanded=True):
        for log in reversed(st.session_state.live_logs): st.text(log)
