#!/usr/bin/env python3
"""
PODCASTカード再生成スクリプト
- build/podcasts.json を元に index.html の
  <!-- PODCAST_CARDS_START --> ... <!-- PODCAST_CARDS_END --> 区間を書き換える。
- show に "rss" URLがあれば最新エピソードのタイトル/日付を取得して説明文に追記する（任意）。
- RSSが空・取得失敗の場合は podcasts.json の desc をそのまま使う（壊れない設計）。

使い方:  python3 build/refresh_podcasts.py
launchdで毎日自動実行する場合は README.md 参照。
標準ライブラリのみで動作（外部依存なし）。
"""
import json, os, re, sys, html, urllib.request, xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
DATA = os.path.join(ROOT, "build", "podcasts.json")
START = "<!-- PODCAST_CARDS_START (build/refresh_podcasts.py がこの区間を再生成) -->"
END = "<!-- PODCAST_CARDS_END -->"

def latest_episode(rss_url):
    """RSSから最新エピソードの (title, pubdate) を返す。失敗時は None。"""
    if not rss_url:
        return None
    try:
        req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0 (animesensei-build)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read()
        root = ET.fromstring(raw)
        item = root.find(".//item")
        if item is None:
            return None
        title = (item.findtext("title") or "").strip()
        return title or None
    except Exception as e:
        print(f"  [warn] RSS取得失敗 ({rss_url}): {e}", file=sys.stderr)
        return None

def esc(s):
    return html.escape(s, quote=True)

def build_cards(shows):
    out = ['      <div class="pod-grid">']
    for s in shows:
        desc = s.get("desc", "")
        ep = latest_episode(s.get("rss", ""))
        if ep:
            desc = f'{desc}<br><span style="color:var(--accent-ink);font-weight:700">最新: {esc(ep)}</span>'
        else:
            desc = esc(desc)
        out.append(
            f'        <a class="pod" href="{esc(s["url"])}" target="_blank" rel="noopener">\n'
            f'          <img class="cover" src="{esc(s["cover"])}" alt="{esc(s["name"])}" loading="lazy" width="600" height="600">\n'
            f'          <div class="body"><div class="pname">{esc(s["name"])}</div>'
            f'<div class="pdesc">{desc}</div><div class="plink">聴く →</div></div>\n'
            f'        </a>'
        )
    out.append('      </div>')
    return "\n".join(out)

def main():
    with open(DATA, encoding="utf-8") as f:
        shows = json.load(f)["shows"]
    with open(INDEX, encoding="utf-8") as f:
        htmltext = f.read()
    if START not in htmltext or END not in htmltext:
        print("[error] index.html にカードのマーカーが見つかりません", file=sys.stderr)
        sys.exit(1)
    cards = build_cards(shows)
    new = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        START + "\n" + cards + "\n      " + END,
        htmltext, flags=re.DOTALL,
    )
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"[ok] {len(shows)}番組のカードを再生成しました → index.html")

if __name__ == "__main__":
    main()
