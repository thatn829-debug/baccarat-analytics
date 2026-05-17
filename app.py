import streamlit as st

st.set_page_config(page_title="Oracle Baccarat v18", page_icon="🔮", layout="centered")

# Giao diện nút bấm to, rõ nét trên màn hình Chrome điện thoại
st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; width: 100% !important; }
    div[data-testid="stColumn"] { flex: 1 1 50% !important; padding: 2px !important; }
    .hud-box { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px; border: 1px solid #444; background-color: #1e1e1e; }
    .hud-title { font-size: 12px; font-weight: 700; color: #aaa; }
    .hud-value { font-size: 32px; font-weight: 800; font-family: monospace; margin-top: 4px; }
    .win-p { background-color: #0c2461 !important; border: 2px solid #1e3799 !important; color: #54a0ff !important; }
    .win-b { background-color: #b33939 !important; border: 2px solid #ff5252 !important; color: #ff7675 !important; }
    .trend-bar { padding: 10px; border-radius: 8px; background-color: #111; border: 1px dashed #555; margin-top: 10px; overflow-x: auto; }
    .trend-str { font-size: 18px; font-family: monospace; letter-spacing: 6px; font-weight: 800; white-space: nowrap; }
    .c-p { color: #54a0ff; } .c-b { color: #ff7675; } .c-t { color: #2ecc71; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None

def calculate_baccarat(p_cards, b_cards, shoe_history, shoe_decks=8):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    for card_val in shoe_history:
        if card_val in deck_structure: deck_structure[card_val] -= 1
    cards_left = total_initial_cards - len(shoe_history)
    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: score_deck[0] += count
        else: score_deck[card_num] += count
    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] -= 1
    N_total = float(sum(score_deck))
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
        "Player": round((player_wins / total_prob) * 100, 1),
        "Banker": round((banker_wins / total_prob) * 100, 1),
        "Tie": round((ties / total_prob) * 100, 1)
    }

st.title("🔮 Oracle Mobile v18")
decks = st.selectbox("Số bộ bài:", [8, 6, 4], index=0)

if st.session_state.last_results:
    res = st.session_state.last_results
    p_style = "hud-box win-p" if res['Player'] > res['Banker'] else "hud-box"
    b_style = "hud-box win-b" if res['Banker'] > res['Player'] else "hud-box"
    col1, col2 = st.columns(2)
    with col1: st.markdown(f'<div class="{p_style}"><div class="hud-title">🔵 PLAYER</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="{b_style}"><div class="hud-title">🔴 BANKER</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
    if st.session_state.outcome_history:
        letters = [f'<span class="c-p">P</span>' if x == "Player" else (f'<span class="c-b">B</span>' if x == "Banker" else '<span class="c-t">T</span>') for x in st.session_state.outcome_history]
        st.markdown(f'<div class="trend-bar"><div class="trend-str">{" ".join(letters)}</div></div>', unsafe_allow_html=True)

def parse_mobile_input(raw):
    if not raw: return []
    raw = raw.upper().replace(" ", "")
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13, '0': 10, 'T': 10}
    cards = []
    i = 0
    while i < len(raw):
        if raw[i:i+2] == '10': cards.append(10); i += 2
        elif raw[i] in mapping: cards.append(mapping[raw[i]]); i += 1
        elif raw[i].isdigit(): cards.append(int(raw[i])); i += 1
        else: i += 1
    return cards

c_p, c_b = st.columns(2)
with c_p: p_in = st.text_input("🔵 Bài PLAYER:", placeholder="Gõ liền ví dụ: 5K")
with c_b: b_in = st.text_input("🔴 Bài BANKER:", placeholder="Gõ liền ví dụ: J7")

if st.button("🚀 TÍNH XÁC SUẤT VÁN TIẾP", use_container_width=True, type="primary"):
    p_list = parse_mobile_input(p_in)
    b_list = parse_mobile_input(b_in)
    if p_list or b_list:
        res = calculate_baccarat(p_list, b_list, st.session_state.shoe_history, shoe_decks=decks)
        st.session_state.last_results = res
        st.session_state.shoe_history.extend(p_list + b_list)
        p_sc = sum([0 if c >= 10 else c for c in p_list]) % 10
        b_sc = sum([0 if c >= 10 else c for c in b_list]) % 10
        if p_sc > b_sc: st.session_state.outcome_history.append("Player")
        elif b_sc > p_sc: st.session_state.outcome_history.append("Banker")
        else: st.session_state.outcome_history.append("Tie")
        st.rerun()

if st.button("🔄 LÀM MỚI KHAY BÀI", use_container_width=True):
    st.session_state.shoe_history, st.session_state.outcome_history, st.session_state.last_results = [], [], None
    st.rerun()
