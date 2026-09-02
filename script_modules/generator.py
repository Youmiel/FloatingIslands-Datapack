import importlib
import os
import sys
import typing as ty
from pathlib import Path
from types import ModuleType
import zipfile
import zlib

from script_modules import file_util, io_util
from script_modules.resource_locator import VersionResourceManager


def get_source_full_path(key: str, relative_source: Path, res_manager: VersionResourceManager):
    if key is None:
        return Path(relative_source)
    elif key == 'COMMON':
        return res_manager.get_common_source_path(relative_source)
    else:
        return res_manager.get_built_file_path(key, relative_source)


def clean_directory(build_dir: ty.Union[str, Path]) -> bool:
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    if not file_util.clean_dir(build_dir):
        print('  Clean build directory fail.', file=sys.stderr)
        return False
    return True


def scan_sources(res_manager: VersionResourceManager, exclude_file_list: ty.List[str]):
    source_file_list: ty.List[str] = file_util.scan_folder(res_manager.get_current_version_root())

    patch_file_list, static_file_list = [], []
    patch_predicate, cache_predicate = file_util.extension_match('.py'), file_util.part_match('__pycache__')
    exclude_full_path_list = [os.path.join(res_manager.get_current_version_root(), path) for path in exclude_file_list]

    for filename in source_file_list:
        if patch_predicate(filename):
            patch_file_list.append(filename)
        elif not cache_predicate(filename) and filename not in exclude_full_path_list:
            static_file_list.append(filename)
        else:
            pass
    return (sorted(static_file_list), sorted(patch_file_list))


def collect_json(version_key: str, source: Path, patch_module: ModuleType, res_manager: VersionResourceManager):
    source_full_path = get_source_full_path(version_key, source, res_manager)
    charset = io_util.get_charset(source_full_path)
    return io_util.read_json_dict(source_full_path, charset)


def patch_json(rel_patch_path: Path, patch_module: ModuleType, res_manager: VersionResourceManager):
    raw_ref = patch_module.reference_file(rel_patch_path, res_manager.get_current_version_config())
    file_ref: ty.List[ty.Tuple[str, Path, Path]] = []
    if isinstance(raw_ref, tuple): # single file
        file_ref = [raw_ref]
    elif isinstance(raw_ref, list): # multi-file
        file_ref = raw_ref
    else: # None or other, ingore
        pass

    content_list: ty.List[ty.Tuple[Path, ty.Dict[str, ty.Any]]] = []
    for version_key, relative_source, target_path_o in file_ref:
        # to detect path type, we must get full path 
        source_full_path = get_source_full_path(version_key, relative_source, res_manager)
        if not source_full_path.exists():
            print(f'    Source file {source_full_path} not found, skip.', file=sys.stderr)
            continue
        if source_full_path.is_file():
            content_list.append(
                (target_path_o, collect_json(version_key, relative_source, patch_module, res_manager)))
        elif source_full_path.is_dir():
            for sub_path in sorted(source_full_path.glob('*.json')):
                if sub_path.is_file():
                    relative_source_file = relative_source / sub_path.name
                    target_file = target_path_o / sub_path.name
                    content_list.append(
                        (target_file, collect_json(version_key, relative_source_file, patch_module, res_manager)))
        else: # None or other, ingore
            pass

    modified_contents: ty.List[ty.Tuple[Path, ty.Dict]] = []
    if len(content_list) == 1:
        modified_contents = [patch_module.process_single(content_list[0])]
    elif len(content_list) > 1:
        modified_contents = patch_module.process_multi(content_list)
        
    for target_path_m, dict_content in modified_contents:
        full_target_path = res_manager.get_current_build_version_root().joinpath(target_path_m)
        os.makedirs(full_target_path.parent, exist_ok=True)
        io_util.write_json_dict(dict_content, full_target_path)


def process_patch(source_version_root: Path, patch_strpath: str, res_manager: VersionResourceManager):
    relative_patch_path = Path(patch_strpath).relative_to(source_version_root)
    module_name = '.'.join(Path(patch_strpath).with_suffix('').parts)
    patch_module = importlib.import_module(module_name)

    # only handles json now
    if patch_module.TYPE == 'json':
        patch_json(relative_patch_path, patch_module, res_manager)
    else:
        print(f'    Unhandled patch {relative_patch_path}')


def pack_zipfile(build_path: Path, result_root: Path, config: ty.Dict[str, str], extra_file_list: ty.List[str]):
    pack_name = config['name'].format(**config)
    pack_path = os.path.join(build_path, pack_name + '.zip')
    pack_path_temp = os.path.join(build_path, pack_name + '.zip.tmp')
    datapack_files = file_util.scan_folder(result_root)
    try:
        with zipfile.ZipFile(pack_path_temp, 'w') as pack_zip:
            for fpath in datapack_files:
                pack_zip.write(fpath, 
                                arcname=os.path.relpath(fpath, result_root),
                                compress_type=zipfile.ZIP_DEFLATED, 
                                compresslevel=zlib.Z_DEFAULT_COMPRESSION)
            for extra_file in extra_file_list:
                pack_zip.write(extra_file,
                                compress_type=zipfile.ZIP_DEFLATED, 
                                compresslevel=zlib.Z_DEFAULT_COMPRESSION)
        os.replace(pack_path_temp, pack_path)
        # shutil.move(pack_path_temp, pack_path)
    except OSError as e:
        print(e, file=sys.stderr)