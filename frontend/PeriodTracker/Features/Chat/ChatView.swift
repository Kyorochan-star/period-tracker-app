//
//  ChatView.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/04.
//
//  機能説明:
//  - AIチャット相談画面

import SwiftUI

struct ChatMessage: Identifiable {
    let id: UUID = UUID()
    let text: String
    let isUser: Bool
}

struct ChatView: View {
    @State private var messages: [ChatMessage] = []
    @State private var inputText: String = ""
    var body: some View {
        VStack (spacing: 0){
            HStack(spacing: 10) {
                Image(systemName: "message.circle.fill")
                    .resizable()
                    .frame(width: 30, height: 30)
                    .foregroundColor(.blue)
                VStack(alignment: .leading, spacing: 2) {
                    Text("相談チャット")
                        .font(.title)
                        .bold()
                    Text("気軽に相談してみましょう")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                Spacer()
            }
            .padding()
            Divider()
            ScrollViewReader { scrollProxy in
                ScrollView{
                    VStack(alignment: .leading, spacing: 8){
                        ForEach(messages) { message in
                            HStack {
                                if message.isUser {
                                    Spacer()
                                    Text(message.text)
                                        .padding()
                                        .background(Color.green.opacity(0.3))
                                        .cornerRadius(10)
                                    VStack {
                                        Image(systemName: "person.fill")
                                            .foregroundColor(.green)
                                        Text("ユーザー")
                                            .font(.caption2)
                                            .foregroundColor(.secondary)
                                    }
                                } else {
                                    VStack {
                                        Image(systemName: "bubble.left.fill")
                                            .foregroundColor(.gray)
                                        Text("ボット")
                                            .font(.caption2)
                                            .foregroundColor(.secondary)
                                    }
                                    Text(message.text)
                                        .padding()
                                        .background(Color.gray.opacity(0.2))
                                        .cornerRadius(10)
                                    Spacer()
                                }
                            }
                            .id(message.id)
                        }
                    }
                    .padding()
                }
                .onChange(of: messages.count) { _ in
                    if let last = messages.last {
                        withAnimation {
                            scrollProxy.scrollTo(last.id, anchor: .bottom)
                        }
                    }
                }
            }
            
            
            HStack {
                TextField("メッセージを入力...", text: $inputText)
                    .padding(12)
                    .background(Color(UIColor.secondarySystemBackground))
                    .clipShape(Capsule())
                    .font(.body)
                    .onSubmit{
                        sendMessage()
                    }
                Button(action: {
                    sendMessage()
                }) {
                    Text("送信")
                        .padding(.horizontal, 16)
                        .padding(.vertical, 10)
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .clipShape(Capsule())
                }
            }
            .padding()
            .background(Color(UIColor.systemBackground))
        }
        .background(Color(UIColor.systemBackground))
    }
    
    func sendMessage() {
        let trimmedText = inputText.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmedText.isEmpty else { return }
        messages.append(ChatMessage(text: trimmedText, isUser: true))
        let response = "こんにちは、デモの応答です。"
        messages.append(ChatMessage(text: response, isUser:false))
        inputText = "" // Clear input field after sending
    }
    
}

#Preview {
    ChatView()
}
