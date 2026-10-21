import XCTest

/// Screen-recording walkthrough for the Action Button ② (Start review) short; not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of WidgetUITests.swift in a cached app checkout and records
/// the simulator. Fixture notes only, plus "Bless your heart" from app-capture/bless-note.patch (capture-only).
final class WidgetUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor func testReviewWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-notes", "--qa-note-review",
            "--qa-note-review-three", "--qa-note-detail", "--qa-note-bless", "--qa-route", "lanclo://vocabulary/review/today",
            "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        let card = app.descendants(matching: .any)["notes.review.card"].firstMatch
        if !card.waitForExistence(timeout: 8) {                         // new notes: start from My Notes' study button
            let start = app.buttons["notes.review"]
            if start.waitForExistence(timeout: 5) { start.tap() }
            _ = card.waitForExistence(timeout: 8)
        }
        hold(1.5)                                                       // the first card, front
        for _ in 0..<4 where card.exists {
            card.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.4)).tap()             // flip: the meaning
            let rate = app.buttons["notes.review.comfortable"]
            _ = rate.waitForExistence(timeout: 3)
            for _ in 0..<40 where !rate.isEnabled { hold(0.25) }        // the card is dimmed while the model voice plays
            hold(1.8)                                                   // the meaning, readable
            if rate.isHittable { rate.tap() }
            hold(1.2)                                                   // the next card
        }
        hold(2.0)
    }
}
