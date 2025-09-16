import pytest
from cpymad_lhc.ir_orbit import orbit_setup, get_current_orbit_scheme, check_crabbing
from tests.conftest import MadxMock, silence_stdout
from cpymad.madx import Madx


def test_orbit_setup():
    madx = MadxMock()

    # ----- Test Flat
    madx.globals = {}
    orbit_setup(madx, "lhc", 2018, scheme="flat")
    assert len(madx.globals) > 12

    all_numbers = [v for v in madx.globals.values() if isinstance(v, int | float)]
    all_strings = [v for v in madx.globals.values() if isinstance(v, str)]

    assert len(all_numbers) + len(all_strings) == len(madx.globals)
    assert all(v == 0 for v in all_numbers)

    assert "on_x1_v" not in madx.globals
    assert "on_x1" in madx.globals

    # ----- Test Flat with on_x1_v
    madx.globals = {}
    orbit_setup(madx, "lhc", 2022, scheme="flat", on_x1_v=122)
    assert "on_x5_h" in madx.globals
    assert "on_x5" not in madx.globals
    assert madx.globals["on_x1_v"] == 122

    # ----- Test top with wrong key
    madx.globals = {}
    orbit_setup(madx, "lhc", 2022, scheme="top", on_x1=1000)
    assert "on_x1_v" in madx.globals
    assert "on_x1" not in madx.globals

    # ----- Test hllhc top with right key
    madx.globals = {}
    orbit_setup(madx, "hllhc", 2022, scheme="top", on_x1=1000, on_alice=1)
    assert "on_x1_v" not in madx.globals
    assert "on_x1" in madx.globals
    assert madx.globals["on_x1"] == 1000
    assert madx.globals["on_alice"] == 1
    assert "on_crab1" in madx.globals
    assert "on_crab5" in madx.globals


def test_get_current_crossing_scheme():  # capsys to suppress madx-output
    with silence_stdout():
        madx = Madx()

    old_globals = list(madx.globals)
    orbit_setup(madx, "lhc", 2022, scheme="flat", on_x1_v=122)
    scheme = get_current_orbit_scheme(madx, "lhc", 2022)

    for key in madx.globals:
        if key in old_globals:
            continue
        assert madx.globals[key] == scheme[key]

def test_check_crabbing(caplog):
    madx = MadxMock()
    orbit_setup(madx, "hllhc", 2022, scheme="flat", on_x1=-10, on_crab1=12, on_crab5=-15, on_x5=15)

    with pytest.raises(ValueError):
        check_crabbing(madx, auto_set=False)

    caplog.clear()
    check_crabbing(madx, auto_set=True)
    assert madx.globals["on_crab1"] == 10
    assert madx.globals["on_crab5"] == -15
    assert "Limiting on_crab1" in caplog.text
    assert "on_crab5" not in caplog.text

    caplog.clear()
    orbit_setup(madx, "hllhc", 2022, scheme="flat", on_x1=-10, on_crab1=6, on_crab5=-15, on_x5=4)
    check_crabbing(madx, auto_set=True)
    assert madx.globals["on_crab1"] == 6
    assert madx.globals["on_crab5"] == -4
    assert "Limiting on_crab5" in caplog.text
    assert "on_crab1" not in caplog.text

    caplog.clear()
    orbit_setup(madx, "hllhc", 2022, scheme="flat", on_x1=-10, on_crab1=-20, on_crab5=10, on_x5=4)
    check_crabbing(madx, auto_set=True)
    assert madx.globals["on_crab1"] == -10
    assert madx.globals["on_crab5"] == 4
    assert "Limiting on_crab1" in caplog.text
    assert "Limiting on_crab5" in caplog.text
