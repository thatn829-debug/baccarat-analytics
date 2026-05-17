import streamlit as st
import pandas as pd
import time

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
    from selenium.webdriver.common.action_chains import ActionChains
except ImportError:
    SELENIUM_AVAILABLE = False

# =========================================================================
# SYSTEM CORE v18.2: ULTRA QUANTUM ENGINE
# =========================================================================
def calculate_baccarat_v18_ultimate(p_cards, b_cards, shoe_history, shoe_decks=8, 
                                    manual_cards_used=0, manual_games_played=0,
                                    p_wins=0, b_wins=0, tie_wins=0):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}

    if manual_cards_used > total_initial_cards or manual_games_played > int(total_initial_cards / 4):
        return "❌ Bất hợp lý: Cấu hình vượt quá giới hạn vật lý của khay bài!", {}, 0.0, 0.0, "LỖI", total_initial_cards, False, []

    detailed_cards_count = len(shoe_history)
    
    if detailed_cards_count > 0:
        for card_val in shoe_history:
            if card_val in deck_structure:
                deck_structure[card_val] -= 1
        cards_left = total_initial_cards - detailed_cards_count
        mode = "SIÊU TỔ HỢP MARKOV PHI HOÀN LẠI (CHI TIẾT)"
    else:
        cards_removed = max(0, manual_cards_used if manual_cards_used > 0 else int((p_wins * 4.86) + (b_wins * 4.81) + (tie_wins * 5.23)))
        if cards_removed == 0 and manual_games_played > 0:
            cards_removed = int(manual_games_played * 4.852)
            
        cards_left = max(0, total_initial_cards - cards_removed)
        mode = "MA TRẬN PHÂN RÃ BAYES PHI TUYẾN TÍNH" if cards_removed > 0 else "KHAY BÀI NGUYÊN BẢN (XÁC SUẤT GỐC)"
        
        if cards_removed > 0:
            consumed_ratio = cards_removed / total_initial_cards
            for card_num in deck_structure:
                reduction = (4 * shoe_decks) * consumed_ratio
                deck_structure[card_num] = max(0.0, (4 * shoe_decks) - reduction)

    invalid_cards_list = []
    for card_num, count in deck_structure.items():
        if count < 0:
            card_labels = {1: "A", 11: "J", 12: "Q", 13: "K"}
            label = card_labels.get(card_num, f"[{card_num}]")
            invalid_cards_list.append(f"{label} ({round(count, 1)} lá)")
            
    is_shoe_logical = (len(invalid_cards_list) == 0)
    
    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: score_deck[0] += count
        else: score_deck[card_num] += count

    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] -= 1

    N_total = float(sum(score_deck))
    if N_total <= 12:
        return "⚠️ Cảnh báo: Khay bài không đủ quân để thiết lập không gian mẫu!", deck_structure, 0.0, 0.0, mode, cards_left, is_shoe_logical, invalid_cards_list

    p_pair_prob = sum((deck_structure[i]/N_total)*((deck_structure[i]-1)/(N_total-1)) for i in range(1, 14) if deck_structure[i] >= 2)
    p_pair_odds = round(p_pair_prob * 100, 4)

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
    b_pair_odds = round(b_pair_prob * 100, 4)

    p_score = sum([0 if c >= 10 else c for c in p_cards]) % 10
    b_score = sum([0 if c >= 10 else c for c in b_cards]) % 10

    if (len(p_cards) == 2 and p_score >= 8) or (len(b_cards) == 2 and b_score >= 8):
        if p_score == b_score: return {"Player": 0.0, "Banker": 0.0, "Tie": 100.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list
        elif p_score > b_score: return {"Player": 100.0, "Banker": 0.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list
        else: return {"Player": 0.0, "Banker": 100.0, "Tie": 0.0}, deck_structure, p_pair_odds, b_pair_odds, mode, cards_left, is_shoe_logical, invalid_cards_list

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

# =========================================================================
# ULTRA SCRAPER: ĐIỀU HƯỚNG TỰ ĐỘNG (CLICK SẢNH -> CHỌN TRÒ -> VÀO BÀN)
# =========================================================================
def auto_navigation_and_scrape(url, casino_btn_xpath, baccarat_tab_xpath, table_click_xpath, result_xpath):
    if not SELENIUM_AVAILABLE:
        return "ERROR_LIB", "Thiếu thư viện Selenium."
    
    options = Options()
    # Gỡ bỏ headless tạm thời nếu trang web chặn bot mạnh, hoặc giữ nếu chạy ngầm ổn định
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1440,900")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        
        # BƯỚC 1: Tìm và Click vào danh mục Casino/Sòng Bài Trực Tuyến
        if casino_btn_xpath:
            btn_casino = wait.until(EC.element_to_be_clickable((By.XPATH, casino_btn_xpath)))
            btn_casino.click()
            time.sleep(2) # Chờ hiệu ứng chuyển trang
            
        # XỬ LÝ IFRAME (Hầu hết các sảnh live đều lồng iframe)
        if len(driver.find_elements(By.TAG_NAME, "iframe")) > 0:
            driver.switch_to.frame(0) # Nhảy vào iframe đầu tiên chứa game

        # BƯỚC 2: Chọn tab trò chơi "Baccarat" trong sảnh
        if baccarat_tab_xpath:
            tab_bac = wait.until(EC.element_to_be_clickable((By.XPATH, baccarat_tab_xpath)))
            tab_bac.click()
            time.sleep(1.5)

        # BƯỚC 3: Click chọn bàn cụ thể
        if table_click_xpath:
            target_table = wait.until(EC.element_to_be_clickable((By.XPATH, table_click_xpath)))
            ActionChains(driver).move_to_element(target_table).click().perform()
            time.sleep(4) # Đợi bàn cược tải xong đồ họa hiển thị kết quả

        # BƯỚC 4: Tiến hành bóc tách chuỗi kết quả (Road map)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, result_xpath)))
        elements = driver.find_elements(By.XPATH, result_xpath)
        
        scraped_outcomes = []
        for elem in elements:
            text = elem.text.strip().upper()
            # Đọc theo Text hoặc theo Class định dạng màu của ô tròn
            class_attr = elem.get_attribute("class").upper()
            if 'PLAYER' in text or text == 'P' or 'PLAYER' in class_attr: scraped_outcomes.append('Player')
            elif 'BANKER' in text or text == 'B' or 'BANKER' in class_attr: scraped_outcomes.append('Banker')
            elif 'TIE' in text or text == 'T' or 'HÒA' in text or 'HOA' in text or 'TIE' in class_attr: scraped_outcomes.append('Tie')
            
        if not scraped_outcomes:
            return "ERROR_EMPTY", "Đã vào được giao diện nhưng chưa lấy được kết quả từ XPath đích."
            
        return "SUCCESS", scraped_outcomes
    except Exception as e:
        return "ERROR_NAV", f"Lỗi tại tiến trình điều hướng: {str(e)}"
    finally:
        if driver:
            driver.quit()

# =========================================================================
# INTERFACE DESIGN & STYLES
# =========================================================================
st.set_page_config(page_title="Oracle Engine v18.2 Patched", page_icon="🔮", layout="centered")

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
    .neon-tie-alert { border: 2px solid #2ecc71 !important; box-shadow: 0 0 15px rgba(46, 204, 113, 0.8); }
    .validation-hud { padding: 12px; border-radius: 6px; text-align: center; font-weight: 700; font-size: 14px; margin-top: 12px; font-family: monospace; }
    .logic-pass { background-color: rgba(46, 204, 113, 0.15); border: 2px solid #2ecc71; color: #2ecc71; }
    .trend-hud { padding: 14px; border-radius: 6px; background-color: #151515; border: 1px dashed #444; margin-top: 12px; }
    .trend-string { font-size: 18px; font-family: monospace; letter-spacing: 6px; font-weight: 800; overflow-x: auto; }
    .char-p { color: #54a0ff; } .char-b { color: #ff7675; } .char-t { color: #2ecc71; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None
if 'last_played_cards' not in st.session_state: st.session_state.last_played_cards = ""

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ CẤU HÌNH KHAY BÀI")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌐 LUỒNG TRUY CẬP ĐIỀU HƯỚNG")

auto_scrape_enabled = st.sidebar.checkbox("Kích hoạt Robot Tự Động Vào Bàn", value=False)
target_url = st.sidebar.text_input("1. Nhập Link Trang Chủ:", value="https://example-game.com")

st.sidebar.markdown("**Tọa độ XPath điều hướng:**")
xpath_casino = st.sidebar.text_input("XPath nút [CASINO]:", value="//a[contains(text(), 'Live Casino')]")
xpath_baccarat = st.sidebar.text_input("XPath tab [BACCARAT]:", value="//div[@id='baccarat-tab']")
xpath_table = st.sidebar.text_input("XPath chọn [BÀN SỐ 1]:", value="//button[contains(@class, 'table-join-btn')][1]")
xpath_results = st.sidebar.text_input("XPath bóc chuỗi ô tròn kết quả:", value="//div[contains(@class, 'road-cell')]")

refresh_rate = st.sidebar.slider("Tần suất đồng bộ lại (Giây):", min_value=15, max_value=120, value=30)

if auto_scrape_enabled and AUTOREFRESH_AVAILABLE:
    st_autorefresh(interval=refresh_rate * 1000, key="auto_nav_scraper_v18")

# Đồng bộ dữ liệu nâng cao qua luồng tự động click
p_wins_input, b_wins_input, tie_wins_input, manual_games, manual_cards = 0, 0, 0, 0, 0
if auto_scrape_enabled and SELENIUM_AVAILABLE:
    with st.spinner("🤖 Robot đang click điều hướng sảnh & bóc tách dữ liệu bàn..."):
        status, web_data = auto_navigation_and_scrape(target_url, xpath_casino, xpath_baccarat, xpath_table, xpath_results)
        if status == "SUCCESS" and len(web_data) > 0:
            st.sidebar.success(f"✅ Đã kết nối trực tiếp! Quét được {len(web_data)} ván gần nhất.")
            st.session_state.outcome_history = web_data
            p_wins_input = web_data.count("Player")
            b_wins_input = web_data.count("Banker")
            tie_wins_input = web_data.count("Tie")
            manual_games = len(web_data)
        elif status.startswith("ERROR"):
            st.sidebar.error(f"❌ {web_data}")

# --- PANEL OUTPUT CONTROL ---
if st.session_state.last_results:
    results_data = st.session_state.last_results
    if not isinstance(results_data[0], str):
        res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical, invalid_cards = results_data
        
        p_box_css = "hud-box"
        b_box_css = "hud-box"
        tie_box_css = "hud-box"
        if res['Player'] > res['Banker']: p_box_css = "hud-box neon-player-advantage"
        elif res['Banker'] > res['Player']: b_box_css = "hud-box neon-banker-advantage"
            
        left_result_col, right_pair_col = st.columns(2)
        with left_result_col:
            st.markdown("#### 📊 Dự Đoán Xác Suất Cửa Chính")
            st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
            
        with right_pair_col:
            st.markdown("#### 💎 Tỷ Lệ Cược Phụ & Xu hướng")
            st.metric("🔵 PLAYER PAIR", f"{p_pair}%")
            st.metric("🔴 BANKER PAIR", f"{b_pair}%")
            
            if st.session_state.outcome_history:
                trend_letters = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.outcome_history]
                st.markdown(f'<div class="trend-hud"><div class="trend-string">{" ".join(trend_letters)}</div></div>', unsafe_allow_html=True)
else:
    st.info("🔮 ENGINE READY. Vui lòng nạp quân bài ván trực tiếp hoặc bật chế độ tự động.")

# --- ĐIỀU KHIỂN NHẬP TAY KHI CẦN THIẾT ---
st.markdown("---")
st.subheader("🃏 Nhập Dữ Liệu Dự Đoán Ván Tiếp Theo")
col_p, col_b = st.columns(2)
with col_p: p_input = st.text_input("PLAYER (Các lá vừa chia):", value="", placeholder="Ví dụ: 5,K")
with col_b: b_input = st.text_input("BANKER (Các lá vừa chia):", value="", placeholder="Ví dụ: J,7")

def clean_and_parse_input(raw_str):
    if not raw_str: return []
    normalized = raw_str.upper().replace(" ", "")
    tokens = normalized.split(",") if "," in normalized else list(normalized)
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    res = []
    for t in tokens:
        if t in mapping: res.append(mapping[t])
        elif t.isdigit() and 2 <= int(t) <= 10: res.append(int(t))
    return res

if st.button("🚀 GHI NHẬN VÀ TÍNH TOÁN VÁN TIẾP THEO", use_container_width=True, type="primary"):
    current_game_signature = f"P:{p_input.strip()}|B:{b_input.strip()}"
    p_list = clean_and_parse_input(p_input)
    b_list = clean_and_parse_input(b_input)
    
    core_output = calculate_baccarat_v18_ultimate(
        p_list, b_list, st.session_state.shoe_history, shoe_decks=decks,
        manual_cards_used=manual_cards, manual_games_played=manual_games,
        p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
    )
    if not isinstance(core_output, str):
        st.session_state.last_results = core_output
        if not auto_scrape_enabled:
            st.session_state.shoe_history.extend(p_list + b_list)
        st.rerun()
