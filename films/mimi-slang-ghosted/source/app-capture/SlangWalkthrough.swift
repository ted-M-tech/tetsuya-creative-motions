import XCTest

/// Screen-recording walkthrough for 070 Real Slang 3「既読スルー、英語で？」 (films/mimi-slang-ghosted); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of OfficialDecksUITests.swift in a cached app checkout and records
/// the simulator. Same launch as OfficialDecksUITests/testBundledJapaneseCatalogBrowseAndSave: the shipped (bundled) deck catalogue
/// (no --qa-official-decks fixture), isolated QA notes (the fixture "Please"), no network or audio action.
/// My Notes → 単語帳 → スラング・カジュアル → ユニット8 (SNS・ネット文化, below the fold: one slow swipe) → the "ghost" card → save (bookmark) → the "leave sb on read" card.
/// Series template (Real Slang): change DECK_UNIT and CARD_ID for the episode's card; the rest stays.
final class OfficialDecksUITests: XCTestCase {
    static let DECK_UNIT = "8", CARD_ID = "ghost", NEXT_ID = "leave-sb-on-read", UNIT_FIRST_TERM = "DM"
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func dump(_ app: XCUIApplication, _ name: String) {
        try? app.debugDescription.write(toFile: "/tmp/mimi-ghosted-\(name).txt", atomically: true, encoding: .utf8)
    }
    @MainActor func testSlangWalkthrough() {
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
        let unit = app.buttons["decks.unit." + Self.DECK_UNIT]
        if !unit.waitForExistence(timeout: 8) { dump(app, "units") }
        hold(1.8)                                                         // the unit list (units 1-5)
        for _ in 0..<4 where !(unit.isHittable && unit.frame.maxY < 760) { app.swipeUp(velocity: .slow); hold(0.4) }
        hold(1.2)                                                         // the unit list, ユニット8 in view
        unit.tap()
        let card = app.descendants(matching: .any)["decks.card." + Self.CARD_ID].firstMatch
        let save = app.buttons["decks.save." + Self.CARD_ID]
        _ = app.staticTexts[Self.UNIT_FIRST_TERM].waitForExistence(timeout: 8)
        hold(2.0)                                                         // the unit top
        // fast scroll past the earlier cards (cut in the edit), then place the card near the top
        for _ in 0..<60 where !(card.exists && card.frame.minY < 700) { app.swipeUp(); hold(0.1) }
        if !card.exists { dump(app, "card") }
        hold(0.8)
        for _ in 0..<6 {
            let y = card.frame.minY
            if y > 100 && y < 260 { break }
            let origin = app.coordinate(withNormalizedOffset: .zero)
            let from = min(max(y + 40, 320), 780), to = from - (y - 170)
            origin.withOffset(CGVector(dx: 200, dy: from)).press(forDuration: 0.1,
                thenDragTo: origin.withOffset(CGVector(dx: 200, dy: min(max(to, 60), 820))), withVelocity: 300, thenHoldForDuration: 0.6)
            hold(0.6)
        }
        hold(2.2)                                                         // the "ghost" card
        if save.isHittable { save.tap() } else { dump(app, "save") }
        hold(1.6)                                                         // saved: the bookmark fills, the tag menu opens
        app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.12)).tap()
        hold(2.0)                                                         // the card, saved
        // one slow swipe to the next card ("leave sb on read")
        app.swipeUp(velocity: .slow)
        hold(1.0)
        let next = app.descendants(matching: .any)["decks.card." + Self.NEXT_ID].firstMatch
        if next.exists { dump(app, "next") }
        hold(2.5)
    }
}
