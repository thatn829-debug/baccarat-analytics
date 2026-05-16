import streamlit as st
import pandas as pd

# =========================================================================
# SYSTEM CORE v12.6: FIXED PAIRS & DRAGON BONUS MATRIX SENSOR
# =========================================================================
def calculate_baccarat_v12_6(shoe_history, shoe_decks=8, manual_cards_used=0):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    if manual_cards_used > total_initial_cards:
        return "❌ Dữ liệu nạp thủ công vượt quá giới hạn vật lý khay bài!", {}, 0.0, 0.0, 0.0, 0.0, "LỖI", total_initial_cards, False

    detailed_cards_count = len(shoe_history)
    
    # 1. KHẤU TRỪ BÀI THEO LỊCH SỬ THỰC TẾ VÀ ƯỚC LƯỢNG
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure:
                deck_structure[card_val] -= 1
        cards_left = total_initial_cards - detailed_cards_count
        mode = "TỔ HỢP PHI LẶP CHUỖI (CORE V12.6)"
    else:
        # Sửa lỗi: Đồng bộ hóa biến manual_cards_used tránh lỗi NameError
        cards_removed = manual_cards_used
        cards_left = max(0, total_initial_cards - cards_removed)
        ratio = cards_left / total_initial_cards if total_initial_cards > 0 else 0
        for card_num in deck_structure:
            deck_structure[card_num] = (4 * shoe_decks) * ratio
        mode = "MA TRẬN ƯỚC LƯỢNG TIỆM CẬN"

    is_shoe_logical = all(val >= 0 for val in deck_structure.values())
    N = float(sum(deck_structure.values()))
    if N <= 6:
        return "⚠️ Cảnh báo: Khay bài đã vơi quá giới hạn!", {}, 0.0, 0.0, 0.0, 0.0, mode, int(N), is_shoe_logical

    # 2. TOÁN HỌC CỬA ĐÔI (PAIRS) - CHUẨN XÁC V12.5
    p_pair_prob = sum((deck_structure[i]/N)*((deck_structure[i]-1)/(N-1)) for i in range(1, 14) if deck_structure[i] >= 2)
    p_pair_odds = round(p_pair_prob * 100, 2)

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
    b_pair_odds = round(b_pair_prob * 100, 2)

    # 3. CHUẨN HÓA SANG MÔ HÌNH ĐIỂM (MODULO 10) ĐỂ TÍNH CỬA CHÍNH & LONG BẢO
    score_deck = {i: 0.0 for i in range(10)}
    for card_num, count in deck_structure.items():
        score_deck[0 if card_num >= 10 else card_num] += count

    # GIẢ LẬP ĐẦU VÁN MỚI (TÍNH TOÁN LONG BẢO TOÀN DIỆN)
    player_wins, banker_wins, ties = 0.0, 0.0, 0.0
    p_dragon_weight, b_dragon_weight = 0.0, 0.0
    total_weight = 0.0

    for p_score_init in range(10):
        w_p = score_deck[p_score_init]
        if w_p <= 0: continue
        for b_score_init in range(10):
            w_b = score_deck[b_score_init]
            if w_b <= 0: continue
            
            w_comb = w_p * w_b
            total_weight += w_comb
            
            is_p_natural = p_score_init in [8, 9]
            is_b_natural = b_score_init in [8, 9]
            
            if is_p_natural or is_b_natural:
                if p_score_init > b_score_init:
                    player_wins += w_comb
                    if is_p_natural: p_dragon_weight += w_comb
                elif b_score_init > p_score_init:
                    banker_wins += w_comb
                    if is_b_natural: b_dragon_weight += w_comb
                else:
                    ties += w_comb
            else:
                if p_score_init > b_score_init:
                    player_wins += w_comb
                    if (p_score_init - b_score_init) >= 4: p_dragon_weight += w_comb * 0.45
                elif b_score_init > p_score_init:
                    banker_wins += w_comb
                    if (b_score_init - p_score_init) >= 4: b_dragon_weight += w_comb * 0.45
                else:
                    ties += w_comb * 0.5

    if total_weight == 0: total_weight = 1.0
    
    odds_res = {
        "Player": round((player_wins / total_weight) * 100, 2),
        "Banker": round((banker_wins / total_weight) * 100, 2),
        "Tie": round((ties / total_weight) * 100, 2)
    }
    
    p_dragon_odds = round((p_dragon_weight / total_weight) * 100, 2)
    b_dragon_odds = round((b_dragon_weight / total_weight) * 100, 2)

    return odds_res, deck_structure, p_pair_odds, b_pair_odds, p_dragon_odds, b_dragon_odds, mode, int(cards_left), is_shoe_logical

# =========================================================================
# INTERFACE DESIGN
# =========================================================================
st.set_page_config(page_title="Oracle Matrix v12.6", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stColumn"] { width: 50% !important; min-width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    
    .hud-box { padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; border: 1px solid #4f4f4f; background-color: #1a1a1a; }
    .hud-title { font-size: 12px; font-weight: 600; color: #b0b0b0; letter-spacing: 0.5px; }
    .hud-value { font-size: 32px; font-weight: 800; font-family: monospace; margin-top: 2px; }
    
    .neon-player-advantage { background-color: #0984e3 !important; border: 2px solid #74b9ff !important; box-shadow: 0 0 12px rgba(9, 132, 227, 0.6); }
    .neon-banker-advantage { background-color: #d63031 !important; border: 2px solid #ff7675 !important; box-shadow: 0 0 12px rgba(214, 48, 49, 0.6); }
    
    .badge-normal { background-color: #262626; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #444; }
    .badge-alert { background-color: #d35400; padding: 10px; border-radius: 6px; text-align: center; border: 2px solid #e67e22; box-shadow: 0 0 12px rgba(230, 126, 34, 0.6); }
    .badge-dragon { background-color: #6c5ce7; padding: 10px; border-radius: 6px; text-align: center; border: 2px solid #a29bfe; box-shadow: 0 0 12px rgba(108, 92, 231, 0.6); }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'manual_cards' not in st.session_state: st.session_state.manual_cards = 0

# SIDEBAR CONFIG
st.sidebar.header("⚙️ CẤU HÌNH CƠ SỞ")
decks = st.sidebar.selectbox("Số bộ bài:", [8, 6], index=0)
manual_cards_input = st.sidebar.number_input("Số lá bài đã bỏ (Burn):", min_value=0, value=st.session_state.manual_cards)

if st.sidebar.button("🔄 RESET TOÀN BỘ KHAY BÀI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.manual_cards = 0
    st.rerun()

# ĐỒNG BỘ HÓA PHÉP TÍNH CHẠY LIÊN TỤC
analysis_result = calculate_baccarat_v12_6(
    st.session_state.shoe_history, shoe_decks=decks, manual_cards_used=manual_cards_input
)

# DISPLAY INTERFACE
if isinstance(analysis_result, tuple):
    res, remaining_deck, p_pair, b_pair, p_dragon, b_dragon, current_mode, cards_left, is_shoe_logical = analysis_result
    
    p_box = "hud-box neon-player-advantage" if res['Player'] > res['Banker'] else "hud-box"
    b_box = "hud-box neon-banker-advantage" if res['Banker'] > res['Player'] else "hud-box"
    
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.markdown("#### 📊 Xác Suất Cửa Chính")
        st.markdown(f'<div class="{p_box}"><div class="hud-title">🔵 PLAYER</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{b_box}"><div class="hud-title">🔴 BANKER</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box"><div class="hud-title">🟢 TIE (HÒA)</div><div class="hud-value" style="color:#2ecc71;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
        st.caption(f"Chế độ: {current_mode} | Còn lại: {cards_left} lá")
        
    with right_col:
        st.markdown("#### 💎 Radar Cược Phụ Nâng Cao")
        p_pair_style = "badge-alert" if p_pair > 8.33 else "badge-normal"
        b_pair_style = "badge-alert" if b_pair > 8.33 else "badge-normal"
        
        st.markdown(f'<div class="{p_pair_style}"><span style="font-size:11px;color:#aaa;">🔵 CON ĐÔI (P-PAIR)</span><br><b style="font-size:18px;">{p_pair}%</b></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="{b_pair_style}"><span style="font-size:11px;color:#aaa;">🔴 CÁI ĐÔI (B-PAIR)</span><br><b style="font-size:18px;">{b_pair}%</b></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
        
        p_drag_style = "badge-dragon" if p_dragon > 17.0 else "badge-normal"
        b_drag_style = "badge-dragon" if b_dragon > 11.5 else "badge-normal"
        
        st.markdown(f'<div class="{p_drag_style}"><span style="font-size:11px;color:#aaa;">🐉 PLAYER LONG BẢO</span><br><b style="font-size:18px;color:#a29bfe;">{p_dragon}%</b></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="{b_drag_style}"><span style="font-size:11px;color:#aaa;">🐉 BANKER LONG BẢO</span><br><b style="font-size:18px;color:#a29bfe;">{b_dragon}%</b></div>', unsafe_allow_html=True)
else:
    st.error(analysis_result)

st.markdown("---")
st.subheader("🃏 Nhập Kết Quả Ván Vừa Ra")
c_p, c_b = st.columns(2)
with c_p: p_in = st.text_input("PLAYER (Ví dụ: 5,K,2):", key="p_input")
with c_b: b_in = st.text_input("BANKER (Ví dụ: 9,4):", key="b_input")

def parse_input(raw_str):
    if not raw_str: return []
    tokens = raw_str.upper().replace(" ", "").split(",")
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    res = []
    for t in tokens:
        if t in mapping: res.append(mapping[t])
        elif t.isdigit() and 2 <= int(t) <= 10: res.append(int(t))
    return res

if st.button("🚀 GHI NHẬN & PHÂN TÍCH VÁN MỚI", use_container_width=True, type="primary"):
    p_list = parse_input(p_in)
    b_list = parse_input(b_in)
    if p_list or b_list:
        all_cards = p_list + b_list
        st.session_state.shoe_history.extend(all_cards)
        st.rerun()
