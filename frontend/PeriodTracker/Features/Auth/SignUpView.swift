//
//  SignUp.swift
//  FriendsFavoriteMovies
//
//  Created by 藤瀬太翼 on 2025/07/04.
//

import SwiftUI

struct SignUpView: View {
    @State private var isAgreementChecked = false
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
                
                TextField("お名前", text: .constant(""))
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                TextField("メールアドレス", text: .constant(""))
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                SecureField("パスワード", text: .constant(""))
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                SecureField("パスワード（確認）", text: .constant(""))
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                Button(action: {
                    isAgreementChecked.toggle()
                }) {
                    HStack(alignment: .top) {
                        Image(systemName: isAgreementChecked ? "checkmark.square" : "square")
                            .padding(.top, 2)
                        Text(.init("[利用規約](https://example.com/terms)及び[プライバシーポリシー](https://example.com/privacy)に同意してアカウントを作成します。"))
                            .font(.footnote)
                            .foregroundColor(.primary)
                    }
                }
                .buttonStyle(PlainButtonStyle())
                .padding()
                
                Button(action: {
                    // 登録処理
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
    SignUpView()
}
