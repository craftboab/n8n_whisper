# GitHubリポジトリ設定とCoolify接続ガイド

## 🚨 Coolifyで「Not Found」エラーが発生する場合の対処法

### 1. GitHubリポジトリの確認

#### 1.1 リポジトリが正しく作成されているか確認
```bash
# ローカルでリポジトリの状態を確認
git remote -v
```

出力例：
```
origin  https://github.com/YOUR_USERNAME/ai-secretary.git (fetch)
origin  https://github.com/YOUR_USERNAME/ai-secretary.git (push)
```

#### 1.2 GitHub.comでリポジトリを手動作成
1. GitHub.comにログイン
2. 右上の「+」ボタン → 「New repository」をクリック
3. 設定：
   - **Repository name**: `ai-secretary`
   - **Description**: `AI Secretary - Voice input AI assistant`
   - **Visibility**: `Public` または `Private`
   - **Initialize this repository with**: チェックを外す
4. 「Create repository」をクリック

#### 1.3 ローカルリポジトリをGitHubにプッシュ
```bash
# リモートリポジトリを追加（まだ追加していない場合）
git remote add origin https://github.com/YOUR_USERNAME/ai-secretary.git

# メインブランチを設定
git branch -M main

# 初回プッシュ
git push -u origin main
```

### 2. GitHubリポジトリのURL形式

#### 2.1 HTTPS形式（推奨）
```
https://github.com/YOUR_USERNAME/ai-secretary.git
```

#### 2.2 SSH形式（SSHキーが設定されている場合）
```
git@github.com:YOUR_USERNAME/ai-secretary.git
```

### 3. Coolifyでの設定手順

#### 3.1 正しいURLを入力
Coolifyのプロジェクト作成画面で：

**Repository URL**: `https://github.com/YOUR_USERNAME/ai-secretary.git`

**注意**: 
- `YOUR_USERNAME` を実際のGitHubユーザー名に置き換える
- `.git` 拡張子を含める
- 大文字小文字を正確に入力

#### 3.2 ブランチの指定
- **Branch**: `main`
- **Build Pack**: `Docker Compose`

### 4. よくある間違いと解決方法

#### 4.1 URLの間違い
❌ 間違いの例：
```
https://github.com/ai-secretary.git
https://github.com/YOUR_USERNAME/ai-secretary
git@github.com:YOUR_USERNAME/ai-secretary
```

✅ 正しい例：
```
https://github.com/YOUR_USERNAME/ai-secretary.git
```

#### 4.2 リポジトリ名の間違い
- リポジトリ名が正確に `ai-secretary` になっているか確認
- 大文字小文字を正確に入力

#### 4.3 プライベートリポジトリの場合
プライベートリポジトリを使用する場合：

1. **GitHub Personal Access Token** を作成
   - GitHub.com → Settings → Developer settings → Personal access tokens
   - 「Generate new token」→ 「Generate new token (classic)」
   - 権限: `repo` にチェック
   - トークンをコピー

2. **Coolifyでトークンを設定**
   - Coolifyダッシュボード → Settings → Source Control
   - GitHub の設定で Personal Access Token を追加

### 5. トラブルシューティング

#### 5.1 リポジトリが存在しない場合
```bash
# GitHubでリポジトリを作成
# または、ローカルでリポジトリを初期化してプッシュ
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ai-secretary.git
git push -u origin main
```

#### 5.2 権限の問題
- GitHubアカウントにログインしているか確認
- リポジトリへのアクセス権限があるか確認
- プライベートリポジトリの場合はPersonal Access Tokenが必要

#### 5.3 ネットワークの問題
- インターネット接続を確認
- ファイアウォール設定を確認
- VPNを使用している場合は一時的に無効化してテスト

### 6. 確認手順

#### 6.1 GitHubでの確認
1. GitHub.comにログイン
2. プロフィール → Repositories
3. `ai-secretary` リポジトリが表示されるか確認
4. リポジトリをクリックして内容を確認

#### 6.2 ブラウザで直接アクセス
```
https://github.com/YOUR_USERNAME/ai-secretary
```
このURLでリポジトリにアクセスできるか確認

#### 6.3 Gitコマンドで確認
```bash
# リモートリポジトリの確認
git remote -v

# リモートリポジトリのテスト
git ls-remote origin
```

### 7. 代替手段

#### 7.1 SSHキーを使用
```bash
# SSHキーを生成（まだ作成していない場合）
ssh-keygen -t ed25519 -C "your_email@example.com"

# GitHubにSSHキーを追加
# GitHub.com → Settings → SSH and GPG keys → New SSH key
```

#### 7.2 手動でファイルをアップロード
CoolifyでGitリポジトリが見つからない場合の一時的な解決策：

1. Coolifyで「Upload Files」オプションを選択
2. プロジェクトファイルをZIPで圧縮
3. ZIPファイルをアップロード

### 8. 最終確認チェックリスト

- [ ] GitHubリポジトリが正しく作成されている
- [ ] リポジトリ名が正確（`ai-secretary`）
- [ ] ローカルファイルがGitHubにプッシュされている
- [ ] Coolifyで正しいURLを入力している
- [ ] ブランチ名が正しい（`main`）
- [ ] プライベートリポジトリの場合はPersonal Access Tokenを設定

### 9. サポート

問題が解決しない場合は：

1. **GitHubのリポジトリURL**を確認
2. **Coolifyのログ**を確認
3. **ネットワーク接続**を確認
4. **GitHubアカウントの権限**を確認

詳細なエラーメッセージがあれば、より具体的な解決方法を提供できます。 