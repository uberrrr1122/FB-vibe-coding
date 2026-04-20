import requests
from playwright.sync_api import sync_playwright

TG_TOKEN = "xxxxxxxxxxxxxxxx"
TG_CHAT_ID = "xxxxxxxxxx"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def start_fb_hunter(keywords):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="auth.json")
        page = context.new_page()
        group_id = "581526018702375"

        print(f"📡 正在前往社團：{group_id}...")
        page.goto(f"https://www.facebook.com/groups/{group_id}")
        page.wait_for_timeout(5000)

        # --- 切換排序為「新貼文」---
        try:
            print("⚙️ 正在尋找排序選單...")
            sort_btn = page.locator(
                'div[role="button"]:has-text("最相關"), '
                'div[role="button"]:has-text("最新動態"), '
                'div[role="button"]:has-text("新貼文")'
            ).first

            if sort_btn.is_visible():
                sort_btn.click()
                print("🔽 已點開選單，正在尋找【新貼文】選項...")
                page.wait_for_timeout(2000)

                new_post_option = page.locator(
                    '//span[contains(text(), "新貼文")]/ancestor::div[@role="menuitem"]'
                ).first

                if new_post_option.is_visible():
                    new_post_option.click()
                    print("✅ 已成功切換至【新貼文】排序！")
                else:
                    page.get_by_text("新貼文", exact=True).first.click()
                    print("✅ 已成功切換至【新貼文】排序（文字備援）")

                page.wait_for_timeout(4000)
            else:
                print("💡 目前似乎已經是新貼文排序，或找不到選單按鈕。")

        except Exception as e:
            print(f"⚠️ 切換排序失敗。原因: {e}")

        print("⌛ 等待網頁刷新內容...")
        page.wait_for_timeout(5000)

        # --- 持續滾動，累積收集貼文 ---
        print("🖱️ 開始滾動，目標收集15則貼文...")
        collected = {}
        max_attempts = 40

        for attempt in range(max_attempts):
            page.mouse.wheel(0, 600)
            page.wait_for_timeout(2500)

            current = page.evaluate('''() => {
                const results = [];
                const feedItems = document.querySelectorAll('[role="feed"] > div');

                for (let i = 1; i < feedItems.length; i++) {
                    const div = feedItems[i];

                    // 擴大連結搜尋範圍，抓所有 groups 相關連結
                    const allLinks = div.querySelectorAll('a[href*="/groups/"]');
                    let url = null;
                    for (const link of allLinks) {
                        const href = link.href;
                        if (
                            href.includes("/posts/") ||
                            href.includes("permalink") ||
                            href.includes("story_fbid") ||
                            href.includes("?fbid=")
                        ) {
                            url = href.split("?")[0];
                            break;
                        }
                    }

                    // 沒連結也收，用 index 當 key
                    const text = div.innerText;
                    if (text && text.length >= 5) {
                        results.push({
                            text: text,
                            url: url || ("no_url_" + i)
                        });
                    }
                }
                return results;
            }''')

            for post in current:
                key = post['url']
                if key not in collected:
                    collected[key] = post

            print(f"  滾動第 {attempt+1} 次，累積收集到 {len(collected)} 則...")

            if len(collected) >= 15:
                print("✅ 已達到15則，停止滾動！")
                break

        posts = list(collected.values())
        print(f"🕵️ 總共收集到 {len(posts)} 則貼文，開始掃描前15則...")

        # --- 掃描關鍵字 ---
        for i, post in enumerate(posts[:15]):
            try:
                content = post['text']
                url = post['url']

                print(f"DEBUG [{i+1}]: {content[:30].replace(chr(10), ' ')}...")

                found_kw = [k for k in keywords if k.lower() in content.lower()]
                is_fresh = any(m in content for m in ["剛剛", "分鐘", "小時", "天"])

                if found_kw and is_fresh:
                    # 沒找到連結就給社團連結
                    if url.startswith("no_url_"):
                        url = f"https://www.facebook.com/groups/{group_id}"

                    msg = (
                        f"🎯 【獵人通報】\n"
                        f"關鍵字：{found_kw}\n\n"
                        f"{content[:150]}...\n\n"
                        f"🔗 貼文連結：{url}"
                    )
                    send_telegram_msg(msg)
                    print(f"🔥 命中！關鍵字：{found_kw}，訊息已發送！")

            except Exception as e:
                print(f"⚠️ 第 {i+1} 則處理失敗：{e}")
                continue

        print("\n✅ 掃描任務完成。")
        browser.close()

if __name__ == "__main__":
    search_keywords = ["3DS","PS4"]
    send_telegram_msg("🚀 獵人系統：社團監控啟動！")
    start_fb_hunter(search_keywords)
