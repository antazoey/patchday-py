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


def _write_data_model(file: Path, model: BASEMODEL_T) -> None:
    data = model.model_dump_json()
    _write_data_str(file, data)


def _write_data(file: Path, data: list | dict) -> None:
    data_str = json.dumps(data)
    _write_data_str(file, data_str)


def _write_data_str(file: Path, data: str) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    file.unlink(missing_ok=True)

    if not data.endswith("\n"):
        data += "\n"

    file.write_text(data, encoding="utf-8")


class ManagedData:
    def __init__(self, key: str, base_path: Path):
        self.key = key
        self.base_path = base_path

    @property
    def path(self) -> Path:
        return self.base_path / f"{self.key}.json"

    def load_list(self, model_cls: type[BASEMODEL_T], **kwargs) -> list[BASEMODEL_T]:
        items: list[dict] = self._load_data([])

        for item in items:
            for key, val in kwargs.items():
                item[key] = val

        return [model_cls.model_validate(obj) for obj in items]

    def load_object(self, model_cls: type[BASEMODEL_T]) -> BASEMODEL_T:
        item: dict = self._load_data({})
        return model_cls.model_validate(item)

    def persist_list(self, items: list[BASEMODEL_T]):
        data = [itm.model_dump(mode="json") for itm in items]
        _write_data(self.path, data)

    def persist_list_object(self, item: BASEMODEL_T, id_key: str = "id"):
        items = _load_file(self.path, self.key, [])
        data = item.model_dump(mode="json")

        # Remove existing.
        if existing := [x for x in items if x[id_key] == getattr(item, id_key)]:
            items = [x for x in items if x not in existing]

        items.append(data)
        _write_data(self.path, items)

    def persist_object(self, item: BASEMODEL_T):
        _write_data_model(self.path, item)

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
