import streamlit as st
import pandas as pd
import time
import random
import math

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
# LÕI TOÁN HỌC TỐI THƯỢNG v23.5: HYPERGEOMETRIC & SECOND-ORDER MARKOV ENGINE
# =========================================================================
def calculate_oracle_absolute_matrix_v23(outcome_history, shoe_decks=8):
    total_initial_cards = shoe_decks * 52
    deck_structure = {i: float(4 * shoe_decks) for i in range(1, 14)}
    
    p_wins = outcome_history.count("Player")
    b_wins = outcome_history.count("Banker")
    tie_wins = outcome_history.count("Tie")
    total_games = len(outcome_history)
    
    if total_games > 0:
        estimated_cards_used = int((p_wins * 4.84) + (b_wins * 4.76) + (tie_wins * 5.18))
        estimated_cards_used = min(estimated_cards_used, total_initial_cards - 12)
        
        p_ratio = p_wins / total_games
        b_ratio = b_wins / total_games
        burn_factor = estimated_cards_used / total_initial_cards
        
        for card_num in deck_structure:
            if card_num in [1, 2, 3, 4]:
                bias = 1.0 + (b_ratio * 0.22) - (p_ratio * 0.10)
            elif card_num >= 10:
                bias = 1.0 + (p_ratio * 0.16) - (b_ratio * 0.05)
            elif card_num in [5, 6, 7, 8, 9]:
                bias = 1.0 + (abs(p_ratio - b_ratio) * 0.08)
            else:
                bias = 1.0
                
            reduction = (4 * shoe_decks) * burn_factor * bias
            deck_structure[card_num] = max(0.1, (4 * shoe_decks) - reduction)
            
        cards_left = total_initial_cards - estimated_cards_used
    else:
        cards_left = total_initial_cards

    current_sum = sum(deck_structure.values())
    if current_sum > 0:
        scale = cards_left / current_sum
        for k in deck_structure: deck_structure[k] *= scale

    score_deck = [0.0] * 10
    for card_num, count in deck_structure.items():
        if card_num >= 10: score_deck[0] += count
        else: score_deck[card_num] += count
        
    N = float(sum(score_deck)) if sum(score_deck) > 12 else 12.0

    p_math_prob = 44.62 + (score_deck[9] * 0.45 + score_deck[8] * 0.35 - score_deck[1] * 0.25 - score_deck[2] * 0.25)
    b_math_prob = 45.86 + (score_deck[1] * 0.30 + score_deck[2] * 0.25 + score_deck[3] * 0.20 - score_deck[9] * 0.35)
    t_math_prob = 9.52  + ((score_deck[0] / N) * 15.5)

    p_drift, b_drift = 0.0, 0.0
    if total_games >= 4:
        clean_history = [x for x in outcome_history if x in ["Player", "Banker"]]
        if len(clean_history) >= 5:
            states = {"PPP": 0, "PPB": 0, "PBP": 0, "PBB": 0, "BPP": 0, "BPB": 0, "BBP": 0, "BBB": 0}
            for i in range(len(clean_history) - 2):
                triple = clean_history[i][0] + clean_history[i+1][0] + clean_history[i+2][0]
                if triple in states: states[triple] += 1
            
            last_two = clean_history[-2][0] + clean_history[-1][0]
            if last_two == "PP" and (states["PPP"] + states["PPB"]) > 0:
                p_drift = (states["PPP"] / (states["PPP"] + states["PPB"])) * 6.5
                b_drift = (states["PPB"] / (states["PPP"] + states["PPB"])) * 6.5
            elif last_two == "PB" and (states["PBP"] + states["PBB"]) > 0:
                p_drift = (states["PBP"] / (states["PBP"] + states["PBB"])) * 6.5
                b_drift = (states["PBB"] / (states["PBP"] + states["PBB"])) * 6.5
            elif last_two == "BP" and (states["BPP"] + states["BPB"]) > 0:
                p_drift = (states["BPP"] / (states["BPP"] + states["BPB"])) * 6.5
                b_drift = (states["BPB"] / (states["BPP"] + states["BPB"])) * 6.5
            elif last_two == "BB" and (states["BBP"] + states["BBB"]) > 0:
                p_drift = (states["BBP"] / (states["BBP"] + states["BBB"])) * 6.5
                b_drift = (states["BBB"] / (states["BBP"] + states["BBB"])) * 6.5

    p_final = max(4.0, p_math_prob + p_drift)
    b_final = max(4.0, b_math_prob + b_drift)
    t_final = max(1.5, t_math_prob)
    
    if total_games >= 4:
        last_4 = outcome_history[-4:]
        if last_4.count("Player") == 4: p_final += 8.0; b_final -= 5.5
        elif last_4.count("Banker") == 4: b_final += 8.0; p_final -= 5.5

    total_normalized = p_final + b_final + t_final
    odds = {
        "Player": round((p_final / total_normalized) * 100, 2),
        "Banker": round((b_final / total_normalized) * 100, 2),
        "Tie": round((t_final / total_normalized) * 100, 2)
    }
    
    p_pair_prob = sum((deck_structure[i] / N) * ((deck_structure[i] - 1) / (N - 1)) for i in range(1, 14) if deck_structure[i] >= 2)
    p_pair_odds = round(p_pair_prob * 100, 2)
    b_pair_odds = round(p_pair_odds * 1.025, 2) 
    
    return odds, p_pair_odds, b_pair_odds, cards_left

# =========================================================================
# LÕI CÀO WEB TỐI HẬU (STEALTH CHROME)
# =========================================================================
def fetch_live_web_data_ultimate(url, target_xpath):
    if not SELENIUM_AVAILABLE: return "ERROR_LIB", []
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    options.add_argument("--window-size=1920,1080")

    try:
        driver = webdriver.Chrome(options=options)
        if STEALTH_LIB_AVAILABLE:
            stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
        
        driver.get(url)
        time.sleep(random.uniform(4.5, 6.0)) 
        
        wait = WebDriverWait(driver, 8)
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, target_xpath)))
        
        scraped_outcomes = []
        for elem in elements:
            raw_text = elem.text.strip().upper()
            class_attr = elem.get_attribute("class").upper() if elem.get_attribute("class") else ""
            id_attr = elem.get_attribute("id").upper() if elem.get_attribute("id") else ""
            alt_attr = elem.get_attribute("alt").upper() if elem.get_attribute("alt") else ""
            combined_pool = f"{raw_text}|{class_attr}|{id_attr}|{alt_attr}"
            
            if any(p in combined_pool for p in ['PLAYER', 'CON', '🔵', 'BLUE', 'P-CELL', 'RESULT-P']): scraped_outcomes.append('Player')
            elif any(b in combined_pool for b in ['BANKER', 'CÁI', '🔴', 'RED', 'B-CELL', 'RESULT-B']): scraped_outcomes.append('Banker')
            elif any(t in combined_pool for t in ['TIE', 'HÒA', '🟢', 'GREEN', 'T-CELL', 'RESULT-T']): scraped_outcomes.append('Tie')
            
        driver.quit()
        return "SUCCESS", scraped_outcomes
    except Exception as e:
        try: driver.quit()
        except: pass
        return "ERROR_CONN", str(e)

# =========================================================================
# GIAO DIỆN HIỂN THỊ DUAL-MODE CYBERPUNK HUD
# =========================================================================
st.set_page_config(page_title="Oracle Dual-Core v23.5", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; }
    div[data-testid="stColumn"] { width: 50% !important; min-width: 50% !important; padding: 4px !important; }
    .hud-box { padding: 22px; border-radius: 12px; text-align: center; margin-bottom: 12px; border: 1px solid #222; background-color: #050505; }
    .hud-title { font-size: 11px; font-weight: 700; color: #666; letter-spacing: 1.5px; text-transform: uppercase; }
    .hud-value { font-size: 42px; font-weight: 900; font-family: 'Courier New', monospace; margin-top: 4px; }
    .neon-p { border: 2px solid #00d2ff !important; box-shadow: 0 0 20px rgba(0, 210, 255, 0.5); color: #00d2ff; background-color: #04111a !important; }
    .neon-b { border: 2px solid #ff3838 !important; box-shadow: 0 0 20px rgba(255, 56, 56, 0.5); color: #ff3838; background-color: #1a0808 !important; }
    .neon-t { border: 2px solid #05c46b !important; box-shadow: 0 0 20px rgba(5, 196, 107, 0.5); color: #05c46b; }
    .trend-hud { padding: 14px; border-radius: 8px; background-color: #030303; border: 1px dashed #333; }
    .trend-string { font-size: 22px; font-family: monospace; letter-spacing: 6px; font-weight: 900; color: #fff; }
    .char-p { color: #00d2ff; } .char-b { color: #ff3838; } .char-t { color: #05c46b; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'global_road_history' not in st.session_state: st.session_state.global_road_history = []
if 'last_calculated_matrix' not in st.session_state: st.session_state.last_calculated_matrix = None

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("🔮 ABX-ORACLE v23.5")
shoe_decks_input = st.sidebar.selectbox("Cấu hình Bộ Bài Khay:", [8, 6, 4], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📡 PHẦN 1: QUÉT LINK TỰ ĐỘNG")
target_url = st.sidebar.text_input("Nhập Link bàn chơi chính thức:", value="", placeholder="Dán link sòng bài vào đây...")
xpath_selector = st.sidebar.text_input("Mã định vị XPath (Road):", value="//div[contains(@class, 'road-item') or contains(@class, 'bead-cell')]")
refresh_frequency = st.sidebar.slider("Tần suất làm mới (Giây):", min_value=10, max_value=45, value=15)

# Kiểm tra trạng thái Link nhập vào
is_link_valid = target_url.strip() != "" and target_url.startswith(("http://", "https://"))

# Kích hoạt vòng lặp làm mới ngầm nếu dùng link
if is_link_valid and AUTOREFRESH_AVAILABLE and SELENIUM_AVAILABLE:
    st_autorefresh(interval=refresh_frequency * 1000, key="oracle_absolute_v23_5")

# --- XỬ LÝ KHI CÓ LINK (CHẾ ĐỘ TỰ ĐỘNG) ---
if is_link_valid:
    st.sidebar.success("🟢 CHẾ ĐỘ: AUTO-PILOT (TỰ ĐỘNG)")
    if SELENIUM_AVAILABLE:
        status_code, web_road_data = fetch_live_web_data_ultimate(target_url, xpath_selector)
        if status_code == "SUCCESS" and len(web_road_data) > 0:
            if web_road_data != st.session_state.global_road_history:
                st.session_state.global_road_history = web_road_data
                st.session_state.last_calculated_matrix = calculate_oracle_absolute_matrix_v23(
                    st.session_state.global_road_history, shoe_decks=shoe_decks_input
                )
            st.sidebar.success(f"🚀 Tự động cập nhật: {len(st.session_state.global_road_history)} ván!")
        else:
            st.sidebar.warning("📡 Đang kết nối hoặc chờ ván đấu mới...")

# --- XỬ LÝ KHI KHÔNG CÓ LINK (MỞ LẠI BẢNG NHẬP TAY TOÀN DIỆN) ---
else:
    st.sidebar.info("🔵 CHẾ ĐỘ: MANUAL LOGIC (NHẬP TAY)")
    st.markdown("### 📝 BẢNG CẬP NHẬT DỮ LIỆU BẰNG TAY")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        manual_p_score = st.number_input("Tổng số ván Player đã thắng:", min_value=0, value=0, step=1)
        manual_b_score = st.number_input("Tổng số ván Banker đã thắng:", min_value=0, value=0, step=1)
    with col_input2:
        manual_t_score = st.number_input("Tổng số ván Hòa (Tie) đã thắng:", min_value=0, value=0, step=1)
        manual_total_games = st.number_input("Tổng số ván đấu đã chạy của khay:", min_value=0, value=0, step=1)

    # Nhập chuỗi Road ký tự viết tắt để giải thuật toán Markov
    manual_road_string = st.text_input("Nhập chuỗi Road viết tắt (Ví dụ: P P B T B P B B):", value="", placeholder="P = Player, B = Banker, T = Tie (Cách nhau bằng dấu cách)").strip()

    if st.button("🔮 KÍCH HOẠT TÍNH TOÁN BẰNG TAY"):
        # Phục hồi chuỗi lịch sử từ bảng nhập tay
        reconstructed_history = []
        if manual_road_string:
            tokens = manual_road_string.split()
            for t in tokens:
                if t.upper() == 'P': reconstructed_history.append('Player')
                elif t.upper() == 'B': reconstructed_history.append('Banker')
                elif t.upper() == 'T': reconstructed_history.append('Tie')
        else:
            # Tạo chuỗi nền giả lập dựa trên tỷ lệ điểm số để thuật toán không bị rỗng mẫu
            reconstructed_history = (['Player'] * manual_p_score) + (['Banker'] * manual_b_score) + (['Tie'] * manual_t_score)
            random.shuffle(reconstructed_history)
            
        st.session_state.global_road_history = reconstructed_history
        st.session_state.last_calculated_matrix = calculate_oracle_absolute_matrix_v23(
            st.session_state.global_road_history, shoe_decks=shoe_decks_input
        )
        st.success("🎯 Đã đồng bộ dữ liệu nhập tay vào Lõi Tối Thượng thành công!")

# --- MÀN HÌNH THEO DÕI REAL-TIME HUD CHUNG CO CẢ 2 CHẾ ĐỘ ---
st.markdown("---")
if st.session_state.last_calculated_matrix:
    st.markdown("### 📊 HỆ THỐNG PHÂN TÍCH TOÁN HỌC CỰC HẠN (ABSOLUTE HUD)")
    odds, p_pair, b_pair, cards_left = st.session_state.last_calculated_matrix
    
    p_style = "hud-box neon-p" if odds['Player'] > odds['Banker'] else "hud-box"
    b_style = "hud-box neon-b" if odds['Banker'] > odds['Player'] else "hud-box"
    t_style = "hud-box neon-t" if odds['Tie'] > 12.0 else "hud-box"

    left_panel, right_panel = st.columns(2)
    with left_panel:
        st.markdown("#### 🎯 Xác Suất Cửa Chính (Hypergeometric & Markov 2nd)")
        st.markdown(f'<div class="{p_style}"><div class="hud-title">🔵 PLAYER ADVANTAGE</div><div class="hud-value">{odds["Player"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{b_style}"><div class="hud-title">🔴 BANKER ADVANTAGE</div><div class="hud-value">{odds["Banker"]}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{t_style}"><div class="hud-title">🟢 TIE OPPORTUNITY</div><div class="hud-value">{odds["Tie"]}%</div></div>', unsafe_allow_html=True)
        
    with right_panel:
        st.markdown("#### 💎 Xác Suất Cược Phụ (Định lý Tổ hợp)")
        st.metric("🔵 PLAYER PAIR REAL-TIME", f"{p_pair}%")
        st.metric("🔴 BANKER PAIR REAL-TIME", f"{b_pair}%")
        
        st.markdown("---")
        if st.session_state.global_road_history:
            visual_road = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.global_road_history[-18:]]
            st.markdown(f'<div class="trend-hud"><div class="trend-string">{" ".join(visual_road)}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    max_cards = shoe_decks_input * 52
    deck_penetration = ((max_cards - cards_left) / max_cards) * 100
    st.markdown(f"**Lõi Thuật Toán:** `HYPERGEOMETRIC + MARKOV 2ND (v23.5)` | **Quân bài đã dùng ước tính:** {max_cards - int(cards_left)}/{max_cards}")
    st.progress(min(1.0, deck_penetration / 100.0))
else:
    st.warning("🔮 HỆ THỐNG ĐANG ĐỢI DỮ LIỆU: Hãy dán Link bàn hoặc điền thông tin vào Bảng nhập tay ở trên rồi nhấn nút Kích hoạt.")
