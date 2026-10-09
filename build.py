#!/usr/bin/env python3
"""
Simple SSI processor for GitHub Pages deployment.
Processes <!--#include virtual="..." --> directives in .shtml files.
"""
import os
import re
import sys
import shutil
from pathlib import Path


def process_ssi(content, base_dir):
    """Process SSI include directives in content."""
    pattern = re.compile(r'<!--\s*#include\s+virtual="([^"]+)"\s*-->')

    def replace_include(match):
        include_path = match.group(1)
        full_path = os.path.join(base_dir, include_path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            try:
                with open(full_path, "r", encoding="utf-8") as inc:
                    return inc.read()
            except Exception as e:
                return f"<!-- Error including {include_path}: {e} -->"
        return f"<!-- File not found: {include_path} -->"

    return pattern.sub(replace_include, content)


def main():
    src_dir = Path(".")
    out_dir = Path("_site")
    out_dir.mkdir(exist_ok=True)

    # Process all .shtml files
    for shtml_file in src_dir.glob("*.shtml"):
        with open(shtml_file, "r", encoding="utf-8") as f:
            content = f.read()

        processed = process_ssi(content, str(src_dir))
        html_file = out_dir / f"{shtml_file.stem}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(processed)
        print(f"Processed: {shtml_file} -> {html_file}")

    # Copy assets
    for asset in ["images", "audio", "presse", "partials", "style.css", "favicon.jpg", ".nojekyll"]:
        src = src_dir / asset
        dst = out_dir / asset
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            print(f"Copied: {asset}")

    print(f"\nBuild complete. Output in {out_dir}/")


if __name__ == "__main__":
    main()