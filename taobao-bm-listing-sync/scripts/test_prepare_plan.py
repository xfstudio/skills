import copy, unittest
from prepare_plan import prepare

class PlanTests(unittest.TestCase):
    def setUp(self):
        self.d=[{'account':'测试账号','name':'平台名称','appkey':'123','code':'formal-code','status':'已上架','scope':'定向','text':'当前版本\n1.0.1\n','observedAt':'2026-11-04T07:00:00Z'}]
        self.h=[{'file':'a.zip','skill_name':'local-skill','platform_name':'平台名称','platform_appkey':'123','platform_code':'formal-code','sha256':'abc','local_version_update':{'status':'verified','newPackageId':'PKG','newCatalogId':'12345678-abc-xyz','sha256':'abc'}}]
        self.p=[{'id':'PKG','name':'本地包 · BM 12345678-abc','description':'来源：原包；本地导入，尚未核对淘宝上架。','can_write':True,'updated_at':'1'}]
    def test_confirmed_identity_and_preserves_uncertainty(self):
        result=prepare(self.d,self.h,self.p,1);self.assertEqual(len(result['planned']),1)
        self.assertIn('定向已上架',result['planned'][0]['after']);self.assertIn('内容尚未核对',result['planned'][0]['after']);self.assertTrue(result['planned'][0]['after'].startswith('淘宝状态：定向已上架'));self.assertIn('来源：原包；本地导入。',result['planned'][0]['after'])
    def test_refresh_existing_generated_observation(self):
        first=prepare(self.d,self.h,self.p,1)['planned'][0]
        updated=copy.deepcopy(self.p);updated[0]['description']=first['after']
        d=copy.deepcopy(self.d);d[0]['text']='当前版本\n1.0.2\n'
        next_plan=prepare(d,self.h,updated,1)['planned'][0]
        self.assertIn('1.0.2',next_plan['after']);self.assertEqual(next_plan['after'].count('淘宝状态：'),1)
    def test_old_revision_is_labeled_and_requires_parent(self):
        h=copy.deepcopy(self.h);h[0]['local_version_update'].update(oldPackageId='OLD',parentCatalogId='87654321-abc-xyz')
        p=self.p+[{'id':'OLD','name':'旧包 · BM 87654321-abc','description':'来源：旧包；尚未核对淘宝上架。','can_write':True,'updated_at':'1'}]
        plan=prepare(self.d,h,p,1)['planned'];self.assertEqual(len(plan),2)
        self.assertIn('本地旧修订与该版本内容尚未核对',next(x['after'] for x in plan if x['packageId']=='OLD'))
        del h[0]['local_version_update']['parentCatalogId']
        self.assertEqual(len(prepare(self.d,h,p,1)['planned']),1)
    def test_conflicting_package_mappings_are_all_excluded(self):
        h=copy.deepcopy(self.h);other=copy.deepcopy(h[0]);other.update(platform_code='other-code',platform_name='其他技能',platform_appkey='456');h.append(other)
        d=copy.deepcopy(self.d);other_detail=copy.deepcopy(d[0]);other_detail.update(code='other-code',name='其他技能',appkey='456');d.append(other_detail)
        result=prepare(d,h,self.p,2);self.assertEqual(result['planned'],[]);self.assertEqual(sum(x['reason']=='本地包重复映射' for x in result['skipped']),2)
    def test_unmatched_code_never_updates(self):
        d=copy.deepcopy(self.d);d[0]['code']='different';self.assertEqual(len(prepare(d,self.h,self.p,1)['planned']),0)
    def test_missing_or_inconsistent_account_stops(self):
        d=copy.deepcopy(self.d);del d[0]['account']
        with self.assertRaises(ValueError):prepare(d,self.h,self.p,1)
        d=copy.deepcopy(self.d);other=copy.deepcopy(d[0]);other.update(account='另一账号',name='另一技能',appkey='234',code='other');d.append(other)
        with self.assertRaises(ValueError):prepare(d,self.h,self.p,2)
    def test_mismatched_appkey_never_updates(self):
        d=copy.deepcopy(self.d);d[0]['appkey']='456';self.assertEqual(len(prepare(d,self.h,self.p,1)['planned']),0)
    def test_empty_description_gets_status(self):
        p=copy.deepcopy(self.p);p[0]['description']='';self.assertTrue(prepare(self.d,self.h,p,1)['planned'][0]['after'].startswith('淘宝状态：'))
    def test_unexpected_description_never_updates(self):
        p=copy.deepcopy(self.p);p[0]['description']='人工撰写的说明';self.assertEqual(len(prepare(self.d,self.h,p,1)['planned']),0)
    def test_mismatched_digest_never_updates(self):
        h=copy.deepcopy(self.h);h[0]['local_version_update']['sha256']='different';self.assertEqual(len(prepare(self.d,h,self.p,1)['planned']),0)
    def test_incomplete_or_duplicate_observations_stop(self):
        with self.assertRaises(ValueError):prepare(self.d,self.h,self.p,2)
        with self.assertRaises(ValueError):prepare(self.d*2,self.h,self.p,2)
if __name__=='__main__':unittest.main()
