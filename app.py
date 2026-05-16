import streamlit as st
import pandas as pd
import numpy as np

# =========================================================================
# SYSTEM CORE: v13.0 - ULTRA PRECISION COMBINATORICS ENGINE (PURE MATH)
# =========================================================================

def calculate_ultra_precision_odds_v13(p_cards, b_cards, shoe_history, total_decks):
    # 1. Khởi tạo cấu trúc khay bài nguyên thủy vật lý 100%
    initial_cards = {i: total_decks * 4 for i in range(1, 14)}
    
    # 2. Khấu trừ chính xác tuyệt đối lịch sử khay bài thực tế
    for card in shoe_history:
        if card in initial_cards and initial_cards[card] > 0:
            initial_cards[card] -= 1

    # Tính tổng số bài còn lại trong khay TRƯỚC KHI chia ván hiện tại
    base_cards_left = sum(initial_cards.values())
    if base_cards_left <= 6:
        return "CRITICAL_LIMIT", {}, 0.0, 0.0, base_cards_left

    # 3. TÍNH XÁC SUẤT CỬA ĐÔI CHÍNH XÁC (Phân phối Siêu hình học truy hồi)
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

    # 4. KHẤU TRỪ BÀI TRÊN TAY (Bảo đảm tính độc lập xác suất cho lá thứ 3)
    active_deck = initial_cards.copy()
    for card in p_cards + b_cards:
        if card in active_deck and active_deck[card] > 0:
            active_deck[card] -= 1

    # Tạo mảng trọng số điểm (0-9) từ khay bài sau khấu trừ tức thời
    score_weights = {i: 0.0 for i in range(10)}
    for card_val, count in active_deck.items():
        score_val = 0 if card_val >= 10 else card_val
        score_weights[score_val] += float(count)

    cards_left_for_third = sum(score_weights.values())
    
    # Tính điểm gốc ban đầu của 2 lá đầu tiên
    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    # Kiểm tra trạng thái Thắng tự nhiên (Natural Lock)
    if p_score >= 8 or b_score >= 8:
        if p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, initial_cards, p_pair_odds, b_pair_odds, cards_left_for_third
        elif b_score > p_score: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, initial_cards, p_pair_odds, b_pair_odds, cards_left_for_third
        else: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, initial_cards, p_pair_odds, b_pair_odds, cards_left_for_third

    # 5. MA TRẬN TÍCH CHẬP XÁC SUẤT CÓ ĐIỀU KIỆN KHÔNG HOÀN LẠI DÀNH CHO LÁ THỨ 3
    player_wins = 0.0
    banker_wins = 0.0
    ties = 0.0

    if p_score >= 6:  # Đứng bài Player
        if b_score <= 5:  # Rút bài Banker
            for card3_b, w_b in score_weights.items():
                if w_b > 0:
                    prob_b = w_b / cards_left_for_third
                    final_b = (b_score + card3_b) % 10
                    if p_score > final_b: player_wins += prob_b
                    elif final_b > p_score: banker_wins += prob_b
                    else: ties += prob_b
        else:  # Cả hai cùng đứng
            if p_score > b_score: player_wins += 1.0
            elif b_score > p_score: banker_wins += 1.0
            else: ties += 1.0
    else:  # Player bắt buộc rút lá thứ 3
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

# =========================================================================
# OMNI PARSER TOKENIZER
# =========================================================================
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
# GRAPHICAL INTERFACE DESIGN
# =========================================================================
st.set_page_config(page_title="v13.0 Pure Quantitative Engine", page_icon="📊", layout="centered")

# Nhúng CSS Engine cao cấp để tạo hiệu ứng khối Neon nổi bật tỷ lệ cao áp đảo
st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; }
    div[data-testid="stColumn"] { width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    
    /* Thiết kế khối HUD hiển thị phân phối xác suất */
    .metric-container {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid #3e3e3e;
        background-color: #1e1e1e;
    }
    .metric-label { font-size: 14px; font-weight: 600; color: #a0a0a0; text-transform: uppercase; letter-spacing: 1px;}
    .metric-value { font-size: 38px; font-weight: 800; font-family: 'Courier New', monospace; margin-top: 5px; }
    
    /* Các định dạng Highlight Neon cực mạnh khi xuất hiện tỉ lệ cao */
    .neon-player-win { background-color: #0984e3 !important; border: 2px solid #74b9ff !important; color: #ffffff !important; box-shadow: 0 0 15px rgba(9, 132, 227, 0.6); }
    .neon-banker-win { background-color: #d63031 !important; border: 2px solid #ff7675 !important; color: #ffffff !important; box-shadow: 0 0 15px rgba(214, 48, 49, 0.6); }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'live_logs' not in st.session_state: st.session_state.live_logs = []
if 'edge_history_df' not in st.session_state: st.session_state.edge_history_df = pd.DataFrame(columns=["Ván", "Player", "Banker"])
if 'last_cards_count' not in st.session_state: st.session_state.last_cards_count = []

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("⚙️ THIẾT LẬP KHAY BÀI")
decks = st.sidebar.selectbox("Số lượng bộ bài:", [8, 6, 4], index=0)

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
        st.rerun()

if st.sidebar.button("🔄 LÀM MỚI KHAY BÀI (XÓA HẾT)", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.live_logs = []
    st.session_state.last_cards_count = []
    st.session_state.edge_history_df = pd.DataFrame(columns=["Ván", "Player", "Banker"])
    st.rerun()

# --- MAIN HUD DISPLAY ---
st.title("📊 v13.0 PURE QUANTITATIVE ENGINE")
st.caption("Core v13.0: Loại bỏ hoàn toàn quản lý vốn - Tập trung tối đa ma trận xác suất tích chập")

# Thống kê cơ bản số lượng thẻ bài vật lý còn lại
total_deck_cards = decks * 52
cards_used = len(st.session_state.shoe_history)
cards_left_in_shoe = total_deck_cards - cards_used

st.markdown(f"**Trạng thái khay bài:** Đã dùng `{cards_used}` lá / Còn lại `{cards_left_in_shoe}` lá trong tổng số `{total_deck_cards}` lá.")
st.progress(cards_used / total_deck_cards if total_deck_cards > 0 else 0.0)

st.markdown("### 🃏 Nhập Bài Ván Hiện Tại")
col_p, col_b = st.columns(2)
with col_p: p_input = st.text_input("PLAYER CARDS (Ví dụ: 7,A,K):", value="", key="p_in")
with col_b: b_input = st.text_input("BANKER CARDS (Ví dụ: Q,9):", value="", key="b_in")

p_list = parse_raw_cards(p_input)
b_list = parse_raw_cards(b_input)

if len(p_list) >= 2 or len(b_list) >= 2:
    calculation_output = calculate_ultra_precision_odds_v13(p_list[:2], b_list[:2], st.session_state.shoe_history, decks)
    
    if calculation_output[0] == "CRITICAL_LIMIT":
        st.error("🚨 HẾT BÀI: Khay bài đã chạm giới hạn vật lý để chạy tổ hợp toán học.")
    else:
        res, remaining_deck, p_pair, b_pair, cards_left = calculation_output
        
        # Quyết định class CSS để làm nổi bật phần tỉ lệ cao
        p_box_class = "metric-container"
        b_box_class = "metric-container"
        
        if res['Player'] > res['Banker']:
            p_box_class = "metric-container neon-player-win"
        elif res['Banker'] > res['Player']:
            b_box_class = "metric-container neon-banker-win"
            
        st.markdown("---")
        st.markdown("### 📈 Kết Quả Phân Tích Xác Suất v13.0")
        
        hud1, hud2 = st.columns(2)
        with hud1:
            st.markdown(
                f"""
                <div class="{p_box_class}">
                    <div class="metric-label">🔵 PLAYER WIN ODDS</div>
                    <div class="metric-value">{res['Player']}%</div>
                </div>
                <div class="{b_box_class}">
                    <div class="metric-label">🔴 BANKER WIN ODDS</div>
                    <div class="metric-value">{res['Banker']}%</div>
                </div>
                <div class="metric-container">
                    <div class="metric-label">🟢 TIE WIN ODDS</div>
                    <div class="metric-value" style="color: #2ecc71; font-size:28px;">{res['Tie']}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with hud2:
            st.markdown(
                f"""
                <div class="metric-container" style="margin-bottom: 25px;">
                    <div class="metric-label">🔵 PLAYER PAIR</div>
                    <div class="metric-value" style="color: #74b9ff; font-size:30px;">{p_pair}%</div>
                </div>
                <div class="metric-container" style="margin-bottom: 25px;">
                    <div class="metric-label">🔴 BANKER PAIR</div>
                    <div class="metric-value" style="color: #ff7675; font-size:30px;">{b_pair}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.caption(f"Lõi bài thực tế còn lại tính toán cho lá thứ 3: **{int(cards_left)} lá**")

        st.markdown("---")
        if st.button("💾 CHỐT KẾT QUẢ VÀO KHAY BÀI", use_container_width=True):
            all_current_cards = p_list + b_list
            st.session_state.shoe_history.extend(all_current_cards)
            st.session_state.last_cards_count.append(len(all_current_cards))
            
            p_score_final = sum([0 if c >= 10 else c for c in p_list]) % 10
            b_score_final = sum([0 if c >= 10 else c for c in b_list]) % 10
            winner = "PLAYER" if p_score_final > b_score_final else ("BANKER" if b_score_final > p_score_final else "TIE")
            
            game_idx = len(st.session_state.live_logs) + 1
            st.session_state.live_logs.append(f"Ván {game_idx}: P({p_input}) [{p_score_final}đ] vs B({b_input}) [{b_score_final}đ] ➔ {winner}")
            
            new_trend = pd.DataFrame([{"Ván": f"V{game_idx}", "Player": res['Player'], "Banker": res['Banker']}])
            st.session_state.edge_history_df = pd.concat([st.session_state.edge_history_df, new_trend], ignore_index=True)
            st.rerun()
else:
    st.info("💡 Điền tối thiểu 2 lá bài đầu của mỗi bên để kích hoạt ma trận tính chập tổ hợp.")

# --- BIỂU ĐỒ XU HƯỚNG LỢI THẾ TOÁN HỌC ---
if not st.session_state.edge_history_df.empty:
    st.markdown("---")
    st.markdown("### 📈 Biểu Đồ Biến Động Lợi Thế Khay Bài Thực Tế")
    st.line_chart(st.session_state.edge_history_df.set_index("Ván"))

# --- NHẬT KÝ CHI TIẾT ---
if st.session_state.live_logs:
    with st.expander("📝 Nhật Ký Khay Bài Chi Tiết (Live Historical Logs)", expanded=True):
        for log in reversed(st.session_state.live_logs):
            st.text(log)
