//
//  HomeView.swift
//  FriendsFavoriteMovies
//
//  Created by 藤瀬太翼 on 2025/07/04.
//

import SwiftUI

struct HomeView: View {
    @State private var showModal = true
    @State private var selectedOption = ""
    @State private var savedOption = ""
    var options = ["生理周期", "月経過多", "お腹の痛み", "こめかみの痛み"]
    
    var body: some View {
        ZStack{
            if showModal {
                Color.black.opacity(0.2)
                    .ignoresSafeArea()
                RecordModalView(
                    options: options,
                    selectedOption: $selectedOption,
                    savedOption: $savedOption,
                    showModal: $showModal
                )
            } else {
                VStack(spacing: 24) {
                    VStack {
                        Text("今日の記録")
                            .font(.largeTitle)
                            .bold()
                            .padding(.bottom)
                            .frame(maxWidth: 350, alignment: .leading)
                        
                        HStack {
                            ForEach(0..<6, id: \.self) { offset in
                                let date = Calendar.current.date(byAdding: .day, value: offset - 5, to: Date())!
                                let day = Calendar.current.component(.day, from: date)
                                let japaneseWeekdays = ["日", "月", "火", "水", "木", "金", "土"]
                                let weekdaySymbol = japaneseWeekdays[Calendar.current.component(.weekday, from: date) - 1]
                                
                                VStack {
                                    Text(weekdaySymbol)
                                        .font(.caption)
                                    Text("\(day)")
                                        .font(.caption)
                                        .bold()
                                }
                                .padding()
                                .background(
                                    RoundedRectangle(cornerRadius: 12)
                                        .fill(offset == 5 ? Color.blue.opacity(0.8): Color.white)
                                )
                                .overlay(
                                    RoundedRectangle(cornerRadius: 12)
                                        .stroke(Color.gray, lineWidth: 1)
                                )
                                .foregroundColor(offset == 5 ? Color.white:Color.black)
                            }
                        }
                        .padding(.horizontal)
                    }
                    .frame(maxWidth: 350, maxHeight: 200, alignment: .top)
                    .background(
                        RoundedRectangle(cornerRadius: 12)
                            .fill(Color.white)
                    )
                    VStack(alignment: .leading, spacing: 16) {
                        Text("詳細記録")
                            .font(.title)
                            .bold()
                            .padding(.bottom, 4)
                        VStack(alignment: .leading, spacing: 8) {
                            Text("生理周期")
                                .font(.headline)
                                .foregroundColor(.red)
                            Text("次回予測: 3月28日")
                                .font(.subheadline)
                                .foregroundColor(.primary)
                        }
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(
                            RoundedRectangle(cornerRadius: 12)
                                .fill(Color.red.opacity(0.3))
                        )
                        VStack(alignment: .leading, spacing: 8) {
                            Text("体調")
                                .font(.headline)
                                .foregroundColor(.blue)
                            Text("記録なし")
                                .font(.subheadline)
                                .foregroundColor(.primary)
                        }
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(
                            RoundedRectangle(cornerRadius: 12)
                                .fill(Color.blue.opacity(0.3))
                        )
                        VStack(alignment: .leading, spacing: 8) {
                            Text("症状")
                                .font(.headline)
                                .foregroundColor(.green)
                            Text("記録なし")
                                .font(.subheadline)
                                .foregroundColor(.primary)
                        }
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(
                            RoundedRectangle(cornerRadius: 12)
                                .fill(Color.green.opacity(0.3))
                        )
                    }
                    .padding()
                    .background(Color.white)
                    .cornerRadius(16)
                    .frame(maxWidth: 350)
                }
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color(UIColor.systemBackground))
    }
}



#Preview {
    HomeView()
}
