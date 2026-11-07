"""Observer location and local horizon calculations."""

from skyfield.api import wgs84


class Observer:
    def __init__(self, ephemeris, latitude: float, longitude: float, elevation_m: float = 0):
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90 degrees.")
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180 degrees.")

        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.elevation_m = float(elevation_m)
        self.location = wgs84.latlon(
            self.latitude,
            self.longitude,
            elevation_m=self.elevation_m,
        )
        self.topos = ephemeris.earth + self.location
