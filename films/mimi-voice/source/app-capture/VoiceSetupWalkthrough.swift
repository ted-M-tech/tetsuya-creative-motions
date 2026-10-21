import XCTest

/// Screen-recording walkthrough for the AI voice setup short (films/mimi-voice); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of EnrollmentRecoveryUITests.swift in a cached app checkout and
/// records the simulator. Fixture data only; first-voice.patch (capture-only) makes the fixture learner one without a voice yet.
/// Part 1: /voice/new — consent toggles, the consent statement read once, a 10–30 s voice sample (simulator microphone; nothing is sent:
/// the walkthrough stops before「自分の声を作る」). Part 2: relaunch on /voice/preview — the fixture's ready AI voice.
final class EnrollmentRecoveryUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func allowMic() {
        let sb = XCUIApplication(bundleIdentifier: "com.apple.springboard")
        for label in ["許可", "OK", "Allow"] where sb.alerts.buttons[label].exists { sb.alerts.buttons[label].tap(); return }
    }
    @MainActor func testVoiceSetupWalkthrough() {
        let app = XCUIApplication()
        let base = ["--uitesting", "--visual-fixtures", "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP",
                    "-UIPreferredContentSizeCategoryName", "UICTContentSizeCategoryL"]
        app.launchArguments = base + ["--qa-film-first-voice", "--qa-route", "/voice/new"]
        app.launch()
        let proceed = app.buttons["enrollment.continue"]
        XCTAssertTrue(proceed.waitForExistence(timeout: 10))
        hold(2.0)                                                         // 声の登録, read the page
        for id in ["enrollment.adult", "enrollment.consent", "enrollment.retain", "enrollment.feedback"] {
            let toggle = app.switches[id]
            for _ in 0..<4 where !toggle.isHittable { app.swipeUp(velocity: .slow) }
            if toggle.exists { toggle.coordinate(withNormalizedOffset: CGVector(dx: 0.94, dy: 0.5)).tap() }
            hold(0.7)
        }
        let details = app.buttons["声の取り扱い"].firstMatch                // the privacy note, opened
        for _ in 0..<3 where details.exists && !details.isHittable { app.swipeUp(velocity: .slow) }
        if details.exists && details.isHittable { details.tap(); hold(2.5) }
        proceed.tap()
        let record = app.buttons["enrollment.record"]
        XCTAssertTrue(record.waitForExistence(timeout: 5))
        hold(2.0)                                                         // 同意を録音: the statement
        record.tap(); hold(1.0); allowMic()
        hold(3.5); if record.exists { record.tap() }
        let next = app.buttons["enrollment.next"]
        _ = next.waitForExistence(timeout: 5); hold(1.2)
        next.tap()
        XCTAssertTrue(record.waitForExistence(timeout: 5))
        hold(2.0)                                                         // 声のサンプル: the passage, 静かな場所で、10〜30秒。
        record.tap(); hold(1.0); allowMic()
        hold(11.5); if record.exists { record.tap() }
        _ = next.waitForExistence(timeout: 5)
        hold(2.5)                                                         // 自分の声を作る (not tapped: no provider call)
        app.terminate()
        app.launchArguments = base + ["--qa-route", "/voice/preview"]
        app.launch()
        hold(3.0)
        let preview = app.buttons["試聴"].firstMatch
        if preview.waitForExistence(timeout: 3) && preview.isHittable { preview.tap() }
        hold(4.0)
    }
}
