import XCTest

/// Screen-recording walkthrough for the Mimi short "The R Came Back"; not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of LessonLevelUITests.swift in a cached app checkout and
/// records the simulator, with PATCH=recheck-row.patch (the fifth sentence is an /ɹ/ re-check). Fixture data only.
final class LessonLevelUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor func testRecheckWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-route", "/practice/daily", "--qa-lesson-overview",
                               "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        XCTAssertTrue(app.buttons["lesson.start"].waitForExistence(timeout: 20), app.debugDescription)
        hold(4.0)                                               // the overview: Mimi noticed, the five sentences and their chips
        let row = app.descendants(matching: .any)["lesson.preview.4"]
        if row.exists && !row.isHittable { app.swipeUp(velocity: .slow); hold(1.0) }
        hold(4.0)                                               // the /ɹ/ (right) · 再確認 row
    }
}
