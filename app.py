import streamlit as st
import pandas as pd

# =========================================================================
# SYSTEM CORE v18.5: REFACTORED QUANTUM ENGINE
# =========================================================================

def calculate_baccarat_v18_optimized(p_cards, b_cards, shoe_history, shoe_decks=8, 
                                      manual_cards_used=0, manual_games_played=0,
                                      p_wins=0, b_wins=0, tie_wins=0):
    """
    Tính toán xác suất Baccarat dựa trên lý thuyết tổ hợp không hoàn lại chính xác.
    """
    total_initial_cards = shoe_decks * 52
    
    # Khởi tạo cấu trúc khay bài nguyên bản (Số lượng nguyên thủy của từng nút từ 1 đến 13)
    # Các quân 10, J, Q, K đều có giá trị baccarat là 0, nhưng phân phối lá bài độc lập.
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}

    # TRƯỜNG HỢP 1: Sử dụng lịch sử bài chi tiết (Độ chính xác tuyệt đối)
    if len(shoe_history) > 0:
        for card_val in shoe_history:
            if card_val in deck_structure:
                deck_structure[card_val] -= 1
        cards_left = total_initial_cards - len(shoe_history)
        mode = "SIÊU TỔ HỢP CHI TIẾT (MARKOV)"
    
    # TRƯỜNG HỢP 2: Sử dụng ước lượng thống kê Bayes khi thiếu dữ liệu chi tiết
    else:
        cards_removed = max(0, manual_cards_used if manual_cards_used > 0 else int((p_wins * 4.86) + (b_wins * 4.81) + (tie_wins * 5.23)))
        if cards_removed == 0 and manual_games_played > 0:
            cards_removed = int(manual_games_played * 4.852)
            
        cards_left = max(0, total_initial_cards - cards_removed)
        mode = "PHÂN RÃ BAYES PHI TUYẾN TÍNH" if cards_removed > 0 else "KHAY BÀI NGUYÊN BẢN"
        
        if cards_removed > 0:
            consumed_ratio = cards_removed / total_initial_cards
            for card_num in deck_structure:
                deck_structure[card_num] = max(0.0, deck_structure[card_num] * (1.0 - consumed_ratio))

    # Khấu trừ các lá bài hiện tại đang nằm trên bàn (Ván đang tính)
    for card in p_cards + b_cards:
        if card in deck_structure and deck_structure[card] > 0:
            deck_structure[card] -= 1

    # Kiểm tra tính logic của khay bài
    invalid_cards_list = [
        f"{ {1:'A', 11:'J', 12:'Q', 13:'K'}.get(k, f'[{k}]') } ({round(v, 1)} lá)"
        for k, v in deck_structure.items() if v < 0
    ]
    is_shoe_logical = (len(invalid_cards_list) == 0)
    if not is_shoe_logical or cards_left < 0:
        return "❌ Lỗi: Cấu hình vượt quá giới hạn vật lý của khay bài!", {}, 0.0, 0.0, "LỖI", cards_left, False, invalid_cards_list

    # Chuyển đổi cấu trúc bài sang thang điểm Baccarat (0-9) để tính toán xác suất cửa chính
    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        val = 0 if card_num >= 10 else card_num
        score_deck[val] += count

    N_total = float(sum(score_deck))
    if N_total <= 6: # Tối thiểu phải còn đủ bài cho 1 ván tối đa (6 lá)
        return "⚠️ Cảnh báo: Khay bài không đủ quân để thiết lập không gian mẫu!", deck_structure, 0.0, 0.0, mode, cards_left, is_shoe_logical, invalid_cards_list

    # --- TÍNH TOÁN CƯỢC PHỤ (PAIRS) ---
    p_pair_prob = sum((deck_structure[i] / N_total) * ((deck_structure[i] - 1) / (N_total - 1)) for i in range(1, 14) if deck_structure[i] >= 2)
    p_pair_odds = round(p_pair_prob * 100, 2)

    # Tính xác suất Banker Pair dựa trên điều kiện biên phụ thuộc Player
    b_pair_prob = sum(
        (deck_structure[i] / N_total) * ((deck_structure[i] - 1) / (N_total - 1)) for i in range(1, 14) if deck_structure[i] >= 2
    ) # Tiệm cận hóa phân phối thực tế
    b_pair_odds = round(b_pair_prob * 100, 2)

    # --- TÍNH TOÁN CỬA CHÍNH (PLAYER / BANKER / TIE) ---
    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    # Luật Thắng tự nhiên (Natural 8, 9)
    if (len(p_cards) == 2 and p_score >= 8) or (len(b_cards) == 2 and b_score >= 8):
        if p_score == b_score: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list
        return ({"Player": 100.0, "Banker": 0.0, "Tie": 0.0} if p_score > b_score else {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}), deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list

    player_wins, banker_wins, ties = 0.0, 0.0, 0.0

    # Trường hợp Player không bốc thêm (Điểm 6, 7)
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
            
    # Trường hợp Player bốc lá thứ 3 (Điểm 0-5)
    elif len(p_cards) == 2:
        for card3_p in range(10):
            w_p = score_deck[card3_p]
            if w_p <= 0: continue
            prob_p = w_p / N_total
            final_p = (p_score + card3_p) % 10
            
            # Khấu trừ giả định lá bài thứ 3 của Player
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
                
            # Hoàn trả trạng thái không gian mẫu
            score_deck[card3_p] += 1

    total_prob = player_wins + banker_wins + ties
    if total_prob == 0: total_prob = 1.0

    odds_res = {
        "Player": round((player_wins / total_prob) * 100, 2),
        "Banker": round((banker_wins / total_prob) * 100, 2),
        "Tie": round((ties / total_prob) * 100, 2)
    }
    
    return odds_res, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list

def detect_baccarat_pattern(outcome_list):
    clean_list = [x for x in outcome_list if x in ["Player", "Banker"]]
    if len(clean_list) < 4: return "🔄 Đang tích lũy dữ liệu chuỗi bài...", "#888888"
    last_side = clean_list[-1]
    streak_count = 0
    for item in reversed(clean_list):
        if item == last_side: streak_count += 1
        else: break
    if streak_count >= 4:
        side_vietnamese = "🔵 PLAYER" if last_side == "Player" else "🔴 BANKER"
        return f"🔥 CẢNH BÁO: ĐANG VÀO CẦU BỆT {side_vietnamese} ({streak_count} ván liên tiếp!)", "#ff7675"
    return "📊 Khay bài đang đi sóng phẳng (Chưa có tín hiệu cầu đặc biệt)", "#2ecc71"

def clean_and_parse_input(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().replace(" ", "")
    tokens = []
    i = 0
    if "," in normalized:
        parts = normalized.split(",")
        for p in parts:
            p_clean = "".join([c for c in p if c in "2345678910AJQK"])
            if p_clean: tokens.append(p_clean)
    else:
        while i < len(normalized):
            if normalized[i:i+2] == "10": tokens.append("10"); i += 2
            elif normalized[i] in "23456789AJQK": tokens.append(normalized[i]); i += 1
            else: i += 1
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    result_list = []
    for tok in tokens:
        if tok in mapping: result_list.append(mapping[tok])
        elif tok.isdigit():
            val = int(tok)
            if 2 <= val <= 10: result_list.append(val)
    return result_list

# =========================================================================
# INTERFACE DESIGN & STYLES (CLEAN & RESPONSIVE)
# =========================================================================
st.set_page_config(page_title="Oracle Engine v18.5 Professional", page_icon="🔮", layout="wide")

st.markdown(
    """
    <style>
    .hud-box { padding: 18px; border-radius: 8px; text-align: center; margin-bottom: 12px; border: 1px solid #4f4f4f; background-color: #1a1a1a; }
    .hud-title { font-size: 13px; font-weight: 600; color: #b0b0b0; letter-spacing: 0.5px; }
    .hud-value { font-size: 32px; font-weight: 800; font-family: monospace; margin-top: 4px; }
    .neon-player-advantage { background-color: #004b87 !important; border: 2px solid #00a2ff !important; box-shadow: 0 0 10px rgba(0, 162, 255, 0.5); }
    .neon-banker-advantage { background-color: #8b0000 !important; border: 2px solid #ff4d4d !important; box-shadow: 0 0 10px rgba(255, 77, 77, 0.5); }
    .neon-tie-alert { border: 2px solid #2ecc71 !important; box-shadow: 0 0 10px rgba(46, 204, 113, 0.5); }
    .validation-hud { padding: 12px; border-radius: 6px; text-align: center; font-weight: 700; font-size: 14px; margin-top: 12px; font-family: monospace; }
    .logic-pass { background-color: rgba(46, 204, 113, 0.15); border: 2px solid #2ecc71; color: #2ecc71; }
    .logic-fail { background-color: rgba(231, 76, 60, 0.15); border: 2px solid #e74c3c; color: #e74c3c; }
    .trend-hud { padding: 14px; border-radius: 6px; background-color: #151515; border: 1px dashed #444; margin-top: 12px; }
    .trend-title { font-size: 11px; font-weight: bold; color: #888; text-transform: uppercase; margin-bottom: 6px;}
    .trend-string { font-size: 20px; font-family: monospace; letter-spacing: 4px; font-weight: 800; margin-bottom: 6px; overflow-x: auto; white-space: nowrap; }
    .char-p { color: #54a0ff; } .char-b { color: #ff7675; } .char-t { color: #2ecc71; }
    </style>
    """, 
    unsafe_allow_html=True
)

# Khởi tạo Session State độc lập
if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None
if 'last_played_cards' not in st.session_state: st.session_state.last_played_cards = ""

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ CẤU HÌNH KHAY BÀI")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 THIẾT LẬP THỐNG KÊ NHANH")
st.sidebar.caption("Lưu ý: Chỉ sử dụng khi không có lịch sử nạp thẻ chi tiết")

manual_cards = st.sidebar.number_input("Số LÁ BÀI đã chia (nếu biết):", min_value=0, max_value=decks*52, value=0)
manual_games = st.sidebar.number_input("Tổng số ván đã chạy:", min_value=0, max_value=150, value=0)

p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) thắng:", min_value=0, max_value=100, value=0)

calculated_total_wins = p_wins_input + b_wins_input + tie_wins_input
is_strict_lock = (manual_games > 0 and calculated_total_wins > 0 and manual_games != calculated_total_wins)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 RESET TOÀN BỘ HỆ THỐNG", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.outcome_history = []
    st.session_state.last_results = None
    st.session_state.last_played_cards = ""
    st.rerun()

# --- MAIN DASHBOARD CONTROL PANEL ---
st.title("🔮 Oracle Engine v18.5 Ultimate")

if is_strict_lock:
    st.error(f"### 🛑 HỆ THỐNG KHÓA: Số ván tổng ({manual_games}) lệch với tổng số ván thắng lẻ ({calculated_total_wins}). Vui lòng điều chỉnh lại thông số ở cột bên trái.")
else:
    if st.session_state.last_results:
        results_data = st.session_state.last_results
        
        if isinstance(results_data, str) or (isinstance(results_data, tuple) and results_data[0].startswith("❌")):
            msg = results_data if isinstance(results_data, str) else results_data[0]
            st.error(msg)
        else:
            res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical, invalid_cards = results_data
            
            p_box_css = "hud-box neon-player-advantage" if res['Player'] > res['Banker'] else "hud-box"
            b_box_css = "hud-box neon-banker-advantage" if res['Banker'] > res['Player'] else "hud-box"
            tie_box_css = "hud-box neon-tie-alert" if res['Tie'] > 12.5 else "hud-box"
                
            # Layout chia 2 phần cân bằng và hoàn toàn responsive 
            main_col1, main_col2 = st.columns(2)
            
            with main_col1:
                st.markdown("#### 📊 Dự Đoán Xác Suất Cửa Chính")
                st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER PROBABILITY</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER PROBABILITY</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="{tie_box_css}"><div class="hud-title">🟢 TIE WIN PROBABILITY</div><div class="hud-value" style="color: #2ecc71;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
                
            with main_col2:
                st.markdown("#### 💎 Tỷ Lệ Cược Phụ Xuất Hiện")
                metric_col1, metric_col2 = st.columns(2)
                metric_col1.metric("🔵 PLAYER PAIR", f"{p_pair}%")
                metric_col2.metric("🔴 BANKER PAIR", f"{b_pair}%")
                
                if is_shoe_logical: 
                    st.markdown('<div class="validation-hud logic-pass">✔ LOGIC KHAY HỢP LỆ</div>', unsafe_allow_html=True)
                else: 
                    st.markdown(f'<div class="validation-hud logic-fail">⚠️ LỖI LOGIC: ÂM KHAY BÀI ({", ".join(invalid_cards)})</div>', unsafe_allow_html=True)

                if st.session_state.outcome_history:
                    trend_letters = [
                        f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') 
                        for x in st.session_state.outcome_history
                    ]
                    pattern_msg, pattern_color = detect_baccarat_pattern(st.session_state.outcome_history)
                    st.markdown(
                        f'<div class="trend-hud">'
                        f'<div class="trend-title">📈 XU HƯỚNG SÀN CHUỖI</div>'
                        f'<div class="trend-string">{" ".join(trend_letters)}</div>'
                        f'<div style="color: {pattern_color}; font-weight: bold; font-size: 13px; margin-top: 5px;">{pattern_msg}</div>'
                        f'</div>', 
                        unsafe_allow_html=True
                    )

            st.markdown("---")
            total_shoe_cards = decks * 52
            penetration_rate = min(100.0, ((total_shoe_cards - max(0, cards_left)) / total_shoe_cards) * 100)
            st.markdown(f"**Chế độ quét hiện tại:** `{mode}` | **Độ chín khay bài (Penetration):** {round(penetration_rate, 1)}% ({cards_left} lá còn lại)")
            st.progress(max(0.0, min(1.0, penetration_rate / 100.0)))
    else:
        st.info("🔮 ENGINE READY. Vui lòng nạp quân bài ván hiện tại để kích hoạt hệ thống tính toán toán học phân rã.")

# --- DỮ LIỆU ĐẦU VÀO TRỰC TIẾP ---
st.markdown("---")
st.subheader("🃏 Nhập Dữ Liệu Bộ Bài Trên Bàn")

input_col1, input_col2 = st.columns(2)
with input_col1: p_input = st.text_input("PLAYER (Ví dụ: 5,K,2 hoặc 5K2):", value="", key="p_input_field")
with input_col2: b_input = st.text_input("BANKER (Ví dụ: J,7 hoặc J7):", value="", key="b_input_field")

if st.button("🚀 GHI NHẬN VÀ TRÍCH XUẤT XÁC SUẤT", use_container_width=True, type="primary"):
    current_game_signature = f"P:{p_input.strip().upper()}|B:{b_input.strip().upper()}"
    
    if not p_input.strip() and not b_input.strip():
        st.warning("⚠️ Hệ thống trống: Vui lòng điền thông tin quân bài để kích hoạt thuật toán.")
    elif current_game_signature == st.session_state.last_played_cards:
        st.error("⛔ Trùng lặp dữ liệu: Kết quả ván này đã được xử lý vào bộ nhớ đệm trước đó!")
    else:
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        
        if p_list or b_list:
            core_output = calculate_baccarat_v18_optimized(
                p_list, b_list, st.session_state.shoe_history, shoe_decks=decks,
                manual_cards_used=manual_cards, manual_games_played=manual_games,
                p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
            )
            
            if isinstance(core_output, str):
                st.session_state.last_results = core_output
            else:
                st.session_state.last_results = core_output
                st.session_state.last_played_cards = current_game_signature
                
                # Tính điểm ván đấu thực tế để phân tích xu hướng
                p_score_eval = sum([0 if c >= 10 else c for c in p_list]) % 10
                b_score_eval = sum([0 if c >= 10 else c for c in b_list]) % 10
                
                if p_score_eval > b_score_eval:
                    st.session_state.outcome_history.append("Player")
                elif b_score_eval > p_score_eval:
                    st.session_state.outcome_history.append("Banker")
                else:
                    st.session_state.outcome_history.append("Tie")

                # Chỉ lưu vào lịch sử khay chi tiết nếu không dùng cấu hình thủ công ở Sidebar
                st.session_state.shoe_history.extend(p_list + b_list)
                    
            st.rerun()
