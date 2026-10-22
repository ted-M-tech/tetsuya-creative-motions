import XCTest

/// Screen-recording walkthrough for the Mimi short 「AIと会話、何話そう…」 (031); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of SituationUITests.swift in a cached app checkout and records
/// the simulator. QA visual fixtures only (no backend, no personal data): Home with today's lesson, the Practice menu,
/// the roleplay scenes, the photo gallery, the debate topics, then today's lesson.
final class SituationUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func drag(_ app: XCUIApplication, from: Double, to: Double, hold seconds: Double = 0.1) {
        app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: from))
            .press(forDuration: 0.05, thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: to)),
                   withVelocity: 600, thenHoldForDuration: seconds)
    }
    @MainActor private func back(_ app: XCUIApplication) {
        let b = app.navigationBars.buttons.element(boundBy: 0)
        if b.exists && b.isHittable { b.tap() }
        hold(1.0)
    }
    @MainActor private func open(_ id: String, _ app: XCUIApplication) {
        let e = app.buttons[id]
        _ = e.waitForExistence(timeout: 8)
        for _ in 0..<8 where !e.isHittable { app.swipeUp() }
        hold(0.6); e.tap()
    }
    @MainActor func testTopicsWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-situations", "--qa-roleplay-language", "en",
                               "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        _ = app.waitForHome(timeout: 15); hold(3.0)                    // MARK 1 Home: today's lesson is ready
        app.tabBars.buttons["練習"].tap(); hold(2.5)                    // MARK 2 the Practice menu
        open("roleplay.open", app)
        _ = app.buttons["roleplay.category.cafe"].waitForExistence(timeout: 5); hold(2.0)   // MARK 3 roleplay scenes
        drag(app, from: 0.75, to: 0.3, hold: 0.3); hold(1.5)
        back(app)
        open("describe.open", app); hold(2.5)                          // MARK 4 photos to describe
        back(app)
        open("debate.open", app); hold(2.5)                            // MARK 5 debate topics
        drag(app, from: 0.75, to: 0.3, hold: 0.3); hold(1.5)
        back(app)
        app.tabBars.buttons["ホーム"].tap(); hold(1.0)
        _ = app.openDailyLesson(); hold(2.5)                           // MARK 6 the first sentence of today's lesson
        let model = app.buttons["lesson.model"]
        if model.exists && model.isHittable { model.tap(); hold(3.0) }
        hold(1.0)
    }
}
