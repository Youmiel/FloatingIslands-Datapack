from pathlib import Path
import typing as ty

TYPE = 'json'


def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
        -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:

    path_source_common = Path('vanilla_noise')
    path_target_common = patch_path.parent / 'worldgen' / 'noise_settings'

    return [
        ('COMMON', path_source_common / '1_18_floating_islands.json', path_target_common / 'overworld.json'),
        ('COMMON', path_source_common / '1_18_nether.json', path_target_common / 'nether.json')
    ]


def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    for path, data in content:
        data['legacy_random_source'] = False                                # TODO: should nether be true?
        data['default_fluid'] = {'Name': 'minecraft:air'}
        
        data['noise'].pop('island_noise_override', None)
        data['noise'] = {'island_noise_override': True, **data['noise']}
        data['noise']['sampling'] = {
            # TODO: in 1.16/1.17/1.18.2, nether sampling scales are xz_scale = 2, y_scale = 1, not sure whether they should be the same
            'xz_scale': 4.0,
            'y_scale': 2.0,
            'xz_factor': 80.0,
            'y_factor': 160.0,
        }
        data['noise']['top_slide'] = {
            'target': -23.4375,
            'size': 64,
            'offset': -46,
        }
        data['noise']['bottom_slide']= {
            'target': -0.234375,
            'size': 7,
            'offset': 1,
        }

        # dimension specific settings
        if path.stem == 'overworld':
            data['default_block']['Name'] = 'minecraft:stone'
            data['noise']['size_horizontal'] = 2
            data['noise']['size_vertical'] = 2
            data['noise']['min_y'] = -48
            data['noise']['height'] = 144

            data['noise']['top_slide']['offset'] = -59
            data['noise']['bottom_slide']['size'] = 14
            data['noise']['bottom_slide']['offset'] = -2

            data['noise_caves_enabled'] = True
            data['noodle_caves_enabled'] = True
            data['ore_veins_enabled'] =True
            data['sea_level'] = 63
        elif path.stem == 'nether':
            data['default_block']['Name'] = 'minecraft:netherrack'
            data['noise']['size_horizontal'] = 2
            data['noise']['size_vertical'] = 1
        else:
            pass
    return content
