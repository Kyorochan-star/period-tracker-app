//  ChatDTO.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/11.
//
//  機能説明:
//  - チャット機能で使用するDTO
//  内容：
//  - チャット送信
//  - チャット履歴取得

import Foundation

// チャット送信 request 型定義
struct ChatSendRequestDTO: Codable {
    let query: String         // ユーザーの質問
    let role: String
    let mode: String          // 選択したモード (例: "王子様モード")
}

// チャット送信 response 型定義（1 メッセージ分）
struct ChatSendResponseDTO: Codable {
    let id: Int
    let userId: Int
    let role: String
    let query: String 
    let response: String 
    let timestamp: String  
    let mode: String 
}

// チャット履歴取得 response 型定義（配列）
typealias ChatHistoryResponseDTO = [ChatSendResponseDTO]

extension ChatSendResponseDTO {
    func toDomain() -> ChatMessage {
        ChatMessage(id: id,
                    userId: userId,
                    role: role,
                    text: response)
    }
}

// 送信リクエストDTO -> ドメイン変換（プレビューなどで再利用）
extension ChatSendRequestDTO {
    func toDomain(id: Int, userId: Int) -> ChatMessage {
        ChatMessage(id: id,
                    userId: userId,
                    role: role,
                    text: query)
    }
}
