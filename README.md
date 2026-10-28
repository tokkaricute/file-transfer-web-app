# File Transfer Web App

FastAPIを使用した、ブラウザ経由で指定したディレクトリ内のファイルを閲覧、アップロード、およびダウンロードできる軽量なウェブアプリケーションです。

## 主な機能

- **ファイルブラウザ**: ディレクトリおよびサブディレクトリの階層移動が可能です。
- **複数ファイルアップロード**: 複数のファイルを同時に選択してアップロードでき、リアルタイムで進捗状況を表示します。
- **一括ダウンロード**: 複数のファイルを選択し、ZIP形式でまとめてダウンロードできます。
- **認証機能**: パスワード設定により、アクセス制限をかけることができます。
- **軽量・高速**: FastAPI と `uv` を使用した、最小限の構成による高速な動作。

## 技術スタック

- **バックエンド**:
  - [FastAPI](https://fastapi.tiangolo.com/): 高性能なWebフレームワーク。
  - [Uvicorn](https://www.uvicorn.org/): ASGIサーバー。
  - [Jinja2](https://jinja.palletsprojects.com/): テンプレートエンジン。
- **フロントエンド**:
  - Vanilla JavaScript (アップロード進捗管理にXMLHttpRequestを使用)
  - CSS3
- **パッケージ管理**:
  - [uv](https://github.com/astral-sh/uv): 非常に高速なPythonパッケージインストーラーおよびリゾルバー。

## 動作要件

- Python 3.10 以上
- `uv` がシステムにインストールされていること

## インストール

1. **リポジトリのクローン**:
   ```bash
   git clone <repository_url>
   cd file-transfer-web-app
   ```

2. **`uv` を使用した依存関係のインストール**:
   ```bash
   uv sync
   ```

## 使用方法

`uv run` を使用してアプリケーションを起動します。共有したいディレクトリやパスワードをオプションで指定できます。

### 基本的な使用方法 (カレントディレクトリ、パスワードなし)
```bash
uv run python src/main.py
```

### ディレクトリとパスワードを指定する場合
```bash
uv run python src/main.py /path/to/your/files -p mysecretpassword
```

アプリケーションは `http://localhost:8000` で起動します。

## プロジェクト構成

```text
.
├── src/
│   ├── main.py           # エントリーポイントおよびFastAPIルート
│   ├── file_manager.py   # ファイル操作およびZIP作成ロジック
│   └── auth.py           # パスワード検証ロジック
├── static/
│   ├── css/
│   │   └── style.css     # アプリケーション用スタイルシート
│   └── js/
│       └── app.js        # クライアントサイドのロジック
├── templates/
│   └── index.html        # HTMLテンプレート
├── requirements.md        # プロジェクト要件定義書
├── pyproject.toml         # Pythonプロジェクト構成ファイル
└── README.md             # プロジェクトドキュメント
```