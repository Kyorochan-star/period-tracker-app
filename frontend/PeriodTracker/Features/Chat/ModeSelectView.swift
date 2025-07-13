import SwiftUI

struct ModeSelectView: View {
    @StateObject private var viewModel = ModeSelectViewModel()
    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "message.circle.fill")
                .resizable()
                .frame(width: 30, height: 30)
                .foregroundColor(.blue)
            Text("相談チャット")
                .font(.title2)
                .bold()
            Text("話しやすい相手を選んでください")
                .font(.title3)
                .foregroundColor(.gray)
            ForEach(viewModel.modes, id: \.id) { mode in
                NavigationLink(destination: {
                    let vm = ChatViewModel(chatRepository: NetworkChatRepository(), mode: mode)
                    ChatView(viewModel: vm)
                }) {
                    HStack(spacing: 16) {
                        Image(systemName: mode.iconName)
                            .foregroundColor(.blue)
                        VStack(alignment: .leading) {
                            Text(mode.title).bold()
                            Text(mode.description)
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .background(Color.blue.opacity(0.1))
                    .cornerRadius(10)
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
