import json
import tempfile
from pathlib import Path

from file_org.organiser import classify, organise


def test_classify():
    assert classify(".jpg") == "Images"
    assert classify(".MP4") == "Video"
    assert classify(".zip") == "Archives"
    assert classify(".py") == "Code"
    assert classify(".unknown") == "Misc"


def test_organise_moves_files():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "photo.jpg").touch()
        (d / "doc.pdf").touch()

        result = organise(d)

        assert len(result.moved) == 2
        assert (d / "Images" / "photo.jpg").exists()
        assert (d / "Documents" / "doc.pdf").exists()


def test_organise_dry_run():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "photo.jpg").touch()

        result = organise(d, dry_run=True)

        assert len(result.moved) == 1
        assert not (d / "Images" / "photo.jpg").exists()


def test_organise_undo():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "photo.jpg").touch()

        organise(d)
        assert (d / "Images" / "photo.jpg").exists()

        result = organise(d, undo=True)
        assert len(result.moved) == 1
        assert (d / "photo.jpg").exists()
        assert not (d / "Images" / "photo.jpg").exists()


def test_skip_existing():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "photo.jpg").touch()
        (d / "Images").mkdir()
        (d / "Images" / "photo.jpg").touch()

        result = organise(d)
        assert len(result.skipped) == 1
