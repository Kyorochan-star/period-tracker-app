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
        return try await withCheckedThrowingContinuation { continuation in
            api.post("/auth/register", data: dto) { (result: Result<UserRegisterResponseDTO, Error>) in
                switch result {
                case .success(let responseDTO):
                    continuation.resume(returning: responseDTO.toDomain())
                case .failure(let error):
                    continuation.resume(throwing: error)
                }
            }
        }
    }
    
    func login(_ dto: UserLoginRequestDTO) async throws -> User {
        // FastAPI の /auth/login は application/x-www-form-urlencoded で username/password を要求する

        return try await withCheckedThrowingContinuation { continuation in
            api.post("/auth/login", data: dto) { (result: Result<UserLoginResponseDTO, Error>) in
                switch result {
                case .success(let responseDTO):
                    // 取得した JWT を保存。APIService が自動で Authorization ヘッダに付与する
                    UserDefaults.standard.set(responseDTO.access_token, forKey: "authToken")
                    continuation.resume(returning: responseDTO.toDomain())
                case .failure(let error):
                    continuation.resume(throwing: error)
                }
            }
        }
    }

    // パスワード再設定要求
    func sendResetPassword(_ dto: ForgotPasswordRequestDTO) async throws -> ForgotPasswordResponseDTO {
        return try await withCheckedThrowingContinuation { continuation in
            api.post("/auth/forgot-password", data: dto) { (result: Result<ForgotPasswordResponseDTO, Error>) in
                switch result {
                case .success(let responseDTO):
                    continuation.resume(returning: responseDTO)
                case .failure(let error):
                    continuation.resume(throwing: error)
                }
            }
        }
    }

    func fetchProfile() async throws -> User {
        return try await withCheckedThrowingContinuation { continuation in
            api.get("/auth/me") { (result: Result<UserProfileResponseDTO, Error>) in
                switch result {
                case .success(let responseDTO):
                    continuation.resume(returning: responseDTO.toDomain())
                case .failure(let error):
                    continuation.resume(throwing: error)
                }
            }
        }
    }
}
