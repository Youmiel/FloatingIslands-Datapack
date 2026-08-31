from pathlib import Path
import typing as ty

TYPE = 'json'

BIOME_NAMES = [
    'badlands',
    'bamboo_jungle',
    'beach',
    'birch_forest',
    'cold_ocean',
    'dark_forest',
    'deep_cold_ocean',
    'deep_frozen_ocean',
    'deep_lukewarm_ocean',
    'deep_ocean',
    'desert',
    'dripstone_caves',
    'eroded_badlands',
    'flower_forest',
    'forest',
    'frozen_ocean',
    'frozen_peaks',
    'frozen_river',
    'grove',
    'ice_spikes',
    'jagged_peaks',
    'jungle',
    'lukewarm_ocean',
    'lush_caves',
    'meadow',
    'mushroom_fields',
    'ocean',
    'old_growth_birch_forest',
    'old_growth_pine_taiga',
    'old_growth_spruce_taiga',
    'plains',
    'river',
    'savanna',
    'savanna_plateau',
    'snowy_beach',
    'snowy_plains',
    'snowy_slopes',
    'snowy_taiga',
    'sparse_jungle',
    'stony_peaks',
    'stony_shore',
    'sunflower_plains',
    'swamp',
    'taiga',
    'warm_ocean',
    'windswept_forest',
    'windswept_gravelly_hills',
    'windswept_hills',
    'windswept_savanna',
    'wooded_badlands',
]

def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
     -> ty.Union[ty.Tuple[str, Path, Path], ty.List[ty.Tuple[str, Path, Path]], None]:

    path_source_common = Path('vanilla_biomes/1_18_overworld')
    path_target_common = patch_path.parent / 'worldgen' / 'biome'
    
    process_files = []
    for biome_name in BIOME_NAMES:
        process_files.append(('COMMON', path_source_common / f'{biome_name}.json', path_target_common / f'{biome_name}.json'))

    return process_files


def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    for path, data in content:
        data['features'][4].append('floating_island:end_gateway_return_overworld')

        for key, item in data['carvers'].items():
            if len(item) == 1:
                data['carvers'][key] = data['carvers'][key][0]
    return content