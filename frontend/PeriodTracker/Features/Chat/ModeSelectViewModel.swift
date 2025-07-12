//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/12.
//

import Foundation

@MainActor
final class ModeSelectViewModel: ObservableObject {
    // 画面に表示するモード一覧（ローカル定義）
    @Published var modes: [ChatMode] = [
        ChatMode(id: "boyfriend", title: "彼氏", description: "理解のある優しい彼氏", iconName: "person.fill"),
        ChatMode(id: "prince", title: "王子様", description: "優しく気遣ってくれる王子様", iconName: "crown.fill"),
        ChatMode(id: "nurse", title: "先生", description: "医学的知識豊富な保健室の先生", iconName: "stethoscope"),
        ChatMode(id: "grandma", title: "おばあちゃん", description: "経験豊富で知恵のあるおばあちゃん", iconName: "figure.and.child.holdinghands"),
        ChatMode(id: "mother", title: "お母さん", description: "暖かく包み込んでくれるお母さん", iconName: "heart.fill")
    ]

    // 選択されたモード（必要に応じて利用）
    @Published var selectedMode: ChatMode? = nil
}