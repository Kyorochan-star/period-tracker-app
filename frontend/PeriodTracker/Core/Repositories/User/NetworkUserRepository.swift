//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/11.
//
//  機能説明:
//  - ユーザーリポジトリのネットワーク実装（本番環境のAPIを使用）
//  内容：
//  - ユーザー新規登録
//  - ユーザーログイン
//  - ユーザープロフィール取得

// 拡張：
//  - ベースURLを環境変数で管理
//  - HTTPS+認証ヘッダの追加
//  - リフレッシュトークン処理、タイムアウト・リトライポリシー

import Foundation 

final class NetworkUserRepository: UserRepository {

    private let api = APIService()
    

    func register(_ dto: UserRegisterRequestDTO) async throws -> User {
        let responseDTO: UserRegisterResponseDTO = 
            try await api.post("本番環境のAPIのURL", data: dto)
            // 本番環境のAPIのURLに差し替え
        return responseDTO.toDomain()
    }
    func login(_ dto: UserLoginRequestDTO) async throws -> User {
        let responseDTO: UserLoginResponseDTO = 
            try await api.post("本番環境のAPIのURL", data: dto)
            // 本番環境のAPIのURLに差し替え
        return responseDTO.toDomain()
    }
    func fetchProfile() async throws -> User {
        let responseDTO: UserProfileResponseDTO = 
            try await api.get("本番環境のAPIのURL")
            // 本番環境のAPIのURLに差し替え
        return responseDTO.toDomain()
    }
}