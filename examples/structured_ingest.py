#!/usr/bin/env python3
"""Illustrative HTML → structured, traceable passages. NOT a PDF/OCR engine.

No external dependencies. ACL fields are labels, not an authorization check.
For production, enforce access control before retrieval and keep source versions.
"""
from __future__ import annotations
import hashlib
import json
from html.parser import HTMLParser


class StructureParser(HTMLParser):
    """Read basic HTML headings/paragraphs and preserve 2D table associations."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks: list[dict[str, str]] = []
        self.section = "未标记章节"
        self.kind: str | None = None
        self.buffer: list[str] = []
        self.table_rows: list[list[str]] | None = None
        self.row: list[str] | None = None
        self.cell: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3", "p", "li") and self.table_rows is None:
            self.kind, self.buffer = tag, []
        elif tag == "table":
            self.table_rows = []
        elif tag == "tr" and self.table_rows is not None:
            self.row = []
        elif tag in ("th", "td") and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)
        elif self.kind is not None:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        if tag in ("th", "td") and self.cell is not None and self.row is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None and self.table_rows is not None:
            self.table_rows.append(self.row)
            self.row = None
        elif tag == "table" and self.table_rows is not None:
            rows = self.table_rows
            if rows:
                headers = rows[0]
                for index, row in enumerate(rows[1:], 1):
                    cells = [
                        f"{headers[i] if i < len(headers) else f'列{i + 1}'}：{value}"
                        for i, value in enumerate(row)
                    ]
                    self.blocks.append({
                        "kind": "table_row", "section": self.section,
                        "locator": f"table:row:{index}", "text": "；".join(cells)
                    })
            self.table_rows = None
        elif tag == self.kind:
            text = " ".join("".join(self.buffer).split())
            if text:
                if tag.startswith("h"):
                    self.section = text
                self.blocks.append({
                    "kind": "heading" if tag.startswith("h") else "text",
                    "section": self.section,
                    "locator": f"element:{len(self.blocks) + 1}",
                    "text": text
                })
            self.kind, self.buffer = None, []


def ingest_html(html: str, source_id: str, version: str, access_group: str):
    """Return normalized blocks with deterministic content IDs and provenance."""
    parser = StructureParser()
    parser.feed(html)
    parser.close()
    digest = hashlib.sha256(html.encode("utf-8")).hexdigest()
    result = []
    for index, block in enumerate(parser.blocks):
        payload = f"{source_id}\x00{version}\x00{index}\x00{block['text']}"
        record = {
            "chunk_id": hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16],
            "source_id": source_id, "version": version, "access_group": access_group,
            "source_sha256": digest, **block,
        }
        result.append(record)
    return result


EXAMPLE_HTML = """<h2>退款规则（示例）</h2>
<p>仅适用于2026版购买记录。</p>
<table><tr><th>地区</th><th>退款时限</th></tr>
<tr><td>中国大陆</td><td>7天</td></tr>
<tr><td>其他地区</td><td>以当地规则为准</td></tr></table>"""


if __name__ == "__main__":
    records = ingest_html(EXAMPLE_HTML, "policy:refund", "2026", "support")
    assert any("地区：中国大陆；退款时限：7天" in item["text"] for item in records)
    print(json.dumps(records, ensure_ascii=False, indent=2))
