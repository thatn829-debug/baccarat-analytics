import streamlit as st
import pandas as pd

# =========================================================================
# INTERFACE DESIGN & MOBILE OPTIMIZATION
# =========================================================================
st.set_page_config(page_title="Oracle Mobile Engine v18.2", page_icon="🔮", layout="centered")

# CSS cấu trúc lại giao diện để các nút bấm to, rõ, dễ bấm trên màn hình cảm ứng điện thoại
st.markdown(
    """
    <style>
    /* Cấu hình cột hiển thị dọc hoặc chia đều trên mobile */
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; width: 100% !important; }
    div[data-testid="stColumn"] { flex: 1 1 50% !important; padding: 3px !important; }
    
    /* Hộp HUD hiển thị kết quả */
    .hud-box { padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 8px; border: 1px solid #4f4f4f; background-color: #1a1a1a; }
    .hud-title { font-size: 11px; font-weight: 600; color: #b0b0b0; letter-spacing: 0.5px; }
    .hud-value { font-size: 28px; font-weight: 800; font-family: monospace; margin-top: 2px; }
    
    /* Hiệu ứng màu viền khi có lợi thế */
    .neon-player-advantage { background-color: #0984e3 !important; border: 2px solid #74b9ff !important; }
    .neon-banker-advantage { background-color: #d63031 !important; border: 2px solid #ff7675 !important; }
    
    /* Thanh hiển thị lịch sử xúc xắc/xu hướng */
    .trend-hud { padding: 10px; border-radius: 6px; background-color: #151515; border: 1px dashed #444; margin-top: 8px; }
    .trend-string { font-size: 16px; font-family: monospace; letter-spacing: 4px; font-weight: 800; white-space: nowrap; overflow-x: auto; }
    .char-p { color: #54a0ff; } .char-b { color: #ff7675; } .char-t { color: #2ecc71; }
    </style>
    """, 
    unsafe_allow_html=True
)

# Khởi tạo dữ liệu lưu trữ ván bài
if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None

# =========================================================================
# CODE THUẬT TOÁN GỐC CORE v18.2 (GIỮ NGUYÊN HOÀN TOÀN LOGIC TOÁN HỌC)
# =========================================================================
def calculate_baccarat_v18_ultimate(p_cards, b_cards, shoe_history, shoe_decks=8):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}

    detailed_cards_count = len(shoe_history)
    for card_val in shoe_history:
        if card_val in deck_structure:
            deck_structure[card_val] -= 1
    cards_left = total_initial_cards - detailed_cards_count

    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: score_deck[0] += count
        else: score_deck[card_num] += count

    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] -= 1

    N_total = float(sum(score_deck))
    if N_total <= 12:
        return {"Player": 33.3, "Banker": 33.3, "Tie": 33.3}, 0.0, 0.0, cards_left

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
        if p_score == b_score: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, p_pair_odds, b_pair_odds, cards_left
        elif p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, p_pair_odds, b_pair_odds
