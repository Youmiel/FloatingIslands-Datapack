from pathlib import Path
import typing as ty

TYPE = 'json'

BIOME_NAMES = [
    'basalt_deltas',
    # 'crimson_forest',
    'nether_wastes',
    'soul_sand_valley',
    'warped_forest'
]

def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
     -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:

    path_source_common = Path('vanilla_biome/1_19_4_nether')
    path_target_common = patch_path.parent / 'worldgen' / 'biome'
    
    process_files = []
    for biome_name in BIOME_NAMES:
        process_files.append(('COMMON', path_source_common / f'{biome_name}.json', path_target_common / f'{biome_name}.json'))

    return process_files


def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    for path, data in content:
        if path.stem == 'warped_forest':
            data['features'][4].append('floating_island:end_gateway_return_warped')
        else:
            data['features'][4].append('floating_island:end_gateway_return_nether')
    return content