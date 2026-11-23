"""Offline contract and package invariants; never execute catalog examples."""

import hashlib
import json
from pathlib import Path
import shlex
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_batch import build_one, read_archive
from mcp_catalog import example_params, invoke_command, join_segments, schema_parameters, validate


class CatalogContracts(unittest.TestCase):
    def test_complete_unicode_segments_and_missing_segment_rejection(self):
        text = json.dumps([{"参数名": "名称", "类型": "string", "必填": True}], ensure_ascii=False)
        cut = len(text) // 2
        rows = [
            {"A": "MCP编码", "B": "字段", "C": "分段序号", "D": "总分段数", "E": "内容"},
            {"A": "tool_abc1234567", "B": "请求参数", "C": "2", "D": "2", "E": text[cut:]},
            {"A": "tool_abc1234567", "B": "请求参数", "C": "1", "D": "2", "E": text[:cut]},
        ]
        self.assertEqual(join_segments({"details": rows})[("tool_abc1234567", "请求参数")], text)
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            join_segments({"details": rows[:2]})

    def test_nested_required_and_array_types_are_not_flattened(self):
        parameters = [{"参数名": "param1", "类型": "object", "必填": True, "子参数": [
            {"参数名": "ids", "类型": "array", "必填": True, "数组元素": {"类型": "string"}},
        ]}]
        schema = schema_parameters(parameters)
        self.assertEqual(validate({"param1": {"ids": ["100"]}}, schema), [])
        self.assertEqual(validate({"param1": {}}, schema)[0]["path"], "$.param1.ids")
        self.assertEqual(validate({"param1": {"ids": [100]}}, schema)[0]["reason"], "type_mismatch")

    def test_shell_example_roundtrip_keeps_payload_literal(self):
        payload = {"name": "shop's $(touch do-not-run); `no`", "nested": {"ids": ["1"]}}
        command = invoke_command("tool_abc1234567", "0.0.7", payload)
        words = shlex.split(command)
        self.assertEqual(words[:6], ["atp", "invoke", "--code", "tool_abc1234567", "--version", "0.0.7"])
        self.assertEqual(json.loads(words[-1]), payload)
        self.assertEqual(example_params(command, "tool_abc1234567", "0.0.7"), payload)

    def test_source_annotation_and_wrong_pinned_version(self):
        command = "atp invoke --code tool_abc1234567 --version 0.0.1 --params '{}'（示例参数，未实调）"
        self.assertEqual(example_params(command, "tool_abc1234567", "0.0.1"), {})
        with self.assertRaisesRegex(ValueError, "does not match"):
            example_params(command, "tool_abc1234567", "0.0.2")


class ReviewedPackage(unittest.TestCase):
    def test_rebuild_preserves_business_files_and_blocks_changed_base(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            package = root / "reviewed.zip"
            mapping = {"skill": "sample", "operations": {"read_item": {"codes": ["tool_abc1234567"], "notes": ["仅查询本店商品。字段为mappingType旧格式；不获取竞品评价。"]}}, "contracts": {"tool_abc1234567": {}}}
            business = b"# never execute during packaging\nraise RuntimeError('business action')\n"
            inner = b"---\nname: inner\ndescription: Inner template.\n---\n# untouched template\n"
            with zipfile.ZipFile(package, "w") as archive:
                archive.writestr("sample/SKILL.md", "---\nname: sample\ndescription: Sample skill.\n---\n\n## 淘系 ATP 执行约定\n\nOld execution section.\n\n# Business procedure\n\nKeep the merchant scope. Use taobao__get_item_detail for the own item.\n")
                archive.writestr("sample/scripts/business.py", business)
                archive.writestr("sample/assets/template/SKILL.md", inner)
                archive.writestr("sample/references/atp-routing.json", json.dumps(mapping))
                archive.writestr("sample/references/atp-routing.md", "old")
            item = {"row": 2, "skill_name": "sample", "package_path": str(package), "package_sha256": hashlib.sha256(package.read_bytes()).hexdigest()}
            contract = {"code": "tool_abc1234567", "name": "Read item", "version": "0.0.7", "operation_type": "只读查询", "verification_status": "调用失败", "available": False, "schema_available": False, "example_available": False}
            catalog = {"source": "https://example.test/verified-catalog", "source_sha256": "a" * 64, "contracts": {"tool_abc1234567": contract, "tool_a63f7roe6d": {**contract, "code": "tool_a63f7roe6d"}}}
            result = build_one(item, catalog, root / "out")
            files = read_archive(result["package_path"])
            self.assertEqual(files["sample/scripts/business.py"], business)
            self.assertEqual(files["sample/assets/template/SKILL.md"], inner)
            self.assertIn(b"Keep the merchant scope.", files["sample/SKILL.md"])
            self.assertNotIn(b"taobao__get_item_detail", files["sample/SKILL.md"])
            self.assertIn(b"tool_a63f7roe6d", files["sample/SKILL.md"])
            routing = json.loads(files["sample/references/atp-routing.json"])
            self.assertEqual(routing["operations"]["read_item"]["execution_codes"], [])
            self.assertIn("不获取竞品评价", routing["operations"]["read_item"]["notes"][0])
            package.write_bytes(b"changed after review")
            with self.assertRaisesRegex(ValueError, "changed"):
                build_one(item, catalog, root / "out")

    def test_archive_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "unsafe.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("../escape", "never extract")
            with self.assertRaisesRegex(ValueError, "Unsafe"):
                read_archive(path)


if __name__ == "__main__":
    unittest.main()

class PublicationGuards(unittest.TestCase):
    def test_version_intent_is_not_retried_and_package_digest_is_bound(self):
        from workflow import publication_gate
        item = {'package_sha256': 'a' * 64}
        target = {'account': 'account', 'publicAppId': '100', 'formalCode': 'sample', 'editorUrl': 'https://example.test/editor', 'existingMode': '定向', 'authorizationReadback': {'complete': True, 'shops': []}}
        bm = {'phase': 'fixed_asset_verified', 'sha256': 'a' * 64}
        proof = {'verified': True, 'expected_package_sha256': 'a' * 64}
        self.assertTrue(publication_gate(item, target, bm, proof, {}))
        with self.assertRaisesRegex(ValueError, 'reconciled'):
            publication_gate(item, target, bm, proof, {'phase': 'version_submitting'})
        with self.assertRaisesRegex(ValueError, 'fixed asset'):
            publication_gate(item, target, {'phase': 'fixed_asset_verified', 'sha256': 'b' * 64}, proof, {})

    def test_no_package_row_and_protected_field_changes_are_rejected(self):
        from workflow import verify_feishu
        baseline = [{'A': '技能名称'}, {'A': 'One', 'I': 'old.zip'}, {'A': 'Two'}]
        manifest = [{'row': 2, 'package_path': '/tmp/new.zip'}]
        current = [baseline[0], {'A': 'One', 'I': 'new.zip', 'E': '升级更新中', 'AD': '待同步'}, baseline[2]]
        self.assertTrue(verify_feishu(baseline, current, manifest, {'I', 'E', 'AD'})['verified'])
        current[2] = {'A': 'overwritten'}
        self.assertFalse(verify_feishu(baseline, current, manifest, {'I', 'E', 'AD'})['verified'])


class PlatformPackageProof(unittest.TestCase):
    def test_reviewed_hidden_cache_marker_cannot_hide_cache_content(self):
        from package_io import compare
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            expected, actual = root / 'expected.zip', root / 'actual.zip'
            content = {'root/SKILL.md': '---\nname: sample\ndescription: example\n---\n', 'root/scripts/report.py': 'print("local report")\n'}
            with zipfile.ZipFile(expected, 'w') as z:
                for name, value in content.items():
                    z.writestr(name, value)
            def write(marker=b'', extra=None, folder='scripts/__pycache__'):
                with zipfile.ZipFile(actual, 'w') as z:
                    for name, value in content.items():
                        z.writestr(name, value)
                    z.writestr('root/' + folder + '/.gitkeep', marker)
                    if extra:
                        z.writestr('root/' + folder + '/unknown.py', extra)
            allowed = ['scripts/__pycache__/.gitkeep']
            write()
            self.assertFalse(compare(expected, actual, 'sample')['verified'])
            self.assertTrue(compare(expected, actual, 'sample', allowed)['verified'])
            write(marker=b'nonempty')
            with self.assertRaisesRegex(ValueError, 'Nonempty'):
                compare(expected, actual, 'sample', allowed)
            write(extra=b'unknown content')
            with self.assertRaises(ValueError):
                compare(expected, actual, 'sample', allowed)
            write(folder='unknown/__pycache__')
            with self.assertRaises(ValueError):
                compare(expected, actual, 'sample', ['unknown/__pycache__/.gitkeep'])

    def test_reviewed_agent_marker_is_row_scoped_and_cannot_hide_content(self):
        from package_io import compare
        from publish_batch import reviewed_empty_markers
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            expected, actual = root / 'expected.zip', root / 'actual.zip'
            business = {'root/SKILL.md': '---\nname: sample\ndescription: example\n---\n', 'root/agents/openai.yaml': 'interface: {}\n'}
            with zipfile.ZipFile(expected, 'w') as z:
                for name, value in business.items():
                    z.writestr(name, value)
            def write_marker(value):
                with zipfile.ZipFile(actual, 'w') as z:
                    for name, content in business.items():
                        z.writestr(name, content)
                    z.writestr('root/agents/.gitkeep', value)
            plan = {'124': ['agents/.gitkeep']}
            write_marker(b'')
            self.assertFalse(compare(expected, actual, 'sample', reviewed_empty_markers(plan, 125))['verified'])
            self.assertTrue(compare(expected, actual, 'sample', reviewed_empty_markers(plan, 124))['verified'])
            write_marker(b'not an empty marker')
            with self.assertRaisesRegex(ValueError, 'Nonempty'):
                compare(expected, actual, 'sample', reviewed_empty_markers(plan, 124))
            with self.assertRaises(ValueError):
                reviewed_empty_markers({'124': ['../agents/.gitkeep']}, 124)

    def test_only_explicit_empty_marker_and_formal_frontmatter_name_are_normalized(self):
        from package_io import compare
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            expected=root/'expected.zip';actual=root/'actual.zip'
            def archive(path, name, marker):
                with zipfile.ZipFile(path,'w') as z:
                    z.writestr('root/SKILL.md','---\nname: '+name+'\ndescription: example\n---\nBody\n')
                    z.writestr('root/references/contract.md','same')
                    if marker is not None:z.writestr('root/references/.gitkeep',marker)
            archive(expected,'sample',None);archive(actual,'formal-code',b'')
            self.assertFalse(compare(expected,actual,'formal-code')['verified'])
            self.assertTrue(compare(expected,actual,'formal-code',['references/.gitkeep'])['verified'])
            archive(actual,'formal-code',b'nonempty')
            with self.assertRaisesRegex(ValueError,'Nonempty'):
                compare(expected,actual,'formal-code',['references/.gitkeep'])

class ReviewedInstallationMetadata(unittest.TestCase):
    def test_reviewed_legacy_sidecar_requires_exact_bytes_and_known_timestamp_schema(self):
        from package_io import compare
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            expected, actual = root / 'expected.zip', root / 'actual.zip'
            skill = '---\nname: sample\ndescription: example\n---\n'
            with zipfile.ZipFile(expected, 'w') as z:
                z.writestr('root/SKILL.md', skill)
            def write(value):
                raw = json.dumps(value).encode()
                with zipfile.ZipFile(actual, 'w') as z:
                    z.writestr('root/SKILL.md', skill)
                    z.writestr('root/.version.json', raw)
                return hashlib.sha256(raw).hexdigest()
            value = {'createdAt': '2026-10-25T04:45:49.595Z', 'source': 'user-created'}
            sha = write(value)
            self.assertFalse(compare(expected, actual, 'sample')['verified'])
            self.assertTrue(compare(expected, actual, 'sample', (), {'.version.json': sha})['verified'])
            write({**value, 'createdAt': '2026-10-26T04:45:49.595Z'})
            with self.assertRaisesRegex(ValueError, 'changed'):
                compare(expected, actual, 'sample', (), {'.version.json': sha})
            for invalid in [{**value, 'createdAt': 'unknown'}, {**value, 'createdAt': '2026-10-25'}, {**value, 'source': 'other'}, {**value, 'extra': 'unknown'}]:
                sha = write(invalid)
                with self.assertRaisesRegex(ValueError, 'Unknown'):
                    compare(expected, actual, 'sample', (), {'.version.json': sha})

    def test_sidecar_requires_exact_reviewed_hash_known_schema_and_matching_code(self):
        from package_io import compare
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);expected=root/'expected.zip';actual=root/'actual.zip'
            skill='---\nname: formal-code\ndescription: example\n---\nBusiness procedure\n'
            metadata={'skillId':'installation','skillCode':'formal-code','skillName':'Example','skillDescription':'Example installation metadata','skillVersion':'v1.6.5','dataSensitive':False,'source':'user-created','installedAt':1,'createMethod':'zip-install','createdAt':'2026-11-11','ossUploaded':True}
            def write(value):
                raw=json.dumps(value).encode()
                with zipfile.ZipFile(actual,'w') as z:
                    z.writestr('root/SKILL.md',skill);z.writestr('root/.version.json',raw)
                return hashlib.sha256(raw).hexdigest()
            with zipfile.ZipFile(expected,'w') as z:z.writestr('root/SKILL.md',skill)
            sha=write(metadata)
            self.assertFalse(compare(expected,actual,'formal-code')['verified'])
            self.assertTrue(compare(expected,actual,'formal-code',(),{'.version.json':sha})['verified'])
            write({**metadata,'skillVersion':'v2.0.0'})
            with self.assertRaisesRegex(ValueError,'changed'):
                compare(expected,actual,'formal-code',(),{'.version.json':sha})
            sha=write({**metadata,'token':'synthetic-forbidden-field'})
            with self.assertRaisesRegex(ValueError,'Unknown'):
                compare(expected,actual,'formal-code',(),{'.version.json':sha})
            sha=write({**metadata,'skillCode':'another-target'})
            with self.assertRaisesRegex(ValueError,'Unknown'):
                compare(expected,actual,'formal-code',(),{'.version.json':sha})


class ResumeIdentity(unittest.TestCase):
    def test_mismatched_pinned_target_is_rejected_before_ui(self):
        from publish_batch import reconcile_public_target
        prior={'target':{'account':'authorized','publicAppId':'1','formalCode':'sample','searchName':'Sample'}}
        public={'account':'authorized','publicAppId':'1','formalCode':'sample'}
        self.assertEqual(reconcile_public_target(prior,public)['formalCode'],'sample')
        for field in ['account','publicAppId','formalCode']:
            with self.assertRaisesRegex(ValueError,'different'):
                reconcile_public_target(prior,{**public,field:'other'})

    def test_approved_refresh_does_not_drop_verified_listing_evidence(self):
        from publish_batch import preserve_reconciled_evidence
        identity={'row':2,'version':'1.0.1','package_sha256':'a','public_app_id':'1','formal_code':'sample'}
        old={**identity,'phase':'listed','online_version':'1.0.1','approved_package_verified':True,'authorization_preserved':True}
        refreshed={**identity,'phase':'version_approved','version_readback':'fresh'}
        merged=preserve_reconciled_evidence(old,refreshed)
        self.assertEqual(merged['phase'],'version_approved')
        self.assertNotIn('online_version',merged)
        self.assertTrue(merged['prior_reconciliation']['approved_package_verified'])
        self.assertTrue(merged['needs_online_recheck'])
        other={**refreshed,'package_sha256':'b'}
        self.assertEqual(preserve_reconciled_evidence(old,other),other)


class PersistedWriteback(unittest.TestCase):
    def test_allowed_fields_alone_cannot_prove_an_unsaved_online_version(self):
        from workflow import verify_results
        before=[{'A':'header'},{'A':'Skill','I':'skill.zip','F':'old','G':'old'}]
        write={'row':2,'expectedName':'Skill','packageName':'skill.zip','formalCode':'sample','currentVersion':'1.0.1','onlineVersion':'1.0.1','batchId':'batch','resultNote':'actual'}
        after=[before[0],{**before[1],'J':'sample','F':'1.0.1','AG':'[batch] actual'}]
        result=verify_results(before,after,[write])
        self.assertFalse(result['verified'])
        self.assertIn({'row':2,'field':'G','reason':'planned_value_not_persisted'},result['failures'])
        after[1]['G']='1.0.1'
        self.assertTrue(verify_results(before,after,[write])['verified'])


class FullResultColumns(unittest.TestCase):
    def test_only_reviewed_cells_change_and_multiline_prior_notes_survive(self):
        from workflow import result_columns, verify_results
        header={'A':'技能名称','I':'自建技能包','E':'技能生成及状态','F':'当前版本','G':'线上版本','J':'技能code','AG':'同步说明'}
        before=[header,{'A':'Skill','I':'skill.zip','E':'升级更新中','F':'old','G':'old','J':'sample','AG':'Other note\nSecond line'},{'A':'No package','F':'keep','AG':'untouched'}]
        write={'row':2,'recordId':'recPinned','expectedName':'Skill','packageName':'skill.zip','formalCode':'sample','currentVersion':'1.0.1','onlineVersion':'1.0.1','platformVersionConfirmed':True,'onlinePackageVerified':True,'generationStatus':'上架完成','listingVerified':True,'batchId':'batch','resultNote':'actual'}
        columns=result_columns(before,[write]);self.assertEqual({x['columnKey'] for x in columns},{'E','F','G','AG'})
        after=[dict(x) for x in before]
        for column in columns:
            for row,value in enumerate(column['values'],1):after[row][column['columnKey']]=value
        self.assertTrue(verify_results(before,after,[write])['verified'])
        self.assertEqual(after[2]['F'],'keep');self.assertEqual(after[2]['AG'],'untouched')
        self.assertTrue(after[1]['AG'].startswith('Other note\nSecond line\n'))
        with self.assertRaisesRegex(ValueError,'Unverified listing'):
            result_columns(before,[{**write,'listingVerified':False}])


class ConcurrentResultLedger(unittest.TestCase):
    def test_two_processes_preserve_each_others_rows(self):
        import subprocess
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'results.json'
            script_dir=str(Path(__file__).resolve().parents[1]/'scripts')
            code="import sys;sys.path.insert(0,sys.argv[1]);from workflow import merge_result;from pathlib import Path;start=int(sys.argv[3]);[(merge_result(Path(sys.argv[2]),{'row':i,'phase':'observed'})) for i in range(start,start+20)]"
            processes=[subprocess.Popen([sys.executable,'-c',code,script_dir,str(output),str(start)]) for start in [1,21]]
            self.assertEqual([p.wait() for p in processes],[0,0])
            values=json.loads(output.read_text());self.assertEqual({x['row'] for x in values},set(range(1,41)))


class ListingStateEvidence(unittest.TestCase):
    def test_new_target_mode_is_verified_without_claiming_a_prior_listing(self):
        from workflow import listed_evidence, was_listed_target
        base={'online_version':'1.0.1','approved_package_verified':True,'authorization_preserved':True}
        self.assertTrue(listed_evidence({**base,'existing_mode_preserved':True}))
        new={**base,'listing_kind':'new','listing_mode_verified':True,'listing_mode':'定向订购','existing_mode_preserved':False}
        self.assertTrue(listed_evidence(new));self.assertFalse(listed_evidence({**new,'listing_mode_verified':False}))
        self.assertFalse(was_listed_target({'publicAppId':'1','cardBefore':'已上架规划器\n未公开\nAppkey\n1\ndescription'}))
        self.assertTrue(was_listed_target({'publicAppId':'1','cardBefore':'Skill\n定向\n已上架\nAppkey\n1'}))


class ApprovedPackageCache(unittest.TestCase):
    def test_cache_requires_exact_identity_bytes_and_current_frozen_source(self):
        from package_io import compare, digest
        from reconcile_batch import cached_approved_package
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp);source=directory/'source.zip';actual=directory/'approved-1.0.1.zip'
            for path in [source,actual]:
                with zipfile.ZipFile(path,'w') as archive:archive.writestr('sample/SKILL.md','---\nname: sample\ndescription: test\n---\nBody\n')
            item={'package_path':str(source),'package_sha256':digest(source)}
            target={'account':'test account','publicAppId':'123','formalCode':'sample'}
            proof=compare(source,actual,'sample');proof['approvalBinding']={**target,'version':'1.0.1','downloadVersion':'1.0.1','packageSha256':item['package_sha256'],'actualDownloadSha256':digest(actual)}
            proof_path=directory/'approved-1.0.1-proof.json';proof_path.write_text(json.dumps(proof))
            self.assertIsNotNone(cached_approved_package(item,target,'1.0.1',directory))
            self.assertIsNone(cached_approved_package(item,{**target,'publicAppId':'999'},'1.0.1',directory))
            self.assertIsNone(cached_approved_package(item,target,'1.0.2',directory))
            actual.write_bytes(b'tampered')
            self.assertIsNone(cached_approved_package(item,target,'1.0.1',directory))
            with self.assertRaisesRegex(ValueError,'Frozen source changed'):
                cached_approved_package({**item,'package_sha256':'wrong'},target,'1.0.1',directory)


class OfflineListingEvidence(unittest.TestCase):
    def test_only_observed_offline_authorization_unavailability_permits_version_update(self):
        from workflow import publication_gate
        item={'package_sha256':'a'*64};bm={'phase':'fixed_asset_verified','sha256':'a'*64};proof={'verified':True,'expected_package_sha256':'a'*64}
        target={'account':'a','publicAppId':'1','formalCode':'sample','editorUrl':'https://example.test/editor','existingMode':'定向订购','wasListed':False,'hadListing':True,'offlineBefore':True,'moreMenuBefore':['修改上架详情','编辑技能','版本管理'],'listingBefore':{'mode':'1'},'authorizationReadback':{'complete':False,'shops':[],'unavailableWhileUnlisted':True}}
        self.assertTrue(publication_gate(item,target,bm,proof,{}))
        for change in [{'offlineBefore':False},{'hadListing':False},{'wasListed':True},{'moreMenuBefore':['授权管理']},{'listingBefore':{'mode':'0'}}]:
            with self.assertRaisesRegex(ValueError,'pagination'):
                publication_gate(item,{**target,**change},bm,proof,{})

    def test_restored_listing_reports_current_authorization_without_inventing_before_list(self):
        from workflow import listed_evidence, had_listing_target
        result={'online_version':'1.0.2','approved_package_verified':True,'listing_kind':'restore','listing_mode':'定向订购','listing_mode_verified':True,'existing_mode_preserved':True,'authorization_preserved':False,'authorization_before_unavailable':True,'authorization_current_readback_complete':True,'authorization_current_shops':[],'authorization_not_changed_by_workflow':True}
        self.assertTrue(listed_evidence(result))
        for change in [{'authorization_current_readback_complete':False},{'authorization_not_changed_by_workflow':False},{'authorization_before_unavailable':False},{'existing_mode_preserved':False},{'listing_kind':'new'}]:self.assertFalse(listed_evidence({**result,**change}))
        self.assertTrue(had_listing_target({'publicAppId':'1','wasListed':False,'cardBefore':'Skill\n定向\n已下架\nAppkey\n1'}))
        self.assertFalse(had_listing_target({'publicAppId':'1','wasListed':False,'cardBefore':'已下架技能生成器\n未公开\nAppkey\n1'}))


class SharedOfflineAuthorizationContract(unittest.TestCase):
    def test_version_gates_share_offline_evidence_cases(self):
        from workflow import version_authorization_allowed
        contract=json.loads((Path(__file__).parent/'offline-auth-cases.json').read_text())
        for case in contract['cases']:
            with self.subTest(case=case['name']):self.assertEqual(version_authorization_allowed({**contract['base'],**case['patch']}),case['allowed'])
