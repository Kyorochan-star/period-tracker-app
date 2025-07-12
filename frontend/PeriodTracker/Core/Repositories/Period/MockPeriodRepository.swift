//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/12.
//
//  機能説明:
//  - 周期リポジトリのモック実装（test.pyのエンドポイントを使用）
//  内容：
//  - 周期開始
//  - 周期終了
//  - カレンダー表示&6ヶ月分の表示

import Foundation 

final class MockPeriodRepository: PeriodRepository {
    private let api = APIService()

    // 周期開始 (POST /period)
    func startPeriod(_ dto: PeriodStartRequestDTO) async throws -> Period {
        let responseDTO: PeriodStartResponseDTO =
            try await api.post("http://127.0.0.1:8000/period", data: dto)
        return responseDTO.toDomain()
    }

    // 周期終了 (POST /period/{period_id})
    func endPeriod(_ dto: PeriodEndRequestDTO) async throws -> Period {
        // id をパスパラメータに埋め込む
        let endpoint = "http://127.0.0.1:8000/period/\(dto.id)"
        let responseDTO: PeriodEndResponseDTO =
            try await api.post(endpoint, data: dto)
        return responseDTO.toDomain()
    }

    // カレンダー表示&6ヶ月分取得 (GET /periods)
    func getPeriods() async throws -> [Period] {
        let responseDTO: [PeriodCalendarResponseDTO] =
            try await api.get("http://127.0.0.1:8000/periods")
        return responseDTO.map { $0.toDomain() }
    }
}