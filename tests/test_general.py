from functools import partial
import os
from pathlib import Path
import pytest
from cpymad_lhc import general
from cpymad.madx import Madx

from tests.conftest import MadxMock


EPS = 1e-12


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


def test_get_kqs():
    kqs_b1 = general.get_kqs_for_coupling_correction(beam=1)
    kqs_b2 = general.get_kqs_for_coupling_correction(beam=2)

    assert kqs_b1 != kqs_b2
    assert len(kqs_b1) == 12
    assert len(kqs_b2) == 12

    kqs_all = kqs_b1 + kqs_b2
    assert len(kqs_all) == len(set(kqs_all))  # all different

    for kqs in kqs_all:
        assert kqs.startswith("KQS.")
        assert kqs[-2] == "B"
        assert kqs[-1] in ("1", "2")

    kqs_nobeam = [kq[:-2] for kq in kqs_all]

    lhc_arcs = general.lhc_arcs()
    assert len(lhc_arcs) == 8

    for arc in lhc_arcs:
        assert f"KQS.A{arc}" in kqs_nobeam

    for side in ("L", "R"):
        for ip in range(1, 9):
            assert f"KQS.{side}{ip}" in kqs_nobeam


def test_get_knobs():
    coupling = general.get_coupling_knobs(accel="hllhc", beam=1, suffix="test")
    assert coupling == ("cmrskew", "cmiskew")

    for beam in (2, 4):
        coupling = general.get_coupling_knobs(accel="lhc", beam=beam, suffix="_test")
        for knob in coupling:
            assert knob.endswith("_test")
            assert "b2" in knob
            assert knob.startswith("cmis.") or knob.startswith("cmrs.")

    with pytest.raises(KeyError):
        general.get_coupling_knobs(accel="unknown", beam=1)


    tune_chroma = general.get_tune_and_chroma_knobs(accel="lhc", beam=1, suffix="test")
    assert len(tune_chroma) == 4
    for knob in tune_chroma:
        assert knob.endswith("test")
        assert "b1" in knob
        assert knob.startswith("dQ")

    tune_chroma = general.get_tune_and_chroma_knobs(accel="hllhc", beam=4, suffix="")
    assert len(tune_chroma) == 4
    for knob in tune_chroma:
        assert knob.endswith("b2")
        assert knob.startswith("kqt") or knob.startswith("ks")

    with pytest.raises(KeyError):
        general.get_tune_and_chroma_knobs(accel="unknown", beam=1)


def test_fractional_tune():
    assert general.fractional_tune(0.1) == 0.1
    assert abs(general.fractional_tune(62.54) - 0.54) < EPS


def test_move_sixtrack_output(tmp_path):
    outputdir = tmp_path / "output"
    outputdir.mkdir()

    madx = MadxMock()

    # Call function
    os.chdir(tmp_path)
    general.sixtrack_output(madx, energy=5050, outputdir=outputdir)

    assert madx.globals["VRF400"] == 16
    assert "LAGRF400.B1" in madx.globals
    assert "LAGRF400.B2" in madx.globals

    for i in range(3):
        assert (outputdir / f"fc{i}.out").exists()
        assert not (tmp_path / f"fc{i}.out").exists()
