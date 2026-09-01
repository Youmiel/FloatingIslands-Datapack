from pathlib import Path
import typing as ty

TYPE = 'json'


def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
        -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:

    path_source_common = Path('vanilla_noise')
    path_target_common = patch_path.parent / 'worldgen' / 'noise_settings'

    return [
        ('COMMON', path_source_common / '1_18_2_overworld.json', path_target_common / 'overworld.json'),
        ('COMMON', path_source_common / '1_18_2_nether.json', path_target_common / 'nether.json')
    ]


def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    for path, data in content:
        data['aquifers_enabled'] = False
        data['default_fluid'] = {'Name': 'minecraft:air'}

        data['noise']['terrain_shaper'] = {
            'offset': 0.0,
            'factor': 0.0,
            'jaggedness': 0.0,
        }    # TODO: verify if this item is necessary
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
            data['legacy_random_source'] = False
            data['default_block']['Name'] = 'minecraft:stone'

            data['noise']['size_horizontal'] = 2
            data['noise']['size_vertical'] = 2
            data['noise']['min_y'] = -48
            data['noise']['height'] = 144

            data['noise']['top_slide']['offset'] = -59
            data['noise']['bottom_slide']['size'] = 14
            data['noise']['bottom_slide']['offset'] = -2

            data['noise']['sampling'] = {
                'xz_scale': 4.0,
                'y_scale': 2.0,
                'xz_factor': 80.0,
                'y_factor': 160.0,
            }

            final_density_arg1 = data['noise_router']['final_density']['argument1']
            final_density_arg1['argument']['argument2']['argument']['argument']['argument'] = "minecraft:overworld/sloped_cheese_override"
            data['noise_router']['final_density'] = final_density_arg1
            
            data['surface_rule']['sequence'][0]['if_true']['true_at_and_below']['above_bottom'] = -16
            data['surface_rule']['sequence'][0]['if_true']['false_at_and_above']['above_bottom'] = -11
        elif path.stem == 'nether':
            data['legacy_random_source'] = True
            data['default_block']['Name'] = 'minecraft:netherrack'

            data['noise']['terrain_shaper']['factor'] = 1.0

            data['noise']['size_horizontal'] = 2
            data['noise']['size_vertical'] = 1

            data['noise']['sampling'] = {
                'xz_scale': 2.0,
                'y_scale': 1.0,
                'xz_factor': 80.0,
                'y_factor': 160.0,
            }
            data['noise_router']['final_density']['argument']['argument2']['argument']['argument']['argument'] = "minecraft:end/sloped_cheese"
        else:
            pass
    return content
