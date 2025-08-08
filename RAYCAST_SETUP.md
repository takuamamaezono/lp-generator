# Raycast設定ガイド - LP欄生成システム

## 🚀 Raycastから起動する3つの方法

### 方法1: Script Commands（推奨）

作成した3つのスクリプトをRaycastに追加できます：

1. **LP欄生成（フル機能）**
   - ファイル: `raycast-lp-generator.sh`
   - Raycast内で対話式入力

2. **LP欄生成（新規ターミナル）**
   - ファイル: `Open LP Generator.applescript`
   - ターミナルを開いて起動

3. **LP欄クイック生成**
   - ファイル: `lp-quick-template.sh`
   - テンプレートから素早く生成

#### 設定手順

1. Raycastを開く
2. `Create Script Command` を検索
3. 以下のいずれかを選択：
   - `Add existing script`
   - ファイルを選択: `/Users/g.ohorudingusu/Docbase/lp_generator/[スクリプト名]`
4. 保存して完了！

### 方法2: エイリアス設定

```bash
# ~/.zshrc に追加
alias lp='cd /Users/g.ohorudingusu/Docbase/lp_generator && ./run_lp_generator.sh'
```

その後、Raycastで：
1. `Terminal` コマンドを選択
2. `lp` と入力してEnter

### 方法3: Quicklinks

1. Raycastの設定を開く
2. Extensions → Quicklinks
3. 新規作成：
   - Name: `LP欄生成`
   - Link: `terminal://cd%20/Users/g.ohorudingusu/Docbase/lp_generator%20&&%20./run_lp_generator.sh`

## 📝 使い方

### Script Commandsの場合

1. Raycastを開く（⌘+Space）
2. 「LP欄」と入力
3. 使いたいコマンドを選択：
   - `LP欄生成` - Raycast内で実行
   - `LP欄生成（新規ターミナル）` - ターミナルで実行
   - `LP欄クイック生成` - テンプレートから素早く

### おすすめの使い分け

- **素早く作りたい時**: `LP欄クイック生成`
- **じっくり作りたい時**: `LP欄生成（新規ターミナル）`
- **Raycast内で完結したい時**: `LP欄生成`

## 🎯 ショートカットキー設定

Raycastの設定でホットキーも設定できます：

1. Script Commandの設定を開く
2. Hotkeyを設定（例: ⌘+Shift+L）
3. 一発で起動可能に！

## 💡 Tips

- Script Commandsは自動的にRaycastの検索対象になります
- アイコンや説明文も表示されるので見つけやすい
- 引数付きで起動することも可能

---

設定で困ったことがあれば聞いてね！