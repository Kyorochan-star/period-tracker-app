//
//  APIService.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/06.
//
//  機能説明:
//  - ネットワークリクエストを行うクラスの定義
//  - データの取得と送信を行う
//  - 使用方法： 
//  - let apiService = APIService() インスタンスの作成
//  - apiService.get("http://127.0.0.1:8000/"){(result: Result<[User], Error>) in これはurlの指定・返り値の型の指定
//  -     case .success(let data):
//  -         print("Get Success: \(data)")
//  -     case .failure(let error):
//  -         print("Get Failed: \(error)")
//  -     }
//  - }

import Foundation 

class APIService{
    // JWTヘッダー自動付与
    private var token: String? { 
        UserDefaults.standard.string(forKey: "authToken")
    }
    private func makeRequest(
        url: URL, 
        method: String, 
        body: Data? = nil
    ) -> URLRequest { 
        var request = URLRequest(url: url)
        request.httpMethod = method 
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        if let token { 
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        request.httpBody = body 
        return request 
    }


    func get<T : Codable> (_ path: String, queryItems: [URLQueryItem]? = nil, completion: @escaping (Result<T, Error>) -> Void) {
        var urlComponents = URLComponents(string: APIConfig.baseURL + path)!
        urlComponents.queryItems = queryItems 
        let request = makeRequest(url: urlComponents.url!, method: "GET")
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            if let error = error {
                completion(.failure(error))
            } else if let data = data {
                do {
                    let jsonData = try JSONDecoder().decode(T.self, from: data)
                    completion(.success(jsonData))
                } catch {
                    completion(.failure(error))
                }
            }
        }
        task.resume()
    }
    
    func post<T: Codable, U: Codable>(_ path: String, data: T, completion: @escaping (Result<U, Error>) -> Void) {
        var urlComponents = URLComponents(string: APIConfig.baseURL + path)!
        let request = makeRequest(url: urlComponents.url!, method: "POST", body: try? JSONEncoder().encode(data))
        
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            if let error = error {
                completion(.failure(error))
            } else if let data = data {
                do {
                    let jsonData = try JSONDecoder().decode(U.self, from: data)
                    completion(.success(jsonData))
                } catch {
                    print("Decoding error: \(error)")
                    if let responseString = String(data: data, encoding: .utf8) {
                        print("Response data: \(responseString)")
                    }
                    completion(.failure(error))
                }
            }
        }
        task.resume()
    }

    func patch<T: Codable, U: Codable>(_ path: String, data: T, completion: @escaping (Result<U, Error>) -> Void) {
        var urlComponents = URLComponents(string: APIConfig.baseURL + path)!
        let request = makeRequest(url: urlComponents.url!, method: "PATCH", body: try? JSONEncoder().encode(data))
        
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            if let error = error {
                completion(.failure(error))
            } else if let data = data {
                do {
                    let jsonData = try JSONDecoder().decode(U.self, from: data)
                    completion(.success(jsonData))
                } catch {
                    completion(.failure(error))
                }
            }
        }
        task.resume()
    }

}

extension APIService {
    // GET
    func get<U: Decodable> (_ path: String,
                           queryItems: [URLQueryItem]? = nil) async throws -> U {

        var components = URLComponents(string: APIConfig.baseURL + path)!
        components.queryItems = queryItems
        let request = makeRequest(url: components.url!, method: "GET")

        let (data, response) = try await URLSession.shared.data(for: request)

//        try validate(response: response)              // ステータスコード判定
        return try JSONDecoder().decode(U.self, from: data)
    }

    // POST
    func post<T: Encodable, U: Decodable>(_ path: String, data: T) async throws -> U {

        var urlComponents = URLComponents(string: APIConfig.baseURL + path)!
        let request = makeRequest(url: urlComponents.url!, method: "POST", body: try? JSONEncoder().encode(data))

        let (data, response) = try await URLSession.shared.data(for: request)

//        try validate(response: response)
        return try JSONDecoder().decode(U.self, from: data)
    }

    // PATCH 
    func patch<T: Encodable, U: Decodable>(_ path: String, data: T) async throws -> U {

        var urlComponents = URLComponents(string: APIConfig.baseURL + path)!
        let request = makeRequest(url: urlComponents.url!, method: "PATCH", body: try? JSONEncoder().encode(data))

    let (data, response) = try await URLSession.shared.data(for: request)

//    try validate(response: response)
    return try JSONDecoder().decode(U.self, from: data)
    }

    // MARK: - application/x-www-form-urlencoded POST
    /// フォームエンコードでPOSTする。username/passwordなどの送信に使用。
    func postForm<U: Decodable>(_ path: String, form: [String: String]) async throws -> U {
        var urlComponents = URLComponents(string: APIConfig.baseURL + path)!

        // key=value&key2=value2 形式にエンコード
        let bodyString = form.map { key, value in
            let encodedKey = key.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? ""
            let encodedVal = value.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? ""
            return "\(encodedKey)=\(encodedVal)"
        }.joined(separator: "&")

        var request = makeRequest(url: urlComponents.url!, method: "POST", body: bodyString.data(using: .utf8))
        request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")

        let (data, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(U.self, from: data)
    }
}
