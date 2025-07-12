import Foundation

final class MockChatRepository: ChatRepository {
    
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
            try await api.get("/chat/history")
        return responseDTO.map { $0.toDomain() }
    }

}
