# Copilot Instructions

## Git Push / Commit の禁止

`git push` および `git commit` は原則実行しないこと。  
ただし、ユーザーから明示的な承認（「OK」「コミットして」等）を得た場合は実行してよい。

## ファイル変更時の差分確認とコミット承認フロー

ファイルの新規作成・編集・削除を行った場合、および `git add` / `git commit` を提案する前に、
**必ず以下の手順を守ること**。

1. **差分をユーザーに提示する**  
   `git diff`（追跡済みファイル）および新規ファイルの内容を表示する。

2. **承認を求める**  
   「この差分でコミットしてよいですか？」とユーザーに確認し、明示的な承認（「OK」「承認」等）を得る。

3. **承認後にステージング・コミット・プッシュを実行する**  
   承認を得てから `git add` → `git commit` → `git push` の順で実行する。

## アプリケーションについての問い合わせ

ユーザーからアプリケーションの仕様・構成・設計について質問があった場合は、
まず `docs/` ディレクトリのドキュメントを参照し、その内容に基づいて回答すること。

- アーキテクチャに関する質問 → `docs/architecture.md` を参照
- ドキュメントに記載がない場合はコードを調査した上で回答し、必要であればドキュメントの更新を提案すること

## コミットメッセージ規約

コミットメッセージは **Conventional Commits** のガイドラインに従うこと。

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

主な type：

| type | 用途 |
|------|------|
| `feat` | 新機能の追加 |
| `fix` | バグ修正 |
| `docs` | ドキュメントのみの変更 |
| `style` | フォーマット・lint 修正（動作変更なし） |
| `refactor` | リファクタリング（機能追加・バグ修正なし） |
| `test` | テストの追加・修正 |
| `chore` | ビルド・設定・依存関係の変更 |

例：
```
feat(api): add /items endpoint
fix(auth): handle expired token correctly
docs: update architecture diagram
chore: add ruff and pytest to dev dependencies
```

## コミット前の必須手順

コードをコミットする前に、必ず以下を実行してください。

1. **Format / Lint チェック**
   ```bash
   uv run ruff check .
   uv run ruff format --check .
   ```

2. **テスト実行**
   ```bash
   uv run pytest -v
   ```

3. **コードレビュー**  
   `/review` コマンドでコードレビューを実施し、指摘事項をすべて解消してから `git commit` を行うこと。

4. **`docs/` の更新（必須・毎回）**  
   コミット内容に関わらず、**毎回** `docs/` 配下のドキュメントを最新状態に更新してから `git commit` を行うこと。  
   特に以下に変更が生じた場合は必ず対応する箇所を更新すること。

   | 変更内容 | 更新対象 |
   |---------|---------|
   | 技術スタック（ライブラリ追加・削除・バージョン変更） | `docs/architecture.md` |
   | コンポーネント構成（モジュール・レイヤーの追加・削除） | `docs/architecture.md` |
   | エンドポイント一覧（追加・削除・パス変更） | `docs/architecture.md` |
   | ファイル構成（ディレクトリ・ファイルの追加・削除・移動） | `docs/architecture.md` |
   | セットアップ手順・環境変数・起動方法の変更 | `README.md` |

   > ドキュメントの更新を `git diff` で確認し、ユーザーへの差分提示に必ず含めること。

上記がすべて成功するまでコミットを提案しないこと。
