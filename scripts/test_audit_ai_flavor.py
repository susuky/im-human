#!/usr/bin/env python3
"""Unit and regression tests for audit_ai_flavor.py and im-human skill integrity."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

import audit_ai_flavor  # noqa: E402


class AuditTextRulesTests(unittest.TestCase):
    def test_clean_taiwan_prose_passes(self) -> None:
        text = (
            "把快取換成 Redis 之後，首頁查詢的 P99 延遲從 820ms 降到 95ms。\n\n"
            "不過這一步只會減輕讀取壓力；如果遇到秒殺活動那種瞬間大量寫入，資料庫還是會鎖死，"
            "那部分下週要另外接 Kafka 佇列來緩衝。\n"
        )
        res = audit_ai_flavor.audit_text(text)
        self.assertEqual(res["status"], "pass")
        self.assertEqual(res["findings"], [])

    def test_clean_english_prose_passes(self) -> None:
        text = (
            "Redis cuts read latency right away. If you hit write spikes during peak traffic, "
            "pair it with a write queue.\n"
        )
        res = audit_ai_flavor.audit_text(text)
        self.assertEqual(res["status"], "pass")
        self.assertEqual(res["findings"], [])

    def test_detects_second_gen_autopsy_and_defensive_slop(self) -> None:
        text = (
            "提交組的重量未另報。在 02:14 處，畫面左側綠圈標出示範者肩部位置，箭頭指向槓鈴。\n"
            "這只回答了讀取問題，沒有解決寫入鎖死。不能拿分數直接判定實際效果。\n"
            "先記下延遲作為比較基準，再把命中率分開記錄。\n"
        )
        res = audit_ai_flavor.audit_text(text)
        rules = {f["rule"] for f in res["findings"]}
        self.assertEqual(res["status"], "review")
        self.assertIn("clinical_autopsy_register", rules)
        self.assertIn("pixel_caption_reporting", rules)
        self.assertIn("defensive_scope_policing", rules)
        self.assertIn("bookkeeper_verbalization", rules)

    def test_detects_first_gen_marketing_slop_and_english_slop(self) -> None:
        text = (
            "在當今瞬息萬變的時代，這個方案全面賦能團隊，打造價值閉環。\n"
            "It's worth noting that we can leverage this seamless platform.\n"
            "希望這對你有幫助！\n"
        )
        res = audit_ai_flavor.audit_text(text)
        rules = {f["rule"] for f in res["findings"]}
        self.assertIn("trend_opener", rules)
        self.assertIn("inflated_abstract_words", rules)
        self.assertIn("assistant_route_marker", rules)
        self.assertIn("en_throat_clearing", rules)
        self.assertIn("en_banned_words", rules)

    def test_detects_simplified_residue_and_mainland_terms(self) -> None:
        text = "這段代碼在內存裡有錯誤，禁助理開場与客套收尾，還要再標注一下視頻連結。\n"
        res = audit_ai_flavor.audit_text(text)
        rules = {f["rule"] for f in res["findings"]}
        self.assertIn("simplified_chinese_residue", rules)
        self.assertIn("mainland_terms", rules)

    def test_detects_tool_artifacts_even_inside_backticks_and_links(self) -> None:
        text = "報名看這裡：`https://example.com/signup?utm_source=chatgpt.com`。\n"
        res = audit_ai_flavor.audit_text(text)
        rules = {f["rule"] for f in res["findings"]}
        self.assertIn("tool_artifacts", rules)

    def test_no_cross_sentence_binary_contrast_false_positive(self) -> None:
        safe_text = "這不是快取失效造成的。不過從監控圖來看，問題反而是連線池太小。\n"
        res = audit_ai_flavor.audit_text(safe_text)
        rules = {f["rule"] for f in res["findings"]}
        self.assertNotIn("binary_contrast", rules)

    def test_masks_programming_code_fences_but_scans_plain_prompt_fences(self) -> None:
        code_doc = (
            "設定檔說明如下：\n\n"
            "```python\n"
            "def empower_client(robust=True):\n"
            "    return 'seamless'\n"
            "```\n"
        )
        self.assertEqual(audit_ai_flavor.audit_text(code_doc)["findings"], [])

        prompt_doc = "```\n這個方案將賦能所有團隊。\n```\n"
        rules = {f["rule"] for f in audit_ai_flavor.audit_text(prompt_doc)["findings"]}
        self.assertIn("inflated_abstract_words", rules)

    def test_masks_negative_examples(self) -> None:
        doc = (
            "**改寫前**\n\n"
            "> 在當今時代，這賦能了團隊，希望這對你有幫助！\n\n"
            "**改寫後**\n\n"
            "> 這套流程幫團隊每週省下兩小時。\n"
        )
        res = audit_ai_flavor.audit_text(doc)
        self.assertEqual(res["status"], "pass")
        self.assertEqual(res["findings"], [])


class AuditShapeAndCrlfTests(unittest.TestCase):
    def test_crlf_paragraph_uniformity_and_real_line_numbers(self) -> None:
        para = "這是一段長度刻意湊得剛剛好差不多的測試文字，用來驗證機器切吐司式的段落長度偵測有沒有正常運作。"
        text = "\r\n\r\n" + "\r\n\r\n".join([para] * 5) + "\r\n\r\n概念：一\r\n問題：二\r\n結論：三\r\n"
        res = audit_ai_flavor.audit_text(text)
        rules = {f["rule"]: f for f in res["findings"]}
        self.assertIn("over_even_paragraph_distribution", rules)
        self.assertIn("template_colon", rules)
        # Check exact 1-based line number (2 leading blank lines + 5 paras separated by blank lines -> line 13)
        self.assertEqual(rules["template_colon"]["line"], 13)

    def test_bold_colon_bullets_and_punctuation_rules(self) -> None:
        text = (
            "- **設計**：重做介面\n"
            "- **速度**：載入變快\n"
            "- **安全**：補上驗證\n"
            "- **成本**：少花一半\n\n"
            "我後來發現,這是“測試”句子——第一處——第二處——第三處。\n"
        )
        res = audit_ai_flavor.audit_text(text)
        rules = {f["rule"] for f in res["findings"]}
        self.assertIn("cookie_cutter_bold_bullets", rules)
        self.assertIn("halfwidth_punct_in_zh", rules)
        self.assertIn("curly_quotes_in_zh", rules)
        self.assertIn("cookie_cutter_em_dash", rules)


class CliAndRepoIntegrityTests(unittest.TestCase):
    def test_cli_glob_and_fail_on_review_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            clean_file = tmp_dir / "clean.md"
            dirty_file = tmp_dir / "dirty.md"
            clean_file.write_text("這裡只改了連線池設定，延遲降到 90ms。\n", encoding="utf-8")
            dirty_file.write_text("在當今時代，這賦能了系統。\n", encoding="utf-8")

            ok = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / "audit_ai_flavor.py"), str(clean_file), "--fail-on-review", "--json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(ok.returncode, 0)
            parsed = json.loads(ok.stdout)
            self.assertEqual(parsed[str(clean_file)]["status"], "pass")

            bad = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / "audit_ai_flavor.py"), str(tmp_dir / "*.md"), "--fail-on-review"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(bad.returncode, 1)

            missing = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / "audit_ai_flavor.py"), str(tmp_dir / "nonexistent.md")],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(missing.returncode, 2)

    def test_repo_readme_passes_and_links_exist(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        res = audit_ai_flavor.audit_text(readme)
        self.assertEqual(res["status"], "pass", msg=f"README findings: {res['findings']}")

        # Check custom instructions prompt body fits <= 1500 chars
        ci_text = (REPO_ROOT / "prompts" / "chatgpt-custom-instructions.md").read_text(encoding="utf-8")
        body = ci_text.split("```\n", 1)[1].rsplit("\n```", 1)[0]
        self.assertLessEqual(len(body), 1500)

        # Check every relative markdown link in all markdown files resolves cleanly
        import re

        for md_file in REPO_ROOT.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", content):
                target = m.group(1)
                if target.startswith(("http://", "https://")):
                    continue
                target_path = target.split("#")[0]
                if not target_path:
                    continue
                resolved = (md_file.parent / target_path).resolve()
                self.assertTrue(
                    resolved.exists(),
                    msg=f"Broken link in {md_file.relative_to(REPO_ROOT)}: {target}",
                )


if __name__ == "__main__":
    unittest.main()
