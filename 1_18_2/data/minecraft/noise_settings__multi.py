from pathlib import Path
import typing as ty

TYPE = 'json'


def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
        -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:

    path_source_common = Path('vanilla_noise')
    path_target_common = patch_path.parent / 'worldgen' / 'noise_settings'

    return [
        ('COMMON', path_source_common / '1_18_2_end.json', path_target_common / 'end_1.json'),
        ('COMMON', path_source_common / '1_18_2_end.json', path_target_common / 'end_2.json'),
        ('COMMON', path_source_common / '1_18_2_overworld.json', path_target_common / 'overworld.json'),
        ('COMMON', path_source_common / '1_18_2_nether.json', path_target_common / 'nether.json')
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

        # data['noise']['terrain_shaper'] = {
        #     'offset': 0.0,
        #     'factor': 0.0,
        #     'jaggedness': 0.0,
        # }
        # maybe it is not appropriate/necessary to set to 0

        # end noise settings
        end_top = end_1['noise']['top_slide']
        end_bottom = end_1['noise']['bottom_slide']
        end_sampling = end_1['noise']['sampling']
        data['noise']['top_slide'].update(end_top)
        data['noise']['bottom_slide'].update(end_bottom)
        data['noise']['sampling'].update(end_sampling)

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

            data['noise']['sampling']['xz_scale'] = 4.0
            data['noise']['sampling']['y_scale'] = 2.0

            # final_density_arg1 = data['noise_router']['final_density']['argument1']
            # final_density_arg1['argument']['argument2']['argument']['argument']['argument'] = "minecraft:overworld/sloped_cheese_override"
            # data['noise_router']['final_density'] = final_density_arg1

            end_final_density = end_1['noise_router']['final_density']
            end_final_density['argument']['argument2']['argument']['argument']['argument'] = "minecraft:overworld/sloped_cheese_override"
            data['noise_router']['final_density'] = end_final_density
            
            data['surface_rule']['sequence'][0]['if_true']['true_at_and_below']['above_bottom'] = -16
            data['surface_rule']['sequence'][0]['if_true']['false_at_and_above']['above_bottom'] = -11
            surface_sequence = data['surface_rule']['sequence'][1]['then_run']
            data['surface_rule']['sequence'][1] = surface_sequence
        elif path.stem == 'nether':
            data['legacy_random_source'] = True
            data['default_block']['Name'] = 'minecraft:netherrack'

            data['noise']['terrain_shaper']['factor'] = 1.0

            data['noise']['size_horizontal'] = 2
            data['noise']['size_vertical'] = 1

            # data['noise_router']['final_density']['argument']['argument2']['argument']['argument']['argument'] = "minecraft:end/sloped_cheese"

            end_final_density = end_2['noise_router']['final_density']
            data['noise_router']['final_density'] = end_final_density
        else:
            pass
    return modified_content
