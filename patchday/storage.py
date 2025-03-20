import json
from pathlib import Path
from typing import TypeVar
from xdg_base_dirs import xdg_config_home
from pydantic import BaseModel

from patchday.exceptions import StorageCorruption


# Defaults to $HOME/.config/patchday (XDG standard).
DEFAULT_STORAGE_PATH = xdg_config_home() / "patchday"
T = TypeVar("T")
BASEMODEL_T = TypeVar("BASEMODEL_T", bound=BaseModel)


def _load_json(content: str, key: str, default: T) -> T:
    try:
        res = json.loads(content)
    except json.decoder.JSONDecodeError as err:
        raise StorageCorruption(key, f"{err}")

    if not isinstance(res, type(default)):
        raise StorageCorruption(key, "Unexpected type")

    return res


def _load_file(file: Path, key: str, default: T) -> T:
    if not file.is_file():
        return default

    content = file.read_text(encoding="utf-8")
    return _load_json(content, key, default)


def _write_data(file: Path, data: list | dict) -> None:
    file.write_text(json.dumps(data), encoding="utf-8")


class ManagedData:
    def __init__(self, key: str, base_path: Path):
        self.key = key
        self.base_path = base_path

    @property
    def path(self) -> Path:
        return self.base_path / f"{self.key}.json"

    def load_list(self, model_cls: type[BASEMODEL_T]) -> list[BASEMODEL_T]:
        items: list[dict] = self._load_data([])
        return [model_cls.model_validate(obj) for obj in items]

    def load_object(self, model_cls: type[BASEMODEL_T]) -> BASEMODEL_T:
        item: dict = self._load_data(self.key, {})
        return model_cls.model_validate(item)

    def persist_list_object(self, item: BASEMODEL_T):
        items = _load_file(self.path, self.key, [])
        items.append(item)
        _write_data(self.path, item)

    def persist_object(self, item: BASEMODEL_T):
        self.path.unlink(missing_ok=True)
        _write_data(self.path, item)

    def _load_data(self, default: T) -> T:
        return _load_file(self.path, self.key, default)

    def _get_path(
        self,
    ) -> Path:
        return self.base_path / f"{self.key}.json"


class PatchData:
    """
    PatchDay's storage manager.
    """

    def __init__(self, path: Path | None = None):
        self.path = path or DEFAULT_STORAGE_PATH

    def open(self, key: str) -> ManagedData:
        return ManagedData(key, self.path)
