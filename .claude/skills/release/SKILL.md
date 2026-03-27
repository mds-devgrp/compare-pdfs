---
name: release
description: Create a version tag and push it to trigger the GitHub Actions release workflow
argument-hint: <version> (e.g. 0.1.0)
disable-model-invocation: true
allowed-tools: Bash, Read, Grep
---

# Release v$ARGUMENTS

バージョン `$ARGUMENTS` のリリースを実行する。

## 事前チェック

1. バージョン番号の形式を検証（`X.Y.Z` の semver 形式であること）
2. 現在のブランチが `main` であることを確認: `git branch --show-current`
3. ワーキングツリーがクリーンであることを確認: `git status --porcelain`
4. リモートと同期済みであることを確認: `git fetch origin && git status`
5. タグ `v$ARGUMENTS` が既に存在しないことを確認: `git tag -l "v$ARGUMENTS"`
6. GitHub Actions ワークフロー `.github/workflows/release.yml` が存在することを確認

いずれかのチェックが失敗した場合は、理由を説明して中断する。

## リリース実行

すべてのチェックが通った場合のみ、以下を実行する:

1. タグを作成: `git tag v$ARGUMENTS`
2. タグを push: `git push origin v$ARGUMENTS`

## 完了報告

以下を報告する:
- 作成したタグ名
- GitHub Actions の実行確認 URL: `https://github.com/mds-devgrp/pdf-layout-diff/actions`
- Release ページ URL: `https://github.com/mds-devgrp/pdf-layout-diff/releases/tag/v$ARGUMENTS`
