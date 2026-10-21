import XCTest

/// Screen-recording walkthrough for the IELTS one-month short; not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of IELTSSpeakingUITests.swift in a cached app checkout and
/// records the simulator. QA fixture only (--qa-ielts: silent synthetic recordings, synthetic feedback and estimate).
final class IELTSSpeakingUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func reveal(_ e: XCUIElement, _ app: XCUIApplication) {
        _ = e.waitForExistence(timeout: 8)
        for _ in 0..<8 where !e.isHittable { app.swipeUp(velocity: .slow) }
    }
    @MainActor private func tap(_ e: XCUIElement, _ app: XCUIApplication) { reveal(e, app); e.tap() }
    @MainActor func testMockWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-ielts", "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        tap(app.tabBars.buttons["練習"], app)
        let part = app.segmentedControls["ielts.part"]
        if !part.waitForExistence(timeout: 4) {                           // the Practice list: スピーキング試験対策 at the bottom
            hold(1.0)
            tap(app.buttons["ielts.open"], app)
            _ = part.waitForExistence(timeout: 10)
        }
        hold(1.5)                                                         // the catalogue
        part.buttons.element(boundBy: 3).tap()                            // 模擬試験
        hold(2.5)                                                         // Mimi: 3つのパートを順に進めます
        tap(app.buttons["ielts.mock.start"], app)
        for index in 0..<9 {
            let prompt = app.staticTexts["ielts.prompt"]
            _ = prompt.waitForExistence(timeout: 8)
            hold(1.8)                                                     // the question
            if index == 6 {                                               // Part 2: one minute to prepare
                tap(app.buttons["ielts.prepare"], app)
                hold(2.0)
            }
            tap(app.buttons["ielts.record"], app)
            hold(2.2)                                                     // recording
            tap(app.buttons["ielts.stop"], app)
            hold(1.0)
            tap(app.buttons["ielts.submit"], app)
            hold(0.4)
        }
        hold(2.5)                                                         // 最後まで話せましたね
        tap(app.buttons["ielts.mock.assess"], app)
        _ = app.buttons["ielts.mock.result.work-study"].waitForExistence(timeout: 20)
        _ = app.staticTexts["ielts.mock.band"].waitForExistence(timeout: 10)
        hold(3.0)                                                         // estimate and the answers
        app.swipeUp(velocity: .slow); hold(2.0)
        app.swipeDown(velocity: .slow); hold(1.0)
        tap(app.buttons["ielts.mock.result.work-study"], app)           // the first answer's feedback
        hold(3.0)
        for _ in 0..<4 { app.swipeUp(velocity: .slow); hold(2.0) }
        hold(1.0)
    }
}
