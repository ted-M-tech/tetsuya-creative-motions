import XCTest

/// Screen-recording walkthrough for the Mimi short 029「3日坊主の私が、1ヶ月続いた理由」(mimi-quitter); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of MimiReportUITests.swift in a cached app checkout and records
/// the simulator. Three launches, QA fixtures only (no backend, no personal data), Japanese UI:
/// ① the daily lesson the Daily lesson widget opens (lanclo://practice/daily), ② Mimi's daily report (--qa-mimi),
/// ③ Home with a 30-day streak (--qa-widgets, 30 study days from month-streak.patch, capture-only).
final class MimiReportUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func launch(_ extra: [String]) -> XCUIApplication {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures"] + extra + ["-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        return app
    }
    @MainActor private func drag(_ app: XCUIApplication, from: Double, to: Double) {
        app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: from))
            .press(forDuration: 0.05, thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: to)),
                   withVelocity: 500, thenHoldForDuration: 0.3)
    }
    @MainActor func testQuitterWalkthrough() {
        // ① Daily lesson overview (the widget's link)
        var app = launch(["--qa-route", "/practice/daily"])
        _ = app.buttons["lesson.start"].waitForExistence(timeout: 15)
        hold(3.5)
        app.buttons["lesson.start"].tap()
        _ = app.buttons["lesson.record"].waitForExistence(timeout: 10)
        hold(3.0)
        app.terminate(); hold(1.0)

        // ② Mimi's daily report
        app = launch(["--qa-mimi", "--qa-route", "/voice?section=report"])
        _ = app.descendants(matching: .any)["mimi.report"].waitForExistence(timeout: 15)
        hold(3.5)
        for _ in 0..<2 { drag(app, from: 0.75, to: 0.45); hold(2.2) }
        app.terminate(); hold(1.0)

        // ③ Home: the streak
        app = launch(["--qa-widgets"])
        let skip = app.buttons["practice.guide.skip"]
        if skip.waitForExistence(timeout: 3) { skip.tap() }
        _ = app.descendants(matching: .any)["home.streak"].firstMatch.waitForExistence(timeout: 15)
        hold(4.0)
        app.tabBars.buttons.element(boundBy: 0).tap(); hold(1.0)
        app = launch(["--qa-widgets", "--qa-route", "/progress"])
        hold(4.0)
        app.terminate()
    }
}
