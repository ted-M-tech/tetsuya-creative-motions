import XCTest

/// Screen-recording walkthrough for the Mimi short 036「Mimiに1ヶ月見張られた結果」(mimi-month); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of MimiReportUITests.swift in a cached app checkout and records
/// the simulator. Five launches of Mimi's daily report (--qa-mimi), Japanese UI, QA fixtures only (no backend, no personal data).
/// month-days.patch (capture-only) adds --qa-mimi-day N: the report N-1 days from today with that day's example records.
/// Day 1 is the first report after the first completed lesson (--qa-completed --qa-first-report).
final class MimiReportUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func drag(_ app: XCUIApplication, from: Double, to: Double) {
        app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: from))
            .press(forDuration: 0.05, thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: to)),
                   withVelocity: 400, thenHoldForDuration: 0.3)
    }
    @MainActor func testMonthWalkthrough() {
        for day in [1, 7, 14, 21, 30] {
            let app = XCUIApplication()
            app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-mimi", "--qa-mimi-day", String(day)]
                + (day == 1 ? ["--qa-completed", "--qa-first-report"] : [])
                + ["--qa-route", "/voice?section=report", "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
            app.launch()
            _ = app.descendants(matching: .any)["mimi.report"].waitForExistence(timeout: 15)
            hold(3.5)
            drag(app, from: 0.7, to: 0.45); hold(2.5)
            app.terminate(); hold(1.0)
        }
    }
}
