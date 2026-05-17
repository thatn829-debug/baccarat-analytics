import streamlit as st

# =========================================================================
# CONFIGURATION & MOBILE UI GRAPHICS
# =========================================================================
st.set_page_config(page_title="Oracle Mobile v18.2", page_icon="🔮", layout="centered")

# Ép giao diện hiển thị gọn gàng, nút bấm to chống ấn nhầm trên điện thoại
st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; width: 100% !important; }
    div[data-testid="stColumn"] { flex: 1 1 50% !important; padding: 2px !important; }
    .hud-box { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px; border: 1px solid #444; background-color: #1e1e1e; }
    .hud-title { font-size: 12px; font-weight: 700; color: #aaa; letter-spacing: 1px; }
    .hud-value { font-size: 32px; font-weight: 800; font-family: monospace; margin-top: 4px; }
    .win-p { background-color: #0c2461 !important; border: 2px solid #1e3799 !important; color: #54a0ff !important; }
    .win-b { background-color: #b33939 !important; border: 2px solid #ff5252 !important; color: #ff7675 !important; }
    .trend-bar { padding: 10px; border-radius: 8px; background-color: #111; border: 1px dashed #555; margin-top: 10px; overflow-x: auto; }
    .trend-str { font-size: 18px; font-family: monospace; letter-spacing: 6px; font-weight: 800; white-space: nowrap; }
    .c-p { color: #54a0ff; } .c-b { color: #ff7675; } .c-t { color: #2ecc71; }
    </style>
    """, 
    unsafe_allow_html=True
)

# Khởi tạo bộ nhớ đệm an toàn, không gây thắt nút cổ chai (Bottleneck)
if 'shoe_history' not in st.session_state: st.session_state.shoe_history = []
if 'outcome_history' not in st.session_state: st.session_state.outcome_history = []
if 'last_results' not in st.session_state: st.session_
