//  ResetPasswordView.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/12.
//

import SwiftUI

struct ResetPasswordView: View {
    @StateObject var viewModel: ResetPasswordViewModel
    @Environment(\.dismiss) private var dismiss
    var body: some View { 
        ZStack {
            Color.blue.opacity(0.1)
                .ignoresSafeArea()
            VStack(spacing: 16) {
                Image(systemName: "heart.fill")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 50, height: 50)
                    .foregroundColor(.blue)

                Text("PeriodCare")
                    .font(.title)
                    .foregroundColor(.blue)

                Text("パスワード再設定")
                    .font(.title2)
                    .fontWeight(.bold)
                Text("登録したメールアドレスを入力してください")
                    .font(.caption)
                    .foregroundColor(.gray)

                TextField("メールアドレス", text: $viewModel.email)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding(.horizontal)

                Button(action: {
                    Task {
                        await viewModel.sendResetPassword()
                        dismiss()
                    }
                }) {
                    Text("パスワード再設定メールを送信")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
            }
            .padding()
            .frame(width: UIScreen.main.bounds.width * 0.8,
                   height: UIScreen.main.bounds.height * 0.5)
            .background(Color.white)
            .cornerRadius(20)
            .shadow(radius:10)
        }
    }
}
#Preview {
    ResetPasswordView(
        viewModel: ResetPasswordViewModel(userRepository: MockUserRepository())
        )
}