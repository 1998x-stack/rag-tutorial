#!/usr/bin/env python3
"""Chromium release smoke tests for the new homepage + chapters 01–03."""
from pathlib import Path
import json, sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
OUT = ROOT / "qa" / "browser"
OUT.mkdir(parents=True, exist_ok=True)
problems = []
results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width, height in ((1440, 900), (390, 844), (360, 800)):
        for name, path in [("home", SITE / "index.html")] + [
            (f"{n:02}", SITE / "chapters" / f"{n:02}.html") for n in (1, 2, 3)
        ]:
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            page_errors = []
            page.on("pageerror", lambda e: page_errors.append(str(e)))
            page.on("console", lambda m: page_errors.append(m.text) if m.type == "error" else None)
            try:
                page.goto(path.as_uri(), wait_until="load")
                page.locator("h1").first.wait_for()
                if page.locator("h1").count() != 1:
                    problems.append(f"{name}@{width}: expected exactly one H1")
                over = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
                if over:
                    problems.append(f"{name}@{width}: whole-page horizontal overflow")
                for img in page.locator("img").all():
                    if not img.evaluate("(e) => e.complete && e.naturalWidth > 0"):
                        problems.append(f"{name}@{width}: broken image {img.get_attribute('src')}")
                if name != "home":
                    mat = page.locator("math").count()
                    if mat:
                        visible = page.locator("math").first.evaluate(
                            "(e) => e.getBoundingClientRect().width > 0 && e.getBoundingClientRect().height > 0"
                        )
                        if not visible:
                            problems.append(f"{name}@{width}: math has zero geometry")
                    btn = page.locator("button[data-demo]")
                    if btn.count():
                        output = page.locator(f"#{btn.first.get_attribute('aria-controls')}")
                        before = output.inner_text()
                        btn.first.click()
                        if output.inner_text() == before:
                            problems.append(f"{name}@{width}: demo did not change output")
                    else:
                        problems.append(f"{name}@{width}: missing interactive example")
                page.screenshot(path=str(OUT / f"{name}-{width}.png"), full_page=True)
                if page_errors:
                    problems.extend([f"{name}@{width}: JS/console {e}" for e in page_errors])
                results.append({"page": name, "width": width, "h1": page.locator("h1").count(),
                                "images": page.locator("img").count(), "errors": len(page_errors)})
            except Exception as exc:
                problems.append(f"{name}@{width}: {exc}")
            finally:
                page.close()
    browser.close()
(OUT / "report.json").write_text(json.dumps(
    {"checks": results, "issues": problems}, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"screenshots": len(results), "issues": problems}, ensure_ascii=False, indent=2))
sys.exit(bool(problems))
