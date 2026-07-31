#!/usr/bin/env python3
"""Generate the 26.2 overworld dimension from Mojang's biome report.

Generate the source report with the official Minecraft 26.2 data generator,
then run:

    python tools/generate_26_2_overworld_dimension.py \
        generated/reports/biome_parameters/minecraft/overworld.json \
        26_2/data/minecraft/dimension/overworld.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


BIOME_REPLACEMENTS = {
    'minecraft:frozen_ocean': 'floating_island:frozen_ocean',
    'minecraft:deep_frozen_ocean': 'floating_island:deep_frozen_ocean',
}
EXPECTED_REPLACEMENT_COUNTS = {
    'minecraft:frozen_ocean': 2,
    'minecraft:deep_frozen_ocean': 2,
}


def generate_dimension(report: dict[str, Any]) -> dict[str, Any]:
    biomes = report['biomes']
    replacement_counts = {biome: 0 for biome in BIOME_REPLACEMENTS}

    for entry in biomes:
        biome = entry['biome']
        replacement = BIOME_REPLACEMENTS.get(biome)
        if replacement is not None:
            entry['biome'] = replacement
            replacement_counts[biome] += 1

    if replacement_counts != EXPECTED_REPLACEMENT_COUNTS:
        raise ValueError(
            'Unexpected 26.2 biome report contents: '
            f'expected {EXPECTED_REPLACEMENT_COUNTS}, got {replacement_counts}'
        )

    return {
        'type': 'minecraft:overworld',
        'generator': {
            'type': 'minecraft:noise',
            'biome_source': {
                'biomes': biomes,
                'type': 'minecraft:multi_noise',
            },
            'settings': 'minecraft:overworld',
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('report', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()

    with args.report.open(encoding='utf-8') as handle:
        report = json.load(handle)

    dimension = generate_dimension(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', encoding='utf-8') as handle:
        json.dump(dimension, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


if __name__ == '__main__':
    main()
