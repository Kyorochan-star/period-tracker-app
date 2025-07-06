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
            Text("カレンダー")
                .font(.title2)
                .bold()
                .frame(maxWidth: 350,alignment: .leading)
            // Month and Year Header with Controls
            HStack {
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

            // Top: Calendar Grid
            VStack {
                LazyVGrid(columns: Array(repeating: .init(.flexible()), count: 7), spacing: 8) {
                    ForEach(days, id: \.self) { day in
                        Text(day)
                            .font(.caption)
                            .frame(maxWidth: .infinity)
                    }

                    ForEach(monthDates, id: \.self) { date in
                        let isToday = calendar.isDateInToday(date)
                        let day = calendar.component(.day, from: date)
                        Text("\(day)")
                            .frame(maxWidth: .infinity, minHeight: 40)
                            .background(isToday ? Color.blue : Color.clear)
                            .foregroundColor(isToday ? .white : .primary)
                            .clipShape(Circle())
                    }
                }
                .padding()
            }
            .padding(.bottom)
            .padding(.horizontal)

            // Bottom: Summary Card
            VStack(alignment: .leading, spacing: 16) {
                Text("月間サマリー")
                    .font(.title)
                    .bold()
                HStack {
                    VStack(alignment: .leading) {
                        Text("生理期間")
                            .font(.title3)
                        Text("5日")
                            .font(.title)
                    }
                    .padding()
                    .frame(maxWidth: 150, alignment: .leading)
                    .background(
                        RoundedRectangle(cornerRadius: 8)
                            .fill(Color.red.opacity(0.2))
                    )

                    VStack(alignment: .leading) {
                        Text("平均周期")
                            .font(.title3)
                        Text("28日")
                            .font(.title)
                    }
                    .padding()
                    .frame(maxWidth: 150, alignment: .leading)
                    .background(
                        RoundedRectangle(cornerRadius: 8)
                            .fill(Color.blue.opacity(0.2))
                    )
                }
            }
            .padding()
            .frame(maxWidth: 350, maxHeight: 200)
            .background(Color(UIColor.secondarySystemBackground))
            .cornerRadius(12)
            .padding(.top, 0)
        }
        .ignoresSafeArea(edges: .top)
    }
}

#Preview {
    CalendarView()
}
