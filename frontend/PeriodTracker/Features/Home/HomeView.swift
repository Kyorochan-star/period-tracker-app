//
//  HomeView.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/04.
//
//  機能説明:
// - ホーム画面
// - showModalがtrueで生理開始を記録するモーダルを表示
// - showModalがfalseでホーム画面を表示

import SwiftUI

struct HomeView: View {
    @State private var showModal = true
    @State private var modifyModal = false
    
    var body: some View {
        ZStack{
            if showModal {
                Color.black.opacity(0.2)
                    .ignoresSafeArea()
                RecordModalView(
                    showModal: $showModal
                )
            } else {
                VStack {
                    HStack{
                        Text("今日の記録")
                            .font(.title)
                            .bold()
                            .frame(maxWidth: 350, alignment: .leading)
                            .padding(.horizontal)
                        Spacer()
                        // 月経期間の修正モーダル
                        Button(action: {
                            modifyModal = true
                        }) {
                            Image(systemName: "square.and.pencil")
                                .font(.title)
                                .foregroundColor(.blue)
                                .padding(.trailing)
                        }
                    }
                    CalendarView()
                }
            }
        }
    }
}

#Preview {
    HomeView()
}
