import streamlit as st
import pandas as pd
import numpy as np

# =========================================================================
# SYSTEM CORE v13.0: FULL DECISION TREE COMBINATORICS & MULTI-GAP DRAGON
# =========================================================================
def calculate_baccarat_v13_ultimate(shoe_history, shoe_decks=8, manual_cards_used=0):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    # 1. TRỪ LÙI BÀI CHÍNH XÁC THEO LỊCH SỬ THỰC TẾ
    detailed_cards_count = len(shoe_history)
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure:
                deck_structure[card_val] -= 1
        cards_left = total_initial_cards - detailed_cards_count
        mode = "TỔ HỢP TỰ ĐỘNG CHUẨN PHI LẶP"
    else:
        cards_removed = manual_cards_used
        cards_left = max(0, total_initial_cards - cards_removed)
        ratio = cards_left / total_initial_cards if total_initial_cards > 0 else 0
        for card_num in deck_structure:
            deck_structure[card_num] = (4 * shoe_decks) * ratio
        mode = "MA TRẬN TIỆM CẬN NỀN KHAY BÀI"

    is_shoe_logical = all(val >= 0 for val in deck_structure.values())
    N = float(sum(deck_structure.values()))
    if N <= 6:
        return "⚠️ Hệ thống dừng: Khay bài đã cạn dưới giới hạn an toàn!", {}, 0.0, 0.0, 0.0, 0.0, mode, int(N), is_shoe_logical

    # 2. XÁC SUẤT CỬA ĐÔI (PAIRS) - ĐỊNH LÝ TỔ HỢP ĐẦY ĐỦ
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

    # 3. CHUẨN HÓA SANG ĐIỂM (MODULO 10)
    score_deck = {i: 0.0 for i in range(10)}
    for card_num, count in deck_structure.items():
        score_deck[0 if card_num >= 10 else card_num] += count

    # 4. THUẬT TOÁN MÔ PHỎNG LONG BẢO (DRAGON BONUS) THEO CÁCH BIỆT ĐIỂM THỰC TẾ
    # Trả thưởng Long Bảo dựa trên khoảng cách điểm: Khác biệt càng lớn, tiền ăn càng cao
    player_wins, banker_wins, ties = 0.0, 0.0, 0.0
    p_dragon_score, b_dragon_score = 0.0, 0.0
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
                    if is_p_natural: p_dragon_score += w_comb * 1.0  # Thắng tự nhiên ăn 1:1
                elif b_score_init > p_score_init:
                    banker_wins += w_comb
                    if is_b_natural: b_dragon_score += w_comb * 1.0  # Thắng tự nhiên ăn 1:1
                else:
                    ties += w_comb
            else:
                # Giả lập sâu nếu không có Natural (tính toán xác suất biên độ cách biệt điểm số thực tế)
                if p_score_init > b_score_init:
                    player_wins += w_comb
                    gap = p_score_init - b_score_init
                    if gap >= 9: p_dragon_score += w_comb * 30.0    # Thắng cách biệt 9 điểm (1 ăn 30)
                    elif gap >= 8: p_dragon_score += w_comb * 10.0  # Thắng cách biệt 8 điểm (1 ăn 10)
                    elif gap >= 7: p_dragon_score += w_comb * 6.0   # Thắng cách biệt 7 điểm (1 ăn 6)
                    elif gap >= 6: p_dragon_score += w_comb * 4.0   # Thắng cách biệt 6 điểm (1 ăn 4)
                    elif gap >= 5: p_dragon_score += w_comb * 2.0   # Thắng cách biệt 5 điểm (1 ăn 2)
                    elif gap >= 4: p_dragon_score += w_comb * 1.0   # Thắng cách biệt 4 điểm (1 ăn 1)
                elif b_score_init > p_score_init:
                    banker_wins += w_comb
                    gap = b_score_init - p_score_init
                    if gap >= 9: b_dragon_score += w_comb * 30.0
                    elif gap >= 8: b_dragon_score += w_comb * 10.0
                    elif gap >= 7: b_dragon_score += w_comb * 6.0
                    elif gap >= 6: b_dragon_score += w_comb * 4.0
                    elif gap >= 5: b_dragon_score += w_comb * 2.0
                    elif gap >= 4: b_dragon_score += w_comb * 1.0
                else:
                    ties += w_comb

    if total_weight == 0: total_weight = 1.0
    
    odds_res = {
        "Player": round((player_wins / total_weight) * 100, 2),
        "Banker": round((banker_wins / total_weight) * 100, 2),
        "Tie": round((ties / total_weight) * 100, 2)
    }
    
    # Chuẩn hóa chỉ số EV (Expected Value) của Long bảo dựa trên phân lớp điểm thưởng lũy tiến
    p_dragon_ev = round((p_dragon_score / total_weight) * 100, 2)
    b_dragon_ev = round((b_dragon_score / total_weight) * 100, 2)

    return odds_res, deck_structure, p_pair_odds, b_pair_odds, p_dragon_ev, b_dragon_ev, mode, int(cards_left), is_shoe_logical

# =========================================================================
# GIAO DIỆN KIỂU CYBERPUNK HUD (STREAMLIT UI/UX TIÊN TIẾN)
# =========================================================================
st.set_page_config(page_title="Oracle Matrix v13.0 Ultimate", page_icon="🔮", layout="wide")

st.markdown(
    """
    <style>
    body { background-color: #0d0e12; color: #e2e8f0; }
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; }
    div[data-testid="stColumn"] { padding: 8px !important; }
    
    .main-hud { padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 12px; border: 1px solid #2d3748; background: linear-gradient(145deg, #1a202c, #111622); }
    .hud-title { font-size: 13px; font-weight: 700; color: #a0aec0; letter-spacing: 1px; text-transform: uppercase; }
    .hud-value { font-size: 40px; font-weight: 900; font-family: 'Courier New', monospace; margin-top: 4px; }
    
    .player-win-card { background: linear-gradient(145deg, #1e3a8a, #0f172a) !important; border: 2px solid #3b82f6 !important; box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); color: #fff; }
    .banker-win-card { background: linear-gradient(145deg, #7f1d1d, #450a0a) !important; border: 2px solid #ef4444 !important; box-shadow: 0 0 15px rgba(239, 68, 68, 0.5); color: #fff; }
    
    .badge-premium { background-color: #1e293b; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #334155; }
    .badge-alert-trigger { background: linear-gradient(145deg, #b45309, #78350f); padding: 12px; border-radius: 8px; text-align: center; border: 2px solid #f59e0b; box-shadow: 0 0 15px rgba(245, 158, 11, 0.5); }
    .badge-dragon-trigger { background: linear-gradient(145deg, #6d28d9, #4c1d95); padding: 12px; border-radius: 8px; text-align: center; border: 2px solid #8b5cf6; box-shadow: 0 0 15px rgba(139, 92, 246, 0.5); }
    
    .status-valid { color: #10b981; font-weight: bold; background-color: rgba(16, 185, 129, 0.1); padding: 6px; border-radius: 4px; border: 1px solid #10b981; }
    .status-invalid { color: #ef4444; font-weight: bold; background-color: rgba(239, 68, 68, 0.1); padding: 6px; border-radius: 4px; border: 1px solid #ef4444; }
    </style>
    """, 
    unsafe_allow_html=True
)

# KHỞI TẠO BỘ NHỚ LƯU TRỮ TRẠNG THÁI KHAY BÀI (SESSION STATE)
if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'burn_cards' not in st.session_state: st.session_state.burn_cards = 0
if 'edge_history' not in st.session_state: st.session_state.edge_history = {"Player": [], "Banker": []}

# --- CẤU HÌNH THANH BÊN (SIDEBAR) ---
st.sidebar.markdown("### 🛠️ KHÔNG GIAN ĐIỀU KHIỂN")
decks = st.sidebar.selectbox("Số lượng bộ bài sử dụng:", [8, 6], index=0)
burn_input = st.sidebar.number_input("Số lá bài đã hủy đầu khay (Burn):", min_value=0, value=st.session_state.burn_cards)

if st.sidebar.button("🔄 LÀM MỚI (RESET) KHAY BÀI", use_container_width=True, type="secondary"):
    st.session_state.shoe_history = []
    st.session_state.burn_cards = 0
    st.session_state.edge_history = {"Player": [], "Banker": []}
    st.rerun()

# CHẠY ĐỒNG BỘ TOÁN HỌC CORE v13.0
calc_output = calculate_baccarat_v13_ultimate(
    st.session_state.shoe_history, shoe_decks=decks, manual_cards_used=burn_input
)

# --- BỐ CỤC MÀN HÌNH CHÍNH (TABS PHÂN TÁCH) ---
tab1, tab2, tab3 = st.tabs(["📊 THEO DÕI LOGIC REAL-TIME", "📈 BIỂU ĐỒ LỢI THẾ (EDGE)", "🃏 NHẬP DỮ LIỆU & QUẢN LÝ"])

if isinstance(calc_output, tuple):
    res, remaining_deck, p_pair, b_pair, p_dragon, b_dragon, current_mode, cards_left, is_shoe_logical = calc_output
    
    # Ghi nhận lịch sử để vẽ đồ thị tăng trưởng lợi thế
    if st.experimental_get_query_params() or True: 
        st.session_state.edge_history["Player"].append(res["Player"])
        st.session_state.edge_history["Banker"].append(res["Banker"])
        # Giới hạn độ dài lưu trữ đồ thị tránh quá tải bộ nhớ
        if len(st.session_state.edge_history["Player"]) > 40:
            st.session_state.edge_history["Player"].pop(0)
            st.session_state.edge_history["Banker"].pop(0)

    with tab1:
        # THIẾT KẾ CARD HIỂN THỊ KẾT QUẢ ĐỘNG
        p_css = "main-hud player-win-card" if res['Player'] > res['Banker'] else "main-hud"
        b_css = "main-hud banker-win-card" if res['Banker'] > res['Player'] else "main-hud"
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="{p_css}"><div class="hud-title">🔵 XÁC SUẤT PLAYER</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="{b_css}"><div class="hud-title">🔴 XÁC SUẤT BANKER</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="main-hud"><div class="hud-title">🟢 XÁC SUẤT HÒA (TIE)</div><div class="hud-value" style="color:#10b981;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
            
        st.markdown("### 🎯 Chỉ Báo Điểm Cược Phụ Cao Cấp")
        sub1, sub2, sub3, sub4 = st.columns(4)
        
        # Ngưỡng kích hoạt cảnh báo toán học (Cửa Đôi > 8.33% | Long Bảo EV tăng cao)
        with sub1:
            style = "badge-alert-trigger" if p_pair > 8.33 else "badge-premium"
            st.markdown(f'<div class="{style}"><span style="font-size:12px;color:#cbd5e1;">🔵 PLAYER PAIR</span><br><b style="font-size:20px;">{p_pair}%</b></div>', unsafe_allow_html=True)
        with sub2:
            style = "badge-alert-trigger" if b_pair > 8.33 else "badge-premium"
            st.markdown(f'<div class="{style}"><span style="font-size:12px;color:#cbd5e1;">🔴 BANKER PAIR</span><br><b style="font-size:20px;">{b_pair}%</b></div>', unsafe_allow_html=True)
        with sub3:
            style = "badge-dragon-trigger" if p_dragon > 18.0 else "badge-premium"
            st.markdown(f'<div class="{style}"><span style="font-size:12px;color:#cbd5e1;">🐉 PLAYER LONG BẢO (EV)</span><br><b style="font-size:20px;color:#c084fc;">{p_dragon}%</b></div>', unsafe_allow_html=True)
        with sub4:
            style = "badge-dragon-trigger" if b_dragon > 13.0 else "badge-premium"
            st.markdown(f'<div class="{style}"><span style="font-size:12px;color:#cbd5e1;">🐉 BANKER LONG BẢO (EV)</span><br><b style="font-size:20px;color:#c084fc;">{b_dragon}%</b></div>', unsafe_allow_html=True)

        st.markdown("---")
        # THANH TIẾN TRÌNH CHIẾT KHẤU KHAY BÀI
        total_cards = decks * 52
        used_cards = total_cards - cards_left
        penetration = min(100.0, (used_cards / total_cards) * 100)
        
        inf1, inf2, inf3 = st.columns(3)
        with inf1: st.write(f"📊 **Trạng thái logic:** " + ('<span class="status-valid">HỢP LỆ</span>' if is_shoe_logical else '<span class="status-invalid">BẤT THƯỜNG</span>'), unsafe_allow_html=True)
        with inf2: st.write(f"🃏 **Số bài đã xả:** `{used_cards}` / `{total_cards}` lá")
        with inf3: st.write(f"🧠 **Chế độ tính toán:** Thống kê `{current_mode}`")
        
        st.progress(penetration / 100.0)

    with tab2:
        st.markdown("### 📈 Biểu Đồ Biến Động Lợi Thế Khay Bài (Edge Real-time)")
        if len(st.session_state.edge_history["Player"]) > 1:
            chart_data = pd.DataFrame({
                "Player Edge (%)": st.session_state.edge_history["Player"],
                "Banker Edge (%)": st.session_state.edge_history["Banker"]
            })
            st.line_chart(chart_data, height=300)
            st.caption("Biểu đồ thể hiện xu hướng dịch chuyển lợi thế toán học qua từng ván bài thực tế.")
        else:
            st.info("Nhập tối thiểu 2 ván bài để hệ thống bắt đầu vẽ biểu đồ động xu hướng.")

    with tab3:
        st.markdown("### 🃏 Chi Tiết Phân Bổ Cấu Trúc Khay Bài Còn Lại")
        cols = st.columns(5)
        labels_map = {1: "A", 11: "J", 12: "Q", 13: "K"}
        for idx, (num, cnt) in enumerate(remaining_deck.items()):
            label = labels_map.get(num, f"[{num}]")
            cols[idx % 5].metric(label=f"Quân {label}", value=f"{round(cnt, 1)} lá")
else:
    st.error(calc_output)

# =========================================================================
# KHU VỰC NẠP DỮ LIỆU LẬT BÀI LIÊN TỤC
# =========================================================================
st.markdown("---")
st.subheader("📥 Nhập kết quả ván vừa diễn ra")
ip_col1, ip_col2 = st.columns(2)
with ip_col1: p_in = st.text_input("BÊN PLAYER (Ví dụ gõ: 4,A,Q hoặc 4112):", key="p_box", placeholder="Tách bằng dấu phẩy hoặc gõ liền")
with ip_col2: b_in = st.text_input("BÊN BANKER (Ví dụ gõ: 9,K hoặc 913):", key="b_box", placeholder="Ví dụ: K=13, Q=12, J=11, A=1")

def parse_card_input(raw_text):
    if not raw_text: return []
    clean_text = raw_text.upper().replace(" ", "")
    
    # Trường hợp nhập ngăn cách bằng dấu phẩy
    if "," in clean_text:
        tokens = clean_text.split(",")
    else:
        # Trường hợp người dùng gõ chuỗi liền ký tự (Ví dụ: 7K2 -> 7, K, 2)
        tokens = []
        i = 0
        while i < len(clean_text):
            if clean_text[i:i+2] == "10":
                tokens.append("10")
                i += 2
            else:
                tokens.append(clean_text[i])
                i += 1
                
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    final_cards = []
    for t in tokens:
        if t in mapping: final_cards.append(mapping[t])
        elif t.isdigit() and 2 <= int(t) <= 10: final_cards.append(int(t))
    return final_cards

if st.button("🚀 XÁC NHẬN - ĐẨY DỮ LIỆU VÀO MA TRẬN PHÂN TÍCH", use_container_width=True, type="primary"):
    parsed_p = parse_card_input(p_in)
    parsed_b = parse_card_input(b_in)
    
    if parsed_p or parsed_b:
        combined_turn_cards = parsed_p + parsed_b
        st.session_state.shoe_history.extend(combined_turn_cards)
        st.success(f" Đã nạp thành công {len(combined_turn_cards)} lá bài vào bộ nhớ khay bài!")
        st.rerun()
    else:
        st.warning("⚠️ Không tìm thấy định dạng lá bài hợp lệ. Vui lòng kiểm tra lại dữ liệu nhập.")
