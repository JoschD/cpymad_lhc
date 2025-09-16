
import os
import sys
from contextlib import contextmanager
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


@contextmanager
def silence_stdout():
    old_target = sys.stdout
    try:
        with Path(os.devnull).open("w") as new_target:
            sys.stdout = new_target
            yield new_target
    finally:
        sys.stdout = old_target
