# Process

The owner's words (Japanese, original):

- 「E：１か月前にして。日めくりカレンダーしながら対策する。」
- The earlier plan for this episode: test-night nerves → a mock in the app → calm on the day.

- Feedback on the first cut (PR #38): 「問題数はあくまでも現時点。9とか出すな」 → no question count anywhere: the 「模擬試験 n / 9」 chip became 「模擬試験 Part 1 / 2 / 3」, the caption became 「最初から最後まで、通しで答える。」, and the app's own counter is masked in the recording.

Decisions:

- The app screen is the IELTS Speaking **Mock exam** (`IELTSMockScreen`), recorded in the simulator with the QA fixture (`--uitesting --visual-fixtures --qa-ielts`, Japanese UI). Without `--reset-onboarding` the app does not jump to the exam screen by itself, so the walkthrough opens it from the Practice list (`ielts.open`). The fixture's recordings are 1 s of silence and its feedback, scores and the Band 6.5 estimate are synthetic; they are shown only with the app's own label 「AIによる非公式の目安」 and the film's note 「AIの練習用フィードバックです（公式スコアではありません）」. The fixture label 「デモデータ」 is masked.
- The app labels: the menu is 「スピーキング試験対策」 and the tab 「模擬試験」; the app also shows a question counter; the film masks it and shows no question count (see below). The copy and captions do not claim an official test, score or Band prediction.
- The tear-off calendar is CSS, so every page is deterministic; tear times accelerate (`scripts/tears.py`) and only the page under the falling one is drawn.
- New poses (nervous with a textbook, tearing a page, practising into the phone, calm on test morning) drawn with codex-p from the official art ([prompt](prompts/01-codex-poses.txt), [log](prompts/01-codex-poses.log)); the friend is `friend-oops` from mimi-action-add.
- Trademark: Lanclo's own IELTS spec notes that "IELTS" in a commercial menu label is not cleared; the film uses the word only to name the test the learner is preparing for. Flagged to the owner for review.

Learned: the first capture stopped on the Practice list (the `--qa-ielts` auto-route to the exam screen did not fire without `--reset-onboarding`); tapping `ielts.open` from the list works.
