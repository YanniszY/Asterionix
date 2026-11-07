import pytest

from asterionix.astronomy.observer import Observer


class DummyEphemeris:
    class Earth:
        def __add__(self, value):
            return value
    earth = Earth()


def test_observer_rejects_invalid_latitude():
    with pytest.raises(ValueError):
        Observer(DummyEphemeris(), 91, 0)


def test_observer_rejects_invalid_longitude():
    with pytest.raises(ValueError):
        Observer(DummyEphemeris(), 0, 181)


def test_observer_accepts_valid_coordinates():
    observer = Observer(DummyEphemeris(), 50.45, 30.52)

    assert observer.latitude == 50.45
    assert observer.longitude == 30.52
    assert observer.elevation_m == 0