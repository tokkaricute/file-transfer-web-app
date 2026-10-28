# Implementation Plan

## [Overview]
「File Transfer Web App」は、ブラウザ経由で指定されたディレクトリ内のファイルをブラウズし、ファイルのアップロード（複数同時）およびダウンロード（複数同時・ZIP圧縮）ができる軽量なウェブアプリケーションです。`uv` を使用して実行され、パスワードによるアクセス制限が可能です。

## [Types]
- **FileEntry**: ファイルまたはディレクトリの情報を保持するデータ構造（名前、サイズ、タイプ、最終更新日時）。
- **UploadStatus**: アップロードの進捗状況をフロントエンドに伝えるためのステータス。

## [Files]
- `src/main.py`: FastAPIアプリケーションのエントリポイントおよびルーティング。
- `src/file_manager.py`: ファイルシステム操作のコアロジック（一覧取得、安全なパス解決、ZIP圧縮、アップロード処理）。
- `src/auth.py`: パスワード認証ロジック。
- `templates/index.html`: Jinja2を使用したメインUIテンプレート。
- `static/css/style.css`: アプリケーションのスタイリング。
- `static/js/app.js`: アップロード進捗表示、ディレクトリ移動、ダウンロード制御のためのクライアントサイド・ロジック。
- `pyproject.toml`: プロジェクト依存関係（`fastapi`, `uvicorn`, `jinja2`, `python-multipart`）の管理。

## [Functions]
- **`file_manager.list_directory(base_dir, rel_path)`**: 指定された相対パスに基づき、安全にファイル一覧を返す。
- **`file_manager.create_zip(file_paths)`**: 選択された複数のファイルを一つのZIPファイルにまとめる。
- **`file_manager.safe_resolve(base_dir, rel_path)`**: ディレクトリ・トラバーサル攻撃を防ぎ、指定されたディレクトリ内のみにアクセスを制限する。
- **`main.upload_file(file, target_rel_path)`**: ファイルのアップロードを処理する。
- **`main.bulk_download(file_rel_paths)`**: 複数ファイルをZIPとして配信する。
- **`auth.is_authenticated(provided_password, target_password)`**: パスワード認証。

## [Classes]
- **`FileManager`**: ファイルシステム操作を集約するクラス（ディレクトリ内検索、ファイル操作の抽象化）。

## [Dependencies]
- `fastapi`: Webフレームワーク（軽量・高速）。
- `uvicorn`: ASGIサーバー。
- `jinja2`: HTMLテンプレートエンジン。
- `python-multipart`: ファイルアップロード処理用。

## [Testing]
- **ディレクトリ・トラバーサル検証**: `../` などのパスを用いた不正アクセスの遮断を確認。
- **複数ファイルアップロード検証**: 進捗バーが正しく動作し、完了通知が出ることを確認。
- **複数ファイルダウンロード検証**: 複数選択したファイルが1つのZIPとして取得できることを確認。
- **認証検証**: パスワード設定時と未設定時の挙動の確認。

## [Implementation Order]
1. **プロジェクト基盤の構築**: `pyproject.toml` の作成とディレクトリ構造の整備。
2. **コアロジックの実装**: `file_manager.py` による安全なファイル操作（一覧取得、ZIP作成）の実装。
3. **認証ロジックの実装**: `auth.py` によるパスワード検証。
4. **バックエンドAPIの実装**: `main.py` によるルーティング（一覧、アップロード、ダウンロード、認証）の実装。
5. **フロントエンド基盤の実装**: `index.html` および `style.css` の作成。
6. **フロントエンド・インタラクションの実装**: `app.js` による非同期通信（アップロード進捗、ディレクトリ遷移、ダウンロード）の実装。
7. **CLIインターフェースの実装**: `main.py` を起点としたコマンドライン引数の処理の実装。
8. **最終検証**: 全機能の動作確認。
