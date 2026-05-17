def auto_navigation_and_scrape(url, casino_btn_xpath, baccarat_tab_xpath, table_click_xpath, result_xpath):
    if not SELENIUM_AVAILABLE:
        return "ERROR_LIB", "Thiếu thư viện Selenium."
    
    options = Options()
    # Chạy ẩn danh và thiết lập cấu hình tối giản chống tốn RAM máy
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1440,900")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    # Thiết lập thời gian tối đa để tải trang (Quá 15 giây tự ngắt, không cho treo)
    options.page_load_strategy = 'eager' 

    driver = None
    try:
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Giới hạn cứng thời gian load trang tối đa 15 giây
        driver.set_page_load_timeout(15) 
        
        driver.get(url)
        wait = WebDriverWait(driver, 8) # Chỉ chờ tối đa 8 giây cho mỗi nút bấm
        
        if casino_btn_xpath:
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, casino_btn_xpath)))
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(2)
            
        if len(driver.find_elements(By.TAG_NAME, "iframe")) > 0:
            driver.switch_to.frame(0)

        if baccarat_tab_xpath:
            tab = wait.until(EC.element_to_be_clickable((By.XPATH, baccarat_tab_xpath)))
            driver.execute_script("arguments[0].click();", tab)
            time.sleep(2)

        if table_click_xpath:
            table = wait.until(EC.element_to_be_clickable((By.XPATH, table_click_xpath)))
            driver.execute_script("arguments[0].click();", table)
            time.sleep(3)

        wait.until(EC.presence_of_element_located((By.XPATH, result_xpath)))
        elements = driver.find_elements(By.XPATH, result_xpath)
        
        scraped_outcomes = []
        for elem in elements:
            text = elem.text.strip().upper()
            cl = elem.get_attribute("class").upper()
            if 'PLAYER' in text or text == 'P' or 'BLUE' in cl: scraped_outcomes.append('Player')
            elif 'BANKER' in text or text == 'B' or 'RED' in cl: scraped_outcomes.append('Banker')
            elif 'TIE' in text or text == 'T' or 'HÒA' in text or 'GREEN' in cl: scraped_outcomes.append('Tie')
            
        if not scraped_outcomes:
            return "ERROR_EMPTY", "Không tìm thấy dữ liệu ô tròn kết quả."
            
        return "SUCCESS", scraped_outcomes
    except Exception as e:
        # Nếu có lỗi (Sai XPath, mạng chậm), đóng driver ngay lập tức và báo lỗi ra màn hình chứ không làm sập app
        return "ERROR_NAV", f"Hệ thống ngắt an toàn. Chi tiết: {str(e)}"
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
