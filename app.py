import streamlit as st

# =========================================================================
# SYSTEM CORE v12.8: REAL-TIME NON-REPLACEMENT COMBINATORIAL ENGINE
# =========================================================================
def calculate_baccarat_v12_8(shoe_history, shoe_decks=8):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: int(4 * shoe_decks) for i in range(1, 14)}
    
    # 1. KHẤU TRỪ BÀI THỰC TẾ THEO ĐỊNH DANH VẬT LÝ
    for card_val in shoe_history:
        if card_val in deck_structure:
            deck_structure[card_val] -= 1
            
    total_cards_left = sum(deck_structure.values())
    if total_cards_left <= 6:
        return "⚠️ Khay bài đã vơi quá giới hạn an toàn!", 0, 0, 0, 0, 0, 0, total_cards_left, False

    # CHUẨN HÓA SANG HỆ ĐIỂM BACCARAT (0-9) GIỮ NGUYÊN SỐ LƯỢNG LÁ THỰC TẾ
    cards_count_by_score = {i: 0 for i in range(10)}
    for card_num, count in deck_structure.items():
        val = 0 if card_num >= 10 else card_num
        cards_count_by_score[val] += count

    # CHUẨN BỊ BIẾN TÍCH LŨY TỔ HỢP XÁC SUẤT
    p_win_prob = 0.0
    b_win_prob = 0.0
    tie_prob = 0.0
    
    p_dragon_prob = 0.0
    b_dragon_prob = 0.0

    # Lấy tổng số bài hiện tại làm mẫu số gốc
    N = float(total_cards_left)

    # -----------------------------------------------------------------
    # VÒNG LẶP TỔ HỢP TÍCH CHẬP CHUỖI PHI LẶP (NON-REPLACEMENT COMBINATORICS)
    # Giả lập chính xác quy trình chia bài: P1 -> B1 -> P2 -> B2
    # -----------------------------------------------------------------
    for p1 in range(10):
        c_p1 = cards_count_by_score[p1]
        if c_p1 == 0: continue
        prob_p1 = c_p1 / N
        
        # Khấu trừ lá P1
        cards_count_by_score[p1] -= 1
        
        for b1 in range(10):
            c_b1 = cards_count_by_score[b1]
            if c_b1 == 0: continue
            prob_b1 = c_b1 / (N - 1)
            
            # Khấu trừ lá B1
            cards_count_by_score[b1] -= 1
            
            for p2 in range(10):
                c_p2 = cards_count_by_score[p2]
                if c_p2 == 0: continue
                prob_p2 = c_p2 / (N - 2)
                
                # Khấu trừ lá P2
                cards_count_by_score[p2] -= 1
                
                for b2 in range(10):
                    c_b2 = cards_count_by_score[b2]
                    if c_b2 == 0: continue
                    prob_b2 = c_b2 / (N - 3)
                    
                    # Xác suất xảy ra tổ hợp 4 lá đầu tiên này là tích chuỗi phụ thuộc:
                    branch_prob = prob_p1 * prob_b1 * prob_p2 * prob_b2
                    
                    p2_score = (p1 + p2) % 10
                    b2_score = (b1 + b2) % 10
                    
                    is_p_nat = p2_score in [8, 9]
                    is_b_nat = b2_score in [8, 9]
                    
                    # Trường hợp thắng tự nhiên (Natural)
                    if is_p_nat or is_b_nat:
                        if p2_score > b2_score:
                            p_win_prob += branch_prob
                            if is_p_nat: p_dragon_prob += branch_prob
                        elif b2_score > p2_score:
                            b_win_prob += branch_prob
                            if is_b_nat: b_dragon_prob += branch_prob
                        else:
                            tie_prob += branch_prob
                        continue
                    
                    # ---------------------------------------------------------
                    # XỬ LÝ LÁ THỨ 3 VỚI SỰ KHẤU TRỪ CHUẨN XÁC TUYỆT ĐỐI
                    # ---------------------------------------------------------
                    p_draws = (p2_score <= 5)
                    
                    if not p_draws:
                        # Player đứng (6, 7). Banker rút nếu từ 0-5
                        if b2_score <= 5:
                            for b3 in range(10):
                                c_b3 = cards_count_by_score[b3]
                                if c_b3 == 0: continue
                                prob_b3 = c_b3 / (N - 4)
                                
                                b_final = (b2_score + b3) % 10
                                final_prob = branch_prob * prob_b3
                                
                                if b_final > p2_score:
                                    b_win_prob += final_prob
                                    if (b_final - p2_score) >= 4: b_dragon_prob += final_prob
                                elif p2_score > b_final:
                                    p_win_prob += final_prob
                                    if (p2_score - b_final) >= 4: p_dragon_prob += final_prob
                                else:
                                    tie_prob += final_prob
                        else:
                            # Cả hai bên đều đứng
                            if b2_score > p2_score:
                                b_win_prob += branch_prob
                                if (b2_score - p2_score) >= 4: b_dragon_prob += branch_prob
                            elif p2_score > b2_score:
                                p_win_prob += branch_prob
                                if (p2_score - b2_score) >= 4: p_dragon_prob += branch_prob
                            else:
                                tie_prob += branch_prob
                    else:
                        # Player rút lá thứ 3
                        # Khấu trừ lá B2 trước khi Player rút lá 3
                        cards_count_by_score[b2] -= 1
                        
                        for p3 in range(10):
                            c_p3 = cards_count_by_score[p3]
                            if c_p3 == 0: continue
                            prob_p3 = c_p3 / (N - 4)
                            
                            p_final = (p2_score + p3) % 10
                            p3_branch_prob = branch_prob * prob_p3
                            
                            # Khấu trừ lá P3 để tính toán nhánh bốc bài tiếp theo của Banker
                            cards_count_by_score[p3] -= 1
                            
                            # Luật rút bài của Banker dựa trên lá thứ 3 của Player (p3)
                            b_draws = False
                            if b2_score <= 2: b_draws = True
                            elif b2_score == 3 and p3 != 8: b_draws = True
                            elif b2_score == 4 and p3 in [2, 3, 4, 5, 6, 7]: b_draws = True
                            elif b2_score == 5 and p3 in [4, 5, 6, 7]: b_draws = True
                            elif b2_score == 6 and p3 in [6, 7]: b_draws = True
                            
                            if b_draws:
                                for b3 in range(10):
                                    c_b3 = cards_count_by_score[b3]
                                    if c_b3 == 0: continue
                                    prob_b3 = c_b3 / (N - 5)
                                    
                                    b_final = (b2_score + b3) % 10
                                    final_prob = p3_branch_prob * prob_b3
                                    
                                    if p_final > b_final:
                                        p_win_prob += final_prob
                                        if (p_final - b_final) >= 4: p_dragon_prob += final_prob
                                    elif b_final > p_final:
                                        b_win_prob += final_prob
                                        if (b_final - p_final) >= 4: b_dragon_prob += final_prob
                                    else:
                                        tie_prob += final_prob
                            else:
                                # Banker đứng
                                if p_final > b2_score:
                                    p_win_prob += p3_branch_prob
                                    if (p_final - b2_score) >= 4: p_dragon_prob += p3_branch_prob
                                elif b2_score > p_final:
                                    b_win_prob += p3_branch_prob
                                    if (b2_score - p_final) >= 4: b_dragon_prob += p3_branch_prob
                                else:
                                    tie_prob += p3_branch_prob
                                    
                            # Trả lại lá P3 cho vòng lặp kế tiếp
                            cards_count_by_score[p3] += 1
                        
                        # Trả lại lá B2
                        cards_count_by_score[b2] += 1
                        
                    # Hoàn trả lá B2 sau khi kết thúc nhánh lặp b2
                    pass
                
                # Trả lại lá P2
                cards_count_by_score[p2] += 1
            
            # Trả lại lá B1
            cards_count_by_score[b1] += 1
            
        # Trả lại lá P1
        cards_count_by_score[p1] += 1

    # -----------------------------------------------------------------
    # TOÁN HỌC CỬA ĐÔI (PAIRS) - ĐỒNG BỘ MA TRẬN PHI LẶP CHUỖI V12.5
    # -----------------------------------------------------------------
    p_pair_prob_calc = sum((deck_structure[i]/N)*((deck_structure[i]-1)/(N-1)) for i in range(1, 14) if deck_structure[i] >= 2)
    p_pair_odds = round(p_pair_prob_calc * 100, 2)

    b_pair_prob_calc = 0.0
    for card_j in range(1, 14):
        cnt_j = deck_structure[card_j]
        if cnt_j >= 2:
            p_not_j = ((N - cnt_j) / N) * ((N - cnt_j - 1) / (N - 1))
            b_pair_given_p_not_j = (cnt_j / (N - 2)) * ((cnt_j - 1) / (N - 3))
            p_one_j = 2 * (cnt_j / N) * ((N - cnt_j) / (N - 1))
            b_pair_given_p_one_j = (max(0.0, float(cnt_j - 1)) / (N - 2)) * (max(0.0, float(cnt_j - 2)) / (N - 3))
            p_two_j = (cnt_j / N) * ((cnt_j - 1) / (N - 1))
            b_pair_given_p_two_j = (max(0.0, float(cnt_j - 2)) / (N - 2)) * (max(0.0, float(cnt_j - 3)) / (N - 3))
            b_pair_prob_calc += (p_not_j * b_pair_given_p_not_j) + (p_one_j * b_pair_given_p_one_j) + (p_two_j * b_pair_given_p_two_j)
    b_pair_odds = round(b_pair_prob_calc * 100, 2)

    # Chuẩn hóa đầu ra phần trăm tuyệt đối
    total_normalized = p_win_prob + b_win_prob + tie_prob
    if total_normalized == 0: total_normalized = 1.0

    return {
        "Player": round((p_win_prob / total_normalized) * 100, 2),
        "Banker": round((b_win_prob / total_normalized) * 100, 2),
        "Tie": round((tie_prob / total_normalized) * 100, 2)
    }, p_pair_odds, b_pair_odds, round((p_dragon_prob / total_normalized) * 100, 2), round((b_dragon_prob / total_normalized) * 100, 2), total_cards_left, True

# =========================================================================
# GIAO DIỆN PHÂN TÍCH MATRIX HUD v12.8
# =========================================================================
st.set_page_config(page_title="Oracle Ultimate v12.8", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stColumn"] { width: 50% !important; min-width: 50% !important; flex: 1 1 50% !important; padding: 5px !important; }
    .hud-box { padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; border: 1px solid #4f4f4f; background-color: #111; }
    .hud-title { font-size: 11px; font-weight: 600; color: #b0b0b0; }
    .hud-value { font-size: 30px; font-weight: 800; font-family: monospace; }
    .neon-p { background-color: #00bcd4 !important; border: 2px solid #00e5ff !important; color: #fff !important; box-shadow: 0 0 15px rgba(0,229,255,0.4); }
    .neon-b { background-color: #ff5252 !important; border: 2px solid #ff1744 !important; color: #fff !important; box-shadow: 0 0 15px rgba(255,23,68,0.4); }
    .badge-normal { background-color: #1e1e1e; padding: 8px; border-radius: 6px; text-align: center; border: 1px solid #333; }
    .badge-alert { background-color: #ff9100; padding: 8px; border-radius: 6px; text-align: center; border: 2px solid #ff6d00; box-shadow: 0 0 10px rgba(255,109,0,0.5); }
    .badge-dragon { background-color: #aa00ff; padding: 8px; border-radius: 6px; text-align: center; border: 2px solid #d500f9; box-shadow: 0 0 12px rgba(213,0,249,0.5); }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None

if st.session_state.last_results is None:
    st.session_state.last_results = calculate_baccarat_v12_8(st.session_state.shoe_history)

st.sidebar.header("⚙️ ORACLE ADVANCED")
decks = st.sidebar.selectbox("Số bộ bài:", [8, 6], index=0)
if st.sidebar.button("🔄 RESTART NEW SHOE", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.last_results = calculate_baccarat_v12_8([])
    st.rerun()

if isinstance(st.session_state.last_results, tuple):
    res, p_pair, b_pair, p_dragon, b_dragon, cards_left, is_ok = st.session_state.last_results
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📊 Lõi Tổ Hợp Phi Lặp Cửa Chính")
        st.markdown(f'<div class="hud-box {"neon-p" if res["Player"]>res["Banker"] else ""}"><div class="hud-title">🔵 PLAYER PROBABILITY</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box {"neon-b" if res["Banker"]>res["Player"] else ""}"><div class="hud-title">🔴 BANKER PROBABILITY</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box"><div class="hud-title">🟢 TIE PROBABILITY</div><div class="hud-value" style="color:#00e676;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
        st.caption(f"Trạng thái khay: {cards_left} lá còn lại")
        
    with col2:
        st.markdown("#### 🎯 Radar Cược Phụ Đọc Chuỗi")
        p_p_style = "badge-alert" if p_pair > 8.33 else "badge-normal"
        b_p_style = "badge-alert" if b_pair > 8.33 else "badge-normal"
        st.markdown(f'<div class="{p_p_style}"><span style="font-size:11px;color:#aaa;">🔵 CON ĐÔI</span><br><b style="font-size:18px;">{p_pair}%</b></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="{b_p_style}"><span style="font-size:11px;color:#aaa;">🔴 CÁI ĐÔI</span><br><b style="font-size:18px;">{b_pair}%</b></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
        
        p_d_style = "badge-dragon" if p_dragon > 16.5 else "badge-normal"
        b_d_style = "badge-dragon" if b_dragon > 10.8 else "badge-normal"
        st.markdown(f'<div class="{p_d_style}"><span style="font-size:11px;color:#aaa;">🐉 PLAYER LONG BẢO</span><br><b style="font-size:18px;color:#f50057;">{p_dragon}%</b></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="{b_d_style}"><span style="font-size:11px;color:#aaa;">🐉 BANKER LONG BẢO</span><br><b style="font-size:18px;color:#f50057;">{b_dragon}%</b></div>', unsafe_allow_html=True)

st.markdown("---")
st.subheader("🃏 Nạp Dữ Liệu Bài")
c_p, c_b = st.columns(2)
with c_p: p_in = st.text_input("PLAYER CARD:", key="p_input", placeholder="V dụ: A,10,6")
with c_b: b_in = st.text_input("BANKER CARD:", key="b_input", placeholder="Ví dụ: K,7")

def parse_input(raw_str):
    if not raw_str: return []
    tokens = raw_str.upper().replace(" ", "").split(",")
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    res = []
    for t in tokens:
        if t in mapping: res.append(mapping[t])
        elif t.isdigit() and 2 <= int(t) <= 10: res.append(int(t))
    return res

if st.button("🚀 EXECUTE ULTIMATE ANALYSIS", use_container_width=True, type="primary"):
    p_list = parse_input(p_in)
    b_list = parse_input(b_in)
    if p_list or b_list:
        st.session_state.shoe_history.extend(p_list + b_list)
        st.session_state.last_results = calculate_baccarat_v12_8(st.session_state.shoe_history, shoe_decks=decks)
        st.rerun()
