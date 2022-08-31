import pytest
import tempfile

from pathlib import Path

import renameat2


def test_exchange():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        apple_path = tmp.joinpath("apple")
        with open(apple_path, "w") as apple_out:
            apple_out.write("apple")

        orange_path = tmp.joinpath("orange")
        with open(orange_path, "w") as apple_out:
            apple_out.write("orange")

        renameat2.exchange(apple_path, orange_path)

        with open(apple_path) as apple_in:
            assert apple_in.read() == "orange"

        with open(orange_path) as orange_in:
            assert orange_in.read() == "apple"


def test_rename_replace():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        apple_path = tmp.joinpath("apple")
        with open(apple_path, "w") as apple_out:
            apple_out.write("apple")

        orange_path = tmp.joinpath("orange")
        with open(orange_path, "w") as apple_out:
            apple_out.write("orange")

        renameat2.rename(apple_path, orange_path, replace=True)

        assert not apple_path.exists()

        with open(orange_path) as orange_in:
            assert orange_in.read() == "apple"


def test_rename_noreplace():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        apple_path = tmp.joinpath("apple")
        with open(apple_path, "w") as apple_out:
            apple_out.write("apple")

        orange_path = tmp.joinpath("orange")
        with open(orange_path, "w") as apple_out:
            apple_out.write("orange")

        with pytest.raises(OSError):
            renameat2.rename(apple_path, orange_path, replace=False)

        assert apple_path.exists()
        assert orange_path.exists()


def test_rename_whiteout():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        apple_path = tmp.joinpath("apple")
        with open(apple_path, "w") as apple_out:
            apple_out.write("apple")

        orange_path = tmp.joinpath("orange")
        with open(orange_path, "w") as apple_out:
            apple_out.write("orange")

        try:
            renameat2.rename(apple_path, orange_path, whiteout=True)
        except:
            raise RuntimeError(f"apple_path = {apple_path} orange_path = {orange_path}")

        assert apple_path.is_char_device()

        with open(orange_path) as orange_in:
            assert orange_in.read() == "apple"
