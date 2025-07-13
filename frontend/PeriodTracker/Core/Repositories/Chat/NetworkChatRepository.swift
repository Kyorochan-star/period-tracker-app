//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/11.
//
//  機能説明:
//  - チャットリポジトリのネットワーク実装（本番環境のAPIを使用）
//  内容：
//  - チャットメッセージ送信
//  - チャット履歴取得

import Foundation

final class NetworkChatRepository: ChatRepository {
    
    private let api = APIService()

    // チャットにメッセージを送信して、メッセージを返す
    func sendMessage(_ dto: ChatSendRequestDTO) async throws -> ChatMessage {
        let responseDTO: ChatSendResponseDTO = 
            try await api.post("/chat", data: dto)
        return responseDTO.toDomain()
    }

    // チャット履歴を取得する
    func getHistory() async throws -> [ChatMessage] {
        let responseDTO: ChatHistoryResponseDTO = 
            try await api.get("/chat")
        return responseDTO.map { $0.toDomain() }
    }

}
