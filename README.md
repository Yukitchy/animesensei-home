# アニメ先生ユウキ — 自前ホームページ（B案・静的サイト）

STUDIO（無料プラン）の制約（コンテンツが古いまま／AIクローラーに本文が届かない／GA連携が有料）を解消するための**自前再構築版**。純HTMLなのでAI検索クローラーにも全文が届き、GA4も無料で設置でき、RSSから番組情報を自動更新できる。

## 構成
```
index.html            ... トップ（日本語）。PODCASTカードは静的HTML（AI/SEO向け）
en/index.html         ... 英語版（訪日ゲスト・ツアー予約導線）
assets/
  img/podcast/*.jpg   ... 番組カバー7枚
  img/og.jpg          ... OGP画像(1200x630) ※将来あなたの写真版に差し替え推奨
  img/favicon.svg     ... ファビコン
  img/qr-site.png     ... サイトURLのQR（名刺・印刷用）
  files/yuuki.vcf     ... デジタル名刺（タップで連絡先保存）
build/
  podcasts.json       ... PODCASTカードの元データ（ここを編集）
  refresh_podcasts.py ... 上記からカードを再生成（RSSがあれば最新話も追記）
llms.txt robots.txt sitemap.xml ... AI検索/SEO向けメタ
```

## ローカル確認
```
cd ~/Projects/animesensei-home
python3 -m http.server 8770
# → http://localhost:8770/  と  http://localhost:8770/en/
```

## ✅ 公開前にやること（プレースホルダの置換）
1. **ドメイン**: 全ファイルの `https://animesensei.jp/` を実ドメインに置換
   （GitHub Pagesなら `https://<user>.github.io/<repo>/` 等。独自ドメイン取得済みならそれ）
   ```
   cd ~/Projects/animesensei-home
   grep -rl 'animesensei.jp' . | xargs sed -i '' 's#https://animesensei.jp#https://本番URL#g'
   ```
2. **SNSリンク**: index.html 末尾 LINKS の `data-todo`（X / YouTube / note）に実URLを入れる
3. **ツアー予約**: `https://www.airbnb.jp/` を実際のAirbnb体験ページURLに変更（ja/en両方）
4. **OG画像**: `assets/img/og.jpg` をあなたの写真入り1200x630に差し替えると共有見栄えUP（任意）
5. **GA4**: 下記参照

## 📊 GA4（Google Analytics）設定 — 自前なら無料
1. https://analytics.google.com/ でプロパティ作成 → 測定ID `G-XXXXXXXXXX` を取得
2. `index.html`（と `en/index.html`）の `<head>` 内、GA4コメントブロックを**コメント解除**し、
   `G-XXXXXXXXXX` を実IDに2か所置換するだけ
   ```bash
   sed -i '' 's/G-XXXXXXXXXX/G-実ID/g' index.html en/index.html
   # その後コメント <!-- --> を外す
   ```
※ STUDIO無料プランではこれが有料ロックだったが、自前ホスティングなら無料で設置できる。

## 🚀 デプロイ（GitHub Pages 無料・推奨）
```bash
cd ~/Projects/animesensei-home
git init && git add -A && git commit -m "init: self-hosted homepage"
gh repo create animesensei-home --public --source=. --push   # 要 gh ログイン
# GitHub → Settings → Pages → Source: main / root を選択
```
独自ドメインを使う場合は Pages の Custom domain にドメインを設定し、DNSにCNAME。

## 🔁 番組情報の自動更新（任意）
`build/podcasts.json` を編集 → 再生成:
```bash
python3 build/refresh_podcasts.py
```
各番組の `rss` にRSS URLを入れると、最新エピソード名が自動でカードに追記される。
毎日自動更新したい場合は launchd 登録（`~/Library/LaunchAgents/com.yuki.animesensei-home-refresh.plist`）:
- ProgramArguments: `python3 /Users/yuki/Projects/animesensei-home/build/refresh_podcasts.py`
- StartCalendarInterval: 毎朝6時 等
- 更新後に `git commit && git push` するシェルを噛ませれば本番も自動反映

## デザイン方針（ユウキの好みに準拠）
- 入口で価格を出さない（料金は予約ページで）／「銭ゲバ」回避
- 視認性優先：白基調＋強い色（アクセントのピンク）は点（CTA・タグ・マーカー）でのみ使用
- 楽しさ・人柄・実績で選んでもらう（プロフィールに正直な「苦手」も掲載）
