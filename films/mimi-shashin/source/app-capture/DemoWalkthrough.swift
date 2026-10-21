import XCTest

/// Screen-recording walkthrough for the Mimi short 「写真で英語」 (not a test of behaviour).
/// capture.sh puts this file in place of DescribeUITests.swift in a throwaway checkout, runs it,
/// and records the simulator. Pauses give the edit time to cut; fixture data only.
final class DescribeUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func scrollTo(_ app: XCUIApplication, _ id: String) {
        let b = app.buttons[id]
        for _ in 0..<30 where !(b.exists && b.isHittable) { app.swipeUp() }
    }
    @MainActor func testWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--reset-onboarding", "--qa-describe", "--qa-free-speech-v3",
                               "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        hold(2.0)                                    // MARK 1 home
        app.tabBars.buttons["練習"].tap(); hold(1.5) // MARK 2 practice tab
        let entry = app.buttons["describe.open"]
        _ = entry.waitForExistence(timeout: 10)
        for _ in 0..<8 where !entry.isHittable { app.swipeUp() }
        entry.tap(); hold(2.0)                       // MARK 3 photo list
        scrollTo(app, "describe.photo.cafe")
        app.buttons["describe.photo.cafe"].tap(); hold(2.5)   // MARK 4 the photo
        app.buttons["describe.record"].tap()
        _ = app.buttons["describe.replay"].waitForExistence(timeout: 5); hold(1.5)   // MARK 5 recorded
        scrollTo(app, "describe.submit")
        app.buttons["describe.submit"].tap()
        _ = app.buttons["describe.next"].waitForExistence(timeout: 10); hold(2.5)    // MARK 6 feedback top
        for _ in 0..<3 { app.swipeUp(velocity: .slow); hold(1.6) }                    // MARK 7 corrections, model answer
        hold(1.5)
    }
}
