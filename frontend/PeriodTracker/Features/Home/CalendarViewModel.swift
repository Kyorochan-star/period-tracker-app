//  CalendarViewModel.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/12.
//

import Foundation
import Combine

private let periodDateFormatter: DateFormatter = {
    let df = DateFormatter()
    df.dateFormat = "yyyy-MM-dd"
    df.locale = Locale(identifier: "en_US_POSIX")
    df.timeZone = TimeZone(secondsFromGMT: 0)
    return df
}()

@MainActor
final class CalendarViewModel: ObservableObject {
    @Published var periods: [Period] = []
    @Published var error: String? = nil

    private let periodRepository: PeriodRepository
    init(periodRepository: PeriodRepository) {
        self.periodRepository = periodRepository
    }

    func fetchPeriods() async {
        do {
            periods = try await periodRepository.getPeriods()
        } catch {
            self.error = error.localizedDescription
        }
    }

    /// 指定日の 0:00 時点が、取得済みの Period のいずれかに含まれているかを判定
    func isDateInPeriod(_ date: Date) -> Bool {
        for period in periods {
            guard let start = periodDateFormatter.date(from: period.startdate) else { continue }
            // enddate が空の場合は開始日のみを対象とする
            let end = periodDateFormatter.date(from: period.enddate) ?? start
            if date >= start && date <= end {
                return true
            }
        }
        return false
    }

    private func validate() -> Bool {
        if periods.isEmpty {
            self.error = "周期情報がありません"
            return false
        }
        self.error = nil
        return true
    }
}