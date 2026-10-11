# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

An AI built a Streamlit number guessing game, and the game was unplayable. Hints were backwards, scoring rewarded wrong guesses, and the game could not be restarted after it ended. This project is about finding those bugs by playing the game, fixing them, and proving the fixes with tests.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`
3. Run the tests: `python -m pytest -v`

## 📝 Document Your Experience

### Game's purpose

A number guessing game built with Streamlit. The player picks a difficulty (Easy, Normal, Hard), which sets the number range and how many attempts they get. They guess the secret number, get a Higher or Lower hint after each guess, and earn or lose points based on how they do.

### Bugs found

| # | What I did | Expected | What actually happened |
|---|-----------|----------|------------------------|
| 1 | Guessed 50 when the secret was 85 | "Go HIGHER" | "Go LOWER" (hint messages were swapped) |
| 2 | Guessed 90 when the secret was 85 | "Go LOWER" | "Go HIGHER" |
| 3 | Guessed 9 on an even attempt, secret 85 | Counted as too low, score goes down | Counted as too high, score went up by 5 (the secret was turned into a string on even attempts, so numbers were compared as text) |
| 4 | Guessed 500 | Rejected as out of range | Accepted and counted as a real guess |
| 5 | Guessed 3.9 | Rejected | Silently turned into 3 |
| 6 | Submitted a blank box, then `abc` | Error, no attempt used | Error shown, but each one used up an attempt and was added to the history |
| 7 | Loaded a fresh game on Normal (8 attempts) | "Attempts left: 8" | "Attempts left: 7" before any guess (attempts started at 1) |
| 8 | Lost the game, then clicked New Game | A fresh game | New secret, but still "Game over", and the old score and history stayed |
| 9 | Switched to Easy mid-game | Secret between 1 and 20 | Sidebar said 1 to 20, but the secret was still 80 and the info box still said "between 1 and 100" |
| 10 | Switched to Hard | Harder than Normal | Range was 1 to 50, narrower than Normal's 1 to 100, so it was easier |
| 11 | Won on the first guess | Highest possible score | Scored 70 (off by one, because the attempt count was already 2) |

One thing I noticed that the instructions did not describe: the README suggests the secret number changes every time you click Submit, but when I watched the Debug panel it stayed the same for the whole game. The real state problems were in New Game and in changing difficulty.

### Fixes applied

- Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` out of `app.py` into `logic_utils.py`, and imported them back into `app.py`.
- `check_guess` now compares numbers only (no string conversion) and the Higher/Lower messages are correct.
- `parse_guess` now rejects blank input, text, decimals, and numbers outside the difficulty range. Invalid input no longer uses up an attempt.
- Attempts now start at 0 and only go up after a valid guess, which fixes "Attempts left" and the first-guess score.
- `update_score` now takes 5 points off for every wrong guess, and a win scores 100 minus 10 per attempt, with a minimum of 10.
- Added a `start_new_game` function that resets the secret, attempts, score, status, and history. It runs on New Game and whenever the difficulty changes, and the secret is picked from that difficulty's range.
- Changed Hard to 1 to 200 so it is actually harder than Normal.
- Rewrote the starter tests (they compared `check_guess` to a plain string, but it returns an outcome and a message) and added tests for parsing, scoring, ranges, and the string comparison bug.

Not fixed: the "Attempts left" box and the Developer Debug Info panel are drawn before the guess is processed, so they show the numbers from one click ago. I left it because it only affects the debug display.

## 📸 Demo Walkthrough

1. Start the app, keep the difficulty on Normal, and open "Developer Debug Info" to see the secret number.
2. Guess a number below the secret and confirm it says "Go HIGHER", then guess one above it and confirm it says "Go LOWER".
3. Submit a blank box, then `abc`, `3.9`, and `500`. Each one shows an error and "Attempts left" does not go down.
4. Switch the difficulty to Easy and confirm the info box says 1 to 20 and the secret in the debug panel is a number from 1 to 20.
5. Guess the secret number on the first try and confirm the game says you won with a final score of 90. Click New Game and confirm you can play again with a score of 0.

## 🧪 Test Results

```
================================================================ test session starts =================================================================
platform darwin -- Python 3.13.9, pytest-8.4.2, pluggy-1.5.0
rootdir: /Users/ernestocoronel/codepath-demo/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.10.0
collected 12 items                                                                                                                                   

tests/test_game_logic.py ............                                                                                                          [100%]

================================================================= 12 passed in 0.03s =================================================================
```

## 🚀 Stretch Features

I did not attempt any stretch features.