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
            LinearGradient(
                gradient: Gradient(colors: [
                    Color(red: 0.8, green: 0.95, blue: 1.0),
                    Color(red: 0.92, green: 0.96, blue: 1.0)
                ]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
                .ignoresSafeArea()
            VStack(spacing: 16) {
                ZStack {
                    Circle()
                        .fill(
                            LinearGradient(
                                gradient: Gradient(colors: [
                                    Color(red: 0.0, green: 0.6, blue: 0.99),
                                    Color(red: 0.1, green: 0.85, blue: 0.95)
                                ]),
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                        .frame(width: 80, height: 80)
                    Image(systemName: "heart.fill")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 38, height: 40)
                        .foregroundColor(.white)
                }
                
                Text("PeriodCare")
                    .font(.title)
                    .fontWeight(.bold)
                
                Text("あなたの健康をサポート")
                    .font(.caption)
                    .foregroundColor(.gray)
                
                Text("新規登録")
                    .font(.title2)
                    .fontWeight(.bold)
                
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
                        .fontWeight(.bold)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(LinearGradient(
                            gradient: Gradient(colors: [
                                Color(red: 0.0, green: 0.6, blue: 0.99),
                                Color(red: 0.1, green: 0.82, blue: 0.95)
                            ]),
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                        )
                        .foregroundColor(.white)
                        .cornerRadius(15)
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
