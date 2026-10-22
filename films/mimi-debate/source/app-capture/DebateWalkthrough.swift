import XCTest

/// Screen-recording walkthrough for the debate short (films/mimi-debate); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of DebateUITests.swift in a cached app checkout and records the
/// simulator. QA debate fixture only (DebateQA + --qa-free-speech-v3: synthetic transcript, feedback and opponent; no backend).
/// live-mic.patch (capture-only) lets the recorder use the simulator microphone so the meter moves; the fixture ignores the audio.
/// Practice tab → ディベート練習 → お金と幸せ → 賛成 → record, send → feedback + 相手の意見 → 返答を録音する → record, send → ディベート完了.
final class DebateUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func drag(_ app: XCUIApplication, from: Double, to: Double, hold seconds: Double = 0.2) {
        app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: from))
            .press(forDuration: 0.05, thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: to)),
                   withVelocity: 500, thenHoldForDuration: seconds)
    }
    @MainActor private func allowAlerts(_ app: XCUIApplication) {
        let sb = XCUIApplication(bundleIdentifier: "com.apple.springboard")
        for label in ["許可", "OK", "Allow"] where sb.alerts.buttons[label].exists { sb.alerts.buttons[label].tap(); hold(0.5) }
        let consent = app.buttons["consent.enable"]
        if consent.exists { consent.tap(); hold(0.5) }
    }
    @MainActor private func visible(_ app: XCUIApplication, _ e: XCUIElement) {
        for _ in 0..<8 where !e.isHittable { drag(app, from: 0.7, to: 0.4) }
    }
    @MainActor private func turn(_ app: XCUIApplication, speak seconds: Double) {
        let record = app.buttons["debate.record"]
        XCTAssertTrue(record.waitForExistence(timeout: 8))
        record.tap(); hold(0.8); allowAlerts(app)
        if !app.buttons["debate.stop"].exists && record.exists { record.tap(); hold(0.8); allowAlerts(app) }
        hold(seconds)
        let stop = app.buttons["debate.stop"]
        if stop.exists { stop.tap() }
        let send = app.buttons["debate.submit"]
        _ = send.waitForExistence(timeout: 5); hold(1.2)                // the take: replay, meter, send
        send.tap(); hold(0.5); allowAlerts(app)
    }
    @MainActor func testDebateWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-debate", "--qa-free-speech-v3", "--qa-film-live-mic",
                               "--qa-roleplay-language", "en", "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP",
                               "-UIPreferredContentSizeCategoryName", "UICTContentSizeCategoryL"]
        app.launch()
        app.tabBars.buttons["練習"].tap()
        let entry = app.buttons["debate.open"]
        _ = entry.waitForExistence(timeout: 10)
        hold(1.0); visible(app, entry); hold(0.6)
        entry.tap()
        let topic = app.buttons["debate.topic.money-happiness"]
        _ = topic.waitForExistence(timeout: 5)
        hold(1.8)                                                       // the themes
        topic.tap()
        let position = app.buttons["debate.position.position-3"]
        _ = position.waitForExistence(timeout: 5)
        hold(1.8)                                                       // お金が増えるほど、人は幸せになる。 立場を選ぶ
        visible(app, position); hold(0.6)
        position.tap()
        hold(2.0)                                                       // 1/2: the claim, 賛成, 自分の意見と、その理由を一つ話してください。
        turn(app, speak: 4.0)
        let reply = app.buttons["debate.reply"]
        _ = reply.waitForExistence(timeout: 10)
        hold(2.5)                                                       // feedback, top
        drag(app, from: 0.75, to: 0.35, hold: 0.3); hold(2.5)           // 次に試すこと / 言い方の例
        drag(app, from: 0.75, to: 0.35, hold: 0.3); hold(2.0)
        drag(app, from: 0.75, to: 0.25, hold: 0.3); hold(3.0)           // 相手の意見: rebuttal and question
        reply.tap()
        hold(2.5)                                                       // 2/2: 相手の意見に応えてください。
        turn(app, speak: 4.0)
        _ = app.buttons["debate.done"].waitForExistence(timeout: 10)
        hold(3.0)                                                       // final feedback, ディベート完了
        drag(app, from: 0.75, to: 0.35, hold: 0.3); hold(2.0)
    }
}
