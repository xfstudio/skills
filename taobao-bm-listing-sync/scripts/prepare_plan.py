#!/usr/bin/env python3
"""Generate a conservative, reviewable package-description plan; never writes BM."""
import argparse
import collections
import datetime
import json
import pathlib
import re

MARK = '尚未核对淘宝上架。'


def original_description(description, code, appkey):
    if description == '': return ''
    if description.startswith('来源：') and description.endswith(MARK):
        return description[:-len(MARK)].rstrip('，； ')+'。'
    identity = re.escape(code)+r'，AppKey '+re.escape(str(appkey))
    legacy = r'淘宝对应技能：[^\n]*（'+identity+r'）；\d{4}-\d{2}-\d{2}平台显示(?:定向|公开)已上架，当前版本 [^；]+；本地包与该版本内容尚未核对。$'
    match = re.search(legacy, description)
    if match and description.startswith('来源：'):
        return description[:match.start()].rstrip('，； ')+'。'
    fresh = r'^淘宝状态：(?:定向|公开)已上架 · [^（]+（\d{4}-\d{2}-\d{2}核对）；关联技能：[^\n]*（'+identity+r'）；本地(?:包|旧修订)与该版本内容尚未核对。(?P<source>(?:来源：[^\n]+)?)$'
    match = re.match(fresh, description)
    return match.group('source') if match else None


def prepare(details, history, packages, expected):
    if len(details) != expected:
        raise ValueError(f'incomplete observation: {len(details)}/{expected}')
    accounts = {x.get('account') for x in details}
    if len(accounts) != 1 or not next(iter(accounts), None):
        raise ValueError('missing or inconsistent platform account')
    pairs = [(x.get('name'),str(x.get('appkey'))) for x in details]
    codes = [x.get('code') for x in details]
    if len(set(pairs)) != expected or len(set(codes)) != expected or any(not c for c in codes):
        raise ValueError('duplicate or missing platform identity')
    by_code = {x.get('code'): x for x in details}
    hist_counts = collections.Counter(x.get('platform_code') for x in history)
    local = {x['id']:x for x in packages}
    package_counts=collections.Counter(pid for row in history for key in ('newPackageId','oldPackageId') if (pid:=(row.get('local_version_update') or {}).get(key)))
    plan=[]; skipped=[]; used=set()
    for row in history:
        code=row.get('platform_code');obs=by_code.get(code);u=row.get('local_version_update') or {}
        reason=None
        if not obs or hist_counts[code] != 1 or obs.get('name') != row.get('platform_name') or (row.get('platform_appkey') and str(row['platform_appkey']) != str(obs.get('appkey'))): reason='平台身份或历史映射不唯一'
        elif obs.get('status') != '已上架' or obs.get('scope') not in ('定向','公开'): reason='平台状态未确认'
        elif u.get('status')!='verified' or not row.get('skill_name') or not row.get('sha256') or u.get('sha256')!=row.get('sha256'): reason='缺少可信的本地版本关联与摘要'
        version = re.search(r'当前版本\s*\n([^\n]+)',obs.get('text','')) if obs else None
        if reason is None and not version:reason='平台版本未显示'
        if reason:
            skipped.append({'file':row.get('file'),'code':code,'reason':reason});continue
        stamp=obs.get('observedAt','')
        try:
            observed_at=datetime.datetime.fromisoformat(stamp.replace('Z','+00:00'))
            if observed_at.tzinfo is None or observed_at.utcoffset() is None: raise ValueError()
            day=observed_at.astimezone(datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y-%m-%d')
        except (ValueError,AttributeError): raise ValueError('invalid observation timestamp') from None
        for kind,package_key,catalog_key in [('new','newPackageId','newCatalogId'),('old','oldPackageId','parentCatalogId')]:
            pid=u.get(package_key);catalog=u.get(catalog_key);pack=local.get(pid);problem=None
            if not pid or not pack or not catalog:problem='缺少本地包或目录记录'
            elif catalog[:12] not in pack.get('name',''):problem='本地包与目录记录不一致'
            elif not pack.get('can_write'):problem='本地包不可编辑'
            elif original_description(pack.get('description',''),str(code),obs.get('appkey')) is None:problem='原描述与预期不同，需人工复核'
            elif package_counts[pid] != 1 or pid in used:problem='本地包重复映射'
            if problem:
                skipped.append({'file':row.get('file'),'packageId':pid,'code':code,'kind':kind,'reason':problem});continue
            noun='旧修订' if kind=='old' else '包'
            note=f"淘宝状态：{obs['scope']}已上架 · {version.group(1).strip()}（{day}核对）；关联技能：{obs['name']}（{obs['code']}，AppKey {obs['appkey']}）；本地{noun}与该版本内容尚未核对。"
            before=pack['description'];after=note+original_description(before,str(code),obs['appkey'])
            plan.append({'packageId':pid,'packageName':pack['name'],'skillName':row['skill_name'],'expectedUpdatedAt':pack['updated_at'],'before':before,'after':after,'platformCode':obs['code'],'platformName':obs['name'],'appkey':obs['appkey'],'scope':obs['scope'],'version':version.group(1).strip(),'observedAt':stamp,'lineageSha256':row['sha256'],'catalogId':catalog,'localRevisionKind':kind})
            used.add(pid)
    return {'platformAccount':next(iter(accounts)),'observedCount':len(details),'planned':plan,'skipped':skipped}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--details',required=True);ap.add_argument('--history',required=True);ap.add_argument('--packages',required=True);ap.add_argument('--expected',required=True,type=int);ap.add_argument('--output',required=True);a=ap.parse_args()
    load=lambda p:json.loads(pathlib.Path(p).read_text())
    hist=load(a.history);result=prepare(load(a.details),hist['items'],load(a.packages),a.expected)
    pathlib.Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f"观察 {result['observedCount']}；可更新 {len(result['planned'])}；待核对 {len(result['skipped'])}")
if __name__=='__main__':main()
