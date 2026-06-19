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

---

## 🎨 v2: STUDIOデザイン寄せ版（2026-06-14）
旧STUDIOサイトの配色・レイアウトに寄せて全面リデザイン。
- 配色: 青 `#008dcb`（主CTA）／紫 `#5001b9`（副CTA）／文字 `#222`（STUDIOから抽出）
- 構成: 写真ヒーロー＋2色CTA → 実績バー → 自己紹介動画 → LESSON&TOUR 2カラム → PODCAST → PROFILE → CONTACTフォーム → LINKS

### 差し替えが必要な写真（`assets/img/photos/` に同名で上書き）
| ファイル | 用途 | 推奨サイズ |
|---|---|---|
| `hero.jpg` | ヒーロー背景（ユウキの写真） | 1600×1000 以上・横長 |
| `lesson.jpg` | 日本語レッスンカード | 1000×750・横長 |
| `tour.jpg` | 秋葉原ツアーカード | 1000×750・横長 |
| `profile.jpg` | （任意・未使用枠） | 縦長 |
※ 現状はプレースホルダ画像。STUDIOで使っている写真をそのまま入れればOK。

### お問い合わせフォーム（Googleフォーム運用）
静的サイトなので自前フォームは使わず、Googleフォームに飛ばす方式。
- 公開フォーム: https://forms.gle/Ea7aasF5zmgrfWHv9 （お名前・メールアドレス・メッセージ）
- 回答は連携スプレッドシートに自動集計（所有者のGoogleアカウント）
- 再生成スクリプト: `build/create_contact_form.gs`（script.google.com に貼って `createContactForm` を実行）
- サイト側は CONTACT セクションの「お問い合わせフォームを開く」ボタンがこのURLを指す。差し替えるときはそのリンクを変更。
※ 「メールで直接」リンク（mailto）はフォールバックとして併記。

### 自己紹介動画
`index.html` の `data-todo="youtube-intro"` の `<a href="#">` に動画URLを入れる（埋め込みに変更も可）。
