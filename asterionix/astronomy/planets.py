"""Position calculations for the five naked-eye planets."""

class Planets:
    def __init__(self, ephemeris, observer):
        self.ephemeris = ephemeris
        self.observer = observer

    def get_positions(self, time):
        results = {}
        for name, body in self.ephemeris.bodies.items():
            apparent = self.observer.topos.at(time).observe(body).apparent()
            altitude, azimuth, distance = apparent.altaz()
            results[name] = {
                "altitude_deg": float(altitude.degrees),
                "azimuth_deg": float(azimuth.degrees),
                "distance_au": float(distance.au),
                "above_horizon": bool(altitude.degrees > 0),
            }
        return results
