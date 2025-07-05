//
//  RecordModal.swift
//  FriendsFavoriteMovies
//
//  Created by 藤瀬太翼 on 2025/07/04.
//

import SwiftUI
import Foundation

struct RecordModalView: View {
    var options: [String]
    @Binding var selectedOption: String
    @Binding var savedOption: String
    @Binding var showModal: Bool
    
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
                            .padding()
                    }
                }
                .frame(height: 0)
                VStack(spacing: 6){
                    Text("今日の記録")
                        .bold()
                        .padding(.bottom, 7)
                    Text("2025年7月4日")
                        .font(.title)
                        .padding(.bottom, 7)
                        .foregroundColor(.blue) 
                    Text("金曜日")
                        .font(.caption)
                        .padding(.bottom, 10)
                    VStack(spacing: 6) {
                        ForEach(options, id: \.self) { option in
                            Button(action: {
                                selectedOption = option
                            }) {
                                Text(option)
                                    .frame(maxWidth: 250)
                                    .padding(.vertical, 8)
                                    .background(
                                        RoundedRectangle(cornerRadius: 8)
                                            .fill(selectedOption == option ? Color.blue.opacity(0.2) : Color.white)
                                    )
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 8)
                                            .stroke(Color.gray, lineWidth: 1)
                                    )
                            }
                            .foregroundColor(.primary)
                        }
                    }
                    .padding(.bottom, 24)
                    
                    Button("記録を保存する") {
                        savedOption = selectedOption
                        showModal = false
                    }
                    .padding(.bottom)
                }
            }
            .frame(width: UIScreen.main.bounds.width * 0.7,
                   height: UIScreen.main.bounds.height * 0.5)
            .background(Color.white)
            .cornerRadius(20)
            .shadow(radius: 10)
        }
    }
