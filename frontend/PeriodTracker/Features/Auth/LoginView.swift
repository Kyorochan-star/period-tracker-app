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
                    .padding(.top, 19)
                    
                    Text("PeriodCare")
                        .font(.title)
                        .fontWeight(.bold)
                    
                    Text("あなたの健康をサポート")
                        .font(.caption)
                        .foregroundColor(.gray)
                    
                    Text("ログイン")
                        .font(.title2)
                        .fontWeight(.bold)
                    
                    TextField("メールアドレス", text: $viewModel.email)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .padding(.horizontal)
                    
                    SecureField("パスワード", text: $viewModel.password)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .padding(.horizontal)
                    
                    if let error = viewModel.error {
                        Text(error)
                            .foregroundColor(.red)
                            .font(.caption)
                            .padding(.horizontal)
                    }
                    
                    Button(action: {
                        // LoginViewModel.login()は非同期関数だが、
                        // Buttonのactionは非同期関数ではないため、
                        // Taskでラップする必要がある
                        Task {
                            await viewModel.login()
                            if viewModel.isLoggedIn {
                                isLoggedIn = true
                                print("Login successful, isLoggedIn set to true")
                            }
                        }
                    }) {
                        Text("ログイン")
                            .fontWeight(.bold)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(
                                LinearGradient(
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
                    .padding(.horizontal)
                    
                    NavigationLink(destination: ResetPasswordView(viewModel: ResetPasswordViewModel(userRepository: NetworkUserRepository()))) {
                        (
                            Text("パスワードをお忘れの方は")
                                .foregroundColor(.black)
                            +
                            Text("こちら")
                                .fontWeight(.bold)
                                .foregroundColor(.blue)
                        )
                        .font(.footnote)
                    }
                    .padding(.horizontal)
                    
                    Divider()
                    
                    Button(action: {
                        // Googleログイン処理
                    }) {
                        Text("Google でログイン")
                            .fontWeight(.bold)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(.white)
                            .foregroundColor(.black)
                            .overlay(
                                RoundedRectangle(cornerRadius: 15)
                                    .stroke(Color.gray.opacity(0.5), lineWidth: 1)
                            )
                            .cornerRadius(15)
                    }
                    .padding(.horizontal)
                    
                    NavigationLink(destination: SignUpView(viewModel: SignUpViewModel(userRepository: NetworkUserRepository()))) {
                        Text("新規登録")
                            .font(.system(size: 16.9))
                            .fontWeight(.bold)
                            .padding()
                            .foregroundColor(.blue)
                    }
                    .padding(.horizontal)
                    .padding(.bottom, 12)
                }
                .frame(width: UIScreen.main.bounds.width * 0.8,
                       height: UIScreen.main.bounds.height * 0.75)
                .background(Color.white)
                .cornerRadius(20)
                .shadow(radius: 10)
            }
        }
    }
}
    
    #Preview {
        LoginView(
            viewModel: LoginViewModel(userRepository: NetworkUserRepository()),
            isLoggedIn: .constant(false))
    }
