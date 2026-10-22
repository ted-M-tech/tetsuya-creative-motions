import XCTest

/// Screen-recording walkthrough for the Mimi short "I Stopped Shadowing Native Speakers" (mimi-no-shadowing); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of DescribeUITests.swift in a cached app checkout and records the
/// simulator. Uses openDailyLesson() from HomeTestSupport.swift. Fixture data only (no backend, no personal data).
final class DescribeUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor func testModelWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        _ = app.waitForHome(timeout: 15); hold(2.0)
        _ = app.openDailyLesson(); hold(2.5)                    // today's first sentence
        let model = app.buttons["lesson.model"]
        if model.exists && model.isHittable { model.tap(); hold(3.5) }   // 自分のAIボイスのお手本
        if model.exists && model.isHittable { model.tap(); hold(0.6) }   // stop
        if model.exists && model.isHittable { model.tap(); hold(3.5) }   // and again
        let record = app.buttons["lesson.record"]
        if record.isHittable { record.tap(); hold(3.5) }        // records along (fixture)
        hold(2.0)
    }
}
