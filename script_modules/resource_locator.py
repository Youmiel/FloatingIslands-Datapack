from pathlib import Path
import typing as ty


class VersionResourceManager():
    def __init__(
            self, 
            build_path: Path, 
            common_path: Path, 
            same_version_keyword: str, 
            version_config: ty.Dict[str, ty.Dict[str, str]]
        ):
        self.build_path = build_path
        self.common_path = common_path
        self.same_version_keyword = same_version_keyword
        self.version_config = version_config

        self._current_version = None
    
    def set_current_version(self, version_key: str):
        if version_key not in self.version_config:
            raise KeyError(f'The version {version_key} is not in config.')
        self._current_version = version_key

    def get_current_version(self) -> str:
        if self._current_version is None:
            raise RuntimeError('Current version is not set.')
        return self._current_version

# ?
    def get_current_version_config(self) -> ty.Dict[str, str]:
        return self.version_config[self.get_current_version()]

# # ?
#     def get_current_version_config_path(self) -> str:
#         return self.get_current_version_config()['path']
    def get_version_root(self, version_key: str) -> Path:
        if version_key == self.same_version_keyword:
            return Path(self.version_config[self.get_current_version()]['path'])
        return Path(self.version_config[version_key]['path'])

    def get_built_version_root(self, version_key: str) -> Path:
        return self.build_path / self.get_version_root(version_key)

    def get_current_version_root(self) -> Path:
        return self.get_version_root(self.get_current_version())

    def get_current_build_version_root(self) -> Path:
        return self.get_built_version_root(self.get_current_version())


    def get_common_source_path(self, resource: Path) -> Path:
        return self.common_path / resource

    def get_source_path(self, version_key: str, resource: Path) -> Path:
        return self.get_version_root(version_key) / resource

    def get_built_file_path(self, version_key: str, resource: Path) -> Path:
        return self.get_built_version_root(version_key) / resource


