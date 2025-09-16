
from pathlib import Path


class MadxMock:
    def __init__(self):
        self.globals = {}
        self.run_twiss = False

    def twiss(self):
        self.run_twiss = True

    def sixtrack(self, **kwargs):
        for i in range(3):
            (Path() / f"fc{i}.out").touch()
        assert "radius" in kwargs
        assert kwargs["cavall"]
