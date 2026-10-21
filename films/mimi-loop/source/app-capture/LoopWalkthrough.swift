import XCTest

/// Screen-recording walkthrough for the Mimi short 「ひとつのループ」 (mimi-loop); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of MimiReportUITests.swift in a cached app checkout and records
/// the simulator. Five launches, QA fixtures only (no backend, no personal data), Japanese UI:
/// Mimi AI report (--qa-mimi), English journal review (--qa-journal-review), café roleplay (--qa-situations),
/// daily lesson overview (--qa-lesson-overview), pronunciation trend (--qa-pronunciation-trend).
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
    @MainActor private func skipGuide(_ app: XCUIApplication) {
        let skip = app.buttons["practice.guide.skip"]
        if skip.waitForExistence(timeout: 2) { skip.tap() }
    }
    @MainActor func testLoopWalkthrough() {
        // ④ Mimi AI report: habits ranking, then the details (phrasing + "ほかの言い方", pronunciation)
        var app = launch(["--qa-mimi", "--qa-route", "/voice?section=report"])
        _ = app.descendants(matching: .any)["mimi.report"].waitForExistence(timeout: 15)
        hold(3.0)
        for _ in 0..<5 { drag(app, from: 0.75, to: 0.4); hold(2.2) }
        app.terminate(); hold(1.0)

        // ③ English journal: what you said, and the native version
        app = launch(["--qa-journal", "--qa-journal-review"])
        skipGuide(app)
        let journal = app.buttons["home.tasks.journal"]
        if journal.waitForExistence(timeout: 10) { hold(1.5); journal.tap() }
        _ = app.buttons["journal.done"].waitForExistence(timeout: 8)
        hold(3.0)
        for _ in 0..<4 { drag(app, from: 0.75, to: 0.4); hold(2.2) }
        app.terminate(); hold(1.0)

        // ③ Roleplay: the partner's line and a reply
        app = launch(["--qa-situations", "--qa-roleplay-language", "en"])
        app.tabBars.buttons["練習"].tap()
        let entry = app.buttons["roleplay.open"]
        _ = entry.waitForExistence(timeout: 10)
        for _ in 0..<8 where !entry.isHittable { app.swipeUp() }
        entry.tap()
        let cafe = app.buttons["roleplay.category.cafe"]
        _ = cafe.waitForExistence(timeout: 5)
        for _ in 0..<8 where !cafe.isHittable { app.swipeUp() }
        cafe.tap()
        let task = app.buttons["roleplay.scene.roleplay-en-food"]
        if task.waitForExistence(timeout: 5) { task.tap() }
        let hint = app.buttons["situation.hint"]
        _ = hint.waitForExistence(timeout: 15)
        hold(2.5)
        if hint.isHittable { hint.tap() }
        hold(2.5)
        let record = app.buttons["situation.record"]
        if record.isHittable { record.tap() }
        _ = app.staticTexts["situation.complete"].waitForExistence(timeout: 15)
        hold(3.0)
        app.terminate(); hold(1.0)

        // ⑤ Daily lesson overview: "Mimiが気づいた" and the reason chips
        app = launch(["--qa-route", "/practice/daily", "--qa-lesson-overview"])
        _ = app.buttons["lesson.start"].waitForExistence(timeout: 15)
        hold(3.5)
        drag(app, from: 0.75, to: 0.45); hold(2.5)
        app.terminate(); hold(1.0)

        // ⑥ Pronunciation trend on the progress screen
        app = launch(["--qa-pronunciation-trend", "--qa-route", "/progress"])
        _ = app.tabBars.firstMatch.waitForExistence(timeout: 10)
        hold(2.5)
        let legend = app.buttons["pronunciation.legend.4"]
        for _ in 0..<12 where !legend.isHittable { drag(app, from: 0.7, to: 0.5); hold(0.6) }
        hold(3.0)
        let first = app.buttons["pronunciation.legend.0"]
        if first.isHittable { first.tap() }
        hold(3.0)
        app.terminate()
    }
}
