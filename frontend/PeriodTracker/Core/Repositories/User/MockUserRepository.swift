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

/// NOTE: モック実装だが実 API に合わせてパスを `/auth/*` へ統一。
final class MockUserRepository: UserRepository {

    private let api = APIService()
    

    func register(_ dto: UserRegisterRequestDTO) async throws -> User {
        let responseDTO: UserRegisterResponseDTO = 
            try await api.post("/auth/register", data: dto)
        return responseDTO.toDomain()
    }
    func login(_ dto: UserLoginRequestDTO) async throws -> User {
        let responseDTO: UserLoginResponseDTO = 
            try await api.post("/auth/login", data: dto)
        return responseDTO.toDomain()
    }

    // パスワード再設定要求
    func sendResetPassword(_ dto: ForgotPasswordRequestDTO) async throws -> ForgotPasswordResponseDTO {
        let responseDTO: ForgotPasswordResponseDTO = 
            try await api.post("/auth/forgot-password", data: dto)
        return responseDTO
    }

    func fetchProfile() async throws -> User {
        let responseDTO: UserProfileResponseDTO = 
            try await api.get("/auth/me")
        return responseDTO.toDomain()
    }
}