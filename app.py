import streamlit as st
import pandas as pd
import time
import random

# =========================================================================
# KHỐI FAIL-SAFE: TỰ ĐỘNG KIỂM TRA VÀ CÔ LẬP LỖI THƯ VIỆN
# =========================================================================
AUTOREFRESH_AVAILABLE = True
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    AUTOREFRESH_AVAILABLE = False

SELENIUM_AVAILABLE = True
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        from selenium_stealth import stealth
        STEALTH_LIB_AVAILABLE = True
    except ImportError:
        STEALTH_LIB_AVAILABLE = False
except ImportError:
    SELENIUM_AVAILABLE = False

# =========================================================================
# SYSTEM CORE v20.1: REFACTORED BAYESIAN ENGINE
# =========================================================================
def calculate_baccarat_v20_ultimate(p_cards, b_cards, shoe_history, shoe_decks=8, 
                                    manual_cards_used=0, manual_games_played=0,
                                    p_wins=0, b_wins=0, tie_wins=0):
    """
    Tính toán xác suất dựa trên số lượng bài còn lại chính xác trong khay (Card Counting)
    """
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}

    # Cập nhật các lá bài đã biết từ lịch sử chi tiết
    detailed_cards_count = len(shoe_history)
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure:
                deck_structure[card_val] = max(0.0, deck_structure[card_val] - 1.0)
        cards_left = total_initial_cards - detailed_cards_count
        mode = "SIÊU TỔ HỢP MARKOV (LIVE-MATRIX v20.1)"
    else:
        # Ước tính nếu không có lịch sử chi tiết
        cards_removed = max(0, manual_cards_used if manual_cards_used > 0 else int((p_wins * 4.9) + (b_wins * 4.9) + (tie_wins * 5.2)))
        if cards_removed == 0 and manual_games_played > 0:
            cards_removed = int(manual_games_played * 4.89)
            
        cards_left = max(0, total_initial_cards - cards_removed)
        mode = "MA TRẬN QUANTUM-BAYES v20.1" if cards_removed > 0 else "KHAY BÀI NGUYÊN BẢN"
        
        if cards_removed > 0:
            consumed_ratio = cards_removed / total_initial_cards
            for card_num in deck_structure:
                deck_structure[card_num] = max(0.0, (4 * shoe_decks) * (1.0 - consumed_ratio))

    # Loại bỏ tiếp các lá bài đang hiển thị trên bàn ở ván hiện tại để tính toán xác suất cho các lá rút thêm
    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: score_deck[0] += count
        else: score_deck[card_num] += count

    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] -= 1

    N_total = float(sum(score_deck))
    if N_total <= 10:
        return "⚠️ Cảnh báo: Khay bài không đủ quân!", deck_structure, 0.0, 0.0, mode, cards_left, True, []

    # Tính toán tỷ lệ Pair (Đôi) cơ bản dựa trên tổ hợp bài còn lại
    p_pair_prob = sum((deck_structure[i]/N_total)*((deck_structure[i]-1)/(N_total-1)) for i in range(1, 14) if deck_structure[i] >= 2)
    p_pair_odds = round(p_pair_prob * 100, 2)
    b_pair_odds = round(p_pair_prob * 100, 2) # Xấp xỉ đồng đều trong không gian mẫu lớn

    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    # Luật Thắng Tự Nhiên (Natural Win)
    if (len(p_cards) == 2 and p_score >= 8) or (len(b_cards) == 2 and b_score >= 8):
        if p_score == b_score: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, True, []
        elif p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, True, []
        else: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, True, []

    # Giả lập luật rút lá bài thứ 3 chuẩn sòng bài quốc tế
    player_wins, banker_wins, ties = 0.0, 0.0, 0.0

    # Trường hợp Player không rút (6 hoặc 7 điểm)
    if p_score >= 6:
        if b_score <= 5: # Banker buộc phải rút
            for card3_b in range(10):
                w_b = score_deck[card3_b]
                if w_b > 0:
                    prob_b = w_b / N_total
                    final_b = (b_score + card3_b) % 10
                    if p_score > final_b: player_wins += prob_b
                    elif final_b > p_score: banker_wins += prob_b
                    else: ties += prob_b
        else: # Cả hai cùng đứng bài
            if p_score > b_score: player_wins += 1.0
            elif b_score > p_score: banker_wins += 1.0
            else: ties += 1.0
    else:
        # Player chắc chắn rút lá thứ 3
        for card3_p in range(10):
            w_p = score_deck[card3_p]
            if w_p <= 0: continue
            prob_p = w_p / N_total
            final_p = (p_score + card3_p) % 10
            
            # Cập nhật khay bài ảo sau khi Player lấy 1 lá
            score_deck[card3_p] -= 1
            N1 = N_total - 1.0
            
            # Kiểm tra luật rút bài của Banker dựa trên lá thứ 3 của Player
            b_draws = False
            if b_score <= 2: b_draws = True
            elif b_score == 3 and card3_p != 8: b_draws = True
            elif b_score == 4 and card3_p in [2, 3, 4, 5, 6, 7]: b_draws = True
            elif b_score == 5 and card3_p in [4, 5, 6, 7]: b_draws = True
            elif b_score == 6 and card3_p in [6, 7]: b_draws = True
            
            if b_draws:
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
                
            score_deck[card3_p] += 1 # Hoàn trả trạng thái mẫu

    total_prob = player_wins + banker_wins + ties
    if total_prob == 0: total_prob = 1.0

    odds_res = {
        "Player": round((player_wins / total_prob) * 100, 2),
        "Banker": round((banker_wins / total_prob) * 100, 2),
        "Tie": round((ties / total_prob) * 100, 2)
    }
    return odds_res, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, True, []

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
        return f"🔥 CẢNH BÁO: ĐANG VÀO CẦU BỆT {side_vietnamese} ({streak_count} ván!)", "#ff7675"
    return "📊 Khay bài đang đi sóng phẳng (Chưa có tín hiệu cầu đặc biệt)", "#2ecc71"

# =========================================================================
# WEB SCRAPER INTERFACE
# =========================================================================
def fetch_live_web_data_stealth(url, target_xpath):
    if not SELENIUM_AVAILABLE:
        return "ERROR_LIB", "Chưa cài đặt bộ thư viện Selenium lõi."
    
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")

    try:
        driver = webdriver.Chrome(options=options)
        if STEALTH_LIB_AVAILABLE:
            stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris", fix_hairline=True)
        
        driver.get(url)
        time.sleep(random.uniform(3.0, 5.0)) 
        
        wait = WebDriverWait(driver, 8)
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, target_xpath)))
        
        scraped_outcomes = []
        for elem in elements:
            text = elem.text.strip().upper()
            if any(p in text for p in ['PLAYER', 'CON', 'P', '🔵']): scraped_outcomes.append('Player')
            elif any(b in text for b in ['BANKER', 'CÁI', 'B', '🔴']): scraped_outcomes.append('Banker')
            elif any(t in text for t in ['TIE', 'HÒA', 'T', '🟢']): scraped_outcomes.append('Tie')
            
        driver.quit()
        return "SUCCESS", scraped_outcomes
    except Exception as e:
        try: driver.quit()
        except: pass
        return "ERROR_CONN", str(e)

# =========================================================================
# UI RENDER
# =========================================================================
st.set_page_config(page_title="Oracle Hybrid Matrix v20.1", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .hud-box { padding: 18px; border-radius: 8px; text-align: center; margin-bottom: 12px; border: 1px solid #4f4f4f; background-color: #1a1a1a; }
    .hud-title { font-size: 13px; font-weight: 600; color: #b0b0b0; letter-spacing: 0.5px; }
    .hud-value { font-size: 36px; font-weight: 800; font-family: monospace; margin-top: 4px; }
    .neon-player-advantage { background-color: #0984e3 !important; border: 2px solid #74b9ff !important; box-shadow: 0 0 15px rgba(9, 132, 227, 0.7); }
    .neon-banker-advantage { background-color: #d63031 !important; border: 2px solid #ff7675 !important; box-shadow: 0 0 15px rgba(214, 48, 49, 0.7); }
    .trend-hud { padding: 14px; border-radius: 6px; background-color: #151515; border: 1px dashed #444; margin-top: 12px; }
    .trend-string { font-size: 18px; font-family: monospace; letter-spacing: 6px; font-weight: 800; }
    .char-p { color: #54a0ff; } .char-b { color: #ff7675; } .char-t { color: #2ecc71; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None

st.sidebar.header("⚙️ CẤU HÌNH KHAY BÀI")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

if AUTOREFRESH_AVAILABLE and SELENIUM_AVAILABLE:
    auto_scrape_enabled = st.sidebar.checkbox("Kích hoạt Quét Tàng Hình Tự Động", value=False)
    if auto_scrape_enabled:
        target_url = st.sidebar.text_input("Nhập Link Web bàn bài:", value="https://example-baccarat-live.com")
        xpath_selector = st.sidebar.text_input("Xpath định vị chuỗi kết quả:", value="//div[contains(@class, 'road-item')]")
        refresh_rate = st.sidebar.slider("Tần suất quét lại (Giây):", 15, 120, 35)
        st_autorefresh(interval=refresh_rate * 1000, key="baccarat_refresh_core")
else:
    auto_scrape_enabled = False
    st.sidebar.warning("Chế độ quét tự động tắt do thiếu thư viện.")

st.sidebar.markdown("---")
manual_cards = st.sidebar.number_input("Số LÁ BÀI đã chia (nếu biết):", 0, decks*52, 0, disabled=auto_scrape_enabled)
p_wins_input = st.sidebar.number_input("🔵 Số ván PLAYER thắng:", 0, 100, 0, disabled=auto_scrape_enabled)
b_wins_input = st.sidebar.number_input("🔴 Số ván BANKER thắng:", 0, 100, 0, disabled=auto_scrape_enabled)
tie_wins_input = st.sidebar.number_input("🟢 Số ván HÒA thắng:", 0, 100, 0, disabled=auto_scrape_enabled)

if st.sidebar.button("🔄 RESET TOÀN BỘ KHAY BÀI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.outcome_history = []
    st.session_state.last_results = None
    st.toast("Đã đặt lại khay bài!")

# HIỂN THỊ KẾT QUẢ ĐÃ TÍNH TOÁN
if st.session_state.last_results:
    res, _, p_pair, b_pair, mode, cards_left, _, _ = st.session_state.last_results
    
    p_box_css = "hud-box neon-player-advantage" if res['Player'] > res['Banker'] else "hud-box"
    b_box_css = "hud-box neon-banker-advantage" if res['Banker'] > res['Player'] else "hud-box"
    
    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box"><div class="hud-title">🟢 TIE (HÒA)</div><div class="hud-value" style="color: #2ecc71;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
        
    with right_col:
        st.markdown("#### 💎 Tỷ Lệ Cược Phụ")
        st.metric("🔵 PLAYER PAIR", f"{p_pair}%")
        st.metric("🔴 BANKER PAIR", f"{b_pair}%")
        
        if st.session_state.outcome_history:
            trend_letters = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.outcome_history]
            pattern_msg, pattern_color = detect_baccarat_pattern(st.session_state.outcome_history)
            st.markdown(f'<div class="trend-hud"><div class="trend-string">{" ".join(trend_letters)}</div><div style="color: {pattern_color}; font-size:12px; font-weight:bold; margin-top:5px;">{pattern_msg}</div></div>', unsafe_allow_html=True)

# KHỐI NHẬP LIỆU VÀ GHI NHẬN QUÂN BÀI THỰC TẾ
st.markdown("---")
st.subheader("🃏 Nhập Dữ Liệu Ván Vừa Diễn Ra")
st.caption("Nhập toàn bộ từ 4 đến 6 lá bài đã lật của ván đó để hệ thống loại trừ bài chính xác (Ví dụ: 10,J,K,2 hoặc 7,A,9).")

col_p, col_b = st.columns(2)
with col_p: p_input = st.text_input("PLAYER (Các lá bài lật):", value="", key="p_input_field")
with col_b: b_input = st.text_input("BANKER (Các lá bài lật):", value="", key="b_input_field")

def clean_and_parse_input(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().replace(" ", "")
    tokens = normalized.split(",") if "," in normalized else list(normalized)
    
    mapping = {'A': 1, 'T': 10, 'J': 11, 'Q': 12, 'K': 13}
    result_list = []
    for tok in tokens:
        if tok in mapping: result_list.append(mapping[tok])
        elif tok.isdigit():
            val = int(tok)
            if 2 <= val <= 10: result_list.append(val)
    return result_list

if st.button("🚀 GHI NHẬN & DỰ ĐOÁN VÁN TIẾP THEO", use_container_width=True, type="primary"):
    if not p_input.strip() and not b_input.strip():
        st.warning("⚠️ Vui lòng điền thông tin quân bài.")
    else:
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        
        if p_list or b_list:
            # 1. Đưa toàn bộ các lá bài thực tế vừa ra vào Khay bài lịch sử lịch sử để triệt tiêu quân bài chuẩn xác
            st.session_state.shoe_history.extend(p_list + b_list)
            
            # Xác định kết quả ván vừa rồi để vẽ bảng Road mạch bài
            p_final = sum([0 if c >= 10 else c for c in p_list]) % 10
            b_final = sum([0 if c >= 10 else c for c in b_list]) % 10
            if p_final > b_final: st.session_state.outcome_history.append("Player")
            elif b_final > p_final: st.session_state.outcome_history.append("Banker")
            else: st.session_state.outcome_history.append("Tie")
            
            # 2. Tính toán xác suất cho ván MỚI TIẾP THEO dựa trên khay bài đã trừ đi các lá trên
            core_output = calculate_baccarat_v20_ultimate(
                [], [], st.session_state.shoe_history, shoe_decks=decks,
                manual_cards_used=manual_cards, manual_games_played=len(st.session_state.outcome_history),
                p_wins=st.session_state.outcome_history.count("Player"), 
                b_wins=st.session_state.outcome_history.count("Banker"), 
                tie_wins=st.session_state.outcome_history.count("Tie")
            )
            
            st.session_state.last_results = core_output
            
            # Thay vì gọi st.rerun(), sử dụng cơ chế đổi trạng thái để Streamlit tự động re-render mượt mà.
            st.success("Đã nạp dữ liệu thành công! Biểu đồ phía trên đã cập nhật cho ván tiếp theo.")
