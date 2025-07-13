//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/12.
//
//  機能説明:
//  - 周期リポジトリのネットワーク実装（本番環境のAPIを使用）
//  内容：
//  - 周期開始
//  - 周期終了
//  - カレンダー表示&6ヶ月分の表示

import Foundation 

final class NetworkPeriodRepository: PeriodRepository {
    private let api = APIService()

    // 直近1件の周期を取得 (GET /periods/latest)
    func latestPeriod() async throws -> Period? {
        let responseDTO: [PeriodCalendarResponseDTO] =
            try await api.get("/periods?limit=1&order_by=created_at&order_direction=desc")
        // 1 件のみ返る想定
        return responseDTO.first?.toDomain()
    }

    // 周期開始 (POST /period)
    func startPeriod(_ dto: PeriodStartRequestDTO) async throws -> Period {
        let responseDTO: PeriodStartResponseDTO =
            try await api.post("/periods", data: dto)
        return responseDTO.toDomain()
    }

    // 周期終了 (POST /period/{period_id})
    func endPeriod(_ dto: PeriodEndRequestDTO) async throws -> Period {
        // id をパスパラメータに埋め込む
        let endpoint = "/periods/\(dto.id)"
        let responseDTO: PeriodEndResponseDTO =
            try await api.post(endpoint, data: dto)
        return responseDTO.toDomain()
    }

    // カレンダー表示&6ヶ月分取得 (GET /periods)
    func getPeriods() async throws -> [Period] {
        let responseDTO: [PeriodCalendarResponseDTO] =
            try await api.get("/periods")
        return responseDTO.map { $0.toDomain() }
    }
}
