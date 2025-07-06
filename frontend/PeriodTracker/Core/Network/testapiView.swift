//
//  testapi.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/06.
//

import SwiftUI

struct testapi: View {
    @State private var getResult = ""
    @State private var postResult = ""
    var body: some View {
        VStack {
            Button("Test get") {
                let apiService = APIService()
                apiService.get("http://127.0.0.1:8000/"){(result: Result<User, Error>) in
                    switch result {
                    case .success(let data):
                        getResult = "Get Success: \(data)"
                    case .failure(let error):
                        getResult = "Get Failed: \(error)"
                    }
                }
            }
            Button("Test post") {
                let user = User(id: 1, name: "test")
                let apiService = APIService()
                apiService.post("http://127.0.0.1:8000/", data: user){(result: Result<String, Error>) in
                    switch result {
                    case .success(let data):
                        postResult = "Post Success: \(data)"
                    case .failure(let error):
                        postResult = "Post Failed: \(error)"
                    }
                }
            }
            Text(getResult)
            Text(postResult)
        }
    }
}

#Preview {
    testapi()
}
