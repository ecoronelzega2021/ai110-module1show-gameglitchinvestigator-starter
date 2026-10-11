# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The game looked normal when I first ran it: a difficulty dropdown, a text box, and a debug panel showing the secret. But it was close to unplayable, because the Higher and Lower hints pointed the wrong way, so following them moved me away from the secret. Wrong guesses could also raise my score, and a blank or non-numeric guess used up one of my attempts. After a game ended, New Game gave a new secret but left me stuck on the "Game over" screen, and changing the difficulty did not change the secret, so I could be guessing a number outside the range shown in the sidebar.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 50 when the secret was 85 | "Go HIGHER" | "Go LOWER" (the hint messages were swapped) | None |
| Guess 9 on an even attempt, secret 85 | Counted as too low, score goes down | Counted as too high, score went up by 5 (the secret became a string on even attempts, so numbers were compared as text) | None |
| Blank box, then `abc` | An error and no attempt used | An error, but each one used up an attempt and was added to the history | None (error shown on the page) |
| Guess 500 (range was 1 to 100) | Rejected as out of range | Accepted as a real guess | None |
| Lose the game, then click New Game | A fresh game | New secret, but still "Game over", with the old score and history kept | None |
| Switch to Easy mid-game | New secret between 1 and 20 | Sidebar said 1 to 20, but the secret stayed at 80 | None |

---

## 2. How did you use AI as a teammate?

I used Claude (Anthropic) in a chat to read the starter code, list the likely bugs, write the fixes, and run through the game in my browser to reproduce the bugs and check the fixes. One correct suggestion was about the hints: Claude pointed out that on every even attempt `app.py` turned the secret into a string, so Python compared "9" and "85" as text instead of as numbers, and it suggested comparing integers only. I checked that by guessing 9 against a secret of 85, which raised my score by 5 before the fix and lowered it after, and I added a test called `test_numeric_not_string_comparison` that passes. One suggestion I did not apply was a way to fix the Debug panel and "Attempts left" showing numbers from one click ago, which would have meant rearranging how the page is drawn. I left it because it only affects the debug display, and I confirmed by playing full games that the hints, score, and attempts were all correct even while the panel lagged.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed when I repeated the exact input that caused it and got the expected result, for example guessing 500, `abc`, and a blank box and checking that the attempt counter did not move. I also ran `pytest`, and the test that taught me the most was `test_numeric_not_string_comparison`, which checks that a guess of 9 against a secret of 50 is "Too Low". It showed that the string comparison was a real separate bug from the swapped hints, and it would fail if the string conversion came back. Claude helped me see that the starter tests would fail even with correct logic, because they compared `check_guess` to a plain string while the function returns an outcome and a message, and it helped me write new tests for parsing, scoring, and the difficulty ranges. All 12 tests passed.

---

## 4. What did you learn about Streamlit and state?

Streamlit runs your whole script again from top to bottom every time you click a button or change a widget, so any normal variable gets wiped on each click. Think of it like a whiteboard that gets erased on every click, except for one box called `st.session_state` that keeps what you put in it. That is why the secret number, attempts, score, and history have to be stored in `st.session_state`. A button is also only true on the single rerun right after it is clicked, and because the Debug panel is drawn before the guess is processed, it shows numbers from one click ago.

---

## 5. Looking ahead: your developer habits

One habit I want to keep is reproducing each bug with a specific input and writing down what I expected and what happened before I change any code, then turning each bug into a test so it cannot quietly come back. Next time I would run the tests after every single change instead of at the end, and I would check claims in the instructions myself sooner. For example, the README suggested the secret changed on every Submit, but when I watched the Debug panel it stayed the same, and the real state bugs were in New Game and changing difficulty. This project made me see that AI-generated code can look finished and still be wrong in ways that only show up when you play it and test it.