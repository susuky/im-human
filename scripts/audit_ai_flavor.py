#!/usr/bin/env python3
"""AI 味回歸掃描（v2）：同時抓出「第一代行銷小編套話」與「第二代推論／代理模型的法醫驗屍報告腔、防禦免責腔、監視器看圖報時腔、記帳員官僚腔」。

結果只作提示，不取代編輯判斷——禁詞表本身、引用原話、技術術語命中都屬誤殺。
注意：本腳本鼓勵教學與操作文自然使用「你」與讀者對話，不再將「你」計入違規。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows 主控台預設非 UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


@dataclass(frozen=True)
class Rule:
    rule_id: str
    label: str
    severity: int
    pattern: re.Pattern[str] | None = None
    terms: tuple[str, ...] = ()


RULES = [
    # ---- 第二代推論／代理模型重災區：驗屍報告、防禦免責、監視器看圖、病歷表、記帳腔 ----
    Rule(
        "defensive_scope_policing",
        "防禦性免責與範圍切割腔（只回答了／是兩碼事／不能單靠）",
        3,
        re.compile(
            r"只回答了[^。！？\n]{1,30}(?:沒有|並未|沒能|不代表)"
            r"|是兩(?:個|件|種)不同的(?:動作|事|問題|機制|概念)"
            r"|不能混為一談|不可混為一談"
            r"|(?:單靠|僅靠)[^，。！？\n]{1,20}(?:並不能|無法|不能)(?:保證|解決|取代)"
            r"|這並不是萬靈丹"
        ),
    ),
    Rule(
        "clinical_autopsy_register",
        "法醫／病歷表抽離稱謂與筆錄開頭（受試者／示範者／未另報）",
        3,
        re.compile(
            r"受試者|(?<!沒有)示範者|協助者"
            r"|未另報|工作重量未標示|來源未標示"
        ),
    ),
    Rule(
        "pixel_caption_reporting",
        "監視器看圖報時腔（綠圈標出／紅框圈出／在 02:14 處畫面）",
        3,
        re.compile(
            r"(?:綠圈|紅圈|黃圈|藍圈|綠框|紅框|黃框|綠線|紅線|黃線)(?:標出|圈出|標示出|畫出)"
            r"|在\s*\d{1,2}:\d{2}\s*處[，,]?\s*(?:畫面|鏡頭|講者)"
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
            r"(?:不是|並非|并非|不在於|不在于|不只是|不止是|不僅是|不仅是).{0,32}"
            r"(?:而是|而在於|而在于|更是)"
            r"|與其說.{0,32}不如說|与其说.{0,32}不如说"
        ),
    ),
    Rule(
        "essence_claim",
        "真正／本質／核心式拔高",
        3,
        re.compile(
            r"真正.{0,24}(?:的是|在於|在于|決定|决定|重要|打動|打动|改變|改变)"
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
        "mainland_terms",
        "中國大陸用語殘留（應改為台灣繁中慣用詞）",
        2,
        terms=(
            "視頻", "视频",
            "軟件", "软件",
            "硬件",
            "信息",
            "數據庫", "数据库",
            "服務器", "服务器",
            "屏幕",
            "鼠標", "鼠标",
            "默認", "默认",
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
            r"(?:基於|基于|依據|依据).{0,18}(?:理論|理论|框架)"
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


def mask_meta_and_negative_examples(text: str) -> str:
    """Mask negative showcase examples (❌ / 原稿 blockquotes) and meta-mentions of banned terms
    with spaces of equal length so line numbers remain identical."""
    lines = text.splitlines(keepends=True)
    masked_lines = []
    in_negative_quote = False
    meta_cue = re.compile(
        r"(?:受夠了|封殺|砍掉|拔除|清除|根除|禁用|嚴格禁止|避免|剃除|抓出|專治|不寫|不用|不用詞|不用句型|高頻詞)"
    )
    quoted_span = re.compile(r"([「『（(][^」』）)\n]+[」』）)]|`[^`\n]+`)")

    for line in lines:
        stripped = line.lstrip()
        content = line.rstrip("\r\n")
        ending = line[len(content) :]

        if re.match(r"^(?:[-*+]\s*)?❌|(?:[-*+]\s*)?(?:原稿|修改前|Before)\s*[：:]", stripped):
            in_negative_quote = True
            masked_lines.append(" " * len(content) + ending)
            continue

        if in_negative_quote:
            if stripped.startswith(">"):
                masked_lines.append(" " * len(content) + ending)
                continue
            elif stripped == "":
                masked_lines.append(line)
                continue
            else:
                in_negative_quote = False

        if meta_cue.search(content):
            content = quoted_span.sub(lambda m: " " * len(m.group(0)), content)

        masked_lines.append(content + ending)

    return "".join(masked_lines)


def audit_text(text: str) -> dict:
    findings = []
    scan_text = mask_meta_and_negative_examples(text)

    for rule in RULES:
        if rule.pattern:
            for match in rule.pattern.finditer(scan_text):
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
                idx = scan_text.find(term, start)
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

    findings.extend(audit_shape(scan_text))
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


def audit_shape(text: str) -> list[dict]:
    findings: list[dict] = []
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    template_prefix = re.compile(
        r"^(?:概念|問題|问题|原因|結論|结论|答案|核心|本質|本质|關鍵|关键|目標|目标|方法|步驟|步骤|"
        r"第一步|第二步|第三步|SOP|"
        r"Hook|Usefulness|Specificity|Trust|Privacy|Tags)"
        r"[：:]"
    )
    colon_lines = []
    for i, line in enumerate(lines, start=1):
        if template_prefix.match(line):
            colon_lines.append((i, line))
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

    paragraph_lengths = [
        len(re.sub(r"\s+", "", line))
        for line in text.split("\n\n")
        if line.strip() and not line.strip().startswith("#")
    ]
    medium_lengths = [length for length in paragraph_lengths if 24 <= length <= 90]
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

    final_line = next((line for line in reversed(lines) if not line.startswith("#")), "")
    if final_line.endswith(("？", "?")) and re.search(
        r"你覺得呢|大家覺得呢|是不是很神奇|你也遇過.{0,12}嗎", final_line
    ):
        findings.append(
            {
                "rule": "ending_engagement_question",
                "label": "結尾假互動提問",
                "severity": 3,
                "line": max(1, len(text.splitlines())),
                "match": final_line,
                "excerpt": final_line,
            }
        )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit Traditional-Chinese (and English) text for Marketing AI Slop and Reasoning/Forensic Autopsy Slop."
    )
    parser.add_argument("paths", nargs="+", help="Markdown, JSON, or text files to audit")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--fail-on-review", action="store_true", help="Exit 1 if any file needs review")
    args = parser.parse_args()

    results = {}
    failed = False
    for raw_path in args.paths:
        path = Path(raw_path)
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
