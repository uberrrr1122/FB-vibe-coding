from playwright.sync_api import sync_playwright

def save_fb_auth():
    with sync_playwright() as p:
        # 改用 firefox 試試看，這通常能繞過 Chrome 特有的自動化檢測
        browser = p.firefox.launch(headless=False) 
        
        # 手動注入一些「真人」特徵
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            viewport={'width': 1280, 'height': 800}
        )
        
        page = context.new_page()
        
        # 額外小撇步：隱藏 webdriver 標記
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("正在前往 Facebook...")
        page.goto("https://www.facebook.com", wait_until="networkidle")
        
        print("---")
        print("請在瀏覽器視窗中完成 FB 登入...")
        print("如果出現驗證碼，請手動點選完成。")
        input("登入完成並看到首頁後，請回到這裡按 Enter 鍵存檔...")
        
        # 存檔
        context.storage_state(path="auth.json")
        print("✅ 登入狀態已成功儲存至 auth.json")
        browser.close()

if __name__ == "__main__":
    save_fb_auth()