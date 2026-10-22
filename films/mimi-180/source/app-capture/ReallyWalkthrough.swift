import XCTest

/// Screen-recording walkthrough for the Mimi short 「180秒しゃべり続けたら、口癖がバレた」 (033); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of DescribeUITests.swift in a cached app checkout and records
/// the simulator, with PATCH=really-take.patch (capture-only: a habit-heavy synthetic transcript and its AI feedback).
/// QA fixture only (--qa-describe --qa-free-speech-v3 --qa-describe-really: silent synthetic take, no backend).
final class DescribeUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func reveal(_ id: String, _ app: XCUIApplication) {
        let b = app.buttons[id]
        _ = b.waitForExistence(timeout: 8)
        for _ in 0..<30 where !(b.exists && b.isHittable) { app.swipeUp() }
    }
    @MainActor func testReallyWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-describe", "--qa-free-speech-v3", "--qa-describe-really",
                               "--qa-route", "/practice/describe/cafe", "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        let record = app.buttons["describe.record"], retry = app.buttons["describe.retry"]
        for _ in 0..<16 where !record.exists && !retry.exists { hold(0.5) }
        if retry.exists && !record.exists { hold(0.5); retry.tap(); _ = record.waitForExistence(timeout: 5) }   // a saved result from an earlier run: もう一度話す
        if !record.waitForExistence(timeout: 2) {
            app.tabBars.buttons["練習"].tap()
            reveal("describe.open", app); app.buttons["describe.open"].tap()
            reveal("describe.photo.cafe", app); app.buttons["describe.photo.cafe"].tap()
            _ = record.waitForExistence(timeout: 8)
        }
        hold(3.0)                                                      // MARK 1 the photo, 最大 3:00 under the record button
        record.tap()
        _ = app.buttons["describe.replay"].waitForExistence(timeout: 5); hold(1.0)
        reveal("describe.submit", app); app.buttons["describe.submit"].tap()
        _ = app.buttons["describe.next"].waitForExistence(timeout: 10); hold(3.0)    // MARK 2 feedback top: scores
        for _ in 0..<7 { app.swipeUp(velocity: .slow); hold(2.2) }                    // MARK 3 transcript, vocabulary, corrections
        hold(1.0)
    }
}
