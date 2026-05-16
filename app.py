import streamlit as st
import pandas as pd

# =========================================================================
# SYSTEM CORE v13.0: EXACT BACCARAT RULE SIMULATION (FIXED ALL PROBABILITIES)
# =========================================================================
def calculate_baccarat_v13_core(shoe_history, shoe_decks=8, 
                                manual_cards_used=0, manual_games_played=0,
                                p_wins=0, b_wins=0, tie_wins=0):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    sum_wins_games = p_wins + b_wins + tie_wins

    if manual_cards_used > total_initial_cards or manual_games_played > int(total_initial_cards / 4):
        return "❌ Bất hợp lý: Dữ liệu cấu hình vượt quá giới hạn vật lý của khay bài!", {}, 0.0, 0.0, 0.0, 0.0, "LỖI", total_initial_cards, False

    detailed_cards_count = len(shoe_history)
    
    # 1. KHẤU TRỪ THEO LỊCH SỬ THỰC TẾ VÀ ƯỚC LƯỢNG
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure:
                deck_structure[card_val] -= 1
        cards_left = total_initial_cards - detailed_cards_count
        mode = "TỔ HỢP PHI LẶP TUYỆT ĐỐI (CORE V13.0)"
    else:
        cards_removed = max(0, manual_cards_used if manual_cards_used > 0 else int((p_wins * 4.86) + (b_wins * 4.81) + (tie_wins * 5.23)))
        cards_left = max(0, total_initial_cards - cards_removed)
        mode = "MA TRẬN PHÂN RÃ ƯỚC LƯỢNG" if cards_removed > 0 else "KHAY BÀI NGUYÊN BẢN"
        if cards_removed > 0:
            ratio = cards_left / total_initial_cards
            for card_num in deck_structure:
                deck_structure[card_num] = (4 * shoe_decks) * ratio

    is_shoe_logical = all(val >= 0 for val in deck_structure.values())
    N = float(sum(deck_structure.values()))
    if N <= 10:
        return "⚠️ Cảnh báo: Khay bài không đủ quân để giả lập ván mới!", {}, 0.0, 0.0, 0.0, 0.0, mode, cards_left, is_shoe_logical

    # 2. TOÁN HỌC ĐIỀU KIỆN CHO CỬA ĐÔI (PAIRS) - CHUẨN XÁC N-1 VÀ N-3
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

    # CHUẨN HÓA SANG MẢNG ĐIỂM (0-9) ĐỂ TỐI ƯU TỐC ĐỘ GIẢ LẬP KHÔNG GIAN MẪU
    score_cards = [0]*10
    for card_num, count in deck_structure.items():
        score_cards[0 if card_num >= 10 else card_num] += count

    # 3. GIẢ LẬP TOÀN BỘ QUY TRÌNH RÚT BÀI BACCARAT CHUẨN QUỐC TẾ
    p_win_w, b_win_w, tie_w = 0.0, 0.0, 0.0
    p_dragon_w, b_dragon_w = 0.0, 0.0
    total_w = 0.0

    # Lặp qua tất cả các điểm số có thể của 4 lá bài đầu tiên (P1, P2, B1, B2)
    for p1 in range(10):
        if score_cards[p1] <= 0: continue
        w1 = score_cards[p1]; score_cards[p1] -= 1
        for p2 in range(10):
            if score_cards[p2] <= 0: continue
            w2 = w1 * score_cards[p2]; score_cards[p2] -= 1
            for b1 in range(10):
                if score_cards[b1] <= 0: continue
                w3 = w2 * score_cards[b1]; score_cards[b1] -= 1
                for b2 in range(10):
                    if score_cards[b2] <= 0: continue
                    w4 = w3 * score_cards[b2]; score_cards[b2] -= 1

                    # Điểm số 2 lá đầu tiên
                    p_score = (p1 + p2) % 10
                    b_score = (b1 + b2) % 10

                    is_p_natural = p_score in [8, 9]
                    is_b_natural = b_score in [8, 9]

                    # Trường hợp Thắng Tự Nhiên (Natural) -> Không rút thêm
                    if is_p_natural or is_b_natural:
                        total_w += w4
                        if p_score > b_score:
                            p_win_w += w4
                            if is_p_natural: p_dragon_w += w4 # Thắng tự nhiên tính Long Bảo 1:1
                        elif b_score > p_score:
                            b_win_w += w4
                            if is_b_natural: b_dragon_w += w4
                        else:
                            tie_w += w4
                    else:
                        # Xét quy tắc rút lá thứ 3
                        # Thỏa mãn luật Player rút trước
                        p3_required = (p_score <= 5)
                        p3_val = -1

                        if p3_required:
                            # Giả lập rút lá thứ 3 cho Player
                            for p3 in range(10):
                                if score_cards[p3] <= 0: continue
                                w5 = w4 * score_cards[p3]; score_cards[p3] -= 1
                                p_final_score = (p_score + p3) % 10
                                
                                # Xác định Banker có được rút lá thứ 3 không dựa trên lá p3 của Player
                                b3_required = False
                                if b_score <= 2: b3_required = True
                                elif b_score == 3: b3_required = (p3 != 8)
                                elif b_score == 4: b3_required = (p3 in [2, 3, 4, 5, 6, 7])
                                elif b_score == 5: b3_required = (p3 in [4, 5, 6, 7])
                                elif b_score == 6: b3_required = (p3 in [6, 7])
                                
                                if b3_required:
                                    for b3 in range(10):
                                        if score_cards[b3] <= 0: continue
                                        w6 = w5 * score_cards[b3]
                                        b_final_score = (b_score + b3) % 10
                                        
                                        total_w += w6
                                        if p_final_score > b_final_score:
                                            p_win_w += w6
                                            gap = p_final_score - b_final_score
                                            if gap >= 4: p_dragon_w += w6
                                        elif b_final_score > p_final_score:
                                            b_win_w += w6
                                            gap = b_final_score - p_final_score
                                            if gap >= 4: b_dragon_w += w6
                                        else:
                                            tie_w += w6
                                else:
                                    total_w += w5
                                    if p_final_score > b_score:
                                        p_win_w += w5
                                        gap = p_final_score - b_score
                                        if gap >= 4: p_dragon_w += w5
                                    elif b_score > p_final_score:
                                        b_win_w += w5
                                        gap = b_score - p_final_score
                                        if gap >= 4: b_dragon_w += w5
                                    else:
                                        tie_w += w5
                                score_cards[p3] += 1
                        else:
                            # Player không rút (Đứng ở 6 hoặc 7), Banker rút nếu điểm <= 5
                            b3_required = (b_score <= 5)
                            if b3_required:
                                for b3 in range(10):
                                    if score_cards[b3] <= 0: continue
                                    w5 = w4 * score_cards[b3]
                                    b_final_score = (b_score + b3) % 10
                                    
                                    total_w += w5
                                    if p_score > b_final_score:
                                        p_win_w += w5
                                        gap = p_score - b_final_score
                                        if gap >= 4: p_dragon_w += w5
                                    elif b_final_score > p_score:
                                        b_win_w += w5
                                        gap = b_final_score - p_score
                                        if gap >= 4: b_dragon_w += w5
                                    else:
                                        tie_w += w5
                            else:
                                total_w += w4
                                if p_score > b_score:
                                    p_win_w += w4
                                    gap = p_score - b_score
                                    if gap >= 4: p_dragon_w += w4
                                civ_b_win = False
                                if b_score > p_score:
                                    b_win_w += w4
                                    gap = b_score - p_score
                                    if gap >= 4: b_dragon_w += w4
                                elif b_score == p_score:
                                    tie_w += w4

                    score_cards[b2] += 1
                score_cards[b1] += 1
            score_cards[p2] += 1
        score_cards[p1] += 1

    if total_w == 0: total_w = 1.0
    
    odds_res = {
        "Player": round((p_win_w / total_w) * 100, 2),
        "Banker": round((b_win_w / total_w) * 100, 2),
        "Tie": round((tie_w / total_w) * 100, 2)
    }
    
    p_dragon_odds = round((p_dragon_w / total_w) * 100, 2)
    b_dragon_odds = round((b_dragon_w / total_w) * 100, 2)

    return odds_res, deck_structure, p_pair_odds, b_pair_odds, p_dragon_odds, b_dragon_odds, mode, cards_left, is_shoe_logical

# =========================================================================
# INTERFACE DESIGN & STYLES
# =========================================================================
st.set_page_config(page_title="Oracle Ultimate v13.0 Pro", page_icon="🔮", layout="centered")

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
    
    .pair-badge-normal { background-color: #1e1e1e; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #444; }
    .pair-badge-alert { background-color: #d35400; padding: 10px; border-radius: 6px; text-align: center; border: 2px solid #e67e22; box-shadow: 0 0 15px rgba(230, 126, 34, 0.6); }
    
    .dragon-p-alert { background: linear-gradient(145deg, #0097a7, #006064) !important; border: 2px solid #00cec9 !important; box-shadow: 0 0 15px rgba(0, 206, 201, 0.8); color: #fff; }
    .dragon-b-alert { background: linear-gradient(145deg, #d35400, #962d00) !important; border: 2px solid #f1c40f !important; box-shadow: 0 0 15px rgba(241, 196, 15, 0.8); color: #fff; }
    
    .validation-hud { padding: 12px; border-radius: 6px; text-align: center; font-weight: 700; font-size: 14px; margin-top: 12px; font-family: monospace; }
    .logic-pass { background-color: rgba(46, 204, 113, 0.15); border: 2px solid #2ecc71; color: #2ecc71; box-shadow: 0 0 10px rgba(46, 204, 113, 0.3); }
    .logic-fail { background-color: rgba(231, 76, 60, 0.15); border: 2px solid #e74c3c; color: #e74c3c; box-shadow: 0 0 10px rgba(231, 76, 60, 0.3); animation: blinker 1.5s linear infinite; }
    
    .game-counter-hud { padding: 10px; border-radius: 6px; text-align: center; font-weight: 800; font-size: 15px; border: 1px dashed #f1c40f; color: #f1c40f; background-color: rgba(241, 196, 15, 0.05); margin-bottom: 15px; font-family: monospace; }
    .waiting-hud { padding: 25px; text-align: center; font-weight: bold; border: 1px dashed #555; background-color: #111; color: #888; border-radius: 8px; margin-bottom: 20px; }
    
    @keyframes blinker { 50% { opacity: 0.6; } }
    </style>
    """, 
    unsafe_allow_html=True
)

# KHỞI TẠO STATE AN TOÀN
if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None
if 'manual_games_counter' not in st.session_state: st.session_state.manual_games_counter = 0
if 'last_entered_round' not in st.session_state: st.session_state.last_entered_round = {"p": [], "b": []}

# --- SIDEBAR CẤU HÌNH ---
st.sidebar.header("⚙️ CẤU HÌNH KHAY BÀI")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Thiết lập nhanh khay bài")
manual_cards = st.sidebar.number_input("Số LÁ BÀI đã chia (nếu biết):", min_value=0, max_value=decks*52, value=0)
manual_games = st.sidebar.number_input("Tổng số ván nền đã chạy:", min_value=0, max_value=150, value=0)

p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0)

is_data_discrepancy = (manual_games != (p_wins_input + b_wins_input + tie_wins_input))

if st.sidebar.button("🔄 RESET TOÀN BỘ KHAY BÀI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.last_results = None
    st.session_state.manual_games_counter = 0
    st.session_state.last_entered_round = {"p": [], "b": []}
    st.rerun()

current_total_games = manual_games + st.session_state.manual_games_counter

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
            p_style = "pair-badge-alert" if p_pair > 11.5 else "pair-badge-normal"
            b_style = "pair-badge-alert" if b_pair > 11.5 else "pair-badge-normal"
            
            st.markdown(f'<div class="{p_style}"><span style="font-size:11px;color:#aaa;">🔵 CON ĐÔI (P-PAIR)</span><br><b style="font-size:18px;">{p_pair}%</b></div>', unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
            st.markdown(f'<div class="{b_style}"><span style="font-size:11px;color:#aaa;">🔴 CÁI ĐÔI (B-PAIR)</span><br><b style="font-size:18px;">{b_pair}%</b></div>', unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
            
            p_drag_style = "dragon-p-alert" if p_dragon > 4.5 else "pair-badge-normal"
            b_drag_style = "dragon-b-alert" if b_dragon > 5.5 else "pair-badge-normal"
            
            st.markdown(f'<div class="{p_drag_style}"><span style="font-size:11px;color:#e0ffff;font-weight:bold;">🐉 PLAYER LONG BẢO</span><br><b style="font-size:20px;color:#00ffff;">{p_dragon}%</b></div>', unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
            st.markdown(f'<div class="{b_drag_style}"><span style="font-size:11px;color:#fff9db;font-weight:bold;">🐉 BANKER LONG BẢO</span><br><b style="font-size:20px;color:#f1c40f;">{b_dragon}%</b></div>', unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
            if is_shoe_logical:
                st.markdown('<div class="validation-hud logic-pass">✔ THẨM ĐỊNH LOGIC: KHAY BÀI HỢP LỆ</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="validation-hud logic-fail">⚠️ CẢNH BÁO: PHÁT HIỆN SỐ LÁ LỖI LOGIC KHAY VƯỢT GIỚI HẠN BÀI</div>', unsafe_allow_html=True)

        st.markdown("---")
        total_shoe_cards = decks * 52
        cards_used_calc = total_shoe_cards - cards_left
        penetration_rate = min(100.0, (cards_used_calc / total_shoe_cards) * 100)
        st.markdown(f"**Chế độ chạy:** `{current_mode}` | **Độ chín khay bài:** {round(penetration_rate, 1)}% (Đã dùng {int(cards_used_calc)} / {total_shoe_cards} lá)")
        st.progress(penetration_rate / 100.0)
    else:
        st.markdown('<div class="waiting-hud">🔮 ORACLE ĐANG CHỜ DỮ LIỆU... VUI LÒNG NẠP KẾT QUẢ VÁN ĐẦU TIÊN PHÍA DƯỚI ĐỂ BẮT ĐẦU TÍNH TOÁN</div>', unsafe_allow_html=True)

# =========================================================================
# KHU VỰC NẠP KẾT QUẢ VÀ BỘ ĐẾM SỐ VÁN TỰ ĐỘNG TĂNG DẦN
# =========================================================================
st.markdown("---")
st.markdown(f'<div class="game-counter-hud">📈 ĐÃ CHẠY TỔNG CỘNG: {current_total_games} VÁN</div>', unsafe_allow_html=True)

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

p_parsed = clean_and_parse_input(p_input)
b_parsed = clean_and_parse_input(b_input)

# KIỂM TRA TRÙNG LẶP DỮ LIỆU
is_duplicate = False
if (p_parsed or b_parsed) and (st.session_state.last_entered_round["p"] == p_parsed and st.session_state.last_entered_round["b"] == b_parsed):
    is_duplicate = True

if is_duplicate:
    st.warning("⚠️ Cảnh báo: Dữ liệu bài vừa nhập trùng khớp hoàn toàn với ván trước đó! Vui lòng nhập ván mới để tiếp tục.")
    st.button("🚀 GHI NHẬN VÀ TÍNH TOÁN VÁN TIẾP THEO", use_container_width=True, type="primary", disabled=True)
else:
    if st.button("🚀 GHI NHẬN VÀ TÍNH TOÁN VÁN TIẾP THEO", use_container_width=True, type="primary"):
        if p_parsed or b_parsed:
            all_added = p_parsed + b_parsed
            st.session_state.shoe_history.extend(all_added)
            
            st.session_state.last_entered_round["p"] = p_parsed
            st.session_state.last_entered_round["b"] = b_parsed
            st.session_state.manual_games_counter += 1
            
            core_output = calculate_baccarat_v13_core(
                st.session_state.shoe_history, shoe_decks=decks,
                manual_cards_used=manual_cards, manual_games_played=manual_games,
                p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
            )
            
            if not isinstance(core_output, str):
                st.session_state.last_results = core_output
                st.rerun()
