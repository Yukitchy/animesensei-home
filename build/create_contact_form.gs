/**
 * お問い合わせ用 Googleフォームを、サイトの自前フォームと同じ質問で自動生成する。
 * 使い方:
 *   1) https://script.google.com で新規プロジェクト → このコードを貼り付け
 *   2) 関数 createContactForm を選んで「実行」→ 初回は権限を承認
 *   3) 「実行ログ」に出る ▼公開URL（回答用）と ▼編集URL、▼回答スプレッドシートURL を控える
 *   4) 公開URLをClaudeに渡す → サイトのお問い合わせをこのフォームに差し替え
 *
 * 既存サイトフォームの質問（index.html）:
 *   - お名前（必須）
 *   - メールアドレス（必須・メール形式）
 *   - メッセージ（必須・長文）
 */
function createContactForm() {
  var form = FormApp.create('お問い合わせ（アニメ先生ユウキ）');

  form.setTitle('お問い合わせ（アニメ先生ユウキ）');
  form.setDescription('レッスン・ツアー・取材・登壇・コラボのご相談はこちらから。');

  // 誰でも（Googleログイン不要で）回答できるように
  // ※ setRequireLogin はWorkspace有料アカウント専用。無料Gmailではデフォルトで誰でも回答可なので不要。
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setConfirmationMessage('お問い合わせありがとうございます。内容を確認のうえ、ご記入のメールアドレス宛にご連絡します。');

  // Q1 お名前（必須・短文）
  form.addTextItem()
    .setTitle('お名前')
    .setHelpText('例: 山田 太郎')
    .setRequired(true);

  // Q2 メールアドレス（必須・メール形式チェック）
  var emailValidation = FormApp.createTextValidation()
    .requireTextIsEmail()
    .setHelpText('正しいメールアドレスを入力してください')
    .build();
  form.addTextItem()
    .setTitle('メールアドレス')
    .setHelpText('返信先になります（例: you@example.com）')
    .setRequired(true)
    .setValidation(emailValidation);

  // Q3 メッセージ（必須・長文）
  form.addParagraphTextItem()
    .setTitle('メッセージ')
    .setHelpText('ご相談内容をお書きください')
    .setRequired(true);

  // 回答を集計するスプレッドシートを自動生成して連携
  var ss = SpreadsheetApp.create('お問い合わせ回答（アニメ先生ユウキ）');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  // 取りこぼし防止: 新着回答が来たらメール通知（任意・下を有効にしたい場合はUIから設定）
  // ※スクリプトからの通知ON切替はAPI制限があるため、フォーム編集画面の「回答」→ベルマークでONにしてください

  var publishedUrl = form.getPublishedUrl();
  var shortUrl = form.shortenFormUrl(publishedUrl);
  var editUrl = form.getEditUrl();
  var sheetUrl = ss.getUrl();

  Logger.log('▼ 公開URL（サイトに貼るのはコレ）: ' + publishedUrl);
  Logger.log('▼ 短縮URL: ' + shortUrl);
  Logger.log('▼ 編集URL（自分用）: ' + editUrl);
  Logger.log('▼ 回答スプレッドシート: ' + sheetUrl);

  return { publishedUrl: publishedUrl, shortUrl: shortUrl, editUrl: editUrl, sheetUrl: sheetUrl };
}
