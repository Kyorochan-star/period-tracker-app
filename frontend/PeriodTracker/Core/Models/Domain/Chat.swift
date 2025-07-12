//  Chat.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/12.
//

import Foundation

// チャットメッセージ
struct ChatMessage : Identifiable {
    let id: Int
    let userId: Int
    let role: String
    let text: String 
}

// チャットモード
struct ChatMode: Identifiable {
    let id: String
    let title: String
    let description: String
    let iconName: String
}