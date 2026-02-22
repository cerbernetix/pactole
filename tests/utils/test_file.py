"""Tests for file-related utilities."""

import csv
import io
import json
import zipfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests

from pactole.utils import (
    EnhancedJSONEncoder,
    ensure_directory,
    fetch_content,
    get_cache_path,
    read_csv_file,
    read_zip_file,
    write_csv_file,
    write_json_file,
)


class TestEnsureDirectory:
    """Tests for ensure_directory function."""

    def test_ensure_directory_creates_parent_directory(self, tmp_path):
        """Test ensure_directory creates missing parent directories."""

        target = tmp_path / "nested" / "folder" / "file.txt"
        ensure_directory(target)

        assert (tmp_path / "nested" / "folder").exists()
        assert (tmp_path / "nested" / "folder").is_dir()

    def test_ensure_directory_handles_existing_directory(self, tmp_path):
        """Test ensure_directory does nothing if directory already exists."""

        existing = tmp_path / "existing"
        existing.mkdir()
        target = existing / "file.txt"
        ensure_directory(target)

        assert existing.exists()
        assert existing.is_dir()

    def test_ensure_directory_accepts_string_path(self, tmp_path):
        """Test ensure_directory accepts string paths."""

        target = tmp_path / "string" / "path" / "file.txt"
        ensure_directory(str(target))

        assert (tmp_path / "string" / "path").exists()
        assert (tmp_path / "string" / "path").is_dir()


class TestGetCachePath:
    """Tests for get_cache_path function."""

    def test_get_cache_path_default(self):
        """Test get_cache_path returns default cache path."""

        cache_path = Path("/tmp/cache")
        with patch("pactole.utils.file.CACHE_PATH", cache_path):
            result = get_cache_path()
            assert isinstance(result, Path)

    def test_get_cache_path_with_string_folder(self):
        """Test get_cache_path with a string folder argument."""

        cache_path = Path("/tmp/cache")
        with patch("pactole.utils.file.CACHE_PATH", cache_path):
            result = get_cache_path("data")
            expected = cache_path / "data"
            assert result == expected

    def test_get_cache_path_with_path_folder(self):
        """Test get_cache_path with a Path folder argument."""

        cache_path = Path("/tmp/cache")
        with patch("pactole.utils.file.CACHE_PATH", cache_path):
            result = get_cache_path(Path("data"))
            expected = cache_path / "data"
            assert result == expected

    def test_get_cache_path_with_nested_folder(self):
        """Test get_cache_path with nested folder paths."""

        cache_path = Path("/tmp/cache")
        with patch("pactole.utils.file.CACHE_PATH", cache_path):
            result = get_cache_path("data/subfolder")
            expected = cache_path / "data/subfolder"
            assert result == expected

    def test_get_cache_path_strips_leading_dot_slash(self):
        """Test that leading './' is stripped from folder paths."""

        cache_path = Path("/tmp/cache")
        with patch("pactole.utils.file.CACHE_PATH", cache_path):
            result = get_cache_path("./data")
            expected = cache_path / "data"
            assert result == expected

            result = get_cache_path("../../data")
            expected = cache_path / "data"
            assert result == expected

    def test_get_cache_path_strips_leading_slash(self):
        """Test that leading '/' is stripped from folder paths."""

        cache_path = Path("/tmp/cache")
        with patch("pactole.utils.file.CACHE_PATH", cache_path):
            result = get_cache_path("/data")
            expected = cache_path / "data"
            assert result == expected

    def test_get_cache_path_strips_trailing_slash(self):
        """Test that trailing '/' is stripped from folder paths."""

        cache_path = Path("/tmp/cache")
        with patch("pactole.utils.file.CACHE_PATH", cache_path):
            result = get_cache_path("data/")
            expected = cache_path / "data"
            assert result == expected

    def test_get_cache_path_create_false_doesnt_create(self, tmp_path):
        """Test that create=False doesn't create directories."""

        with patch("pactole.utils.file.CACHE_PATH", tmp_path):
            test_folder = "test_folder"
            result = get_cache_path(test_folder, create=False)
            assert result == tmp_path / test_folder
            assert not result.exists()

    def test_get_cache_path_create_true_creates_directory(self, tmp_path):
        """Test that create=True creates the directory."""

        with patch("pactole.utils.file.CACHE_PATH", tmp_path):
            test_folder = "test_folder"
            result = get_cache_path(test_folder, create=True)
            assert result == tmp_path / test_folder
            assert result.exists()
            assert result.is_dir()

    def test_get_cache_path_create_true_creates_nested_directories(self, tmp_path):
        """Test that create=True creates nested directories."""

        with patch("pactole.utils.file.CACHE_PATH", tmp_path):
            test_folder = "test_folder/nested/deep"
            result = get_cache_path(test_folder, create=True)
            assert result == tmp_path / "test_folder/nested/deep"
            assert result.exists()
            assert result.is_dir()

    def test_get_cache_path_create_true_on_existing_directory(self, tmp_path):
        """Test that create=True works when directory already exists."""

        with patch("pactole.utils.file.CACHE_PATH", tmp_path):
            test_folder = "existing_folder"
            (tmp_path / test_folder).mkdir()
            result = get_cache_path(test_folder, create=True)
            assert result == tmp_path / test_folder
            assert result.exists()

    def test_get_cache_path_no_folder_with_create_false(self):
        """Test get_cache_path with no folder and create=False."""

        cache_path = Path("/tmp/cache")
        with patch("pactole.utils.file.CACHE_PATH", cache_path):
            result = get_cache_path(folder=None, create=False)
            assert result == cache_path

    def test_get_cache_path_empty_string_folder(self):
        """Test get_cache_path with empty string folder."""

        cache_path = Path("/tmp/cache")
        with patch("pactole.utils.file.CACHE_PATH", cache_path):
            result = get_cache_path("")
            assert result == cache_path


class TestFetchContent:
    """Tests for fetch_content function."""

    def test_fetch_content_text_success(self):
        """Test fetching text content successfully."""

        mock_response = Mock()
        mock_response.text = "Sample text content"
        mock_response.raise_for_status = Mock()

        with patch("pactole.utils.file.requests.get", return_value=mock_response):
            result = fetch_content("https://local.test/data.txt")
            assert result == "Sample text content"
            assert isinstance(result, str)

    def test_fetch_content_binary_success(self):
        """Test fetching binary content successfully."""

        mock_response = Mock()
        mock_response.content = b"Binary data"
        mock_response.raise_for_status = Mock()

        with patch("pactole.utils.file.requests.get", return_value=mock_response):
            result = fetch_content("https://local.test/image.png", binary=True)
            assert result == b"Binary data"
            assert isinstance(result, bytes)

    def test_fetch_content_default_timeout(self):
        """Test that default timeout is used."""

        mock_response = Mock()
        mock_response.text = "Content"
        mock_response.raise_for_status = Mock()

        with patch("pactole.utils.file.requests.get", return_value=mock_response) as mock_get:
            fetch_content("https://local.test/data.txt")
            mock_get.assert_called_once_with(url="https://local.test/data.txt", timeout=(6, 30))

    def test_fetch_content_custom_timeout(self):
        """Test fetching content with custom timeout."""

        mock_response = Mock()
        mock_response.text = "Content"
        mock_response.raise_for_status = Mock()

        with patch("pactole.utils.file.requests.get", return_value=mock_response) as mock_get:
            fetch_content("https://local.test/data.txt", timeout=10)
            mock_get.assert_called_once_with(url="https://local.test/data.txt", timeout=10)

    def test_fetch_content_with_kwargs(self):
        """Test fetching content with additional kwargs."""

        mock_response = Mock()
        mock_response.text = "Content"
        mock_response.raise_for_status = Mock()

        with patch("pactole.utils.file.requests.get", return_value=mock_response) as mock_get:
            fetch_content("https://local.test/data.txt", headers={"Authorization": "Bearer token"})
            mock_get.assert_called_once_with(
                url="https://local.test/data.txt",
                timeout=(6, 30),
                headers={"Authorization": "Bearer token"},
            )

    def test_fetch_content_raises_on_error(self):
        """Test that fetch_content raises exception on request error."""

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.RequestException("Error")

        with patch("pactole.utils.file.requests.get", return_value=mock_response):
            with pytest.raises(requests.RequestException):
                fetch_content("https://local.test/data.txt")


class TestReadZipFile:
    """Tests for read_zip_file function."""

    def test_read_zip_file_by_filename_bytes(self):
        """Test reading a file from ZIP by exact filename returning bytes."""

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("data.txt", "Hello, World!")
        zip_buffer.seek(0)

        result = read_zip_file(zip_buffer, filename="data.txt")
        assert result == b"Hello, World!"
        assert isinstance(result, bytes)

    def test_read_zip_file_by_filename_with_encoding(self):
        """Test reading a file from ZIP by filename with encoding."""

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("data.txt", "Hello, UTF-8! 🎉")
        zip_buffer.seek(0)

        result = read_zip_file(zip_buffer, filename="data.txt", encoding="utf-8")
        assert result == "Hello, UTF-8! 🎉"
        assert isinstance(result, str)

    def test_read_zip_file_by_extension(self):
        """Test reading a file from ZIP by extension."""

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("data.csv", "col1,col2\n1,2")
            zip_file.writestr("other.txt", "Other content")
        zip_buffer.seek(0)

        result = read_zip_file(zip_buffer, ext=".csv", encoding="utf-8")
        assert result == "col1,col2\n1,2"

    def test_read_zip_file_case_insensitive_extension(self):
        """Test that extension matching is case-insensitive."""

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("data.CSV", "col1,col2\n1,2")
        zip_buffer.seek(0)

        result = read_zip_file(zip_buffer, ext=".csv", encoding="utf-8")
        assert result == "col1,col2\n1,2"

    def test_read_zip_file_first_file_no_criteria(self):
        """Test reading first file when no criteria specified."""

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("first.txt", "First file")
            zip_file.writestr("second.txt", "Second file")
        zip_buffer.seek(0)

        result = read_zip_file(zip_buffer, encoding="utf-8")
        assert result == "First file"

    def test_read_zip_file_filename_not_found(self):
        """Test that FileNotFoundError is raised when filename not found."""

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("data.txt", "content")
        zip_buffer.seek(0)

        with pytest.raises(FileNotFoundError, match="does not exist in the archive"):
            read_zip_file(zip_buffer, filename="missing.txt")

    def test_read_zip_file_extension_not_found(self):
        """Test that FileNotFoundError is raised when extension not found."""

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("data.txt", "content")
        zip_buffer.seek(0)

        with pytest.raises(FileNotFoundError, match="does not exist in the archive"):
            read_zip_file(zip_buffer, ext=".csv")

    def test_read_zip_file_decoding_errors_ignore(self):
        """Test decoding errors with 'ignore' mode."""

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("data.txt", b"Hello \xff World")
        zip_buffer.seek(0)

        result = read_zip_file(zip_buffer, filename="data.txt", encoding="utf-8")
        assert "Hello" in result
        assert "World" in result

    def test_read_zip_file_decoding_errors_replace(self):
        """Test decoding errors with 'replace' mode."""

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("data.txt", b"Hello \xff World")
        zip_buffer.seek(0)

        result = read_zip_file(
            zip_buffer, filename="data.txt", encoding="utf-8", decoding_errors="replace"
        )
        assert "Hello" in result
        assert "\ufffd" in result
        assert "World" in result

    def test_read_zip_file_decoding_errors_strict(self):
        """Test decoding errors with 'strict' mode."""

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("data.txt", b"Hello \xff World")
        zip_buffer.seek(0)

        with pytest.raises(UnicodeDecodeError):
            read_zip_file(
                zip_buffer, filename="data.txt", encoding="utf-8", decoding_errors="strict"
            )


class TestReadCsvFile:
    """Tests for read_csv_file function."""

    def test_read_csv_file_with_headers(self):
        """Test reading CSV file with headers as dictionaries."""

        csv_content = "col1,col2\n1,2\n3,4\n"
        file = io.StringIO(csv_content)

        result = read_csv_file(file, dialect="excel")
        assert len(result) == 2
        assert result[0] == {"col1": "1", "col2": "2"}
        assert result[1] == {"col1": "3", "col2": "4"}

    def test_read_csv_file_without_headers(self):
        """Test reading CSV file without headers as lists."""

        csv_content = "col1,col2\n1,2\n3,4\n"
        file = io.StringIO(csv_content)

        result = read_csv_file(file, dialect="excel", fieldnames=False)
        assert len(result) == 3
        assert result[0] == ["col1", "col2"]
        assert result[1] == ["1", "2"]
        assert result[2] == ["3", "4"]

    def test_read_csv_file_auto_dialect(self):
        """Test reading CSV file with auto-detected dialect."""

        csv_content = "col1;col2\n1;2\n3;4\n"
        file = io.StringIO(csv_content)

        result = read_csv_file(file, dialect="auto")
        assert len(result) == 2
        assert result[0] == {"col1": "1", "col2": "2"}
        assert result[1] == {"col1": "3", "col2": "4"}

    def test_read_csv_file_with_iterator(self):
        """Test reading CSV file with iterator mode."""

        csv_content = "col1,col2\n1,2\n3,4\n"
        file = io.StringIO(csv_content)

        result = read_csv_file(file, dialect="excel", iterator=True)
        assert hasattr(result, "__iter__")
        rows = list(result)
        assert len(rows) == 2
        assert rows[0] == {"col1": "1", "col2": "2"}
        assert rows[1] == {"col1": "3", "col2": "4"}

    def test_read_csv_file_with_iterator_no_headers(self):
        """Test reading CSV file with iterator mode and no headers."""

        csv_content = "col1,col2\n1,2\n3,4\n"
        file = io.StringIO(csv_content)

        result = read_csv_file(file, dialect="excel", iterator=True, fieldnames=False)
        assert hasattr(result, "__iter__")
        rows = list(result)
        assert len(rows) == 3
        assert rows[0] == ["col1", "col2"]
        assert rows[1] == ["1", "2"]
        assert rows[2] == ["3", "4"]

    def test_read_csv_file_with_custom_delimiter(self):
        """Test reading CSV file with custom delimiter."""

        csv_content = "col1|col2\n1|2\n3|4\n"
        file = io.StringIO(csv_content)

        result = read_csv_file(file, dialect="excel", delimiter="|")
        assert len(result) == 2
        assert result[0] == {"col1": "1", "col2": "2"}
        assert result[1] == {"col1": "3", "col2": "4"}

    def test_read_csv_file_empty_file(self):
        """Test reading empty CSV file."""

        csv_content = ""
        file = io.StringIO(csv_content)

        result = read_csv_file(file, dialect="excel")
        assert len(result) == 0

    def test_read_csv_file_tab_separated(self):
        """Test reading tab-separated CSV file with auto-detection."""

        csv_content = "col1\tcol2\n1\t2\n3\t4\n"
        file = io.StringIO(csv_content)

        result = read_csv_file(file, dialect="auto")
        assert len(result) == 2
        assert result[0] == {"col1": "1", "col2": "2"}
        assert result[1] == {"col1": "3", "col2": "4"}

    def test_read_csv_file_with_quotes(self):
        """Test reading CSV file with quoted fields."""

        csv_content = 'col1,col2\n"value, with comma","normal"\n'
        file = io.StringIO(csv_content)

        result = read_csv_file(file, dialect="excel")
        assert len(result) == 1
        assert result[0] == {"col1": "value, with comma", "col2": "normal"}

    def test_read_csv_file_auto_dialect_file_position_reset(self):
        """Test that file position is reset after dialect detection."""

        csv_content = "col1,col2\n1,2\n3,4\n"
        file = io.StringIO(csv_content)

        result1 = read_csv_file(file, dialect="auto")
        assert len(result1) == 2

        file.seek(0)
        result2 = read_csv_file(file, dialect="auto")
        assert len(result2) == 2
        assert result1 == result2

    def test_read_csv_file_auto_dialect_retries_until_success(self):
        """Test that auto-detection retries until it succeeds."""

        csv_content = "col1;col2\n1;2\n3;4\n"
        file = io.StringIO(csv_content)
        sniff_calls = []

        class SemiDialect(csv.Dialect):
            """CSV dialect for semicolon-delimited data."""

            delimiter = ";"
            quotechar = '"'
            doublequote = True
            skipinitialspace = False
            lineterminator = "\n"
            quoting = csv.QUOTE_MINIMAL

        def sniff_side_effect(data):
            sniff_calls.append(data)
            if len(sniff_calls) == 1:
                raise csv.Error("sniff failed")
            return SemiDialect

        with patch("pactole.utils.file.csv.Sniffer.sniff", side_effect=sniff_side_effect):
            result = read_csv_file(file, dialect="auto", sample_size=4, max_tries=3)

        assert len(sniff_calls) == 2
        assert len(sniff_calls[1]) > len(sniff_calls[0])
        assert len(result) == 2
        assert result[0] == {"col1": "1", "col2": "2"}
        assert result[1] == {"col1": "3", "col2": "4"}

    def test_read_csv_file_auto_dialect_raises_after_retries(self):
        """Test that auto-detection raises after exhausting retries."""

        csv_content = "col1;col2\n1;2\n3;4\n"
        file = io.StringIO(csv_content)

        with patch("pactole.utils.file.csv.Sniffer.sniff", side_effect=csv.Error("fail")) as sniff:
            with pytest.raises(csv.Error, match="auto-detect CSV dialect"):
                read_csv_file(file, dialect="auto", sample_size=4, max_tries=3)

        assert sniff.call_count == 3


class TestWriteCsvFile:
    """Tests for write_csv_file function."""

    def test_write_csv_file_dicts_infers_headers(self):
        """Test writing dictionaries with inferred headers."""

        file = io.StringIO()
        data = [
            {"col1": "1", "col2": "2"},
            {"col1": "3", "col2": "4"},
        ]

        write_csv_file(file, data)

        file.seek(0)
        assert file.read() == "col1,col2\r\n1,2\r\n3,4\r\n"

    def test_write_csv_file_dicts_with_fieldnames(self):
        """Test writing dictionaries with explicit headers."""

        file = io.StringIO()
        data = [
            {"col1": "1", "col2": "2"},
            {"col1": "3", "col2": "4"},
        ]

        write_csv_file(file, data, fieldnames=["col2", "col1"])

        file.seek(0)
        assert file.read() == "col2,col1\r\n2,1\r\n4,3\r\n"

    def test_write_csv_file_dicts_without_header(self):
        """Test writing dictionaries without a header row."""

        file = io.StringIO()
        data = [
            {"col1": "1", "col2": "2"},
            {"col1": "3", "col2": "4"},
        ]

        write_csv_file(file, data, fieldnames=["col1", "col2"], header=False)

        file.seek(0)
        assert file.read() == "1,2\r\n3,4\r\n"

    def test_write_csv_file_objects_with_to_dict(self):
        """Test writing objects that expose to_dict instead of being dicts."""

        class SampleRow:
            """Simple row object with a to_dict implementation."""

            def __init__(self, col1: str, col2: str) -> None:
                self.col1 = col1
                self.col2 = col2

            def to_dict(self) -> dict[str, str]:
                """Return the row as a dictionary."""

                return {"col1": self.col1, "col2": self.col2}

        file = io.StringIO()
        data = [SampleRow("1", "2"), SampleRow("3", "4")]

        write_csv_file(file, data)

        file.seek(0)
        assert file.read() == "col1,col2\r\n1,2\r\n3,4\r\n"

    def test_write_csv_file_lists(self):
        """Test writing list rows without headers."""

        file = io.StringIO()
        data = [["col1", "col2"], ["1", "2"], ["3", "4"]]

        write_csv_file(file, data)

        file.seek(0)
        assert file.read() == "col1,col2\r\n1,2\r\n3,4\r\n"

    def test_write_csv_file_empty_data(self):
        """Test writing with no data leaves file empty."""

        file = io.StringIO()

        write_csv_file(file, [])

        file.seek(0)
        assert file.read() == ""


class TestEnhancedJsonEncoder:
    """Tests for EnhancedJSONEncoder."""

    def test_enhanced_json_encoder_serializes_path(self):
        """Test serializing Path objects."""

        encoded = json.dumps({"path": Path("/tmp/data.json")}, cls=EnhancedJSONEncoder)

        assert json.loads(encoded) == {"path": "/tmp/data.json"}

    def test_enhanced_json_encoder_raises_for_unknown_types(self):
        """Test that unknown types still raise a TypeError."""

        with pytest.raises(TypeError):
            json.dumps({"value": object()}, cls=EnhancedJSONEncoder)


class TestWriteJsonFile:
    """Tests for write_json_file function."""

    def test_write_json_file_serializes_path_and_model(self):
        """Test writing JSON with Path and Pydantic model values."""

        file = io.StringIO()
        data = {"path": Path("/tmp/data.json")}

        write_json_file(file, data)

        file.seek(0)
        payload = json.loads(file.read())
        assert payload == {"path": "/tmp/data.json"}
