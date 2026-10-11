from logic_utils import (
    check_guess,
    parse_guess,
    update_score,
    get_range_for_difficulty,
)


def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_numeric_not_string_comparison():
    # Regression: as strings, "9" > "50" is True. Numerically 9 is too low.
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"


def test_parse_valid():
    assert parse_guess("42") == (True, 42, None)


def test_parse_blank_and_text():
    assert parse_guess("")[0] is False
    assert parse_guess("abc")[0] is False
    assert parse_guess(None)[0] is False


def test_parse_decimal_rejected():
    assert parse_guess("3.9")[0] is False


def test_parse_out_of_range():
    assert parse_guess("500", 1, 100)[0] is False
    assert parse_guess("0", 1, 100)[0] is False


def test_score_win_first_attempt():
    assert update_score(0, "Win", 1) == 90


def test_score_win_has_floor():
    assert update_score(0, "Win", 12) == 10


def test_score_wrong_guess_always_penalized():
    assert update_score(50, "Too High", 2) == 45
    assert update_score(50, "Too High", 3) == 45
    assert update_score(50, "Too Low", 2) == 45


def test_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    low, high = get_range_for_difficulty("Hard")
    assert high > get_range_for_difficulty("Normal")[1]