from cpymad_lhc import general


class MADXMock:
    def __init__(self):
        self.globals = {}
        self.sequence = {}


def test_lhc_sequence_names():
    name, file, bv = general.get_lhc_sequence_filename_and_bv(beam=1)
    assert file == "lhc_as_built.seq"
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
    madx = MADXMock()

    general.switch_magnetic_errors(madx, default=True)
    assert madx.globals["on_A10s"]
    assert madx.globals["on_A2r"]
    assert madx.globals["on_B6s"]
    assert madx.globals["on_B3r"]
    madx.globals = {}

    general.switch_magnetic_errors(madx, default=False)
    assert not madx.globals["on_A9s"]
    assert not madx.globals["on_A1r"]
    assert not madx.globals["on_B15s"]
    assert not madx.globals["on_B4r"]
    madx.globals = {}

    general.switch_magnetic_errors(madx, default=True, A10s=False, B6r=False)
    assert madx.globals["on_A10s"] is False
    assert madx.globals["on_A2r"]
    assert madx.globals["on_B6r"] is False
    assert madx.globals["on_B3r"]
    madx.globals = {}

    general.switch_magnetic_errors(madx, default=False, AB9=True, B15=True)
    assert madx.globals["on_A9s"]
    assert madx.globals["on_A9r"]
    assert madx.globals["on_B9s"]
    assert madx.globals["on_B9r"]
    assert madx.globals["on_B15s"]
    assert madx.globals["on_B15r"]
    assert not madx.globals["on_A1r"]
    assert not madx.globals["on_B4r"]
    madx.globals = {}
