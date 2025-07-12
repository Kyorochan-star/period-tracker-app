//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/12.
//

import Foundation

@MainActor
final class ModeSelectViewModel: ObservableObject {
    // 画面に表示するモード一覧（ローカル定義）
    @Published var modes: [ChatMode] = ChatModeType.allCases.map { ChatMode($0) }

    // 選択されたモード（必要に応じて利用）
    @Published var selectedMode: ChatMode? = nil
}