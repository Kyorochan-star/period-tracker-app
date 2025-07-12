//
//  SignUpView.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/04.
//
//  機能説明:
//  - ユーザー新規登録画面

import SwiftUI

struct SignUpView: View {
    @StateObject var viewModel: SignUpViewModel
    @Environment(\.dismiss) private var dismiss
    var body: some View {
        ZStack{
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
                    .fontWeight(.bold)
                
                Text("あなたの健康をサポート")
                    .font(.caption)
                    .foregroundColor(.gray)
                
                TextField("お名前", text: $viewModel.name)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                TextField("メールアドレス", text: $viewModel.email)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                SecureField("パスワード", text: $viewModel.password)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                SecureField("パスワード（確認）", text: $viewModel.confirmPassword)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                Button(action: {
                    // 登録処理
                    Task {
                        if await viewModel.signUp() {
                            // 登録成功時の処理
                            dismiss()
                        } else {
                            // 登録失敗時の処理
                        }
                    }
                }) {
                    Text("新規登録")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
            }
            .padding()
            .frame(width: UIScreen.main.bounds.width * 0.8,
                   height: UIScreen.main.bounds.height * 0.7)
            .background(Color.white)
            .cornerRadius(20)
            .shadow(radius:10)
            
        }
        
    }
}

#Preview {
    SignUpView(
        viewModel: SignUpViewModel(userRepository: MockUserRepository())
        )
}
