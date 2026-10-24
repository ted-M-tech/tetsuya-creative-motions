import XCTest

/// Screen-recording walkthrough for 069 Real Slang 2「お腹すいてイライラ＝？」 (films/mimi-slang-hangry); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of OfficialDecksUITests.swift in a cached app checkout and records
/// the simulator. Same launch as OfficialDecksUITests/testBundledJapaneseCatalogBrowseAndSave: the shipped (bundled) deck catalogue
/// (no --qa-official-decks fixture), isolated QA notes (the fixture "Please"), no network or audio action.
/// My Notes → 単語帳 → スラング・カジュアル → ユニット6 (気分・テンション) → scroll to the "hangry" card → save (bookmark) → the next card ("I'm dead").
/// Series template (Real Slang): change DECK_UNIT and CARD_ID for the episode's card; the rest stays.
final class OfficialDecksUITests: XCTestCase {
    static let DECK_UNIT = "6", CARD_ID = "hangry", NEXT_ID = "i-m-dead", UNIT_FIRST_TERM = "chill"
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func dump(_ app: XCUIApplication, _ name: String) {
        try? app.debugDescription.write(toFile: "/tmp/mimi-slang2-\(name).txt", atomically: true, encoding: .utf8)
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
        for _ in 0..<4 where !unit.isHittable { app.swipeUp(velocity: .slow) }
        hold(1.8)                                                         // the unit list (scrolled so ユニット6 shows)
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
        hold(2.2)                                                         // the "hangry" card
        if save.isHittable { save.tap() } else { dump(app, "save") }
        hold(1.6)                                                         // saved: the bookmark fills, the tag menu opens
        app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.12)).tap()
        hold(2.0)                                                         // the card, saved
        // one slow swipe to the next card ("I'm dead")
        app.swipeUp(velocity: .slow)
        hold(1.0)
        let next = app.descendants(matching: .any)["decks.card." + Self.NEXT_ID].firstMatch
        if next.exists { dump(app, "next") }
        hold(2.5)
    }
}
