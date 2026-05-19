# baccarat_engine.py
import streamlit as st
import cv2
import numpy as np

class VisionScannerEngine:
    @staticmethod
    def decode_and_parse_roadmap(image_bytes):
        if image_bytes is None:
            return []
        try:
            file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            img_resized = cv2.resize(img, (1080, 2400))
            
            # Quét ma trận hạt gỗ theo tọa độ từ ảnh sòng bài của bạn
            rows, cols = 6, 4
            start_x, start_y = 15, 1695
            cell_w, cell_h = 63, 64
            detected_roadmap = []
            
            for c in range(cols):
                for r in range(rows):
                    center_x = start_x + (c * cell_w) + (cell_w // 2)
                    center_y = start_y + (r * cell_h) + (cell_h // 2)
                    
                    if center_y < img_resized.shape[0] and center_x < img_resized.shape[1]:
                        color = img_resized[center_y, center_x]
                        b, g, r_val = int(color[0]), int(color[1]), int(color[2])
                        
                        if b > 140 and b > r_val:
                            detected_roadmap.append("Player")
                        elif r_val > 140 and r_val > b:
                            detected_roadmap.append("Banker")
                        elif g > 130 and g > b:
                            detected_roadmap.append("Tie")
            return detected_roadmap
        except Exception:
            return []

    @staticmethod
    def render_camera_hud():
        st.markdown('<p class="section-title">👁️ DIGITAL CAMERA VISION</p>', unsafe_allow_html=True)
        img_file = st.file_uploader("Tải lên ảnh chụp màn hình", type=["png", "jpg", "jpeg"])
        return img_file

def calculate_v68_1_fusion(all_rounds_log, shoe_decks, manual_p, manual_b, manual_t):
    total_p = manual_p + sum(1 for r in all_rounds_log if r['outcome'] == "Player")
    total_b = manual_b + sum(1 for r in all_rounds_log if r['outcome'] == "Banker")
    total_t = manual_t + sum(1 for r in all_rounds_log if r['outcome'] == "Tie")
    
    # Tính toán xác suất cơ bản dựa trên số lượng ván để tránh lỗi luồng toán học
    total_all = total_p + total_b + total_t
    if total_all == 0:
        return 44.6, 45.8, 9.6, shoe_decks * 52, 0, 0, 0, "HỆ THỐNG TRỐNG", None, 0
        
    p_pct = (total_p / total_all) * 100 if total_all > 0 else 44.6
    b_pct = (total_b / total_all) * 100 if total_all > 0 else 45.8
    t_pct = (total_t / total_all) * 100 if total_all > 0 else 9.6
    
    cards_left = max(0, (shoe_decks * 52) - (total_all * 5))
    return p_pct, b_pct, t_pct, cards_left, total_p, total_b, total_t, "CẦU BIẾN ĐỘNG", None, 0

def get_ultimate_directive(p_val, b_val):
    if p_val == 44.6 and b_val == 45.8:
        return {"status": "🛰️ SYSTEM READY", "msg": "Hãy nhập quân bài hoặc tải ảnh để tính toán.", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.08)", "size": "0%"}
    if p_val > b_val:
        return {"status": "🔵 VÀO LỆNH: PLAYER", "msg": "Lợi thế đang nghiêng về cửa Player.", "color": "#00afb9", "bg": "rgba(0,175,185,0.2)", "size": "2.5%"}
    return {"status": "🔴 VÀO LỆNH: BANKER", "msg": "Lợi thế đang nghiêng về cửa Banker.", "color": "#ff4757", "bg": "rgba(255,71,87,0.2)", "size": "2.5%"}

def parse_baccarat_input(raw_str):
    if not raw_str: return []
    tokens = raw_str.upper().strip().split()
    res = []
    mapping = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    for t in tokens:
        if t in mapping: res.append(mapping[t])
        elif t.isdigit(): res.append(int(t))
    return res

class BaccaratInterfaceSystem:
    @staticmethod
    def inject_mobile_css():
        st.markdown(
            """
            <style>
            .stApp { background: #030611 !important; color: #f8fafc !important; }
            .block-container { padding: 0.8rem 0.6rem !important; }
            div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; width: 100% !important; gap: 6px !important; }
            div[data-testid="stHorizontalBlock"] > div { flex: 1 1 0% !important; min-width: 0px !important; }
            .section-title { font-size: 11px; font-weight: 800; color: #94a3b8; }
            .header-hud-bar { background: #1e293b; border-radius: 8px; padding: 8px; text-align: center; font-size: 11px; }
            .action-panel { border-radius: 10px; padding: 14px; text-align: center; margin: 10px 0; }
            .action-status { font-size: 16px; font-weight: 900; }
            .action-msg { font-size: 12px; }
            .mobile-metric-box { background: #0b132b; border: 1px solid #1c2541; border-radius: 8px; padding: 8px; text-align: center; }
            .metric-tag { font-size: 9px; color: #64748b; }
            .metric-num { font-size: 16px; font-weight: 900; }
            </style>
            """, unsafe_allow_html=True
        )
    @staticmethod
    def render_sidebar():
        decks = st.sidebar.selectbox("Số bộ bài:", [8, 6, 4], index=0)
        hist_p = st.sidebar.number_input("🔵 PLAYER:", min_value=0, value=0)
        hist_b = st.sidebar.number_input("🔴 BANKER:", min_value=0, value=0)
        hist_t = st.sidebar.number_input("🟢 TIE:", min_value=0, value=0)
        return decks, hist_p, hist_b, hist_t
