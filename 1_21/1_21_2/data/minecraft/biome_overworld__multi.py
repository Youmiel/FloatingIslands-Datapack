from pathlib import Path
import typing as ty

TYPE = 'json'

def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
        -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:
    dir_source_1 = Path('vanilla_biomes/1_21_2_overworld')
    dir_target = patch_path.parent / 'worldgen' / 'biome'
    return [
        ('COMMON', dir_source_1, dir_target),
    ]


def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    content_map = {path: data for path, data in content}
    for path, data in content_map.items():
        data['features'][4].append('floating_island:end_gateway_return_overworld')
    return [(path, data) for path, data in content_map.items()]