"""Synthetic SOP exports with reordered business and credential columns; no real data."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'


def fixture(path, source_layout):
    headers = {'A': '技能名称', 'W': '消耗token预估'}
    values = {'A': 'Synthetic skill', 'W': '100'}
    if source_layout:
        headers.update(I='技能包链接', J='自建技能包（产品上传）', K='技能code', Z='技能来源', AA='appkey', AB='appsecret', AE='同步状态')
        values.update(I='Source ZIP', J='product.zip', K='sample', Z='synthetic-business-source', AA='SYNTHETIC_KEY_ONLY', AB='SYNTHETIC_SECRET_ONLY', AE='待同步')
        link_column = 'I'
    else:
        headers.update(H='技能包链接', I='自建技能包', J='技能code', Z='appkey', AA='appsecret', AD='同步状态')
        values.update(H='Source ZIP', I='product.zip', J='sample', Z='SYNTHETIC_KEY_ONLY', AA='SYNTHETIC_SECRET_ONLY', AD='待同步')
        link_column = 'H'
    strings = []
    root = ET.Element('worksheet', xmlns=NS)
    data = ET.SubElement(root, 'sheetData')
    for number, cells in [(1, headers), (2, values)]:
        row = ET.SubElement(data, 'row', r=str(number))
        for column, text in cells.items():
            index = len(strings)
            strings.append(text)
            cell = ET.SubElement(row, 'c', r=column + str(number), t='s')
            ET.SubElement(cell, 'v').text = str(index)
            if number == 2 and column == link_column:
                ET.SubElement(cell, 'f').text = 'HYPERLINK("https://public.example.test/source.zip","Source ZIP")'
    shared = ET.Element('sst', xmlns=NS)
    for text in strings:
        ET.SubElement(ET.SubElement(shared, 'si'), 't').text = text
    with zipfile.ZipFile(path, 'w') as archive:
        archive.writestr('xl/worksheets/sheet2.xml', ET.tostring(root))
        archive.writestr('xl/sharedStrings.xml', ET.tostring(shared))
        archive.writestr('[Content_Types].xml', '<Types/>')
        archive.writestr('xl/_rels/workbook.xml.rels', '<Relationships/>')


class HeaderRedactionTest(unittest.TestCase):
    def check_layout(self, source_layout):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'export.xlsx'
            fixture(path, source_layout)
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/redact_feishu_export.py'), str(path)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            rows = json.loads(path.with_suffix('.json').read_text())
            self.assertEqual(rows[1]['source_url'], 'https://public.example.test/source.zip')
            self.assertEqual(rows[1]['W'], '100')
            self.assertEqual(rows[1]['J' if source_layout else 'I'], 'product.zip')
            secrets = {'AA', 'AB'} if source_layout else {'Z', 'AA'}
            self.assertFalse(secrets.intersection(rows[1]))
            if source_layout:
                self.assertEqual(rows[1]['Z'], 'synthetic-business-source')
            with zipfile.ZipFile(path) as archive:
                content = b'\n'.join(archive.read(name) for name in archive.namelist())
            self.assertNotIn(b'SYNTHETIC_KEY_ONLY', content)
            self.assertNotIn(b'SYNTHETIC_SECRET_ONLY', content)
            self.assertNotIn('SYNTHETIC_SECRET_ONLY', path.with_suffix('.json').read_text())

    def test_original_product_upload_layout_is_redacted_by_header(self):
        self.check_layout(True)

    def test_existing_atp_layout_retains_credential_and_url_guards(self):
        self.check_layout(False)


if __name__ == '__main__':
    unittest.main()
