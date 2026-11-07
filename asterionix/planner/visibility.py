
"""Geometric observation-window calculations.

This module checks whether a celestial body satisfies basic geometric
conditions for observation.

It does not account for weather, atmospheric extinction, light pollution,
local obstructions, seeing, or optical equipment.
"""

from datetime import timedelta


def _evaluate(
    ephemeris,
    observer,
    body,
    dt,
    minimum_altitude_deg,
    maximum_sun_altitude_deg,
):
    """Evaluate observation conditions at a specific UTC datetime."""

    time = ephemeris.timescale.from_datetime(dt)
    observer_at_time = observer.topos.at(time)

    target = observer_at_time.observe(body).apparent()
    target_altitude = float(target.altaz()[0].degrees)

    sun = observer_at_time.observe(ephemeris.sun).apparent()
    sun_altitude = float(sun.altaz()[0].degrees)

    suitable = (
        target_altitude >= minimum_altitude_deg
        and sun_altitude <= maximum_sun_altitude_deg
    )

    return {
        "time": dt,
        "target_altitude_deg": target_altitude,
        "sun_altitude_deg": sun_altitude,
        "suitable": suitable,
    }


def _find_boundary(
    ephemeris,
    observer,
    body,
    left,
    right,
    left_state,
    minimum_altitude_deg,
    maximum_sun_altitude_deg,
    precision_seconds=1,
):
    """Find a suitability transition using binary search."""

    while (right - left).total_seconds() > precision_seconds:
        middle = left + (right - left) / 2

        sample = _evaluate(
            ephemeris,
            observer,
            body,
            middle,
            minimum_altitude_deg,
            maximum_sun_altitude_deg,
        )

        if sample["suitable"] == left_state:
            left = middle
        else:
            right = middle

    return left + (right - left) / 2


def _make_window(start, end, samples):
    """Build a result dictionary for one observation window."""

    peak = max(
        samples,
        key=lambda sample: sample["target_altitude_deg"],
    )

    return {
        "start_utc": start,
        "end_utc": end,
        "peak_altitude_deg": peak["target_altitude_deg"],
        "sun_altitude_at_peak_deg": peak["sun_altitude_deg"],
    }


def find_observation_windows(
    ephemeris,
    observer,
    body,
    start_time,
    hours: int = 24,
    step_minutes: int = 10,
    minimum_altitude_deg: float = 10.0,
    maximum_sun_altitude_deg: float = -12.0,
):
    """Find observation windows and refine their boundaries."""

    if hours <= 0:
        raise ValueError("hours must be positive")

    if step_minutes <= 0:
        raise ValueError("step_minutes must be positive")

    start_datetime = start_time.utc_datetime()
    end_datetime = start_datetime + timedelta(hours=hours)
    step = timedelta(minutes=step_minutes)

    current = start_datetime

    first_sample = _evaluate(
        ephemeris,
        observer,
        body,
        current,
        minimum_altitude_deg,
        maximum_sun_altitude_deg,
    )

    previous_state = first_sample["suitable"]

    active_start = start_datetime if previous_state else None
    active_samples = [first_sample] if previous_state else []

    windows = []

    while current < end_datetime:
        next_time = min(current + step, end_datetime)

        sample = _evaluate(
            ephemeris,
            observer,
            body,
            next_time,
            minimum_altitude_deg,
            maximum_sun_altitude_deg,
        )

        current_state = sample["suitable"]

        if current_state != previous_state:
            boundary = _find_boundary(
                ephemeris,
                observer,
                body,
                current,
                next_time,
                previous_state,
                minimum_altitude_deg,
                maximum_sun_altitude_deg,
            )

            boundary_sample = _evaluate(
                ephemeris,
                observer,
                body,
                boundary,
                minimum_altitude_deg,
                maximum_sun_altitude_deg,
            )

            if current_state:
                active_start = boundary
                active_samples = [boundary_sample, sample]

            else:
                active_samples.append(boundary_sample)

                windows.append(
                    _make_window(
                        active_start,
                        boundary,
                        active_samples,
                    )
                )

                active_start = None
                active_samples = []

        elif current_state and active_start is not None:
            active_samples.append(sample)

        current = next_time
        previous_state = current_state

    if active_start is not None:
        windows.append(
            _make_window(
                active_start,
                end_datetime,
                active_samples,
            )
        )

    return windows
