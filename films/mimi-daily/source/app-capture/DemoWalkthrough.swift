import XCTest

/// Screen-recording walkthrough for the Mimi short 「積読」 (daily lesson); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of DescribeUITests.swift in a cached app checkout,
/// runs it and records the simulator. It uses openDailyLesson() from HomeTestSupport.swift. Fixture data only.
final class DescribeUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor func testDailyWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        _ = app.waitForHome(timeout: 15); hold(2.5)            // home: today's tasks
        _ = app.openDailyLesson(); hold(2.5)                    // the first sentence
        let model = app.buttons["lesson.model"]
        if model.exists && model.isHittable { model.tap(); hold(3.0) }   // her own voice, native
        let record = app.buttons["lesson.record"]
        if record.isHittable { record.tap(); hold(3.0) }        // records (fixture)
        let scores = app.staticTexts["feedback.scores"]
        for _ in 0..<6 where !scores.isHittable { app.swipeUp(velocity: .slow); hold(0.8) }
        hold(2.5)                                               // score and what to fix
        for _ in 0..<2 { app.swipeUp(velocity: .slow); hold(1.5) }
        let next = app.buttons["lesson.next"]
        if next.isHittable { next.tap(); hold(3.0) }            // the next sentence
    }
}
