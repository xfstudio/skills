"""Synthetic inlineStr exports keep business IDs and formal codes as separate columns."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
KEY = "SYNTHETIC_PRIVATE_KEY"
SECRET = "SYNTHETIC_PRIVATE_SECRET"


def write_workbook(path, source, fallback=False, duplicate_formal=False):
    headers = {"A": "技能名称", "C": "技能编码", "W": "消耗token预估"}
    values = {"A": "Synthetic skill", "C": "business-id-42", "W": "250"}
    if source:
        headers.update(I="技能包链接", J="自建技能包（产品上传）", K="技能code",
                       Z="技能来源", AA="appkey", AB="appsecret", AE="同步状态")
        values.update(I="Source ZIP", J="product.zip", K="formal-skill-code",
                      Z="synthetic-business-source", AA=KEY, AB=SECRET, AE="待同步")
        link, upload, formal, credentials = "I", "J", "K", {"AA", "AB"}
    else:
        headers.update(H="技能包链接", I="自建技能包", J="技能code",
                       Z="appkey", AA="appsecret", AD="同步状态")
        values.update(H="Source ZIP", I="product.zip", J="formal-skill-code",
                      Z=KEY, AA=SECRET, AD="待同步")
        link, upload, formal, credentials = "H", "I", "J", {"Z", "AA"}
    if fallback:
        headers.pop(formal)
        values.pop(formal)
    if duplicate_formal:
        headers["L"] = "技能 code"
        values["L"] = "other-formal-code"
    root = ET.Element("worksheet", xmlns=NS)
    data = ET.SubElement(root, "sheetData")
    for number, cells in [(1, headers), (2, values)]:
        row = ET.SubElement(data, "row", r=str(number))
        for column, text in cells.items():
            cell = ET.SubElement(row, "c", r=column + str(number), t="inlineStr")
            ET.SubElement(ET.SubElement(cell, "is"), "t").text = text
            if number == 2 and column == link:
                ET.SubElement(cell, "f").text = 'HYPERLINK("https://public.example.test/source.zip","Source ZIP")'
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("xl/worksheets/sheet1.xml", ET.tostring(root))
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr("xl/_rels/workbook.xml.rels", "<Relationships/>")
    return link, upload, formal, credentials


class InlineDistinctCodes(unittest.TestCase):
    def invoke(self, path):
        return subprocess.run([sys.executable, str(ROOT / "scripts/redact_feishu_export.py"), str(path)],
                              text=True, capture_output=True, timeout=20)

    def test_source_and_atp_inline_exports_preserve_both_codes_and_remove_credentials(self):
        for source in [True, False]:
            with self.subTest(source=source), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "synthetic.xlsx"
                _, upload, formal, credentials = write_workbook(path, source)
                with zipfile.ZipFile(path) as archive:
                    self.assertNotIn("xl/sharedStrings.xml", archive.namelist())
                result = self.invoke(path)
                self.assertEqual(result.returncode, 0, result.stderr)
                rows = json.loads(path.with_suffix(".json").read_text())
                self.assertEqual(rows[1]["C"], "business-id-42")
                self.assertEqual(rows[1][formal], "formal-skill-code")
                self.assertEqual(rows[1][upload], "product.zip")
                self.assertEqual(rows[1]["W"], "250")
                self.assertEqual(rows[1]["source_url"], "https://public.example.test/source.zip")
                self.assertFalse(credentials.intersection(rows[1]))
                if source:
                    self.assertEqual(rows[1]["Z"], "synthetic-business-source")
                with zipfile.ZipFile(path) as archive:
                    for name in archive.namelist():
                        content = archive.read(name)
                        self.assertNotIn(KEY.encode(), content)
                        self.assertNotIn(SECRET.encode(), content)
                        ET.fromstring(content)
                self.assertNotIn(KEY, path.with_suffix(".json").read_text())
                self.assertNotIn(SECRET, path.with_suffix(".json").read_text())

    def test_business_label_remains_fallback_when_formal_label_is_absent(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.xlsx"
            write_workbook(path, source=False, fallback=True)
            result = self.invoke(path)
            self.assertEqual(result.returncode, 0, result.stderr)
            row = json.loads(path.with_suffix(".json").read_text())[1]
            self.assertEqual(row["C"], "business-id-42")
            self.assertNotIn("J", row)
            self.assertNotIn("Z", row)
            self.assertNotIn("AA", row)

    def test_actual_duplicate_formal_headers_still_fail_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.xlsx"
            write_workbook(path, source=True, duplicate_formal=True)
            before = path.read_bytes()
            result = self.invoke(path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Ambiguous", result.stderr)
            self.assertEqual(path.read_bytes(), before)
            self.assertFalse(path.with_suffix(".json").exists())
            self.assertFalse(path.with_suffix(".redacted.tmp").exists())


if __name__ == "__main__":
    unittest.main()
