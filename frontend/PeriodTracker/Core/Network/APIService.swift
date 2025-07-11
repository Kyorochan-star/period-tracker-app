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
    func get<T : Codable> (_ url: String, queryItems: [URLQueryItem]? = nil, completion: @escaping (Result<T, Error>) -> Void) {
        var urlComponents = URLComponents(string: url)!
        urlComponents.queryItems = queryItems 
        let request = URLRequest(url: urlComponents.url!)
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
    
    func post<T: Codable, U: Codable>(_ url: String, data: T, completion: @escaping (Result<U, Error>) -> Void) {
        var request = URLRequest(url: URL(string: url)!)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        let encoder = JSONEncoder()
        let jsonData = try? encoder.encode(data)
        request.httpBody = jsonData
        
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

    func patch<T: Codable, U: Codable>(_ url: String, data: T, completion: @escaping (Result<U, Error>) -> Void) {
        var request = URLRequest(url: URL(string: url)!)
        request.httpMethod = "PATCH"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        let encoder = JSONEncoder()
        let jsonData = try? encoder.encode(data)
        request.httpBody = jsonData
        
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
