//
//  SettingView.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/06.
//

import SwiftUI

struct SettingView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 24) {
            Text("設定")
                .font(.largeTitle)
                .bold()
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(.horizontal)

            // Settings List
            VStack(spacing: 1) {
                settingRow(icon: "person", title: "プロフィール設定")
                settingRow(icon: "bell", title: "通知設定")
                settingRow(icon: "shield", title: "プライバシー設定")
                settingRow(icon: "questionmark.circle", title: "ヘルプ・サポート")
                settingRow(icon: "doc.text", title: "利用規約")
            }
            .background(Color(.systemBackground))
            .cornerRadius(16)
            .padding(.horizontal)
            .shadow(color: Color.black.opacity(0.05), radius: 5, x: 0, y: 2)

            // Logout Button
            VStack(spacing: 0) {
                Button(action: {
                    //ここに処理を記述
                }) {
                    HStack {
                        Image(systemName: "rectangle.portrait.and.arrow.right")
                            .font(.title3)
                            .foregroundColor(.red)
                            .frame(width: 30)
                        Text("ログアウト")
                            .font(.body)
                            .foregroundColor(.red)
                        Spacer()
                        Image(systemName: "chevron.right")
                            .foregroundColor(.red)
                            .font(.system(size: 14, weight: .semibold))
                    }
                    .padding()
                    .background(Color(.systemBackground))
                    .cornerRadius(16)
                }
                .padding(.horizontal)
                .shadow(color: Color.black.opacity(0.05), radius: 5, x: 0, y: 2)
            }

            Spacer()
        }
        .padding(.top)
        .background(Color(.systemGroupedBackground).ignoresSafeArea())
    }

    // それぞれの描画処理
    private func settingRow(icon: String, title: String) -> some View {
        Button(action: {
        }) {
            HStack {
                Image(systemName: icon)
                    .font(.title3)
                    .foregroundColor(.primary)
                    .frame(width: 30)
                Text(title)
                    .font(.body)
                    .foregroundColor(.primary)
                Spacer()
                Image(systemName: "chevron.right")
                    .foregroundColor(.gray)
                    .font(.system(size: 14, weight: .semibold))
            }
            .padding()
            .background(Color(.clear))
        }
        .buttonStyle(PlainButtonStyle())
    }
}


#Preview {
    SettingView()
}
