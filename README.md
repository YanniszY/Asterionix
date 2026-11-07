# Asterionix v0.1

A local-first, open-source astronomical observation planner. This first
prototype calculates basic positions for the Moon, Sun, and five naked-eye
planets, then performs a simple geometric scan for possible Moon observation
windows.

## Scope and limitations

This is an early working foundation, not a complete prediction of whether a
person will actually see an object. It currently does **not** account for:

- cloud cover or other weather;
- light pollution / sky brightness;
- mountains, buildings, trees, or other local obstructions;
- atmospheric extinction, transparency, or seeing;
- telescope/binocular specifications or an observer's eyesight.

A body being above the horizon is not by itself proof that it is observable.
The planner currently applies two simple conditions to the Moon: altitude at
least 10 degrees and Sun altitude at most -12 degrees. The scan uses
10-minute samples, so reported boundaries are approximate.

## Requirements

- Python 3.10+
- pip
- Internet access for the initial download of the ephemeris file (unless you
  already have it)

## Installation (Fedora / Linux)

```bash
git clone <your-repository-url>
cd Asterionix

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ephemeris data

Download the JPL DE440s file from the official NAIF/JPL archive:

https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de440s.bsp

Place it here:

```text
Asterionix/
└── data/
    └── de440s.bsp
```

The ephemeris file is intentionally excluded from Git because it is a large
external data asset. Keep the file locally; do not commit it unless you have a
specific reason and have checked repository size/licensing considerations.

## Run

Coordinates are decimal degrees. Date/time is interpreted as UTC. If omitted,
the current UTC time is used.

```bash
python main.py --latitude 50.4501 --longitude 30.5234
```

Choose a specific UTC time and planning horizon:

```bash
python main.py   --latitude 50.4501   --longitude 30.5234   --datetime 2026-11-07T20:00   --hours 24
```

Optional elevation:

```bash
python main.py --latitude 50.4501 --longitude 30.5234 --elevation 180
```

## Tests

```bash
pytest
```

## Project principles

- **Local-first:** coordinates are processed locally by this application.
- **Privacy-conscious:** this prototype has no account, telemetry, or network
  location lookup. The ephemeris is a local file.
- **Scientific calculations first:** deterministic astronomical calculations
  remain separate from any future AI recommendation layer.
- **AI later:** future AI components may help interpret conditions, analyze
  historical observation outcomes, and personalize recommendations. They
  must not replace or fabricate the underlying astronomical calculations.

## Roadmap

1. Validate and test the astronomical calculations.
2. Improve rise/set and observation-window calculations.
3. Add object catalogs and deep-sky objects.
4. Integrate weather and sky-brightness / light-pollution data sources.
5. Add equipment-aware visibility estimates.
6. Build a GUI.
7. Explore an AI-assisted recommendation and analysis layer.
