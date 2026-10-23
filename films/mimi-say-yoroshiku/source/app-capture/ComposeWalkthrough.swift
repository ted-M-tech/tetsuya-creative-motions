import XCTest

/// Screen-recording walkthrough for the "How Do You Say It?" series (063 mimi-say-yoroshiku, episode 1); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of PracticeRefinementUITests.swift in a cached app checkout and
/// records the simulator. QA fixtures only (no backend, no personal data), Japanese UI. The phrase composer (Add phrase):
/// type a Japanese phrase -> フレーズを作成 -> the editable result -> Save -> the saved phrase in the list.
/// The composer's answer comes from the capture-only patch (compose-result.patch), which returns the REAL answer that Lanclo's
/// server composer gave for this input (process/compose-probe-*.jsonl). Series: change INPUT and the patch, nothing else.
final class PracticeRefinementUITests: XCTestCase {
    static let INPUT = ["新しい職場で", "よろしく", "お願いします"]   // typed in chunks so the typing reads on screen

    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func button(_ app: XCUIApplication, _ id: String) -> XCUIElement {
        let b = app.buttons[id]
        _ = b.waitForExistence(timeout: 10)
        for _ in 0..<6 where !b.isHittable { app.swipeUp() }
        return b
    }
    @MainActor func testComposeWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-notes", "--qa-note-detail", "--qa-phrase-compose",
                               "--qa-route", "/vocabulary", "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        button(app, "notes.group.all").tap(); hold(1.5)
        button(app, "notes.group.add").tap(); hold(2.0)            // the empty composer: placeholder 覚えたい表現、または言いたいこと
        let input = app.textFields["notes.manual.text"]
        _ = input.waitForExistence(timeout: 10)
        input.tap(); hold(1.0)
        for chunk in Self.INPUT { input.typeText(chunk); hold(0.6) }
        hold(1.5)
        button(app, "notes.manual.create").tap()                    // フレーズを作成 (the patch keeps 生成を中止 visible for 2 s)
        _ = app.textFields["notes.manual.term"].waitForExistence(timeout: 15)
        hold(4.0)                                                   // the editable result
        button(app, "notes.manual.save").tap(); hold(4.0)           // saved: back in the list
        app.terminate()
    }
}
