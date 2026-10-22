import XCTest

/// Screen-recording walkthrough for the Mimi short "Frozen Abroad" (mimi-frozen-abroad); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of SituationUITests.swift in a cached app checkout and records
/// the simulator, with PATCH=airport-lines.patch (the QA situation fixture speaks the airport scene's authored lines).
/// QA fixture only: synthetic partner lines and hints, no backend, no personal data.
final class SituationUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func drag(_ app: XCUIApplication, from: Double, to: Double, hold seconds: Double = 0.1) {
        app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: from))
            .press(forDuration: 0.05, thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: to)),
                   withVelocity: 600, thenHoldForDuration: seconds)
    }
    @MainActor func testAirportWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-situations", "--qa-situations-loading", "--qa-roleplay-language", "en",
                               "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        app.tabBars.buttons["練習"].tap()
        let entry = app.buttons["roleplay.open"]
        _ = entry.waitForExistence(timeout: 10)
        for _ in 0..<8 where !entry.isHittable { app.swipeUp() }
        hold(0.8); entry.tap()
        let airport = app.buttons["roleplay.category.airport"]
        _ = airport.waitForExistence(timeout: 5)
        hold(2.0)                                                       // the catalogue
        drag(app, from: 0.75, to: 0.45, hold: 0.3); hold(2.0)           // 空港・交通・ホテル
        for _ in 0..<8 where !airport.isHittable { app.swipeUp() }
        airport.tap()
        let task = app.buttons["roleplay.scene.roleplay-en-airport-checkin"]
        _ = task.waitForExistence(timeout: 5)
        hold(1.8)                                                       // the airport scenes
        task.tap()
        let hint = app.buttons["situation.hint"]
        _ = hint.waitForExistence(timeout: 15)                          // loading (6 s), then the partner speaks
        hold(2.2)
        let meaning = app.buttons["meaning.toggle"]
        if meaning.exists && meaning.isHittable { meaning.tap() }
        hold(1.8)
        if hint.isHittable { hint.tap() }
        hold(3.2)                                                       // the hint cards
        let record = app.buttons["situation.record"]
        if record.isHittable { record.tap() }                           // the fixture accepts a silent take and sends it
        _ = app.staticTexts["situation.complete"].waitForExistence(timeout: 15)
        hold(3.2)
        for _ in 0..<2 {
            let back = app.navigationBars.buttons.element(boundBy: 0)
            if back.exists && back.isHittable { back.tap() }
            hold(1.2)
        }
        hold(1.0)
        drag(app, from: 0.8, to: 0.3, hold: 0.3); hold(1.5)
        drag(app, from: 0.8, to: 0.3, hold: 0.3); hold(2.0)
    }
}
