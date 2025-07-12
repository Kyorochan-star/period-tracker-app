//  Period.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/12.
//
//  機能説明:
//  - 周期情報を送信するためのDTO
//  内容：
//  - 開始ボタン
//  - 終了ボタン
//  - カレンダー表示&6ヶ月分の表示

import Foundation

struct Period: Identifiable { 
    let id: Int 
    let userid: Int 
    let startdate: String 
    let enddate: String 
    let prediction_next_date: String 
}
