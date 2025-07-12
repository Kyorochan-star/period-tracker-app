//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/12.
//

import Foundation
import SwiftUI

@MainActor
final class ModeSelectViewModel: ObservableObject {
     画面に表示するモード一覧（ローカル定義）
    @Published var modes: [ChatMode] = [
        ChatMode(id: "boyfriend", title: "彼氏", description: "理解のある優しい彼氏", iconName: "💝", gradient: [Color.pink]),
        ChatMode(id: "prince", title: "王子様", description: "優しく気遣ってくれる王子様", iconName: "👑", gradient: [Color.yellow]),
        ChatMode(id: "nurse", title: "先生", description: "医学的知識豊富な保健室の先生", iconName: "🩺", gradient: [Color.cyan]),
        ChatMode(id: "grandma", title: "おばあちゃん", description: "経験豊富で知恵のあるおばあちゃん", iconName: "👵", gradient: [Color.gray]),
        ChatMode(id: "mother", title: "お母さん", description: "暖かく包み込んでくれるお母さん", iconName: "👩", gradient: [ Color.orange])
    ]

     選択されたモード（必要に応じて利用）
    @Published var selectedMode: ChatMode? = nil
}
