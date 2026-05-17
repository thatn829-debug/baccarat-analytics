import streamlit as st
import pandas as pd
import time
import random
import math
from urllib.parse import urlparse

# =========================================================================
# KHỐI CAO CẤP: TÍCH HỢP LỚP TÀNG HÌNH THẾ HỆ MỚI (ANTI-FINGERPRINTING)
# =========================================================================
AUTOREFRESH_AVAILABLE = True
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    AUTOREFRESH_AVAILABLE = False

UC_AVAILABLE = True
try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    
    try:
        from selenium_stealth import stealth
        STEALTH_LIB_AVAILABLE = True
    except ImportError:
        STEALTH_LIB_AVAILABLE = False
except ImportError:
    UC_AVAILABLE = False

# =========================================================================
# LÕI THUẬT TOÁN TOÁN HỌC KHÔNG LỖI (V20.6.0 - ZERO-FAULT QUANTUM MATRIX)
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
        mode = "SIÊU TỔ HỢP TÍCH PHÂN TỐI CAO (REAL-TIME MATRIX v20.6.0)"
    else:
        cards_removed = max(0, manual_cards_used if manual_cards_used > 0 else int((p_wins * 4.94) + (b_wins * 4.93) + (tie_wins * 5.01)))
        cards_left = max(0, total_initial_cards - cards_removed)
        mode = "HỆ THỐNG ƯỚC LƯỢNG BAYESIAN-QUANTUM v20.6.0"
        if cards_removed > 0:
            consumed_ratio = cards_removed / total_initial_cards
            for card_num in deck_structure:
                deck_structure[card_num] = max(0.0, (4 * shoe_decks) * (1.0 - consumed_ratio))

    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: 
            score_deck[0] += count  
        else: 
            score_deck[card_num] += count

    for card in p_cards + b_cards:
        val = 0 if card >= 10 else card
        if score_deck[val] > 0: score_deck[val] = max(0.0, score_deck[val] - 1.0)

    N_total = float(sum(score_deck))
    if N_total <= 6.0: 
        return {"Player": 44.62, "Banker": 45.86, "Tie": 9.52}, deck_structure, 11.5, mode, max(0.0, cards_left)

    p_pair_prob = sum((deck_structure[i] / N_total) * ((deck_structure[i] - 1.0) / max(1.0, N_total - 1.0)) for i in range(1, 14) if deck_structure[i] >= 2)
    p_pair_odds = round(p_pair_prob * 100, 2)

    player_wins, banker_wins, ties = 0.0, 0.0, 0.0

    for p_draw_1 in range(10):
        w_p1 = score_deck[p_draw_1]
        if w_p1 <= 0.001: continue
        prob_p1 = w_p1 / N_total
        score_deck[p_draw_1] -= 1.0
        
        for b_draw_1 in range(10):
            w_b1 = score_deck[b_draw_1]
            if w_b1 <= 0.001: continue
            prob_b1 = prob_p1 * (w_b1 / max(1.0, N_total - 1.0))
            score_deck[b_draw_1] -= 1.0
            
            for p_draw_2 in range(10):
                w_p2 = score_deck[p_draw_2]
                if w_p2 <= 0.001: continue
                prob_p2 = prob_b1 * (w_p2 / max(1.0, N_total - 2.0))
                score_deck[p_draw_2] -= 1.0
                
                for b_draw_2 in range(10):
                    w_b2 = score_deck[b_draw_2]
                    if w_b2 <= 0.001: continue
                    prob_b2 = prob_p2 * (w_b2 / max(1.0, N_total - 3.0))
                    score_deck[b_draw_2] -= 1.0
                    
                    init_p = (p_draw_1 + p_draw_2) % 10
                    init_b = (b_draw_1 + b_draw_2) % 10
                    
                    if init_p >= 8 or init_b >= 8:
                        if init_p > init_b: player_wins += prob_b2
                        elif init_b > init_p: banker_wins += prob_b2
                        else: ties += prob_b2
                    else:
                        p_draws_3rd = init_p <= 5
                        
                        if p_draws_3rd:
                            for p_draw_3 in range(10):
                                w_p3 = score_deck[p_draw_3]
                                if w_p3 <= 0.001: continue
                                prob_p3 = prob_b2 * (w_p3 / max(1.0, N_total - 4.0))
                                score_deck[p_draw_3] -= 1.0
                                
                                final_p = (init_p + p_draw_3) % 10
                                b_draws_3rd = False
                                if init_b <= 2: b_draws_3rd = True
                                elif init_b == 3 and p_draw_3 != 8: b_draws_3rd = True
                                elif init_b == 4 and p_draw_3 in [2, 3, 4, 5, 6, 7]: b_draws_3rd = True
                                elif init_b == 5 and p_draw_3 in [4, 5, 6, 7]: b_draws_3rd = True
                                elif init_b == 6 and p_draw_3 in [6, 7]: b_draws_3rd = True
                                
                                if b_draws_3rd:
                                    for b_draw_3 in range(10):
                                        w_b3 = score_deck[b_draw_3]
                                        if w_b3 <= 0.001: continue
                                        prob_b3 = prob_p3 * (w_b3 / max(1.0, N_total - 5.0))
                                        final_b = (init_b + b_draw_3) % 10
                                        
                                        if final_p > final_b: player_wins += prob_b3
                                        elif final_b > final_p: banker_wins += prob_b3
                                        else: ties += prob_b3
                                else:
                                    if final_p > init_b: player_wins += prob_p3
                                    elif init_b > final_p: banker_wins += prob_p3
                                    else: ties += prob_p3
                                    
                                score_deck[p_draw_3] += 1.0
                        else:
                            final_p = init_p
                            b_draws_3rd = init_b <= 5
                            
                            if b_draws_3rd:
                                for b_draw_3 in range(10):
                                    w_b3 = score_deck[b_draw_3]
                                    if w_b3 <= 0.001: continue
                                    prob_b3 = prob_b2 * (w_b3 / max(1.0, N_total - 4.0))
                                    final_b = (init_b + b_draw_3) % 10
                                    
                                    if final_p > final_b: player_wins += prob_b3
                                    elif final_b > final_p: banker_wins += prob_b3
                                    else: ties += prob_b3
                            else:
                                if final_p > init_b: player_wins += prob_b2
                                elif init_b > final_p: banker_wins += prob_b2
                                else: ties += prob_b2
                                
                    score_deck[b_draw_2] += 1.0
                score_deck[p_draw_2] += 1.0
            score_deck[b_draw_1] += 1.0
        score_deck[p_draw_1] += 1.0

    total_prob = player_wins + banker_wins + ties
    if total_prob == 0: total_prob = 1.0
    
    odds_res = {
        "Player": round((player_wins / total_prob) * 100, 2),
        "Banker": round((banker_wins / total_prob) * 100, 2),
        "Tie": round((ties / total_prob) * 100, 2)
    }
    return odds_res, deck_structure, p_pair_odds, mode, max(0.0, cards_left)

def detect_baccarat_pattern(outcome_list):
    clean_list = [x for x in outcome_list if x in ["Player", "Banker"]]
    if len(clean_list) < 4: return "🔄 Đang tích lũy dữ liệu...", "#888888"
    last_side = clean_list[-1]
    streak_count = 0
    for item in reversed(clean_list):
        if item == last_side: streak_count += 1
        else: break
    if streak_count >= 4:
        return f"🔥 CẢNH BÁO: CẦU BỆT {'🔵 PLAYER' if last_side == 'Player' else '🔴 BANKER'} ({streak_count} ván!)", "#ff7675"
    return "📊 Khay bài sóng phẳng", "#2ecc71"

def suggest_xpath_by_url(url):
    if not url: return "//div[contains(@class, 'road-item')]"
    parsed_url = urlparse(url).netloc.lower()
    if "evo" in parsed_url or "evolution" in parsed_url:
        return "//div[contains(@data-testid, 'road-cell')] | //svg[contains(@class, 'bead-plate')]"
    elif "pragmatic" in parsed_url or "pplive" in parsed_url:
        return "//div[contains(@class, 'baccarat-road')]//span"
    elif "wmcas" in parsed_url or "wmgaming" in parsed_url:
        return "//td[contains(@class, 'road-ball')]"
    return "//div[contains(@class, 'road') or contains(@class, 'result') or contains(@class, 'cell')]"

# =========================================================================
# LÕI QUÉT BẢO MẬT TỐI HẬU: GIẢ LẬP HÀNH VI TỰ NHIÊN TRÁNH PHÁT HIỆN SÂU
# =========================================================================
def fetch_live_web_data_god_mode(url, target_xpath):
    if not UC_AVAILABLE:
        return "ERROR_LIB", "Chưa cài đặt thư viện undetected-chromedriver."
    
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Random hóa User-Agent ở mức độ sâu chống nhận diện dấu vân tay hệ thống (Fingerprint)
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    
    driver = None
    try:
        driver = uc.Chrome(options=options, version_main=None) 
        if STEALTH_LIB_AVAILABLE:
            stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
            
        driver.get(url)
        # Thời gian chờ ngẫu nhiên tránh tạo nhịp sinh học giống bot (Anti-Bot Pattern Timing)
        time.sleep(random.uniform(6.0, 9.5))
        
        # Mô phỏng tương tác nâng cao (Human-like Interaction Simulator)
        try:
            actions = ActionChains(driver)
            elements_to_hover = driver.find_elements(By.XPATH, "//div | //button")[:5]
            for elem in elements_to_hover:
                try:
                    actions.move_to_element(elem).pause(random.uniform(0.1, 0.4)).perform()
                except:
                    continue
            for _ in range(random.randint(2, 4)):
                actions.scroll_by_amount(0, random.randint(100, 300)).perform()
                time.sleep(random.uniform(0.5, 1.2))
        except:
            pass
            
        wait = WebDriverWait(driver, 12)
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, target_xpath)))
        
        scraped_outcomes = []
        for elem in elements:
            text = elem.text.strip().upper()
            html_class = elem.get_attribute("class").upper()
            
            if any(p in text for p in ['PLAYER', 'CON', 'P', '🔵']) or 'PLAYER' in html_class or 'BLUE' in html_class: 
                scraped_outcomes.append('Player')
            elif any(b in text for b in ['BANKER', 'CÁI', 'B', '🔴']) or 'BANKER' in html_class or 'RED' in html_class: 
                scraped_outcomes.append('Banker')
            elif any(t in text for t in ['TIE', 'HÒA', 'T', '🟢']) or 'TIE' in html_class or 'GREEN' in html_class: 
                scraped_outcomes.append('Tie')
                
        return "SUCCESS", scraped_outcomes
    except Exception as e:
        return "ERROR_CONN", str(e)
    finally:
        if driver is not None:
            try: 
                driver.close()
                driver.quit()
            except: 
                pass

# =========================================================================
# GIAO DIỆN CHÍNH (STREAMLIT UI)
# =========================================================================
st.set_page_config(page_title="Oracle God-Mode v20.6.0", page_icon="🔮", layout="centered")

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
    
    .sys-monitor-box { padding: 12px 18px; border-radius: 8px; margin-bottom: 20px; font-family: system-ui, sans-serif; line-height: 1.5; }
    .sys-good { background-color: rgba(46, 204, 113, 0.1); border: 1px solid #2ecc71; color: #2ecc71; }
    .sys-warn { background-color: rgba(241, 196, 15, 0.15); border: 1px solid #f1c40f; color: #f1c40f; }
    .sys-critical { background-color: rgba(231, 76, 60, 0.15); border: 1px solid #e74c3c; color: #e74c3c; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'last_results' not in st.session_state: st.session_state.last_results = None
if 'system_status' not in st.session_state: st.session_state.system_status = {"level": "NOMINAL", "msg": "Tất cả các lõi đều ổn định. Hệ thống sẵn sàng.", "action": ""}

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("🛡️ TRUNG TÂM KIỂM SOÁT BẢO MẬT")
decks = st.sidebar.selectbox("Số bộ bài sòng dùng:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📡 CẤU HÌNH LIÊN KẾT MẠNG")

auto_scrape_enabled = False
if UC_AVAILABLE and AUTOREFRESH_AVAILABLE:
    auto_scrape_enabled = st.sidebar.checkbox("KÍCH HOẠT QUÉT TÀNG HÌNH TỐI CAO", value=False)
    
    if auto_scrape_enabled:
        target_url = st.sidebar.text_input("Nhập Link Web bàn bài:", value="https://evo-casino-example.com/baccarat1")
        suggested_xpath = suggest_xpath_by_url(target_url)
        xpath_selector = st.sidebar.text_input("Xpath định vị chuỗi kết quả (Auto-Filled):", value=suggested_xpath)
        refresh_rate = st.sidebar.slider("Tần suất quét lại hệ thống (Giây):", 20, 120, 35)
        st_autorefresh(interval=refresh_rate * 1000, key="god_mode_stealth_refresh")
else:
    st.sidebar.error("⚠️ Cần cài đặt 'undetected-chromedriver' để quét tự động.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 CHẾ ĐỘ NHẬP TAY THỦ CÔNG")

disable_inputs = auto_scrape_enabled
manual_cards = st.sidebar.number_input("Số lá bài đã hủy/đã chia:", 0, decks*52, 0, disabled=disable_inputs)
p_wins_sidebar = st.sidebar.number_input("🔵 Số ván Player thắng:", 0, 150, 0, disabled=disable_inputs)
b_wins_sidebar = st.sidebar.number_input("🔴 Số ván Banker thắng:", 0, 150, 0, disabled=disable_inputs)
tie_wins_sidebar = st.sidebar.number_input("🟢 Số ván Hòa thắng:", 0, 150, 0, disabled=disable_inputs)

if st.sidebar.button("🗑️ RESET TOÀN BỘ SỐ LIỆU KHAY BÀI", use_container_width=True):
    st.session_state.shoe_history = []
    st.session_state.outcome_history = []
    st.session_state.last_results = None
    st.session_state.system_status = {"level": "NOMINAL", "msg": "Khay bài đã được đặt lại hoàn toàn. Lõi tính toán sạch.", "action": ""}
    st.rerun()

# --- ENGINE THỰC THI QUÉT WEB TỰ ĐỘNG VÀ ĐÁNH GIÁ SỨC KHỎE HỆ THỐNG ---
if auto_scrape_enabled:
    with st.spinner("🕵️ Lõi Vô Hình đang vượt Cloudflare và thu thập dữ liệu..."):
        status, web_data = fetch_live_web_data_god_mode(target_url, xpath_selector)
        if status == "SUCCESS" and len(web_data) > 0:
            st.session_state.outcome_history = web_data
            st.session_state.last_results = calculate_baccarat_v20_ultimate(
                [], [], st.session_state.shoe_history, shoe_decks=decks,
                manual_games_played=len(web_data),
                p_wins=web_data.count("Player"), b_wins=web_data.count("Banker"), tie_wins=web_data.count("Tie")
            )
            st.session_state.system_status = {
                "level": "NOMINAL",
                "msg": f"Đồng bộ trực tuyến THÀNH CÔNG. Đã quét thấy {len(web_data)} ván bài hoàn toàn ẩn danh.",
                "action": "✅ Không cần can thiệp. Hệ thống tự động làm mới sau mỗi chu kỳ."
            }
        elif status == "SUCCESS" and len(web_data) == 0:
            st.session_state.system_status = {
                "level": "WARNING",
                "msg": "Kết nối thành công tới trang đích nhưng KHÔNG tìm thấy chuỗi dữ liệu lịch sử bài.",
                "action": "⚠️ **Hành động đề xuất:** Cấu trúc HTML của sòng có thể vừa thay đổi. Hãy kiểm tra và điều chỉnh lại ô **Xpath định vị chuỗi kết quả** ở cột trái hoặc chuyển sang chế độ **NHẬP TAY THỦ CÔNG** để không làm gián đoạn dòng tiền."
            }
        elif status.startswith("ERROR"):
            st.session_state.system_status = {
                "level": "CRITICAL",
                "msg": f"Lỗi Luồng Quét: {web_data}",
                "action": "🚨 **Hành động đề xuất:** Tường lửa Cloudflare của sòng đang siết chặt hoặc lỗi mạng. Để bảo mật tuyệt đối, hãy **TẮT** mục 'KÍCH HOẠT QUÉT TÀNG HÌNH' ở cột trái ngay và chuyển sang sử dụng **BÀN ĐIỀU KHIỂN CHẠY BẰNG TAY** ở phía dưới."
            }

if not auto_scrape_enabled:
    if st.session_state.system_status["level"] not in ["NOMINAL", "WARNING", "CRITICAL"]:
        st.session_state.system_status = {
            "level": "NOMINAL_MANUAL",
            "msg": "Đang vận hành ở chế độ OFFLINE (Bằng tay). Cách ly hoàn toàn với máy chủ sòng.",
            "action": "✅ **An toàn 100%:** Hãy sử dụng các nút nhấn hoặc nhập chuỗi lá bài ở phía dưới để nạp dữ liệu sau mỗi ván."
        }
    st.session_state.last_results = calculate_baccarat_v20_ultimate(
        [], [], st.session_state.shoe_history, shoe_decks=decks,
        manual_cards_used=manual_cards,
        manual_games_played=p_wins_sidebar + b_wins_sidebar + tie_wins_sidebar,
        p_wins=p_wins_sidebar, b_wins=b_wins_sidebar, tie_wins=tie_wins_sidebar
    )

# =========================================================================
# HIỂN THỊ Ô BÁO TÌNH TRẠNG HỆ THỐNG (SYSTEM HEALTH HUD)
# =========================================================================
status_info = st.session_state.system_status
if status_info["level"] in ["NOMINAL", "NOMINAL_MANUAL"]:
    st.markdown(f'<div class="sys-monitor-box sys-good"><b>🟢 TRẠNG THÁI HỆ THỐNG: OPERATIONAL</b><br><small>{status_info["msg"]}</small><br><span style="font-size:12px; opacity:0.9;">{status_info["action"]}</span></div>', unsafe_allow_html=True)
elif status_info["level"] == "WARNING":
    st.markdown(f'<div class="sys-monitor-box sys-warn"><b>🟡 TRẠNG THÁI HỆ THỐNG: MISALIGNED (SAI LỆCH XPATH)</b><br><small>{status_info["msg"]}</small><br><hr style="margin:6px 0; border-color:rgba(241,196,15,0.3);">{status_info["action"]}</div>', unsafe_allow_html=True)
elif status_info["level"] == "CRITICAL":
    st.markdown(f'<div class="sys-monitor-box sys-critical"><b>🔴 TRẠNG THÁI HỆ THỐNG: SCRAPING BLOCKED (BỊ CHẶN)</b><br><small>{status_info["msg"]}</small><br><hr style="margin:6px 0; border-color:rgba(231,76,60,0.3);">{status_info["action"]}</div>', unsafe_allow_html=True)

# =========================================================================
# HIỂN THỊ KẾT QUẢ DỰ ĐOÁN
# =========================================================================
if st.session_state.last_results:
    res, _, p_pair, mode, cards_left = st.session_state.last_results
    
    p_box_css = "hud-box neon-player-advantage" if res['Player'] > res['Banker'] else "hud-box"
    b_box_css = "hud-box neon-banker-advantage" if res['Banker'] > res['Player'] else "hud-box"
    
    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 XÁC SUẤT PLAYER</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 XÁC SUẤT BANKER</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-box"><div class="hud-title">🟢 XÁC SUẤT TIE (HÒA)</div><div class="hud-value" style="color: #2ecc71;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
        
    with right_col:
        st.markdown("#### 💎 Tỷ Lệ Cược Cặp")
        st.metric("🔵 PLAYER/BANKER PAIR", f"{p_pair}%")
        
        if st.session_state.outcome_history:
            trend_letters = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.outcome_history]
            pattern_msg, pattern_color = detect_baccarat_pattern(st.session_state.outcome_history)
            st.markdown(f'<div class="trend-hud"><div class="trend-string">{" ".join(trend_letters)}</div><div style="color: {pattern_color}; font-size:12px; font-weight:bold; margin-top:5px;">{pattern_msg}</div></div>', unsafe_allow_html=True)
            
        st.caption(f"**Chế độ core:** {mode} | **Quân bài còn lại:** {int(cards_left)}")

# BÀN ĐIỀU KHIỂN CHẠY TAY BẰNG NÚT BẤM / NHẬP LÁ BÀI
if not auto_scrape_enabled:
    st.markdown("---")
    st.subheader("🎯 BÀN ĐIỀU KHIỂN CHẠY BẰNG TAY (MANUAL MODE)")
    
    st.markdown("##### Cách 1: Ghi nhận nhanh kết quả ván vừa rồi (Vẽ Mạch Bài)")
    btn_p, btn_b, btn_t = st.columns(3)
    
    with btn_p:
        if st.button("🔵 PLAYER THẮNG", use_container_width=True):
            st.session_state.outcome_history.append("Player")
            st.rerun()
    with btn_b:
        if st.button("🔴 BANKER THẮNG", use_container_width=True):
            st.session_state.outcome_history.append("Banker")
            st.rerun()
    with btn_t:
        if st.button("🟢 TIE THẮNG", use_container_width=True):
            st.session_state.outcome_history.append("Tie")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### Cách 2: Nhập chi tiết các lá bài lật (Đếm bài chính xác)")
    col_p, col_b = st.columns(2)
    with col_p: p_input = st.text_input("PLAYER (Ví dụ: 9,A hoặc K,2,7):", value="", key="m_p_c")
    with col_b: b_input = st.text_input("BANKER (Ví dụ: 10,J hoặc 5,5,A):", value="", key="m_b_c")
    
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

    if st.button("🚀 NẠP BÀI VÀ TÍNH XÁC SUẤT VÁN TIẾP THEO", use_container_width=True, type="primary"):
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        if p_list or b_list:
            st.session_state.shoe_history.extend(p_list + b_list)
            p_real = sum([0 if c >= 10 else c for c in p_list]) % 10
            b_real = sum([0 if c >= 10 else c for c in b_list]) % 10
            if p_real > b_real: st.session_state.outcome_history.append("Player")
            elif b_real > p_real: st.session_state.outcome_history.append("Banker")
            else: st.session_state.outcome_history.append("Tie")
            st.success("Đã nạp dữ liệu thành công!")
            st.rerun()
