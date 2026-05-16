import streamlit as st
import pandas as pd
import numpy as np

# =========================================================================
# SYSTEM CORE: v12.2 - COMBINATORICS WITH HIGH-PROBABILITY FOCUS
# =========================================================================

def calculate_ultra_precision_odds(p_cards, b_cards, shoe_history, total_decks, is_super6):
    initial_cards = {i: total_decks * 4 for i in range(1, 14)}
    for card in shoe_history:
        if card in initial_cards and initial_cards[card] > 0:
            initial_cards[card] -= 1

    base_cards_left = sum(initial_cards.values())
    if base_cards_left <= 6:
        return "CRITICAL_LIMIT", {}, 0.0, 0.0, base_cards_left

    p_pair_prob = 0.0
    for card_val, count in initial_cards.items():
        if count >= 2:
            p_pair_prob += (count / base_cards_left) * ((count - 1) / (base_cards_left - 1))
    p_pair_odds = round(p_pair_prob * 100, 2)

    b_pair_prob = 0.0
    for card_val, count in initial_cards.items():
        if count >= 2:
            b_pair_prob += (count / base_cards_left) * ((count - 1) / (base_cards_left - 1))
    b_pair_odds = round(b_pair_prob * 100, 2)

    active_deck = initial_cards.copy()
    for card in p_cards + b_cards:
        if card in active_deck and active_deck[card] > 0:
            active_deck[card] -= 1

    score_weights = {i: 0.0 for i in range(10)}
    for card_val, count in active_deck.items():
        score_val = 0 if card_val >= 10 else card_val
        score_weights[score_val] += float(count)

    cards_left_for_third = sum(score_weights.values())
    
    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, initial_cards, p_pair_odds, b_pair_odds, cards_left_for_third
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, initial_cards, p_pair_odds, b_pair_odds, cards_left_for_third
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, initial_cards, p_pair_odds, b_pair_odds, cards_left_for_third

    player_wins = 0.0
    banker_wins = 0.0
    ties = 0.0

    if p_score >= 6:
        if b_score <= 5:
            for card3_b, w_b in score_weights.items():
                if w_b > 0:
                    prob_b = w_b / cards_left_for_third
                    final_b = (b_score + card3_b) % 10
                    if p_score > final_b: player_wins += prob_b
                    elif final_b > p_score: banker_wins += prob_b
                    else: ties += prob_b
        else:
            if p_score > b_score: player_wins += 1.0
            elif b_score > p_score: banker_wins += 1.0
            else: ties += 1.0
    else:
        for card3_p, w_p in score_weights.items():
            if w_p <= 0: continue
            prob_p = w_p / cards_left_for_third
            final_p = (p_score + card3_p) % 10
            
            rem_cards_left = cards_left_for_third - 1.0
            if rem_cards_left <= 0: continue
            
            b_draws = False
            if b_score <= 2: b_draws = True
            elif b_score == 3 and card3_p != 8: b_draws = True
            elif b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]: b_draws = True
            elif b_score == 5 and card3_p in [4, 5, 6, 7]: b_draws = True
            elif b_score == 6 and card3_p in [6, 7]: b_draws = True
            
            if b_draws:
                for card3_b, w_b in score_weights.items():
                    actual_w_b = w_b - (1.0 if card3_b == card3_p else 0.0)
                    if actual_w_b > 0:
                        prob_b = actual_w_b / rem_cards_left
                        final_b = (b_score + card3_b) % 10
                        combined_weight = prob_p * prob_b
                        
                        if final_p > final_b: player_wins += combined_weight
                        elif final_b > final_p: banker_wins += combined_weight
                        else: ties += combined_weight
            else:
                if final_p > b_score: player_wins += prob_p
                elif b_score > final_p: banker_wins += prob_p
                else: ties += prob_p

    total_weight = player_wins + banker_wins + ties
    if total_weight == 0: total_weight = 1.0

    odds_result = {
        "Player": round((player_wins / total_weight) * 100, 2),
        "Banker": round((banker_wins / total_weight) * 100, 2),
        "Tie": round((ties / total_weight) * 100, 2)
    }
    
    return odds_result, initial_cards, p_pair_odds, b_pair_odds, cards_left_for_third

def parse_raw_cards(raw_string):
    if not raw_string: return []
    normalized = raw_string.upper().replace(" ", "")
    if "," in normalized:
        tokens = [p for p in normalized.split(",") if p in ["2","3","4","5","6","7","8","9","10","A","J","Q","K"]]
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
# GRAPHICAL INTERFACE
# =========================================================================
st.set_page_config(page_title="v12.2 Probability Focus", page_icon="🎯", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; }
    div[data-testid="stColumn"] { width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    .focus-box { background-color: #262730; padding: 12px; border-radius: 8px; border-left: 6px solid #f39c12; margin-bottom: 15px; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'live_logs' not in st.session_state: st.session_state.live_logs = []
if 'edge_history_df' not in st.session_state: st.session_state.edge_history_df = pd.DataFrame(columns=["Ván", "Player_Xác_Suất", "Thực_Tế_Ra"])
if 'last_cards_count' not in st.session_state: st.session_state.last_cards_count = []
if 'reverse_streak' not in st.session_state: st.session_state.reverse_streak = 0

# --- SIDEBAR PANEL ---
st.sidebar.header("⚙️ THIẾT LẬP KHAY BÀI")
decks = st.sidebar.selectbox("Số lượng bộ bài:", [8, 6, 4], index=0)
is_super6_rule = st.sidebar.checkbox("Bàn chơi Super 6", value=False)

st.sidebar.markdown("---")
if st.sidebar.button("↩️ HOÀN TÁC VÁN TRƯỚC", use_container_width=True):
    if st.session_state.live_logs:
        st.session_state.live_logs.pop()
        if not st.session_state.edge_history_df.empty:
            st.session_state.edge_history_df = st.session_state.edge_history_df.iloc[:-1]
        if st.session_state.last_cards_count:
            count_to_pop = st.session_state.last_cards_count.pop()
            if count_to_pop <= len(st.session_state.shoe_history):
                st.session_state.shoe_history = st.session_state.shoe_history[:-count_to_pop]
        st.session_state.reverse_streak = max(0, st.session_state.reverse_streak - 1)
        st.rerun()

if st.sidebar.button("🔄 LÀM MỚI KHAY BÀI (XÓA HẾT)", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.live_logs = []
    st.session_state.last_cards_count = []
    st.session_state.edge_history_df = pd.DataFrame(columns=["Ván", "Player_Xác_Suất", "Thực_Tế_Ra"])
    st.session_state.reverse_streak = 0
    st.rerun()

# --- MAIN HUD ---
st.title("🎯 v12.2 HIGH-PROBABILITY FOCUS")
st.caption("Phiên bản tự động bôi đậm và làm nổi bật cửa có lợi thế toán học cao hơn")

# RADAR QUÉT SÓNG NGƯỢC GIỮ NGUYÊN TỪ v12.1
if st.session_state.reverse_streak >= 3:
    st.error(f"🚨 **DIVERGENCE ALERT: KHAY BÀI ĐANG LOẠN NHỊP ({st.session_state.reverse_streak} VÁN NGƯỢC LIÊN TIẾP)**\n\nToán học cảnh báo cửa có tỷ lệ cao đang bị bẻ liên tục. **HÃY DỪNG ĐẶT CƯỢC ngay lập tức**, chỉ nhập bài để qua đoạn nhiễu.")
elif st.session_state.reverse_streak > 0:
    st.warning(f"⚠️ **CẢNH BÁO SÓNG NGƯỢC:** Phát hiện xu hướng lệch nhẹ ({st.session_state.reverse_streak} ván). Hãy cẩn thận.")
else:
    st.success("⚖️ **STABLE MARKET:** Khay bài phân phối chuẩn, kết quả đi sát với ma trận xác suất.")

st.markdown("### 🃏 Nhập Bài Ván Hiện Tại")
col_p, col_b = st.columns(2)
with col_p: p_input = st.text_input("PLAYER CARDS (Ví dụ: 7K):", value="", key="p_in")
with col_b: b_input = st.text_input("BANKER CARDS (Ví dụ: Q9):", value="", key="b_in")

p_list = parse_raw_cards(p_input)
b_list = parse_raw_cards(b_input)

if len(p_list) >= 2 or len(b_list) >= 2:
    calculation_output = calculate_ultra_precision_odds(p_list[:2], b_list[:2], st.session_state.shoe_history, decks, is_super6_rule)
    
    if calculation_output[0] == "CRITICAL_LIMIT":
        st.error("🚨 HẾT BÀI: Khay bài đã chạm giới hạn vật lý.")
    else:
        res, remaining_deck, p_pair, b_pair, cards_left = calculation_output
        
        # --- THUẬT TOÁN NHẤN MẠNH CỬA CÓ XÁC SUẤT CAO HƠN ---
        p_label, b_label = "🔵 PLAYER WIN", "🔴 BANKER WIN"
        diff = abs(res['Player'] - res['Banker'])
        
        if res['Player'] > res['Banker']:
            p_label = "👑 🔵 PLAYER WIN [CỬA TRÊN]"
            advice_html = f"<div class='focus-box'>🎯 <b>KHUYÊN CƯỢC:</b> Đặt vào <b>PLAYER</b> (Lợi thế cao hơn hẳn <b>+{diff}%</b> so với Banker)</div>"
        elif res['Banker'] > res['Player']:
            b_label = "👑 🔴 BANKER WIN [CỬA TRÊN]"
            advice_html = f"<div class='focus-box'>🎯 <b>KHUYÊN CƯỢC:</b> Đặt vào <b>BANKER</b> (Lợi thế cao hơn hẳn <b>+{diff}%</b> so với Player)</div>"
        else:
            advice_html = "<div class='focus-box'>⚖️ <b>CÂN BẰNG TUYỆT ĐỐI:</b> Tỷ lệ 50-50, không nên vào lệnh ván này.</div>"

        # Hiển thị thanh tiêu điểm khuyên cược lớn
        st.markdown(advice_html, unsafe_allow_html=True)

        st.markdown("---")
        hud1, hud2 = st.columns(2)
        with hud1:
            st.markdown("#### 📊 Xác Suất Thắng Dự Kiến")
            st.metric(p_label, f"{res['Player']}%")
            st.metric(b_label, f"{res['Banker']}%")
            st.metric("🟢 TIE WIN", f"{res['Tie']}%")
        with hud2:
            st.markdown("#### 💎 Tỷ Lệ Cửa Đôi (Pair)")
            st.metric("🔵 PLAYER PAIR", f"{p_pair}%")
            st.metric("🔴 BANKER PAIR", f"{b_pair}%")
            st.caption(f"Bài còn trong khay: {int(cards_left)} lá")

        st.markdown("---")
        if st.button("💾 CHỐT KẾT QUẢ VÀO KHAY BÀI", use_container_width=True):
            all_current_cards = p_list + b_list
            st.session_state.shoe_history.extend(all_current_cards)
            st.session_state.last_cards_count.append(len(all_current_cards))
            
            p_score_final = sum([0 if c >= 10 else c for c in p_list]) % 10
            b_score_final = sum([0 if c >= 10 else c for c in b_list]) % 10
            winner = "PLAYER" if p_score_final > b_score_final else ("BANKER" if b_score_final > p_score_final else "TIE")
            
            is_reversed = False
            if res['Player'] > res['Banker'] and winner == "BANKER": is_reversed = True
            elif res['Banker'] > res['Player'] and winner == "PLAYER": is_reversed = True
            
            if is_reversed:
                st.session_state.reverse_streak += 1
            else:
                if winner != "TIE": st.session_state.reverse_streak = 0
            
            game_idx = len(st.session_state.live_logs) + 1
            status_tag = "❌ NGƯỢC XU HƯỚNG" if is_reversed else "✅ CHUẨN XÁC"
            if winner == "TIE": status_tag = "⚖️ HÒA"
                
            st.session_state.live_logs.append(
                f"Ván {game_idx}: P({p_input}) [{p_score_final}đ] vs B({b_input}) [{b_score_final}đ] ➔ {winner} | {status_tag} (Dự kiến: P {res['Player']}% - B {res['Banker']}%)"
            )
            
            actual_numeric = 100 if winner == "PLAYER" else (0 if winner == "BANKER" else 50)
            new_trend = pd.DataFrame([{"Ván": f"V{game_idx}", "Player_Xác_Suất": res['Player'], "Thực_Tế_Ra": actual_numeric}])
            st.session_state.edge_history_df = pd.concat([st.session_state.edge_history_df, new_trend], ignore_index=True)
            st.rerun()
else:
    st.info("💡 Điền ít nhất 2 lá bài của mỗi bên để bộ phân tích xuất kết quả.")

# --- ĐỒ THỊ VÀ LOGS ---
if not st.session_state.edge_history_df.empty:
    st.markdown("---")
    st.markdown("### 📈 Đồ Thị Đối Chiếu Biên Độ Lệch Xác Suất")
    st.line_chart(st.session_state.edge_history_df.set_index("Ván"))

if st.session_state.live_logs:
    with st.expander("📝 Nhật Ký Khay Bài Chi Tiết", expanded=True):
        for log in reversed(st.session_state.live_logs):
            st.text(log)
