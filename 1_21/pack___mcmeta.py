from pathlib import Path
import typing as ty

TYPE = 'json'

SUPPORTED = { "min_inclusive": 42, "max_inclusive": 81 }
# 24w18a ~ 24w33a ~ 24w44a ~ 1.21.8 

OVERLAYS = [
    {
        'directory': '1_21_2',
        'formats': { 'min_inclusive': 49, 'max_inclusive': 57 },
        # 24w33a ~ 24w44a (exclusive)
    },
    {
        'directory': '1_21_4',
        'formats': { 'min_inclusive': 58, 'max_inclusive': 64 },
        # 24w44a ~ 25w05a (exclusive)
    },
    {
        'directory': '1_21_5',
        'formats': { 'min_inclusive': 65, 'max_inclusive': 81 },
        # 25w05a ~ 1.21.8
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
    json_content['pack']['supported_formats'] = SUPPORTED
    json_content['overlays'] = { 'entries': OVERLAYS }
    json_content['pack']['version'] = version_cache
    return (new_path, json_content)

def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    return []