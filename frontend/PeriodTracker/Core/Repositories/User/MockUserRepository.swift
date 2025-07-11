//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/11.
// 
//  機能説明:
//  - ユーザーリポジトリのモック実装（test.pyのエンドポイントを使用）
//  内容：
//  - ユーザー新規登録
//  - ユーザーログイン
//  - ユーザープロフィール取得

import Foundation 

final class MockUserRepository: UserRepository {

    private let api = APIService()
    

    func register(_ dto: UserRegisterRequestDTO) async throws -> User {
        let responseDTO: UserRegisterResponseDTO = 
            try await api.post("http://127.0.0.1:8000/register", data: dto)
        return responseDTO.toDomain()
    }
    func login(_ dto: UserLoginRequestDTO) async throws -> User {
        let responseDTO: UserLoginResponseDTO = 
            try await api.post("http://127.0.0.1:8000/login", data: dto)
        return responseDTO.toDomain()
    }
    func fetchProfile() async throws -> User {
        let responseDTO: UserProfileResponseDTO = 
            try await api.get("http://127.0.0.1:8000/me")
        return responseDTO.toDomain()
    }
}