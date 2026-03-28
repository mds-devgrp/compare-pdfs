# compare-pdfs

[![CI](https://github.com/mds-devgrp/compare-pdfs/actions/workflows/ci.yml/badge.svg)](https://github.com/mds-devgrp/compare-pdfs/actions/workflows/ci.yml)
[![Release](https://github.com/mds-devgrp/compare-pdfs/actions/workflows/release.yml/badge.svg)](https://github.com/mds-devgrp/compare-pdfs/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

PDFのレイアウト差分（微小ズレ含む）を自動検出するバッチツールです。

---

## クイックスタート

Python 不要で今すぐ使い始められます。

1. [Releases](https://github.com/mds-devgrp/compare-pdfs/releases) ページから最新の `compare-pdfs-*-win-x64.zip` をダウンロード
2. 任意のフォルダに展開
3. 比較したい PDF を `old`（旧）/ `new`（新）フォルダに配置（ファイル名を揃える）
4. コマンドプロンプトまたは PowerShell で実行:

```
compare_pdfs.exe --old-dir old --new-dir new --output-dir output
```

5. `output\report.xlsx` に判定結果（レポート＋画像比較シート）、`output\diff_images\` に差分画像が出力されます

> 設定をカスタマイズしたい場合は、同梱の `config.yaml` を編集するか、`--config` で別ファイルを指定してください。

---

## 概要

本ツールは以下を目的としています：

- 年次帳票のレイアウト変更検知
- 微小なズレ（位置・余白・段ズレ）の検出
- 大量PDF（100件以上）の自動処理

---

## 特徴

- ピクセル単位での差分検出（OpenCV）
- 位置ズレ補正（ECC）
- ノイズ除去（モルフォロジー処理）
- 差分領域の可視化（赤枠）
- XLSX / CSV / JSON レポート出力（デフォルト: XLSX）
- XLSX レポートには画像比較シート（OLD / OVERLAY / NEW）を含む
- OK / REVIEW / NG の自動判定

---

## 前提条件

| ソフトウェア | バージョン | 確認コマンド |
| --- | --- | --- |
| Python | 3.10 以上 | `python --version` |
| Git | 任意 | `git --version` |

### Python のインストール

Python が未インストールの場合、以下のいずれかの方法でインストールしてください。

**方法1: 公式インストーラー**

[python.org](https://www.python.org/downloads/) からインストーラーをダウンロードし、「Add Python to PATH」にチェックを入れてインストールしてください。

**方法2: winget（Windows パッケージマネージャー）**

```powershell
winget install Python.Python.3.12
```

インストール後、PowerShell を再起動してパスを反映させてください。

### Git のインストール

Git が未インストールの場合：

```powershell
winget install Git.Git
```

---

## セットアップ

### 1. リポジトリのクローン

```powershell
cd C:\tools
git clone https://github.com/mds-devgrp/compare-pdfs.git
cd compare-pdfs
```

### 2. 仮想環境の作成と依存パッケージのインストール

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
```

> **注意**: `Activate.ps1` の実行でエラーが出る場合、PowerShell の実行ポリシーを変更してください：
>
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

## ディレクトリ構成

```text
old/   ← 旧PDF
new/   ← 新PDF
output/
```

※ `old/` と `new/` のファイル名は一致させてください（自動ペアリング）。

ファイル名の一括整形が必要な場合は、[PowerRename](https://learn.microsoft.com/ja-jp/windows/powertoys/powerrename)（Microsoft PowerToys）の利用を推奨します。正規表現による一括リネームが可能です。

```powershell
# PowerToys 未インストールの場合
winget install Microsoft.PowerToys
```

インストール後、エクスプローラーで対象ファイルを選択 → 右クリック →「PowerRename でリネーム」から利用できます。

---

## 実行方法

### Python から実行

```powershell
# デフォルト: XLSX レポート出力
python compare_pdfs.py `
  --old-dir old `
  --new-dir new `
  --output-dir output
```

### オプション

| オプション | 説明 | デフォルト |
| --- | --- | --- |
| `--format {csv,json,xlsx}` | レポート出力形式 | `xlsx` |
| `--without-diff-image` | diff_images/ の生成をスキップ | なし |
| `--limit N` | 先頭 N ペアのみ処理 | 全件 |
| `--config PATH` | 設定ファイルパス | `config.yaml` |

```powershell
# CSV 出力
python compare_pdfs.py --old-dir old --new-dir new --format csv

# diff 画像なしで XLSX のみ（レポートシートのみ）
python compare_pdfs.py --old-dir old --new-dir new --without-diff-image
```

### exe（スタンドアロン）で実行

Python 未インストールの環境では、[Releases](https://github.com/mds-devgrp/compare-pdfs/releases) ページから zip をダウンロードして使用できます。

```powershell
.\compare_pdfs.exe `
  --old-dir old `
  --new-dir new `
  --output-dir output
```

バージョン確認:

```powershell
.\compare_pdfs.exe --version
```

---

## 出力内容

出力先にレポートファイルや `diff_images/` が既に存在する場合、上書き確認のプロンプトが表示されます。承諾すると既存の出力を削除してから処理を開始します。

レポートの行はファイル名順でソートされます（OLD_ONLY / NEW_ONLY も含めて統合）。

### 1. XLSX レポート（`report.xlsx`）— デフォルト

* **Sheet 1「レポート」**: 各ページの判定結果（15列）、条件付き書式でステータスを色分け
* **Sheet 2 以降（画像比較）**: REVIEW / NG ページごとに「旧 (OLD)」「差分 (OVERLAY)」「新 (NEW)」の 3 画像を横並びで表示
* `--without-diff-image` 指定時は画像比較シートなし（レポートシートのみ）

### 2. CSV レポート（`report.csv`）

`--format csv` で出力。

```text
ファイル名,ページ,旧_幅,旧_高さ,新_幅,新_高さ,判定,差分領域数,差分面積,差分率,判定理由,差分画像,旧_ブロック数,新_ブロック数,ブロック数差分
```

* ペアリングされたPDFの各ページごとに1行出力
* 片方のディレクトリにのみ存在するファイルも `OLD_ONLY` / `NEW_ONLY` ステータスで出力

### 3. JSON レポート（`report.json`）

`--format json` で出力。

* 詳細な差分情報（各領域の座標・面積）
* 設定値
* 警告一覧

### 4. 差分オーバーレイ画像（`diff_images/`）

* REVIEW / NG 判定のページのみ出力（`--without-diff-image` で省略可）
* 旧画像と新画像を半透明で重ね合わせ、差分領域を赤く強調表示
* ファイル名形式: `{元ファイル名}_p{ページ番号}_diff.png`（例: `文書様式_010_p001_diff.png`）

---

## 判定基準

| ステータス   | 内容                           |
| --------- | ----------------------------- |
| OK        | 差分なし                       |
| REVIEW    | 微小差分あり                   |
| NG        | 明確なレイアウト変更             |
| OLD_ONLY  | 旧ディレクトリにのみ存在         |
| NEW_ONLY  | 新ディレクトリにのみ存在         |

---

## 設定（config.yaml）

```yaml
dpi: 300
pixel_threshold: 10
min_region_area: 20
align_images: true
```

---

## チューニング指針

* 微小ズレを強く検出したい → `pixel_threshold` を下げる
* ノイズを減らしたい → `min_region_area` を上げる

---

## 想定ユースケース

* 医療帳票の年次改定チェック
* 帳票レイアウト変更検知
* PDF出力仕様の回帰テスト

---

## 開発

### テスト・Lint

```powershell
pip install pytest pytest-cov ruff pre-commit

# Lint
ruff check compare_pdfs.py
ruff format --check compare_pdfs.py

# テスト
pytest test_compare_pdfs.py -v

# テスト + カバレッジ
pytest test_compare_pdfs.py --cov=compare_pdfs --cov-report=term-missing

# pre-commit hook のインストール（commit 時に自動 lint）
pre-commit install
```

### CI

GitHub Actions で以下を自動実行（push to main / PR）:

* **lint**: ruff check + ruff format
* **test**: pytest

### ローカルビルド（exe 作成）

Windows exe をローカルで作成する場合:

```powershell
.\build.bat
```

出力先: `dist\compare_pdfs\`

---

## リリース

GitHub Actions によるタグベースの自動リリースを採用しています。

### 手順

1. `main` ブランチで変更をマージ済みであることを確認
2. バージョンタグを作成・push:

```powershell
git tag v0.1.0
git push origin v0.1.0
```

3. GitHub Actions が自動で Windows exe をビルドし、[Releases](https://github.com/mds-devgrp/compare-pdfs/releases) ページに zip を添付

### Claude Code からリリース

[Claude Code](https://claude.com/claude-code) を使用している場合、カスタムスラッシュコマンドでリリースできます:

```
/release 0.1.0
```

事前チェック（ブランチ・クリーンツリー・タグ重複）を自動で行い、タグ作成・push を実行します。

---

## 注意事項

* フォントレンダリング差で微小差分が出ることがあります
* DPIを上げると精度は向上しますが処理時間が増加します

---

## ライセンス

[MIT License](LICENSE)
