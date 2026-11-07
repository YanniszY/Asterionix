"""Command-line interface for Asterionix v0.1."""

import argparse
from datetime import datetime, timezone

from asterionix.astronomy.ephemeris import Ephemeris
from asterionix.astronomy.observer import Observer
from asterionix.planner.observation import (
    build_report,
    get_moon_windows,
    get_moon_events,
)


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Asterionix — local astronomical observation planner"
    )
    parser.add_argument("--latitude", type=float, required=True, help="Observer latitude")
    parser.add_argument("--longitude", type=float, required=True, help="Observer longitude")
    parser.add_argument("--elevation", type=float, default=0, help="Elevation in metres")
    parser.add_argument(
        "--datetime",
        dest="datetime_text",
        help="UTC date/time, e.g. 2026-11-07T20:00. Defaults to current UTC time.",
    )
    parser.add_argument("--hours", type=int, default=24, help="Planning horizon in hours")
    return parser.parse_args()


def _format_utc(value):
    return value.strftime("%Y-%m-%d %H:%M UTC")


def main():
    args = _parse_args()

    if args.datetime_text:
        try:
            requested = datetime.fromisoformat(args.datetime_text)
        except ValueError as exc:
            raise SystemExit(f"Invalid --datetime value: {exc}")
        if requested.tzinfo is None:
            requested = requested.replace(tzinfo=timezone.utc)
        else:
            requested = requested.astimezone(timezone.utc)
    else:
        requested = datetime.now(timezone.utc)

    ephemeris = Ephemeris()
    observer = Observer(
        ephemeris,
        args.latitude,
        args.longitude,
        args.elevation,
    )
    time = ephemeris.timescale.from_datetime(requested)

    report = build_report(ephemeris, observer, time)

    print("\n" + "=" * 58)
    print("ASTERIONIX v0.1 — OBSERVATION REPORT")
    print("=" * 58)
    print(f"Location: {args.latitude:.4f}, {args.longitude:.4f} ({args.elevation:.0f} m)")
    print(f"Time:     {_format_utc(requested)}")
    print("\nMOON")
    moon = report["moon"]
    print(f"  Altitude:       {moon['altitude_deg']:.2f}°")
    print(f"  Azimuth:        {moon['azimuth_deg']:.2f}°")
    print(f"  Distance:       {moon['distance_km']:,.0f} km")
    print(f"  Illuminated:    {moon['percentage']:.1f}%")
    print(f"  Above horizon:  {'yes' if moon['above_horizon'] else 'no'}")
    print("\nSUN / SKY")
    sun = report["sun"]
    print(f"  Solar altitude: {sun['altitude_deg']:.2f}°")
    print(f"  Sky state:      {sun['state'].replace('_', ' ')}")

    print("\nPLANETS")
    for name, values in report["planets"].items():
        status = "above horizon" if values["above_horizon"] else "below horizon"
        print(
            f"  {name:<8} alt {values['altitude_deg']:>7.2f}° | "
            f"az {values['azimuth_deg']:>7.2f}° | {status}"
        )

    print(f"\nMOON OBSERVATION WINDOWS (next {args.hours} hours)")
    windows = get_moon_windows(ephemeris, observer, time, hours=args.hours)
    if not windows:
        print("  No sampled intervals meet the current geometric criteria.")
    else:
        for window in windows:
            print(
                f"  {_format_utc(window['start_utc'])} — "
                f"{_format_utc(window['end_utc'])} | "
                f"peak altitude {window['peak_altitude_deg']:.1f}°"
            )
            
            
    
    
    print(f"\nMOONRISE / MOONSET (next {args.hours} hours)")

    moon_events = get_moon_events(
        ephemeris,
        observer,
        time,
        hours=args.hours,
    )

    if not moon_events:
        print("  No moonrise or moonset found in this period.")
    else:
        for event in moon_events:
            event_time = event["time"].utc_datetime()
            formatted_time = event_time.strftime("%Y-%m-%d %H:%M UTC")

            print(f"  {event['type']:<8} {formatted_time}")
    
    
    
    

    print("\nLimitations:")
    print("  This version uses geometry only. It does not yet model weather,")
    print("  light pollution, terrain/buildings, atmospheric extinction, or optics.")
    print("  Observation windows are approximate and use 10-minute sampling.")
    print("=" * 58)


if __name__ == "__main__":
    main()
