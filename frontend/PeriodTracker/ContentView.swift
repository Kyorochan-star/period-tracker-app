//
//  ContentView.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/04.
//
//  機能説明:
//  - アプリのメインコンテナ
//  - ログイン状態の管理
//  - タブナビゲーション（カレンダー、ホーム、チャット）

import SwiftUI

struct ContentView: View {
    @State private var isLoggedIn = false
    @State private var selectedTab = 1

    var body: some View {
        if !isLoggedIn {
            LoginView(isLoggedIn: $isLoggedIn)
        } else{
        TabView(selection: $selectedTab) {
            ChatView()
                .tabItem {
                    Label("チャット", systemImage: "message.fill")
                }
                .tag(0)
            
            HomeView()
                .tabItem {
                    Label("ホーム", systemImage: "house.fill")
                }
                .tag(1)
            
            SettingView()
                .tabItem {
                    Label("設定", systemImage: "gearshape")
                }
                .tag(2)
        }
    }
    }
}

#Preview {
    ContentView()
}
