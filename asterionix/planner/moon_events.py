"""Moonrise and moonset calculations."""

from skyfield import almanac


def find_moon_events(ephemeris, observer, start_time, hours=24):
    end_time = start_time + hours / 24

    rise_times, rise_flags = almanac.find_risings(
        observer.topos,
        ephemeris.moon,
        start_time,
        end_time,
    )

    set_times, set_flags = almanac.find_settings(
        observer.topos,
        ephemeris.moon,
        start_time,
        end_time,
    )

    events = []

    for event_time, actually_rises in zip(rise_times, rise_flags):
        if actually_rises:
            events.append({
                "type": "Moonrise",
                "time": event_time,
            })

    for event_time, actually_sets in zip(set_times, set_flags):
        if actually_sets:
            events.append({
                "type": "Moonset",
                "time": event_time,
            })

    events.sort(key=lambda event: event["time"].tt)

    return events