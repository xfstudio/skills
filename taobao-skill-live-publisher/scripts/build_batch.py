"""Rebuild reviewed skills against one pinned, UI-exported MCP catalog."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import zipfile


OLD_SOURCE = "https://freecallai.feishu.cn/wiki/F7guwjSNZi0tiokNwrPcWWm7nvh"
LEGACY_ROUTES = {
    "taobao__get_item_detail": ("tool_a63f7roe6d", "商品详情路由（本店商品使用 tool_a63f7roe6d；竞品详情、评价、问大家或目录缺口使用 ecom-borswer MCP 电商浏览器；版本、参数及示例见 references/atp-routing.md）"),
    "taobao__list_competitor_items": ("tool_755beaox3r", "已配置竞品查询路由（tool_755beaox3r；版本、参数及示例见 references/atp-routing.md；不以已配置清单代替新竞品发现，目录缺口用 ecom-borswer MCP 电商浏览器）"),
    "taobao__batch_add_competitor_items": (None, "使用 ecom-borswer MCP 电商浏览器添加已确认的竞品配置（仅在原技能允许且本轮已授权时执行）"),
    "taobao__batch_delete_competitor_items": (None, "使用 ecom-borswer MCP 电商浏览器移除已确认的竞品配置（仅在原技能允许且本轮已授权时执行）"),
    "taobao__batch_add": (None, "使用 ecom-borswer MCP 电商浏览器执行原步骤已明确的添加操作（对象不明、只读或未获本轮授权时停止）"),
}
HEADER_START = "## 淘系 ATP 执行约定"
HEADER = """## 淘系 MCP 执行约定

执行淘系步骤前，读取 [MCP 编码、版本、请求参数与调用示例](references/atp-routing.md)。逐项按业务对象、指标、周期、读写性质核对等价能力，不一次调用本包全部代码。

- 有等价且可用能力时，用 Bash 执行参考表中的 `atp invoke --code <MCP编码> --version <目录在线版本> --params '<实际JSON对象>'`。保留准确嵌套字段、类型和必填项，不拼接旧接口参数。
- 调用示例来自用户指定目录，只说明调用形状；实际店铺、商品、日期、预算和动作必须来自本轮授权输入。不要原样执行示例中的业务 ID、日期、价格或预算；模板 null 必须补齐。
- 目录标注调用失败、参数不接受、无业务权限或异常提示时，先核对实际注册 schema 和回执，不能声称已获取数据。契约不可用、示例与必填项不一致且无法核对、或没有等价能力的步骤，使用用户指定的 ecom-borswer MCP 电商浏览器补齐，并保留原对象、周期与交付要求。
- 写操作仅 schema 核实不等于实调通过。只在原技能允许该动作且本轮业务授权、原阶段确认均已满足时执行；只读技能不因参考表含写代码而取得写权限，历史归档或废止动作不恢复执行。结果未知先回查，不重复提交。
- 现有本地计算、分析、报告和校验流程保留；旧淘系接口脚本不直接运行，不把新 MCP 回执伪装成旧作业 ID 或完整采集结果。登录、验证码和协议交给用户。
- 不在参数、技能或日志中写入系统身份、密钥、令牌或固定鉴权值。不同指标、不同商家或不完整比较数据不能互相代替；缺项如实报告。

"""


def read_archive(path):
    with zipfile.ZipFile(path) as archive:
        infos = [x for x in archive.infolist() if not x.is_dir()]
        if sum(x.file_size for x in infos) > 100 * 1024 * 1024:
            raise ValueError("Skill exceeds the decompressed size limit")
        result = {}
        for info in infos:
            name = PurePosixPath(info.filename)
            if name.is_absolute() or ".." in name.parts or "\\" in info.filename:
                raise ValueError("Unsafe skill archive path")
            if info.filename in result:
                raise ValueError("Duplicate skill archive path")
            if (info.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("Symlink in skill archive")
            result[info.filename] = archive.read(info)
        return result


def replace_instruction(text, source):
    if HEADER_START in text:
        start = text.index(HEADER_START)
        match = re.search(r"(?m)^#{1,2} ", text[start + len(HEADER_START):])
        if not match:
            raise ValueError("Cannot locate the existing execution section boundary")
        end = start + len(HEADER_START) + match.start()
        text = text[:start] + HEADER + text[end:]
    elif "## 淘系 MCP 执行约定" not in text:
        if text.startswith("---\n"):
            end = text.find("\n---", 4)
            if end < 0:
                raise ValueError("Invalid skill frontmatter")
            end = text.find("\n", end + 1)
            text = text[:end + 1] + "\n" + HEADER + text[end + 1:]
        else:
            raise ValueError("No reviewed skill frontmatter")
    return text.replace(OLD_SOURCE, source)


def public_contract(contract):
    keys = [
        "code", "name", "version", "operation_type", "verification_status", "source_row",
        "notes", "parameters", "request_schema", "request_template", "example_command",
        "example_params", "example_schema_discrepancies", "available", "schema_available",
        "example_available", "schema_error", "example_error",
    ]
    return {key: contract[key] for key in keys if key in contract}


def route_document(routing):
    output = [
        "# MCP 编码、请求参数与调用示例\n",
        f"目录来源：{routing['source']}\n",
        f"目录快照 SHA256：`{routing['source_sha256']}`。本包未执行目录中的商家业务调用。\n",
        "先选本步骤的等价能力，再核对代码、在线版本、必填和嵌套类型。示例只作形状参考，"
        "不是本轮真实业务输入；写操作示例不得在升级、校验或发布流程中运行。\n",
        "## 原步骤与能力边界\n",
    ]
    for operation, mapping in routing.get("operations", {}).items():
        output.append(f"### {operation}\n")
        output.append("目录候选：" + (", ".join(f"`{x}`" for x in mapping.get("codes", [])) or "无，使用电商浏览器") + "\n")
        for note in mapping.get("notes", []):
            output.append("- " + note + "\n")
        unavailable = mapping.get("unavailable_codes", [])
        if unavailable:
            output.append("- 本快照不可用，不能当作实调成功：" + ", ".join(unavailable) + "。按 SKILL.md 使用浏览器补齐。\n")
    output.append("## 版本固定的公开请求契约\n")
    for code, contract in routing["contracts"].items():
        output.extend([
            f"### {code} — {contract['name']}\n",
            f"版本：`{contract['version'] or '未取得'}`；操作：{contract['operation_type']}；核验：{contract['verification_status']}。\n",
        ])
        if not contract["available"]:
            output.append("本项不得据目录示例宣称可用；按原业务范围使用电商浏览器或报告缺口。\n")
        if contract.get("example_schema_discrepancies"):
            output.append("目录示例与 schema 有以下差异，须以运行时实际注册契约核对，不自行补造系统上下文：\n")
            output.append("```json\n" + json.dumps(contract["example_schema_discrepancies"], ensure_ascii=False, indent=2) + "\n```\n")
        if contract.get("request_schema"):
            output.append("请求字段、类型、嵌套与必填：\n```json\n" + json.dumps(contract["request_schema"], ensure_ascii=False, indent=2) + "\n```\n")
        if contract.get("example_command"):
            output.append("目录调用形状（仅示例，不直接执行）：\n```bash\n" + contract["example_command"] + "\n```\n")
        if contract.get("request_template") is not None:
            output.append("待替换为本轮真实输入的完整结构模板：\n```json\n" + json.dumps(contract["request_template"], ensure_ascii=False, indent=2) + "\n```\n")
    return "\n".join(output)


def build_one(item, catalog, output):
    path = Path(item.get("package_path", item.get("path", "")))
    expected = item.get("package_sha256", item.get("sha256"))
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError("Reviewed base package changed: " + str(item["row"]))
    files = read_archive(path)
    routes = [name for name in files if name.endswith("/references/atp-routing.json") or name == "references/atp-routing.json"]
    if len(routes) != 1:
        raise ValueError("Base requires one agent-reviewed operation mapping, not guessed MCP matching")
    route_path = routes[0]
    main_skill = route_path[:-len("references/atp-routing.json")] + "SKILL.md"
    old = json.loads(files[route_path])
    old_codes = set(old.get("contracts", {}))
    legacy_seen = set()
    for name, content in files.items():
        if name.endswith('.md') and not name.endswith('/references/atp-routing.md'):
            text = content.decode('utf-8')
            legacy_seen.update(alias for alias in LEGACY_ROUTES if re.search(re.escape(alias) + r'(?![a-zA-Z0-9_])', text))
    for alias in legacy_seen:
        code, _ = LEGACY_ROUTES[alias]
        if code:
            old_codes.add(code)
    for mapping in old.get("operations", {}).values():
        old_codes.update(mapping.get("codes", []))
    missing_codes = old_codes - catalog["contracts"].keys()
    if missing_codes:
        raise ValueError("Catalog removed mapped codes; semantic review required: " + str(sorted(missing_codes)))
    contracts = {code: public_contract(catalog["contracts"][code]) for code in sorted(old_codes)}
    operations = old.get("operations", {})
    for alias in sorted(legacy_seen):
        code, instruction = LEGACY_ROUTES[alias]
        operations[alias.replace('taobao__', 'legacy-')] = {'codes': [code] if code else [], 'notes': [instruction]}
    for mapping in operations.values():
        mapping["unavailable_codes"] = [code for code in mapping.get("codes", []) if not contracts[code]["available"]]
        mapping["execution_codes"] = [code for code in mapping.get("codes", []) if contracts[code]["available"]]
        # Legacy mappingType fields describe the previous export's internal SDK,
        # not the current public request schema; retain the business boundary.
        mapping["notes"] = [
            cleaned for note in mapping.get("notes", [])
            if (cleaned := "；".join(
                clause for clause in re.split("[。；]", note)
                if clause and "mappingType" not in clause and "paramPath" not in clause
            ))
        ]
    routing = {
        "source": catalog["source"], "source_sha256": catalog["source_sha256"],
        "skill": old.get("skill", item.get("skill_name")), "operations": operations,
        "contracts": contracts,
        "browser_fallback_codes": sorted(code for code, c in contracts.items() if not c["available"]),
        "business_calls_executed_during_upgrade": 0,
    }
    files[route_path] = json.dumps(routing, ensure_ascii=False, indent=2).encode()
    files[route_path[:-4] + "md"] = route_document(routing).encode()
    changed = [route_path, route_path[:-4] + "md"]
    for name, content in list(files.items()):
        if not name.endswith(".md") or name.endswith("/references/atp-routing.md"):
            continue
        text = content.decode("utf-8")
        new = replace_instruction(text, catalog["source"]) if HEADER_START in text or name == main_skill else text.replace(OLD_SOURCE, catalog["source"])
        for alias in sorted(legacy_seen, key=len, reverse=True):
            new = re.sub(re.escape(alias) + r'(?![a-zA-Z0-9_])', LEGACY_ROUTES[alias][1], new)
        if new != text:
            files[name] = new.encode()
            changed.append(name)
    output.mkdir(parents=True, exist_ok=True)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    raw_package = buffer.getvalue()
    package_sha256 = hashlib.sha256(raw_package).hexdigest()
    filename = f"{item['row']:04d}_{item['skill_name']}_mcp-{catalog['source_sha256'][:8]}-{package_sha256[:8]}.zip"
    destination = output / filename
    try:
        with destination.open('xb') as writer:
            writer.write(raw_package)
    except FileExistsError:
        if hashlib.sha256(destination.read_bytes()).hexdigest() != package_sha256:
            raise ValueError('Frozen output path already contains different bytes') from None
    return {
        **item, "base_package_path": str(path), "base_package_sha256": expected,
        "package_path": str(destination.resolve()), "package_sha256": package_sha256,
        "catalog_source": catalog["source"], "catalog_sha256": catalog["source_sha256"],
        "changed_files": sorted(changed), "files": len(files),
        "mapped_codes": len(contracts), "unavailable_codes": routing["browser_fallback_codes"],
        "business_calls_executed": 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-manifest", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.base_manifest.read_text())
    catalog = json.loads(args.catalog.read_text())
    results = [build_one(item, catalog, args.output / "packages") for item in manifest]
    (args.output / "package-manifest.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(json.dumps({"packages": len(results), "business_calls_executed": 0, "catalog_sha256": catalog["source_sha256"]}))


if __name__ == "__main__":
    main()
