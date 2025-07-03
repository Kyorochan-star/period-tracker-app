## Dockerイメージのビルドとコンテナの実行
1. `backend`ディレクトリに移動して
```cd backend```

2. イメージのビルド（backendディレクトリ配下をビルドコンテキストに&myappはイメージ名なので自由に変えていいです）
```docker build -t myapp .```

3. コンテナの実行
```docker run myapp```
または
```docker run -p 8000:8000 myapp```
→ これだったらローカルのPCだけじゃなくて外部からAPI叩ける

## APIエンドポイント