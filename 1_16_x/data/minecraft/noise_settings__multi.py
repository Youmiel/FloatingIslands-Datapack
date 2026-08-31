from pathlib import Path
import typing as ty

TYPE = 'json'


def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
        -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:

    path_source = Path('vanilla_noise/1_16_floating_islands.json')
    path_target_common = patch_path.parent / 'worldgen' / 'noise_settings'

    return [
        ('COMMON', path_source, path_target_common / 'overworld.json'),
        ('COMMON', path_source, path_target_common / 'nether.json')
    ]


def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    for path, data in content:
        data['noise'].pop('island_noise_override', None)
        data['noise'] = {'island_noise_override': True, **data['noise']}
        data['noise']['density_factor'] = 0.1
        data["noise"]["top_slide"] = {
            "target": -800,
            "size": 32,
            "offset": -14,
        }
        data["default_fluid"] = {"Name": "minecraft:air"}

        # dimension specific settings
        if path.stem == 'overworld':
            data['default_block']['Name'] = 'minecraft:stone'
        elif path.stem == 'nether':
            data['default_block']['Name'] = 'minecraft:netherrack'
            data['structures'].pop('stronghold', None)
            data['structures']['structures']['minecraft:ruined_portal']['separation'] = 10
            data['structures']['structures']['minecraft:ruined_portal']['spacing'] = 25
        else:
            pass
    return content
