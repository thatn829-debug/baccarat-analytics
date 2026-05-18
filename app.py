import streamlit as st
import numpy as np

# =========================================================================
# MODULE 1: BỘ TRỌNG TÀI LOGIC & PHÂN TÍCH CHUỖI MARKOV THỰC TẾ
# =========================================================================
def analyze_markov_momentum(outcome_history, total_p, total_b, total_t):
    """
    Thuật toán Ma trận chuyển trạng thái Markov thay thế hoàn toàn lõi cũ.
    Tự động bắt bài thuật toán của sảnh dựa trên dòng chảy thực tế.
    """
    global_games = total_p + total_b + total_t
    if global_games == 0:
        return 44.62, 45.86, 9.52

    # Tỷ lệ cơ sở mặc định của Baccarat
    base_p, base_b, base_t = 44.62, 45.86, 9.52
    
    # Nếu số lượng ván quá ít, sử dụng tỷ lệ phân phối thực tế đơn giản làm trọng số nền
    p_weight = (total_p / global_games) if global_games > 0 else 0.45
    b_weight = (total_b / global_games) if global_games > 0 else 0.45
    t_weight = (total_t / global_games) if global_games > 0 else 0.10

    # Phân tích sâu chuỗi chuyển dịch trạng thái (Markov Chain) khi có >= 3 ván
    if len(outcome_history) >= 3:
        transitions = {"Player": {"Player": 0, "Banker": 0, "Tie": 0},
                       "Banker": {"Player": 0, "Banker": 0, "Tie": 0},
                       "Tie":    {"Player": 0, "Banker": 0, "Tie": 0}}
        
        for i in range(len(outcome_history) - 1):
            current_state = outcome_history[i]
            next_state = outcome_history[i+1]
            if current_state in transitions and next_state in transitions:
                transitions[current_state][next_state] += 1
                
        last_state = outcome_history[-1]
        state_counts = transitions[last_state]
        total_trans = sum(state_counts.values())
        
        # Nếu trạng thái gần nhất có dữ liệu lặp lại, tính toán xác suất chuyển dịch cụ thể
        if total_trans > 0:
            markov_p = (state_counts["Player"] / total_trans) * 100
            markov_b = (state_counts["Banker"] / total_trans) * 100
            markov_t = (state_counts["Tie"] / total_trans) * 100
            
            # Tính toán Momentum (Đà bệt của bàn chơi)
            streak = 1
            for i in range(len(outcome_history)-2, -1, -1):
                if outcome_history[i] == last_state: streak += 1
                else: break
            
            # Nếu bàn đang bệt cực mạnh, tăng mạnh trọng số theo phe đang bệt để chống lỗi bẻ cầu mù quáng
            momentum_factor = min(0.4, streak * 0.08)
            
            if last_state == "Player":
                markov_p += (streak * 4.5)
                markov_b -= (streak * 3.0)
            elif last_state == "Banker":
                markov_b += (streak * 4.5)
                markov_p -= (streak * 3.0)

            # Dung hợp tỷ lệ giữa Ma trận trạng thái (70%) và Tổng phân phối bàn (30%)
            final_p = (markov_p * 0.7) + (p_weight * 100 * 0.3)
            final_b = (markov_b * 0.7) + (b_weight * 100 * 0.3)
            final_t = (markov_t * 0.7) + (t_weight * 100 * 0.3)
            
            return final_p, final_b, final_t

    # Trường hợp có dữ liệu sidebar nhưng chưa có chuỗi lịch sử chi tiết
    adaptive_p = (base_p * 0.4) + (p_weight * 100 * 0.6)
    adaptive_b = (base_b * 0.4) + (b_weight * 100 * 0.6)
    adaptive_t = (base_t * 0.4) + (t_weight * 100 * 0.6)
    
    return adaptive_p, adaptive_b, adaptive_t


# =========================================================================
# BỘ LỌC ĐƯỜNG MÁU & RA QUYẾT ĐỊNH LỆNH AI
# =========================================================================
def detect_baccarat_pattern(outcome_list):
    clean_list = [x for x in outcome_list if x in ["Player", "Banker"]]
    if len(clean_list) < 3: return "🔄 Đang phân tích sóng sảnh bài...", "#888888", None, 0
    last_side = clean_list[-1]
    streak_count = 0
    for item in reversed(clean_list):
        if item == last_side: streak_count += 1
        else: break
    if streak_count >= 3:
        side_vietnamese = "🔵 PLAYER" if last_side == "Player" else "🔴 BANKER"
        return f"🔥 THUẬT TOÁN BỆT {side_vietnamese} ({streak_count} ván)", "#00cec9", last_side, streak_count
    return "📊 BÀN ĐI SÓNG PHẲNG (NHẢY ĐƠN/ĐÔI)", "#2ed573", "Sóng phẳng", 0

def get_ai_recommendation_v4(p_val, b_val, t_val, outcome_history):
    if len(outcome_history) < 3:
        return "⚠️ QUAN SÁT THỰC TẾ: Đang nạp dữ liệu ma trận nền (Cần tối thiểu 3 ván để nhận diện đường bài).", "rgba(164, 176, 190, 0.1)", "#a4b0be"
        
    _, _, real_trend_side, streak_count = detect_baccarat_pattern(outcome_history)
    
    # Cảnh báo nổ Hòa dựa trên ma trận thực tế
    if t_val > 18.0:
        return f"🟢 ĐỘT BIẾN KHỚP LỆNH HÒA (TIE): Ma trận điểm rơi báo tỷ lệ Hòa chạm ngưỡng {t_val:.1f}%. Lót nhẹ cửa Hòa!", "rgba(46, 213, 115, 0.15)", "#2ed573"

    if real_trend_side == "Player" and p_val > b_val:
        return f"🔥 THUẬN QUY QUYẾT: ĐU THEO KHUÔN 🔵 PLAYER | Bàn đang bệt ăn khớp đà dịch chuyển ma trận.", "rgba(0, 175, 185, 0.2)", "#00afb9"
    elif real_trend_side == "Banker" and b_val > p_val:
        return f"🔥 THUẬN QUY QUYẾT: ĐU THEO KHUÔN 🔴 BANKER | Thuật toán bàn đang nghiêng mạnh về Cái. Không bẻ cầu!", "rgba(254, 217, 255, 0.2)", "#fed9ff"
        
    # Xử lý khi lệch pha giữa toán học nền và xu hướng bề nổi
    if p_val > b_val + 5.0:
        return f"🔵 VÀO LỆNH: PLAYER | Sóng ma trận đảo chiều ưu thế rõ rệt cho Người Chơi ({p_val:.1f}% vs {b_val:.1f}%).", "rgba(0, 175, 185, 0.15)", "#00afb9"
    elif b_val > p_val + 5.0:
        return f"🔴 VÀO LỆNH: BANKER | Sóng ma trận đảo chiều ưu thế rõ rệt cho Nhà Cái ({b_val:.1f}% vs {p_val:.1f}%).", "rgba(254, 217, 255, 0.15)", "#fed9ff"
        
    return "📊 ĐƯỜNG BÀI NHIỄU KHÔNG ĐỒNG BỘ: Thuật toán sòng đang quét tài khoản. Bỏ ván này!", "rgba(164, 176, 190, 0.1)", "#a4b0be"


# =========================================================================
# SYSTEM INTERFACE DISPLAY
# =========================================================================
st.set_page_config(page_title="Oracle Engine v43.0 Markov Adaptive", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(145deg, #0b132b, #1c2541, #3a506b) !important; color: #ecf0f1 !important; }
    
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
    }
    div[data-testid="stHorizontalBlock"] > div {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    .central-game-counter { text-align: center; background: rgba(0, 175, 185, 0.15); border: 1px solid #00afb9; border-radius: 8px; padding: 8px 12px; font-family: monospace; font-size: 15px; font-weight: 800; color: #00afb9; margin-bottom: 12px; }
    .ai-decision-box { text-align: center; border-radius: 10px; padding: 14px 10px; font-size: 15px; font-weight: 800; margin: 12px auto; box-shadow: 0px 4px 15px rgba(0,0,0,0.3); line-height: 1.4; }
    .hud-box { padding: 12px 4px; border-radius: 10px; text-align: center; margin-bottom: 8px; border: 1px solid #1c2541; background: rgba(11, 19, 43, 0.9); min-height: 85px; display: flex; flex-direction: column; justify-content: center; }
    .hud-title { font-size: 11px; font-weight: 700; color: #a4b0be; text-transform: uppercase; }
    .hud-value { font-size: 26px; font-weight: 800; font-family: monospace; margin-top: 1px; }
    .neon-player-advantage { background-color: #1a3a4b !important; border: 2px solid #00afb9 !important; }
    .neon-banker-advantage { background-color: #3a1c1c !important; border: 2px solid #e74c3c !important; }
    .logic-lock { background-color: rgba(28, 37, 65, 0.8); border: 2px dashed #64dfdf; color: #64dfdf; padding: 40px 20px; border-radius: 12px; font-size: 16px; text-align: center; box-shadow: 0px 0px 15px rgba(100, 223, 223, 0.2); }
    .trend-hud { padding: 10px; border-radius: 8px; background-color: rgba(5, 15, 20, 0.9); border: 1px dashed #00afb9; margin-top: 5px; }
    .trend-title { font-size: 10px; font-weight: bold; color: #00afb9; text-transform: uppercase; margin-bottom: 4px;}
    .trend-string { font-size: 15px; font-family: monospace; letter-spacing: 3px; font-weight: 800; }
    .char-p { color: #00afb9; font-weight: bold; } 
    .char-b { color: #e74c3c; font-weight: bold; } 
    .char-t { color: #2ed573; font-weight: bold; }
    
    div.stButton > button { background-color: #64dfdf !important; color: #0b132b !important; border-radius: 8px; font-weight: 900; padding: 10px 0px; font-size: 15px !important; border: none !important; }
    div.stButton > button:hover { background-color: #48cae4 !important; box-shadow: 0px 0px 10px #48cae4; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'form_counter' not in st.session_state: st.session_state.form_counter = 0

st.sidebar.header("📊 THIẾT LẬP DỮ LIỆU CƠ SỞ")
p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER đã thắng:", min_value=0, max_value=100, value=0)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER đã thắng:", min_value=0, max_value=100, value=0)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA (TIE) đã thắng:", min_value=0, max_value=100, value=0)

# Đồng bộ hóa tổng số ván
total_p_wins = p_wins_input + sum(1 for x in st.session_state.outcome_history if x == "Player")
total_b_wins = b_wins_input + sum(1 for x in st.session_state.outcome_history if x == "Banker")
total_t_wins = tie_wins_input + sum(1 for x in st.session_state.outcome_history if x == "Tie")
global_total_games = total_p_wins + total_b_wins + total_t_wins

st.markdown("### 🃏 ĐỒNG BỘ DỮ LIỆU BÀN CHƠI")
next_game_number = global_total_games + 1
st.markdown(f'<div class="central-game-counter">🔮 KẾT QUẢ KHOÁ LỆNH VÁN THỨ: {next_game_number}</div>', unsafe_allow_html=True)

# Giao diện nhập kết quả ván nhanh chóng, chính xác
st.write("**Bấm chọn kết quả thực tế vừa ra của bàn chơi:**")
col_btn_p, col_btn_b, col_btn_t = st.columns(3)

with col_btn_p:
    if st.button("🔵 PLAYER WIN", use_container_width=True):
        st.session_state.outcome_history.append("Player")
        st.session_state.form_counter += 1
        st.rerun()
with col_btn_b:
    if st.button("🔴 BANKER WIN", use_container_width=True):
        st.session_state.outcome_history.append("Banker")
        st.session_state.form_counter += 1
        st.rerun()
with col_btn_t:
    if st.button("🟢 TIE WIN", use_container_width=True):
        st.session_state.outcome_history.append("Tie")
        st.session_state.form_counter += 1
        st.rerun()

st.markdown("---")

# GUARDRAIL: KHÓA CHẶT TUYỆT ĐỐI HIỂN THỊ NẾU CHƯA NHẬP CƠ SỞ
if global_total_games == 0:
    st.markdown(
        '<div class="logic-lock">'
        '🔒 <b>HỆ THỐNG ĐANG KHÓA TỶ LỆ CHỐNG LỆCH ẢO</b><br>'
        '<span style="font-size:13.5px; font-weight:normal; opacity:0.85;">'
        'Thuật toán Markov v43.0 từ chối xuất kết quả lý thuyết suông. '
        'Vui lòng nhập kết quả ván vừa ra bằng các nút phía trên hoặc điền lịch sử bàn chơi vào Sidebar để mở khóa ma trận xác suất thực tế.</span>'
        '</div>', 
        unsafe_allow_html=True
    )
else:
    # Tính toán dựa trên mô hình Markov thế hệ mới
    raw_p, raw_b, raw_t = analyze_markov_momentum(
        st.session_state.outcome_history, total_p_wins, total_b_wins, total_t_wins
    )
    
    # Khớp tổng tỷ lệ về chuẩn 100%
    total_sum = raw_p + raw_b + raw_t
    final_p = round((raw_p / total_sum) * 100, 2)
    final_b = round((raw_b / total_sum) * 100, 2)
    final_t = round(100 - final_p - final_b, 2)

    st.markdown("### 🔮 PHÂN TÍCH MA TRẬN ADAPTIVE ENGINE")
    
    # Xuất khuyến nghị AI hành động nhanh
    rec_text, rec_bg, rec_border = get_ai_recommendation_v4(final_p, final_b, final_t, st.session_state.outcome_history)
    st.markdown(f'<div class="ai-decision-box" style="background-color: {rec_bg}; border: 2px solid {rec_border}; color: {rec_border};">{rec_text}</div>', unsafe_allow_html=True)
    
    # Định dạng neon hiển thị cửa lợi thế lớn
    p_box_css, b_box_css = "hud-box", "hud-box"
    if final_p > final_b + 2.0: p_box_css = "hud-box neon-player-advantage"
    elif final_b > final_p + 2.0: b_box_css = "hud-box neon-banker-advantage"
    
    col_p, col_b, col_t = st.columns(3, gap="small")
    with col_p:
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER</div><div class="hud-value" style="color:#00afb9;">{final_p}%</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER</div><div class="hud-value" style="color:#ff4757;">{final_b}%</div></div>', unsafe_allow_html=True)
    with col_t:
        st.markdown(f'<div class="hud-box"><div class="hud-title">🟢 TIE WIN</div><div class="hud-value" style="color: #2ed573;">{final_t}%</div></div>', unsafe_allow_html=True)
        
    st.write("")
    
    # Hiển thị đường xu hướng trực quan dạng chuỗi ký tự
    if st.session_state.outcome_history:
        trend_letters = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.outcome_history]
        pattern_msg, pattern_color, _, _ = detect_baccarat_pattern(st.session_state.outcome_history)
        st.markdown(f'<div class="trend-hud"><div class="trend-title">📈 DÒNG CHẢY ĐƯỜNG BÀI THỰC TẾ TRÊN SÀN</div><div class="trend-string">{" ".join(trend_letters)}</div><div style="color: {pattern_color}; font-weight: bold; font-size: 12px; margin-top:4px;">{pattern_msg}</div></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
util_col_1, util_col_2 = st.columns(2, gap="small")
with util_col_1:
    if st.button("⏪ HOÀN TÁC (UNDO)", use_container_width=True):
        if st.session_state.outcome_history:
            st.session_state.outcome_history.pop()
            st.rerun()
with util_col_2:
    if st.button("🔄 LÀM TRỐNG (ĐỔI BÀN)", use_container_width=True):
        st.session_state.outcome_history = []
        st.session_state.form_counter = 0
        st.rerun()
