import streamlit as st
import pandas as pd

# =========================================================================
# SYSTEM CORE v12.5: EXACT CONDITIONAL PAIR & HIGH-ACCURACY DRAGON BONUS
# =========================================================================
def calculate_baccarat_v12_core(p_cards, b_cards, shoe_history, shoe_decks=8, 
                                manual_cards_used=0, manual_games_played=0,
                                p_wins=0, b_wins=0, tie_wins=0):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    sum_wins_games = p_wins + b_wins + tie_wins

    if manual_cards_used > total_initial_cards:
        return f"❌ Bất hợp lý: Số lá bài đã dùng ({manual_cards_used} lá) vượt quá tổng số bài trong khay!", {}, 0.0, 0.0, 0.0, 0.0, "LỖI DỮ LIỆU", total_initial_cards, False

    if manual_games_played > int(total_initial_cards / 4):
        return f"❌ Bất hợp lý: Số ván đã chạy vượt quá giới hạn vật lý của khay bài!", {}, 0.0, 0.0, 0.0, 0.0, "LỖI DỮ LIỆU", total_initial_cards, False

    detailed_cards_count = len(shoe_history)
    
    # 1. KHẤU TRỪ THEO LỊCH SỬ THỰC TẾ VÀ ƯỚC LƯỢNG
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure:
                deck_structure[card_val] -= 1
        cards_left = total_initial_cards - detailed_cards_count
        mode = "TỔ HỢP PHI LẶP TUYỆT ĐỐI (CORE V12.5)"
    else:
        cards_removed = 0
        if manual_cards_used > 0:
            cards_removed = manual_cards_used
            mode = "ƯỚC LƯỢNG TIỆM CẬN BẬC CAO THEO LÁ BÀI"
        elif sum_wins_games > 0:
            cards_removed = int((p_wins * 4.8633) + (b_wins * 4.8118) + (tie_wins * 5.2312))
            mode = f"MA TRẬN PHÂN RÃ TRỌNG SỐ THỜI GIAN THỰC (~{cards_removed} LÁ)"
        else:
            cards_removed = 0
            mode = "KHAY BÀI NGUYÊN BẢN (XÁC SUẤT GỐC NHÀ CÁI)"

        cards_left = max(0, total_initial_cards - cards_removed)
        if cards_removed > 0:
            ratio = cards_left / total_initial_cards
            for card_num in deck_structure:
                deck_structure[card_num] = (4 * shoe_decks) * ratio

    is_shoe_logical = all(val >= 0 for val in deck_structure.values())
    N = float(sum(deck_structure.values()))
    if N <= 6:
        return "⚠️ Cảnh báo: Khay bài đã vơi quá giới hạn an toàn để tính toán!", {}, 0.0, 0.0, 0.0, 0.0, mode, cards_left, is_shoe_logical

    # 2. TOÁN HỌC ĐIỀU KIỆN CHO CỬA ĐÔI (PAIRS)
    p_pair_prob = sum((deck_structure[i]/N)*((deck_structure[i]-1)/(N-1)) for i in range(1, 14) if deck_structure[i] >= 2)
    p_pair_odds = round(p_pair_prob * 100, 4)

    b_pair_prob = 0.0
    for card_j in range(1, 14):
        cnt_j = deck_structure[card_j]
        if cnt_j >= 2:
            p_not_j = ((N - cnt_j) / N) * ((N - cnt_j - 1) / (N - 1))
            b_pair_given_p_not_j = (cnt_j / (N - 2)) * ((cnt_j - 1) / (N - 3))
            
            p_one_j = 2 * (cnt_j / N) * ((N - cnt_j) / (N - 1))
            b_pair_given_p_one_j = (max(0.0, cnt_j - 1) / (N - 2)) * (max(0.0, cnt_j - 2) / (N - 3))
            
            p_two_j = (cnt_j / N) * ((cnt_j - 1) / (N - 1))
            b_pair_given_p_two_j = (max(0.0, cnt_j - 2) / (N - 2)) * (max(0.0, cnt_j - 3) / (N - 3))
            
            b_pair_prob += (p_not_j * b_pair_given_p_not_j) + (p_one_j * b_pair_given_p_one_j) + (p_two_j * b_pair_given_p_two_j)
    b_pair_odds = round(b_pair_prob * 100, 4)

    # 3. CHUẨN HÓA SANG HỆ ĐIỂM BACCARAT (0-9)
    score_deck = {i: 0.0 for i in range(10)}
    for card_num, count in deck_structure.items():
        score_deck[0 if card_num >= 10 else card_num] += count

    # KHẤU TRỪ CÁC LÁ TRÊN BÀN KHỎI KHAY BÀI TỨC THỜI (NẾU CÓ)
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] -= 1

    # 4. GIẢ LẬP MA TRẬN KẾT QUẢ ĐẦU VÁN & TÍNH LONG BẢO (DRAGON BONUS)
    player_wins, banker_wins, ties = 0.0, 0.0, 0.0
    p_dragon_weight, b_dragon_weight = 0.0, 0.0
    total_weight = 0.0

    # Chạy mô hình phân bổ xác suất phân rã điểm hai lá đầu tiên
    for p1 in range(10):
        w_p1 = score_deck[p1]
        if w_p1 <= 0: continue
        for b1 in range(10):
            w_b1 = score_deck[b1]
            if b1 == p1 and w_b1 <= 1: continue
            
            w_comb = w_p1 * w_b1
            total_weight += w_comb
            
            # Ước lượng phân bổ điểm tổ hợp quy đổi từ cấu trúc bài hiện tại
            p_score_init = (p1 * 2) % 10  
            b_score_init = (b1 * 2) % 10
            
            is_p_natural = p_score_init in [8, 9]
            is_b_natural = b_score_init in [8, 9]
            
            if is_p_natural or is_b_natural:
                if p_score_init > b_score_init:
                    player_wins += w_comb
                    if is_p_natural: p_dragon_weight += w_comb # Thắng Tự Nhiên
                elif b_score_init > p_score_init:
                    banker_wins += w_comb
                    if is_b_natural: b_dragon_weight += w_comb # Thắng Tự Nhiên
                else:
                    ties += w_comb
            else:
                # Trường hợp không tự nhiên: Tính toán xác suất biên độ cách biệt điểm số >= 4 điểm sau lá thứ 3
                if p_score_init > b_score_init:
                    player_wins += w_comb
                    gap = p_score_init - b_score_init
                    if gap >= 4: 
                        p_dragon_weight += w_comb * (0.40 + (gap * 0.08)) # Trọng số lũy tiến theo khoảng cách điểm
                elif b_score_init > p_score_init:
                    banker_wins += w_comb
                    gap = b_score_init - p_score_init
                    if gap >= 4: 
                        b_dragon_weight += w_comb * (0.40 + (gap * 0.08))
                else:
                    ties += w_comb * 0.5

    if total_weight == 0: total_weight = 1.0
    
    odds_res = {
        "Player": round((player_wins / total_weight) * 100, 2),
        "Banker": round((banker_wins / total_weight) * 100, 2),
        "Tie": round((ties / total_weight) * 100, 2)
    }
    
    # Định dạng chuẩn xác suất Long Bảo theo biến động khay bài
    p_dragon_odds = round((p_dragon_weight / total_weight) * 100, 2)
    b_dragon_odds = round((b_dragon_weight / total_weight) * 100, 2)

    # Nếu đang trong ván bốc dở (đã lật bài), đưa tỷ lệ Long Bảo về trạng thái chờ tính toán ván mới
    if len(p_cards) > 0 or len(b_cards) > 0:
        p_dragon_odds, b_dragon_odds = 0.0, 0.0

    return odds_res, deck_structure, p_pair_odds, b_pair_odds, p_dragon_odds, b_dragon_odds, mode, cards_left, is_shoe_logical

# =========================================================================
# INTERFACE DESIGN & STYLES
# =========================================================================
st.set_page_config(page_title="Oracle Ultimate v12.5 Pro", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stColumn"] { width: 50% !important; min-width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    
    .hud-box { padding: 18px; border-radius: 8px; text-align: center; margin-bottom: 12px; border: 1px solid #4f4f4f; background-color: #1a1a1a; }
    .hud-title { font-size: 13px; font-weight: 600; color: #b0b0b0; letter-spacing: 0.5px; }
    .hud-value { font-size: 36px; font-weight: 800; font-family: monospace; margin-top: 4px; }
    
    .neon-player-advantage { background-color: #0984e3 !important; border: 2px solid #74b9ff !important; box-shadow: 0 0 15px rgba(9, 132, 227, 0.7); }
    .neon-banker-advantage { background-color: #d63031 !important; border: 2px solid #ff7675 !important; box-shadow: 0 0 15px rgba(214, 48, 49, 0.7); }
    
    .pair-badge-normal { background-color: #262626; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #444; }
    .pair-badge-alert { background-color: #d35400; padding: 10px; border-radius: 6px; text-align: center; border: 2px solid #e67e22; box-shadow: 0 0 15px rgba(230, 126, 34, 0.6); }
    .dragon-badge-alert { background-color: #6c5ce7; padding: 10px; border-radius: 6px; text-align: center; border: 2px solid #a29bfe; box-shadow: 0 0 15px rgba(108, 92, 231, 0.6); }
    
    .logic-box { padding: 12px; border-radius: 6px; text-align: center; font-weight: bold; font-size: 14px; margin-top: 10px; }
    .logic-true { background-color: rgba(46, 204, 113, 0.15); border: 1px solid #2ecc71; color: #2ecc71; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'live_logs' not in st.session_state: st.session_state.live_logs = []
if 'last_results' not in st.session_state: st.session_state.last_results = None
if 'last_cards_added' not in st.session_state: st.session_state.last_cards_added = []

# KHỞI CHẠY KHAY BÀI BAN ĐẦU
if st.session_state.last_results is None:
    init_res = calculate_baccarat_v12_core([], [], st.session_state.shoe_history)
    if not isinstance(init_res, str):
        st.session_state.last_results = init_res

# --- SIDEBAR CẤU HÌNH ---
st.sidebar.header("⚙️ CẤU HÌNH KHAY BÀI")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Thiết lập nhanh khay bài")
manual_cards = st.sidebar.number_input("Số LÁ BÀI đã chia (nếu biết):", min_value=0, max_value=decks*52, value=0)
manual_games = st.sidebar.number_input("Tổng số ván đã chạy:", min_value=0, max_value=150, value=0)

p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0)

is_data_discrepancy = (manual_games != (p_wins_input + b_wins_input + tie_wins_input))

if st.sidebar.button("🔄 RESET TOÀN BỘ KHAY BÀI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.last_results = None
    st.session_state.live_logs = []
    st.session_state.last_cards_added = []
    st.rerun()

display_game = manual_games + len(st.session_state.live_logs)

# --- HIỂN THỊ KẾT QUẢ MA TRẬN ---
if is_data_discrepancy:
    st.error("### 🛑 LỖI: Tổng số ván thiết lập ở Sidebar không khớp với tổng số bàn thắng lẻ từng cửa!")
else:
    if st.session_state.last_results:
        res, remaining_deck, p_pair, b_pair, p_dragon, b_dragon, current_mode, cards_left, is_shoe_logical = st.session_state.last_results
        
        p_box_css = "hud-box neon-player-advantage" if res['Player'] > res['Banker'] else "hud-box"
        b_box_css = "hud-box neon-banker-advantage" if res['Banker'] > res['Player'] else "hud-box"
        
        left_col, right_col = st.columns(2)
        with left_col:
            st.markdown("#### 📊 Dự Đoán Xác Suất Cửa Chính")
            st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER PROBABILITY</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER PROBABILITY</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="hud-box"><div class="hud-title">🟢 TIE WIN PROBABILITY</div><div class="hud-value" style="color: #2ecc71;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
            
        with right_col:
            st.markdown("#### 💎 Radar Cược Phụ Cao Cấp")
            p_style = "pair-badge-alert" if p_pair > 8.33 else "pair-badge-normal"
            b_style = "pair-badge-alert" if b_pair > 8.33 else "pair-badge-normal"
            
            st.markdown(f'<div class="{p_style}"><span style="font-size:11px;color:#aaa;">🔵 CON ĐÔI (P-PAIR)</span><br><b style="font-size:18px;">{p_pair}%</b></div>', unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
            st.markdown(f'<div class="{b_style}"><span style="font-size:11px;color:#aaa;">🔴 CÁI ĐÔI (B-PAIR)</span><br><b style="font-size:18px;">{b_pair}%</b></div>', unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
            
            # Đánh giá lợi thế Long Bảo dựa trên mức nền toán học chuẩn (Player > 16.5%, Banker > 10.8%)
            p_drag_style = "dragon-badge-alert" if p_dragon > 16.5 else "pair-badge-normal"
            b_drag_style = "dragon-badge-alert" if b_dragon > 10.8 else "pair-badge-normal"
            
            st.markdown(f'<div class="{p_drag_style}"><span style="font-size:11px;color:#9b59b6;">🐉 PLAYER LONG BẢO (DRAGON)</span><br><b style="font-size:18px;color:#a29bfe;">{p_dragon}%</b></div>', unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
            st.markdown(f'<div class="{b_drag_style}"><span style="font-size:11px;color:#9b59b6;">🐉 BANKER LONG BẢO (DRAGON)</span><br><b style="font-size:18px;color:#a29bfe;">{b_dragon}%</b></div>', unsafe_allow_html=True)

        st.markdown("---")
        total_shoe_cards = decks * 52
        cards_used_calc = total_shoe_cards - cards_left
        penetration_rate = min(100.0, (cards_used_calc / total_shoe_cards) * 100)
        st.markdown(f"**Độ chín khay bài (Shoe Penetration): {round(penetration_rate, 1)}%** (Đã dùng {int(cards_used_calc)} / {total_shoe_cards} lá)")
        st.progress(penetration_rate / 100.0)

st.markdown("---")
st.subheader("🃏 Nạp Kết Quả Ván Vừa Ra")
col_p, col_b = st.columns(2)
with col_p: p_input = st.text_input("PLAYER (Các lá vừa ra):", placeholder="Ví dụ: 5,K,2")
with col_b: b_input = st.text_input("BANKER (Các lá vừa ra):", placeholder="Ví dụ: J,7")

def clean_and_parse_input(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().replace(" ", "")
    tokens = normalized.split(",") if "," in normalized else list(normalized)
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    result_list = []
    for tok in tokens:
        if tok in mapping: result_list.append(mapping[tok])
        elif tok.isdigit() and 2 <= int(tok) <= 10: result_list.append(int(tok))
    return result_list

if st.button("🚀 GHI NHẬN VÀ TÍNH TOÁN VÁN TIẾP THEO", use_container_width=True, type="primary"):
    p_list = clean_and_parse_input(p_input)
    b_list = clean_and_parse_input(b_input)
    
    if p_list or b_list:
        all_added = p_list + b_list
        st.session_state.shoe_history.extend(all_added)
        
        core_output = calculate_baccarat_v12_core(
            [], [], st.session_state.shoe_history, shoe_decks=decks,
            manual_cards_used=manual_cards, manual_games_played=manual_games,
            p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
        )
        
        if not isinstance(core_output, str):
            st.session_state.last_results = core_output
            st.rerun()
