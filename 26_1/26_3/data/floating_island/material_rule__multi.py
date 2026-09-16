from pathlib import Path
import typing as ty

TYPE = 'json'

patch_namespace = None

def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
        -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:
    global patch_namespace
    patch_namespace = patch_path.parent.name

    path_source_common = Path('vanilla_material_rule') / '26_3'
    path_target_common = patch_path.parent / 'worldgen' / 'material_rule'
    return [
        ('COMMON', path_source_common / '26_3_overworld.json', path_target_common / 'overworld.json'),
        ('COMMON', path_source_common / '26_3_bedrock_floor.json', path_target_common / 'bedrock_floor_overworld.json'),
    ]


def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    modified_content: ty.List[ty.Tuple[Path, ty.Dict]] = content

    for path, data in modified_content:
        if path.stem == 'overworld':
            data['sequence'][3] = 'minecraft:overworld/surface'
            data['sequence'][0] = f'{patch_namespace}:bedrock_floor_overworld'
        if path.stem == 'bedrock_floor':
            data['if_true']['true_at_and_below']['above_bottom'] = -16
            data['if_true']['false_at_and_above']['above_bottom'] = -11

    return modified_content