"""Read the user's exported MCP workbook without calling its business operations."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex
import xml.etree.ElementTree as ET
import zipfile

SOURCE = "https://freecallai.feishu.cn/wiki/O9FZwGp83izmx7kshBqcJdq2n1e?sheet=0HecIe"
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def workbook(path):
    """Read cell values and hyperlink formulas from an ordinary UI XLSX export."""
    with zipfile.ZipFile(path) as archive:
        strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            strings = ["".join(x.itertext()) for x in ET.fromstring(archive.read("xl/sharedStrings.xml"))]
        relations = {
            x.get("Id"): x.get("Target")
            for x in ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        }
        result = {}
        root = ET.fromstring(archive.read("xl/workbook.xml"))
        for sheet in root.find("s:sheets", NS):
            relation = sheet.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            target = relations[relation]
            target = target.lstrip("/") if target.startswith("/") else "xl/" + target
            rows = []
            for row in ET.fromstring(archive.read(target)).findall(".//s:sheetData/s:row", NS):
                values = {}
                for cell in row:
                    column = re.sub(r"\d", "", cell.get("r", ""))
                    value = cell.find("s:v", NS)
                    if cell.get("t") == "s":
                        text = strings[int(value.text)]
                    elif cell.get("t") == "inlineStr":
                        text = "".join(cell.find("s:is", NS).itertext())
                    else:
                        text = value.text if value is not None else ""
                    values[column] = text or ""
                    formula = cell.find("s:f", NS)
                    if formula is not None:
                        match = re.match(r'HYPERLINK\("([^"]+)"', formula.text or "", re.I)
                        if match:
                            values[column + "_url"] = match[1]
                rows.append(values)
            result[sheet.get("name")] = rows
        return result


def named_rows(rows):
    header = rows[0]
    return [{label: row.get(column, "") for column, label in header.items()} for row in rows[1:]]


def join_segments(sheets):
    groups = {}
    for rows in sheets.values():
        if not rows or "分段序号" not in rows[0].values():
            continue
        for row in named_rows(rows):
            key = (row["MCP编码"], row["字段"])
            count, index = int(row["总分段数"]), int(row["分段序号"])
            group = groups.setdefault(key, {"count": count, "parts": {}})
            if group["count"] != count or index in group["parts"] or not 1 <= index <= count:
                raise ValueError("Conflicting MCP continuation segments: " + str(key))
            group["parts"][index] = row["内容"]
    result = {}
    for key, group in groups.items():
        if set(group["parts"]) != set(range(1, group["count"] + 1)):
            raise ValueError("Incomplete MCP continuation segments: " + str(key))
        result[key] = "".join(group["parts"][i] for i in range(1, group["count"] + 1))
    return result


def schema_node(node):
    kind = node.get("类型", "object" if "子参数" in node else None)
    if kind not in {"object", "array", "string", "number", "integer", "boolean", "null"}:
        raise ValueError("Unrecognized public parameter type: " + repr(kind))
    result = {"type": kind}
    if node.get("说明"):
        result["description"] = node["说明"]
    if isinstance(node.get("枚举"), list):
        result["enum"] = node["枚举"]
    if kind == "object":
        result.update(schema_parameters(node.get("子参数", [])))
    if kind == "array":
        if "数组元素" not in node:
            result["items"] = {}
        else:
            result["items"] = schema_node(node["数组元素"])
    return result


def schema_parameters(parameters):
    properties, required = {}, []
    for node in parameters:
        name = node["参数名"]
        if not isinstance(name, str) or not name or name in properties:
            raise ValueError("Ambiguous public parameter name")
        properties[name] = schema_node(node)
        if node.get("必填") is True:
            required.append(name)
    return {"type": "object", "properties": properties, "required": required}


def placeholder(schema):
    if schema.get("type") == "object":
        return {key: placeholder(value) for key, value in schema.get("properties", {}).items()}
    if schema.get("type") == "array":
        return [placeholder(schema["items"])] if schema.get("items") else []
    return None


def validate(value, schema, path="$"):
    """Report type/required/enum discrepancies; do not silently rewrite examples."""
    errors = []
    kind = schema.get("type")
    checks = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "boolean": isinstance(value, bool),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "null": value is None,
    }
    if kind and not checks[kind]:
        return [{"path": path, "reason": "type_mismatch", "expected": kind}]
    if "enum" in schema and value not in schema["enum"]:
        errors.append({"path": path, "reason": "enum_mismatch"})
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append({"path": path + "." + key, "reason": "required_missing"})
        for key, child in schema.get("properties", {}).items():
            if key in value:
                errors.extend(validate(value[key], child, path + "." + key))
    if isinstance(value, list) and schema.get("items"):
        for index, child in enumerate(value):
            errors.extend(validate(child, schema["items"], path + f"[{index}]"))
    return errors


def example_params(text, code, version):
    """Decode the JSON argument, including a source's trailing Chinese annotation."""
    prefix, separator, tail = text.partition("--params")
    if not separator:
        raise ValueError("Invocation example has no --params")
    if shlex.split(prefix) != ["atp", "invoke", "--code", code, "--version", version]:
        raise ValueError("Invocation code/version does not match the catalog row")
    tail = tail.strip()
    try:
        candidate = shlex.split(tail)[0]
    except (ValueError, IndexError):
        # A source example may quote JSON containing a literal apostrophe
        # incorrectly. Decode its JSON data, then render a safely quoted argv;
        # the source text itself is never executed.
        candidate = tail[1:] if tail.startswith(("'", '"')) else tail
    value, _ = json.JSONDecoder().raw_decode(candidate)
    if not isinstance(value, dict):
        raise ValueError("Invocation params must be an object")
    return value


def invoke_command(code, version, params):
    if not re.fullmatch(r"tool_[a-z0-9]+", code) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("A verified MCP code and pinned version are required")
    return " ".join(shlex.quote(x) for x in [
        "atp", "invoke", "--code", code, "--version", version, "--params",
        json.dumps(params, ensure_ascii=False, separators=(",", ":")),
    ])


def load_catalog(path, source=SOURCE):
    sheets = workbook(path)
    candidates = [rows for rows in sheets.values() if rows and "调用示例" in rows[0].values()]
    if len(candidates) != 1:
        raise ValueError("Select one verified MCP catalog sheet")
    segments = join_segments(sheets)
    contracts = {}
    issues = []
    for line, row in enumerate(named_rows(candidates[0]), 2):
        code, version = row["MCP编码"].strip(), row["在线版本"].strip()
        if not code:
            continue
        if code in contracts or not re.fullmatch(r"tool_[a-z0-9]+", code):
            raise ValueError("Ambiguous MCP code: " + code)
        record = {
            "code": code, "name": row["MCP名称"], "version": version,
            "operation_type": row["操作类型"], "verification_status": row["核验状态"],
            "source_row": line, "notes": row["备注"], "source_example": row["调用示例"],
            "schema_available": False, "example_available": False,
            "business_call_executed_by_pipeline": False,
        }
        try:
            raw = segments.get((code, "请求参数"), row["请求参数"])
            parameters = json.loads(raw)
            if not isinstance(parameters, list):
                raise ValueError("The source explicitly has no available public schema")
            record.update(parameters=parameters, request_schema=schema_parameters(parameters), schema_available=True)
            record["request_template"] = placeholder(record["request_schema"])
        except (ValueError, KeyError, TypeError) as error:
            record["schema_error"] = str(error)
        try:
            params = example_params(row["调用示例"], code, version)
            record.update(example_params=params, example_command=invoke_command(code, version, params), example_available=True)
            if record["schema_available"]:
                record["example_schema_discrepancies"] = validate(params, record["request_schema"])
        except (ValueError, KeyError, TypeError) as error:
            record["example_error"] = str(error)
        record["available"] = (
            record["schema_available"] and record["example_available"]
            and row["核验状态"] not in {"调用失败", "已调通｜参数不被接受"}
        )
        if not record["available"] or record.get("example_schema_discrepancies"):
            issues.append({"code": code, "status": row["核验状态"], "schema_error": record.get("schema_error"),
                           "example_error": record.get("example_error"), "example_schema_discrepancies": record.get("example_schema_discrepancies", [])})
        contracts[code] = record
    return {
        "source": source, "source_sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        "contracts": contracts, "issues": issues,
        "continuation_fields_restored": len(segments), "business_calls_executed": 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source", default=SOURCE)
    args = parser.parse_args()
    result = load_catalog(args.workbook, args.source)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps({
        "codes": len(result["contracts"]), "issues": len(result["issues"]),
        "continuation_fields_restored": result["continuation_fields_restored"],
        "business_calls_executed": 0, "source_sha256": result["source_sha256"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
