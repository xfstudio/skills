"""Synthetic original/ATP tables keep business ID separate from formal skillCode."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('redactor', ROOT / 'scripts/redact_feishu_export.py')
REDACTOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REDACTOR)


class DistinctBusinessCodes(unittest.TestCase):
    def test_original_business_identifier_and_formal_code_are_distinct(self):
        headers = {'A': '技能名称', 'C': '技能编码', 'I': '技能包链接',
                   'J': '自建技能包（产品上传）', 'K': '技能code',
                   'Z': '技能来源', 'AA': 'appkey', 'AB': 'appsecret', 'AE': '同步状态'}
        self.assertEqual(REDACTOR.sheet_layout(headers), ('I', {'AA', 'AB'}))

    def test_atp_business_identifier_and_formal_code_are_distinct(self):
        headers = {'A': '技能名称', 'C': '技能编码', 'H': '技能包链接',
                   'I': '自建技能包', 'J': '技能code',
                   'Z': 'appkey', 'AA': 'appsecret', 'AD': '同步状态'}
        self.assertEqual(REDACTOR.sheet_layout(headers), ('H', {'Z', 'AA'}))

    def test_two_formal_codes_remain_ambiguous(self):
        headers = {'A': '技能名称', 'C': '技能编码', 'H': '技能包链接',
                   'I': '自建技能包', 'J': '技能code', 'K': '技能 code',
                   'Z': 'appkey', 'AA': 'appsecret', 'AD': '同步状态'}
        with self.assertRaisesRegex(RuntimeError, 'Ambiguous'):
            REDACTOR.sheet_layout(headers)


if __name__ == '__main__':
    unittest.main()
