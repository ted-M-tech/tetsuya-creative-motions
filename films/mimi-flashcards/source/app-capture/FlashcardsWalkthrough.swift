import XCTest

/// Screen-recording walkthrough for the flashcards CSV short (follow-up to films/mimi-import) (films/mimi-flashcards); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of NoteImportUITests.swift in a cached app checkout and records
/// the simulator. Fixture data only: the fixture note "Please" plus 単語帳.csv (10 rows: term, meaning, tags; this folder), copied beforehand into the
/// simulator's Files (On My iPhone). note-import.patch (capture-only) lets the fixture guest import, since import is for signed-in learners.
/// My Notes → … → CSVを読み込む → CSVファイルを選ぶ → the system picker → the preview → 10件を追加 → close → the 単語帳 folder → 学習開始.
final class NoteImportUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor private func dump(_ app: XCUIApplication, _ name: String) {
        try? app.debugDescription.write(toFile: "/tmp/mimi-flashcards-\(name).txt", atomically: true, encoding: .utf8)
    }
    @MainActor func testImportWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "--qa-notes", "--qa-note-detail", "--qa-film-import", "--qa-route", "/vocabulary",
                               "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP", "-UIPreferredContentSizeCategoryName", "UICTContentSizeCategoryL"]
        app.launch()
        let more = app.buttons["notes.more"]
        XCTAssertTrue(more.waitForExistence(timeout: 10))
        hold(1.5)                                                         // My Notes: すべて 1
        more.tap(); hold(0.8)
        app.buttons["notes.importCSV"].tap()
        let choose = app.buttons["noteImport.choose"]
        XCTAssertTrue(choose.waitForExistence(timeout: 5))
        hold(2.0)                                                         // the import sheet
        choose.tap()
        hold(2.0)
        let file = app.descendants(matching: .any).matching(NSPredicate(format: "label BEGINSWITH '単語帳, csv'")).firstMatch
        if !file.waitForExistence(timeout: 3) {
            dump(app, "picker")
            for label in ["ブラウズ", "Browse"] where app.buttons[label].exists { app.buttons[label].tap(); hold(1.0); break }
            for label in ["このiPhone内", "On My iPhone"] {
                let place = app.descendants(matching: .any).matching(NSPredicate(format: "label == %@", label)).firstMatch
                if place.exists { place.tap(); hold(1.5); break }
            }
        }
        if !file.waitForExistence(timeout: 4) { dump(app, "picker2") }
        file.tap()
        let addAll = app.buttons["noteImport.add"]
        if !addAll.waitForExistence(timeout: 5) {
            for label in ["開く", "Open"] where app.buttons[label].exists { app.buttons[label].tap(); break }
            _ = addAll.waitForExistence(timeout: 5)
        }
        hold(2.5)                                                         // the preview: 新しく追加できるノート 10件
        if !addAll.exists { dump(app, "preview") }
        addAll.tap()
        _ = app.staticTexts["noteImport.message"].waitForExistence(timeout: 10)
        hold(2.0)                                                         // 10件を追加しました。
        app.buttons["閉じる"].firstMatch.tap()
        let folder = app.buttons["notes.group.単語帳"]
        _ = folder.waitForExistence(timeout: 5)
        hold(2.0)                                                         // My Notes: すべて 11, 単語帳 10
        folder.tap()
        hold(2.5)                                                         // the 単語帳 list
        let start = app.buttons["notes.review"]
        if start.waitForExistence(timeout: 5) { start.tap() } else { dump(app, "list") }
        let card = app.descendants(matching: .any)["notes.review.card"].firstMatch
        _ = card.waitForExistence(timeout: 8)
        hold(1.5)                                                         // the first card, front
        for _ in 0..<2 where card.exists {
            card.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.4)).tap()             // flip: the meaning
            let rate = app.buttons["notes.review.comfortable"]
            _ = rate.waitForExistence(timeout: 3)
            for _ in 0..<40 where !rate.isEnabled { hold(0.25) }        // dimmed while the model voice plays
            hold(1.8)
            if rate.isHittable { rate.tap() }
            hold(1.2)
        }
        hold(1.0)
    }
}
