"""File related utilities and classes."""

from __future__ import annotations

import csv
import json
from itertools import tee
from pathlib import PurePath
from typing import IO, Any, Iterable

# The amount of bytes to read for auto-detecting the CSV dialect
CSV_SAMPLE_SIZE = 4096
CSV_MAX_TRIES = 8


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
