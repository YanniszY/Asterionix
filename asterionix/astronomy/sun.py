"""Solar altitude and twilight calculations."""

from skyfield import almanac


class Sun:
    def __init__(self, ephemeris, observer):
        self.ephemeris = ephemeris
        self.observer = observer

    def get_position(self, time):
        apparent = self.observer.topos.at(time).observe(self.ephemeris.sun).apparent()
        altitude, azimuth, distance = apparent.altaz()
        return {
            "altitude_deg": float(altitude.degrees),
            "azimuth_deg": float(azimuth.degrees),
            "distance_au": float(distance.au),
        }

    def get_sun_altitude(self, time):
        return self.get_position(time)["altitude_deg"]

    def get_twilight_state(self, time):
        altitude = self.get_sun_altitude(time)
        if altitude >= 0:
            state = "daylight"
        elif altitude >= -6:
            state = "civil_twilight"
        elif altitude >= -12:
            state = "nautical_twilight"
        elif altitude >= -18:
            state = "astronomical_twilight"
        else:
            state = "astronomical_night"
        return {"altitude_deg": altitude, "state": state}
