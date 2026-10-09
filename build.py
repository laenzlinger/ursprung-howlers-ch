#!/usr/bin/env python3
"""
Build script for GitHub Pages deployment.
- Processes SSI includes in .shtml files
- Minifies HTML output
- Generates sitemap.xml
- Copies static assets
"""
import os
import re
import sys
import shutil
from datetime import datetime
from pathlib import Path

try:
    import minify_html
    HAS_MINIFY = True
except ImportError:
    HAS_MINIFY = False
    print("Warning: minify_html not installed, skipping HTML minification")


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


def minify_html_content(content):
    """Minify HTML if minify_html is available."""
    if HAS_MINIFY:
        return minify_html.minify(content, minify_js=True, minify_css=True, remove_processing_instructions=True)
    return content


def generate_sitemap(pages, base_url, out_dir):
    """Generate sitemap.xml from list of pages."""
    today = datetime.now().strftime("%Y-%m-%d")
    urls = []
    for page in pages:
        urls.append(f"""  <url>
    <loc>{base_url}/{page}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{'1.0' if page == 'index.html' else '0.8'}</priority>
  </url>""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""

    sitemap_path = out_dir / "sitemap.xml"
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"Generated: sitemap.xml ({len(pages)} URLs)")


def main():
    src_dir = Path(".")
    out_dir = Path("_site")
    out_dir.mkdir(exist_ok=True)

    base_url = "https://laenzlinger.github.io/ursprung-howlers-ch"
    pages = []

    # Process all .shtml files
    for shtml_file in src_dir.glob("*.shtml"):
        with open(shtml_file, "r", encoding="utf-8") as f:
            content = f.read()

        processed = process_ssi(content, str(src_dir))
        processed = minify_html_content(processed)

        html_file = out_dir / f"{shtml_file.stem}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(processed)
        print(f"Processed: {shtml_file} -> {html_file}")

        if shtml_file.stem != "404":
            pages.append(f"{shtml_file.stem}.html")

    # Copy assets (exclude partials - not needed in production)
    for asset in ["images", "audio", "presse", "style.css", "favicon.jpg", ".nojekyll", "_headers", "robots.txt"]:
        src = src_dir / asset
        dst = out_dir / asset
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            print(f"Copied: {asset}")

    # Generate sitemap.xml
    generate_sitemap(pages, base_url, out_dir)

    print(f"\nBuild complete. Output in {out_dir}/")


if __name__ == "__main__":
    main()