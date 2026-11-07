"""Load the JPL ephemeris and Skyfield time scale."""

from pathlib import Path

from skyfield.api import Loader


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
EPHEMERIS_PATH = DATA_DIR / "de440s.bsp"


class Ephemeris:
    """A single shared source of astronomical data."""

    def __init__(self, path: Path = EPHEMERIS_PATH):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.path = Path(path)

        if not self.path.exists():
            raise FileNotFoundError(
                f"Ephemeris file not found: {self.path}\n"
                "Download de440s.bsp and place it in the project's data/ folder.\n"
                "See README.md for instructions."
            )

        loader = Loader(str(DATA_DIR))
        self.timescale = loader.timescale()
        self.data = loader(str(self.path))
        self.earth = self.data["earth"]
        self.moon = self.data["moon"]
        self.sun = self.data["sun"]

        self.bodies = {
            "Mercury": self.data["mercury"],
            "Venus": self.data["venus"],
            "Mars": self.data["mars barycenter"],
            "Jupiter": self.data["jupiter barycenter"],
            "Saturn": self.data["saturn barycenter"],
        }
