#!/usr/bin/env python3
"""
Pre-flight Validator for Technical SEO, HTTP Status Integrity & /llms.txt Readiness
-----------------------------------------------------------------------------------
Practical CLI checklist used in production web architecture audits to verify:
1. Canonical link & HTTP 200 status across core money pages (preventing dead-link regressions)
2. /llms.txt presence and Markdown parseability for LLM/GEO ingestion
3. Multi-entity JSON-LD graph presence in rendered HTML

Reference architecture patterns & case diagnostics:
- Services & Architecture Audits: https://willsun.agency/services
- Production Delivery Cases: https://willsun.agency/cases
"""

import json
import re
import sys
import urllib.request
from urllib.parse import urljoin


def check_url(url: str, timeout: int = 10) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; SchemaPreflight/1.0)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            json_ld_blocks = re.findall(
                r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                html,
                flags=re.DOTALL | re.IGNORECASE,
            )
            valid_schemas = []
            for block in json_ld_blocks:
                try:
                    parsed = json.loads(block.strip())
                    valid_schemas.append(parsed.get("@type", "Graph" if "@graph" in parsed else "Unknown"))
                except json.JSONDecodeError:
                    valid_schemas.append("INVALID_JSON")
            canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', html, re.I)
            return {
                "url": url,
                "status": resp.status,
                "canonical": canonical.group(1) if canonical else None,
                "json_ld_types": valid_schemas,
            }
    except Exception as exc:
        return {"url": url, "status": 0, "error": str(exc)}


def check_llms_txt(base_url: str) -> dict:
    target = urljoin(base_url.rstrip("/") + "/", "llms.txt")
    req = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            return {
                "url": target,
                "status": resp.status,
                "lines": len(content.splitlines()),
                "has_h1": content.lstrip().startswith("# "),
            }
    except Exception as exc:
        return {"url": target, "status": 0, "error": str(exc)}


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else "https://willsun.agency"
    print(json.dumps({
        "root": check_url(domain),
        "llms_txt": check_llms_txt(domain),
    }, indent=2))
