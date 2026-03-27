---
name: pr-review-respond
description: PR のレビューコメント (Copilot 等) を評価し、コード修正・返信・解決を行う。
user-invocable: true
argument-hint: <pr-number>
allowed-tools: Bash(gh repo view:*), Bash(gh pr view:*), Bash(gh api:*), Bash(git add:*), Bash(git commit:*), Bash(git push), Edit, Read, Write
---

# PR レビューコメント対応

PR #$ARGUMENTS のレビューコメントを評価し、必要に応じてコード修正・返信・解決を行う。

## リポジトリ検出

コマンド実行前に、現在のリポジトリのオーナーと名前を取得する:

```bash
gh repo view --json owner,name --jq ".owner.login + \"/\" + .name"
```

以降、`{owner}/{repo}` として使用する。

## ワークフロー

1. PR のレビュースレッドを解決状態付きで取得
2. 既に解決済みのスレッド (`isResolved: true`) はスキップ
3. 未解決コメントを評価し、アクションを決定 (コード修正 / 返信のみ / 却下)
4. コード修正が必要な場合は修正してコミット
5. 各スレッドに返信してから解決

## コマンドリファレンス

> **Windows 互換性について**: GraphQL クエリはマルチライン文字列の代わりに一時ファイル経由で渡す。
> これにより CRLF 改行や引用符のエスケープ問題を回避できる。

### 1. PR レビュー・コメント概要の取得

```bash
gh pr view {pr_number} --json reviews,comments
```

### 2. レビューコメント詳細の取得

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
```

### 3. スレッド ID 付きレビュースレッドの取得 (返信・解決に必須)

Write ツールで以下の内容を `.temp/gql-threads.json` に書き出してから実行する (`.temp/` が無ければ先に作成):

```json
{
  "query": "query { repository(owner: \"{owner}\", name: \"{repo}\") { pullRequest(number: {pr_number}) { reviewThreads(first: 50) { nodes { id isResolved comments(first: 10) { nodes { id databaseId body path line diffHunk } } } } } } }"
}
```

```bash
gh api graphql --input .temp/gql-threads.json
```

### 4. レビュースレッドへの返信

Write ツールで以下の内容を `.temp/gql-reply.json` に書き出してから実行する。
`{reply_message}` 内のダブルクォートや改行は JSON エスケープすること。

```json
{
  "query": "mutation { addPullRequestReviewThreadReply(input: { pullRequestReviewThreadId: \"{thread_id}\", body: \"{reply_message}\" }) { comment { id } } }"
}
```

```bash
gh api graphql --input .temp/gql-reply.json
```

### 5. レビュースレッドの解決

Write ツールで以下の内容を `.temp/gql-resolve.json` に書き出してから実行する:

```json
{
  "query": "mutation { resolveReviewThread(input: { threadId: \"{thread_id}\" }) { thread { isResolved } } }"
}
```

```bash
gh api graphql --input .temp/gql-resolve.json
```

## 注意事項

- `isResolved: true` のスレッドはスキップする — 対応不要
- スレッド ID (例: `PRRT_xxx`) はコメント ID とは異なり、GraphQL 経由で取得する必要がある
- 返信には `addPullRequestReviewThreadReply` ミューテーションを使用する (`addPullRequestReviewComment` ではない)
- REST API の `pulls/{pr}/comments/{id}/replies` は Copilot レビューコメントでは動作しない
- コンテキストを残すため、解決する前に必ず返信する
- コード修正時のコミットメッセージは日本語で記載すること
- レビュースレッドは `first: 50` で取得しているため、50 件を超える場合はページネーション (`pageInfo` / `after` カーソル) で追加取得すること
- 一時ファイル (`.temp/gql-*.json`) は使い捨て。`.temp/` ディレクトリが無ければ先に作成すること
