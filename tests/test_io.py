from pathlib import Path

from cpymad_lhc.io import PathContainer

THIS_DIR  = Path(__file__)

def test_path_container():
    class Paths(PathContainer):
        this: Path = Path(__file__)

    assert Paths.this == THIS_DIR
    assert Paths.get("this", "inputs") == THIS_DIR / "inputs"
    assert Paths.str("this") == str(THIS_DIR)
    assert Paths.str("this", "inputs", "other") == str(THIS_DIR / "inputs" / "other")
