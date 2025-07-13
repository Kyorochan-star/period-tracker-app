//  Chat.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/12.
//

import Foundation

// MARK: - Message
struct ChatMessage: Identifiable {
    let id: Int
    let userId: Int
    let role: String   // "user" / "assistant"
    let text: String
    let createdAt: String? = nil // 使わない場合は nil
}

// MARK: - Mode Type (通信キー)
enum ChatModeType: String, Codable, CaseIterable, Identifiable {
    case prince = "PRINCE"
    case mom = "MOM"
    case grandma = "GRANDMA"
    case boyfriend = "BOYFRIEND"
    case nurse = "NURSE"

    var id: String { rawValue }
}

// MARK: - Mode Meta (UI 用)
struct ChatMode: Identifiable {
    let id: ChatModeType              // 通信キー
    let title: String
    let description: String
    let iconName: String

    init(_ type: ChatModeType) {
        self.id = type
        switch type {
        case .prince:
            title = "王子様"
            description = "優しくロマンチックに励まします"
            iconName = "👑"
        case .mom:
            title = "お母さん"
            description = "温かく実践的なアドバイス"
            iconName = "👩"
        case .grandma:
            title = "おばあちゃん"
            description = "昔ながらの知恵で安心感を"
            iconName = "👵"
        case .boyfriend:
            title = "彼氏"
            description = "共感力高めで寄り添います"
            iconName = "💝"
        case .nurse:
            title = "保健室の先生"
            description = "医学的に正確で丁寧な説明"
            iconName = "🩺"
        }
    }
}
