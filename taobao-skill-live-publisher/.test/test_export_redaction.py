"""Credential-column removal must also remove unreferenced XLSX shared strings."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

class ExportRedaction(unittest.TestCase):
    def test_shared_credentials_do_not_survive_in_any_zip_entry(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'table.xlsx'
            namespace='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
            sheet=f'''<worksheet xmlns="{namespace}"><sheetData>
<row r="1"><c r="A1" t="inlineStr"><is><t>技能名称</t></is></c><c r="AD1" t="inlineStr"><is><t>同步状态</t></is></c></row>
<row r="2"><c r="A2" t="s"><v>2</v></c><c r="Z2" t="s"><v>0</v></c><c r="AA2" t="s"><v>1</v></c></row>
</sheetData></worksheet>'''
            with zipfile.ZipFile(path,'w') as z:
                z.writestr('xl/worksheets/sheet1.xml',sheet)
                z.writestr('xl/sharedStrings.xml',f'<sst xmlns="{namespace}"><si><t>SYNTHETIC_KEY_DO_NOT_KEEP</t></si><si><t>SYNTHETIC_SECRET_DO_NOT_KEEP</t></si><si><t>Public skill</t></si></sst>')
                z.writestr('[Content_Types].xml','<Types><Override PartName="/xl/sharedStrings.xml"/></Types>')
                z.writestr('xl/_rels/workbook.xml.rels','<Relationships><Relationship Target="sharedStrings.xml"/></Relationships>')
            script=Path(__file__).resolve().parents[1]/'scripts/redact_feishu_export.py'
            result=subprocess.run([sys.executable,str(script),str(path)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            with zipfile.ZipFile(path) as z:
                self.assertNotIn('xl/sharedStrings.xml',z.namelist())
                for name in z.namelist():self.assertNotIn(b'SYNTHETIC_',z.read(name))
            rows=json.loads(path.with_suffix('.json').read_text())
            self.assertEqual(rows[1],{'A':'Public skill'})

if __name__=='__main__':unittest.main()
