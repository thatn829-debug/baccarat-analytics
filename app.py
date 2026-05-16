import streamlit as st
import pandas as pd
import numpy as np
import threading
from queue import Queue

# =========================================================================
# SYSTEM CORE v20.0: OMNISCIENT SENTINEL KERNEL (ZERO-MUTATION MEMORY)
# =========================================================================

def _singularity_core_worker(q_in, q_out):
    # Cấp phát mảng tĩnh nguyên thủy một lần duy nhất tại tầng lõi phần cứng
    deck_structure = np.zeros(14, dtype=np.float64)
    score_deck = np.zeros(10, dtype=np.float64)
    
    while True:
        data = q_in.get()
        if data is None: break
        
        p_cards, b_cards, shoe_history, shoe_decks, is_super6 = data
        
        # Reset mảng tĩnh không thông qua cấp phát mới (Zero-Mutation Allocation)
        deck_structure.fill(float(4 * shoe_decks))
        deck_structure[0] = 0.0
        
        for card_val in shoe_history:
            if 1 <= card_val <= 13 and deck_structure[card_val] > 0:
                deck_structure[card_val] -= 1.0
                
        cards_left = float(np.sum(deck_structure))
        if cards_left <= 6:
            q_out.put(("⚠️ TERMINAL CRITICAL: Khay bài đã chạm giới hạn vật lý!", {}, 0.0, 0.0, "DEAD_SHOE", cards_left, 0.0))
            continue
            
        # Xác suất Siêu hình học Khóa đôi (Hypergeometric Anchor Matrix)
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

        score_deck.fill(0.0)
        for num in range(1, 14):
            score_deck[0 if num >= 10 else num] += deck_structure[num]

        for card in p_cards + b_cards:
            val = 0 if card >= 10 else card
            if score_deck[val] > 0: score_deck[val] -= 1.0

        p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
        b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

        if p_score >= 8 or b_score >= 8:
            res = {"Player": 100.0, "Banker": 0.0, "Tie": 0.0} if p_score > b_score else ({"Player": 0.0, "Banker": 100.0, "Tie": 0.0} if b_score > p_score else {"Player": 0.0, "Banker": 0.0, "Tie": 100.0})
            q_out.put((res, {i: float(deck_structure[i]) for i in range(1, 14)}, p_pair_odds, b_pair_odds, "OMNISCIENT_NATURAL_LOCK", cards_left, 0.0))
            continue

        current_sum = float(np.sum(score_deck))
        player_wins, banker_wins, ties = 0.0, 0.0, 0.0

        # Tích chập ma trận Markov mật độ cao không đồng bộ
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
        
        probs_entropy = score_deck[score_deck > 0] / np.sum(score_deck)
        system_entropy = -np.sum(probs_entropy * np.log2(probs_entropy))

        out_deck = {i: float(deck_structure[i]) for i in range(1, 14)}
        q_out.put((odds_res, out_deck, p_pair_odds, b_pair_odds, "OMNISCIENT CORE v20.0", cards_left, system_entropy))

if 'singularity_initialized' not in st.session_state:
    st.session_state.q_in_v20 = Queue()
    st.session_state.q_out_v20 = Queue()
    st.session_state.singularity_thread = threading.Thread(
        target=_singularity_core_worker, 
        args=(st.session_state.q_in_v20, st.session_state.q_out_v20), 
        daemon=True
    )
    st.session_state.singularity_thread.start()
    st.session_state.singularity_initialized = True

# =========================================================================
# RADAR ĐO LƯỜNG BIẾN ĐỘNG ENTROPY SHANNON
# =========================================================================
def analyze_singularity_density(shoe_history, outcome_history):
    clean_outcomes = [o for o in outcome_history if o != "Tie"]
    if len(clean_outcomes) < 3:
        return "⚖️ INITIALIZING STREAM", "Hệ thống đang thiết lập cấu trúc nền.", "Normal"
        
    last_side = clean_outcomes[-1]
    streak = 0
    for o in reversed(clean_outcomes):
        if o == last_side: streak += 1
        else: break

    if len(shoe_history) >= 10:
        recent_cards = np.array(shoe_history[-10:])
        high_density = np.sum(recent_cards >= 10) / 10
        if high_density > 0.50:
            return "🚨 DENSITY OVERFLOW: BÃO HÒA HÌNH HỌC", "Mật độ bài Tây vượt ngưỡng an toàn. Khuyên bạn nên dừng lại nhìn hoặc hạ cược.", "Critical_Alert"

    if streak >= 4:
        return "⚠️ STREAK DETECTED: PHÁT HIỆN CẦU BỆT DÀI", f"Cửa **{last_side.upper()}** đang duy trì chuỗi bệt dài **{streak} ván**. Tuyệt đối không cược chặn bẻ cầu.", "Streak_Alert"
        
    return "⚖️ ABSOLUTE STABLE", "Hệ thống đang ở vùng phân phối chuẩn lý tưởng.", "Normal"

# =========================================================================
# OMNI-FORMAT HIGH SPEED PARSER
# =========================================================================
def fast_tokenizer(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().replace(" ", "")
    if "," in normalized:
        parts = normalized.split(",")
        tokens = [p for p in parts if p in ["2","3","4","5","6","7","8","9","10","A","J","Q","K"]]
    else:
        tokens = []
        i = 0
        while i < len(normalized):
            if normalized[i:i+2] == "10":
                tokens.append("10")
                i += 2
            elif normalized[i] in "23456789AJQK":
                tokens.append(normalized[i])
                i += 1
            else: i += 1
                
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    return [mapping[t] if t in mapping else int(t) for t in tokens]

# =========================================================================
# EXECUTIVE MONOLITHIC HUD DESIGN
# =========================================================================
st.set_page_config(page_title="Omniscient Engine v20.0", page_icon="⚡", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stColumn"] { width: 50% !important; min-width: 50% !important; flex: 1 1 50% !important; padding: 1px !important; }
    h4 { margin-bottom: -18px !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

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

# --- CONTROL SIDEBAR ---
st.sidebar.header("⚡ OMNISCIENT SYSTEMS v20.0")
decks = st.sidebar.selectbox("Số lượng bộ bài khay:", [8, 6, 4], index=0)
is_super6_rule = st.sidebar.checkbox("Luật bàn chơi Super 6 nâng cao", value=False)

st.sidebar.markdown("---")
capital_strategy = st.sidebar.selectbox(
    "Chiến thuật quản lý dòng tiền:",
    ["Omniscient Kelly (Tối ưu EV)", "Fibonacci Tiến Cấp An Toàn", "Martingale Khóa Biên Trần Cược"]
)
base_bet = st.sidebar.number_input("Tiền cược cơ sở (VNĐ):", min_value=10000, value=50000, step=10000)
table_max_limit = st.sidebar.number_input("Giới hạn tối đa bàn cược (VNĐ):", min_value=1000000, value=50000000, step=5000000)

st.sidebar.markdown("---")
if st.session_state.live_logs:
    if st.sidebar.button("↩️ HOÀN TÁC VÁN GẦN NHẤT", use_container_width=True):
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

if st.sidebar.button("🔄 TRANSCENDENTAL PURGE DATA", use_container_width=True):
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

# --- PANEL METRIC MONITOR HUD ---
if st.session_state.last_results:
    results_data = st.session_state.last_results
    if isinstance(results_data[0], str) and "⚠️" in results_data[0]:
        st.error(results_data[0])
    else:
        res, p_pair, b_pair, remaining_deck, current_mode, cards_left, entropy_val = results_data
        
        col_m, col_p = st.columns(2)
        with col_m:
            st.markdown("#### 📊 Tỷ Lệ Xác Suất Real-time")
            st.metric("🔵 PLAYER WIN", f"{res['Player']}%")
            st.metric("🔴 BANKER WIN", f"{res['Banker']}%")
            st.metric("🟢 TIE WIN", f"{res['Tie']}%")
            st.progress(res['Banker'] / 100.0 if res['Banker'] > 0 else 0.0)
        with col_p:
            st.markdown("#### 💎 Biên Độ Lợi Thế Cửa Đôi")
            st.metric("🔵 P PAIR", f"{p_pair}%", delta="🔥 KHAI THÁC TỐT" if p_pair > 7.47 else "⚖️ CHƯA ĐỦ BIÊN")
            st.metric("🔴 B PAIR", f"{b_pair}%", delta="🔥 KHAI THÁC TỐT" if b_pair > 7.47 else "⚖️ CHƯA ĐỦ BIÊN")

        st.markdown("---")
        st.markdown("### 🧬 Hệ Thống Cảnh Báo An Toàn Khay Bài (Entropy Radar)")
        trend_title, trend_desc, trend_level = analyze_singularity_density(st.session_state.shoe_history, st.session_state.outcome_history)
        if trend_level == "Critical_Alert": st.error(f"**{trend_title}** \n\n {trend_desc}")
        elif trend_level == "Streak_Alert": st.warning(f"**{trend_title}** \n\n {trend_desc}")
        else: st.success(f"**{trend_title}** \n\n {trend_desc}")

        st.markdown("---")
        st.markdown(f"### 💰 Kế Hoạch Đi Vốn Thông Minh Đề Xuất")
        k_col1, k_col2 = st.columns(2)
        max_side = "Player" if res['Player'] > res['Banker'] else "Banker"
        max_prob = res[max_side] / 100.0
        
        b_factor = 1.00 if is_super6_rule else (0.95 if max_side == "Banker" else 1.00)
        q_factor = 1.0 - max_prob
        kelly_per = ((b_factor * max_prob) - q_factor) / b_factor * 100
        kelly_per = max(0.0, kelly_per)
        
        fibo_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        fibo_unit = fibo_sequence[min(st.session_state.fibo_index, len(fibo_sequence)-1)]
        martingale_unit = 2 ** (st.session_state.martingale_step - 1)

        with k_col1:
            if res['Player'] == 100.0 or res['Banker'] == 100.0:
                st.success(f"🎯 PHÁN QUYẾT TUYỆT ĐỐI: Đặt cửa **{max_side.upper()}**")
            elif "Kelly" in capital_strategy:
                if kelly_per > 0.1 and trend_level != "Critical_Alert":
                    safe_investment = round(kelly_per / 4, 2)
                    if safe_investment >= 0.25: st.info(f"✨ LỆNH PHÂN BỔ: Đặt **{max_side.upper()}**\n\n💵 Quy mô cược đề xuất: **{safe_investment}%** Tài khoản.")
                    else: st.warning("⚖️ LỢI NHUẬN KỲ VỌNG QUÁ THẤP -> BỎ QUA VÁN NÀY.")
                else: st.warning("⚖️ EV ÂM HOẶC KHAY BÀI NHIỄU SÓNG -> TUYỆT ĐỐI BỎ QUA VÁN NÀY.")
            elif "Fibonacci" in capital_strategy:
                current_total_bet = fibo_unit * base_bet
                if current_total_bet > table_max_limit * 0.85:
                    st.error(f"🚨 HỆ THỐNG PHANH CƯỢC: Tiền cược ({current_total_bet:,} VNĐ) chạm ngưỡng trần rủi ro!")
                else: st.info(f"✨ LỆNH PHÂN BỔ: Đặt **{max_side.upper()}**\n\n💵 Số tiền: **{fibo_unit} Đơn vị** ({current_total_bet:,} VNĐ)")
            elif "Martingale" in capital_strategy:
                current_total_bet = martingale_unit * base_bet
                if current_total_bet > table_max_limit * 0.85:
                    st.error(f"🚨 HỆ THỐNG PHANH CƯỢC: Tiền cược ({current_total_bet:,} VNĐ) chạm ngưỡng trần rủi ro!")
                else: st.info(f"✨ LỆNH PHÂN BỔ: Đặt **{max_side.upper()}**\n\n💵 Số tiền: **{martingale_unit} Đơn vị** ({current_total_bet:,} VNĐ)")
                
        with k_col2:
            st.caption(f"Lõi xử lý: {current_mode}")
            if entropy_val > 0: st.caption(f"Shannon Entropy: {round(entropy_val, 4)}")
            if "Fibonacci" in capital_strategy or "Martingale" in capital_strategy:
                st.markdown("**Xác nhận kết quả thực tế:**")
                f_win, f_lose = st.columns(2)
                if f_win.button("👍 THẮNG", use_container_width=True):
                    st.session_state.fibo_index = max(0, st.session_state.fibo_index - 2)
                    st.session_state.martingale_step = 1
                    st.rerun()
                if f_lose.button("👎 THUA", use_container_width=True):
                    st.session_state.fibo_index += 1
                    st.session_state.martingale_step += 1
                    st.rerun()

        st.markdown("---")
        if not st.session_state.edge_history_df.empty:
            st.markdown("### 📈 Biểu Đồ Lợi Thế Khay Bài")
            st.line_chart(st.session_state.edge_history_df.set_index("Ván"))

        total_shoe_cards = decks * 52
        cards_used_calc = total_shoe_cards - cards_left
        penetration_rate = min(100.0, (cards_used_calc / total_shoe_cards) * 100)
        st.markdown(f"**Độ vơi khay bài thực tế (Shoe Penetration): {round(penetration_rate, 1)}%**")
        st.progress(penetration_rate / 100.0)

        with st.expander("📊 Kiểm toán chi tiết số lượng bài vật lý còn lại"):
            cols = st.columns(5)
            labels_13 = {1: "A", 11: "J", 12: "Q", 13: "K"}
            for idx, (num, cnt) in enumerate(remaining_deck.items()):
                card_label = labels_13.get(num, f"[{num}]")
                cols[idx % 5].text(f"{card_label}: {round(cnt, 1)} lá")
else:
    st.info("🔮 Hệ thống tối cao đang trực tuyến. Nhập chuỗi bài viết liền bên dưới để phân tích.")

st.markdown("---")

# =========================================================================
# DYNAMIC ZERO-KEYPRESS ENGINE (REACTIVE TOKENIZER)
# =========================================================================
head_col, status_col = st.columns([2, 1])
with head_col: st.subheader("🃏 Nạp Chuỗi Bài Tốc Độ Cao")
with status_col: st.markdown(f"<div style='text-align: right; margin-top: 10px; font-weight: bold; color: #ff4b4b;'>#Mã ván: {display_game}</div>", unsafe_allow_html=True)

col_p, col_b = st.columns(2)
p_input = st.text_input("PLAYER CARDS (Ví dụ: 7K2 hoặc 7,K,2):", value="")
b_input = st.text_input("BANKER CARDS (Ví dụ: Q9 hoặc Q,9):", value="")

# Cơ chế tự động kích hoạt ngầm không qua nút bấm
if p_input.strip() or b_input.strip():
    current_game_signature = f"P:{p_input.strip().upper()}|B:{b_input.strip().upper()}"
    
    if current_game_signature != st.session_state.last_played_cards:
        p_list = fast_tokenizer(p_input)
        b_list = fast_tokenizer(b_input)
        
        # Chỉ kích hoạt xử lý khi dữ liệu đầu vào hợp lệ (Tối thiểu 2 lá mỗi bên)
        if len(p_list) >= 2 or len(b_list) >= 2:
            p_calc = p_list[:2]
            b_calc = b_list[:2]
            
            st.session_state.q_in_v20.put((p_calc, b_calc, st.session_state.shoe_history, decks, is_super6_rule))
            core_output = st.session_state.q_out_v20.get()
            
            if isinstance(core_output[0], str) and "⚠️" in core_output[0]:
                st.session_state.last_results = (core_output[0], {}, 0.0, 0.0, "EXHAUSTED", 0, 0.0)
            else:
                res, remaining_deck, p_pair, b_pair, mode, cards_left, entropy_val = core_output
                st.session_state.last_results = (res, p_pair, b_pair, remaining_deck, mode, cards_left, entropy_val)
                
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
    with st.expander("📝 Live Shoe Logs (Zero-Mutation Memory Stack)", expanded=True):
        for log in reversed(st.session_state.live_logs): st.text(log)
