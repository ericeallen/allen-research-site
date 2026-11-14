"""Build the site: python -m sitegen [output-directory]."""

from __future__ import annotations

import sys
from pathlib import Path

from sitegen.build import DEFAULT_OUT, build


def main(argv: list[str]) -> int:
    out = Path(argv[1]).resolve() if len(argv) > 1 else DEFAULT_OUT
    files = build(out)
    total = sum(path.stat().st_size for path in files)
    print(f"Wrote {len(files)} files ({total / 1024:.0f} KiB) to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
