import XCTest

/// Screen-recording walkthrough for the Mimi short 「3分、話しつづけて」 (free speech: Describe a photo); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of DescribeUITests.swift in a cached app checkout and records
/// the simulator. QA fixture only (--qa-describe --qa-free-speech-v3: silent synthetic take, synthetic AI feedback, no backend).
final class DescribeUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func reveal(_ id: String, _ app: XCUIApplication) {
        let b = app.buttons[id]
        _ = b.waitForExistence(timeout: 8)
        for _ in 0..<30 where !(b.exists && b.isHittable) { app.swipeUp() }
    }
    @MainActor func testFreeSpeechWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-describe", "--qa-free-speech-v3",
                               "--qa-route", "/practice/describe/cafe", "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        let record = app.buttons["describe.record"]
        if !record.waitForExistence(timeout: 8) {                      // no deep link: Practice tab -> 写真描写 -> cafe
            app.tabBars.buttons["練習"].tap()
            reveal("describe.open", app); app.buttons["describe.open"].tap()
            reveal("describe.photo.cafe", app); app.buttons["describe.photo.cafe"].tap()
            _ = record.waitForExistence(timeout: 8)
        }
        hold(3.0)                                                      // MARK 1 the photo, 最大 3:00 under the record button
        record.tap()
        _ = app.buttons["describe.replay"].waitForExistence(timeout: 5); hold(1.0)   // MARK 2 the take (fixture)
        reveal("describe.submit", app); app.buttons["describe.submit"].tap()
        _ = app.buttons["describe.next"].waitForExistence(timeout: 10); hold(3.0)    // MARK 3 feedback top: scores
        for _ in 0..<5 { app.swipeUp(velocity: .slow); hold(2.0) }                    // MARK 4 transcript, corrections, model answer
        hold(1.0)
    }
}
