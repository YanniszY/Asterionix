"""High-level observation report assembly."""

from asterionix.astronomy.moon import Moon
from asterionix.astronomy.sun import Sun
from asterionix.astronomy.planets import Planets

from asterionix.planner.visibility import find_observation_windows
from asterionix.planner.moon_events import find_moon_events


def build_report(ephemeris, observer, time):
    moon = Moon(ephemeris, observer)
    sun = Sun(ephemeris, observer)
    planets = Planets(ephemeris, observer)

    moon_position = moon.get_position(time)
    moon_illumination = moon.get_illumination(time)
    sun_position = sun.get_position(time)
    planet_positions = planets.get_positions(time)

    return {
        "moon": {
            **moon_position,
            **moon_illumination,
            "above_horizon": moon_position["altitude_deg"] > 0,
        },
        "sun": {
            **sun_position,
            **sun.get_twilight_state(time),
        },
        "planets": planet_positions,
    }


def get_moon_windows(ephemeris, observer, time, hours=24):
    return find_observation_windows(
        ephemeris=ephemeris,
        observer=observer,
        body=ephemeris.moon,
        start_time=time,
        hours=hours,
    )


def get_moon_events(ephemeris, observer, time, hours=24):
    return find_moon_events(
        ephemeris=ephemeris,
        observer=observer,
        start_time=time,
        hours=hours,
    )