import streamlit as st
import pandas as pd

# =========================================================================
# SYSTEM CORE v18.2: ULTRA QUANTUM ENGINE (PATCHED & OPTIMIZED)
# =========================================================================
def calculate_baccarat_v18_ultimate(p_cards, b_cards, shoe_history, shoe_decks=8, 
                                    manual_cards_used=0, manual_games_played=0,
                                    p_wins=0, b_wins=0, tie_wins=0):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}

    if manual_cards_used > total_initial_cards or manual_games_played > int(total_initial_cards / 4):
        return "❌ Bất hợp lý khay bài!", {}, 0.0, 0.0, "LỖI", total_initial_cards, False, []

    detailed_cards_count = len(shoe_history)
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure: deck_structure[card_val] -= 1
        cards_left = total_initial_cards - detailed_cards_count
        mode = "MARKOV CHI TIẾT"
    else:
        cards_removed = max(0, manual_cards_used if manual_cards_used > 0 else int((p_wins * 4.86) + (b_wins * 4.81) + (tie_wins * 5.23)))
        if cards_removed == 0 and manual_games_played > 0:
            cards_removed = int(manual_games_played * 4.852)
        cards_left = max(0, total_initial_cards - cards_removed)
        mode = "BAYES PHÂN RÃ" if cards_removed > 0 else "GỐC"
        if cards_removed > 0:
            consumed_ratio = cards_removed / total_initial_cards
            for card_num in deck_structure:
                reduction = (4 * shoe_decks) * consumed_ratio
                deck_structure[card_num] = max(0.0, (4 * shoe_decks) - reduction)

    invalid_cards_list = []
    for card_num, count in deck_structure.items():
        if count < 0:
            card_labels = {1: "A", 11: "J", 12: "Q", 13: "K"}
            invalid_cards_list.append(card_labels.get(card_num, f"[{card_num}]"))
            
    is_shoe_logical = (len(invalid_cards_list) == 0)
    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: score_deck[0] += count
        else: score_deck[card_num] += count

    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] -= 1

    N_total = float(sum(score_deck))
    if N_total <= 12:
        return "⚠️ Khay thiếu bài!", deck_structure, 0.0, 0.0, mode, cards_left, is_shoe_logical, invalid_cards_list

    p_pair_prob = sum((deck_structure[i]/N_total)*((deck_structure[i]-1)/(N_total-1)) for i in range(1, 14) if deck_structure[i] >= 2)
    p_pair_odds = round(p_pair_prob * 100, 2)

    b_pair_prob = 0.0
    for card_j in range(1, 14):
        cnt_j = deck_structure[card_j]
        if cnt_j >= 2:
            p_not_j = ((N_total - cnt_j) / N_total) * ((N_total - cnt_j - 1) / (N_total - 1))
            b_pair_given_p_not_j = (cnt_j / (N_total - 2)) * ((cnt_j - 1) / (N_total - 3))
            p_one_j = 2 * (cnt_j / N_total) * ((N_total - cnt_j) / (N_total - 1))
            b_pair_given_p_one_j = (max(0.0, cnt_j - 1) / (N_total - 2)) * (max(0.0, cnt_j - 2) / (N_total - 3))
            p_two_j = (cnt_j / N_total) * ((cnt_j - 1) / (N_total - 1))
            b_pair_given_p_two_j = (max(0.0, cnt_j - 2) / (N_total - 2)) * (max(0.0, cnt_j - 3) / (N_total - 3))
            b_pair_prob += (p_not_j * b_pair_given_p_not_j) + (p_one_j * b_pair_given_p_one_j) + (p_two_j * b_pair_given_p_two_j)
    b_pair_odds = round(b_pair_prob * 100, 2)

    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    if (len(p_cards) == 2 and p_score >= 8) or (len(b_cards) == 2 and b_score >= 8):
        if p_score == b_score: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list
        elif p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list
        else: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list

    player_wins, banker_wins, ties = 0.0, 0.0, 0.0
    if len(p_cards) >= 2 and p_score >= 6:
        if b_score <= 5 and len(b_cards) == 2:
            for card3_b in range(10):
                w_b = score_deck[card3_b]
                if w_b > 0:
                    final_b = (b_score + card3_b) % 10
                    if p_score > final_b: player_wins += (w_b / N_total)
                    elif final_b > p_score: banker_wins += (w_b / N_total)
                    else: ties += (w_b / N_total)
        else:
            if p_score > b_score: player_wins += 1.0
            elif b_score > p_score: banker_wins += 1.0
            else: ties += 1.0
    elif len(p_cards) == 2:
        for card3_p in range(10):
            w_p = score_deck[card3_p]
            if w_p <= 0: continue
            prob_p = w_p / N_total
            final_p = (p_score + card3_p) % 10
            score_deck[card3_p] -= 1
            N1 = N_total - 1.0
            b_draws = False
            if b_score <= 2: b_draws = True
            elif b_score == 3 and card3_p != 8: b_draws = True
            elif b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]: b_draws = True
            elif b_score == 5 and card3_p in [4, 5, 6, 7]: b_draws = True
            elif b_score == 6 and card3_p in [6, 7]: b_draws = True
            
            if b_draws and len(b_cards) == 2:
                for card3_b in range(10):
                    w_b = score_deck[card3_b]
                    if w_b > 0:
                        final_b = (b_score + card3_b) % 10
                        combined_weight = prob_p * (w_b / N1)
                        if final_p > final_b: player_wins += combined_weight
                        elif final_b > final_p: banker_wins += combined_weight
                        else: ties += combined_weight
            else:
                if final_p > b_score: player_wins += prob_p
                elif b_score > final_p: banker_wins += prob_p
                else: ties += prob_p
            score_deck[card3_p] += 1

    total_prob = player_wins + banker_wins + ties
    if total_prob == 0: total_prob = 1.0
    return {"Player": round((player_wins / total_prob) * 100, 1), "Banker": round((banker_wins / total_prob) * 100, 1), "Tie": round((ties / total_prob) * 100, 1)}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list

def detect_baccarat_pattern(outcome_list):
    clean_list = [x for x in outcome_list if x in ["Player", "Banker"]]
    if len(clean_list) < 4: return "🔄 Quét...", "#888888"
    last_side = clean_list[-1]
    streak_count = 0
    for item in reversed(clean_list):
        if item == last_side: streak_count += 1
        else: break
    if streak_count >= 4:
        return f"🔥 BỆT { 'P' if last_side == 'Player' else 'B' } ({streak_count}v)", "#ff7675"
    return "📊 Sóng phẳng", "#2ecc71"

# =========================================================================
# THIẾT KẾ INTERFACE & GIỚI HẠN BỀ RỘNG TRÊN DI ĐỘNG (NARROW UI)
# =========================================================================
st.set_page_config(page_title="Oracle Engine Mobile Minimal", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    /* KHÓA CỨNG TOÀN BỘ APP TRÊN MOBILE TRONG KHUNG DI ĐỘNG SIÊU GỌN CHỐNG TRÀN */
    .stAppDeployButton { display:none !important; }
    [data-testid="stMainBlockContainer"] {
        max-width: 360px !important;  /* Bóp nghẹt bề rộng cho vừa khít màn hình điện thoại */
        margin: 0 auto !important;     /* Căn giữa màn hình */
        padding: 10px 5px !important;
    }

    /* ÉP BUỘC GIỮ NGUYÊN HÀNG NGANG (KHÔNG CHO CHỒNG DỌC) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        gap: 6px !important;
    }
    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 0 !important;
    }

    /* THU GỌN PHẦN TỬ TRONG KHỐI KẾT QUẢ */
    .hud-box { padding: 5px 2px; border-radius: 4px; text-align: center; margin-bottom: 4px; border: 1px solid #4f4f4f; background-color: #1a1a1a; }
    .hud-title { font-size: 8px; font-weight: 600; color: #b0b0b0; text-transform: uppercase; }
    .hud-value { font-size: 18px; font-weight: 800; font-family: monospace; margin-top: 1px; }
    .neon-player-advantage { background-color: #0984e3 !important; border: 1px solid #74b9ff !important; }
    .neon-banker-advantage { background-color: #d63031 !important; border: 1px solid #ff7675 !important; }
    .neon-tie-alert { border: 1px solid #2ecc71 !important; }
    
    .validation-hud { padding: 4px 1px; border-radius: 3px; text-align: center; font-weight: 700; font-size: 9px; font-family: monospace; margin-top: 3px; }
    .logic-pass { background-color: rgba(46, 204, 113, 0.1); border: 1px solid #2ecc71; color: #2ecc71; }
    .logic-fail { background-color: rgba(231, 76, 60, 0.1); border: 1px solid #e74c3c; color: #e74c3c; }
    
    .trend-hud { padding: 3px; border-radius: 3px; background-color: #151515; border: 1px dashed #444; margin-top: 3px; text-align: center; }
    .trend-string { font-size: 10px; font-family: monospace; letter-spacing: 0px; font-weight: 800; white-space: nowrap; overflow-x: auto; }
    .trend-alert { font-size: 9px; margin-top: 1px; }
    .char-p { color: #54a0ff; } .char-b { color: #ff7675; } .char-t { color: #2ecc71; }
    
    /* Ép kích cỡ chữ số Metric nhỏ nhất có thể */
    [data-testid="stMetricValue"] { font-size: 14px !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { font-size: 9px !important; }
    div[data-testid="stMetric"] { padding: 0px !important; margin: 0px !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

# Khởi tạo Session State
if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None

# --- KHỞI TẠO KEY CHO Ô NHẬP LIỆU ĐỂ PHỤC VỤ AUTOMATIC CLEAR ---
if 'p_input_val' not in st.session_state: st.session_state.p_input_val = ""
if 'b_input_val' not in st.session_state: st.session_state.b_input_val = ""

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("⚙️ THÔNG SỐ KHAY")
decks = st.sidebar.selectbox("Số bộ bài:", [8, 6, 4], index=0)
manual_cards = st.sidebar.number_input("Số lá đã chia:", min_value=0, value=0)
manual_games = st.sidebar.number_input("Số ván đã chạy:", min_value=0, value=0)
p_wins_input = st.sidebar.number_input("🔵 PLAYER thắng:", min_value=0, value=0)
b_wins_input = st.sidebar.number_input("🔴 BANKER thắng:", min_value=0, value=0)
tie_wins_input = st.sidebar.number_input("🟢 TIE thắng:", min_value=0, value=0)

if st.sidebar.button("🔄 RESET KHAY BÀI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.outcome_history = []
    st.session_state.last_results = None
    st.session_state.p_input_val = ""
    st.session_state.b_input_val = ""
    st.rerun()

# --- INPUT PANEL (PHÍA TRÊN) ---
st.write("<b style='font-size:13px;'>🃏 Nhập Bài Ván Vừa Ra</b>", unsafe_allow_html=True)
col_p, col_b = st.columns(2)
with col_p: 
    p_input = st.text_input("PLAYER:", key="p_input_val", placeholder="Ví dụ: 5,K")
with col_b: 
    b_input = st.text_input("BANKER:", key="b_input_val", placeholder="Ví dụ: J,7")

def clean_and_parse_input(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().replace(" ", "")
    tokens = []
    i = 0
    if "," in normalized:
        for p in normalized.split(","):
            p_clean = "".join([c for c in p if c in "2345678910AJQK"])
            if p_clean: tokens.append(p_clean)
    else:
        while i < len(normalized):
            if normalized[i:i+2] == "10": tokens.append("10"); i += 2
            elif normalized[i] in "23456789AJQK": tokens.append(normalized[i]); i += 1
            else: i += 1
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    return [mapping[t] if t in mapping else int(t) for t in tokens if t in mapping or (t.isdigit() and 2 <= int(t) <= 10)]

# --- NÚT TÍNH TOÁN & XỬ LÝ XÓA DỮ LIỆU ---
if st.button("🚀 TÍNH TOÁN VÁN TIẾP THEO", use_container_width=True, type="primary"):
    if not p_input.strip() and not b_input.strip():
        st.warning("⚠️ Chưa nhập bài!")
    else:
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        
        if p_list or b_list:
            # 1. Thực hiện tính toán bằng dữ liệu vừa lấy
            core_output = calculate_baccarat_v18_ultimate(
                p_list, b_list, st.session_state.shoe_history, shoe_decks=decks,
                manual_cards_used=manual_cards, manual_games_played=manual_games,
                p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
            )
            
            if not isinstance(core_output, str):
                st.session_state.last_results = core_output
                
                p_score_eval = sum([0 if c >= 10 else c for c in p_list]) % 10
                b_score_eval = sum([0 if c >= 10 else c for c in b_list]) % 10
                if p_score_eval > b_score_eval: st.session_state.outcome_history.append("Player")
                elif b_score_eval > p_score_eval: st.session_state.outcome_history.append("Banker")
                else: st.session_state.outcome_history.append("Tie")
                st.session_state.shoe_history.extend(p_list + b_list)
            
            # 2. XÓA SẠCH CHỮ TRÊN Ô NHẬP LIỆU NGAY LẬP TỨC
            st.session_state.p_input_val = ""
            st.session_state.b_input_val = ""
            st.rerun()

st.markdown("<hr style='margin: 8px 0;'/>", unsafe_allow_html=True)

# --- OUTPUT PANEL (2 CỘT SONG SONG KHÓA CỨNG + THU GỌN BỀ RỘNG) ---
if st.session_state.last_results:
    res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical, invalid_cards = st.session_state.last_results
    
    p_box_css = "hud-box"
    b_box_css = "hud-box"
    tie_box_css = "hud-box"
    if res['Player'] > res['Banker']: p_box_css = "hud-box neon-player-advantage"
    elif res['Banker'] > res['Player']: b_box_css = "hud-box neon-banker-advantage"
    if res['Tie'] > 12.5: tie_box_css = "hud-box neon-tie-alert"
    
    left_col, right_col = st.columns(2)
    
    # --- CỘT TRÁI: CỬA CHÍNH ---
    with left_col:
        st.markdown("<div style='font-size:9px; color:#aaa; font-weight:bold; margin-bottom:2px; text-align:center;'>📊 CỬA CHÍNH</div>", unsafe_allow_html=True)
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{tie_box_css}"><div class="hud-title">🟢 HÒA</div><div class="hud-value" style="color: #2ecc71;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
    
    # --- CỘT PHẢI: CỬA ĐÔI & LOGIC ---
    with right_col:
        st.markdown("<div style='font-size:9px; color:#aaa; font-weight:bold; margin-bottom:2px; text-align:center;'>💎 ĐÔI & LOGIC</div>", unsafe_allow_html=True)
        st.metric("🔵 CON ĐÔI", f"{p_pair}%")
        st.metric("🔴 CÁI ĐÔI", f"{b_pair}%")
        
        if is_shoe_logical: 
            st.markdown('<div class="validation-hud logic-pass">✔ KHAY OK</div>', unsafe_allow_html=True)
        else: 
            st.markdown('<div class="validation-hud logic-fail">⚠️ LỖI KHAY</div>', unsafe_allow_html=True)
        
        if st.session_state.outcome_history:
            trend_letters = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.outcome_history]
            pattern_msg, pattern_color = detect_baccarat_pattern(st.session_state.outcome_history)
            st.markdown(f'<div class="trend-hud"><div class="trend-string">{" ".join(trend_letters[-5:])}</div><div class="trend-alert" style="color: {pattern_color}; font-weight: bold;">{pattern_msg}</div></div>', unsafe_allow_html=True)
else:
    st.info("🔮 Sẵn sàng. Hãy nạp điểm.")
