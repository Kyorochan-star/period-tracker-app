//
//  testapi.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/06.
//
import SwiftUI
import Foundation
// DTOファイルを直接import
// もしmodule importが不要なら下記importは省略可
// import "../Models/DTO/UserDTO.swift"
// import "../Models/DTO/PeriodDTO.swift"
// import "../Models/DTO/ChatDTO.swift"
// import "../Models/DTO/AuthDTO.swift"

struct TestAPIView: View {
    @State private var resultText = ""
    
    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                // /register (POST)
                Button("Test /register (POST)") {
                    let apiService = APIService()
                    let registerData = UserRegisterRequestDTO(email: "test@example.com", password: "password", name: "テストユーザー")
                    apiService.post("\(APIConfig.baseURL)/auth/register", data: registerData) { (result: Result<UserRegisterResponseDTO, Error>) in
                        switch result {
                        case .success(let data):
                            resultText = "register: \(data)"
                        case .failure(let error):
                            resultText = "register error: \(error.localizedDescription)"
                        }
                    }
                }
                // /login (POST)
                Button("Test /login (POST)") {
                    let apiService = APIService()
                    let loginData = UserLoginRequestDTO(email: "test@example.com", password: "password")
                    apiService.post("\(APIConfig.baseURL)/auth/login", data: loginData) { (result: Result<UserLoginResponseDTO, Error>) in
                        switch result {
                        case .success(let data):
                            resultText = "login: \(data)"
                        case .failure(let error):
                            resultText = "login error: \(error.localizedDescription)"
                        }
                    }
                }
                // /google (POST)
                Button("Test /google (POST)") {
                    let apiService = APIService()
                    let googleData = ["id_token_str": "sample_id_token"] // 必要ならDTO化
                    apiService.post("\(APIConfig.baseURL)/auth/google", data: googleData) { (result: Result<UserLoginResponseDTO, Error>) in
                        switch result {
                        case .success(let data):
                            resultText = "google: \(data)"
                        case .failure(let error):
                            resultText = "google error: \(error.localizedDescription)"
                        }
                    }
                }
                // /forgot-password (POST)
                Button("Test /forgot-password (POST)") {
                    let apiService = APIService()
                    let forgotData = ForgotPasswordRequestDTO(email: "test@example.com")
                    apiService.post("\(APIConfig.baseURL)/auth/forgot-password", data: forgotData) { (result: Result<ForgotPasswordResponseDTO, Error>) in
                        switch result {
                        case .success(let data):
                            resultText = "forgot-password: \(data)"
                        case .failure(let error):
                            resultText = "forgot-password error: \(error.localizedDescription)"
                        }
                    }
                }
                // /reset-password (POST)
                Button("Test /reset-password (POST)") {
                    let apiService = APIService()
                    let resetData = ResetPasswordRequestDTO(token: "sampletoken", password: "newpassword")
                    apiService.post("\(APIConfig.baseURL)/auth/reset-password", data: resetData) { (result: Result<ResetPasswordResponseDTO, Error>) in
                        switch result {
                        case .success(let data):
                            resultText = "reset-password: \(data)"
                        case .failure(let error):
                            resultText = "reset-password error: \(error.localizedDescription)"
                        }
                    }
                }
                // /me (GET)
                Button("Test /me (GET)") {
                    let apiService = APIService()
                    apiService.get("\(APIConfig.baseURL)/auth/me") { (result: Result<UserProfileResponseDTO, Error>) in
                        switch result {
                        case .success(let data):
                            resultText = "me: \(data)"
                        case .failure(let error):
                            resultText = "me error: \(error.localizedDescription)"
                        }
                    }
                }
                // /period (POST)
                Button("Test /period (POST)") {
                    let apiService = APIService()
                    let periodData = PeriodStartRequestDTO(startdate: "2025-07-11")
                    apiService.post("\(APIConfig.baseURL)/periods", data: periodData) { (result: Result<PeriodStartResponseDTO, Error>) in
                        switch result {
                        case .success(let data):
                            resultText = "period post: \(data)"
                        case .failure(let error):
                            resultText = "period post error: \(error.localizedDescription)"
                        }
                    }
                }
                // /period (PATCH)
                Button("Test /period (PATCH)") {
                    let apiService = APIService()
                    let periodUpdate = PeriodEndRequestDTO(id: 1, userid: 1, enddate: "2025-07-17")
                    apiService.patch("\(APIConfig.baseURL)/periods/1", data: periodUpdate) { (result: Result<PeriodEndResponseDTO, Error>) in
                        switch result {
                        case .success(let data):
                            resultText = "period patch: \(data)"
                        case .failure(let error):
                            resultText = "period patch error: \(error.localizedDescription)"
                        }
                    }
                }
                // /period (GET)
                Button("Test /period (GET)") {
                    let apiService = APIService()
                    apiService.get("\(APIConfig.baseURL)/periods") { (result: Result<PeriodCalendarResponseDTO, Error>) in
                        switch result {
                        case .success(let data):
                            resultText = "period: \(data)"
                        case .failure(let error):
                            resultText = "period error: \(error.localizedDescription)"
                        }
                    }
                }
                // /period (DELETE)
                Button("Test /period (DELETE)") {
                    let url = URL(string: "\(APIConfig.baseURL)/periods/1")!
                    var request = URLRequest(url: url)
                    request.httpMethod = "DELETE"
                    let task = URLSession.shared.dataTask(with: request) { data, response, error in
                        if let error = error {
                            resultText = "period delete error: \(error.localizedDescription)"
                        } else {
                            resultText = "period delete: success"
                        }
                    }
                    task.resume()
                }
                // /chat (POST)
                Button("Test /chat (POST)") {
                    let apiService = APIService()
                    let chatData = ChatSendRequestDTO(query: "生理痛がつらいです…",
                                                      role: "user", mode: "PRINCE")
                    apiService.post("http://127.0.0.1:8000/chat", data: chatData) { (result: Result<ChatSendResponseDTO, Error>) in
                        switch result {
                        case .success(let data):
                            resultText = "chat post: \(data)"
                        case .failure(let error):
                            resultText = "chat post error: \(error.localizedDescription)"
                        }
                    }
                }
                // /chat (GET)
                Button("Test /chat (GET)") {
                    let apiService = APIService()
                    apiService.get("http://127.0.0.1:8000/chat") { (result: Result<ChatHistoryResponseDTO, Error>) in
                        switch result {
                        case .success(let data):
                            resultText = "chat: \(data)"
                        case .failure(let error):
                            resultText = "chat error: \(error.localizedDescription)"
                        }
                    }
                }
                Text(resultText)
                    .padding()
            }
            .padding()
        }
    }
}

#Preview {
    TestAPIView()
}
