//
//  LoginView.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/04.
//
//  機能説明:
//  - ユーザーログイン画面

import SwiftUI

struct LoginView: View {
    @StateObject var viewModel: LoginViewModel
    @Binding var isLoggedIn: Bool
    var body: some View {
        NavigationStack {
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
                            .fontWeight(.bold)
                        
                        Text("ログイン")
                            .font(.title2)
                            .fontWeight(.bold)
                        
                        Text("あなたの健康をサポート")
                            .font(.caption)
                            .foregroundColor(.gray)
                        
                        TextField("メールアドレス", text: $viewModel.email)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .padding(.horizontal)
                        
                        SecureField("パスワード", text: $viewModel.password)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .padding(.horizontal)
                        
                        NavigationLink(destination: ResetPasswordView(viewModel: ResetPasswordViewModel(userRepository: MockUserRepository()))) {
                            Text("パスワードをお忘れの方はこちら")
                                .font(.footnote)
                                .foregroundColor(.blue)
                        }
                        .padding(.horizontal)


                        Button(action: {
                            // LoginViewModel.login()は非同期関数だが、
                            // Buttonのactionは非同期関数ではないため、
                            // Taskでラップする必要がある
                            Task {
                                await viewModel.login()
                                if viewModel.isLoggedIn {
                                    isLoggedIn = true
                                }
                            }
                        }) {
                            Text("ログイン")
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(8)
                        }
                        .padding(.horizontal)
                        
                        
                        
                        Button(action: {
                            // Googleログイン処理
                        }) {
                            Text("Google でログイン")
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(Color.gray.opacity(0.2))
                                .foregroundColor(.black)
                                .cornerRadius(8)
                        }
                        .padding(.horizontal)
                        Divider()
                        Text("登録がお済みでない方はこちら")
                            .font(.caption)

                        NavigationLink(destination: SignUpView(viewModel: SignUpViewModel(userRepository: MockUserRepository()))) {
                            Text("新規登録")
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(8)
                        }
                        .padding(.horizontal)
                    
                }
                .frame(width: UIScreen.main.bounds.width * 0.8,
                       height: UIScreen.main.bounds.height * 0.7)
                .background(Color.white)
                .cornerRadius(20)
                .shadow(radius:10)
            }
        }
    }
}

#Preview {
    LoginView(
        viewModel: LoginViewModel(userRepository: MockUserRepository()),
        isLoggedIn: .constant(false))
}
