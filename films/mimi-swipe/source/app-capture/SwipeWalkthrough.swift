import XCTest

/// Screen-recording walkthrough for the Mimi short 「スワイプ復習」 (swipe review); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of NotesPerformanceUITests.swift in a cached app checkout and
/// records the simulator. Fixture notes only, plus "Bless your heart" from app-capture/bless-note.patch (capture-only).
/// Each card is dragged slowly and held before release, so the rating label (覚えていた / もう一度 / 簡単) is readable.
final class NotesPerformanceUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor func testSwipeWalkthrough() {
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
        let rate = app.buttons["notes.review.comfortable"]
        func ready() { _ = rate.waitForExistence(timeout: 3); for _ in 0..<40 where !rate.isEnabled { hold(0.25) } }
        func drag(_ from: CGVector, _ to: CGVector) {
            card.coordinate(withNormalizedOffset: from).press(forDuration: 0.15,
                thenDragTo: card.coordinate(withNormalizedOffset: to), withVelocity: .slow, thenHoldForDuration: 0.7)
        }
        let right = (CGVector(dx: 0.3, dy: 0.45), CGVector(dx: 0.95, dy: 0.5))
        let left = (CGVector(dx: 0.7, dy: 0.45), CGVector(dx: 0.05, dy: 0.5))
        let up = (CGVector(dx: 0.5, dy: 0.7), CGVector(dx: 0.5, dy: 0.12))
        ready(); hold(1.5)                                              // the first card, front
        card.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.4)).tap()   // flip: the meaning
        ready(); hold(1.8)
        for (i, move) in [right, left, right, up].enumerated() where card.exists {
            if i > 0 { ready(); hold(1.2) }                             // the next card, readable
            drag(move.0, move.1); hold(1.0)
        }
        hold(2.5)
    }
}
