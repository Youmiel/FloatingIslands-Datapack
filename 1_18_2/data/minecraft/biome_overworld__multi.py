from pathlib import Path
import typing as ty

TYPE = 'json'

def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
        -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:
    dir_source = Path('vanilla_biomes/1_18_overworld')
    dir_target = patch_path.parent / 'worldgen' / 'biome'
    return ('COMMON', dir_source, dir_target)


def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    for path, data in content:
        data['features'][4].append('floating_island:end_gateway_return_overworld')

        for key, item in data['carvers'].items():
            if len(item) == 1:
                data['carvers'][key] = data['carvers'][key][0]
    return content