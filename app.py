# --- ĐIỀU KHIỂN NHẬP TAY (ĐÃ SỬA LỖI STREAMLIT WIDGET MUTATION) ---
st.subheader("🃏 Nhập Dữ Liệu Dự Đoán Ván Tiếp Theo")

# Sử dụng form với thuộc tính tự động xóa dữ liệu sau khi submit
with st.form(key="baccarat_input_form", clear_on_submit=True):
    col_p, col_b = st.columns(2)
    with col_p: 
        p_input = st.text_input("PLAYER (Lá bài vừa ra):", placeholder="Ví dụ: 5,K,2")
    with col_b: 
        b_input = st.text_input("BANKER (Lá bài vừa ra):", placeholder="Ví dụ: J,7")
        
    submit_button = st.form_submit_button("🚀 GHI NHẬN VÀ TÍNH TOÁN VÁN TIẾP THEO", use_container_width=True, type="primary")

if submit_button:
    current_game_signature = f"P:{p_input.strip().upper()}|B:{b_input.strip().upper()}"
    
    if not p_input.strip() and not b_input.strip():
        st.warning("⚠️ Vui lòng điền thông tin quân bài để kích hoạt phép tính.")
    elif current_game_signature == st.session_state.last_played_cards and current_game_signature != "P:|B:":
        st.error("⛔ Trùng lặp hoàn toàn với dữ liệu ván vừa nạp!")
    else:
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        
        if p_list or b_list:
            core_output = calculate_baccarat_v18_ultimate(
                p_list, b_list, st.session_state.shoe_history, shoe_decks=decks,
                manual_cards_used=manual_cards, manual_games_played=manual_games,
                p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
            )
            
            if isinstance(core_output, str):
                st.session_state.last_results = core_output  # Lưu trực tiếp String lỗi
            else:
                st.session_state.last_results = core_output
                st.session_state.last_played_cards = current_game_signature
                
                # Tự động tính điểm từ bài vừa nhập tay để đẩy vào đồ thị Xu Hướng (P - B - T)
                p_score_eval = sum([0 if c >= 10 else c for c in p_list]) % 10
                b_score_eval = sum([0 if c >= 10 else c for c in b_list]) % 10
                if p_score_eval > b_score_eval:
                    st.session_state.outcome_history.append("Player")
                elif b_score_eval > p_score_eval:
                    st.session_state.outcome_history.append("Banker")
                else:
                    st.session_state.outcome_history.append("Tie")

                st.session_state.shoe_history.extend(p_list + b_list)
                    
            st.rerun()

st.markdown("---")

# --- PANEL OUTPUT CONTROL (HIỂN THỊ KẾT QUẢ ĐÃ ĐƯỢC ĐỒNG BỘ LUỒNG) ---
if is_strict_lock:
    st.error(f"### 🛑 HỆ THỐNG KHÓA: Số ván tổng ({manual_games}) lệch với tổng số ván thắng lẻ ({calculated_total_wins}). Vui lòng điều chỉnh lại thông số ở cột bên trái.")
else:
    if st.session_state.last_results:
        results_data = st.session_state.last_results
        
        if isinstance(results_data, str):
            if results_data.startswith("❌"): 
                st.error(results_data)
            else: 
                st.warning(results_data)
        else:
            res, remaining_deck, p_pair, b_pair, mode, cards_left, is_shoe_logical, invalid_cards = results_data
            
            p_box_css = "hud-box"
            b_box_css = "hud-box"
            tie_box_css = "hud-box"
            if res['Player'] > res['Banker']: p_box_css = "hud-box neon-player-advantage"
            elif res['Banker'] > res['Player']: b_box_css = "hud-box neon-banker-advantage"
            if res['Tie'] > 12.5: tie_box_css = "hud-box neon-tie-alert"
                
            left_result_col, right_pair_col = st.columns(2)
            with left_result_col:
                st.markdown("#### 📊 Dự Đoán Xác Suất Cửa Chính")
                st.markdown(f'<div class="{p_box_css}"><div class="hud-title">🔵 PLAYER PROBABILITY</div><div class="hud-value">{res["Player"]}%</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="{b_box_css}"><div class="hud-title">🔴 BANKER PROBABILITY</div><div class="hud-value">{res["Banker"]}%</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="{tie_box_css}"><div class="hud-title">🟢 TIE WIN PROBABILITY</div><div class="hud-value" style="color: #2ecc71;">{res["Tie"]}%</div></div>', unsafe_allow_html=True)
                
            with right_pair_col:
                st.markdown("#### 💎 Tỷ Lệ Cược Phụ Xuất Hiện")
                st.metric("🔵 CON ĐÔI (PLAYER PAIR)", f"{p_pair}%")
                st.metric("🔴 CÁI ĐÔI (BANKER PAIR)", f"{b_pair}%")
                
                if is_shoe_logical: 
                    st.markdown('<div class="validation-hud logic-pass">✔ LOGIC KHAY HỢP LỆ</div>', unsafe_allow_html=True)
                else: 
                    st.markdown(f'<div class="validation-hud logic-fail">⚠️ LỖI LOGIC: ÂM KHAY BÀI ({", ".join(invalid_cards)})</div>', unsafe_allow_html=True)

                if st.session_state.outcome_history:
                    trend_letters = [f'<span class="char-p">P</span>' if x == "Player" else (f'<span class="char-b">B</span>' if x == "Banker" else '<span class="char-t">T</span>') for x in st.session_state.outcome_history]
                    pattern_msg, pattern_color = detect_baccarat_pattern(st.session_state.outcome_history)
                    st.markdown(f'<div class="trend-hud"><div class="trend-title">📈 XU HƯỚNG SÀN</div><div class="trend-string">{" ".join(trend_letters)}</div><div class="trend-alert" style="border-left-color: {pattern_color}; color: {pattern_color};">{pattern_msg}</div></div>', unsafe_allow_html=True)

            st.markdown("---")
            total_shoe_cards = decks * 52
            penetration_rate = min(100.0, (((total_shoe_cards - max(0, cards_left))) / total_shoe_cards) * 100)
            st.markdown(f"**Chế độ quét:** `{mode}` | **Độ chín khay bài:** {round(penetration_rate, 1)}%")
            st.progress(penetration_rate / 100.0)
    else:
        st.info("🔮 ENGINE READY. Vui lòng nạp quân bài ván trực tiếp để lấy dữ liệu phân tích.")
