if st.button("🚀 GHI NHẬN VÀ TRÍCH XUẤT XÁC SUẤT", use_container_width=True, type="primary"):
    current_game_signature = f"P:{p_input.strip().upper()}|B:{b_input.strip().upper()}"
    
    if not p_input.strip() and not b_input.strip():
        st.warning("⚠️ Hệ thống trống: Vui lòng điền thông tin quân bài để kích hoạt thuật toán.")
    elif current_game_signature == st.session_state.last_played_cards:
        st.error("⛔ Trùng lặp dữ liệu: Kết quả ván này đã được xử lý vào bộ nhớ đệm trước đó!")
    else:
        p_list = clean_and_parse_input(p_input)
        b_list = clean_and_parse_input(b_input)
        
        if p_list or b_list:
            core_output = calculate_baccarat_v18_optimized(
                p_list, b_list, st.session_state.shoe_history, shoe_decks=decks,
                manual_cards_used=manual_cards, manual_games_played=manual_games,
                p_wins=p_wins_input, b_wins=b_wins_input, tie_wins=tie_wins_input
            )
            
            if isinstance(core_output, str):
                st.session_state.last_results = core_output
            else:
                st.session_state.last_results = core_output
                st.session_state.last_played_cards = current_game_signature
                
                # Tính điểm ván đấu thực tế để phân tích xu hướng
                p_score_eval = sum([0 if c >= 10 else c for c in p_list]) % 10
                b_score_eval = sum([0 if c >= 10 else c for c in b_list]) % 10
                
                if p_score_eval > b_score_eval:
                    st.session_state.outcome_history.append("Player")
                elif b_score_eval > p_score_eval:
                    st.session_state.outcome_history.append("Banker")
                else:
                    st.session_state.outcome_history.append("Tie")

                st.session_state.shoe_history.extend(p_list + b_list)
            
            # Giải pháp ép tải lại giao diện an toàn không sợ lỗi crash phiên bản
            try:
                st.rerun()
            except AttributeError:
                try:
                    st.experimental_rerun()
                except:
                    st.success("🔄 Đã ghi nhận dữ liệu! Hãy cuộn lên để xem kết quả cập nhật.")
