import streamlit as st
import pandas as pd
import time
import random
from urllib.parse import urlparse

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
# LÕI TOÁN HỌC BACCARAT v20.2 (HỖ TRỢ ĐẾM BÀI CHUYÊN SÂU & ƯỚC TÍNH PHÂN RÃ)
# =========================================================================
def calculate_baccarat_v20_ultimate(p_cards, b_cards, shoe_history, shoe_decks=8, 
                                    manual_cards_used=0, manual_games_played=0,
                                    p_wins=0, b_wins=0, tie_wins=0):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}

    detailed_cards_count = len(shoe_history)
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure:
                deck_structure[card_val] = max(0.0, deck_structure[card_val] - 1.0)
        cards_left = total_initial_cards - detailed_cards_count
        mode = "SIÊU TỔ HỢP MARKOV (LIVE-MATRIX v20.2)"
    else:
        cards_removed = max(0, manual_cards_used if manual_cards_used > 0 else int((p_wins * 4.9) + (b_wins * 4.9) + (tie_wins * 5.2)))
        if cards_removed == 0 and manual_games_played > 0:
            cards_removed = int(manual_games_played * 4.89)
            
        cards_left = max(0, total_initial_cards - cards_removed)
        mode = "MA TRẬN QUANTUM-BAYES v20.2" if cards_removed > 0 else "KHAY BÀI NGUYÊN BẢN"
        
        if cards_removed > 0:
            consumed_ratio = cards_removed / total_initial_cards
            for card_num in deck_structure:
                deck_structure[card_num] = max(0.0, (4 * shoe_decks) * (1.0 - consumed_ratio))

    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: score_deck[0] += count
        else: score_deck[card_num] += count

    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] -= 1

    N_total = float(sum(score_deck))
    if N_total <= 10:
        return {"Player": 44.62, "Banker": 45.86, "Tie": 9.52}, deck_structure, 11.5, 11.5, "KHÔNG ĐỦ MẪU - ĐANG DÙNG XÁC SUẤT GỐC", cards_left, True

    p_pair_prob = sum((deck_structure[i]/N_total)*((deck_structure[i]-1)/(N_total-1)) for i in range(1, 14) if deck_structure[i] >= 2)
    p_pair_odds = round(p_pair_prob * 100, 2)

    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    if (len(p_cards) == 2 and p_score >= 8) or (len(b_cards) == 2 and b_score >= 8):
        if p_score == b_score: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, p_pair_odds, mode, cards_left, True
        elif p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, p_pair_odds, mode, cards_left, True
        else: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, p_pair_odds, mode, cards_left, True

    player_wins, banker_wins, ties = 0.0, 0.0, 0.0

    if p_score >= 6:
        if b_score <= 5:
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
    else:
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
                
            score_deck[card3_p] += 1

    total_prob = player_wins + banker_wins + ties
    if total_prob == 0: total_prob = 1.0

    odds_res = {
        "Player": round((player_wins / total_prob) * 100, 2),
        "Banker": round((banker_wins / total_prob) * 100, 2),
        "Tie": round((ties / total_prob) * 100, 2)
    }
    return odds_res, deck_structure, p_pair_odds, p_pair_odds, mode, cards_left, True

def detect_baccarat_pattern(outcome_list):
    clean_list = [x for x in outcome_list if x in ["Player", "Banker"]]
    if len(clean_list) < 4: return "🔄 Đang tích lũy dữ liệu...", "#888888"
    last_side = clean_list[-1]
    streak_count = 0
    for item in reversed(clean_list):
        if item == last_side: streak_count += 1
        else: break
    if streak_count >= 4:
        side_vietnamese = "🔵 PLAYER" if last_side == "Player" else "🔴 BANKER"
        return f"🔥 CẦU BỆT {side_vietnamese} ({streak_count} ván!)", "#ff7675"
    return "📊 Khay bài sóng phẳng", "#2ecc71"

# =========================================================================
# LÕI CÀO DỮ LIỆU TỰ ĐỘNG - AUTO XPATH CHUYÊN SÂU
# =========================================================================
def suggest_xpath_by_url(url):
    """
    Tự động phân tích tên miền/đường dẫn sòng bạc để xuất XPath khớp với thiết kế Web của sòng đó
    """
    if not url:
        return "//div[contains(@class, 'road-item')]"
    
    parsed_url = urlparse(url).netloc.lower()
    
    if "evo" in parsed_url or "evolution" in parsed_url:
        return "//div[contains(@data-testid, 'road-cell')] | //svg[contains(@class, 'bead-plate')]"
    elif "pragmatic" in parsed_url or "pplive" in parsed_url:
        return "//div[contains(@class, 'baccarat-road')]//span"
    elif "wmcas" in parsed_url or "wmgaming" in parsed_url:
        return "//td[contains(@class, 'road-ball')]"
    elif "sa-gaming" in parsed_url or "sanie" in parsed_url:
        return "//div[contains(@id, 'BeadRoad')]//div"
    elif "dg" in parsed_url or "dreamgaming" in parsed_url:
        return "//div[contains(@class, 'road_bead')]//i"
    
    # XPath mặc định thông minh có khả năng bao quát cao nếu không khớp sòng nào phía trên
    return "//div[contains(@class, 'road') or contains(@class, 'result') or contains(@class, 'cell')]"

def fetch_live_web_data_stealth(url, target_xpath):
    if not SELENIUM_AVAILABLE:
        return "ERROR_LIB", "Chưa cài đặt Selenium."
    
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    try:
        driver = webdriver.Chrome(options=options)
        if STEALTH_LIB_AVAILABLE:
            stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris", fix_hairline=True)
        
        driver.get(url)
        time.sleep(4.0) 
        
        wait = WebDriverWait(driver, 7)
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, target_xpath)))
        
        scraped_outcomes = []
        for elem in elements:
            text = elem.text.strip().upper()
            # Đọc cả text lẫm các class màu sắc/ký tự đặc trưng
            html_class = elem.get_attribute("class").upper()
            
            if any(p in text for p in ['PLAYER', 'CON', 'P', '🔵']) or 'PLAYER' in html_class or 'BLUE' in html_class: 
                scraped_outcomes.append('Player')
            elif any(b in text for b in ['BANKER', 'CÁI', 'B', '🔴']) or 'BANKER' in html_class or 'RED' in html_class: 
                scraped_outcomes.append('Banker')
            elif any(t in text for t in ['TIE', 'HÒA', 'T', '🟢']) or 'TIE' in html_class or 'GREEN' in html_class: 
                scraped_outcomes.append('Tie')
            
        driver.quit()
        return "SUCCESS", scraped_outcomes
    except Exception as e:
        try: driver.quit()
        except: pass
        return "ERROR_CONN", str(e)

# =========================================================================
# GIAO DIỆN CHÍNH (STREAMLIT UI RENDER)
# =========================================================================
st.set_page_config(page_title="Oracle Hybrid Matrix v20.2", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    .hud-box { padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px; border: 1px solid #4f4f4f; background-color: #1a1a1a; }
    .hud-title { font-size: 12px; font-weight: 600; color: #b0b0b0; }
    .hud-value { font-size: 32px; font-weight: 800; font-family: monospace; margin-top: 4px; }
    .neon-player-advantage { background-color: #0984e3 !important; border: 2px solid #74b9ff !important; box-shadow: 0 0 12px rgba(9, 132, 227, 0.6); }
    .neon-banker-advantage { background-color: #d63031 !important; border: 2px solid #ff7675 !important; box-shadow: 0 0 12px rgba(214, 48, 49, 0.6); }
    .trend-hud { padding: 12px; border-radius: 6px; background-color: #151515; border: 1px dashed #444; margin-top: 10px; }
    .trend-string { font-size: 18px; font-family: monospace; letter-spacing: 5px; font-weight: 800; }
    .char-p { color: #54a0ff; } .char-b { color: #ff7675; } .char-t { color: #2ecc71; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("🔮 THIẾT LẬP HỆ THỐNG")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📡 CHẾ ĐỘ QUÉT AUTO CƠ SỞ")

auto_scrape_enabled = False
if AUTOREFRESH_AVAILABLE and SELENIUM_AVAILABLE:
    auto_scrape_enabled = st.sidebar.checkbox("Kích hoạt Quét Link Tự Động", value=False)
    
    if auto_scrape_enabled:
        target_url = st.sidebar.text_input("Nhập Link Web bàn bài:", value="https://evo-casino-example.com/baccarat1")
        
        # [TÍNH NĂNG ĐỘNG]: Tự động sinh XPath phù hợp dựa trên đường dẫn vừa nhập
        suggested_xpath = suggest_xpath_by_url(target_url)
        xpath_selector = st.sidebar.text_input("Xpath định vị chuỗi kết quả (Đã tự điền mẫu):", value=suggested_xpath)
        
        refresh_rate = st.sidebar.slider("Tần suất quét lại (Giây):", 15, 120, 30)
        st_autorefresh(interval=refresh_rate * 1000, key="baccarat_auto_scraped_core")
else:
    st.sidebar.warning("⚠️ Không thể bật quét tự động do máy thiếu thư viện Chrome Driver/Selenium.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 THIẾT LẬP NỀN (CHỈ DÙNG KHI CHẠY BẰNG TAY)")

# Vô hiệu hóa cấu hình nền trong sidebar nếu đang chạy Auto để tránh xung đột dữ liệu
disable_inputs = auto_scrape_enabled

manual_cards = st.sidebar.number_input("Số lá bài đã hủy/đã chia:", 0, decks*52, 0, disabled=disable_inputs)
p_wins_sidebar = st.sidebar.number_input("🔵 Số ván Player thắng:", 0, 150, 0, disabled=disable_inputs)
b_wins_sidebar = st.sidebar.number_input("🔴 Số ván Banker thắng:", 0, 150, 0, disabled=disable_inputs)
tie_wins_sidebar = st.sidebar.number_input("🟢 Số ván Hòa thắng:", 0, 150, 0, disabled=disable_inputs)

if st.sidebar.button("🗑️ RESET TOÀN BỘ SỐ LIỆU", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.outcome_history = []
    st.session_state.last_results = None
    st.toast("Đã làm sạch toàn bộ khay bài ảo!")

# --- XỬ LÝ LẤY DỮ LIỆU TỰ ĐỘNG ---
if auto_scrape_enabled:
    with st.spinner("🕵️ Khay tàng hình đang đồng bộ dữ liệu Road sòng bài..."):
        status, web_data = fetch_live_web_data_stealth(target_url, xpath_selector)
        if status == "SUCCESS" and len(web_data) > 0:
            st.session_state.outcome_history = web_data
            # Tính toán ma trận dựa trên kết quả đồng bộ tự động
            st.session_state.last_results = calculate_baccarat_v20_ultimate(
                [], [], st.session_state.shoe_history, shoe_decks=decks,
                manual_games_played=len(web_data),
                p_wins=web_data.count("Player"),
                b_wins=web_data.count("Banker"),
                tie_wins=web_data.count("Tie")
            )
        elif status.startswith("ERROR"):
            st.sidebar.error("❌ Không thể cào dữ liệu từ link này. Hãy kiểm tra lại cấu hình XPath hoặc chuyển về chạy BẰNG TAY.")

# --- NẾU CHẠY BẰNG TAY (KHI KHÔNG DÙNG LINK HOẶC KHÔNG BẬT AUTO) ---
if not auto_scrape_enabled and not st.session_state.last_results:
    # Khởi tạo bảng tính ban đầu cho chế độ chạy tay
    st.session_state.last_results = calculate_baccarat_v20_ultimate(
        [], [], st.session_state.shoe_history, shoe_decks=decks,
        manual_cards_used=manual_cards,
        manual_games_played=p_wins_sidebar + b_wins_sidebar + tie_wins_sidebar,
        p_wins=p_wins_sidebar, b_wins=b_wins_sidebar, tie_wins=tie_wins_sidebar
    )

# =========================================================================
# KHỐI HIỂN THỊ KẾT QUẢ DỰ ĐOÁN HUD
# =========================================================================
if st.session_state.last_results:
    res, _, p_pair, _, mode, cards_left, _ = st.session_state.last_results
    
    p_box_css = "hud-box neon-player-advantage" if res['Player'] > res['Banker'] else "hud-box"
    b_box_css = "hud-box neon-banker-advantage" if res['Banker'] > res['Player'] else "hud-box"
    
    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 XÁC SUẤT PLAYER</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 XÁC SUẤT BANKER</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box"><div class="hud-title">🟢 XÁC SUẤT TIE (HÒA)</div><div class="hud-value" style="color: #2ecc71;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
        
    with right_col:
        st.markdown("#### 💎 Tỷ Lệ Cược Cặp")
        st.metric("🔵 PLAYER PAIR / CÁI ĐÔI", f"{p_pair}%")
        
        # Hiển thị chuỗi Road bài hiện tại
        if st.session_state.outcome_history:
            trend_letters = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.outcome_history]
            pattern_msg, pattern_color = detect_baccarat_pattern(st.session_state.outcome_history)
            st.markdown(f'<div class="trend-hud"><div class="trend-string">{" ".join(trend_letters)}</div><div style="color: {pattern_color}; font-size:12px; font-weight:bold; margin-top:5px;">{pattern_msg}</div></div>', unsafe_allow_html=True)
        else:
            st.info("Chưa có chuỗi dữ liệu xu hướng Road.")
            
        st.caption(f"**Chế độ core:** {mode} | **Quân bài còn lại:** {int(cards_left)}")

# =========================================================================
# KHỐI ĐIỀU KHIỂN & GHI NHẬN BẰNG TAY (CHỈ HIỆN KHI KHÔNG DÙNG LINK HOẶC BẬT CHẠY TAY)
# =========================================================================
if not auto_scrape_enabled:
    st.markdown("---")
    st.subheader("🎯 BÀN ĐIỀU KHIỂN CHẠY BẰNG TAY (MANUAL MODE)")
    
    # Lựa chọn 1: Ghi nhận nhanh kết quả (Dành cho người chơi muốn điền Road nhanh không cần nhập lá bài)
    st.markdown("##### Cách 1: Ghi nhận nhanh kết quả ván vừa rồi (Vẽ Mạch Bài)")
    btn_p, btn_b, btn_t = st.columns(3)
    
    with btn_p:
        if st.button("🔵 PLAYER THẮNG", use_container_width=True):
            st.session_state.outcome_history.append("Player")
            st.session_state.last_results = calculate_baccarat_v20_ultimate(
                [], [], st.session_state.shoe_history, shoe_decks=decks,
                manual_games_played=len(st.session_state.outcome_history),
                p_wins=st.session_state.outcome_history.count("Player"),
                b_wins=st.session_state.outcome_history.count("Banker"),
                tie_wins=st.session_state.outcome_history.count("Tie")
            )
            st.toast("Đã thêm Player vào mạch bài!")
            
    with btn_b:
        if st.button("🔴 BANKER THẮNG", use_container_width=True):
            st.session_state.outcome_history.append("Banker")
            st.session_state.last_results = calculate_baccarat_v20_ultimate(
                [], [], st.session_state.shoe_history, shoe_decks=decks,
                manual_games_played=len(st.session_state.outcome_history),
                p_wins=st.session_state.outcome_history.count("Player"),
                b_wins=st.session_state.outcome_history.count("Banker"),
                tie_wins=st.session_state.outcome_history.count("Tie")
            )
            st.toast("Đã thêm Banker vào mạch bài!")
            
    with btn_t:
        if st.button("🟢 TIE (HÒA) THẮNG", use_container_width=True):
            st.session_state.outcome_history.append("Tie")
            st.session_state.last_results = calculate_baccarat_v20_ultimate(
                [], [], st.session_state.shoe_history, shoe_decks=decks,
                manual_games_played=len(st.session_state.outcome_history),
                p_wins=st.session_state.outcome_history.count("Player"),
                b_wins=st.session_state.outcome_history.count("Banker"),
                tie_wins=st.session_state.outcome_history.count("Tie")
            )
            st.toast("Đã thêm Hòa vào mạch bài!")

    # Lựa chọn 2: Nhập chi tiết quân bài lật để đếm bài chính xác tuyệt đối
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### Cách 2: Nhập chi tiết các lá bài lật (Để triệt tiêu quân bài khay chính xác)")
    
    col_p, col_b = st.columns(2)
    with col_p: p_input = st.text_input("PLAYER (Ví dụ: 9,A hoặc K,2,7):", value="", key="manual_p_cards")
    with col_b: b_input = st.text_input("BANKER (Ví dụ: 10,J hoặc 5,5,A):", value="", key="manual_b_cards")
    
    def clean_and_parse_input(raw_str):
        if not raw_str: return []
        normalized = raw_str.upper().replace(" ", "")
        tokens = normalized.split(",") if "," in normalized else list(normalized)
        mapping = {'A': 1, 'T': 10, 'J': 11, 'Q': 12, 'K': 13}
        res_list = []
        for t in tokens:
            if t in mapping: res_list.append(mapping[t])
            elif t.isdigit() and 2 <= int(t) <= 10: res_list.append(int(t))
        return res_list

    if st.button("🚀 NẠP BÀI VÀ DỰ ĐOÁN XÁC SUẤT VÁN TIẾP THEO", use_container_width=True, type="primary"):
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        
        if p_list or b_list:
            # Lưu các quân bài đã lật vào lịch sử khay bài
            st.session_state.shoe_history.extend(p_list + b_list)
            
            # Phân định thắng thua thực tế từ các quân bài vừa nhập để đồng bộ vào mạch bài Road
            p_score_real = sum([0 if c >= 10 else c for c in p_list]) % 10
            b_score_real = sum([0 if c >= 10 else c for c in b_list]) % 10
            
            if p_score_real > b_score_real: st.session_state.outcome_history.append("Player")
            elif b_score_real > p_score_real: st.session_state.outcome_history.append("Banker")
            else: st.session_state.outcome_history.append("Tie")
            
            # Tính toán cho ván tiếp theo
            st.session_state.last_results = calculate_baccarat_v20_ultimate(
                [], [], st.session_state.shoe_history, shoe_decks=decks,
                manual_games_played=len(st.session_state.outcome_history),
                p_wins=st.session_state.outcome_history.count("Player"),
                b_wins=st.session_state.outcome_history.count("Banker"),
                tie_wins=st.session_state.outcome_history.count("Tie")
            )
            st.success("Đã ghi nhận các lá bài và tính toán lại ma trận!")
else:
    st.info("📡 Đang ở chế độ quét tự động từ Link bàn. Toàn bộ bảng điều khiển bằng tay tạm thời ẩn để bảo vệ tiến trình dữ liệu.")
