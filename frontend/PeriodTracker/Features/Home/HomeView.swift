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
    @StateObject private var viewModel = HomeViewModel(periodRepository: NetworkPeriodRepository())

    var body: some View {
        ZStack{
            LinearGradient(
                gradient: Gradient(colors: [
                    Color(red: 0.8, green: 0.95, blue: 1.0),
                    Color(red: 0.92, green: 0.96, blue: 1.0)
                ]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
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
                            ZStack {
                                Circle()
                                    .fill(
                                        LinearGradient(
                                            gradient: Gradient(colors: [
                                                Color(red: 0.0, green: 0.6, blue: 0.99),
                                                Color(red: 0.1, green: 0.85, blue: 0.95)
                                            ]),
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        )
                                    )
                                    .frame(width: 45, height: 45)
                                
                                Image(systemName: "square.and.pencil")
                                    .resizable()
                                    .scaledToFit()
                                    .fontWeight(.bold)
                                    .frame(width: 28, height: 29)
                                    .foregroundColor(.white)
                                    .offset(x: 2.23)
                            }
                        }
                        .padding(.trailing)
                    }
                    .padding(.bottom, 20)
                    .background(Color.white)
                    
                    CalendarView(viewModel: CalendarViewModel(periodRepository: NetworkPeriodRepository()))
                        .padding(.top, 13)
                        .padding(.horizontal)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
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
