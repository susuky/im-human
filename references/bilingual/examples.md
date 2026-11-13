# 改寫範例

> 本文件是解釋、範例與操作細則；行為合約的單一來源是 `SKILL.md`，兩處表述不一致時以 `SKILL.md` 為準。

> 每個範例展示同一段內容的 AI 版和人話版。

## 中文範例

### 範例 1：項目介紹

**AI 版：**
> 該項目是一個創新性的解決方案，旨在通過深度整合多種前沿技術，為用戶提供全方位、一站式的智能化體驗。它不僅能夠顯著提升工作效率，還能有效降低運營成本，實現真正的降本增效。

**人話版：**
> 這個項目把語音識別和自動翻譯接到一起，用戶說中文就能直接出英文字幕。上線兩週日活 1200，翻譯準確率 94%。

**改了什麼：**
- 刪掉「創新性」「前沿技術」「全方位」「一站式」「智能化」——全是空詞
- 刪掉「不僅…還能…」的二元結構
- 加了具體功能描述和數據

---

### 範例 2：技術總結

**AI 版：**
> 綜上所述，通過對系統架構的全面優化和持續迭代，我們在性能、安全性和可維護性等方面均取得了顯著提升。這一成果充分體現了團隊在技術創新方面的不懈追求和卓越實力。

**人話版：**
> 這輪改完之後：API 回應時間從 800ms 降到 120ms，修了 3 個 SQL 注入漏洞，把 6000 行的 God Class 拆成了 12 個模組。

**改了什麼：**
- 刪掉「綜上所述」和整個總結式開頭
- 「顯著提升」換成具體數據
- 刪掉「充分體現」「不懈追求」「卓越實力」——自吹自擂
- 用具體改動代替抽象描述

---

### 範例 3：消息回覆

**AI 版：**
> 好問題！這確實是一個值得深入探討的話題。讓我來為你詳細解釋一下。首先，我們需要了解的是，這個問題的本質在於……

**人話版：**
> 核心原因是快取沒失效。用戶改了頭像但 CDN 還在用舊的，TTL 設了 7 天太長了。改成 1 小時就行。

**改了什麼：**
- 刪掉全部諂媚和鋪墊
- 直接給原因和解決方案

---

### 範例 4：新聞摘要

**AI 版：**
> 在當今快速發展的人工智能領域，OpenAI 近日發布了其最新的大語言模型，引發了業界的廣泛關注和熱烈討論。該模型在多個關鍵指標上實現了顯著突破，標誌著人工智能技術邁入了一個全新的發展階段。

**人話版：**
> OpenAI 發了 GPT-5。MMLU 跑分 92.3%，比上一代高 7 個點。上下文視窗翻倍到 256K。API 價格沒漲。

**改了什麼：**
- 刪掉「在當今」「快速發展」「廣泛關注」「熱烈討論」——全是廢話
- 「顯著突破」換成具體跑分
- 「全新的發展階段」刪掉——讀者自己會判斷

---

### 範例 5：工程師腔 / 調試腔

**AI 版：**
> 我先拆開看了一下，發現根因偏硬，不太好直接打掉。目前已經把差異收窄了，和剛抓到的現象也對上了。接下來穩穩兜住，落盤之後就能收口。

**人話版：**
> 查了一下，原因是配置寫死了，不能直接改。我把排查範圍縮小到兩個可能的地方，和之前的錯誤訊息對得上。先把結論記下來，回頭改一版就行。

**改了什麼：**
- 「拆開看」→「查了一下」，「根因偏硬」→「原因是配置寫死了」
- 「打掉」→「改」，「收窄」→「縮小」，「抓到的現象」→「錯誤訊息」
- 「兜住」→刪掉，「落盤」→「記下來」，「收口」→「就行」
- 整段從 postmortem 腔調改成正常同事對話

---

### 範例 6：小紅書 AI 腔

**AI 版：**
> 姐妹們！今天給大家拆解一個保姆級避坑攻略！這個工具真的絕絕子，狠狠提升了效率！建議收藏！劃重點：免費！

**人話版：**
> 推薦一個工具：Raycast。免費版就夠用，主要是啟動快、外掛多。我之前用 Alfred，切過來之後每天大概能省十幾分鐘，主要省在切視窗和查文件上。

**改了什麼：**
- 刪掉全部硬凹人設的網路語
- 「拆解」「保姆級」「避坑」「絕絕子」「狠狠」「建議收藏」「劃重點」全刪
- 換成具體工具名、具體用法、具體省了多少時間

---

### 範例 7：語域混搭

**AI 版：**
> 誠然，這個 bug 的修復確實存在一定的技術複雜度。不過說白了就是絕絕子的體驗！我們需要進一步深入探討其底層邏輯，穩穩把核心鏈路兜住。綜上所述，未來可期。

**人話版：**
> 這個 bug 不好修，涉及到三個服務之間的呼叫順序。我先把支付服務的逾時時間從 3 秒調到 10 秒，觀察一週再說。

**改了什麼：**
- 原文混搭了 5 種語域（學術/網路/商業/工程/雞湯），統一成技術口語
- 把空泛描述換成具體方案

---

## English Examples

### Example 1: Product description

**AI version:**
> Our groundbreaking platform serves as a testament to the transformative potential of AI, empowering teams to navigate complex challenges and unlock unprecedented levels of productivity. Nestled at the intersection of innovation and practicality, it showcases how cutting-edge technology can foster meaningful collaboration.

**Human version:**
> The platform auto-assigns tickets based on who fixed similar bugs before. Teams using it close issues 2 days faster on average.

**What changed:**
- Removed "groundbreaking", "testament", "empowering", "navigate", "unprecedented", "nestled", "showcases", "cutting-edge", "foster"
- Replaced vague claims with specific functionality and data

---

### Example 2: Technical update

**AI version:**
> We're excited to announce a comprehensive update that significantly enhances performance, bolsters security, and streamlines the developer experience. This pivotal release underscores our commitment to delivering robust, scalable solutions.

**Human version:**
> This release cuts cold start time by 60%, patches CVE-2024-3891, and drops the config from 200 lines to 40. Upgrade guide is in the changelog.

**What changed:**
- "Comprehensive update" → specific changes
- "Significantly enhances" → "cuts by 60%"
- "Bolsters security" → specific CVE
- "Streamlines developer experience" → specific config reduction
- Deleted "pivotal", "underscores", "commitment", "robust", "scalable"

---

### Example 3: Analysis (two-pass demo)

**AI version:**
> The landscape of remote work has undergone a profound transformation. It's not just about working from home — it's about reimagining the very fabric of how we collaborate. Companies that fail to navigate this paradigm shift risk being left behind in an increasingly competitive ecosystem.

**First pass:**
> Remote work changed how teams collaborate. The teams that leaned into async communication and cut meetings adapted faster.

**Audit — what still feels AI?**
- "changed how teams collaborate" is still broad
- "adapted faster" is vague and a bit polished

**Final:**
> Remote work changed how teams collaborated, but not every company adjusted in the same way. Some changed how they communicated and worked together. Others just kept the same habits in a different setting.

**What changed in second pass:**
- Replaced the broad opener with a clearer contrast that stays inside the original claim
- Removed the vague "adapted faster"
- Broke the rhythm a bit without inventing new facts

---

## Two-pass examples | Residual Audit

### 範例 A：公開寫作裡的一遍 vs 兩遍

**原文：**
> 這次把 onboarding 流程改了一遍，新用戶從註冊到完成首次導入少走了兩步。更重要的是，這也說明我們開始真正理解用戶在第一天最容易卡住的地方。

**第一遍：**
> 這次把 onboarding 流程改了一遍，新用戶從註冊到完成首次導入少走了兩步。我們也更清楚用戶第一天最容易卡在哪裡。

**第二遍：**
> 這次把 onboarding 流程改了一遍，新用戶從註冊到完成首次導入少走了兩步。用戶第一天最容易卡的地方，就是首次導入。

**第二遍改了什麼：**
- 去掉了 `更重要的是 / 這也說明我們開始真正理解` 這層 narrator 話術
- 保留原文已有判斷，只把它壓回更直接的句子
- 沒有補新事實，也沒有重寫整段

### 範例 B：status 場景裡的克制 second pass

**原文：**
> 4 月 13 日把重試次數從 2 次調到 5 次。支付逾時從 1.9% 降到 0.7%。這次調整也進一步驗證了我們的優化方向是正確的。明天繼續看晚高峰數據。

**第一遍：**
> 4 月 13 日把重試次數從 2 次調到 5 次後，支付逾時從 1.9% 降到 0.7%。這次調整說明方向是對的。明天繼續看晚高峰數據。

**第二遍：**
> 4 月 13 日把重試次數從 2 次調到 5 次後，支付逾時從 1.9% 降到 0.7%。明天繼續看晚高峰數據。

**第二遍改了什麼：**
- 只刪掉 `方向是對的` 這種空判斷
- 保留日期、數字和下一步，不往更口語的方向拋光
- `status` 場景如果第一遍已經夠直接，第二遍就到這裡停

---

## Bounded 雙合約範例 | Bounded Scope Example

> bounded 的輸出分兩部分：句內洗過的正文，和一份交用戶確認的刪除清單。範例（合成文本）：

**原文**

> 在數字化浪潮席卷各行各業的今天，提效工具層出不窮。我們團隊過去三個月把週報流程從手填 Excel 改成了機器人自動匯總，每週大約省出兩小時。研究表明，重複性事務的自動化能顯著提升組織效能。具體做法是：機器人每週五拉取任務系統的狀態變更，生成草稿，負責人只補一句風險說明。這不僅僅是一次流程優化，更是一種工作方式的革新。下個月我們準備把例會紀要也接進來。

**正文（句內洗後）**

> 提效工具很多。我們團隊過去三個月把週報流程從手填 Excel 改成了機器人自動匯總，每週大約省出兩小時。具體做法是：機器人每週五拉取任務系統的狀態變更，生成草稿，負責人只補一句風險說明。下個月我們準備把例會紀要也接進來。

**建議刪除（待確認）**

1. 「研究表明，重複性事務的自動化能顯著提升組織效能。」——無源權威鋪墊；刪掉後該段資訊點不變（前後句已經給出做法和收益），也不承擔過渡。不建議改寫成「聽說 / 據說」，那只是把無源說法換個殼。
2. 「這不僅僅是一次流程優化，更是一種工作方式的革新。」——價值拔高收尾；剝掉句式後沒有剩餘資訊，前句（具體做法）和後句（下月計畫）直接相接不斷裂。

第一句「在數字化浪潮……層出不窮」沒有進清單：剝掉鋪墊後還剩「提效工具很多」這個實質判斷，所以走句內洗，不刪整句。

---

## 標註模式範例 | Annotation Mode Examples

> 下面這幾組展示同一段文本在 `annotation mode` 和預設改寫模式下的區別。

### 範例 A：公開文案裡的無源引用

**原文：**
> 研究表明，採用 AI 協作開發的團隊交付效率顯著提升。業內人士認為，這一趨勢將在未來十年持續加速。

**Annotation mode：**
- `問題族`：無源引用
- `觸發點`：`研究表明`、`業內人士認為`
- `建議動作`：補具體來源；如果沒有來源，刪掉權威鋪墊
- `是否建議改寫`：是

**預設改寫：**
> 用 AI 協作開發的團隊，交付速度可能會更快，但這段話沒有給出具體來源。要麼補研究出處，要麼直接把結論改寫得更克制。

### 範例 B：status 場景裡的保守處理

**原文：**
> 數據顯示，這次改版顯著提升了留存率。業內人士認為，這個方向已經驗證可行。

**Annotation mode：**
- `問題族`：無源引用
- `觸發點`：`數據顯示`、`業內人士認為`
- `建議動作`：在 `status` 場景優先補數據來源和歸屬，不要改寫成像已證實的事實
- `是否建議改寫`：是

**預設改寫：**
> 這段缺數據來源和觀點歸屬。作為 status，同步時應補具體報表、時間範圍或負責人；在補齊之前，不建議把它寫成已經證實的結論。

### 範例 C：技術文件裡的不改案例

**原文：**
> 閘道在請求逾時後返回 504。快取服務每 5 分鐘刷新一次熱點 key。負載均衡器將流量按權重分配到三個後端節點。

**Annotation mode：**
- `問題族`：無明顯問題
- `觸發點`：系統主語和技術術語都屬於正常文件寫法
- `建議動作`：保持不動
- `是否建議改寫`：否

**預設改寫：**
> 閘道在請求逾時後返回 504。快取服務每 5 分鐘刷新一次熱點 key。負載均衡器將流量按權重分配到三個後端節點。
