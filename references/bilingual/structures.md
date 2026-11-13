# 結構反模式（跨語言）

> 本文件是解釋、範例與操作細則；行為合約的單一來源是 `SKILL.md`，兩處表述不一致時以 `SKILL.md` 為準。

> 這些模式不是某個詞的問題，而是句子和段落層面的 AI 痕跡。中英文通用。

## 1. 二元對比假戲劇

**模式**：先否定 X，再肯定 Y，製造虛假的頓悟感。

```
❌ 這不是技術問題，而是管理問題。
❌ It's not about the code. It's about the culture.
```

```
✅ 管理流程比程式碼本身更容易出問題。
✅ The culture around code review matters more than the code itself.
```

**檢測**：看密度和分布，不看單次出現。**先按下面「保留條件」把豁免項剔除，再對剩下的計數**——豁免項不計入密度，也不因為密度超標被改；只有剩餘項超標才處理。這樣改完的輸出重新過一遍規則不會再次命中。命中信號：

- 同段連續 2 組以上（含與價值拔高骨架混合疊加）
- 全文按長度歸一（計數口徑同 [嚴重度分級](./severity.md)：中文按字數，英文按詞數，程式碼片段 / 路徑 / 命令 / 版本號各計 1，標點和空白不計）：< 300 字/詞 出現 2 處以上；300–1000 字/詞 出現 3 處以上；> 1000 字/詞 平均每 300 字/詞 1 處以上
- 變體同樣計入：`不像 A，像 B`、`要的是 X，不是 Y`、`X 不行，Y 才行`，以及連續多條以否定收尾的列表項或表格行
- 讀到後面能預判下一句形狀

**預設動作**：豁免項原樣保留；剩餘超標的骨架按 `in-place` 替代動作換成中性連接或直接陳述（`X 不夠，Y 更重要`、`相比 X，Y 更能說明問題`），兩邊資訊都要保留。只把 `不是 X，是 Y` 倒裝成 `Y，不是 X` 不算完成降密度——骨架還在。不要見一個殺一個，也不要把豁免項一起抹平成同一種平鋪句。

**保留條件**：豁免上限 2 處。超過 2 處都聲稱「承擔論證」時不再逐條豁免——每一處都說得出理由，恰恰是骨架依賴的表現，仍按密度處理。逐條判據：

- **術語定義**（最多 1 處，通常在首句或定位句）：`X 不是 A，是 B` 用來糾正讀者對 X 是什麼的誤讀
- **論證骨架**（最多 1 處）：前半句是讀者會真實持有的誤解，且刪掉它之後，後文的數據、結論或動作會失去依據——「讀起來氣勢弱一點」不算
- **引用原文、被討論對象**：不計入密度，也不受上述數量上限約束

## 2. 否定式列舉

**模式**：先說不是什麼，再說是什麼。繞了一圈。

```
❌ 它不是框架，不是庫，也不是工具——它是一種思維方式。
❌ It's not a framework. It's not a library. It's a way of thinking.
```

```
✅ 把它當作一種思維方式，不是一個具體工具。
✅ Think of it as a mental model, not a tool.
```

## 3. 戲劇化碎句

**模式**：用句子碎片製造假的力量感。

```
❌ 三年。兩個人。一個想法。
❌ Three years. Two people. One idea.
```

```
✅ 兩個人花了三年把這個想法做成了產品。
✅ Two people spent three years turning the idea into a product.
```

## 4. 反問式鋪墊

**模式**：用反問或「如果」開頭吊胃口。

```
❌ 如果我告訴你，90% 的創業公司都在犯同一個錯誤呢？
❌ What if I told you 90% of startups make the same mistake?
```

```
✅ 90% 的創業公司在定價上犯同一個錯誤：按成本定價而不是按價值定價。
✅ 90% of startups misprice their product, using cost-based pricing instead of value-based.
```

## 5. 虛假主語（False Agency）

**模式**：給無生命的事物安上人類動作（「賦能」「助力」「驅動」）。當句子抽象空泛、沒有具體資訊時優先改寫。技術文件中描述系統行為的非人主語（「閘道返回 504」「快取過期」）是合理的，不需要改。

```
❌ 該框架賦能了開發者社群。
❌ The framework empowers the developer community.
```

```
✅ 開發者用這個框架能少寫 30% 的樣板程式碼。
✅ Developers write 30% less boilerplate with this framework.
✅ 閘道在逾時後返回 504。（技術描述，不改）
```

## 6. 被動語態堆砌

**模式**：連續使用被動語態，隱藏動作執行者。研究論文、實驗報告或正式學術摘要裡的常規被動不一定要改。

```
❌ 系統被優化後，性能被顯著提升，用戶體驗被大幅改善。
❌ The system was optimized, performance was improved, and user experience was enhanced.
```

```
✅ 我們優化了資料庫查詢，頁面載入從 3 秒降到 0.8 秒。
✅ We optimized database queries and cut page load time from 3s to 0.8s.
```

```
✅ The experiment was conducted by researchers at MIT.（學術語體，可保留）
```

## 7. 三件套列舉

**模式**：AI 偏愛三個一組。兩個或一個往往更自然。

```
❌ 創新、協作、卓越。
❌ Innovation, collaboration, and excellence.
```

```
✅ 把東西做出來，做好。
✅ Build things. Build them well.
```

## 8. 「首先…其次…最後…」 機械排列

**模式**：中文特有的機械遞進，製造假的邏輯感。

```
❌ 首先，我們需要明確目標；其次，制定計畫；最後，執行落地。
```

```
✅ 先把目標定清楚，然後排優先級，邊做邊調。
```

## 9. Wh- 開頭句（英文特有）

**模式**：用 What/When/Where/Which/Who/Why/How 開頭的句子在 AI 文本中過度集中。

```
❌ What makes this approach unique is its simplicity.
```

```
✅ This approach works because it's simple.
```

## 10. 總結式收尾

**模式**：每段或全文末尾用「總之」「綜上」做總結，重複已說過的內容。

```
❌ 綜上所述，該方案在性能、安全性和可維護性方面都表現優異。
❌ In conclusion, this approach excels in performance, security, and maintainability.
```

```
✅ 刪掉。前面說清楚了就不用再說一遍。
✅ Delete it. If you said it clearly above, don't repeat it.
```

## 11. 對稱填充（Symmetry Padding）

**模式**：為了「平衡」而硬湊對仗，沒有資訊增量。

```
❌ 既要保證速度，又要保證品質；既要創新突破，又要穩定可靠。
```

```
✅ 速度和品質之間我們優先品質。
```

## 12. 無源引用

**模式**：用「研究表明」「數據顯示」「專家指出」但不給具體來源，製造假的權威感。

```
❌ 研究表明，遠程辦公能提高 30% 的生產力。
❌ Studies show that remote work increases productivity by 30%.
```

```
✅ Stanford 2023 年的一項實驗發現，全遠程員工的程式碼提交量比混合辦公多 13%。
✅ A 2023 Stanford experiment found fully remote employees committed 13% more code than hybrid workers.
```

## 13. 加粗濫用

**模式**：機械地給每個要點加粗，製造假的層次感。

```
❌ **用戶體驗：** 界面全面升級。**性能優化：** 演算法顯著提升。**安全加固：** 新增端到端加密。
```

```
✅ 界面重新設計了，演算法快了 2 倍，加了端到端加密。
```

## 14. 分條列點強迫癥

**模式**：任何內容都要 1. 2. 3. 分條，連簡單回覆也列點，製造假的條理感。

```
❌ 關於這個問題，我的建議如下：
   1. 先檢查設定檔
   2. 確認環境變數
   3. 重啟服務
```

```
✅ 設定檔裡的 DB_HOST 可能寫錯了，先看一眼。不是的話重啟一下服務試試。
```

## 15. 正能量收尾強迫癥

**模式**：不管前面說了什麼，最後一段必須上價值、給雞湯、展望未來。

```
❌ ……總之，讓我們擁抱變化，積極迎接 AI 時代的無限可能！未來可期！
```

```
✅ 刪掉。前面說完了就結束。
```

## 16. 假口語化 / 硬凹網感

**模式**：AI 試圖「接地氣」時硬塞網路流行語（絕絕子、誰懂啊、真的會謝），反而更假。真人用這些詞是隨機的，AI 是批量的。

```
❌ 姐妹們！這個工具真的絕絕子！誰懂啊，效率直接拉滿！狠狠心動了！
```

```
✅ 這個工具確實好用，主要是批量處理的速度快，省了不少時間。
```

## 17. 調試腔敘事

**模式**：AI 在編程場景中用 postmortem / SRE 口吻講日常事務——「兜住」「落盤」「根因」「收口」。把 debug 術語泛化到一切對話中。

```
❌ 我已經把差異收窄了，根因基本坐實，接下來做一個更硬的排除法把問題打掉。
```

```
✅ 原因找到了：是快取過期導致的。我把可能性排查了一遍，現在就剩這一個。
```

## 18. 節奏單調（統計信號）

**模式**：AI 文本的節奏比人類均勻得多。兩個子信號：

- **句長均勻**：每句話長度幾乎一樣（句長標準差約 1.2，人類約 4.7+）。表現為「讀起來很平，沒有呼吸感」。
- **句式骨架重複**：同一種句法形狀反覆出現，最常見的是二元對比（`不是 X，是 Y`），其次是每一節末尾都落一個對仗短句。單句都成立，連著讀能預判下一句形狀。

**檢測**：不是看單個詞，而是看整段乃至全文的節奏。長短句應該交替出現；同型骨架的密度閾值見第 1 條。

**預設動作**：句長層面合併或拆分句子，製造長短交替；骨架層面按第 1 條先剔除豁免項，再改剩餘超標的那幾處。兩個層面都不重寫全文。

## 19. 價值拔高骨架

**模式**：先給一個事實，再用 `不僅僅是……更是……`、`真正的 X 不是……而是……`、`最後比拼的是……` 把句子抬高成「洞見」。

```
❌ 這不僅僅是一個產品，更是一種信念的傳承。
❌ 真正的競爭力不是功能堆砌，而是體驗細節。最後比拼的是執行效率。
```

```
✅ 這就是一個產品判斷：體驗細節決定它能不能長期被用下去。
✅ 產品做得再多，最後還是看體驗細節和執行效率。
```

## 20. 標點腔（破折號過密）

**模式**：把英文 em-dash 的使用習慣帶進中文——首句就用破折號起手，一段裡連續多個 `——`，插入、轉折、補充全靠破折號承接；常伴隨分號連用、頓號亂燉和中英混排下的標點崩壞。跨模型現象，提示詞往往壓不住。

**檢測**：看密度和位置，不看單次出現。命中信號：首句破折號起手、單段兩處以上 `——`、連續多段都靠破折號承接。單個破折號不是問題，不要見一個殺一個。

```
❌ 這個工具最打動我的是速度——打開就是結果。搜索、啟動、剪貼簿——所有操作都在一個輸入框裡——你甚至不用記快捷鍵。
```

```
✅ 這個工具最打動我的是速度：打開就是結果。搜索、啟動、剪貼簿，所有操作都在一個輸入框裡，你甚至不用記快捷鍵。
```

**預設動作**：多餘的破折號按語義改回冒號、逗號、括號或直接斷句；一段最多保留一處真正承擔插入或遞進的。

**保留條件**：標題和命名裡的連接符（`todo — 終端待辦`）；引用原文；破折號本身是討論對象；全段僅一處且確實承擔插入語氣。

## 21. 防禦性免責與範圍切割腔（Defensive Scope-Policing）

**模式**：推論型模型為了避免話說太滿，每講一個方法就先花兩句強調「這只解決了 A，沒解決 B」「A 與 B 是兩碼事」「單靠 X 並不能保證 Y」。

依 `SKILL.md` A1 檢查整段意圖：不替未出現的質疑辯解，不列無關的未做事項，不自行加設驗證或排名標準。純粹防禦的句子整句刪除，不換詞重寫或搬到表格、附註、摺疊區及文末的「限制與風險」。

```
❌ 這只回答了讀取延遲的問題，並沒有解決寫入鎖死。讀取與寫入是兩件不同的事，單靠快取並不能保證系統穩定。
❌ Switching to Redis only addresses read latency; it does not solve write contention. Reads and writes are two distinct mechanisms, and relying solely on caching cannot guarantee stability.
```

```
✅ 換成 Redis 能先壓低讀取延遲；若同時遇到寫入爆量，前面還要再接一層佇列緩衝。
✅ Redis cuts read latency right away. If you also hit write spikes during peak traffic, pair it with a write queue.
```

使用者只要求比較技能用途與規則時，下面三種句子直接刪除：

| 繁中反例 | English counterexample |
|---|---|
| ❌ 不能拿分數直接判定文章品質。 | ❌ You cannot judge writing quality directly from the score. |
| ❌ 本次未修改檔案，也未做模型輸出的 A/B 測試。 | ❌ No files were changed, and no A/B tests of model outputs were run. |
| ❌ 尚不能代表實際輸出效果排名。 | ❌ This does not establish a ranking of actual output quality. |

直接報告看到的差異，結論與證據對齊後就停。例如：✅「這份規則涵蓋更多教材情境。」／✅ "These rules cover more teaching scenarios." 使用者問到風險、缺漏或工作狀態時，直接回答該項事實。

被指出問題後直接修正，不再補 ❌「不過必要限制仍須保留。」／❌ "But necessary caveats must still be retained." 送出前檢查正文、表格、附註與最後一段。

## 22. 監視器看圖報時腔（Surveillance / Pixel-Reporting Captioning）

**模式**：在圖說（caption）、影片整理或截圖教學中，只描述畫筆顏色、框線位置或秒數切換，不講背後的判斷標準。

```
❌ 綠圈標出示範者肩部位置，紅線顯示前臂角度。在 02:14 處，畫面切換至側面視角。
❌ The green circle marks the subject's shoulder position, while the red line indicates the forearm angle at 02:14.
```

```
✅ 從側面看，觸胸時前臂要保持垂直地面，避免肩膀往前滑出支撐點。
✅ From the side view, keep your forearm vertical at the bottom so the shoulder stays pinned to the bench.
```

## 23. 病歷表抽離稱謂與記帳員官僚腔（Clinical Dossier & Bookkeeper Verbalization）

**模式**：把活人叫成「受試者、示範者（the subject / the demonstrator）」，在開頭報告「未另報數據（weight and reps were not reported）」，或把自然觀察寫成「將 A 與 B 分開記錄（record A and B separately as a baseline）」。

```
❌ 提交組的參數未另報。受試者先記下初始延遲作為比較基準，再把快取命中率與逾時次數分開記錄。
❌ Environment parameters were not separately reported. The subject records initial latency as a baseline and logs cache hits and timeouts separately.
```

```
✅ 先看改參數前的延遲落在幾毫秒，再單獨觀察快取命中率有沒有拉上來。
✅ Check your latency before changing the config, then watch whether the cache hit rate climbs on its own.
```
