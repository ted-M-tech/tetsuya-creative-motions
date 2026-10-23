import XCTest

/// Screen-recording walkthrough for 065「I'm fine, thank you. しか言えない」 (films/mimi-decks-fine); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of OfficialDecksUITests.swift in a cached app checkout and records
/// the simulator. Same launch as OfficialDecksUITests/testBundledJapaneseCatalogBrowseAndSave: the shipped (bundled) deck catalogue,
/// isolated QA notes (the fixture "Please"), no network or audio action.
/// My Notes → 単語帳 → スラング・カジュアル → ユニット4 (あいさつ・お礼・謝罪) → scroll to the "all good" card → save (bookmark).
final class OfficialDecksUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func dump(_ app: XCUIApplication, _ name: String) {
        try? app.debugDescription.write(toFile: "/tmp/mimi-decks-fine-\(name).txt", atomically: true, encoding: .utf8)
    }
    @MainActor func testDecksWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-notes", "--qa-route", "/vocabulary",
                               "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP", "-UIPreferredContentSizeCategoryName", "UICTContentSizeCategoryL"]
        app.launch()
        let decks = app.buttons["単語帳"]
        XCTAssertTrue(decks.waitForExistence(timeout: 10))
        hold(1.5)                                                         // My Notes with the 単語帳 destination
        decks.tap()
        let slang = app.buttons["decks.deck.slang-casual"]
        if !slang.waitForExistence(timeout: 8) { dump(app, "list") }
        for _ in 0..<4 where !slang.isHittable { app.swipeUp(velocity: .slow) }
        hold(2.0)                                                         // the deck list: 初級 … スラング・カジュアル
        slang.tap()
        let unit = app.buttons["decks.unit.4"]
        if !unit.waitForExistence(timeout: 8) { dump(app, "units") }
        hold(1.8)                                                         // the unit list
        unit.tap()
        let card = app.descendants(matching: .any)["decks.card.all-good"].firstMatch
        let save = app.buttons["decks.save.all-good"]
        _ = app.staticTexts["how's it going"].waitForExistence(timeout: 8)
        hold(2.0)                                                         // ユニット4 あいさつ・お礼・謝罪: what's up, sup, yo, …
        // fast scroll past the earlier cards (what's up, sup, yo, …; cut in the edit), then place the "all good" card near the top
        for _ in 0..<40 where !card.exists { app.swipeUp(); hold(0.1) }
        if !card.exists { dump(app, "card") }
        hold(0.6)
        for _ in 0..<6 {
            let y = card.frame.minY
            if y > 120 && y < 230 { break }
            let from = min(max(y, 300), 780), to = from - (y - 160)
            let origin = app.coordinate(withNormalizedOffset: .zero)
            origin.withOffset(CGVector(dx: 200, dy: from)).press(forDuration: 0.05,
                thenDragTo: origin.withOffset(CGVector(dx: 200, dy: min(max(to, 60), 820))), withVelocity: .slow, thenHoldForDuration: 0.3)
        }
        hold(2.2)                                                         // the "all good" card
        save.tap()
        hold(1.6)                                                         // saved: the bookmark fills, the tag menu opens
        app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.12)).tap()
        hold(2.0)                                                         // the card, saved
    }
}
