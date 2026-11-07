from datetime import datetime, timedelta, timezone

from asterionix.planner import visibility


class DummyTime:
    def __init__(self, dt):
        self.dt = dt

    def utc_datetime(self):
        return self.dt


class DummyEphemeris:
    pass


class DummyObserver:
    pass


def run_visibility(monkeypatch, intervals):
    """Run visibility planner with artificial observation intervals."""

    base_time = datetime(2026, 11, 7, tzinfo=timezone.utc)

    def fake_evaluate(
        ephemeris,
        observer,
        body,
        dt,
        minimum_altitude_deg,
        maximum_sun_altitude_deg,
    ):
        suitable = any(
            start <= dt < end
            for start, end in intervals
        )

        return {
            "time": dt,
            "target_altitude_deg": 30.0 if suitable else -5.0,
            "sun_altitude_deg": -15.0 if suitable else 10.0,
            "suitable": suitable,
        }

    monkeypatch.setattr(visibility, "_evaluate", fake_evaluate)

    return visibility.find_observation_windows(
        ephemeris=DummyEphemeris(),
        observer=DummyObserver(),
        body=None,
        start_time=DummyTime(base_time),
        hours=1,
        step_minutes=10,
    )


def test_no_observation_windows(monkeypatch):
    windows = run_visibility(monkeypatch, [])

    assert windows == []


def test_full_observation_window(monkeypatch):
    base = datetime(2026, 11, 7, tzinfo=timezone.utc)

    windows = run_visibility(
        monkeypatch,
        [(base, base + timedelta(hours=1))],
    )

    assert len(windows) == 1
    assert windows[0]["start_utc"] == base
    expected_end = base + timedelta(hours=1)

    assert abs(
        (windows[0]["end_utc"] - expected_end).total_seconds()
    ) <= 1


def test_finds_window_inside_period(monkeypatch):
    base = datetime(2026, 11, 7, tzinfo=timezone.utc)

    expected_start = base + timedelta(minutes=3)
    expected_end = base + timedelta(minutes=27)

    windows = run_visibility(
        monkeypatch,
        [(expected_start, expected_end)],
    )

    assert len(windows) == 1

    assert abs(
        (windows[0]["start_utc"] - expected_start).total_seconds()
    ) <= 1

    assert abs(
        (windows[0]["end_utc"] - expected_end).total_seconds()
    ) <= 1


def test_finds_multiple_windows(monkeypatch):
    base = datetime(2026, 11, 7, tzinfo=timezone.utc)

    intervals = [
        (
            base + timedelta(minutes=5),
            base + timedelta(minutes=15),
        ),
        (
            base + timedelta(minutes=35),
            base + timedelta(minutes=55),
        ),
    ]

    windows = run_visibility(monkeypatch, intervals)

    assert len(windows) == 2


def test_window_reaches_end_of_period(monkeypatch):
    base = datetime(2026, 11, 7, tzinfo=timezone.utc)

    windows = run_visibility(
        monkeypatch,
        [(base + timedelta(minutes=30), base + timedelta(hours=1))],
    )

    assert len(windows) == 1
    expected_end = base + timedelta(hours=1)

    assert abs(
        (windows[0]["end_utc"] - expected_end).total_seconds()
    ) <= 1