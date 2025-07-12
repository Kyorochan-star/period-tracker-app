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
                    .frame(width: 80, height: 80)
                Text("💬")
                    .font(.system(size: 35))
            }
            
            Text("相談チャット")
                .font(.title)
                .bold()
            Text("話しやすい相手を選んでください")
                .font(.title3)
                .foregroundColor(.gray)
            
            Divider()
            
            ForEach(viewModel.modes, id: \.id) { mode in
                NavigationLink(destination: {
                    let vm = ChatViewModel(chatRepository: MockChatRepository(), mode: mode)
                    ChatView(viewModel: vm)
                }) {
                    HStack(spacing: 16) {
                        ZStack {
                            Circle()
                                .fill(
                                    LinearGradient(
                                        gradient: Gradient(colors: mode.Clor),
                                        //tartPoint: .topLeading,
                                        //endPoint: .bottomTrailing
                                    )
                                )
                                .frame(width: 60, height: 60)
                            
                            Text(mode.iconName)
                                .font(.system(size: 27))
                        }
                        
                        VStack(alignment: .leading) {
                            Text(mode.title)
                                .bold()
                                .foregroundColor(.black)
                            Text(mode.description)
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .background(Color.white)
                    .cornerRadius(15)
                    .foregroundColor(.black)
                    .overlay(
                        RoundedRectangle(cornerRadius: 15)
                            .stroke(Color.gray.opacity(0.5), lineWidth: 1)
                        )
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


