import XCTest

/// Screen-recording walkthrough for the voice tuning short (films/mimi-tuning); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of EnrollmentRecoveryUITests.swift in a cached app checkout and
/// records the simulator. Fixture data only (no backend). Part 1: AIボイス → 声の調整 — pick 落ち着いて / ゆっくり / 穏やか and type
/// 「イギリス英語っぽく」 into 発音・話し方のリクエスト; stops on「試聴音声を作る」 (not tapped: it calls the voice provider).
/// Part 2: relaunch with --qa-voice-generated — the fixture's other preview selected in すべてのボイス; british-preview.patch
/// (capture-only) gives that fixture preview the same request text, so the list shows how a preview made with it is labelled.
final class EnrollmentRecoveryUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor func testTuningWalkthrough() {
        let app = XCUIApplication()
        let base = ["--uitesting", "--visual-fixtures", "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP",
                    "-UIPreferredContentSizeCategoryName", "UICTContentSizeCategoryL", "--qa-film-tuning", "--qa-voice-library"]
        app.launchArguments = base + ["--qa-route", "/voice"]
        app.launch()
        let tune = app.buttons["voice.create-preview"]
        XCTAssertTrue(tune.waitForExistence(timeout: 10))
        hold(2.5)                                                          // AIボイス: 将来の発音
        tune.tap()
        let calm = app.buttons["voice.style.0"]
        XCTAssertTrue(calm.waitForExistence(timeout: 5))
        hold(2.0)                                                          // 声の調整, read the sheet
        calm.tap(); hold(1.0)
        for id in ["voice.pace.0", "voice.expression.0"] {
            let b = app.buttons[id]
            if b.exists && b.isHittable { b.tap() }
            hold(0.9)
        }
        let field = app.textFields["voice.direction"].exists ? app.textFields["voice.direction"] : app.textViews["voice.direction"]
        for _ in 0..<4 where !field.isHittable { app.swipeUp(velocity: .slow) }
        field.tap(); hold(1.0)
        for ch in "イギリス英語っぽく" { app.typeText(String(ch)); hold(0.22) }
        hold(1.5)
        let create = app.buttons["試聴音声を作る"].firstMatch
        for _ in 0..<4 where !(create.exists && create.isHittable) { app.swipeUp(velocity: .slow) }
        hold(3.0)                                                          // 試聴音声を作る (not tapped: no provider call)
        app.terminate()
        app.launchArguments = base + ["--qa-voice-generated", "--qa-route", "/voice"]
        app.launch()
        hold(5.0)                                                          // the new preview, selected in すべてのボイス
    }
}
