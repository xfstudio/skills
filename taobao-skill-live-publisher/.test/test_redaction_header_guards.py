"""Independent synthetic guards for header-directed redaction and pre-decode refusal."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("redactor", ROOT / "scripts/redact_feishu_export.py")
REDACTOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REDACTOR)
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
SECRET_KEY = "SYNTHETIC_PRIVATE_KEY"
SECRET_VALUE = "SYNTHETIC_PRIVATE_SECRET"


def workbook(path, layouts=("reordered",), inline_credentials=False, invalid_credential_index=False):
    strings = [SECRET_KEY, SECRET_VALUE]

    def shared_cell(row, reference, text=None, index=None):
        if index is None:
            index = len(strings)
            strings.append(text)
        cell = ET.SubElement(row, "c", r=reference, t="s")
        ET.SubElement(cell, "v").text = str(index)
        return cell

    sheets = {}
    for number, layout in enumerate(layouts, 1):
        headers = {"B": "技能名称", "C": "同步状态", "D": "技能包链接", "E": "自建技能包（产品上传）",
                   "F": "技能code", "M": "APP KEY", "N": "App_Secret", "W": "消耗token预估",
                   "X": "token预算", "Z": "技能来源"}
        if layout == "unknown":
            headers = {"A": "技能名称", "B": "同步状态"}
        elif layout == "duplicate":
            headers["O"] = "appkey"
        root = ET.Element("worksheet", xmlns=NS)
        data = ET.SubElement(root, "sheetData")
        row = ET.SubElement(data, "row", r="1")
        for column, text in headers.items():
            shared_cell(row, column + "1", text=text)
        row = ET.SubElement(data, "row", r="2")
        for column, text in {"B": "Synthetic skill", "C": "待同步", "E": "product.zip", "F": "sample-code",
                             "W": "100", "X": "200", "Z": "synthetic-business-source"}.items():
            shared_cell(row, column + "2", text=text)
        link = shared_cell(row, "D2", text="Public package")
        ET.SubElement(link, "f").text = 'HYPERLINK("https://public.example.test/pkg.zip","Public package")'
        # A credential shared-string reused outside its credential column must not leak.
        shared_cell(row, "P2", index=0)
        for column, index, text in [("M", 0, SECRET_KEY), ("N", 1, SECRET_VALUE)]:
            if inline_credentials:
                cell = ET.SubElement(row, "c", r=column + "2", t="inlineStr")
                ET.SubElement(ET.SubElement(cell, "is"), "t").text = text
            else:
                shared_cell(row, column + "2", index=999999 if invalid_credential_index else index)
        sheets[f"xl/worksheets/sheet{number}.xml"] = ET.tostring(root)
    shared = ET.Element("sst", xmlns=NS)
    for text in strings:
        ET.SubElement(ET.SubElement(shared, "si"), "t").text = text
    with zipfile.ZipFile(path, "w") as archive:
        for name, data in sheets.items():
            archive.writestr(name, data)
        archive.writestr("xl/sharedStrings.xml", ET.tostring(shared))
        archive.writestr("[Content_Types].xml", '<Types><Override PartName="/xl/sharedStrings.xml"/></Types>')
        archive.writestr("xl/_rels/workbook.xml.rels", '<Relationships><Relationship Target="sharedStrings.xml"/></Relationships>')


class HeaderGuards(unittest.TestCase):
    def assert_no_credentials(self, path):
        with zipfile.ZipFile(path) as archive:
            self.assertNotIn("xl/sharedStrings.xml", archive.namelist())
            for name in archive.namelist():
                data = archive.read(name)
                self.assertNotIn(SECRET_KEY.encode(), data)
                self.assertNotIn(SECRET_VALUE.encode(), data)
                if name.endswith(".xml"):
                    ET.fromstring(data)
        rows = json.loads(path.with_suffix(".json").read_text())
        self.assertEqual(rows[1]["source_url"], "https://public.example.test/pkg.zip")
        self.assertEqual(rows[1]["E"], "product.zip")
        self.assertEqual(rows[1]["W"], "100")
        self.assertEqual(rows[1]["X"], "200")
        self.assertEqual(rows[1]["Z"], "synthetic-business-source")
        self.assertNotIn("M", rows[1])
        self.assertNotIn("N", rows[1])
        return rows

    def test_reordered_headers_and_reused_secret_index_never_decode_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.xlsx"
            workbook(path)
            original = REDACTOR.SharedStrings.__getitem__
            decoded = []

            def public_only(instance, index):
                self.assertNotIn(index, {0, 1}, "Credential string reached text resolution")
                decoded.append(index)
                return original(instance, index)

            with patch.object(REDACTOR.SharedStrings, "__getitem__", public_only):
                REDACTOR.redact(path)
            rows = self.assert_no_credentials(path)
            self.assertNotIn("P", rows[1])
            self.assertTrue(decoded)

    def test_inline_credentials_are_removed_before_cell_decoder(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.xlsx"
            workbook(path, inline_credentials=True)
            # The shared index alias is still credential material, so use a direct
            # credential-column reference as well to establish its tainted index.
            with zipfile.ZipFile(path) as archive:
                entries = {name: archive.read(name) for name in archive.namelist()}
            root = ET.fromstring(entries["xl/worksheets/sheet1.xml"])
            row = root.find(f".//{{{NS}}}row[@r='2']")
            third = ET.SubElement(root.find(f"{{{NS}}}sheetData"), f"{{{NS}}}row", r="3")
            alias = ET.SubElement(third, f"{{{NS}}}c", r="M3", t="s")
            ET.SubElement(alias, f"{{{NS}}}v").text = "0"
            entries["xl/worksheets/sheet1.xml"] = ET.tostring(root)
            with zipfile.ZipFile(path, "w") as archive:
                for name, data in entries.items():
                    archive.writestr(name, data)
            original = REDACTOR.cell_text

            def public_only(cell, shared):
                self.assertNotIn(cell.get("r"), {"M2", "N2", "M3"})
                return original(cell, shared)

            with patch.object(REDACTOR, "cell_text", public_only):
                REDACTOR.redact(path)
            self.assert_no_credentials(path)

    def test_inline_credential_body_never_reaches_xml_text_decoder(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.xlsx"
            workbook(path, inline_credentials=True)
            with zipfile.ZipFile(path) as archive:
                entries = {name: archive.read(name) for name in archive.namelist()}
            root = ET.fromstring(entries["xl/worksheets/sheet1.xml"])
            row = root.find(f".//{{{NS}}}row[@r='2']")
            row.remove(row.find(f"{{{NS}}}c[@r='P2']"))
            entries["xl/worksheets/sheet1.xml"] = ET.tostring(root)
            with zipfile.ZipFile(path, "w") as archive:
                for name, data in entries.items():
                    archive.writestr(name, data)
            original = REDACTOR.ET.fromstring

            def public_xml_only(raw, *args, **kwargs):
                self.assertNotIn(SECRET_KEY.encode(), raw)
                self.assertNotIn(SECRET_VALUE.encode(), raw)
                return original(raw, *args, **kwargs)

            with patch.object(REDACTOR.ET, "fromstring", public_xml_only):
                REDACTOR.redact(path)
            self.assert_no_credentials(path)

    def test_credential_shared_index_is_not_resolved_even_when_out_of_range(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.xlsx"
            workbook(path, invalid_credential_index=True)
            # Remove the unrelated public alias; this test targets the skipped cells.
            with zipfile.ZipFile(path) as archive:
                entries = {name: archive.read(name) for name in archive.namelist()}
            root = ET.fromstring(entries["xl/worksheets/sheet1.xml"])
            row = root.find(f".//{{{NS}}}row[@r='2']")
            row.remove(row.find(f"{{{NS}}}c[@r='P2']"))
            entries["xl/worksheets/sheet1.xml"] = ET.tostring(root)
            with zipfile.ZipFile(path, "w") as archive:
                for name, data in entries.items():
                    archive.writestr(name, data)
            REDACTOR.redact(path)
            self.assert_no_credentials(path)

    def test_unknown_multiple_and_ambiguous_sop_fail_before_body_or_file_mutation(self):
        for layouts in [("unknown",), ("reordered", "reordered"), ("duplicate",)]:
            with self.subTest(layouts=layouts), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "synthetic.xlsx"
                workbook(path, layouts)
                before = path.read_bytes()
                json_path = path.with_suffix(".json")
                json_path.write_text("prior output stays untouched")
                original = REDACTOR.cell_text

                def header_only(cell, shared):
                    self.assertTrue(cell.get("r", "").endswith("1"), "Body decoded before SOP selection")
                    return original(cell, shared)

                with patch.object(REDACTOR, "cell_text", header_only), self.assertRaises(RuntimeError):
                    REDACTOR.redact(path)
                self.assertEqual(path.read_bytes(), before)
                self.assertEqual(json_path.read_text(), "prior output stays untouched")
                self.assertFalse(path.with_suffix(".redacted.tmp").exists())

    def test_expat_character_callback_only_receives_shared_string_indices(self):
        raw = f'<worksheet xmlns="{NS}"><sheetData><row r="1"><c r="A1" t="s"><v>7</v></c></row><row r="2"><c r="M2" t="inlineStr"><is><t>{SECRET_KEY}</t></is></c><c r="N2" t="str"><v>{SECRET_VALUE}</v></c><c r="B2" t="s"><v>8</v></c><c r="P2"><v>123</v></c></row></sheetData></worksheet>'.encode()
        original = REDACTOR.expat.ParserCreate
        observed = []
        test = self

        class ParserProbe:
            def __init__(self, *args, **kwargs):
                object.__setattr__(self, "parser", original(*args, **kwargs))

            def __getattr__(self, name):
                return getattr(self.parser, name)

            def __setattr__(self, name, value):
                if name == "CharacterDataHandler" and value is not None:
                    callback = value

                    def record_index(text):
                        test.assertTrue(text.isascii() and text.isdigit(), "Non-index body reached Expat character callback")
                        observed.append(text)
                        callback(text)

                    value = record_index
                setattr(self.parser, name, value)

        with patch.object(REDACTOR.expat, "ParserCreate", ParserProbe):
            worksheet = REDACTOR.Worksheet(raw)
        self.assertEqual(observed, ["7", "8"])
        self.assertEqual([cell["index"] for cell in worksheet.cells], [7, None, None, 8, None])

    def test_lazy_shared_strings_preserve_prefixed_rich_text_and_empty_entries(self):
        raw = f'<x:sst xmlns:x="{NS}" hint="a > b"><x:si/><x:si><x:r><x:t>Public </x:t></x:r><x:r><x:t>text</x:t></x:r></x:si></x:sst>'.encode()
        strings = REDACTOR.SharedStrings(raw)
        self.assertEqual(strings[0], "")
        self.assertEqual(strings[1], "Public text")


if __name__ == "__main__":
    unittest.main()
