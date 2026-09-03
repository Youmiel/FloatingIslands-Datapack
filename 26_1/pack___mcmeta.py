from pathlib import Path
import typing as ty

TYPE = 'json'

FORMAT_RANGE = { "min_format": [100, 0], "max_format": [107, 1] }
# 26.1 snapshot-11 ~ 26.2 snapshot-3, 26.2 snapshot-5 ~ ? (26.2)
OVERLAYS = [
    {
        'directory': '26_2_biome',    # 26.2 snapshot-3 ~ ? (26.2) 
        'min_format': [102, 0],
        'max_format': [107, 1]
    },
    {
        'directory': '26_2_noise',    # 26.2 snapshot-5 ~ ? (26.2)
        'min_format': [104, 0],
        'max_format': [107, 1]
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