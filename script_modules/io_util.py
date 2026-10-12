import dataclasses
import datetime
import enum
import json
import os
from pathlib import Path
import types
import typing as ty
import chardet


def get_charset(file_path: ty.Union[str, Path]) -> str:
    with open(file_path, 'br') as byte_content:
        return chardet.detect(byte_content.read())['encoding']


def read_json_dict(file_path: ty.Union[str, Path], charset: str) -> ty.Dict[str, ty.Any]:
    with open(file_path, 'r', encoding=charset) as json_file:
        return json.load(json_file)


def _slot_names(obj: ty.Any) -> ty.List[str]:
    names: ty.List[str] = []
    for cls in reversed(type(obj).__mro__):
        for name in getattr(cls, '__slots__', ()):
            if isinstance(name, str) and name not in names:
                names.append(name)
    return names


def _convert_object(obj: ty.Any) -> ty.Any:
    if isinstance(obj, enum.Enum):
        return obj.value
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    if isinstance(obj, os.PathLike):
        return os.fspath(obj)
    if isinstance(obj, (set, frozenset)):
        return sorted(obj, key=repr)
    if isinstance(obj, (type, types.ModuleType)) or callable(obj):
        raise TypeError(f'{type(obj).__name__} is not JSON serializable')
    if dataclasses.is_dataclass(obj):
        return {field.name: getattr(obj, field.name) for field in dataclasses.fields(obj)}
    if hasattr(obj, '__dict__'):
        return dict(vars(obj))
    slot_values = {name: getattr(obj, name) for name in _slot_names(obj) if hasattr(obj, name)}
    if slot_values:
        return slot_values
    raise TypeError(f'Object of type {type(obj).__name__} is not JSON serializable')


def _to_jsonable(obj: ty.Any, on_path: ty.Set[int]) -> ty.Any:
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    obj_id = id(obj)
    if obj_id in on_path:
        raise ValueError(f'Circular reference detected: {type(obj).__name__}')
    on_path.add(obj_id)
    try:
        if isinstance(obj, dict):
            return {key: _to_jsonable(value, on_path) for key, value in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_to_jsonable(value, on_path) for value in obj]
        return _to_jsonable(_convert_object(obj), on_path)
    finally:
        on_path.discard(obj_id)


def write_json_dict(content: ty.Dict[ty.Any, ty.Any], file_path: ty.Union[str, Path], charset: str = 'utf8'):
    jsonable = _to_jsonable(content, set())
    with open(file_path, 'w', encoding=charset) as json_file:
        json.dump(jsonable, json_file, indent=2, allow_nan=False)
