import XCTest

/// Screen-recording walkthrough for the origin short (films/mimi-origin); not a test of behaviour.
/// kits/mimi-short/app-capture/capture.sh puts this file in place of DescribeUITests.swift in a cached app checkout and
/// records the simulator. Fixture data only. Part 1: Home (the launch shot). Part 2: Settings › ヘルプとアプリ情報, to check
/// the label of the support entry the film mentions.
final class DescribeUITests: XCTestCase {
    @MainActor private func hold(_ s: Double) { Thread.sleep(forTimeInterval: s) }
    @MainActor func testHomeWalkthrough() {
        let app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--visual-fixtures", "-AppleLanguages", "(ja)", "-AppleLocale", "ja_JP"]
        app.launch()
        _ = app.waitForHome(timeout: 15); hold(4.0)             // home
        app.tabBars.buttons.element(boundBy: 3).tap(); hold(1.0)
        let settings = app.buttons["nav.settings"]
        if settings.waitForExistence(timeout: 5) { settings.tap(); hold(1.5) }
        let about = app.buttons["settings.about"]
        for _ in 0..<6 where about.exists && !about.isHittable { app.swipeUp(velocity: .slow) }
        if about.exists { about.tap(); hold(3.0) }               // ヘルプとアプリ情報: サポート, 利用規約, ...
    }
}
