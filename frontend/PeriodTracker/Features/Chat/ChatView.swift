//
//  ChatView.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/04.
//
//  機能説明:
//  - AIチャット相談画面

import SwiftUI


struct ChatView: View {
    @StateObject private var viewModel: ChatViewModel

    // 初期化時に外部から ViewModel を受け取って StateObject に昇格させる
    init(viewModel: ChatViewModel) {
        _viewModel = StateObject(wrappedValue: viewModel)
    }


    var body: some View {
        VStack (spacing: 0){
            HStack(spacing: 10) {
                Image(systemName: viewModel.mode.iconName)
                    .resizable()
                    .frame(width: 30, height: 30)
                    .foregroundColor(.blue)
                VStack(alignment: .leading, spacing: 2) {
                    Text(viewModel.mode.title)
                        .font(.title)
                        .bold()
                    Text(viewModel.mode.description)
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
                        ForEach(viewModel.messages, id: \.id) { message in
                            HStack {
                                if message.role == "user" {
                                    Spacer()
                                    Text(message.text)
                                        .padding()
                                        .background(Color.green.opacity(0.3))
                                        .cornerRadius(10)
                                    VStack {
                                        Image(systemName: "person.fill")
                                            .foregroundColor(.green)
                                        Text("あなた")
                                            .font(.caption2)
                                            .foregroundColor(.secondary)
                                    }
                                } else {
                                    VStack {
                                        Image(systemName: "bubble.left.fill")
                                            .foregroundColor(.gray)
                                        Text(viewModel.mode.title)
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
                            .padding(.vertical, 4)
                        }
                    }
                    .padding()
                }
                .onChange(of: viewModel.messages.count) { _ in
                    if let last = viewModel.messages.last {
                        withAnimation {
                            scrollProxy.scrollTo(last.id, anchor: .bottom)
                        }
                    }
                }
            }
            
            Divider()
            
            HStack {
                TextField("メッセージを入力...", text: $viewModel.text)
                    .padding(12)
                    .background(Color(UIColor.secondarySystemBackground))
                    .clipShape(Capsule())
                    .font(.body)
                    .onSubmit{
                        Task {
                            await viewModel.sendMessage()
                        }
                    }
                Button(action: {
                    Task {
                        await viewModel.sendMessage()
                    }
                }) {
                    Image(systemName: "paperplane")
                        .foregroundColor(.white)
                        .padding(12)
                        .bold()
                        .background(
                            LinearGradient(
                                gradient: Gradient(colors: [
                                    Color(red: 0.1, green: 0.6, blue: 0.99),
                                    Color(red: 0.1, green: 0.82, blue: 0.95)
                                ]),
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                        .clipShape(Circle())
                }
            }
            .padding()
            .background(Color(UIColor.systemBackground))
        }
        .background(Color(UIColor.systemBackground))
    }
    
    
}

#Preview {
    ChatView(viewModel: ChatViewModel(chatRepository: NetworkChatRepository(), mode: ChatMode(.prince)))
}
