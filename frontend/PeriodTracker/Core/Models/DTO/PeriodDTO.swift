//  PeriodDTO.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/11.
//
//  機能説明:
//  - 周期情報を送信するためのDTO
//  内容：
//  - 開始ボタン
//  - 終了ボタン
//  - カレンダー表示&6ヶ月分の表示

import Foundation

// 開始ボタン request型定義
struct PeriodStartRequestDTO: Codable {
    let id : Int 
    let startdate: String
}

// 開始ボタン response型定義
struct PeriodStartResponseDTO: Codable {
    let id: Int 
    let userid: Int 
    let startdate: String 
    let enddate : String 
    let prediction_next_date: String 
    let prediction_end_date: String 
    let created_at: String 
    let updated_at : String 
}

extension PeriodStartResponseDTO {
    func toDomain() -> Period {
        return Period(id: id, userid: userid, startdate: startdate, enddate: enddate, prediction_next_date: prediction_next_date)
    }
}

// 終了ボタン request型定義
struct PeriodEndRequestDTO: Codable {
    let id : Int 
    let userid : Int 
    let enddate : String 
} 

// 終了ボタン response型定義
struct PeriodEndResponseDTO: Codable {
    let id : Int 
    let userid : Int 
    let startdate : String 
    let enddate : String 
    let prediction_next_date : String 
    let prediction_end_date : String 
    let created_at : String 
    let updated_at : String 
} 

extension PeriodEndResponseDTO {
    func toDomain() -> Period {
        return Period(id: id, userid: userid, startdate: startdate, enddate: enddate, prediction_next_date: prediction_next_date)
    }
}

// カレンダー表示&6ヶ月分の表示 request型定義
struct PeriodCalendarRequestDTO: Codable {
    let id : Int 
    let userid : Int 
} 

// カレンダー表示&6ヶ月分の表示 response型定義
struct PeriodCalendarResponseDTO: Codable {
    let id : Int 
    let userid : Int 
    let startdate : String 
    let enddate : String 
    let prediction_next_date : String 
    let created_at : String 
    let updated_at : String 
} 

extension PeriodCalendarResponseDTO {
    func toDomain() -> Period {
        return Period(id: id, userid: userid, startdate: startdate, enddate: enddate, prediction_next_date: prediction_next_date)
    }
}