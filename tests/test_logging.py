from cpymad.madx import Madx

from cpymad_lhc.logging import cpymad_logging_setup


def test_logging(tmp_path, capsys):
    commands = tmp_path / "commands.log"
    full_output = tmp_path / "full_output.log"
    output = tmp_path / "output.log"

    # Run Some Madx Code ---------------------
    madx = Madx(**cpymad_logging_setup(
        command_log=commands,
        full_log=full_output,
        output_log=output
    ))

    madx.globals["A"] = 1
    madx.globals["A"] = 2

    # Expected Outputs ---

    header_checks = (
        "MAD-X",
        "++++++++",
        "mad@cern.ch",
    )

    command_checks = (
        "A = 1;",
        "A = 2;",
    )

    out_checks = (
        "info: a redefined",
    )

    # Test Files ---------------------

    assert commands.exists()
    assert full_output.exists()
    assert output.exists()

    # Test Output ---------------------

    stdout = capsys.readouterr().out
    full = full_output.read_text()
    commands = commands.read_text()
    output = output.read_text()

    for check in header_checks:
        assert check in stdout
        assert check in full
        assert check not in commands
        assert check in output

    for check in command_checks:
        assert check in stdout
        assert check in full
        assert check in commands
        assert check not in output

    for check in out_checks:
        assert check in stdout
        assert check in full
        assert check not in commands
        assert check in output
