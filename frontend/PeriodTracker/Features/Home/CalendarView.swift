//
//  CalendarView.swift
//  PeriodTracker
//
//  Created by 藤瀬太翼 on 2025/07/04.
//
//  機能説明:
//  - 月間カレンダー表示
//  - 月間サマリー（生理期間、平均周期）

import SwiftUI

struct CalendarView: View {
    @StateObject var viewModel: CalendarViewModel

    private let calendar = Calendar.current
    private let days = ["日", "月", "火", "水", "木", "金", "土"]

    @State private var selectedDate = Date()

    private var monthDates: [Date] {
        guard let monthInterval = calendar.dateInterval(of: .month, for: selectedDate) else { return [] }
        var dates = [Date]()
        let start = calendar.date(from: calendar.dateComponents([.year, .month], from: selectedDate))!
        for offset in 0..<35 {
            if let date = calendar.date(byAdding: .day, value: offset - calendar.component(.weekday, from: start) + 1, to: start) {
                dates.append(date)
            }
        }
        return dates
    }

    private var headerTitle: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy年 M月"
        return formatter.string(from: selectedDate)
    }

    var body: some View {
        VStack {
            HStack {
                Text("カレンダー")
                    .font(.title2)
                    .bold()
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.top, 18)
                
                Button(action: {
                    if let newDate = calendar.date(byAdding: .month, value: -1, to: selectedDate) {
                        selectedDate = newDate
                    }
                }) {
                    Image(systemName: "chevron.left")
                }
                Spacer()
                Text(headerTitle)
                    .font(.title2)
                    .bold()
                Spacer()
                Button(action: {
                    if let newDate = calendar.date(byAdding: .month, value: 1, to: selectedDate) {
                        selectedDate = newDate
                    }
                }) {
                    Image(systemName: "chevron.right")
                }
            }
            .padding()
            .padding(.horizontal)
            .background(Color.white)
            
            // Top: Calendar Grid
            VStack {
                LazyVGrid(columns: Array(repeating: .init(.flexible()), count: 7), spacing: 8) {
                    ForEach(days, id: \.self) { day in
                        Text(day)
                            .font(.caption)
                            .frame(maxWidth: .infinity)
                    }
                    
                    ForEach(monthDates, id: \.self) { date in
                        CalendarDateCell(date: date, isToday: calendar.isDateInToday(date), inPeriod: viewModel.isDateInPeriod(date))
                    }
                }
                .padding()
            }
            .padding(.bottom)
            .padding(.horizontal)
            .task {
                await viewModel.fetchPeriods()
            }
        }
            .ignoresSafeArea(edges: .top)
            .background(Color.white)
            .padding(.horizontal)

        VStack {
            // Bottom: 直近6ヶ月分の生理記録
            VStack(alignment: .leading, spacing: 16) {
                Text("直近6ヶ月分の生理記録")
                    .font(.title3)
                    .bold()
                    .background(Color.white)
                    .frame(maxWidth: .infinity, alignment: .leading)
                
                ForEach(viewModel.periods, id: \.id) { period in
                    VStack(alignment: .leading) {
                        Text("\(period.startdate) ~ \(period.enddate)")
                            .font(.title3)
                            .fontWeight(.bold)
                            .foregroundColor(Color.red.opacity(0.8))
                    }
                }
            }
        }
        .padding()
        .frame(maxWidth: 350)
        .ignoresSafeArea(edges: .top)
        .background(
            Color.white
                .cornerRadius(15)
        )
        .padding(.horizontal)
    }
}

#Preview {
    CalendarView(viewModel: CalendarViewModel(periodRepository: NetworkPeriodRepository()))
}

private struct CalendarDateCell: View {
    let date: Date
    let isToday: Bool
    let inPeriod: Bool

    var body: some View {
        let day = Calendar.current.component(.day, from: date)
        Text("\(day)")
            .frame(maxWidth: .infinity, minHeight: 40)
            .background(
                isToday ? Color.blue : (inPeriod ? Color.red : Color.clear)
            )
            .foregroundColor(
                isToday ? .white : (inPeriod ? .white : .primary)
            )
            .clipShape(Circle())
    }
}

private struct PeriodSummaryView: View {
    let period: Period
    let cycle: Int?

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("\(period.startdate) ~ \(period.enddate)")
                .font(.headline)
                .foregroundColor(Color.red.opacity(0.8))
            if let cycle = cycle {
                Text("周期：\(cycle)日")
                    .font(.subheadline)
            }
        }
        .padding(8)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color.red.opacity(0.1))
        .cornerRadius(8)
    }
}
