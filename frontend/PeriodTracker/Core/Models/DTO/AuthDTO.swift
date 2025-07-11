//
//  AuthDTO.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/11.
//
//  機能説明:
//  - 認証情報を送信するためのDTO
//  内容：
//  - パスワード再設定要求
//  - パスワード再設定実行

import Foundation

// パスワード再設定要求 request型定義
struct ForgotPasswordRequestDTO: Codable {
    let email: String 
} 

// パスワード再設定要求 response型定義
struct ForgotPasswordResponseDTO: Codable {
    let message: String 
} 


// パスワード再設定実行 request型定義
struct ResetPasswordRequestDTO: Codable {
    let token: String
    let password: String
}

// パスワード再設定実行 response型定義
struct ResetPasswordResponseDTO: Codable {
    let message: String 
} 
