from pathlib import Path
import typing as ty

TYPE = 'json'


def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
        -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:

    path_source_common = Path('vanilla_noise')
    path_target_common = patch_path.parent / 'worldgen' / 'noise_settings'

    return [
        ('COMMON', path_source_common / '1_21_9_end.json', path_target_common / 'end_1.json'),
        ('COMMON', path_source_common / '1_21_9_end.json', path_target_common / 'end_2.json'),
        ('COMMON', path_source_common / '1_21_9_overworld.json', path_target_common / 'overworld.json'),
        ('COMMON', path_source_common / '1_21_9_nether.json', path_target_common / 'nether.json')
    ]


def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    modified_content: ty.List[ty.Tuple[Path, ty.Dict]] = []

    # dirty hacks to get the end noise data
    end_1: ty.Dict = {}
    end_2: ty.Dict = {}
    for path, data in content:
        if path.stem == 'overworld' or path.stem == 'nether':
            modified_content.append((path, data))
        if path.stem == 'end_1':
            end_1 = data
        if path.stem == 'end_2':
            end_2 = data

    for path, data in modified_content:
        data['aquifers_enabled'] = False
        data['default_fluid'] = {'Name': 'minecraft:air'}

        # dimension specific settings
        if path.stem == 'overworld':
            ### TODO: Why did mojang remove this?
            # end_preliminary_surface = end_1['noise_router']['preliminary_surface_level']
            # end_preliminary_surface['density']['argument2']['argument2']['argument1']['from_y'] = -64
            # end_preliminary_surface['density']['argument2']['argument2']['argument1']['to_y'] = 48
            # end_preliminary_surface['density']['argument2']['argument2']['argument2']['argument2']['argument2']['argument1']['from_y'] = 56
            # end_preliminary_surface['density']['argument2']['argument2']['argument2']['argument2']['argument2']['argument1']['to_y'] = 568
            # data['noise_router']['preliminary_surface_level'] = end_preliminary_surface

            end_final_density = end_1['noise_router']['final_density']
            end_final_density['argument']['argument2']['argument']['argument']['argument2']['argument1']['from_y'] = -64
            end_final_density['argument']['argument2']['argument']['argument']['argument2']['argument1']['to_y'] = 48
            end_final_density['argument']['argument2']['argument']['argument']['argument2']['argument2']['argument2']['argument2']['argument1']['to_y'] = 568
            end_final_density['argument']['argument2']['argument']['argument']['argument2']['argument2']['argument2']['argument2']['argument2']['argument2'] = 'minecraft:overworld/sloped_cheese_override'
            data['noise_router']['final_density'] = end_final_density

            data['surface_rule']['sequence'][0]['if_true']['true_at_and_below']['above_bottom'] = -16
            data['surface_rule']['sequence'][0]['if_true']['false_at_and_above']['above_bottom'] = -11
            surface_rule_seq_item_body = data['surface_rule']['sequence'][1]['then_run']
            data['surface_rule']['sequence'][1] = surface_rule_seq_item_body

            data['noise']['size_horizontal'] = 2
            data['noise']['size_vertical'] = 2
            data['noise']['min_y'] = -48
            data['noise']['height'] = 144

            data['spawn_target'] = []
        elif path.stem == 'nether':
            ### TODO: Why did mojang remove this?
            # end_preliminary_surface = end_2['noise_router']['preliminary_surface_level']
            # data['noise_router']['preliminary_surface_level'] = end_preliminary_surface

            end_final_density = end_2['noise_router']['final_density']
            data['noise_router']['final_density'] = end_final_density

            data['noise']['size_horizontal'] = 2
            data['noise']['size_vertical'] = 1
        else:
            pass
    return modified_content
