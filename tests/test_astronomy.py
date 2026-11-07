
import pytest

from asterionix.astronomy.ephemeris import Ephemeris
from asterionix.astronomy.observer import Observer
from asterionix.astronomy.moon import Moon
from asterionix.astronomy.sun import Sun
from asterionix.astronomy.planets import Planets


@pytest.fixture(scope="module")
def ephemeris():
    return Ephemeris()


@pytest.fixture(scope="module")
def observer(ephemeris):
    return Observer(
        ephemeris,
        latitude=50.45,
        longitude=30.52,
        elevation_m=180,
    )


@pytest.fixture(scope="module")
def time(ephemeris):
    return ephemeris.timescale.utc(2026, 11, 7, 12, 0, 0)


def test_moon_position(ephemeris, observer, time):
    moon = Moon(ephemeris, observer)
    result = moon.get_position(time)

    assert -90 <= result["altitude_deg"] <= 90
    assert 0 <= result["azimuth_deg"] < 360
    assert result["distance_km"] > 0


def test_moon_illumination(ephemeris, observer, time):
    moon = Moon(ephemeris, observer)
    result = moon.get_illumination(time)

    assert 0 <= result["fraction"] <= 1
    assert result["percentage"] == pytest.approx(
        result["fraction"] * 100
    )


def test_sun_position(ephemeris, observer, time):
    sun = Sun(ephemeris, observer)
    result = sun.get_position(time)

    assert -90 <= result["altitude_deg"] <= 90
    assert 0 <= result["azimuth_deg"] < 360
    assert 0.98 < result["distance_au"] < 1.02


def test_sun_twilight_state(ephemeris, observer):
    sun = Sun(ephemeris, observer)

    cases = [
        (10, "daylight"),
        (-3, "civil_twilight"),
        (-9, "nautical_twilight"),
        (-15, "astronomical_twilight"),
        (-25, "astronomical_night"),
    ]

    for altitude, expected_state in cases:
        sun.get_sun_altitude = lambda time, value=altitude: value

        result = sun.get_twilight_state(None)

        assert result["state"] == expected_state
        assert result["altitude_deg"] == altitude


def test_planet_positions(ephemeris, observer, time):
    planets = Planets(ephemeris, observer)
    results = planets.get_positions(time)

    assert set(results.keys()) == {
        "Mercury",
        "Venus",
        "Mars",
        "Jupiter",
        "Saturn",
    }

    for result in results.values():
        assert -90 <= result["altitude_deg"] <= 90
        assert 0 <= result["azimuth_deg"] < 360
        assert result["distance_au"] > 0

        assert result["above_horizon"] == (
            result["altitude_deg"] > 0
        )


def test_ephemeris_missing_file(tmp_path):
    missing_file = tmp_path / "missing.bsp"

    with pytest.raises(FileNotFoundError):
        Ephemeris(path=missing_file)
