import Foundation 

protocol PeriodRepository {
    // 直近1件の周期を取得
    func latestPeriod() async throws -> Period?
    // 周期開始
    func startPeriod(_ request: PeriodStartRequestDTO) async throws -> Period 
    // 周期終了
    func endPeriod(_ request: PeriodEndRequestDTO) async throws -> Period 
    // カレンダー表示&6ヶ月分の表示
    func getPeriods() async throws -> [Period] 
}