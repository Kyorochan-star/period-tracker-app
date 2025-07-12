import Foundation
import Combine

@MainActor
final class HomeViewModel: ObservableObject {

    @Published var showModal = false 
    @Published var isStartModal = true 
    @Published var nextPredictionDate: String = ""
    @Published var error: String? = nil

    @Published var showModifyModal = false

    private let periodRepository: PeriodRepository

    init(periodRepository: PeriodRepository) {
        self.periodRepository = periodRepository
    }

    func loadModalState() async { 
        do { 
            guard let latestPeriod = try await periodRepository.latestPeriod() else {
                // 周期がない場合は開始モーダル
                setStartModal()
                return
            }
            // enddateが空なら終了モーダル、それ以外は開始モーダル
            if latestPeriod.enddate.isEmpty {
                setEndModal()
            } else {
                setStartModal()
            }
        } catch {
            self.error = error.localizedDescription
        }
    }

    func startPeriod(date: Date) async {
        let dto = PeriodStartRequestDTO(startdate: dateToString(date))
        do {
            _ = try await periodRepository.startPeriod(dto)
            // 周期開始後は終了モーダルに
            setEndModal()
        } catch {
            self.error = error.localizedDescription
        }
    }

    func endPeriod(periodId: Int, userId: Int, date: Date) async {
        let dto = PeriodEndRequestDTO(id: periodId, userid: userId, enddate: dateToString(date))
        do {
            _ = try await periodRepository.endPeriod(dto)
            // 周期終了後は開始モーダルに
            setStartModal()
        } catch {
            self.error = error.localizedDescription
        }
    }

    func dismissModals() {
        dismissModal()
    }

    // 開始モーダル
    private func setStartModal() { 
        isStartModal = true 
        showModal = true 
    }

    // 終了モーダル
    private func setEndModal() { 
        isStartModal = false 
        showModal = true 
    }

    // モーダルを閉じる
    private func dismissModal() { 
        showModal = false 
    }

    // 日付を文字列に変換
    private func dateToString(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        formatter.timeZone = .current
        return formatter.string(from: date)
    }

}