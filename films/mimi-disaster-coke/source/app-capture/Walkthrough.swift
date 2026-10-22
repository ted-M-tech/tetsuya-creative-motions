import XCTest

/// Screen-recording walkthrough for the Mimi short "Pronunciation Disasters - Coke / C*ck"; not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of DescribeUITests.swift in a cached app checkout and
/// records the simulator, with PATCH=coke-lesson.patch (the first daily sentence is "One Coke, please."). Fixture data only.
final class DescribeUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor func testWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        _ = app.waitForHome(timeout: 15); hold(2.0)            // home: today's tasks
        _ = app.openDailyLesson(); hold(3.0)                    // "One Coke, please."
        let model = app.buttons["lesson.model"]
        if model.exists && model.isHittable { model.tap(); hold(3.0) }   // the model, in your own voice
        let record = app.buttons["lesson.record"]
        if record.isHittable { record.tap(); hold(3.0) }        // records (fixture)
        let scores = app.staticTexts["feedback.scores"]
        for _ in 0..<6 where !scores.isHittable { app.swipeUp(velocity: .slow); hold(0.8) }
        hold(2.5)                                               // the score
        for _ in 0..<3 { app.swipeUp(velocity: .slow); hold(2.0) }   // the sound to fix: "Coke"
        hold(2.0)
    }
}
