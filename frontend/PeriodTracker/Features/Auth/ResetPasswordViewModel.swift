//  ResetPasswordViewModel.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/12.
//

import Foundation
import Combine

@MainActor
final class ResetPasswordViewModel: ObservableObject {
    @Published var email: String = ""
    @Published var error: String? = nil

    private let userRepository: UserRepository
    init(userRepository: UserRepository) {
        self.userRepository = userRepository
    }

    func sendResetPassword() async -> Bool {
        guard validate() else { return false }

        do {
            let request = ForgotPasswordRequestDTO(email: email)
            let response = try await userRepository.sendResetPassword(request)
            return true
        } catch {
            self.error = error.localizedDescription
            return false
        }
    }
    
    private func validate() -> Bool {
        if email.isEmpty {
            self.error = "メールアドレスを入力してください"
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