#!/usr/bin/env python3
"""AI 味回歸掃描（v2）：同時抓出「第一代行銷小編套話」與「第二代推論／代理模型的法醫驗屍報告腔、防禦免責腔、監視器看圖報時腔、記帳員官僚腔」、簡體／大陸用語殘留與標點問題。

結果只作提示，不取代編輯判斷——禁詞表本身、引用原話、技術術語命中都屬誤殺。
注意：本腳本鼓勵教學與操作文自然使用「你」與讀者對話，不再將「你」計入違規。
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows 主控台預設非 UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CODE_FENCE_LANGS = {
    "bash", "bat", "c", "cmd", "cpp", "css", "diff", "dockerfile", "go",
    "html", "ini", "java", "javascript", "js", "json", "powershell", "ps1",
    "py", "python", "rust", "sh", "shell", "sql", "toml", "ts", "typescript",
    "xml", "yaml", "yml", "zsh",
}

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}
SCAN_EXTENSIONS = {".md", ".txt", ".json"}


@dataclass(frozen=True)
class Rule:
    rule_id: str
    label: str
    severity: int
    pattern: re.Pattern[str] | None = None
    terms: tuple[str, ...] = ()
    scan_code_spans: bool = False


# 嚴格確認不在 Big5 (cp950) 內的簡體專用字 + 常見繁簡轉換誤字
SIMPLIFIED_RESIDUE_PATTERN = re.compile(
    r"[这们说为吗发开关过还进经现实业产动东车书长专认让记讲设试话该请读调谈谢谁课给结继维综统线总质资费软较输转办务协单卖历压双变号叹听响图团园围场块坚坛报执扩扫扬护拟拥择换据损摆携摄数断无旧时显晋晓暂术杂权条来标栈栏树样档桥检欢岁归汇汉汤沟浅测济涨润滥湾湿满炼烂烦烧热爱独环电画畅疗盘监盖盗矿码确碍礼积称稳穷竞笔筛筹签简节药荣获虑虽补装裤]"
    r"|与(?![共俱])"
    r"|這里|哪里|什么|怎么|這么|那么"
    r"|重復|復雜|復現|復制|復述|反復"
    r"|干凈|范圍|范式|規范|示范|咨詢|關系|聯系|標簽|夸張|空夸|日志|標志|雜志|游戲"
    r"|沖鋒|緩沖|沖突|云原生|云端|工作臺|注冊|注釋|標注|杠桿|愿景|愿意"
)


RULES = [
    # ---- 工具殘留（即使在反引號或連結內也需掃描）----
    Rule(
        "tool_artifacts",
        "AI 工具追蹤參數或引用殘碼（utm_source=chatgpt.com / turn0search）",
        3,
        re.compile(
            r"utm_source=(?:chatgpt\.com|openai|copilot\.com)"
            r"|referrer=grok\.com"
            r"|(?:cite)?turn\d+(?:search|news)\d+",
            re.IGNORECASE,
        ),
        scan_code_spans=True,
    ),
    # ---- 第二代推論／代理模型重災區：驗屍報告、防禦免責、監視器看圖、病歷表、記帳腔 ----
    Rule(
        "defensive_scope_policing",
        "防禦性免責與範圍切割腔（只回答了／是兩碼事／不能單靠／未修改檔案）",
        3,
        re.compile(
            r"只回答了[^。！？\n]{1,30}(?:沒有|並未|沒能|不代表)"
            r"|這只能處理[^。！？\n]{1,24}(?:無法|不能)取代"
            r"|是兩(?:個|件|種)不同的(?:動作|事|問題|機制|概念)"
            r"|不能混為一談|不可混為一談"
            r"|(?:單靠|僅靠)[^，。！？\n]{1,20}(?:並不能|無法|不能)(?:保證|解決|取代)"
            r"|這並不是萬靈丹"
            r"|在討論[^。！？\n]{1,24}之前[，,]?我們必須先釐清"
            r"|不能拿分數直接判定|尚不能代表實際"
            r"|未修改檔案|未做[^，。！？\n]{0,12}(?:A/B\s*)?測試"
            r"|必要限制仍須保留"
        ),
    ),
    Rule(
        "clinical_autopsy_register",
        "法醫／病歷表抽離稱謂與筆錄開頭（受試者／示範者／未另報）",
        3,
        re.compile(
            r"受試者|(?<!沒有)示範者|協助者|提交者|目標對象|該名使用者"
            r"|未另報|工作重量未標示|來源未標示|未提及具體|未標示系統環境"
        ),
    ),
    Rule(
        "pixel_caption_reporting",
        "監視器看圖報時腔（綠圈標出／紅框圈出／在 02:14 處畫面／如圖所示）",
        3,
        re.compile(
            r"(?:綠圈|紅圈|黃圈|藍圈|綠框|紅框|黃框|綠線|紅線|黃線)(?:標出|圈出|標示出|畫出)"
            r"|在\s*\d{1,2}:\d{2}\s*處[，,]?\s*(?:畫面|鏡頭|講者)"
            r"|如圖所示|箭頭指向|穿(?:黑|白|藍|紅|紫|綠)衣的"
        ),
    ),
    Rule(
        "bookkeeper_verbalization",
        "記帳員／官僚檢核表腔（分開記錄／一起記錄／記下作為比較基準）",
        2,
        re.compile(
            r"(?:分開|一起|分別)記錄"
            r"|先記下[^。！？\n]{1,24}作為[^。！？\n]{0,12}比較基準"
            r"|納入觀察清單"
        ),
    ),
    # ---- 第一代對話／行銷小編模型重災區：二元對比殼、拔高、路標、翻譯腔 ----
    Rule(
        "binary_contrast",
        "二分對照殼（不是 A，而是 B）",
        2,
        re.compile(
            r"(?:不是|並非|并非|不在於|不在于|不只是|不止是|不僅是|不仅是)[^。！？\n]{0,32}"
            r"(?:而是|而在於|而在于|更是)"
            r"|與其說[^。！？\n]{0,32}不如說|与其说[^。！？\n]{0,32}不如说"
        ),
    ),
    Rule(
        "essence_claim",
        "真正／本質／核心式拔高",
        3,
        re.compile(
            r"真正[^。！？\n]{0,20}(?:的是|在於|在于|決定|决定|重要|打動|打动|改變|改变)"
            r"|本質上|本质上|核心在於|核心在于|底層邏輯|底层逻辑|說到底|歸根究柢|归根结底"
        ),
    ),
    Rule(
        "assistant_route_marker",
        "助理路標詞與客套殘留",
        3,
        terms=(
            "下面我們來", "下面我们来",
            "接下來我會", "接下来我会",
            "我們可以看到", "我们可以看到",
            "希望這能幫到你", "希望这能帮到你",
            "希望這對你有幫助", "希望这对你有帮助",
            "這是一個很好的問題", "这是一个很好的问题",
            "廢話不多說", "話不多說直接進入主題",
            "作為AI", "作为AI",
            "截至我的知識", "截至我的知识",
        ),
    ),
    Rule(
        "lecture_marker",
        "講義腔／總結腔",
        2,
        terms=(
            "總的來說", "总的来说",
            "綜上所述", "综上所述",
            "值得注意的是", "值得一提的是",
            "不可否認的是", "不可否认的是",
            "不難看出", "不难看出",
            "不難發現", "不难发现",
            "由此可見", "由此可见",
            "在這個過程中", "在这个过程中",
            "這背後其實", "这背后其实",
            "這意味著", "这意味着",
            "說白了", "说白了",
            "劃重點", "划重点",
            "捋一捋", "盤一盤", "盘一盘", "拆一拆",
        ),
    ),
    Rule(
        "inflated_abstract_words",
        "抽象包裝詞與商業黑話堆疊",
        2,
        terms=(
            "賦能", "赋能",
            "助力", "抓手",
            "閉環", "闭环",
            "深耕",
            "沉澱", "沉淀",
            "顆粒度", "颗粒度",
            "收口", "落盤", "落盘", "兜住",
            "價值感", "价值感",
            "長期主義", "长期主义",
            "意義深遠", "意义深远",
            "前景廣闊", "前景广阔",
            "開創性", "开创性",
            "不可或缺", "至關重要", "至关重要",
        ),
    ),
    Rule(
        "simplified_chinese_residue",
        "簡體中文字符或繁簡轉換誤字殘留",
        2,
        SIMPLIFIED_RESIDUE_PATTERN,
    ),
    Rule(
        "mainland_terms",
        "中國大陸用語殘留（應改為台灣繁中慣用詞）",
        2,
        terms=(
            "視頻", "短視頻", "视频",
            "軟件", "软件",
            "硬件",
            "信息",
            "數據庫", "数据库",
            "服務器", "服务器",
            "屏幕",
            "鼠標", "鼠标",
            "默認", "默认",
            "網絡", "兼容", "靠譜", "移動端", "性價比", "顏值", "貓膩", "卸載",
            "代碼", "內存", "文件夾", "網關", "博客",
            "小夥伴", "小伙伴",
            "給力", "给力",
            "接地氣", "接地气",
            "立馬", "立马",
        ),
    ),
    Rule(
        "progressive_verb_shell",
        "進行體與名詞化殭屍句（進行了討論→討論了）",
        2,
        re.compile(
            r"(?:進行|进行)(?:了|過|过)?(?:一次|一場|一场)?(?:深入|全面|初步)?的?"
            r"(?:討論|讨论|分析|研究|探討|探讨|評估|评估|溝通|沟通|梳理|盤點|盘点|調整|调整|優化|优化)"
            r"|做出[^，。！？\n]{1,12}的動作"
        ),
    ),
    Rule(
        "translationese",
        "翻譯腔（扮演角色／起到作用）",
        2,
        re.compile(
            r"扮演(?:著|着)?[^。\n]{0,10}角色"
            r"|起(?:到了?|著|着)[^。\n]{0,8}作用"
            r"|被廣泛認為|被广泛认为"
        ),
    ),
    Rule(
        "trend_opener",
        "時代／趨勢大帽子開場",
        3,
        re.compile(
            r"(?:隨著|随着)[^。\n]{2,20}的?(?:發展|发展|普及|進步|进步|興起|兴起|到來|到来)"
            r"|在(?:這個|这个|當今|当今)[^。\n]{0,12}(?:時代|时代|世代|社會|社会)"
            r"|(?:如今|時至今日|时至今日)[^。\n]{0,10}(?:已經|已经)"
        ),
    ),
    Rule(
        "hedge_filler",
        "程度模糊避險墊詞",
        1,
        terms=(
            "一定程度上",
            "某種程度上", "某种程度上",
            "在某種意義上", "在某种意义上",
            "可能潛在地",
        ),
    ),
    Rule(
        "academic_filler",
        "無源權威與學術填充套話",
        2,
        re.compile(
            r"(?:基於|基于|依據|依据)[^。！？\n]{0,18}(?:理論|理论|框架)"
            r"|研究表明|專家認為|专家认为|業內普遍認為|业内普遍认为"
            r"|具有重要(?:理論|理论|現實|现实)?(?:意義|意义)"
            r"|提供了新思路|開闢了新方向|开辟了新方向"
        ),
    ),
    Rule(
        "rigid_enumeration",
        "整齊切吐司編號邏輯（首先⋯其次⋯最後）",
        2,
        re.compile(
            r"首先.{0,80}其次|其次.{0,80}(?:再次|再者|最後|最后)|一方面.{0,80}另一方面"
        ),
    ),
    Rule(
        "fiction_cliche",
        "小說正文套話",
        1,
        terms=(
            "不禁", "情不自禁", "不由自主",
            "映入眼簾", "映入眼帘",
            "心中暗道", "暗自思忖",
            "嘴角微揚", "嘴角微扬",
            "勾起一抹弧度",
            "臉色一變", "脸色一变",
            "身形一頓", "身形一顿",
            "緩緩說道", "缓缓说道",
            "淡淡地說", "淡淡地说",
        ),
    ),
    # ---- English layer ----
    Rule(
        "en_throat_clearing",
        "英文開場清嗓／助理路標",
        3,
        re.compile(
            r"(?i)\b(?:it'?s worth noting|it'?s important to note"
            r"|in today'?s (?:fast-paced |digital |ever-changing )?world"
            r"|at the end of the day|let'?s dive in|let'?s delve"
            r"|in conclusion|i hope this helps|great question"
            r"|here'?s the thing|let that sink in)\b"
        ),
    ),
    Rule(
        "en_inflation",
        "英文空泛拔高句式",
        2,
        re.compile(
            r"(?i)\b(?:plays? a (?:vital|crucial|key|pivotal) role"
            r"|serves? as a|stands? as a testament|a testament to"
            r"|in the realm of|a wide range of"
            r"|is designed to (?:provide|ensure|deliver)"
            r"|aims? to (?:provide|ensure|deliver|empower))\b"
        ),
    ),
    Rule(
        "en_banned_words",
        "英文 AI 高頻詞",
        1,
        re.compile(
            r"(?i)\b(?:delv(?:e|es|ed|ing)|leverag(?:e|es|ed|ing)"
            r"|seamless(?:ly)?|robust|comprehensive|crucial|pivotal"
            r"|foster(?:s|ed|ing)?|harness(?:es|ed|ing)?"
            r"|elevat(?:e|es|ed|ing)|streamlin(?:e|es|ed|ing)"
            r"|empower(?:s|ed|ing)?|underscor(?:e|es|ed|ing)"
            r"|boasts?|vibrant|myriad|plethora|game-?changer)\b"
        ),
    ),
]


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def excerpt(text: str, start: int, end: int) -> str:
    left = max(0, start - 24)
    right = min(len(text), end + 24)
    return text[left:right].replace("\n", "\\n")


def mask_meta_and_negative_examples(text: str) -> tuple[str, str]:
    """Mask negative showcase examples (❌ / 改寫前 / AI 版), programming fenced code blocks,
    and meta-mentions of banned terms with spaces of equal length so line numbers remain identical.

    Returns (prose_scan_text, artifact_scan_text).
    """
    lines = text.splitlines(keepends=True)
    prose_lines = []
    artifact_lines = []
    in_negative_quote = False
    in_code_fence = False
    fence_marker = ""
    fence_is_code = False

    neg_header_re = re.compile(
        r"^(?:[-*+]\s*)?❌"
        r"|^(?:[-*+]\s*)?(?:\*\*)?(?:原稿|修改前|改寫前|Before|AI\s*版|AI\s*version)(?:\s*[：:][^。！？\n]*)?(?:\*\*)?\s*[：:]?$"
    )
    meta_cue = re.compile(
        r"(?:受夠了|封殺|砍掉|拔除|清除|根除|禁用|嚴格禁止|嚴禁|禁止|禁詞|禁改|避免|剃除|抓出|專治|不寫|不用|不用詞|不用句型|高頻詞|識別信號|反例|誤殺|放行|殘留|黑話|AI\s*味)"
    )
    quoted_span = re.compile(r"([「『（(][^」』）)\n]+[」』）)]|“[^”\n]+”|\"[^\"\n]+\"|`[^`\n]+`)")
    inline_code_re = re.compile(r"`[^`\n]+`")

    for line in lines:
        stripped = line.lstrip()
        content = line.rstrip("\r\n")
        ending = line[len(content) :]

        fence_match = re.match(r"^(`{3,}|~{3,})(.*)$", stripped)
        if fence_match:
            marker = fence_match.group(1)
            info = fence_match.group(2).strip().lower().split()[0] if fence_match.group(2).strip() else ""
            if not in_code_fence:
                in_code_fence = True
                fence_marker = marker[0]
                fence_is_code = info in CODE_FENCE_LANGS
            elif marker[0] == fence_marker and len(marker) >= 3 and not info:
                in_code_fence = False
                fence_marker = ""
                fence_is_code = False
            prose_lines.append(" " * len(content) + ending if fence_is_code else line)
            artifact_lines.append(line)
            continue

        if in_code_fence and fence_is_code:
            prose_lines.append(" " * len(content) + ending)
            artifact_lines.append(" " * len(content) + ending)
            continue

        if neg_header_re.match(stripped):
            in_negative_quote = True
            blank = " " * len(content) + ending
            prose_lines.append(blank)
            artifact_lines.append(blank)
            continue

        if in_negative_quote:
            if stripped.startswith(">"):
                blank = " " * len(content) + ending
                prose_lines.append(blank)
                artifact_lines.append(blank)
                continue
            elif stripped == "":
                prose_lines.append(line)
                artifact_lines.append(line)
                continue
            else:
                in_negative_quote = False

        artifact_line = content
        prose_line = content

        if meta_cue.search(prose_line):
            prose_line = quoted_span.sub(lambda m: " " * len(m.group(0)), prose_line)
        else:
            # 技術文件內聯反引號中的變數/路徑/參數不應當成英文或大陸用語散文
            prose_line = inline_code_re.sub(lambda m: " " * len(m.group(0)), prose_line)

        prose_lines.append(prose_line + ending)
        artifact_lines.append(artifact_line + ending)

    return "".join(prose_lines), "".join(artifact_lines)


def audit_text(raw_text: str) -> dict:
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    findings = []
    prose_scan_text, artifact_scan_text = mask_meta_and_negative_examples(text)

    for rule in RULES:
        target_text = artifact_scan_text if rule.scan_code_spans else prose_scan_text
        if rule.pattern:
            for match in rule.pattern.finditer(target_text):
                findings.append(
                    {
                        "rule": rule.rule_id,
                        "label": rule.label,
                        "severity": rule.severity,
                        "line": line_number(text, match.start()),
                        "match": match.group(0),
                        "excerpt": excerpt(text, match.start(), match.end()),
                    }
                )
        for term in rule.terms:
            start = 0
            while True:
                idx = target_text.find(term, start)
                if idx < 0:
                    break
                findings.append(
                    {
                        "rule": rule.rule_id,
                        "label": rule.label,
                        "severity": rule.severity,
                        "line": line_number(text, idx),
                        "match": term,
                        "excerpt": excerpt(text, idx, idx + len(term)),
                    }
                )
                start = idx + len(term)

    findings.extend(audit_shape(prose_scan_text))
    findings.sort(key=lambda item: (item["line"], -item["severity"], item["rule"]))
    score = sum(item["severity"] for item in findings)
    blockers = [item for item in findings if item["severity"] >= 3]
    return {
        "score": score,
        "finding_count": len(findings),
        "blocker_count": len(blockers),
        "status": "pass" if not blockers and score <= 2 else "review",
        "findings": findings,
    }


def _strip_urls_and_code(text: str) -> str:
    text = re.sub(r"https?://\S+", lambda m: " " * len(m.group(0)), text)
    text = re.sub(r"`[^`\n]+`", lambda m: " " * len(m.group(0)), text)
    return text


def audit_shape(text: str) -> list[dict]:
    findings: list[dict] = []
    raw_lines = text.splitlines()
    numbered_nonempty = [(i, line.strip()) for i, line in enumerate(raw_lines, start=1) if line.strip()]

    template_prefix = re.compile(
        r"^(?:概念|問題|问题|原因|結論|结论|答案|核心|本質|本质|關鍵|关键|目標|目标|方法|步驟|步骤|"
        r"第一步|第二步|第三步|SOP|"
        r"Hook|Usefulness|Specificity|Trust|Privacy|Tags)"
        r"[：:]"
    )
    colon_lines = [(lineno, line) for lineno, line in numbered_nonempty if template_prefix.match(line)]
    if len(colon_lines) >= 3:
        findings.append(
            {
                "rule": "template_colon",
                "label": "冒號模板重複",
                "severity": 2,
                "line": colon_lines[0][0],
                "match": f"{len(colon_lines)} colon-template lines",
                "excerpt": " / ".join(line for _, line in colon_lines[:3]),
            }
        )

    # 檢查連續 4 行以上「- **小標**：一句話」簡報式列點
    bold_bullet_re = re.compile(r"^(?:[-*+]|\d+\.)\s+\*\*[^*\n]{1,24}\*\*[：:]")
    streak: list[tuple[int, str]] = []
    for lineno, line in enumerate(raw_lines, start=1):
        s = line.strip()
        if bold_bullet_re.match(s):
            streak.append((lineno, s))
        elif s == "":
            continue
        else:
            if len(streak) >= 4:
                findings.append(
                    {
                        "rule": "cookie_cutter_bold_bullets",
                        "label": "簡報式粗體冒號列點過長（建議改為散文或自然敘述）",
                        "severity": 2,
                        "line": streak[0][0],
                        "match": f"{len(streak)} consecutive bold-colon bullets",
                        "excerpt": " / ".join(item[1] for item in streak[:3]),
                    }
                )
            streak = []
    if len(streak) >= 4:
        findings.append(
            {
                "rule": "cookie_cutter_bold_bullets",
                "label": "簡報式粗體冒號列點過長（建議改為散文或自然敘述）",
                "severity": 2,
                "line": streak[0][0],
                "match": f"{len(streak)} consecutive bold-colon bullets",
                "excerpt": " / ".join(item[1] for item in streak[:3]),
            }
        )

    # 檢查「先 A，再 B」是否在同一篇被當成標題／短句模具連刷 4 次以上
    xian_zai_matches = list(re.finditer(r"先[^，。！？\n]{2,18}[，,]\s*再[^，。！？\n]{2,20}", text))
    if len(xian_zai_matches) >= 4:
        first = xian_zai_matches[0]
        findings.append(
            {
                "rule": "cookie_cutter_xian_zai",
                "label": "「先 A，再 B」句型模具過度重複（建議打散句型）",
                "severity": 2,
                "line": line_number(text, first.start()),
                "match": f"{len(xian_zai_matches)} occurrences of '先...再...'",
                "excerpt": " / ".join(m.group(0) for m in xian_zai_matches[:3]),
            }
        )

    # 檢查破折號（——）密度：每 500 字超過 1 次且達 3 次以上
    em_dashes = list(re.finditer(r"——", text))
    char_count = len(re.sub(r"\s+", "", text))
    if len(em_dashes) >= 3 and char_count > 0 and len(em_dashes) > max(1, char_count / 500):
        findings.append(
            {
                "rule": "cookie_cutter_em_dash",
                "label": "破折號（——）密度過高（每 500 字最多 1 次）",
                "severity": 1,
                "line": line_number(text, em_dashes[0].start()),
                "match": f"{len(em_dashes)} em-dashes in {char_count} chars",
                "excerpt": excerpt(text, em_dashes[0].start(), em_dashes[0].end()),
            }
        )

    # 檢查中文語境誤用彎引號 “...” 與半形標點
    clean_punct_text = _strip_urls_and_code(text)
    for m in re.finditer(r"“[^”\n]*[\u4e00-\u9fff][^”\n]*”", clean_punct_text):
        findings.append(
            {
                "rule": "curly_quotes_in_zh",
                "label": "中文誤用彎引號 “ ”（應改用「」）",
                "severity": 1,
                "line": line_number(text, m.start()),
                "match": m.group(0),
                "excerpt": excerpt(text, m.start(), m.end()),
            }
        )

    for m in re.finditer(r"[\u4e00-\u9fff][,;!?:](?:\s*[\u4e00-\u9fff]|$)", clean_punct_text, re.M):
        findings.append(
            {
                "rule": "halfwidth_punct_in_zh",
                "label": "中文句中混用半形標點（應改用全形）",
                "severity": 1,
                "line": line_number(text, m.start()),
                "match": m.group(0),
                "excerpt": excerpt(text, m.start(), m.end()),
            }
        )

    # 段落長度過於均勻（只檢查純散文段落，排除標題、表格、清單、引用、分隔線）
    prose_blocks = []
    for block in re.split(r"\n\s*\n", text):
        lines_in_block = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines_in_block:
            continue
        first_line = lines_in_block[0]
        if first_line.startswith(("#", ">", "|", "-", "*", "+", "---", "```", "~~~")):
            continue
        if re.match(r"^\d+\.\s", first_line):
            continue
        prose_blocks.append(len(re.sub(r"\s+", "", block)))

    medium_lengths = [length for length in prose_blocks if 24 <= length <= 90]
    if len(medium_lengths) >= 5 and max(medium_lengths) - min(medium_lengths) <= 12:
        findings.append(
            {
                "rule": "over_even_paragraph_distribution",
                "label": "段落長度過於均勻（切吐司結構）",
                "severity": 1,
                "line": 1,
                "match": f"paragraph lengths={medium_lengths[:8]}",
                "excerpt": "Vary paragraph weight; over-even distribution looks model-sorted.",
            }
        )

    non_heading_lines = [(lineno, line) for lineno, line in numbered_nonempty if not line.startswith("#")]
    if non_heading_lines:
        final_lineno, final_line = non_heading_lines[-1]
        if final_line.endswith(("？", "?")) and re.search(
            r"你覺得呢|大家覺得呢|是不是很神奇|你也遇過.{0,12}嗎", final_line
        ):
            findings.append(
                {
                    "rule": "ending_engagement_question",
                    "label": "結尾假互動提問",
                    "severity": 3,
                    "line": final_lineno,
                    "match": final_line,
                    "excerpt": final_line,
                }
            )

    return findings


def expand_input_paths(raw_paths: list[str]) -> list[Path]:
    """Expand file paths, globs (for Windows shells), and directories into deduplicated file paths."""
    resolved: list[Path] = []
    seen: set[Path] = set()

    def add_file(p: Path) -> None:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            resolved.append(p)

    for raw in raw_paths:
        if any(ch in raw for ch in "*?["):
            matches = sorted(Path(m) for m in glob.glob(raw, recursive=True))
            if not matches:
                raise FileNotFoundError(f"找不到符合條件的檔案：{raw}")
            for match in matches:
                if match.is_file():
                    add_file(match)
            continue

        path = Path(raw)
        if not path.exists():
            raise FileNotFoundError(f"找不到檔案或資料夾：{raw}")
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and child.suffix.lower() in SCAN_EXTENSIONS:
                    if not any(part in SKIP_DIRS for part in child.parts):
                        add_file(child)
        else:
            add_file(path)

    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit Traditional-Chinese (and English) text for Marketing AI Slop and Reasoning/Forensic Autopsy Slop."
    )
    parser.add_argument("paths", nargs="+", help="Files, directories, or glob patterns to audit")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--fail-on-review", action="store_true", help="Exit 1 if any file needs review")
    args = parser.parse_args()

    try:
        target_paths = expand_input_paths(args.paths)
    except FileNotFoundError as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 2

    if not target_paths:
        print("錯誤：沒有可掃描的檔案。", file=sys.stderr)
        return 2

    results = {}
    failed = False
    for path in target_paths:
        text = path.read_text(encoding="utf-8")
        result = audit_text(text)
        results[str(path)] = result
        failed = failed or result["status"] != "pass"

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for path, result in results.items():
            print(
                f"{path}: {result['status']} score={result['score']} "
                f"findings={result['finding_count']} blockers={result['blocker_count']}"
            )
            for item in result["findings"][:12]:
                print(f"  L{item['line']} [{item['label']}] {item['match']}")
            if len(result["findings"]) > 12:
                print(f"  ... {len(result['findings']) - 12} more")

    return 1 if args.fail_on_review and failed else 0


if __name__ == "__main__":
    sys.exit(main())
