import XCTest

/// Screen-recording walkthrough for the multilingual own-voice short (films/mimi-multilang); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of MeaningPracticeUITests.swift in a cached app checkout and
/// records the simulator. Fixture data only; voice-stub.patch (capture-only) answers the language switch with a silent WAV,
/// because the fixture has no voice provider. AI Voice screen (/voice, 将来の発音 with its passage): switch the AI-voice language (🌐 menu)
/// (Français, 한국어) and press 試聴 after each switch. The audition language is view state only (not saved).
/// 中文（普通话）was tried first: its long name pushes the menu into the toolbar's overflow, so it was left out.
final class MeaningPracticeUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func pick(_ app: XCUIApplication, _ name: String) {
        let menu = app.buttons["voice.language"]
        guard menu.waitForExistence(timeout: 5) else { return }
        menu.tap(); hold(1.2)
        let item = app.buttons[name].firstMatch
        for _ in 0..<4 where item.exists && !item.isHittable { app.swipeUp(velocity: .slow) }
        if item.waitForExistence(timeout: 3) { item.tap() }
        hold(2.2)                                                         // 読み込み中…, then the passage in the new language
    }
    @MainActor private func preview(_ app: XCUIApplication) {
        let play = app.buttons["試聴"].firstMatch
        if play.waitForExistence(timeout: 3) && play.isHittable { play.tap() }
        hold(3.5)
    }
    @MainActor func testMultilangWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-film-voice-stub", "--qa-route", "/voice",
                               "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP", "-UIPreferredContentSizeCategoryName", "UICTContentSizeCategoryL"]
        app.launch()
        XCTAssertTrue(app.buttons["voice.language"].waitForExistence(timeout: 10))
        hold(2.5)                                                         // 将来の発音 with the English passage
        pick(app, "Français"); preview(app)
        pick(app, "한국어"); preview(app)
        hold(1.0)
    }
}
