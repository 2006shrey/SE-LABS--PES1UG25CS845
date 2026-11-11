
import pytest
from bowling_alley import lane_cost, frame_score, lane_assignment


# Lane cost tests
def test_weekday_booking():
    assert lane_cost("weekday", 2, 4, 2, False) == 900


def test_weekend_booking_with_league_member():
    assert lane_cost("weekend", 2, 5, 2, True) == 1200


def test_unknown_day_type():
    with pytest.raises(ValueError):
        lane_cost("holiday", 1, 2, 1, False)


def test_invalid_booking():
    with pytest.raises(ValueError):
        lane_cost("weekday", 0, 2, 1, False)


def test_too_many_shoe_rentals():
    with pytest.raises(ValueError):
        lane_cost("weekday", 1, 2, 3, False)


# Frame score tests
def test_open_frame():
    assert frame_score(3, 4, []) == 7


def test_strike():
    assert frame_score(10, 0, [5, 3]) == 18


def test_spare():
    assert frame_score(6, 4, [5]) == 15


def test_invalid_roll():
    with pytest.raises(ValueError):
        frame_score(11, 0, [])


def test_invalid_frame():
    with pytest.raises(ValueError):
        frame_score(8, 3, [])


# Lane assignment tests
def test_no_lanes_available():
    assert lane_assignment(4, False, 0) == "wait"


def test_bumper_lane():
    assert lane_assignment(4, True, 2) == "bumper lane"


def test_two_lanes():
    assert lane_assignment(7, False, 2) == "two lanes"


def test_wait_for_second_lane():
    assert lane_assignment(7, False, 1) == "wait"


def test_standard_lane():
    assert lane_assignment(4, False, 2) == "standard lane"
