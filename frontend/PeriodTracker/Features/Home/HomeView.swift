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
    @StateObject private var viewModel = HomeViewModel(periodRepository: MockPeriodRepository())

    var body: some View {
        ZStack{
            if viewModel.showModal {
                Color.black.opacity(0.2)
                    .ignoresSafeArea()
                RecordModalView(
                    showModal: $viewModel.showModal,
                    isStart: viewModel.isStartModal
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
                            viewModel.showModifyModal = true
                        }) {
                            Image(systemName: "square.and.pencil")
                                .font(.title)
                                .foregroundColor(.blue)
                                .padding(.trailing)
                        }
                    }
                    CalendarView(viewModel: CalendarViewModel(periodRepository: MockPeriodRepository()))
                }
            }
        }
        .task {
            await viewModel.loadModalState()
        }
    }
}

#Preview {
    HomeView()
}
