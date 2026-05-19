# app.py
import streamlit as st
import cv2
import numpy as np

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN MOBILE
# ==========================================
st.set_page_config(layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: #030611 !important; color: #f8fafc !important; }
    .block-container { padding: 0.8rem 0.6rem !important; }
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; width: 100% !important; gap: 6px !important; }
    div[data-testid="stHorizontalBlock"] > div { flex: 1 1 0% !important; min-width: 0px !important; }
    .section-title { font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; }
    .header-hud-bar { background: #1e293b; border-radius: 8px; padding: 8px; text-align: center; font-size: 11px; }
    .action-panel { border-radius: 10px; padding: 14px; text-align: center; margin: 10px 0; }
    .action-status { font-size: 16px; font-weight: 900; }
    .mobile-metric-box { background: #0b132b; border: 1px solid #1c2541; border-radius: 8px; padding: 8px; text-align: center; }
    .metric-tag { font-size: 9px; color: #64748b; }
    .metric-num { font-size: 16px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True
)

# Cấu hình thanh Sidebar độc lập
decks = st.sidebar.selectbox("Số bộ bài:", [8, 6, 4], index=0)
hist_p = st.sidebar.number_input("🔵 PLAYER WINS:", min_value=0, value=0)
hist_b = st.sidebar.number_input("🔴 BANKER WINS:", min_value=0, value=0)
hist_t = st.sidebar.number_input("🟢 TIE WINS:", min_value=0, value=0)

if 'round_detailed_log' not in st.session_state:
    st.session_state.round_detailed_log = []

st.markdown("### ⚡ ORACLE TREND TRACKING v68.1")

# ==========================================
# 2. XỬ LÝ QUÉT ẢNH QUANG HỌC (MÃ MÀU TRỰC TIẾP)
# ==========================================
st.markdown('<p class="section-title">👁️ DIGITAL CAMERA VISION</p>', unsafe_allow_html=True)
img_file = st.file_uploader("Tải lên ảnh chụp màn hình", type=["png", "jpg", "jpeg"])

if img_file is not None:
    if st.button("🔮 PHÂN TÍCH ẢNH VÀ ĐỒNG BỘ"):
        try:
            file_bytes = np.asarray(bytearray(img_file.getvalue()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            img_resized = cv2.resize(img, (1080, 2400))
            
            # Tọa độ quét ma trận hạt gỗ sòng của bạn (6 hàng x 4 cột hiển thị)
            rows, cols = 6, 4
            start_x, start_y = 15, 1695
            cell_w, cell_h = 63, 64
            
            for c in range(cols):
                for r in range(rows):
                    cx = start_x + (c * cell_w) + (cell_w // 2)
                    cy = start_y + (r * cell_h) + (cell_h // 2)
                    
                    if cy < img_resized.shape[0] and cx < img_resized.shape[1]:
                        color = img_resized[cy, cx]
                        b, g, r_val = int(color[0]), int(color[1]), int(color[2])
                        
                        if b > 140 and b > r_val:
                            st.session_state.round_detailed_log.append({'outcome': "Player"})
                        elif r_val > 140 and r_val > b:
                            st.session_state.round_detailed_log.append({'outcome': "Banker"})
                        elif g > 130 and g > b:
                            st.session_state.round_detailed_log.append({'outcome': "Tie"})
            st.success("Đã quét ma trận hạt gỗ thành công!")
        except Exception:
            st.error("Lỗi định dạng ảnh chụp màn hình.")

st.markdown("---")

# ==========================================
# 3. ĐỘNG CƠ TÍNH TOÁN XÁC SUẤT KHẤU TRỪ
# ==========================================
total_p = hist_p + sum(1 for r in st.session_state.round_detailed_log if r.get('outcome') == "Player")
total_b = hist_b + sum(1 for r in st.session_state.round_detailed_log if r.get('outcome') == "Banker")
total_t = hist_t + sum(1 for r in st.session_state.round_detailed_log if r.get('outcome') == "Tie")
total_all = total_p + total_b + total_t

if total_all == 0:
    final_p, final_b, final_t = 44.6, 45.8, 9.6
    cmd_status, cmd_msg, cmd_color, cmd_bg = "🛰️ SYSTEM READY", "Hãy nhập dữ liệu để ma trận khởi chạy.", "#94a3b8", "rgba(148, 163, 184, 0.08)"
else:
    final_p = (total_p / total_all) * 100
    final_b = (total_b / total_all) * 100
    final_t = (total_t / total_all) * 100
    if final_p > final_b:
        cmd_status, cmd_msg, cmd_color, cmd_bg = "🔵 LỆNH: PLAYER", "Lợi thế nghiêng về toán học cửa Player.", "#00afb9", "rgba(0,175,185,0.2)"
    else:
        cmd_status, cmd_msg, cmd_color, cmd_bg = "🔴 LỆNH: BANKER", "Lợi thế nghiêng về toán học cửa Banker.", "#ff4757", "rgba(255,71,87,0.2)"

cards_left = max(0, (decks * 52) - (total_all * 5))
st.markdown(f'<div class="header-hud-bar">🎰 VÁN ĐÃ QUÉT: <b>{total_all}</b> | 🎴 CÒN LẠI: <b>{cards_left}</b> / {decks * 52}</div>', unsafe_allow_html=True)

# ==========================================
# 4. NHẬP LIỆU THỦ CÔNG
# ==========================================
st.markdown('<p class="section-title">🎴 NHẬP QUÂN BÀI THỦ CÔNG</p>', unsafe_allow_html=True)
with st.form(key="manual_form", clear_on_submit=True):
    cols = st.columns(2)
    p_str = cols[0].text_input("🔵 PLAYER CARD:")
    b_str = cols[1].text_input("🔴 BANKER CARD:")
    calc_triggered = st.form_submit_button("🔥 KHỞI CHẠY MA TRẬN")

if calc_triggered and (p_str.strip() or b_str.strip()):
    # Xử lý chuỗi nhập ký tự bài nhanh
    p_tokens = p_str.upper().strip().split()
    b_tokens = b_str.upper().strip().split()
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    
    p_score = sum([mapping.get(t, int(t) if t.isdigit() else 0) for t in p_tokens]) % 10
    b_score = sum([mapping.get(t, int(t) if t.isdigit() else 0) for t in b_tokens]) % 10
    
    outcome = "Tie" if p_score == b_score else ("Player" if p_score > b_score else "Banker")
    st.session_state.round_detailed_log.append({'outcome': outcome})

st.markdown("---")

# ==========================================
# 5. KHỐI HIỂN THỊ KẾT QUẢ ĐẦU RA
# ==========================================
st.markdown(f'<div class="action-panel" style="background-color: {cmd_bg}; border: 1px solid {cmd_color}; color: {cmd_color};"><div class="action-status">{cmd_status}</div><div class="action-msg" style="color: #f1f5f9;">{cmd_msg}</div></div>', unsafe_allow_html=True)

prob_grid = st.columns(3)
prob_grid[0].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔵 PLAYER</span><br><span class="metric-num" style="color:#00afb9;">{final_p:.1f}%</span></div>', unsafe_allow_html=True)
prob_grid[1].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🔴 BANKER</span><br><span class="metric-num" style="color:#ff4757;">{final_b:.1f}%</span></div>', unsafe_allow_html=True)
prob_grid[2].markdown(f'<div class="mobile-metric-box"><span class="metric-tag">🟢 TIE</span><br><span class="metric-num" style="color:#2ecc71;">{final_t:.1f}%</span></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
util_cols = st.columns(2)
if util_cols[0].button("⏪ HOÀN TÁC") and st.session_state.round_detailed_log:
    st.session_state.round_detailed_log.pop()
if util_cols[1].button("🔄 LÀM TRỐNG"):
    st.session_state.round_detailed_log = []
