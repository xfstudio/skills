"""Remove header-identified credentials before resolving exported cell text."""
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.parsers import expat

NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
S = "{" + NS["s"] + "}"
CREDENTIAL_HEADERS = {
    "appkey", "appsecret", "tbtoken", "token", "accesstoken", "refreshtoken",
    "cookie", "cookies", "secret", "password", "密钥", "密码",
}
PACKAGE_HEADERS = {"技能包链接"}
UPLOAD_HEADERS = {"自建技能包", "自建技能包(产品上传)"}
CODE_HEADERS = {"技能code", "技能编码"}


def normalize_header(text):
    return re.sub(r"[\s_-]+", "", unicodedata.normalize("NFKC", text)).casefold()


def tag_end(data, start):
    quote = None
    for index in range(start, len(data)):
        char = data[index]
        if quote is not None:
            if char == quote:
                quote = None
        elif char in (34, 39):
            quote = char
        elif char == 62:
            return index + 1
    raise RuntimeError("Invalid shared-string XML tag")


class SharedStrings:
    """Index raw SI slices; only requested public/header strings are decoded."""

    def __init__(self, data):
        self.data = data
        self.spans = []
        self.opening = b""
        self.closing = b""
        depth = 0
        start = None
        parser = expat.ParserCreate()

        def reject_doctype(*_):
            raise RuntimeError("Shared-string DTD is not supported")

        def begin(name, _attributes):
            nonlocal depth, start
            if depth == 0:
                if name.split(":")[-1] != "sst":
                    raise RuntimeError("Invalid shared-string root")
                offset = parser.CurrentByteIndex
                self.opening = data[offset:tag_end(data, offset)]
                self.closing = b"</" + name.encode("utf-8") + b">"
            elif depth == 1 and name.split(":")[-1] == "si":
                start = parser.CurrentByteIndex
            depth += 1

        def end(name):
            nonlocal depth, start
            depth -= 1
            if depth == 1 and name.split(":")[-1] == "si" and start is not None:
                opening_end = tag_end(data, start)
                finish = opening_end if data[start:opening_end].rstrip().endswith(b"/>") else tag_end(data, parser.CurrentByteIndex)
                self.spans.append((start, finish))
                start = None

        parser.StartElementHandler = begin
        parser.EndElementHandler = end
        parser.StartDoctypeDeclHandler = reject_doctype
        parser.ExternalEntityRefHandler = lambda *_: 0
        # No character-data handler: do not materialize credential string bodies.
        parser.Parse(data, True)

    def __getitem__(self, index):
        if not 0 <= index < len(self.spans):
            raise RuntimeError("Invalid shared-string reference")
        start, end = self.spans[index]
        root = ET.fromstring(self.opening + self.data[start:end] + self.closing)
        return "".join(node.text or "" for node in root.iter(S + "t"))


class Worksheet:
    """Keep body cells as byte spans until credential columns have been removed."""

    def __init__(self, data):
        self.data, self.cells = data, []
        stack, active, row_number = [], None, None
        parser = expat.ParserCreate()

        def begin(name, attributes):
            nonlocal active, row_number
            local = name.split(":")[-1]
            if not stack:
                offset = parser.CurrentByteIndex
                self.opening = data[offset:tag_end(data, offset)]
                self.closing = b"</" + name.encode("utf-8") + b">"
            if local == "row" and stack[-1:] == ["sheetData"]:
                row_number = attributes.get("r")
            if local == "c" and stack[-2:] == ["sheetData", "row"]:
                reference = attributes.get("r", "")
                match = re.fullmatch(r"([A-Z]+)[1-9]\d*", reference)
                if not match:
                    raise RuntimeError("Invalid exported cell reference")
                active = {"start": parser.CurrentByteIndex, "depth": len(stack),
                          "row": row_number, "column": match.group(1),
                          "type": attributes.get("t"), "index_text": ""}
            if local == "v" and active is not None and active["type"] == "s" and stack[-1:] == ["c"]:
                parser.CharacterDataHandler = text
            stack.append(local)

        def text(value):
            if active is not None and active["type"] == "s" and stack[-1:] == ["v"]:
                active["index_text"] += value

        def end(name):
            nonlocal active
            local = name.split(":")[-1]
            if local == "v":
                parser.CharacterDataHandler = None
            stack.pop()
            if active is not None and local == "c" and len(stack) == active["depth"]:
                start = active["start"]
                opening_end = tag_end(data, start)
                active["end"] = opening_end if data[start:opening_end].rstrip().endswith(b"/>") else tag_end(data, parser.CurrentByteIndex)
                index = active.pop("index_text")
                try:
                    active["index"] = int(index) if re.fullmatch(r"\d+", index) else None
                except ValueError:
                    active["index"] = None
                self.cells.append(active)
                active = None

        def reject_doctype(*_):
            raise RuntimeError("Worksheet DTD is not supported")

        parser.StartElementHandler, parser.EndElementHandler = begin, end
        parser.StartDoctypeDeclHandler = reject_doctype
        parser.ExternalEntityRefHandler = lambda *_: 0
        parser.Parse(data, True)

    def headers(self, shared):
        headers = {}
        for record in self.cells:
            if record["row"] != "1":
                continue
            root = ET.fromstring(self.opening + self.data[record["start"]:record["end"]] + self.closing)
            cell = next(iter(root))
            col = column(cell)
            if col in headers:
                raise RuntimeError("Duplicate SOP header cell")
            headers[col] = cell_text(cell, shared)
        return headers

    def without_credentials(self, credentials, tainted_indices):
        parts, start = [], 0
        for cell in self.cells:
            if (cell["row"] != "1" and cell["column"] in credentials) or (
                cell["type"] == "s" and cell["index"] in tainted_indices
            ):
                parts.append(self.data[start:cell["start"]])
                start = cell["end"]
        return b"".join(parts) + self.data[start:]


def column(cell):
    match = re.fullmatch(r"([A-Z]+)[1-9]\d*", cell.get("r", ""))
    if not match:
        raise RuntimeError("Invalid exported cell reference")
    return match.group(1)


def shared_index(cell):
    value = cell.find("s:v", NS)
    text = value.text if value is not None else None
    if text is None or not re.fullmatch(r"\d+", text):
        return None
    try:
        return int(text)
    except ValueError:
        return None


def cell_text(cell, shared):
    value = cell.find("s:v", NS)
    if cell.get("t") == "s":
        index = shared_index(cell)
        if index is None:
            raise RuntimeError("Invalid shared-string reference")
        return shared[index]
    if cell.get("t") == "inlineStr":
        return "".join(node.text or "" for node in cell.iter(S + "t"))
    return value.text or "" if value is not None else ""


def sheet_layout(headers):
    normalized = {col: normalize_header(text) for col, text in headers.items()}
    matches = lambda labels: [col for col, text in normalized.items() if text in labels]
    names, statuses = matches({"技能名称"}), matches({"同步状态"})
    credentials = set(matches(CREDENTIAL_HEADERS))
    if not names and not statuses:
        return None, credentials
    # 技能编码 is a business identifier when a formal 技能code column exists.
    codes = matches({"技能code"}) or matches({"技能编码"})
    roles = [names, statuses, matches(PACKAGE_HEADERS), matches(UPLOAD_HEADERS), codes]
    if any(len(cols) > 1 for cols in roles) or len(matches({"appkey"})) > 1 or len(matches({"appsecret"})) > 1:
        raise RuntimeError("Ambiguous SOP headers")
    if all(len(cols) == 1 for cols in roles) and matches({"appkey"}) and matches({"appsecret"}):
        return roles[2][0], credentials
    # Compatibility with old minimal ATP exports whose credential headers are blank.
    # Never apply this positional fallback over an explicitly labelled business column.
    legacy = {"A": {"技能名称"}, "AD": {"同步状态"}, "H": PACKAGE_HEADERS,
              "I": UPLOAD_HEADERS, "J": CODE_HEADERS, "Z": {"appkey"}, "AA": {"appsecret"}}
    if names == ["A"] and statuses == ["AD"] and all(
        not normalized.get(col) or normalized[col] in allowed for col, allowed in legacy.items()
    ):
        return "H", credentials | {"Z", "AA"}
    raise RuntimeError("Unrecognized SOP headers")


def redact(path):
    path = Path(path).resolve()
    with zipfile.ZipFile(path) as archive:
        entries = {name: archive.read(name) for name in archive.namelist()}
    shared = SharedStrings(entries["xl/sharedStrings.xml"]) if "xl/sharedStrings.xml" in entries else []
    sheets, candidates, credential_indices = [], [], set()
    for name, data in entries.items():
        if not re.fullmatch(r"xl/worksheets/sheet[^/]*\.xml", name):
            continue
        worksheet = Worksheet(data)
        link_column, credentials = sheet_layout(worksheet.headers(shared))
        sheets.append((name, worksheet, link_column, credentials))
        if link_column is not None:
            candidates.append(name)
        for cell in worksheet.cells:
            if cell["row"] != "1" and cell["column"] in credentials and cell["type"] == "s" and cell["index"] is not None:
                credential_indices.add(cell["index"])
    # Refuse ambiguous/unknown exports before changing any file or decoding body cells.
    if len(candidates) != 1:
        raise RuntimeError("Multiple candidate SOP sheets" if candidates else "SOP sheet not found")
    rows = None
    for name, worksheet, link_column, credentials in sheets:
        root = ET.fromstring(worksheet.without_credentials(credentials, credential_indices))
        sheet_rows = root.findall(".//s:sheetData/s:row", NS)
        decoded_rows = []
        for row in sheet_rows:
            values = {}
            for cell in row.findall("s:c", NS):
                col = column(cell)
                if (row.get("r") != "1" and col in credentials) or (
                    cell.get("t") == "s" and shared_index(cell) in credential_indices
                ):
                    row.remove(cell)
                    continue
                text = cell_text(cell, shared)
                formula = cell.find("s:f", NS)
                if cell.get("t") == "s":
                    value = cell.find("s:v", NS)
                    if formula is not None:
                        cell.set("t", "str")
                        value.text = text
                    else:
                        cell.remove(value)
                        cell.set("t", "inlineStr")
                        inline = ET.SubElement(cell, S + "is")
                        ET.SubElement(inline, S + "t", {"{http://www.w3.org/XML/1998/namespace}space": "preserve"}).text = text
                if text:
                    values[col] = text
                if col == link_column and formula is not None:
                    match = re.search(r'HYPERLINK\("([^"]+)"', formula.text or "", re.I)
                    if match:
                        values["source_url"] = match.group(1)
            decoded_rows.append(values)
        entries[name] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        if name == candidates[0]:
            rows = decoded_rows
    entries.pop("xl/sharedStrings.xml", None)
    for name in ["[Content_Types].xml", "xl/_rels/workbook.xml.rels"]:
        root = ET.fromstring(entries[name])
        for element in list(root):
            if "sharedStrings" in str(element.attrib):
                root.remove(element)
        entries[name] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    temporary = path.with_suffix(".redacted.tmp")
    with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in entries.items():
            archive.writestr(name, data)
    temporary.replace(path)
    path.with_suffix(".json").write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    return {"records": len(rows) - 1, "credential_columns_removed": True}


if __name__ == "__main__":
    print(json.dumps(redact(sys.argv[1])))
