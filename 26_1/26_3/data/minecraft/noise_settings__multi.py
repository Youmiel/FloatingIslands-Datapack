from pathlib import Path
import typing as ty

TYPE = 'json'


def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
        -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:

    path_source_common = Path('vanilla_noise') / '26_3'
    path_target_common = patch_path.parent / 'worldgen' / 'noise_settings'

    return [
        ('COMMON', path_source_common / '26_3_end.json', path_target_common / 'end_1.json'),
        ('COMMON', path_source_common / '26_3_end.json', path_target_common / 'end_2.json'),
        ('COMMON', path_source_common / '26_3_overworld.json', path_target_common / 'overworld.json'),
        ('COMMON', path_source_common / '26_3_nether.json', path_target_common / 'nether.json'),
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
        data['default_fluid'] =  'minecraft:air'    # TODO: test if this is necessary since aquifers are removed

        # dimension specific settings
        if path.stem == 'overworld':
            del data['aquifers']   # 26.3 new: optional aquifer

            end_final_density = end_1['noise_router']['final_density']
            end_final_density['left']['input']['cell_size_xz'] = 8
            end_final_density['left']['input']['cell_size_y'] = 8
            end_final_density['left']['input']['input']['left']['input']['alpha']['from_coordinate'] = -64
            end_final_density['left']['input']['input']['left']['input']['alpha']['to_coordinate'] = 48
            end_final_density['left']['input']['input']['left']['input']['second']['alpha']['from_coordinate'] = 56
            end_final_density['left']['input']['input']['left']['input']['second']['alpha']['to_coordinate'] = 568
            end_final_density['left']['input']['input']['left']['input']['second']['second'] = 'floating_island:overworld/sloped_cheese'
            data['noise_router']['final_density'] = end_final_density

            data['noise']['min_y'] = -48
            data['noise']['height'] = 144

            data['material_rule'] = 'floating_island:overworld'

            data['spawn_target'] = []
        elif path.stem == 'nether':
            end_final_density = end_2['noise_router']['final_density']
            data['noise_router']['final_density'] = end_final_density
            # noise cell size is integrated into final_denstiy function in 26.3
        else:
            pass
    return modified_content
