"""File related utilities and classes."""

from __future__ import annotations

import csv
import datetime
import json
import logging
import zipfile
from enum import Enum
from itertools import tee
from pathlib import Path, PurePath
from typing import IO, Any, Iterable, Iterator, Literal

import requests

logger = logging.getLogger(__name__)

# The path to the cache folder
CACHE_PATH = Path("~/.cache")

# The amount of bytes to read for auto-detecting the CSV dialect
CSV_SAMPLE_SIZE = 4096
CSV_MAX_TRIES = 8


def ensure_directory(path: Path | str) -> None:
    """Ensure that the directory for the given path exists.

    Args:
        path (Path | str): The file path for which to ensure the directory exists.

    Examples:
        >>> ensure_directory('data/archive.csv')
        >>> Path('data').exists()
        True
    """
    directory = Path(path).parent
    if directory and not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)


def get_cache_path(folder: Path | str = None, create: bool = False) -> Path:
    """Return the cache path, optionally creating it.

    Args:
        folder (Path | str, optional): A subpath within the cache directory.
            Defaults to None.
        create (bool, optional): Whether to create the directory if it does not exist.
            Defaults to False.

    Returns:
        Path: The cache path.

    Raises:
        OSError: If the directory cannot be created.

    Examples:
        >>> get_cache_path()
        PosixPath('/home/user/.cache')
        >>> get_cache_path('data', create=True)
        PosixPath('/home/user/.cache/data')
    """
    cache_path = CACHE_PATH.expanduser()
    if folder is not None:
        cache_path = cache_path / Path(folder).as_posix().strip("./").replace("..", "_")

    if create and not cache_path.exists():
        cache_path.mkdir(parents=True, exist_ok=True)

    return cache_path


def fetch_content(
    url: str,
    binary: bool = False,
    timeout: int | tuple = (6, 30),
    **kwargs,
) -> str | bytes:
    """Fetch content from a URL.

    Args:
        url (str): The URL to fetch content from.
        binary (bool, optional): Whether to return content as bytes. Defaults to False.
        timeout (int | tuple, optional): Timeout for the request. Defaults to (6, 30).
        **kwargs: Additional arguments to pass to requests

    Returns:
        str | bytes: The content fetched from the URL.

    Raises:
        requests.RequestException: If the request fails.

    Examples:
        >>> content = fetch_content('https://example.com/data.txt')
        >>> print(content)
        '...'
        >>> binary_content = fetch_content('https://example.com/image.png', binary=True)
        >>> print(binary_content)
        b'...'
    """
    response = requests.get(url=url, timeout=timeout, **kwargs)
    response.raise_for_status()
    return response.content if binary else response.text


def read_zip_file(
    file: IO[bytes],
    filename: str = None,
    ext: str = None,
    encoding: str | None = None,
    decoding_errors: Literal["ignore", "strict", "replace"] = "ignore",
) -> bytes | str:
    """Read a specific file from a ZIP archive in memory.

    Args:
        file (IO[bytes]): The file object of the ZIP archive. It must be opened in binary mode.
        filename (str, optional): The exact filename to extract. Defaults to None.
        ext (str, optional): The file extension to filter by if filename is not provided.
            Defaults to None.
        encoding (str | None, optional): The encoding to decode the file content.
            If None, returns bytes. Defaults to None.
        decoding_errors (Literal["ignore", "strict", "replace"], optional): The error
            handling scheme for decoding. Defaults to "ignore".

    Returns:
        bytes | str: The content of the extracted file.

    Raises:
        FileNotFoundError: If no file matches the given criteria.

    Examples:
        >>> with open('archive.zip', 'rb') as f:
        ...     content = read_zip_file(f, filename='data.csv', encoding='utf-8')
        >>> print(content)
        'col1,col2\\n1,2\\n3,4'
        >>> with open('archive.zip', 'rb') as f:
        ...     content = read_zip_file(f, ext='.json')
        >>> print(content)
        b'{"key": "value"}'
    """
    with zipfile.ZipFile(file) as zip_file:
        found = False
        for info in zip_file.infolist():
            if filename:
                if filename == info.filename:
                    found = True
                    break

            elif ext:
                file_extension = Path(info.filename).suffix
                if file_extension.lower() == ext.lower():
                    filename = info.filename
                    found = True
                    break
            else:
                filename = info.filename
                found = True
                break

        if not found:
            raise FileNotFoundError("The file does not exist in the archive.")

        with zip_file.open(filename, "r") as nested_file:
            content = nested_file.read()

        if encoding:
            return content.decode(encoding, errors=decoding_errors)
        return content


def read_csv_file(
    file: IO[str],
    dialect: str = "auto",
    iterator: bool = False,
    sample_size: int = CSV_SAMPLE_SIZE,
    max_tries: int = CSV_MAX_TRIES,
    **kwargs,
) -> Iterable[dict | list]:
    """Read a CSV file and return its content.

    Args:
        file (IO[str]): The file object to read from. It must be opened in text mode.
        dialect (str, optional): The CSV dialect to use. If "auto", it will be
            auto-detected. Defaults to "auto".
        iterator (bool, optional): If True, returns an iterator instead of a list.
            Defaults to False.
        sample_size (int, optional): The number of bytes to read for auto-detecting
            the CSV dialect. Defaults to CSV_SAMPLE_SIZE.
        max_tries (int, optional): The maximum number of attempts to auto-detect the
            CSV dialect. Defaults to CSV_MAX_TRIES.
        **kwargs: Additional arguments to pass to csv.DictReader or csv.reader.

    Returns:
        Iterable[dict | list]: An iterable of rows as dictionaries or lists.

    Raises:
        csv.Error: If there is an error reading the CSV file.

    Examples:
        >>> with open('data.csv', 'r', encoding='utf-8') as f:
        ...     rows = read_csv_file(f)
        >>> for row in rows:
        ...     print(row)
        {'col1': '1', 'col2': '2'}
        {'col1': '3', 'col2': '4'}
        >>> with open('data.csv', 'r', encoding='utf-8') as f:
        ...     rows = read_csv_file(f, fieldnames=False)
        >>> for row in rows:
        ...     print(row)
        ['col1', 'col2']
        ['1', '2']
        ['3', '4']
        >>> with open('data.csv', 'r', encoding='utf-8') as f:
        ...     rows_iter = read_csv_file(f, iterator=True)
        >>> for row in rows_iter:
        ...     print(row)
        {'col1': '1', 'col2': '2'}
        {'col1': '3', 'col2': '4'}
    """
    if kwargs.get("fieldnames") is False:
        reader_factory = csv.reader
        kwargs.pop("fieldnames")
    else:
        reader_factory = csv.DictReader

    if dialect == "auto":
        for i in range(max_tries):
            data = file.read(sample_size * (i + 1))
            file.seek(0)
            try:
                dialect = csv.Sniffer().sniff(data)
                break
            except csv.Error:
                continue
        else:
            raise csv.Error("Could not auto-detect CSV dialect after multiple attempts.")

    reader = reader_factory(file, dialect=dialect, **kwargs)

    if iterator:
        return reader

    return list(reader)


def write_csv_file(
    file: IO[str],
    data: Iterable[dict | list],
    fieldnames: list[str] | None = None,
    dialect: str = "excel",
    header: bool = True,
    **kwargs,
) -> None:
    """Write data to a CSV file.

    Args:
        file (IO[str]): The file object to write to. It must be opened in text mode.
        data (Iterable[dict | list]): The data to write, as an iterable of dictionaries or lists.
        fieldnames (list[str] | None, optional): The field names to use if data is an iterable of
            dictionaries. If None, field names will be inferred from the first dictionary.
            Defaults to None.
        dialect (str, optional): The CSV dialect to use. Defaults to "excel".
        header (bool, optional): Whether to write the header row. Defaults to True.
        **kwargs: Additional arguments to pass to csv.DictWriter or csv.writer.

    Raises:
        csv.Error: If there is an error writing to the CSV file.

    Examples:
        >>> with open('output.csv', 'w', encoding='utf-8', newline='') as f:
        ...     write_csv_file(f, [{'col1': '1', 'col2': '2'}, {'col1': '3', 'col2': '4'}])
        >>> with open('output.csv', 'w', encoding='utf-8', newline='') as f:
        ...     write_csv_file(f, [['col1', 'col2'], ['1', '2'], ['3', '4']])
    """
    [discover, walk] = tee(
        (line.to_dict() if line and hasattr(line, "to_dict") else line) for line in data
    )

    writer = None
    for line in discover:
        if isinstance(line, dict):
            if not fieldnames:
                fieldnames = line.keys()

            writer = csv.DictWriter(file, dialect=dialect, fieldnames=fieldnames, **kwargs)
            if header:
                writer.writeheader()
        else:
            writer = csv.writer(file, dialect=dialect, **kwargs)
        break

    if writer:
        writer.writerows(walk)


class EnhancedJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles additional types like Path objects.

    Examples:
        >>> json.dumps({'path': Path('/home/user/file.txt')}, cls=EnhancedJSONEncoder)
        '{"path": "/home/user/file.txt"}'
    """

    def default(self, o: Any) -> Any:
        """Convert unhandled objects for JSON serialization.

        Args:
            o (Any): The object to serialize.

        Returns:
            Any: The serialized object.
        """
        if isinstance(o, PurePath):
            return str(o)
        return super().default(o)


def write_json_file(
    file: IO[str],
    data: Any,
    indent: int | str | None = None,
    ensure_ascii: bool = False,
    **kwargs,
) -> None:
    """Write data to a JSON file.

    Args:
        file (IO[str]): The file object to write to. It must be opened in text mode.
        data (Any): The data to write to the JSON file.
        indent (int | str | None, optional): The indentation level for pretty-printing the JSON
            data. Defaults to None.
        ensure_ascii (bool, optional): Whether to escape non-ASCII characters. Defaults to False.
        **kwargs: Additional arguments to pass to json.dump.

    Raises:
        TypeError: If the data cannot be serialized to JSON.

    Examples:
        >>> with open('output.json', 'w', encoding='utf-8') as f:
        ...     write_json_file(f, {'key': 'value'})
    """
    json.dump(
        data,
        file,
        cls=EnhancedJSONEncoder,
        indent=indent,
        ensure_ascii=ensure_ascii,
        **kwargs,
    )


class FileType(Enum):
    """Enumeration of file types."""

    CSV = "csv"
    JSON = "json"
    TEXT = "txt"

    @classmethod
    def get(cls, file_type: FileType | str) -> FileType:
        """Get the FileType from a file extension or type string.

        Unknown types default to TEXT.

        Args:
            file_type (FileType | str): The file extension (e.g., ".csv", ".json", ".txt"),
                or the file type string (e.g., "csv", "json", "txt"). If a FileType enum member
                is passed, it will be returned as is.

        Returns:
            FileType: The corresponding FileType enum member.

        Examples:
            >>> FileType.get(".csv")
            <FileType.CSV: 'csv'>
            >>> FileType.get(".json")
            <FileType.JSON: 'json'>
            >>> FileType.get(".txt")
            <FileType.TEXT: 'txt'>
            >>> FileType.get(".log")
            <FileType.TEXT: 'txt'>
            >>> FileType.get(FileType.CSV)
            <FileType.CSV: 'csv'>
        """
        if isinstance(file_type, cls):
            return file_type

        try:
            return cls(str(file_type).lower().lstrip("."))
        except ValueError:
            return cls.TEXT


class File:
    """A class representing a file with its path, type, and encoding.

    Args:
        path (Path | str): The file path.
        file_type (FileType | str | None, optional): The file type or extension.
            If None, it will be inferred from the file extension. Defaults to None.
        encoding (str, optional): The file encoding. Defaults to "utf-8".

    Examples:
        >>> file = File('data.csv')
        >>> file.path
        PosixPath('data.csv')
        >>> file.type
        <FileType.CSV: 'csv'>
        >>> file.encoding
        'utf-8'
    """

    _path: Path
    _type: FileType
    _encoding: str

    def __init__(
        self,
        path: Path | str,
        file_type: FileType | str | None = None,
        encoding: str = "utf-8",
    ) -> None:
        self._path = Path(path)
        self._encoding = encoding
        self._type = FileType.get(file_type or self._path.suffix)

    @property
    def path(self) -> Path:
        """Return the file path.

        Returns:
            Path: The file path.

        Examples:
            >>> file = File('data.csv')
            >>> file.path
            PosixPath('data.csv')
        """
        return self._path

    @property
    def type(self) -> FileType:
        """Return the file type.

        Returns:
            FileType: The file type.

        Examples:
            >>> file = File('data.csv')
            >>> file.type
            <FileType.CSV: 'csv'>
        """
        return self._type

    @property
    def encoding(self) -> str:
        """Return the file encoding.

        Returns:
            str: The file encoding.

        Examples:
            >>> file = File('data.csv')
            >>> file.encoding
            'utf-8'
        """
        return self._encoding

    def exists(self) -> bool:
        """Check if the file exists.

        Returns:
            bool: True if the file exists, False otherwise.

        Examples:
            >>> file = File('nonexistent_file.txt')
            >>> file.exists()
            False  # Assuming nonexistent_file.txt does not exist yet
            >>> file = File('existing_file.txt')
            >>> file.exists()
            True  # Assuming existing_file.txt exists
        """
        return self._path.exists()

    def date(self) -> datetime.datetime:
        """Return the last modification time of the file as a timestamp.

        Returns:
            datetime.datetime: The last modification time as a datetime object.

        Raises:
            FileNotFoundError: If the file does not exist.

        Examples:
            >>> file = File('data.csv')
            >>> file.date()
            datetime.datetime(2024, 6, 1, 12, 0, 0)  # Example modification time
        """
        timestamp = self._path.stat().st_mtime
        return datetime.datetime.fromtimestamp(timestamp)

    def size(self) -> int:
        """Return the size of the file in bytes.

        Returns:
            int: The size of the file in bytes.

        Examples:
            >>> file = File('data.csv')
            >>> file.size()
            1024  # Example size in bytes
        """
        if not self._path.exists():
            return 0
        return self._path.stat().st_size

    def read(self, throw: bool = True) -> Any | None:
        """Read the file content.

        Args:
            throw (bool, optional): Whether to throw exceptions on errors. Defaults to True.

        Returns:
            Any | None: The content of the file, with respect to its type,
                or None if the file does not exist or cannot be read.

        Raises:
            FileNotFoundError: If the file does not exist and throw is True.
            IOError: If there is an error reading the file.

        Examples:
            >>> file = File('data.csv')
            >>> file.read()
            [{'col1': '1', 'col2': '2'}, {'col1': '3', 'col2': '4'}]  # Example CSV content
            >>> file = File('data.json')
            >>> file.read()
            {'key': 'value', 'items': [1, 2, 3]}  # Example JSON content
            >>> file = File('note.txt')
            >>> file.read()
            'hello world'  # Example text content
            >>> file = File('nonexistent_file.txt')
            >>> file.read(False)
            None  # Assuming nonexistent_file.txt does not exist yet
            >>> file.read()
            Traceback (most recent call last):
                ...
            FileNotFoundError: The file nonexistent_file.txt does not exist.
        """
        if not self._path.exists():
            if throw:
                raise FileNotFoundError(f"The file {self._path} does not exist.")
            return None

        with self.open() as file:
            if self._type == FileType.CSV:
                try:
                    return read_csv_file(file)
                except csv.Error as e:
                    if throw:
                        raise IOError(f"Failed to read CSV file: {self._path}") from e
                    logger.warning("Failed to read CSV file: %s, error: %s", self._path, e)
                    return None

            if self._type == FileType.JSON:
                try:
                    return json.load(file)
                except json.JSONDecodeError as e:
                    if throw:
                        raise IOError(f"Failed to read JSON file: {self._path}") from e
                    logger.warning("Failed to read JSON file: %s, error: %s", self._path, e)
                    return None

            return file.read()

    def readlines(self, throw: bool = True) -> Iterator:
        """Read the file content as lines.

        Args:
            throw (bool, optional): Whether to throw exceptions on errors. Defaults to True.

        Returns:
            Iterator: An iterator over the lines of the file, or an empty iterator if the file
                does not exist or cannot be read.

        Raises:
            FileNotFoundError: If the file does not exist and throw is True.
            IOError: If there is an error reading the file.

        Examples:
            >>> file = File('note.txt')
            >>> for line in file.readlines():
            ...     print(line)
            hello world  # Example content of note.txt
        """
        if not self._path.exists():
            if throw:
                raise FileNotFoundError(f"The file {self._path} does not exist.")
            return

        with self.open() as file:
            if self._type == FileType.CSV:
                try:
                    yield from read_csv_file(file, iterator=True)
                except csv.Error as e:
                    if throw:
                        raise IOError(f"Failed to read CSV file: {self._path}") from e
                    logger.warning("Failed to read CSV file: %s, error: %s", self._path, e)
                return

            for line in file:
                yield line.rstrip("\n")

    def write(self, content: Any, throw: bool = True) -> None:
        """Write content to the file.

        Ensures the parent directory exists before writing.

        Args:
            content (Any): The content to write to the file. The type of content should match
                the file type (e.g., list of dicts for CSV, dict for JSON, string for text).
            throw (bool, optional): Whether to throw exceptions on errors. Defaults to True.

        Raises:
            IOError: If there is an error writing to the file.

        Examples:
            >>> file = File('data.csv')
            >>> file.write([{'col1': '1', 'col2': '2'}, {'col1': '3', 'col2': '4'}])
            >>> file = File('data.json')
            >>> file.write({'key': 'value', 'items': [1, 2, 3]})
            >>> file = File('note.txt')
            >>> file.write('hello world')
        """
        with self.open("w") as file:
            if self._type == FileType.CSV:
                try:
                    write_csv_file(file, content)
                except csv.Error as e:
                    if throw:
                        raise IOError(f"Failed to write CSV file: {self._path}") from e
                    logger.warning("Failed to write CSV file: %s, error: %s", self._path, e)

            elif self._type == FileType.JSON:
                try:
                    write_json_file(file, content)
                except json.JSONDecodeError as e:
                    if throw:
                        raise IOError(f"Failed to write JSON file: {self._path}") from e
                    logger.warning("Failed to write JSON file: %s, error: %s", self._path, e)

            else:
                file.write(content)

    def delete(self, throw: bool = True) -> None:
        """Delete the file.

        Args:
            throw (bool, optional): Whether to throw exceptions on errors. Defaults to True.

        Raises:
            FileNotFoundError: If the file does not exist and throw is True.
            IOError: If there is an error deleting the file.

        Examples:
            >>> file = File('data.csv')
            >>> file.delete()
        """
        if not self._path.exists():
            if throw:
                raise FileNotFoundError(f"The file {self._path} does not exist.")
            return

        self._path.unlink()

    def open(self, mode: str = "r") -> IO[Any]:
        """Open the file with the appropriate mode and encoding.

        If the mode includes writing, ensure the parent directory exists.

        Args:
            mode (str, optional): The mode to open the file. Defaults to "r".

        Returns:
            IO[Any]: The opened file object.

        Raises:
            IOError: If there is an error opening the file.

        Examples:
            >>> file = File('data.csv')
            >>> with file.open('w') as f:
            ...     f.write('new content')
            >>> with file.open() as f:
            ...     content = f.read()
        """
        if "w" in mode or "a" in mode:
            ensure_directory(self._path)

        return self._path.open(mode, encoding=self._encoding)
