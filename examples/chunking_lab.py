#!/usr/bin/env python3
"""Character-unit chunking baseline and heading-aware parent/child records.

Units are Python Unicode code points, NOT LLM tokens. No semantic model is used.
"""
from __future__ import annotations
import json
from math import ceil


def fixed_windows(text: str, size: int, overlap: int = 0):
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("require size > 0 and 0 <= overlap < size")
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append({"start": start, "end": end, "text": text[start:end]})
        if end == len(text):
            break
        start = end - overlap
    return chunks


def expected_windows(length: int, size: int, overlap: int = 0):
    if length < 0 or size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("invalid window configuration")
    if length == 0:
        return 0
    if length <= size:
        return 1
    return 1 + ceil((length - size) / (size - overlap))


def section_spans(text: str):
    """Preserve original characters and offsets while splitting at ## headings."""
    result, current, title = [], 0, "文档开头"
    cursor = 0
    for line in text.splitlines(keepends=True):
        if line.startswith("## ") and cursor > current:
            result.append({"start": current, "end": cursor,
                           "title": title, "text": text[current:cursor]})
            current = cursor
        if line.startswith("## "):
            title = line.strip()[3:]
        cursor += len(line)
    if cursor > current:
        result.append({"start": current, "end": cursor,
                       "title": title, "text": text[current:cursor]})
    return result


def parent_child_records(text: str, child_size: int, overlap: int = 0):
    parents = section_spans(text)
    children = []
    for p_idx, parent in enumerate(parents):
        for w in fixed_windows(parent["text"], child_size, overlap):
            children.append({
                "parent_id": f"P{p_idx + 1}", "section": parent["title"],
                "start": parent["start"] + w["start"],
                "end": parent["start"] + w["end"],
                "text": w["text"]
            })
    return parents, children


EXAMPLE = ("## 退款规则\n2026版付款后7天内可申请退款。"
           "\n请保留购买凭证。\n"
           "## 账户安全\n建议启用二次验证。\n")


if __name__ == "__main__":
    fixed = fixed_windows(EXAMPLE, size=16, overlap=4)
    parents, children = parent_child_records(EXAMPLE, child_size=16, overlap=4)
    assert len(fixed) == expected_windows(len(EXAMPLE), 16, 4)
    assert "".join(p["text"] for p in parents) == EXAMPLE
    print(json.dumps({"fixed": fixed, "parents": parents, "children": children},
                     ensure_ascii=False, indent=2))
