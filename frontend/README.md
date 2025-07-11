## 開発環境

### 必要環境
- **Xcode**: Version 16.4 (16F6) 
- **iOS Simulator**: iOS 18.0 以上
- **Swift**: 6.0 以上

## セットアップ手順

### 1. Xcodeのインストール
- App StoreからXcode 16.4以上をインストール

### 2. プロジェクトを開く
```bash
# ターミナルでプロジェクトディレクトリに移動
cd frontend

# Xcodeでプロジェクトを開く
open PeriodTracker.xcodeproj
```

### 3. ビルド・実行
1. Xcodeでプロジェクトが開いたら、**Product → Run** を選択
2. または **⌘ + R** でビルド・実行
3. iOSシミュレータが起動し、アプリが表示される

## 依存関係

### 依存関係の管理方法
このプロジェクトでは**Xcode内のPackage Dependencies**で依存関係を管理。

#### 現在使用しているライブラリ
- **標準ライブラリのみ使用**（外部ライブラリは追加していない）

### 依存関係の追加方法
将来的に外部ライブラリが必要になった場合：

1. **Xcodeでプロジェクトを開く**
2. **プロジェクトナビゲーターでPeriodTrackerを選択**
3. **"Package Dependencies"タブをクリック**
4. **"+"ボタンでパッケージを追加**

### 依存関係の共有
- **Package Dependencies**の設定は`PeriodTracker.xcodeproj`に保存される
- **他の開発者がプロジェクトを開くと自動的に依存関係が反映される**
- **Gitで共有可能**（`Package.resolved`ファイルも含む）
- **全員が同じバージョンを使用**できる

## プロジェクト構成

```
PeriodTracker/
├── PeriodTrackerApp.swift      # アプリのエントリーポイント
├── ContentView.swift           # メイン画面
├── Features/                   # 機能別フォルダ
│   ├── Auth/                  # 認証機能
│   │   ├── LoginView.swift
│   │   └── SignUpView.swift
│   │   
│   ├── Home/                  # ホーム機能
│   │   ├── HomeView.swift
│   │   └── RecordModal.swift
│   │   └── CalendarView.swift      # カレンダー機能
│   └── Chat/                  # チャット機能
│       └── ChatView.swift
├── Models/                    # データモデル
│   └── Record.swift
├── Services/                  # API通信サービス（今後実装予定）
│   └── APIService.swift
├── Resources/                 # モックデータ格納
│   └── mock_records.json
└── Assets.xcassets/           # 画像・リソース
```

アーキテクチャは機能ごとに分割した上でのMVVMパターンを採用。
今後、それぞれの機能のフォルダにViewModelを配置する。
型定義やAPI通信関連も未実装。
