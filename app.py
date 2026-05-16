import streamlit as st
import pandas as pd

# =========================================================================
# SYSTEM CORE v12.7: DEEP SIMULATION MATRIX (PAIRS & EXACT DRAGON BONUS)
# =========================================================================
def calculate_baccarat_v12_7(shoe_history, shoe_decks=8):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    # 1. KHẤU TRỪ BÀI THEO LỊCH SỬ THỰC TẾ
    for card_val in shoe_history:
        if card_val in deck_structure:
            deck_structure[card_val] -= 1
            
    N = float(sum(deck_structure.values()))
    cards_left = int(N)
    
    if N <= 6:
        return "⚠️ Khay bài đã vơi quá giới hạn!", 0, 0, 0, 0, 0, 0, cards_left, False

    # 2. TOÁN HỌC CỬA ĐÔI (PAIRS) - CHUẨN V12.5
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

    # 3. CHUẨN HÓA SANG MÔ HÌNH ĐIỂM (MODULO 10) ĐỂ GIẢ LẬP LÁ THỨ 3
    # Mảng lưu trữ trọng số xác suất xuất hiện từ điểm 0 đến 9
    card_probs = {i: 0.0 for i in range(10)}
    for card_num, count in deck_structure.items():
        val = 0 if card_num >= 10 else card_num
        card_probs[val] += count / N

    # KHỞI TẠO MA TRẬN KẾT QUẢ
    p_win_total = 0.0
    b_win_total = 0.0
    tie_total = 0.0
    p_dragon_total = 0.0
    b_dragon_total = 0.0

    # GIẢ LẬP ĐỘC LẬP TOÀN BỘ KỊCH BẢN ĐIỂM SỐ BAN ĐẦU (2 LÁ ĐẦU TIÊN)
    for p2_score in range(10):
        prob_p2 = card_probs[p2_score]
        if prob_p2 == 0: continue
        for b2_score in range(10):
            prob_b2 = card_probs[b2_score]
            if prob_b2 == 0: continue
            
            p2_b2_prob = prob_p2 * prob_b2
            
            # Kiểm tra Thắng tự nhiên (Natural 8, 9)
            is_p_nat = p2_score in [8, 9]
            is_b_nat = b2_score in [8, 9]
            
            if is_p_nat or is_b_nat:
                if p2_score > b2_score:
                    p_win_total += p2_b2_prob
                    if is_p_nat: p_dragon_total += p2_b2_prob  # Thắng tự nhiên (Ăn 1:1)
                elif b2_score > p2_score:
                    b_win_total += p2_b2_prob
                    if is_b_nat: b_dragon_total += p2_b2_prob  # Thắng tự nhiên (Ăn 1:1)
                else:
                    tie_total += p2_b2_prob
                continue # Kết thúc ván bài ngay lập tức nếu có Natural
                
            # -----------------------------------------------------------------
            # GIẢ LẬP CHUYÊN SÂU LÁ THỨ 3 (DEEP DRAWING ENGINE)
            # -----------------------------------------------------------------
            # Bước 1: Xác định xem Player có rút lá thứ 3 không
            p_draws = (p2_score <= 5)
            
            if not p_draws:
                # Player đứng (6 hoặc 7 điểm). Banker rút nếu Banker từ 0 đến 5.
                if b2_score <= 5:
                    for b3 in range(10):
                        prob_b3 = card_probs[b3]
                        b_final = (b2_score + b3) % 10
                        final_prob = p2_b2_prob * prob_b3
                        
                        if b_final > p2_score:
                            b_win_total += final_prob
                            if (b_final - p2_score) >= 4: b_dragon_total += final_prob
                        elif p2_score > b_final:
                            p_win_total += final_prob
                            if (p2_score - b_final) >= 4: p_dragon_total += final_prob
                        else:
                            tie_total += final_prob
                else:
                    # Cả hai bên đều đứng (6 hoặc 7)
                    if b2_score > p2_score:
                        b_win_total += p2_b2_prob
                        if (b2_score - p2_score) >= 4: b_dragon_total += p2_b2_prob
                    elif p2_score > b2_score:
                        p_win_total += p2_b2_prob
                        if (p2_score - b2_score) >= 4: p_dragon_total += p2_b2_prob
                    else:
                        tie_total += p2_b2_prob
            else:
                # Player rút lá thứ 3 (Quét qua tất cả khả năng của lá thứ 3 Player)
                for p3 in range(10):
                    prob_p3 = card_probs[p3]
                    p_final = (p2_score + p3) % 10
                    p3_prob = p2_b2_prob * prob_p3
                    
                    # Áp dụng Luật rút bài chuẩn Quốc tế của Banker dựa trên lá thứ 3 của Player (p3)
                    b_draws = False
                    if b2_score <= 2: b_draws = True
                    elif b2_score == 3 and p3 != 8: b_draws = True
                    elif b2_score == 4 and p3 in [2, 3, 4, 5, 6, 7]: b_draws = True
                    elif b2_score == 5 and p3 in [4, 5, 6, 7]: b_draws = True
                    elif b2_score == 6 and p3 in [6, 7]: b_draws = True
                    
                    if b_draws:
                        # Banker rút lá thứ 3
                        for b3 in range(10):
                            prob_b3 = card_probs[b3]
                            b_final = (b2_score + b3) % 10
                            final_prob = p3_prob * prob_b3
                            
                            if p_final > b_final:
                                p_win_total += final_prob
                                if (p_final - b_final) >= 4: p_dragon_total += final_prob
                            elif b_final > p_final:
                                b_win_total += final_prob
                                if (b_final - p_final) >= 4: b_dragon_total += final_prob
                            else:
                                tie_total += final_prob
                    else:
                        # Banker đứng
                        if p_final > b2_score:
                            p_win_total += p3_prob
                            if (p_final - b2_score) >= 4: p_dragon_total += p3_prob
                        elif b2_score > p_final:
                            b_win_total += p3_prob
                            if (b2_score - p_final) >= 4: b_dragon_total += p3_prob
                        else:
                            tie_total += p3_prob

    # Chuẩn hóa tỷ lệ phần trăm đầu ra
    total_all = p_win_total + b_win_total + tie_total
    if total_all == 0: total_all = 1.0
    
    odds_res = {
        "Player": round((p_win_total / total_all) * 100, 2),
        "Banker": round((b_win_total / total_all) * 100, 2),
        "Tie": round((tie_total / total_all) * 100, 2)
    }
    
    p_dragon_odds = round((p_dragon_total / total_all) * 100, 2)
    b_dragon_odds = round((b_dragon_total / total_all) * 100, 2)

    return odds_res, p_pair_odds, b_pair_odds, p_dragon_odds, b_dragon_odds, cards_left, True

# =========================================================================
# GIAO DIỆN HIỂN THỊ CHUYÊN SÂU v12.7
# =========================================================================
st.set_page_config(page_title="Oracle Deep Simulation v12.7", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stColumn"] { width: 50% !important; min-width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    .hud-box { padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 10px; border: 1px solid #4f4f4f; background-color: #111; }
    .hud-title { font-size: 11px; font-weight: 600; color: #b0b0b0; }
    .hud-value { font-size: 28px; font-weight: 800; font-family: monospace; }
    .neon-p { background-color: #0984e3 !important; border: 2px solid #74b9ff !important; box-shadow: 0 0 10px rgba(9, 132, 227, 0.5); }
    .neon-b { background-color: #d63031 !important; border: 2px solid #ff7675 !important; box-shadow: 0 0 10px rgba(214, 48, 49, 0.5); }
    .badge-normal { background-color: #1e1e1e; padding: 8px; border-radius: 6px; text-align: center; border: 1px solid #333; }
    .badge-alert { background-color: #d35400; padding: 8px; border-radius: 6px; text-align: center; border: 2px solid #e67e22; box-shadow: 0 0 10px rgba(230, 126, 34, 0.5); }
    .badge-dragon { background-color: #4a148c; padding: 8px; border-radius: 6px; text-align: center; border: 2px solid #8e24aa; box-shadow: 0 0 12px rgba(142, 36, 170, 0.6); }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None

if st.session_state.last_results is None:
    st.session_state.last_results = calculate_baccarat_v12_7(st.session_state.shoe_history)

# SIDEBAR CONFIG
st.sidebar.header("⚙️ CONFIG v12.7")
decks = st.sidebar.selectbox("Số bộ bài:", [8, 6], index=0)
if st.sidebar.button("🔄 REFRESH SHOE", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.last_results = calculate_baccarat_v12_7([])
    st.rerun()

# RENDER
if isinstance(st.session_state.last_results, tuple):
    res, p_pair, b_pair, p_dragon, b_dragon, cards_left, is_ok = st.session_state.last_results
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📊 Cửa Chính (Modulo 10)")
        st.markdown(f'<div class="hud-box {"neon-p" if res["Player"]>res["Banker"] else ""}"><div class="hud-title">🔵 PLAYER</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box {"neon-b" if res["Banker"]>res["Player"] else ""}"><div class="hud-title">🔴 BANKER</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box"><div class="hud-title">🟢 TIE</div><div class="hud-value" style="color:#2ecc71;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
        st.caption(f"Bài còn lại trong khay: {cards_left} lá")
        
    with col2:
        st.markdown("#### 🎯 Bộ Lọc Cược Phụ Cao Cấp")
        # Định dạng Đôi
        p_p_style = "badge-alert" if p_pair > 8.33 else "badge-normal"
        b_p_style = "badge-alert" if b_pair > 8.33 else "badge-normal"
        st.markdown(f'<div class="{p_p_style}"><span style="font-size:11px;color:#aaa;">🔵 CON ĐÔI</span><br><b style="font-size:18px;">{p_pair}%</b></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="{b_p_style}"><span style="font-size:11px;color:#aaa;">🔴 CÁI ĐÔI</span><br><b style="font-size:18px;">{b_pair}%</b></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
        
        # Ngưỡng kích hoạt chuẩn toán học Deep Sim cho Long Bảo: Player > 16.5%, Banker > 10.8%
        p_d_style = "badge-dragon" if p_dragon > 16.5 else "badge-normal"
        b_d_style = "badge-dragon" if b_dragon > 10.8 else "badge-normal"
        st.markdown(f'<div class="{p_d_style}"><span style="font-size:11px;color:#aaa;">🐉 PLAYER LONG BẢO</span><br><b style="font-size:18px;color:#e040fb;">{p_dragon}%</b></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="{b_d_style}"><span style="font-size:11px;color:#aaa;">🐉 BANKER LONG BẢO</span><br><b style="font-size:18px;color:#e040fb;">{b_dragon}%</b></div>', unsafe_allow_html=True)

st.markdown("---")
st.subheader("🃏 Ghi Nhận Dữ Liệu")
c_p, c_b = st.columns(2)
with c_p: p_in = st.text_input("PLAYER CARD:", key="p_input")
with c_b: b_in = st.text_input("BANKER CARD:", key="b_input")

def parse_input(raw_str):
    if not raw_str: return []
    tokens = raw_str.upper().replace(" ", "").split(",")
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    res = []
    for t in tokens:
        if t in mapping: res.append(mapping[t])
        elif t.isdigit() and 2 <= int(t) <= 10: res.append(int(t))
    return res

if st.button("🚀 EXECUTE SIMULATION", use_container_width=True, type="primary"):
    p_list = parse_input(p_in)
    b_list = parse_input(b_in)
    if p_list or b_list:
        st.session_state.shoe_history.extend(p_list + b_list)
        st.session_state.last_results = calculate_baccarat_v12_7(st.session_state.shoe_history, shoe_decks=decks)
        st.rerun()
