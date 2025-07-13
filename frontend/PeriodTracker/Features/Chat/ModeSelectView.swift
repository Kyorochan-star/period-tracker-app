import SwiftUI

struct ModeSelectView: View {
    @StateObject private var viewModel = ModeSelectViewModel()
    var body: some View {
        VStack(spacing: 24) {
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
            }.padding(.bottom, 2)

            Text("相談チャット")
                .font(.title)
                .bold()
                .padding(.bottom, 0)
            Text("話しやすい相手を選んでください")
                .font(.title3)
                .foregroundColor(.gray)
                .padding(.bottom, 2)
            
            Divider()
            
            ForEach(viewModel.modes, id: \.id) { mode in
                NavigationLink(destination: {
                    let vm = ChatViewModel(chatRepository: NetworkChatRepository(), mode: mode)
                    ChatView(viewModel: vm)
                }) {
                    HStack(spacing: 16) {

                        VStack(alignment: .leading) {
                            Text(mode.title)
                                .bold()
                                .foregroundColor(.black)
                            Text(mode.description)
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                    .frame(maxWidth: .infinity, minHeight: 50, alignment: .leading)
                    .padding()
                    .background(Color.white)
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(Color.gray.opacity(0.3), lineWidth: 1)
                    )
                    .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 2)
                    .cornerRadius(15)
                }
            }
        }
        .padding()
    }
}

#Preview {
    NavigationStack {
        ModeSelectView()
    }
}
