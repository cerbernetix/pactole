"""Unit tests for FileCache class."""

import datetime
import json
import os
from unittest.mock import Mock

import pytest

from pactole.utils import FileCache, FileType


class TestFileCache:
    """Tests for FileCache class."""

    def test_init_sets_file_path_and_type_csv(self, tmp_path):
        """Test that CSV extension selects CSV file type."""

        file_path = tmp_path / "data.csv"
        cache = FileCache(file_path)

        assert cache.path == file_path
        assert cache.type == FileType.CSV

    def test_init_sets_file_type_json(self, tmp_path):
        """Test that JSON extension selects JSON file type."""

        cache = FileCache(tmp_path / "data.json")

        assert cache.type == FileType.JSON

    def test_init_sets_file_type_text_for_unknown_extension(self, tmp_path):
        """Test that unknown extensions are treated as text."""

        cache = FileCache(tmp_path / "data.log")

        assert cache.type == FileType.TEXT

    def test_exists_false_when_missing(self, tmp_path):
        """Test exists is False when file does not exist."""

        cache = FileCache(tmp_path / "missing.json")

        assert cache.exists() is False

    def test_exists_true_after_write(self, tmp_path):
        """Test exists is True after writing to the cache file."""

        cache = FileCache(tmp_path / "data.json")

        assert cache.exists() is False

        cache.set({"value": 1})

        assert cache.exists() is True

    def test_date_returns_file_timestamp(self, tmp_path):
        """Test date returns the file modification datetime."""

        file_path = tmp_path / "note.txt"
        cache = FileCache(file_path)
        cache.set("hello")
        fixed_time = datetime.datetime(2024, 1, 1, 12, 0, 0)
        fixed_timestamp = fixed_time.timestamp()
        os.utime(file_path, (fixed_timestamp, fixed_timestamp))

        file_date = cache.date()

        assert isinstance(file_date, datetime.datetime)
        assert file_date.timestamp() == pytest.approx(fixed_timestamp)

    def test_size_returns_file_size(self, tmp_path):
        """Test size returns the file size in bytes."""

        file_path = tmp_path / "note.txt"
        cache = FileCache(file_path)
        cache.set("hello")

        assert cache.size() == 5

    def test_load_returns_none_when_file_missing(self, tmp_path):
        """Test load returns None if file does not exist."""

        cache = FileCache(tmp_path / "missing.json")

        assert cache.load() is None
        assert cache.data is None

    def test_load_reads_csv_file(self, tmp_path):
        """Test load reads CSV file as list of dicts."""

        file_path = tmp_path / "data.csv"
        file_path.write_text("col1,col2\n1,2\n3,4\n", encoding="utf-8")
        cache = FileCache(file_path)

        result = cache.load()

        assert result == [{"col1": "1", "col2": "2"}, {"col1": "3", "col2": "4"}]

    def test_load_reads_json_file(self, tmp_path):
        """Test load reads JSON file."""

        file_path = tmp_path / "data.json"
        payload = {"key": "value", "items": [1, 2, 3]}
        file_path.write_text(json.dumps(payload), encoding="utf-8")
        cache = FileCache(file_path)

        result = cache.load()

        assert result == payload

    def test_load_reads_text_file(self, tmp_path):
        """Test load reads text file."""

        file_path = tmp_path / "note.txt"
        file_path.write_text("hello world", encoding="utf-8")
        cache = FileCache(file_path)

        result = cache.load()

        assert result == "hello world"

    def test_load_applies_transformer(self, tmp_path):
        """Test load applies the transformer to the file data."""

        file_path = tmp_path / "data.json"
        file_path.write_text(json.dumps({"items": [1, 2, 3]}), encoding="utf-8")
        cache = FileCache(file_path, transformer=lambda data: data["items"])

        result = cache.load()

        assert result == [1, 2, 3]

    def test_load_raw_reads_file_without_transformer(self, tmp_path):
        """Test load_raw returns file content without applying the transformer."""

        file_path = tmp_path / "data.json"
        payload = {"items": [1, 2, 3]}
        file_path.write_text(json.dumps(payload), encoding="utf-8")
        transformer = Mock(side_effect=lambda data: data["items"])
        cache = FileCache(file_path, transformer=transformer)

        result = cache.load_raw()

        assert result == payload
        transformer.assert_not_called()

    def test_load_raw_returns_none_when_file_missing(self, tmp_path):
        """Test load_raw returns None if file does not exist."""

        cache = FileCache(tmp_path / "missing.json", transformer=Mock())

        assert cache.load_raw() is None

    def test_load_invokes_transformer_only_on_refresh(self, tmp_path):
        """Test transformer is called only when a refresh is needed."""

        file_path = tmp_path / "data.json"
        file_path.write_text(json.dumps({"value": 1}), encoding="utf-8")
        transformer = Mock(side_effect=lambda data: {"value": data["value"] + 1})
        cache = FileCache(file_path, transformer=transformer)

        first = cache.load()
        second = cache.load()
        file_path.write_text(json.dumps({"value": 2}), encoding="utf-8")
        forced = cache.load(force=True)

        assert first == {"value": 2}
        assert second == {"value": 2}
        assert forced == {"value": 3}
        assert transformer.call_count == 2

    def test_set_writes_csv_file(self, tmp_path):
        """Test set writes CSV data to file."""

        file_path = tmp_path / "data.csv"
        cache = FileCache(file_path)
        data = [{"col1": "1", "col2": "2"}, {"col1": "3", "col2": "4"}]

        cache.set(data)

        assert cache.data == data
        assert file_path.read_text(encoding="utf-8") == "col1,col2\n1,2\n3,4\n"

    def test_set_writes_json_file(self, tmp_path):
        """Test set writes JSON data to file."""

        file_path = tmp_path / "data.json"
        cache = FileCache(file_path)
        data = {"key": "value"}

        cache.set(data)

        assert cache.data == data
        assert json.loads(file_path.read_text(encoding="utf-8")) == data

    def test_set_writes_text_file(self, tmp_path):
        """Test set writes text data to file."""

        file_path = tmp_path / "note.txt"
        cache = FileCache(file_path)

        cache.set("hello world")

        assert cache.data == "hello world"
        assert file_path.read_text(encoding="utf-8") == "hello world"

    def test_load_uses_cache_until_forced(self, tmp_path):
        """Test load returns cached data unless force=True."""

        file_path = tmp_path / "data.json"
        cache = FileCache(file_path)

        file_path.write_text(json.dumps({"value": 1}), encoding="utf-8")
        first = cache.load()

        file_path.write_text(json.dumps({"value": 2}), encoding="utf-8")
        second = cache.load()
        forced = cache.load(force=True)

        assert first == {"value": 1}
        assert second == {"value": 1}
        assert forced == {"value": 2}

    def test_clear_removes_file_and_cache(self, tmp_path):
        """Test clear removes the file and resets cached data."""

        file_path = tmp_path / "data.json"
        file_path.write_text(json.dumps({"value": 1}), encoding="utf-8")
        cache = FileCache(file_path)

        cache.load()
        cache.clear()

        assert cache.data is None
        assert not file_path.exists()

    def test_clear_returns_none_on_reload_without_file(self, tmp_path):
        """Test load after clear returns None because file was removed."""

        file_path = tmp_path / "data.json"
        file_path.write_text(json.dumps({"value": 1}), encoding="utf-8")
        cache = FileCache(file_path)

        cache.load()
        cache.clear()
        reloaded = cache.load()

        assert reloaded is None

    def test_clear_with_missing_file_keeps_cache_reset(self, tmp_path):
        """Test clear works when the file does not exist."""

        file_path = tmp_path / "missing.json"
        cache = FileCache(file_path)

        cache.set({"value": 1})
        assert file_path.exists()

        file_path.unlink()
        cache.clear()

        assert cache.data is None
        assert not file_path.exists()
