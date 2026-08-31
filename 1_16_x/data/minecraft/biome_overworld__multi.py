from pathlib import Path
import typing as ty

TYPE = 'json'

BIOME_NAMES = [
    'badlands',
    'badlands_plateau',
    'bamboo_jungle',
    'bamboo_jungle_hills',
    'beach',
    'birch_forest',
    'birch_forest_hills',
    'cold_ocean',
    'dark_forest',
    'dark_forest_hills',
    'deep_cold_ocean',
    'deep_frozen_ocean',
    'deep_lukewarm_ocean',
    'deep_ocean',
    'deep_warm_ocean',
    'desert',
    'desert_hills',
    'desert_lakes',
    'eroded_badlands',
    'flower_forest',
    'forest',
    'frozen_ocean',
    'frozen_river',
    'giant_spruce_taiga',
    'giant_spruce_taiga_hills',
    'giant_tree_taiga',
    'giant_tree_taiga_hills',
    'gravelly_mountains',
    'ice_spikes',
    'jungle',
    'jungle_edge',
    'jungle_hills',
    'lukewarm_ocean',
    'modified_badlands_plateau',
    'modified_gravelly_mountains',
    'modified_jungle',
    'modified_jungle_edge',
    'modified_wooded_badlands_plateau',
    'mountains',
    'mountain_edge',
    'mushroom_fields',
    'mushroom_field_shore',
    'ocean',
    'plains',
    'river',
    'savanna',
    'savanna_plateau',
    'shattered_savanna',
    'shattered_savanna_plateau',
    'snowy_beach',
    'snowy_mountains',
    'snowy_taiga',
    'snowy_taiga_hills',
    'snowy_taiga_mountains',
    'snowy_tundra',
    'stone_shore',
    'sunflower_plains',
    'swamp',
    'swamp_hills',
    'taiga',
    'taiga_hills',
    'taiga_mountains',
    'tall_birch_forest',
    'tall_birch_hills',
    'warm_ocean',
    'wooded_badlands_plateau',
    'wooded_hills',
    'wooded_mountains',
]

def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
     -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:

    path_source_common = Path('vanilla_biomes/1_16_overworld')
    path_target_common = patch_path.parent / 'worldgen' / 'biome'
    
    process_files = []
    for biome_name in BIOME_NAMES:
        process_files.append(('COMMON', path_source_common / f'{biome_name}.json', path_target_common / f'{biome_name}.json'))

    return process_files


def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    for path, data in content:
        data['features'][4].append('minecraft:end_gateway_return_overworld')
        # in 1.16/1.17, only 'minecraft' namespace works
    return content