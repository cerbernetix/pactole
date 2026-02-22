# File

[Pactole Index](../README.md#pactole-index) / [Utils](./index.md#utils) / File

> Auto-generated documentation for [utils.file](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py) module.

#### Attributes

- `CACHE_PATH` - The path to the cache folder: Path('~/.cache')

- `CSV_SAMPLE_SIZE` - The amount of bytes to read for auto-detecting the CSV dialect: 4096


- [File](#file)
  - [EnhancedJSONEncoder](#enhancedjsonencoder)
    - [EnhancedJSONEncoder().default](#enhancedjsonencoder()default)
  - [File](#file-1)
    - [File().date](#file()date)
    - [File().delete](#file()delete)
    - [File().encoding](#file()encoding)
    - [File().exists](#file()exists)
    - [File().open](#file()open)
    - [File().path](#file()path)
    - [File().read](#file()read)
    - [File().readlines](#file()readlines)
    - [File().size](#file()size)
    - [File().type](#file()type)
    - [File().write](#file()write)
  - [FileType](#filetype)
    - [FileType.get](#filetypeget)
  - [ensure_directory](#ensure_directory)
  - [fetch_content](#fetch_content)
  - [get_cache_path](#get_cache_path)
  - [read_csv_file](#read_csv_file)
  - [read_zip_file](#read_zip_file)
  - [write_csv_file](#write_csv_file)
  - [write_json_file](#write_json_file)

## EnhancedJSONEncoder

[Show source in file.py:297](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L297)

JSON encoder that handles additional types like Path objects.

#### Examples

```python
>>> json.dumps({'path': Path('/home/user/file.txt')}, cls=EnhancedJSONEncoder)
'{"path": "/home/user/file.txt"}'
```

#### Signature

```python
class EnhancedJSONEncoder(json.JSONEncoder): ...
```

### EnhancedJSONEncoder().default

[Show source in file.py:305](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L305)

Convert unhandled objects for JSON serialization.

#### Arguments

- `o` *Any* - The object to serialize.

#### Returns

- `Any` - The serialized object.

#### Signature

```python
def default(self, o: Any) -> Any: ...
```



## File

[Show source in file.py:395](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L395)

A class representing a file with its path, type, and encoding.

#### Arguments

path (Path | str): The file path.
file_type (FileType | str | None, optional): The file type or extension.
    If None, it will be inferred from the file extension. Defaults to None.
- `encoding` *str, optional* - The file encoding. Defaults to "utf-8".

#### Examples

```python
>>> file = File('data.csv')
>>> file.path
PosixPath('data.csv')
>>> file.type
<FileType.CSV: 'csv'>
>>> file.encoding
'utf-8'
```

#### Signature

```python
class File:
    def __init__(
        self,
        path: Path | str,
        file_type: FileType | str | None = None,
        encoding: str = "utf-8",
    ) -> None: ...
```

### File().date

[Show source in file.py:486](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L486)

Return the last modification time of the file as a timestamp.

#### Returns

- `datetime.datetime` - The last modification time as a datetime object.

#### Raises

- `FileNotFoundError` - If the file does not exist.

#### Examples

```python
>>> file = File('data.csv')
>>> file.date()
datetime.datetime(2024, 6, 1, 12, 0, 0)  # Example modification time
```

#### Signature

```python
def date(self) -> datetime.datetime: ...
```

### File().delete

[Show source in file.py:655](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L655)

Delete the file.

#### Arguments

- `throw` *bool, optional* - Whether to throw exceptions on errors. Defaults to True.

#### Raises

- `FileNotFoundError` - If the file does not exist and throw is True.
- `IOError` - If there is an error deleting the file.

#### Examples

```python
>>> file = File('data.csv')
>>> file.delete()
```

#### Signature

```python
def delete(self, throw: bool = True) -> None: ...
```

### File().encoding

[Show source in file.py:456](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L456)

Return the file encoding.

#### Returns

- `str` - The file encoding.

#### Examples

```python
>>> file = File('data.csv')
>>> file.encoding
'utf-8'
```

#### Signature

```python
@property
def encoding(self) -> str: ...
```

### File().exists

[Show source in file.py:470](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L470)

Check if the file exists.

#### Returns

- `bool` - True if the file exists, False otherwise.

#### Examples

```python
>>> file = File('nonexistent_file.txt')
>>> file.exists()
False  # Assuming nonexistent_file.txt does not exist yet
>>> file = File('existing_file.txt')
>>> file.exists()
True  # Assuming existing_file.txt exists
```

#### Signature

```python
def exists(self) -> bool: ...
```

### File().open

[Show source in file.py:676](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L676)

Open the file with the appropriate mode and encoding.

If the mode includes writing, ensure the parent directory exists.

#### Arguments

- `mode` *str, optional* - The mode to open the file. Defaults to "r".

#### Returns

- `IO[Any]` - The opened file object.

#### Raises

- `IOError` - If there is an error opening the file.

#### Examples

```python
>>> file = File('data.csv')
>>> with file.open('w') as f:
...     f.write('new content')
>>> with file.open() as f:
...     content = f.read()
```

#### Signature

```python
def open(self, mode: str = "r") -> IO[Any]: ...
```

### File().path

[Show source in file.py:428](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L428)

Return the file path.

#### Returns

- `Path` - The file path.

#### Examples

```python
>>> file = File('data.csv')
>>> file.path
PosixPath('data.csv')
```

#### Signature

```python
@property
def path(self) -> Path: ...
```

### File().read

[Show source in file.py:518](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L518)

Read the file content.

#### Arguments

- `throw` *bool, optional* - Whether to throw exceptions on errors. Defaults to True.

#### Returns

Any | None: The content of the file, with respect to its type,
    or None if the file does not exist or cannot be read.

#### Raises

- `FileNotFoundError` - If the file does not exist and throw is True.
- `IOError` - If there is an error reading the file.

#### Examples

```python
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
```

#### Signature

```python
def read(self, throw: bool = True) -> Any | None: ...
```

### File().readlines

[Show source in file.py:576](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L576)

Read the file content as lines.

#### Arguments

- `throw` *bool, optional* - Whether to throw exceptions on errors. Defaults to True.

#### Returns

- `Iterator` - An iterator over the lines of the file, or an empty iterator if the file
    does not exist or cannot be read.

#### Raises

- `FileNotFoundError` - If the file does not exist and throw is True.
- `IOError` - If there is an error reading the file.

#### Examples

```python
>>> file = File('note.txt')
>>> for line in file.readlines():
...     print(line)
hello world  # Example content of note.txt
```

#### Signature

```python
def readlines(self, throw: bool = True) -> Iterator: ...
```

### File().size

[Show source in file.py:503](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L503)

Return the size of the file in bytes.

#### Returns

- `int` - The size of the file in bytes.

#### Examples

```python
>>> file = File('data.csv')
>>> file.size()
1024  # Example size in bytes
```

#### Signature

```python
def size(self) -> int: ...
```

### File().type

[Show source in file.py:442](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L442)

Return the file type.

#### Returns

- [FileType](#filetype) - The file type.

#### Examples

```python
>>> file = File('data.csv')
>>> file.type
<FileType.CSV: 'csv'>
```

#### Signature

```python
@property
def type(self) -> FileType: ...
```

#### See also

- [FileType](#filetype)

### File().write

[Show source in file.py:614](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L614)

Write content to the file.

Ensures the parent directory exists before writing.

#### Arguments

- `content` *Any* - The content to write to the file. The type of content should match
    the file type (e.g., list of dicts for CSV, dict for JSON, string for text).
- `throw` *bool, optional* - Whether to throw exceptions on errors. Defaults to True.

#### Raises

- `IOError` - If there is an error writing to the file.

#### Examples

```python
>>> file = File('data.csv')
>>> file.write([{'col1': '1', 'col2': '2'}, {'col1': '3', 'col2': '4'}])
>>> file = File('data.json')
>>> file.write({'key': 'value', 'items': [1, 2, 3]})
>>> file = File('note.txt')
>>> file.write('hello world')
```

#### Signature

```python
def write(self, content: Any, throw: bool = True) -> None: ...
```



## FileType

[Show source in file.py:353](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L353)

Enumeration of file types.

#### Signature

```python
class FileType(Enum): ...
```

### FileType.get

[Show source in file.py:360](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L360)

Get the FileType from a file extension or type string.

Unknown types default to TEXT.

#### Arguments

file_type (FileType | str): The file extension (e.g., ".csv", ".json", ".txt"),
    or the file type string (e.g., "csv", "json", "txt"). If a FileType enum member
    is passed, it will be returned as is.

#### Returns

- [FileType](#filetype) - The corresponding FileType enum member.

#### Examples

```python
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
```

#### Signature

```python
@classmethod
def get(cls, file_type: FileType | str) -> FileType: ...
```



## ensure_directory

[Show source in file.py:27](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L27)

Ensure that the directory for the given path exists.

#### Arguments

path (Path | str): The file path for which to ensure the directory exists.

#### Examples

```python
>>> ensure_directory('data/archive.csv')
>>> Path('data').exists()
True
```

#### Signature

```python
def ensure_directory(path: Path | str) -> None: ...
```



## fetch_content

[Show source in file.py:74](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L74)

Fetch content from a URL.

#### Arguments

- `url` *str* - The URL to fetch content from.
- `binary` *bool, optional* - Whether to return content as bytes. Defaults to False.
timeout (int | tuple, optional): Timeout for the request. Defaults to (6, 30).
- `**kwargs` - Additional arguments to pass to requests

#### Returns

str | bytes: The content fetched from the URL.

#### Raises

- `requests.RequestException` - If the request fails.

#### Examples

```python
>>> content = fetch_content('https://example.com/data.txt')
>>> print(content)
'...'
>>> binary_content = fetch_content('https://example.com/image.png', binary=True)
>>> print(binary_content)
b'...'
```

#### Signature

```python
def fetch_content(
    url: str, binary: bool = False, timeout: int | tuple = (6, 30), **kwargs
) -> str | bytes: ...
```



## get_cache_path

[Show source in file.py:43](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L43)

Return the cache path, optionally creating it.

#### Arguments

folder (Path | str, optional): A subpath within the cache directory.
    Defaults to None.
- `create` *bool, optional* - Whether to create the directory if it does not exist.
    Defaults to False.

#### Returns

- `Path` - The cache path.

#### Raises

- `OSError` - If the directory cannot be created.

#### Examples

```python
>>> get_cache_path()
PosixPath('/home/user/.cache')
>>> get_cache_path('data', create=True)
PosixPath('/home/user/.cache/data')
```

#### Signature

```python
def get_cache_path(folder: Path | str = None, create: bool = False) -> Path: ...
```



## read_csv_file

[Show source in file.py:172](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L172)

Read a CSV file and return its content.

#### Arguments

- `file` *IO[str]* - The file object to read from. It must be opened in text mode.
- `dialect` *str, optional* - The CSV dialect to use. If "auto", it will be
    auto-detected. Defaults to "auto".
- `iterator` *bool, optional* - If True, returns an iterator instead of a list.
    Defaults to False.
- `sample_size` *int, optional* - The number of bytes to read for auto-detecting
    the CSV dialect. Defaults to CSV_SAMPLE_SIZE.
- `max_tries` *int, optional* - The maximum number of attempts to auto-detect the
    CSV dialect. Defaults to CSV_MAX_TRIES.
- `**kwargs` - Additional arguments to pass to csv.DictReader or csv.reader.

#### Returns

Iterable[dict | list]: An iterable of rows as dictionaries or lists.

#### Raises

- `csv.Error` - If there is an error reading the CSV file.

#### Examples

```python
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
```

#### Signature

```python
def read_csv_file(
    file: IO[str],
    dialect: str = "auto",
    iterator: bool = False,
    sample_size: int = CSV_SAMPLE_SIZE,
    max_tries: int = CSV_MAX_TRIES,
    **kwargs
) -> Iterable[dict | list]: ...
```

#### See also

- [CSV_MAX_TRIES](#csv_max_tries)
- [CSV_SAMPLE_SIZE](#csv_sample_size)



## read_zip_file

[Show source in file.py:107](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L107)

Read a specific file from a ZIP archive in memory.

#### Arguments

- `file` *IO[bytes]* - The file object of the ZIP archive. It must be opened in binary mode.
- `filename` *str, optional* - The exact filename to extract. Defaults to None.
- `ext` *str, optional* - The file extension to filter by if filename is not provided.
    Defaults to None.
encoding (str | None, optional): The encoding to decode the file content.
    If None, returns bytes. Defaults to None.
decoding_errors (Literal["ignore", "strict", "replace"], optional): The error
    handling scheme for decoding. Defaults to "ignore".

#### Returns

bytes | str: The content of the extracted file.

#### Raises

- `FileNotFoundError` - If no file matches the given criteria.

#### Examples

```python
>>> with open('archive.zip', 'rb') as f:
...     content = read_zip_file(f, filename='data.csv', encoding='utf-8')
>>> print(content)
'col1,col2\n1,2\n3,4'
>>> with open('archive.zip', 'rb') as f:
...     content = read_zip_file(f, ext='.json')
>>> print(content)
b'{"key": "value"}'
```

#### Signature

```python
def read_zip_file(
    file: IO[bytes],
    filename: str = None,
    ext: str = None,
    encoding: str | None = None,
    decoding_errors: Literal["ignore", "strict", "replace"] = "ignore",
) -> bytes | str: ...
```



## write_csv_file

[Show source in file.py:247](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L247)

Write data to a CSV file.

#### Arguments

- `file` *IO[str]* - The file object to write to. It must be opened in text mode.
data (Iterable[dict | list]): The data to write, as an iterable of dictionaries or lists.
fieldnames (list[str] | None, optional): The field names to use if data is an iterable of
    dictionaries. If None, field names will be inferred from the first dictionary.
    Defaults to None.
- `dialect` *str, optional* - The CSV dialect to use. Defaults to "excel".
- `header` *bool, optional* - Whether to write the header row. Defaults to True.
- `**kwargs` - Additional arguments to pass to csv.DictWriter or csv.writer.

#### Raises

- `csv.Error` - If there is an error writing to the CSV file.

#### Examples

```python
>>> with open('output.csv', 'w', encoding='utf-8', newline='') as f:
...     write_csv_file(f, [{'col1': '1', 'col2': '2'}, {'col1': '3', 'col2': '4'}])
>>> with open('output.csv', 'w', encoding='utf-8', newline='') as f:
...     write_csv_file(f, [['col1', 'col2'], ['1', '2'], ['3', '4']])
```

#### Signature

```python
def write_csv_file(
    file: IO[str],
    data: Iterable[dict | list],
    fieldnames: list[str] | None = None,
    dialect: str = "excel",
    header: bool = True,
    **kwargs
) -> None: ...
```



## write_json_file

[Show source in file.py:319](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/file.py#L319)

Write data to a JSON file.

#### Arguments

- `file` *IO[str]* - The file object to write to. It must be opened in text mode.
- [Data](../data/index.md#data) *Any* - The data to write to the JSON file.
indent (int | str | None, optional): The indentation level for pretty-printing the JSON
    data. Defaults to None.
- `ensure_ascii` *bool, optional* - Whether to escape non-ASCII characters. Defaults to False.
- `**kwargs` - Additional arguments to pass to json.dump.

#### Raises

- `TypeError` - If the data cannot be serialized to JSON.

#### Examples

```python
>>> with open('output.json', 'w', encoding='utf-8') as f:
...     write_json_file(f, {'key': 'value'})
```

#### Signature

```python
def write_json_file(
    file: IO[str],
    data: Any,
    indent: int | str | None = None,
    ensure_ascii: bool = False,
    **kwargs
) -> None: ...
```