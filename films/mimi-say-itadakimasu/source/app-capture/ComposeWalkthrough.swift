import XCTest

/// Screen-recording walkthrough for the "How Do You Say It?" series (077 mimi-say-itadakimasu, episode 3); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of PracticeRefinementUITests.swift in a cached app checkout and
/// records the simulator. QA fixtures only (no backend, no personal data), Japanese UI. The phrase composer (フレーズを追加, Lanclo
/// origin/main 1088ae0b): type a Japanese phrase -> フレーズを作成 -> 表現を考えています… -> フレーズを確認 (the editable result with
/// its example) -> 保存 -> マイノートに保存したよ。 The composer's answer and the example come from the capture-only patch
/// (compose-result.patch), which returns the REAL answers Lanclo's server gave (process/compose-probe-*.jsonl, example-probe-*.jsonl).
final class PracticeRefinementUITests: XCTestCase {
    static let INPUT = ["食べる前の", "いただきます"]   // typed in chunks so the typing reads on screen

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
        button(app, "notes.group.add").tap(); hold(2.0)            // the empty composer (意味・表現を知りたい is selected)
        let input = app.textFields["notes.manual.text"]
        _ = input.waitForExistence(timeout: 10)
        input.tap(); hold(1.0)
        for chunk in Self.INPUT { input.typeText(chunk); hold(0.6) }
        hold(1.5)
        button(app, "notes.manual.create").tap()                    // フレーズを作成 (the patch keeps 表現を考えています… for 2 s)
        _ = app.textFields["notes.manual.term"].waitForExistence(timeout: 15)
        hold(5.0)                                                   // フレーズを確認: the result and its example
        button(app, "notes.manual.save").tap(); hold(4.0)           // マイノートに保存したよ。
        button(app, "notes.manual.done").tap(); hold(2.0)
        app.terminate()
    }
}
