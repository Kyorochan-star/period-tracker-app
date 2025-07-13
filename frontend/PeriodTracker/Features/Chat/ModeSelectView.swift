import SwiftUI

struct ModeSelectView: View {
    @StateObject private var viewModel = ModeSelectViewModel()
    var body: some View {
        ScrollView {
            VStack(spacing: 32) {
                Spacer(minLength: 20)
                
                // ヘッダーアイコン
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
                        .frame(width: 87, height: 87)
                    Text("💬")
                        .font(.system(size: 41.5))
                }
                .padding(.bottom, 8)

                // タイトル部分
                VStack(spacing: 12) {
                    Text("相談チャット")
                        .font(.title)
                        .bold()
                    Text("話しやすい相手を選んでください")
                        .font(.title3)
                        .foregroundColor(.gray)
                        .multilineTextAlignment(.center)
                }
                .padding(.bottom, 8)
                
                Divider()
                    .padding(.horizontal, 20)
                
                // キャラクター選択カード
                VStack(spacing: 20) {
                    ForEach(viewModel.modes, id: \.id) { mode in
                        NavigationLink(destination: {
                            let vm = ChatViewModel(chatRepository: MockChatRepository(), mode: mode)
                            ChatView(viewModel: vm)
                        }) {
                            HStack(spacing: 20) {
                                ZStack {
                                    Circle()
                                        .fill(mode.color)
                                        .frame(width: 70, height: 70)
                                    Text(mode.iconName)
                                        .font(.system(size: 35))
                                }

                                VStack(alignment: .leading, spacing: 6) {
                                    Text(mode.title)
                                        .font(.title2)
                                        .bold()
                                        .foregroundColor(.black)
                                    Text(mode.description)
                                        .font(.subheadline)
                                        .foregroundColor(.secondary)
                                        .lineLimit(2)
                                }
                                
                                Spacer()
                            }
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding(.horizontal, 20)
                            .padding(.vertical, 16)
                            .background(Color.white)
                            .overlay(
                                RoundedRectangle(cornerRadius: 12)
                                    .stroke(Color.gray.opacity(0.2), lineWidth: 1)
                            )
                            .shadow(color: Color.black.opacity(0.08), radius: 6, x: 0, y: 3)
                            .cornerRadius(12)
                        }
                        .padding(.horizontal, 4)
                    }
                }
                
                Spacer(minLength: 40)
            }
            .padding(.horizontal, 20)
        }
    }
}

#Preview {
    NavigationStack {
        ModeSelectView()
    }
}
