# FB-vibe-coding： 二手交易監控

## 📌 專案用途 (Introduction)
本專案為基礎程式設計(二)期中作業 。
針對 Facebook 社團中二手遊戲主機資訊更新快速、排序混亂的問題，開發此自動化監控工具。系統會自動切換至「新貼文」排序，並篩選特定關鍵字，將目標貼文即時推送至個人 Telegram 

## ⚙️ 執行方式 (Installation & Usage)
1. **環境安裝**：
   - 確保已安裝 Python 3.10+
   - 安裝套件：`pip install playwright requests`
   - 安裝瀏覽器：`playwright install chromium`
2. **登入設定**：先執行 `執行登入狀態.py` 產出 `auth.json`。
3. **啟動獵人**：執行 `抓取CODE.py` 開始自動掃描。

## 🤖 AI 協作說明 (AI Implementation)
本專案全程使用 **Google Gemini**與**Claude** 協助開發 
- **Debug 支援**：解決了 Facebook 動態選單定位失敗（Timeout）的問題 [cite: 25]。
- **技術優化**：由 AI 建議改採「鍵盤模擬導航」與「URL 去重」技術，提升爬取穩定性。

## ⚙️ 備註 (NOTE)
1.抓取CODE.py中，5至6行請自行更改為telegram的bot(因隱私問題，這邊不開啟自己的)
2.抓取CODE中有幾項可以客製化:
   - 第20行可更換想搜尋的社團代碼
   - 第64可更改滾動次數
   - 第112行可更改抓取貼文的數量
   - 第152行可更改想搜尋的商品
