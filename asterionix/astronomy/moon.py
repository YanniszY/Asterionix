"""Moon-specific calculations."""

from skyfield import almanac


class Moon:
    def __init__(self, ephemeris, observer):
        self.ephemeris = ephemeris
        self.observer = observer

    def get_position(self, time):
        astrometric = self.observer.topos.at(time).observe(self.ephemeris.moon)
        apparent = astrometric.apparent()
        altitude, azimuth, distance = apparent.altaz()

        return {
            "altitude_deg": float(altitude.degrees),
            "azimuth_deg": float(azimuth.degrees),
            "distance_km": float(distance.km),
        }

    def get_illumination(self, time):
        fraction = float(almanac.fraction_illuminated(
            self.ephemeris.data, "moon", time
        ))

        return {
            "fraction": fraction,
            "percentage": fraction * 100.0,
        }
