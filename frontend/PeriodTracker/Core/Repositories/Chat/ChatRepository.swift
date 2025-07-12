import Foundation

protocol ChatRepository {
    // チャットにメッセージを送信して、メッセージを返す
    func sendMessage(_ request: ChatSendRequestDTO) async throws -> ChatMessage
    // チャット履歴を取得する
    func getHistory() async throws -> [ChatMessage]
}