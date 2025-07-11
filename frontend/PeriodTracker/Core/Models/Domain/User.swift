import Foundation

struct User: Identifiable { 
    let user_id: Int 
    let email: String 
    let name: String
    let auth_provider: String
    // ユーザーIDをIDとして使用（Identifiable用）
    var id: Int { user_id }
}
