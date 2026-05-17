import streamlit as st

# =========================================================================
# 1. SỬA LỖI ĐỒ HỌA MOBILE (CHỐNG TRÀN MÀN HÌNH ĐIỆN THOẠI)
# =========================================================================
st.set_page_config(page_title="Oracle Mobile v18", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    /* Cấu hình nút bấm và các ô hiển thị vừa vặn với mọi màn hình điện thoại */
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; width: 100% !important; }
    div[data-testid="stColumn"] { flex: 1 1 50% !important; padding: 2px !important; }
    .hud-box { padding: 14px; border-radius: 8px; text-align: center; margin-bottom: 8px; border: 1px solid #444; background-color: #1a1a1a; }
    .hud-title { font-size: 11px; font-weight: 700; color: #888; letter-spacing: 0.5px; }
    .hud-value { font-size: 28px; font-weight: 800; font-family: monospace; margin-top: 2px; }
    .win-p { background-color: #0c2461 !important; border: 2px solid #1e3799 !important; color: #54a0ff !important; }
    .win-b { background-color: #b33939 !important; border: 2px solid #ff5252 !important; color: #ff7675 !important; }
    .trend-bar { padding: 8px; border-radius: 6px; background-color: #111; border: 1px dashed #555; margin-top: 8px; overflow-x: auto; }
    .trend-str { font-size: 16px; font-family: monospace; letter-spacing: 4px; font-weight: 800; white-space: nowrap; }
    .c-p { color: #54a0ff; } .c-b { color: #ff7675; } .c-t { color: #2ecc71; }
    </style>
    """, 
    unsafe_allow_html=True
)

# Sửa lỗi tràn bộ nhớ (Memory Leak) bằng cách thiết lập bộ nhớ đệm an toàn
if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None

# =========================================================================
# 2. SỬA LỖI TOÁN HỌC (TỰ ĐỘNG CÂN BẰNG KHAY BÀI KHI THIẾU DỮ LIỆU)
# =========================================================================
def calculate_baccarat(p_cards, b_cards, shoe_history, shoe_decks=8):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    for card_val in shoe_history:
        if card_val in deck_structure: deck_structure[card_val] -= 1
        
    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: score_deck[0] += count
        else: score_deck[card_num] += count
        
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] -= 1
        
    N_total = float(sum(score_deck))
    # Sửa lỗi chia cho ván bài trống (ZeroDivisionError)
    if N_total <= 6: return {"Player": 45.8, "Banker": 44.6, "Tie": 9.6}
    
    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10
    
    if (len(p_cards) == 2 and p_score >= 8) or (len(b_cards) == 2 and b_score >= 8):
        if p_score == b_score: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}
        elif p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}
        else: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}
        
    player_wins, banker_wins, ties = 0.0, 0.0, 0.0
    if len(p_cards) >= 2 and p_score >= 6:
        if b_score <= 5 and len(b_cards) == 2:
            for card3_b in range(10):
                w_b = score_deck[card3_b]
                if w_b > 0:
                    prob_b = w_b / N_total
                    final_b = (b_score + card3_b) % 10
                    if p_score > final_b: player_wins += prob_b
                    elif final_b > p_score: banker_wins += prob_b
                    else: ties += prob_b
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
                        prob_b = w_b / N1
                        final_b = (b_score + card3_b) % 10
                        combined_weight = prob_p * prob_b
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
    return {
        "Player": round((player
