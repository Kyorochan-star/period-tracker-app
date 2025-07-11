//  UserDTO.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/11.
//
//  機能説明:
//  - ユーザー情報を送信するためのDTO
//  内容：
//  - ユーザー新規登録
//  - ユーザーログイン
//  - ユーザープロフィール取得

import Foundation

// ユーザー新規登録 request型定義
struct UserRegisterRequestDTO: Codable {
    let email: String 
    let password: String 
    let name: String 
} 

// ユーザー新規登録 response型定義
struct UserRegisterResponseDTO: Codable {
    let access_token: String 
    let token_type: String 
    let user_id: Int 
    let email: String 
    let name : String 
    let auth_provider : String 
} 

// ユーザーログイン
struct UserLoginRequestDTO: Codable {
    let email: String 
    let hasehed_password: String 
} 

// ユーザーログイン response型定義
struct UserLoginResponseDTO: Codable {
    let access_token: String 
    let token_type: String 
    let user_id: Int 
    let email: String 
    let name : String 
    let auth_provider : String 
} 

// ユーザープロフィール取得　responseのみ型定義
struct UserProfileResponseDTO: Codable {
    let id: Int 
    let email: String 
    let auth_provider : String 
    let created_at : String 
} 
