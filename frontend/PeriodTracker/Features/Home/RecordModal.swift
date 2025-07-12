//
//  RecordModal.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/04.
//
//  機能説明:
//  - 記録入力用のモーダル画面
//  - 生理開始日ボタン

import SwiftUI
import Foundation

struct RecordModalView: View {
    @Binding var showModal: Bool
    let isStart: Bool // true = 生理開始, false = 生理終了
    
    var body: some View {
        VStack(spacing: 8) {
            HStack {
                Spacer()
                Button(action: {
                    showModal = false
                }) {
                    Image(systemName: "xmark.circle.fill")
                        .font(.title2)
                        .foregroundColor(.gray)
                        .padding(.trailing)
                }
            }
            .frame(height: 0)
            VStack(spacing: 6){
                Text(isStart ? "今日の記録" : "終了の記録")
                    .bold()
                    .padding(.bottom, 30)
                    .font(.title2)
                Text("2025年7月4日")
                    .font(.largeTitle)
                    .bold()
                    .padding(.top, 1)
                    .foregroundColor(Color(red: 0.0, green: 0.8, blue: 1.0))
                Text("金曜日")
                    .font(.callout)
                    .padding(.top, 2)
                    .padding(.bottom, 20)
                
                Button(action: {
                    showModal = false
                }) {
                    Text(isStart ? "生理開始" : "生理終了")
                        .bold()
                    Image(systemName: "drop.fill")
                        .foregroundColor(isStart ? .red : .blue)
                }
                .frame(maxWidth: .infinity)
                .padding()
                .background(isStart ? Color.red.opacity(0.05) : Color.blue.opacity(0.05))
                .foregroundColor(isStart ? .red : .blue)
                .cornerRadius(8)
                .overlay(
                    RoundedRectangle(cornerRadius: 10)
                        .stroke(isStart ? Color.red : Color.blue, lineWidth: 1)
                )
                .frame(maxWidth: .infinity)
                .padding(.horizontal)
            }
        }
        .frame(width: UIScreen.main.bounds.width * 0.7,
               height: UIScreen.main.bounds.height * 0.3)
        .background(Color.white)
        .cornerRadius(20)
        .shadow(radius: 10)
    }
}

#Preview {
    RecordModalView(showModal: .constant(true), isStart: true)
}
