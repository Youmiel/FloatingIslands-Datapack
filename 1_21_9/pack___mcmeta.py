from pathlib import Path
import typing as ty

TYPE = 'json'

FORMAT_RANGE = { "min_format": [82, 0], "max_format": [94, 1] }
# 25w31a ~ 25w42a, 25w45a ~ 1.21.11
OVERLAYS = [
    {
        'directory': '1_21_9',    # 25w31a ~ 25w42a (exclusive)
        'min_format': [82, 0],
        'max_format': [89, 0]
    },
    {
        'directory': '1_21_11',    # 25w45a ~ 1.21.11
        'min_format': [93, 0],
        'max_format': [94, 1]
    },
]

version_cache = '0.0.0'

def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
        -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:
    global version_cache
    file_name = patch_path.with_suffix('').with_name(patch_path.stem.replace('___','.'))
    version_cache = patch_version_config['version']

    return ('COMMON', Path('pack.mcmeta'), file_name)

def process_single(content: ty.Tuple[Path, ty.Dict]) -> ty.Tuple[Path, ty.Dict]:
    new_path, json_content = content
    json_content['pack'].pop('pack_format')
    json_content['pack'].update(FORMAT_RANGE)
    json_content['overlays'] = { 'entries': OVERLAYS }
    json_content['pack']['version'] = version_cache
    return (new_path, json_content)

def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    return []