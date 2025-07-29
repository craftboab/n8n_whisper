# AI Secretary

音声入力対応のAI秘書システム。FastAPI、PostgreSQL、n8nを使用したモダンなアーキテクチャで構築されています。

## 🚀 技術スタック

- **バックエンド**: FastAPI (Python)
- **データベース**: PostgreSQL
- **ワークフロー**: n8n
- **音声認識**: OpenAI Whisper
- **コンテナ化**: Docker & Docker Compose
- **デプロイ**: Coolify (Hetzner Cloud)

## 📁 プロジェクト構成

```
ai-secretary/
├── fastapi_app/
│   ├── main.py              # FastAPIアプリケーション
│   ├── whisper_handler.py   # Whisper音声認識モジュール
│   ├── requirements.txt     # Python依存関係
│   ├── Dockerfile          # FastAPI用Dockerfile
│   └── __init__.py         # パッケージ初期化
├── docker-compose.yml       # 全体のサービス構成
├── env.example             # 環境変数テンプレート
├── .gitignore              # Git除外設定
└── README.md               # このファイル
```

## 🛠️ ローカル開発環境の起動

### 1. 環境変数の設定

```bash
# 環境変数ファイルをコピー
cp env.example .env

# 必要に応じて.envファイルを編集
nano .env
```

### 2. Docker Composeで起動

```bash
# 全サービスを起動
docker-compose up -d

# ログを確認
docker-compose logs -f

# 特定のサービスのログを確認
docker-compose logs -f fastapi
docker-compose logs -f n8n
docker-compose logs -f postgres
```

### 3. アクセス確認

- **FastAPI**: http://localhost:8000
- **FastAPI Docs**: http://localhost:8000/docs
- **n8n**: http://localhost:5678
- **PostgreSQL**: localhost:5432

## 🌐 GitHubアップロードとCoolifyデプロイ

### 1. GitHubリポジトリの準備

```bash
# Gitリポジトリを初期化
git init

# ファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit: AI Secretary project"

# GitHubリポジトリを作成（GitHub.comで手動作成）
# リポジトリ名: ai-secretary

# リモートリポジトリを追加
git remote add origin https://github.com/YOUR_USERNAME/ai-secretary.git

# メインブランチをプッシュ
git branch -M main
git push -u origin main
```

### 2. Coolifyでのプロジェクト作成

#### 2.1 Coolifyダッシュボードにアクセス
1. Hetzner CloudのCoolifyインスタンスにログイン
2. ダッシュボードで「New Project」をクリック

#### 2.2 プロジェクト設定
- **Project Name**: `ai-secretary`
- **Repository**: GitHubリポジトリを選択
- **Branch**: `main`
- **Build Pack**: `Docker Compose`

#### 2.3 デプロイ設定
- **Build Command**: 空欄（Docker Compose使用）
- **Start Command**: `docker-compose up -d`
- **Port**: `8000`（FastAPI用）

### 3. 環境変数の設定

Coolifyのプロジェクト設定で以下の環境変数を設定：

#### 3.1 必須環境変数
```bash
# データベース設定
POSTGRES_DB=ai_secretary
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<strong_password_here>
DATABASE_URL=postgresql://postgres:<strong_password_here>@postgres:5432/ai_secretary

# n8n設定
N8N_USER=admin
N8N_PASSWORD=<strong_n8n_password>
N8N_BASE_URL=http://n8n:5678

# FastAPI設定
ENVIRONMENT=production
PORT=8000
```

#### 3.2 オプション環境変数
```bash
# OpenAI Whisper設定
OPENAI_API_KEY=<your_openai_api_key>
WHISPER_MODEL=base

# タイムゾーン設定
GENERIC_TIMEZONE=America/Los_Angeles
```

### 4. デプロイ実行

#### 4.1 初回デプロイ
1. 「Deploy」ボタンをクリック
2. ビルド進行状況を監視
3. デプロイ完了を確認

#### 4.2 デプロイ後の確認
- **FastAPI**: `https://your-domain.com:8000`
- **n8n**: `https://your-domain.com:5678`
- **ヘルスチェック**: `https://your-domain.com:8000/health`

### 5. ドメインとSSL設定

#### 5.1 カスタムドメイン設定
1. Coolifyプロジェクト設定で「Domains」を開く
2. カスタムドメインを追加（例: `ai-secretary.yourdomain.com`）
3. DNSレコードを設定

#### 5.2 SSL証明書の設定
1. 「SSL」タブでLet's Encrypt証明書を有効化
2. 証明書の自動更新を確認

### 6. 継続的デプロイメント（CD）

#### 6.1 自動デプロイの設定
1. プロジェクト設定で「Auto Deploy」を有効化
2. ブランチ選択: `main`
3. プルリクエストでの自動デプロイも設定可能

#### 6.2 手動デプロイ
```bash
# ローカルで変更をプッシュ
git add .
git commit -m "Update feature"
git push origin main

# Coolifyで自動的にデプロイが開始される
```

## 📡 API エンドポイント

### FastAPI エンドポイント

- `GET /` - ルート情報
- `GET /health` - ヘルスチェック（Whisperモデル状態含む）
- `GET /config` - 設定情報取得
- `GET /whisper/models` - Whisperモデル情報
- `POST /audio/transcribe` - 音声ファイルの文字起こし
- `POST /process/voice-command` - 音声コマンド処理

### 使用例

```bash
# ヘルスチェック
curl https://your-domain.com:8000/health

# 音声ファイルのアップロード
curl -X POST "https://your-domain.com:8000/audio/transcribe" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@sample.wav"

# 音声コマンド処理
curl -X POST "https://your-domain.com:8000/process/voice-command" \
  -H "Content-Type: application/json" \
  -d '{"command": "今日の予定を教えて"}'

# Whisperモデル情報取得
curl https://your-domain.com:8000/whisper/models
```

## 🔧 開発・デバッグ

### サービスの停止

```bash
# 全サービスを停止
docker-compose down

# ボリュームも削除
docker-compose down -v
```

### データベースのリセット

```bash
# PostgreSQLボリュームを削除
docker volume rm ai-secretary_postgres_data

# 再起動
docker-compose up -d
```

### n8nデータのリセット

```bash
# n8nボリュームを削除
docker volume rm ai-secretary_n8n_data

# 再起動
docker-compose up -d
```

## 🔒 セキュリティ設定

### 本番環境での推奨設定

1. **強力なパスワードの使用**
   - PostgreSQLパスワード（32文字以上）
   - n8n認証パスワード（32文字以上）
   - 特殊文字、数字、大文字小文字を含む

2. **環境変数の管理**
   - 機密情報は環境変数で管理
   - `.env`ファイルはGitにコミットしない
   - Coolifyの環境変数設定を使用

3. **ネットワークセキュリティ**
   - Hetzner Cloudのファイアウォール設定
   - 必要最小限のポート開放
   - リバースプロキシの使用

4. **SSL/TLS設定**
   - Let's Encrypt証明書の自動更新
   - HTTPS強制リダイレクト
   - セキュリティヘッダーの設定

## 📝 トラブルシューティング

### よくある問題

1. **ポート競合**
   ```bash
   # 使用中のポートを確認
   lsof -i :8000
   lsof -i :5678
   lsof -i :5432
   ```

2. **Dockerイメージの再ビルド**
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   ```

3. **ログの確認**
   ```bash
   docker-compose logs -f [service_name]
   ```

4. **Coolifyでのデプロイエラー**
   - 環境変数の設定を確認
   - ポート設定の確認
   - リソース制限の確認

5. **Whisperモデルの読み込みエラー**
   - メモリ不足の可能性
   - より小さいモデル（tiny, base）を使用
   - GPUリソースの確認

### Coolify特有のトラブルシューティング

1. **デプロイが失敗する場合**
   - ログを確認: Coolifyダッシュボード → プロジェクト → Logs
   - 環境変数の設定を確認
   - リソース制限を確認

2. **サービスが起動しない場合**
   - ポート設定を確認
   - 依存関係の順序を確認
   - ボリュームの権限を確認

3. **SSL証明書の問題**
   - DNS設定を確認
   - 証明書の有効期限を確認
   - 手動で証明書を更新

## 🚀 パフォーマンス最適化

### 1. リソース設定
```yaml
# docker-compose.yml に追加
services:
  fastapi:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

### 2. Whisperモデルの選択
- **開発環境**: `tiny` または `base`
- **本番環境**: `base` または `small`
- **高精度が必要**: `medium` または `large`

### 3. キャッシュ設定
- Redisの追加を検討
- 音声ファイルの一時キャッシュ
- モデル読み込みの最適化

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📞 サポート

問題や質問がある場合は、GitHubのIssuesページでお知らせください。

## 🔗 関連リンク

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [n8n Documentation](https://docs.n8n.io/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Coolify Documentation](https://coolify.io/docs)
- [Hetzner Cloud](https://www.hetzner.com/cloud) 