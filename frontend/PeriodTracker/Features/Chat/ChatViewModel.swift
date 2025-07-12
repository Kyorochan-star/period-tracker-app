// 
//  ChatViewModel.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/12.
//

import Foundation
import Combine

@MainActor
final class ChatViewModel: ObservableObject {
    // バインディング用のプロパティ
    @Published var text: String = ""
    @Published var messages: [ChatMessage] = []
    @Published var mode: ChatMode
    @Published var error: String? = nil 

    // リポジトリの注入
    private let chatRepository: ChatRepository
    init(chatRepository: ChatRepository, mode: ChatMode) {
        self.chatRepository = chatRepository
        self.mode = mode 
    }

    func sendMessage() async -> Bool { 
        // バリデーション
        guard validate() else { return false } 

        do {
            // ① リクエストDTOを作成し、そのままユーザーメッセージとして追加
            let request = ChatSendRequestDTO(query: text, role: "user", mode: mode.id.rawValue)
            messages.append(request.toDomain(id: messages.count, userId: 1))

            // ② API へ送信
            let response = try await chatRepository.sendMessage(request)

            // ③ ボット返信を追加
            messages.append(response)

            text = ""
            return true
        } catch { 
            // エラー時の処理
            self.error = error.localizedDescription
            return false 
        }
    }

    private func validate() -> Bool { 
        if text.isEmpty { 
            self.error = "メッセージを入力してください"
            return false 
        }
        self.error = nil 
        return true 
    }
}
