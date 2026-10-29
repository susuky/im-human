# im-human｜台灣繁體中文與英文「說人話」寫作技能

受夠了 AI 動不動就寫「在當今瞬息萬變的時代、首先其次最後、不是 A 而是 B」的行銷套話？
或者更慘——當你叫 Codex、o3、GPT、Claude 幫你整理課程筆記、寫技術文件時，它為了「怕講錯話被抓包」，寫出像**法醫驗屍報告、監視器報時筆錄、醫院初診病歷表、律師免責聲明**一樣冰冷難讀的文字？

`im-human` 就是專治這兩代 AI 寫作災難的技能包：

1. **封殺第一代「浮誇行銷小編與客服套話」**：砍掉空洞拔高（賦能、閉環、底層邏輯、全方位）、切吐司路標詞（首先／其次／最後）、二元假對立與馬克杯金句收尾。
2. **根除第二代推論／代理模型的「驗屍報告與防禦免責腔」**：徹底拔除「這只回答了 A 沒有解決 B」的切割說教、「在 02:14 處綠圈標出受試者」的監視器看圖報時、「將 X 與 Y 分開記錄作為基準」的記帳官僚腔，以及把生動痛點洗成平淡字典定義的「悶騷規格書腔」。

無論是日常對話、順稿改寫，還是把幾十部影片與逐字稿整理成教材講義，都能讓模型像一位**腦袋清楚、實話實說的台灣資深同事或領域教練**一樣把事情講明白。

---

## 改寫前後對照（為什麼一般去 AI 味指令沒用？）

一般 Prompt 只叫模型「不要像 AI、不要亂編」，結果推論模型會走向另一個極端——句句防禦、只報畫面像素與秒數。看看 `im-human` 處理這類災難的差別：

### 案例 1：整理教學影片與圖文教材（拔除「監視器報時腔＋病歷表腔＋記帳腔」）

* ❌ **一般推論模型寫出來的災難（驗屍報告＋看圖報時）**：
  > 提交組的負重參數未另報。在 02:52–02:58 處，指導者在上胸與肩前附近接受接觸提示；03:00–03:14 接觸放開後，這位練習者指向自己的胸前。單靠改變手部位置並不能保證胸廓展開，練習時應將起始角度與主觀費力程度分開記錄，作為後續回測的比較基準。
* ✅ **掛載 `im-human` 後的人話（專業教練口吻）**：
  > 站姿拉彈力帶上舉時，很多人會不自覺用肩膀前側硬拉，胸骨根本沒動。助教直接輕點學員的上胸與鎖骨下方，提示「吸氣時胸骨先往前上方送，雙手只是順著張力跟上去」。放手後學員再推一次，馬上能指著胸口確認自己抓到由胸骨帶動雙臂的發力感。

### 案例 2：軟體架構與工程溝通（拔除「防禦免責說教＋名詞化殭屍句＋拔高殼」）

* ❌ **一般模型寫出來的災難（防禦切割＋進行體官腔）**：
  > 值得注意的是，將快取層切換至 Redis 只回答了讀取延遲的問題，並沒有解決資料庫寫入鎖死。讀取快取與寫入佇列是兩個不同的機制，不能混為一談。在本次重構中，系統進行了快取策略的優化，這不僅提升了系統韌性，更為後續的高併發架構奠定了堅實的基礎。
* ✅ **掛載 `im-human` 後的人話（台灣資深工程師口吻）**：
  > 把快取換成 Redis 之後，首頁查詢的 P99 延遲從 820ms 降到 95ms。不過這一步只會減輕讀取壓力；遇到秒殺活動那種瞬間大量寫入，資料庫還是會鎖死，那部分下週要另外接 Kafka 佇列來緩衝。

### 案例 3：產品公告與客服回覆（拔除「頒獎開場＋四層避險墊詞」）

* ❌ **一般模型寫出來的災難**：
  > 感謝您的寶貴回饋！這真是一個非常棒的觀察。關於您提到的匯出報表亂碼問題，可能潛在地與預設編碼格式在某種程度上有所關聯。為了給您帶來更流暢、更高效的體驗，我們已進行了匯出模組的調整，希望這對您有幫助！
* ✅ **掛載 `im-human` 後的人話**：
  > 報表用 Excel 打開會亂碼，是因為舊版預設輸出無 BOM 的 UTF-8。我們剛更新上線，現在匯出 CSV 會自動帶入 BOM 標記，直接雙擊打開就是正常中文字了。請重新匯出試試；如果手邊的舊檔急需轉檔，直接回信傳給我處理。

---

## 安裝方式

在專案資料夾開啟 PowerShell，依你使用的工具複製到對應的技能目錄：

### 1. OpenAI Codex（本機 CLI / 桌面端）

```powershell
$target = Join-Path $env:USERPROFILE '.codex\skills\im-human'
New-Item -ItemType Directory -Path $target -Force | Out-Null
Copy-Item -LiteralPath 'SKILL.md', 'README.md', 'references', 'prompts', 'scripts' -Destination $target -Recurse -Force
```

### 2. Google Antigravity / Gemini CLI / Claude Code

```powershell
# Antigravity App / IDE
$agyTarget = Join-Path $env:USERPROFILE '.gemini\config\skills\im-human'
New-Item -ItemType Directory -Path $agyTarget -Force | Out-Null
Copy-Item -LiteralPath 'SKILL.md', 'README.md', 'references', 'prompts', 'scripts' -Destination $agyTarget -Recurse -Force

# Gemini CLI
$geminiTarget = Join-Path $env:USERPROFILE '.gemini\skills\im-human'
New-Item -ItemType Directory -Path $geminiTarget -Force | Out-Null
Copy-Item -LiteralPath 'SKILL.md', 'README.md', 'references', 'prompts', 'scripts' -Destination $geminiTarget -Recurse -Force

# Claude Code
$claudeTarget = Join-Path $env:USERPROFILE '.claude\skills\im-human'
New-Item -ItemType Directory -Path $claudeTarget -Force | Out-Null
Copy-Item -LiteralPath 'SKILL.md', 'README.md', 'references', 'prompts', 'scripts' -Destination $claudeTarget -Recurse -Force
```

各工具的目錄規則見 [Antigravity](https://antigravity.google/docs/skills)、[Gemini CLI](https://geminicli.com/docs/cli/skills/) 與 [Claude Code](https://code.claude.com/docs/en/skills) 官方文件。

如果是網頁版 ChatGPT 或 Claude Projects，直接複製 [`prompts/chatgpt-custom-instructions.md`](prompts/chatgpt-custom-instructions.md)（短版自訂指令）或 [`prompts/chatgpt-project.md`](prompts/chatgpt-project.md)（完整專案指令）貼進系統設定即可。

---

## 三種運作模式與呼叫範例

你不需要背複雜參數，直接告訴模型要做什麼，它會自動切換對應模式：

| 你要做的事 | 觸發模式 | 運作原則 |
| --- | --- | --- |
| **日常問答、寫 code 解釋、討論方案** | **1. 語態模式（Voice）** | 第一句直接講結論與原因，長短句交錯，零客套開場、零免責結尾。 |
| **幫現成草稿順稿、去 AI 味** | **2. 編輯模式（Edit）** | 嚴守原文的數據、日期、專名與作者立場，只剃除 AI 模板殼、防禦腔與翻譯腔。 |
| **從影片、逐字稿、程式碼產出教材與文件** | **3. 教材與文件產出模式（Authoring）** | 把零散原料轉化為「沒看過原片／原檔的人也能看懂」的教學文，交代原理、步驟與判準，嚴禁寫成監視器流水帳。 |

**常用呼叫方式：**

```text
# 日常問答直接說人話
$im-human 接下來用台灣繁體中文回答，直接講重點，不要寫免責聲明或客套話。

# 幫既有草稿去 AI 味
$im-human 把下面這段文字改得自然好讀，保留裡面的日期、數據與專有名詞：
［貼上草稿］

# 整理課程教材或專案文件
$im-human 讀取這份逐字稿與影格，整理成給學員複習的圖文教材。
直接講動作原理、操作步驟與判斷標準，不要寫成「幾分幾秒誰碰了哪裡」的監視器筆錄。
```

---

## 自動掃描腳本（`audit_ai_flavor.py`）

改完稿或批次產出教材後，可以用內建的 Python 腳本（零外部依賴，僅需 Python 3 標準庫）做機械回歸檢查，把漏網的「行銷小編詞、驗屍報告腔、防禦說教腔、看圖報時腔、中國大陸用語、句型模具連發」一次抓出來：

```bash
# 掃描單一或多個 UTF-8 文字檔
python scripts/audit_ai_flavor.py README.md SKILL.md

# 輸出完整 JSON 報告（含命中類別、行號、扣分與原文片段）
python scripts/audit_ai_flavor.py README.md --json

# 用於 CI 或自動化驗收：有檔案被標為 review 時回傳 1，通過時回傳 0
python scripts/audit_ai_flavor.py README.md --fail-on-review
```

> **判讀提示**：腳本抓的是高風險句型與詞彙。如果命中處屬於「引用原話、討論禁詞本身、或必要專有名詞」，人工確認語境自然即可放行。

---

## 檔案結構與參考武器庫

| 檔案路徑 | 內容說明 |
| --- | --- |
| [`SKILL.md`](SKILL.md) | 技能主合約：三種運作模式、兩大代 AI 病灶總表、跨領域 Before/After 範例與交稿前 15 秒自檢。 |
| [`references/tw/patterns.md`](references/tw/patterns.md) | **核心武器庫**：完整收納台灣繁中 45 種 AI 寫作病灶（含驗屍報告腔、防禦腔、監視器圖說腔、記帳腔、小編腔）與誤殺邊界。 |
| [`references/tw/taiwan-localization.md`](references/tw/taiwan-localization.md) | 台灣日常與工程慣用詞彙對照表（清除「視頻、質量、信息、默認、優化」等詞）與全形標點規範。 |
| [`references/tw/humanize.md`](references/tw/humanize.md) | 如何擺脫「每句都正確、整篇卻像規格書」的溫吞感，寫出有節奏與判斷力的文字。 |
| [`references/tw/scenes.md`](references/tw/scenes.md) | 技術文件、教學講義、工程 PR、商務信件、社群貼文等不同場景的語氣刻度。 |
| [`references/tw/examples.md`](references/tw/examples.md) | 各場景的原稿診斷與改寫前後完整範例。 |
| [`references/bilingual/operation-manual.md`](references/bilingual/operation-manual.md) | 英文寫作去 AI 味規則（封殺 `delve`, `leverage`, `testament to` 等詞）與中英混排原則。 |
| [`scripts/audit_ai_flavor.py`](scripts/audit_ai_flavor.py) | 繁中 AI 痕跡與驗屍報告腔自動化掃描腳本。 |
