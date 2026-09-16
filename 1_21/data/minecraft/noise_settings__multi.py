from pathlib import Path
import typing as ty

TYPE = 'json'

def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
     -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:

    noise_settings_path = patch_path.parent / 'worldgen' / 'noise_settings'
    
    path_overworld_noise = noise_settings_path / 'overworld.json'
    path_nether_noise = noise_settings_path / 'nether.json'

    return [
        ('MC_1_19', path_overworld_noise, path_overworld_noise),
        ('MC_1_19', path_nether_noise, path_nether_noise)
    ]


def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    return content