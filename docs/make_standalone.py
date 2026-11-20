"""Turn the artifact page sources into standalone, offline HTML files.

The artifact host wraps a page in <html>/<head>/<body> and loads Google Fonts. This adds
the document wrapper and inlines the (latin subset) fonts as base64 woff2, so each file
opens straight from disk with no network. Images are already embedded as data: URIs.

    python make_standalone.py src.html out.html [src2.html out2.html ...]
"""
import base64, re, sys, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
_cache: dict[str, str] = {}


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()


def inline_fonts(css_url: str) -> str:
    if css_url in _cache:
        return _cache[css_url]
    css = fetch(css_url.replace("&amp;", "&")).decode()
    # Keep only the latin blocks: Google serves one @font-face per unicode subset.
    blocks = re.findall(r"/\* ([\w-]+) \*/\s*(@font-face\s*{[^}]*})", css)
    out = []
    for subset, block in blocks:
        if subset != "latin":
            continue
        url = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
        data = base64.b64encode(fetch(url)).decode()
        out.append(block.replace(url, f"data:font/woff2;base64,{data}"))
    _cache[css_url] = "\n".join(out)
    return _cache[css_url]


def convert(src: str, dst: str) -> None:
    s = open(src, encoding="utf-8").read()
    title = re.search(r"<title>(.*?)</title>", s).group(1)
    s = s.replace(f"<title>{title}</title>", "", 1)
    s = re.sub(r'<meta name="claude:[^>]*>\s*', "", s)
    link = re.search(r'<link rel="stylesheet" href="(https://fonts.googleapis.com/[^"]+)">', s)
    if link:
        s = s.replace(link.group(0), f"<style>\n{inline_fonts(link.group(1))}\n</style>", 1)
    # Head = everything up to the end of the last <style>; the rest is body.
    cut = s.rindex("</style>") + len("</style>")
    head, body = s[:cut], s[cut:]
    page = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f"<title>{title}</title>\n{head.strip()}\n<style>body {{ margin: 0; }}</style>\n"
        f"</head>\n<body>\n{body.strip()}\n</body>\n</html>\n"
    )
    assert "googleapis" not in page and "gstatic" not in page
    open(dst, "w", encoding="utf-8").write(page)
    print(f"{dst}: {len(page) // 1024} KB")


if __name__ == "__main__":
    args = sys.argv[1:]
    for src, dst in zip(args[::2], args[1::2]):
        convert(src, dst)
