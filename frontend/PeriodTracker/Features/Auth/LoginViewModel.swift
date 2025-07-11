//
//  LoginViewModel.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/11.
//

import Foundation
import Combine


@MainActor
final class LoginViewModel: ObservableObject {
    // バインディング用のプロパティ
    @Published var email: String = ""
    @Published var password: String = ""

    @Published var error: String? = nil
    @Published var isLoggedIn: Bool = false

    // リポジトリの注入
    private let userRepository: UserRepository
    init(userRepository: UserRepository) {
        self.userRepository = userRepository
    }

    func login() async {
        // バリデーション
        guard validate() else { return } 

        do {
            let request = UserLoginRequestDTO(email: email, hashed_password: password)
            let user = try await userRepository.login(request)
            // ログイン成功時の処理
            isLoggedIn = true
        } catch{
            // エラー時の処理＝＞拡張する必要あり
            self.error = error.localizedDescription
        } 
    }

    private func validate() -> Bool {
        if email.isEmpty || password.isEmpty {
            self.error = "メールアドレスとパスワードを入力してください"
            return false
        }
        if !email.contains("@") {
            self.error = "有効なメールアドレスを入力してください"
            return false
        }
        self.error = nil
        return true
    }
}
