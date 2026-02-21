"""Tests for file-related utilities."""

import csv
import datetime
import json
from unittest.mock import patch

import pytest

from pactole.utils import File, FileType


class TestFileType:
    """Tests for FileType."""

    def test_get(self):
        """Test FileType.get behavior."""

        assert FileType.get(FileType.CSV) is FileType.CSV
        assert FileType.get(".json") is FileType.JSON
        assert FileType.get("TXT") is FileType.TEXT
        assert FileType.get("unknown") is FileType.TEXT


class TestFile:
    """Tests for File."""

    def test_file_infers_type_from_path(self, tmp_path):
        """Test that File infers type from the path suffix."""

        file_path = tmp_path / "data.csv"
        file_obj = File(file_path)

        assert file_obj.type is FileType.CSV

    def test_file_path_and_encoding_properties(self, tmp_path):
        """Test path and encoding properties."""

        file_path = tmp_path / "note.txt"
        file_obj = File(file_path, encoding="latin-1")

        assert file_obj.path == file_path
        assert file_obj.encoding == "latin-1"

    def test_file_exists_size_date(self, tmp_path):
        """Test exists, size, and date properties."""

        file_path = tmp_path / "note.txt"
        file_obj = File(file_path)
        file_obj.write("content")

        assert file_obj.exists() is True
        assert file_obj.size() > 0
        file_date = file_obj.date()

        assert isinstance(file_date, datetime.datetime)
        assert file_date.timestamp() > 0

    def test_file_size_missing_file(self, tmp_path):
        """Test size returns zero when the file is missing."""

        file_obj = File(tmp_path / "missing.txt")

        assert file_obj.size() == 0

    def test_file_read_write_text(self, tmp_path):
        """Test writing and reading text content."""

        file_path = tmp_path / "note.txt"
        file_obj = File(file_path)
        file_obj.write("hello\nworld")

        assert file_obj.read() == "hello\nworld"
        assert list(file_obj.readlines()) == ["hello", "world"]

    def test_file_read_write_json(self, tmp_path):
        """Test writing and reading JSON content."""

        file_path = tmp_path / "data.json"
        file_obj = File(file_path)
        payload = {"key": "value", "items": [1, 2, 3]}
        file_obj.write(payload)

        assert file_obj.read() == payload

    def test_file_read_write_csv(self, tmp_path):
        """Test writing and reading CSV content."""

        file_path = tmp_path / "data.csv"
        file_obj = File(file_path)
        rows = [{"col1": "1", "col2": "2"}, {"col1": "3", "col2": "4"}]
        file_obj.write(rows)

        assert file_obj.read() == rows
        assert list(file_obj.readlines()) == rows

    def test_file_missing_read_behaviors(self, tmp_path):
        """Test read and readlines when the file does not exist."""

        file_obj = File(tmp_path / "missing.txt")

        assert file_obj.read(throw=False) is None
        assert not list(file_obj.readlines(throw=False))
        with pytest.raises(FileNotFoundError):
            file_obj.read()
        with pytest.raises(FileNotFoundError):
            list(file_obj.readlines())

    def test_file_json_decode_error(self, tmp_path):
        """Test JSON decoding error handling."""

        file_path = tmp_path / "bad.json"
        file_path.write_text('{"key":', encoding="utf-8")
        file_obj = File(file_path, file_type="json")

        assert file_obj.read(throw=False) is None
        with pytest.raises(IOError):
            file_obj.read()

    def test_file_read_csv_error(self, tmp_path):
        """Test CSV read error handling with patching."""

        file_path = tmp_path / "data.csv"
        file_path.write_text("col1,col2\n1,2", encoding="utf-8")
        file_obj = File(file_path)

        with patch("pactole.utils.file.read_csv_file", side_effect=csv.Error("bad csv")):
            assert file_obj.read(throw=False) is None

        with patch("pactole.utils.file.read_csv_file", side_effect=csv.Error("bad csv")):
            with pytest.raises(IOError):
                file_obj.read()

    def test_file_readlines_csv_error(self, tmp_path):
        """Test CSV readlines error handling."""

        file_path = tmp_path / "data.csv"
        file_path.write_text("col1,col2\n1,2", encoding="utf-8")
        file_obj = File(file_path)

        with patch("pactole.utils.file.read_csv_file", side_effect=csv.Error("bad csv")):
            assert not list(file_obj.readlines(throw=False))

        with patch("pactole.utils.file.read_csv_file", side_effect=csv.Error("bad csv")):
            with pytest.raises(IOError):
                list(file_obj.readlines())

    def test_file_write_csv_error(self, tmp_path):
        """Test CSV write error handling."""

        file_path = tmp_path / "data.csv"
        file_obj = File(file_path)
        rows = [{"col1": "1", "col2": "2"}]

        with patch("pactole.utils.file.write_csv_file", side_effect=csv.Error("bad csv")):
            file_obj.write(rows, throw=False)

        with patch("pactole.utils.file.write_csv_file", side_effect=csv.Error("bad csv")):
            with pytest.raises(IOError):
                file_obj.write(rows)

    def test_file_write_json_error(self, tmp_path):
        """Test JSON write error handling."""

        file_path = tmp_path / "data.json"
        file_obj = File(file_path)
        payload = {"key": "value"}

        with patch(
            "pactole.utils.file.write_json_file",
            side_effect=json.JSONDecodeError("msg", "doc", 0),
        ):
            file_obj.write(payload, throw=False)

        with patch(
            "pactole.utils.file.write_json_file",
            side_effect=json.JSONDecodeError("msg", "doc", 0),
        ):
            with pytest.raises(IOError):
                file_obj.write(payload)

    def test_file_delete_existing(self, tmp_path):
        """Test deleting an existing file."""

        file_path = tmp_path / "note.txt"
        file_obj = File(file_path)
        file_obj.write("content")

        file_obj.delete()

        assert file_obj.exists() is False

    def test_file_delete_missing_no_throw(self, tmp_path):
        """Test deleting a missing file with throw=False."""

        file_obj = File(tmp_path / "missing.txt")

        file_obj.delete(throw=False)

        assert file_obj.exists() is False

    def test_file_delete_missing_raises(self, tmp_path):
        """Test deleting a missing file with throw=True."""

        file_obj = File(tmp_path / "missing.txt")

        with pytest.raises(FileNotFoundError):
            file_obj.delete()

    def test_file_open_creates_parent(self, tmp_path):
        """Test opening a file for writing creates parent directories."""

        file_path = tmp_path / "nested" / "note.txt"
        file_obj = File(file_path)
        with file_obj.open("w") as handle:
            handle.write("content")

        assert file_path.exists()
        assert file_path.read_text(encoding="utf-8") == "content"
