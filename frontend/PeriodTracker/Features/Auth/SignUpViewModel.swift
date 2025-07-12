// 
//  SignUpViewModel.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/11.
//

import Foundation
import Combine

@MainActor
final class SignUpViewModel: ObservableObject {
    // バインディング用のプロパティ
    @Published var name: String = "" 
    @Published var email: String = ""
    @Published var password: String = ""
    @Published var confirmPassword: String = ""

    @Published var error: String? = nil

    // リポジトリの注入
    private let userRepository: UserRepository
    init(userRepository: UserRepository) {
        self.userRepository = userRepository
    }

    func signUp() async -> Bool {
        // バリデーション
        guard validate() else { return false }

        do { 
            let request = UserRegisterRequestDTO(email: email, password: password, name: name)
            let user = try await userRepository.register(request)
            //  登録成功時の処理
            return true 
        } catch {
            // エラー時の処理＝＞拡張する必要あり
            self.error = error.localizedDescription
            return false 
            
        }
    }

    private func validate() -> Bool {
        if name.isEmpty || email.isEmpty || password.isEmpty || confirmPassword.isEmpty {
            self.error = "すべてのフィールドを入力してください"
            return false
        }
        if password != confirmPassword {
            self.error = "パスワードが一致しません"
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
