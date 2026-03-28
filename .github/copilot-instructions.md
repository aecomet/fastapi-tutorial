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

4. **アーキテクチャドキュメントの更新**  
   以下のいずれかに変更が生じた場合は `docs/architecture.md` を更新してから `git commit` を行うこと。
   - 技術スタック（ライブラリ・フレームワークの追加・削除・バージョン変更）
   - コンポーネント構成（新規モジュール・レイヤーの追加・削除）
   - エンドポイント一覧（追加・削除・パス変更）
   - ファイル構成（ディレクトリ・ファイルの追加・削除・移動）

上記がすべて成功するまでコミットを提案しないこと。
