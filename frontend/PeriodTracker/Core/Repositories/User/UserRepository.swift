import Foundation 

// ユーザーリポジトリのプロトコル
// モックと本番の切り替え用


protocol UserRepository {
    // ユーザー新規登録
    func register(_ request: UserRegisterRequestDTO) async throws -> User 
    // ユーザーログイン
    func login(_ request: UserLoginRequestDTO) async throws -> User 
    // ユーザープロフィール取得
    func fetchProfile() async throws -> User 
}

// _ requestは呼び出し側でラベルを書く必要がない
// let request = UserLoginRequestDTO(...)
// 通常：login(request: request)
// この場合：login(request)