"""Exercise BM-root discovery with isolated public fixtures; no live services."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"bm_preflight.py"
FILES={
 "management_routes":"bm-integration/deployment/single_database/management_routes.py",
 "employee_contract":"bm-integration/deployment/single_database/employee_contract.py",
 "verified_sources":"services/feishu-sop-oss-sync/verified_sources.py",
}

class Discovery(unittest.TestCase):
 def run_probe(self,root):
  run=subprocess.run([sys.executable,str(SCRIPT),"--project-root",str(root)],capture_output=True,text=True)
  self.assertIn(run.returncode,(0,2),run.stderr)
  return run.returncode,json.loads(run.stdout)
 def populate(self,root):
  for relative in FILES.values():
   path=root/relative
   path.parent.mkdir(parents=True,exist_ok=True)
   path.write_text("# isolated fixture\n")
 def test_parent_and_octop_entrypoints(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);octop=root/"bm-ai-octop";self.populate(octop)
   before=sorted(str(p.relative_to(root)) for p in root.rglob("*"))
   for entry in (root,octop):
    code,data=self.run_probe(entry)
    self.assertEqual(code,0,data)
    self.assertEqual(Path(data["octop_root"]),octop.resolve())
    for key,relative in FILES.items():
     self.assertEqual(Path(data["sources"][key]),(octop/relative).resolve())
    self.assertEqual(data["runtime_verified"],False)
   self.assertEqual(before,sorted(str(p.relative_to(root)) for p in root.rglob("*")))
 def test_missing_root_is_not_replaced_by_current_checkout(self):
  with tempfile.TemporaryDirectory() as tmp:
   code,data=self.run_probe(Path(tmp)/"missing")
   self.assertEqual(code,2);self.assertEqual(data["status"],"unavailable")
   self.assertIsNone(data["octop_root"]);self.assertFalse(data["runtime_verified"])
 def test_ambiguous_roots_stop(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);self.populate(root);self.populate(root/"bm-ai-octop")
   code,data=self.run_probe(root)
   self.assertEqual(code,2);self.assertEqual(data["status"],"ambiguous")
 def test_incomplete_sources_are_reported(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);self.populate(root)
   (root/FILES["verified_sources"]).unlink()
   code,data=self.run_probe(root)
   self.assertEqual(code,2);self.assertEqual(data["status"],"partial")
   self.assertIsNone(data["sources"]["verified_sources"])

if __name__=="__main__":unittest.main()
