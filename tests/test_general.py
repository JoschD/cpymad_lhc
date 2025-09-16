from cpymad_lhc import general
from cpymad.madx import Madx

class MadxMock:
    def __init__(self):
        self.globals = {}


def test_lhc_sequence_names():
    name, file, bv = general.get_lhc_sequence_filename_and_bv(beam=1)
    assert file == "lhc_as-built.seq"
    assert name == "lhcb1"
    assert bv == 1

    name, file, bv = general.get_lhc_sequence_filename_and_bv(beam=2, accel="hllhc")
    assert file == "lhc.seq"
    assert name == "lhcb2"
    assert bv == -1

    name, file, bv = general.get_lhc_sequence_filename_and_bv(beam=4, accel="hllhc")
    assert file == "lhcb4.seq"
    assert name == "lhcb2"
    assert bv == 1


def test_switch_magnetic_errors():

    madx = MadxMock()

    general.switch_magnetic_errors(madx, default=True)
    assert madx.globals["ON_A10s"]
    assert madx.globals["ON_A2r"]
    assert madx.globals["ON_B6s"]
    assert madx.globals["ON_B3r"]
    madx.globals = {}

    general.switch_magnetic_errors(madx, default=False)
    assert not madx.globals["ON_A9s"]
    assert not madx.globals["ON_A1r"]
    assert not madx.globals["ON_B15s"]
    assert not madx.globals["ON_B4r"]
    madx.globals = {}

    general.switch_magnetic_errors(madx, default=True, A10s=False, B6r=False)
    assert not madx.globals["ON_A10s"]
    assert madx.globals["ON_A2r"]
    assert not madx.globals["ON_B6r"]
    assert madx.globals["ON_B3r"]
    madx.globals = {}

    general.switch_magnetic_errors(madx, default=False, AB9=True, B15=True)
    assert madx.globals["ON_A9s"]
    assert madx.globals["ON_A9r"]
    assert madx.globals["ON_B9s"]
    assert madx.globals["ON_B9r"]
    assert madx.globals["ON_B15s"]
    assert madx.globals["ON_B15r"]
    assert not madx.globals["ON_A1r"]
    assert not madx.globals["ON_B4r"]
    madx.globals = {}


def test_add_expression():
    madx = Madx()

    madx.globals["A"] = "C"
    assert madx.globals["A"] == 0

    madx.globals["C"] = 5
    assert madx.globals["A"] == 5

    general.add_expression(madx, "A", "2")
    assert madx.globals["A"] == 7

    general.add_expression(madx, "B", "A + 2")
    assert madx.globals["B"] == 9

    general.add_expression(madx, "B", "C*2")
    assert madx.globals["B"] == 19


def test_disable_errors():
    madx = MadxMock()

    a = 1
    b = 10

    madx.globals["A"] = a
    madx.globals["B"] = b

    with general.temp_disable_errors(madx, "A", "B"):
        assert madx.globals["A"] == 0
        assert madx.globals["B"] == 0

    assert madx.globals["A"] == a
    assert madx.globals["B"] == b


def test_get_k_strings():
    k = general.get_k_strings()
    assert "K7L" in k
    assert "K0SL" in k
    assert len(k) == 2 * 8  # 8 normal + 8 skew

    k = general.get_k_strings(start=3, stop=5, orientation="skew")
    assert k == ["K3SL", "K4SL"]
