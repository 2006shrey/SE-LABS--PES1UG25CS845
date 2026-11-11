
import pytest
from bowling_alley import lane_cost, frame_score, lane_assignment


# Lane cost branches
def test_weekday_booking():
    assert lane_cost("weekday", 2, 4, 2, False) == 900


def test_weekend_booking():
    assert lane_cost("weekend", 1, 4, 0, False) == 600


def test_invalid_day():
    with pytest.raises(ValueError):
        lane_cost("holiday", 1, 2, 0, False)


def test_invalid_games():
    with pytest.raises(ValueError):
        lane_cost("weekday", 0, 2, 0, False)


def test_invalid_players():
    with pytest.raises(ValueError):
        lane_cost("weekday", 1, 7, 0, False)


def test_too_many_shoes():
    with pytest.raises(ValueError):
        lane_cost("weekday", 1, 2, 3, False)


def test_more_than_four_players():
    assert lane_cost("weekday", 1, 5, 0, False) == 500


def test_league_discount():
    assert lane_cost("weekday", 1, 2, 0, True) == 320


# Frame score branches
def test_invalid_first_roll():
    with pytest.raises(ValueError):
        frame_score(-1, 0, [])


def test_invalid_second_roll():
    with pytest.raises(ValueError):
        frame_score(5, -1, [])


def test_strike():
    assert frame_score(10, 0, [5, 3]) == 18


def test_invalid_frame():
    with pytest.raises(ValueError):
        frame_score(8, 3, [])


def test_spare():
    assert frame_score(6, 4, [5]) == 15


def test_open_frame():
    assert frame_score(3, 4, []) == 7


# Lane assignment branches
def test_no_lanes():
    assert lane_assignment(4, False, 0) == "wait"


def test_kids_get_bumper_lane():
    assert lane_assignment(4, True, 2) == "bumper lane"


def test_more_than_six_players_two_lanes():
    assert lane_assignment(7, False, 2) == "two lanes"


def test_more_than_six_players_wait():
    assert lane_assignment(7, False, 1) == "wait"


def test_standard_lane():
    assert lane_assignment(4, False, 2) == "standard lane"
