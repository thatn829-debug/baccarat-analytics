import streamlit as st
import pandas as pd
import numpy as np

# =========================================================================
# SYSTEM CORE: v12.4 - QUANTUM ENGINE WITH PHYSICAL AUDIT
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
st.set_page_config(page_title="v12.4 Hybrid Quant", page_icon="⚡", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; }
    div[data-testid="stColumn"] { width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    .advice-box { background-color: #1e1e2f; padding: 15px; border-radius: 8px; margin-bottom: 15px; font-size: 16px; text-align: center;}
    .normal-box { border: 2px solid #3498db; color: #3498db; }
    .alert-box { border: 2px solid #e74c3c; color: #e74c3c; background-color: #3a1f1f; }
    .invert-box { border: 2px solid #9b59b6; color: #9b59b6; background-color: #2e1f3a; }
    .audit-table { width: 100%; border-collapse: collapse; margin-bottom: 15px; text-align: center; }
    .audit-table th, .audit-table td { border: 1px solid #444; padding: 8px; font-size: 14px; }
    .audit-table th { background-color: #2c3e50; color: white; }
    </style>
    """, 
    unsafe_allow_html=True
)

# Khởi tạo các biến lưu trữ hệ thống
if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'live_logs' not in st.session_state: st.session_state.live_logs = []
if 'edge_history_df' not in st.session_state: st.session_state.edge_history_df = pd.DataFrame(columns=["Ván", "Player_Xác_Suất", "Thực_Tế_Ra"])
if 'last_cards_count' not in st.session_state: st.session_state.last_cards_count = []
if 'reverse_streak' not in st.session_state: st.session_state.reverse_streak = 0

# Khởi tạo bộ đếm kết quả thắng/thua vật lý
if 'stat_games' not in st.session_state: st.session_state.stat_games = 0
if 'stat_cards_used' not in st.session_state: st.session_state.stat_cards_used = 0
if 'stat_p_wins' not in st.session_state: st.session_state.stat_p_wins = 0
if 'stat_b_wins' not in st.session_state: st.session_state.stat_b_wins = 0
if 'stat_t_wins' not in st.session_state: st.session_state.stat_t_wins = 0
if 'last_winners' not in st.session_state: st.session_state.last_winners = []

# --- SIDEBAR PANEL ---
st.sidebar.header("⚙️ THIẾT LẬP KHAY BÀI")
decks = st.sidebar.selectbox("Số lượng bộ bài:", [8, 6, 4], index=0)
is_super6_rule = st.sidebar.checkbox("Bàn chơi Super 6", value=False)
edge_min = st.sidebar.slider("Ngưỡng biên độ an toàn tối thiểu (%)", 1, 15, 6)

st.sidebar.markdown("---")
if st.sidebar.button("↩️ HOÀN TÁC VÁN TRƯỚC", use_container_width=True):
    if st.session_state.live_logs:
        st.session_state.live_logs.pop()
        if not st.session_state.edge_history_df.empty:
            st.session_state.edge_history_df = st.session_state.edge_history_df.iloc[:-1]
        
        # Hoàn tác số lượng lá bài
        if st.session_state.last_cards_count:
            count_to_pop = st.session_state.last_cards_count.pop()
            if count_to_pop <= len(st.session_state.shoe_history):
                st.session_state.shoe_history = st.session_state.shoe_history[:-count_to_pop]
                st.session_state.stat_cards_used -= count_to_pop
        
        # Hoàn tác bộ đếm thắng thua
        if st.session_state.last_winners:
            last_w = st.session_state.last_winners.pop()
            if last_w == "PLAYER": st.session_state.stat_p_wins -= 1
            elif last_w == "BANKER": st.session_state.stat_b_wins -= 1
            elif last_w == "TIE": st.session_state.stat_t_wins -= 1
            
        st.session_state.stat_games = max(0, st.session_state.stat_games - 1)
        st.session_state.reverse_streak = max(0, st.session_state.reverse_streak - 1)
        st.rerun()

if st.sidebar.button("🔄 LÀM MỚI KHAY BÀI (XÓA HẾT)", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.live_logs = []
    st.session_state.last_cards_count = []
    st.session_state.edge_history_df = pd.DataFrame(columns=["Ván", "Player_Xác_Suất", "Thực_Tế_Ra"])
    st.session_state.reverse_streak = 0
    st.session_state.stat_games = 0
    st.session_state.stat_cards_used = 0
    st.session_state.stat_p_wins = 0
    st.session_state.stat_b_wins = 0
    st.session_state.stat_t_wins = 0
    st.session_state.last_winners = []
    st.rerun()

# --- MAIN HUD ---
st.title("⚡ v12.4 HYBRID QUANT AUDIT")
st.caption("Tích hợp số ván, số lá bài cấu trúc và thống kê bàn thắng thực tế")

# --- BẢNG SỐ LIỆU ĐẾM VÁN VÀ LÁ BÀI (YÊU CẦU MỚI) ---
total_deck_cards = Decks_Total = decks * 52
cards_remaining_display = total_deck_cards - st.session_state.stat_cards_used

st.markdown(
    f"""
    <table class="audit-table">
        <tr>
            <th>Tổng Số Ván</th>
            <th>Số Lá Đã Ra</th>
            <th>Số Lá Còn Lại</th>
            <th style="color:#3498db;">Player Thắng</th>
            <th style="color:#e74c3c;">Banker Thắng</th>
            <th style="color:#2ecc71;">Trận Hòa (Tie)</th>
        </tr>
        <tr>
            <td><b>{st.session_state.stat_games}</b></td>
            <td>{st.session_state.stat_cards_used} / {total_deck_cards}</td>
            <td><b>{cards_remaining_display}</b></td>
            <td style="color:#3498db;"><b>{st.session_state.stat_p_wins}</b></td>
            <td style="color:#e74c3c;"><b>{st.session_state.stat_b_wins}</b></td>
            <td style="color:#2ecc71;"><b>{st.session_state.stat_t_wins}</b></td>
        </tr>
    </table>
    """,
    unsafe_allow_html=True
)

# RADAR TRẠNG THÁI SÓNG
is_inversion_active = False
if st.session_state.reverse_streak >= 5:
    is_inversion_active = True
    st.error(f"🔮 **INVERSION MODE ACTIVE ({st.session_state.reverse_streak} VÁN NGƯỢC)**: Đánh NGƯỢC với ma trận toán học gốc.")
elif st.session_state.reverse_streak >= 3:
    st.warning(f"⚠️ **DIVERGENCE RISK:** Khay bài có xu hướng bẻ toán ({st.session_state.reverse_streak} ván).")

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
        
        diff = abs(res['Player'] - res['Banker'])
        p_label, b_label = "🔵 PLAYER WIN", "🔴 BANKER WIN"
        
        if res['Player'] > res['Banker']:
            theoretical_winner = "PLAYER"
            p_label = "👑 🔵 PLAYER WIN [CỬA TRÊN]"
        elif res['Banker'] > res['Player']:
            theoretical_winner = "BANKER"
            b_label = "👑 🔴 BANKER WIN [CỬA TRÊN]"
        else:
            theoretical_winner = "EQUAL"

        if theoretical_winner == "EQUAL":
            advice_html = "<div class='advice-box normal-box'>⚖️ <b>CÂN BẰNG:</b> Tỷ lệ 50-50, KHÔNG đặt cược.</div>"
        elif diff < edge_min:
            advice_html = f"<div class='advice-box alert-box'>⚠️ <b>BỎ QUA VÁN NÀY:</b> Lợi thế +{diff}% chưa đạt ngưỡng an toàn ({edge_min}%).</div>"
        else:
            if is_inversion_active:
                target_bet = "BANKER" if theoretical_winner == "PLAYER" else "PLAYER"
                advice_html = f"<div class='advice-box invert-box'>🔄 <b>INVERSION BET: ĐẶT VÀO {target_bet}</b><br>Đánh ngược toán học gốc theo Sóng nhà cái!</div>"
            else:
                advice_html = f"<div class='advice-box normal-box'>🎯 <b>LỆNH CƯỢC: ĐẶT VÀO {theoretical_winner}</b><br>Lợi thế an toàn: <b>+{diff}%</b></div>"

        st.markdown(advice_html, unsafe_allow_html=True)

        st.markdown("---")
        hud1, hud2 = st.columns(2)
        with hud1:
            st.markdown("#### 📊 Ma Trận Xác Suất")
            st.metric(p_label, f"{res['Player']}%")
            st.metric(b_label, f"{res['Banker']}%")
            st.metric("🟢 TIE WIN", f"{res['Tie']}%")
        with hud2:
            st.markdown("#### 💎 Tỷ Lệ Cửa Đôi")
            st.metric("🔵 PLAYER PAIR", f"{p_pair}%")
            st.metric("🔴 BANKER PAIR", f"{b_pair}%")
            st.caption(f"Lá bài thực tế trong lõi máy: {int(cards_left)} lá")

        st.markdown("---")
        if st.button("💾 CHỐT KẾT QUẢ VÀO KHAY BÀI", use_container_width=True):
            all_current_cards = p_list + b_list
            st.session_state.shoe_history.extend(all_current_cards)
            st.session_state.last_cards_count.append(len(all_current_cards))
            
            # Tăng các biến thống kê đếm bài vật lý
            st.session_state.stat_games += 1
            st.session_state.stat_cards_used += len(all_current_cards)
            
            p_score_final = sum([0 if c >= 10 else c for c in p_list]) % 10
            b_score_final = sum([0 if c >= 10 else c for c in b_list]) % 10
            
            if p_score_final > b_score_final:
                winner = "PLAYER"
                st.session_state.stat_p_wins += 1
            elif b_score_final > p_score_final:
                winner = "BANKER"
                st.session_state.stat_b_wins += 1
            else:
                winner = "TIE"
                st.session_state.stat_t_wins += 1
                
            st.session_state.last_winners.append(winner)
            
            is_reversed = False
            if res['Player'] > res['Banker'] and winner == "BANKER": is_reversed = True
            elif res['Banker'] > res['Player'] and winner == "PLAYER": is_reversed = True
            
            if is_reversed:
                st.session_state.reverse_streak += 1
            else:
                if winner != "TIE": st.session_state.reverse_streak = 0
            
            status_tag = "❌ NGƯỢC" if is_reversed else "✅ CHUẨN"
            if winner == "TIE": status_tag = "⚖️ HÒA"
                
            st.session_state.live_logs.append(
                f"Ván {st.session_state.stat_games}: P({p_input}) [{p_score_final}đ] vs B({b_input}) [{b_score_final}đ] ➔ {winner} | {status_tag} (Dự kiến: P {res['Player']}% - B {res['Banker']}%)"
            )
            
            actual_numeric = 100 if winner == "PLAYER" else (0 if winner == "BANKER" else 50)
            new_trend = pd.DataFrame([{"Ván": f"V{st.session_state.stat_games}", "Player_Xác_Suất": res['Player'], "Thực_Tế_Ra": actual_numeric}])
            st.session_state.edge_history_df = pd.concat([st.session_state.edge_history_df, new_trend], ignore_index=True)
            st.rerun()
else:
    st.info("💡 Điền ít nhất 2 lá bài của mỗi bên để cập nhật ma trận phân tích.")

# --- ĐỒ THỊ VÀ LOGS ---
if not st.session_state.edge_history_df.empty:
    st.markdown("---")
    st.markdown("### 📈 Đồ Thị Lợi Thế & Đối Chiếu Thực Tế")
    st.line_chart(st.session_state.edge_history_df.set_index("Ván"))

if st.session_state.live_logs:
    with st.expander("📝 Nhật Ký Kiểm Toán Khay Bài", expanded=True):
        for log in reversed(st.session_state.live_logs):
            st.text(log)
