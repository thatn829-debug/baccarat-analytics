def auto_navigation_and_scrape(url, casino_btn_xpath, baccarat_tab_xpath, table_click_xpath, result_xpath):
    if not SELENIUM_AVAILABLE:
        return "ERROR_LIB", "Thiếu thư viện Selenium."
    
    options = Options()
    # CHÚ Ý: Đôi khi chế độ Headless (chạy ngầm) sẽ bị nhà cái chặn. 
    # Nếu vẫn lỗi, hãy thử xóa dấu thăng (#) ở dòng dưới để tắt headless và xem trình duyệt chạy thực tế.
    # options.add_argument("--headless") 
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1440,900")
    
    # Giả lập vân tay trình duyệt của người dùng thật
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        
        # Ẩn cờ Webdriver để qua mặt hệ thống quét Bot
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })
        
        driver.get(url)
        wait = WebDriverWait(driver, 20) # Tăng thời gian chờ load trang lên 20 giây
        
        # BƯỚC 1: Click danh mục Casino
        if casino_btn_xpath:
            btn_casino = wait.until(EC.element_to_be_clickable((By.XPATH, casino_btn_xpath)))
            driver.execute_script("arguments[0].click();", btn_casino) # Dùng JS click để tránh bị chặn đè phần tử
            time.sleep(3)
            
        # BƯỚC 2: Kiểm tra và chuyển đổi vùng kiểm soát (Iframe Handling)
        # Các sảnh Evolution, AG, Sexy... thường nằm trong Iframe riêng
        ifframes = driver.find_elements(By.TAG_NAME, "iframe")
        if len(ifframes) > 0:
            # Thử nhảy vào iframe chứa sảnh game
            driver.switch_to.frame(0)

        # BƯỚC 3: Chọn sảnh Baccarat
        if baccarat_tab_xpath:
            tab_bac = wait.until(EC.element_to_be_clickable((By.XPATH, baccarat_tab_xpath)))
            driver.execute_script("arguments[0].click();", tab_bac)
            time.sleep(2)

        # BƯỚC 4: Vào bàn
        if table_click_xpath:
            target_table = wait.until(EC.element_to_be_clickable((By.XPATH, table_click_xpath)))
            driver.execute_script("arguments[0].click();", target_table)
            time.sleep(5) # Chờ bàn load hẳn đồ họa hột xúc xắc / quân bài

        # BƯỚC 5: Trích xuất chuỗi kết quả
        wait.until(EC.presence_of_element_located((By.XPATH, result_xpath)))
        elements = driver.find_elements(By.XPATH, result_xpath)
        
        scraped_outcomes = []
        for elem in elements:
            text = elem.text.strip().upper()
            class_attr = elem.get_attribute("class").upper()
            
            # Kiểm tra cả ký tự text hiển thị lẫn thuộc tính class màu sắc
            if 'PLAYER' in text or text == 'P' or 'PLAYER' in class_attr or 'BLUE' in class_attr: 
                scraped_outcomes.append('Player')
            elif 'BANKER' in text or text == 'B' or 'BANKER' in class_attr or 'RED' in class_attr: 
                scraped_outcomes.append('Banker')
            elif 'TIE' in text or text == 'T' or 'HÒA' in text or 'HOA' in text or 'TIE' in class_attr or 'GREEN' in class_attr: 
                scraped_outcomes.append('Tie')
            
        if not scraped_outcomes:
            return "ERROR_EMPTY", "Đã kết nối giao diện thành công nhưng cấu trúc XPath kết quả (Roadmap) của trang này đã thay đổi."
            
        return "SUCCESS", scraped_outcomes
    except Exception as e:
        return "ERROR_NAV", f"Dừng tại tiến trình tự động. Lỗi chi tiết: {str(e)}"
    finally:
        if driver:
            driver.quit()
