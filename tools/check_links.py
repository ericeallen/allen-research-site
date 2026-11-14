"""Check every external link on the built site: python tools/check_links.py [site-directory]

Prints one line per link and exits non-zero if any link is dead. A link counts
as dead on a DNS failure, a refused connection, or a 404/410. Publishers that
refuse automated requests (403, 429, 999, or a timeout) are reported as
"unverified": the checker cannot see past the refusal, so those need a human
click, not a conclusion.
"""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Final

USER_AGENT: Final = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
)
DEAD_STATUSES: Final = frozenset({404, 410})
TIMEOUT_SECONDS: Final = 25


@dataclass(frozen=True)
class Result:
    url: str
    verdict: str
    detail: str


def external_links(site: Path) -> tuple[str, ...]:
    # Anchors only: the canonical <link> names this site's own address.
    pattern = re.compile(r'<a href="(https?://[^"]+)"')
    found = {
        match.replace("&amp;", "&")
        for page in site.rglob("*.html")
        for match in pattern.findall(page.read_text(encoding="utf-8"))
    }
    return tuple(sorted(found))


def check(url: str) -> Result:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return Result(url, "ok", str(response.status))
    except urllib.error.HTTPError as error:
        verdict = "DEAD" if error.code in DEAD_STATUSES else "unverified"
        return Result(url, verdict, f"HTTP {error.code}")
    except TimeoutError:
        return Result(url, "unverified", "timed out")
    except urllib.error.URLError as error:
        timed_out = isinstance(error.reason, TimeoutError)
        return Result(url, "unverified" if timed_out else "DEAD", str(error.reason))


def main(argv: list[str]) -> int:
    site = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent / "_site"
    if not site.is_dir():
        print(f"{site} is not a directory; build the site first", file=sys.stderr)
        return 2
    links = external_links(site)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(check, links))
    for result in results:
        print(f"{result.verdict:<11}{result.detail:<28}{result.url}", flush=True)
    counts = {v: sum(r.verdict == v for r in results) for v in ("ok", "unverified", "DEAD")}
    print(
        f"\n{len(results)} links: {counts['ok']} ok, {counts['unverified']} unverified, {counts['DEAD']} dead"
    )
    return 1 if counts["DEAD"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
