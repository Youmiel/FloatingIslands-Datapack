# FloatingIslands-Datapack

A minecraft datapack that creates floating islands in overworld and the nether.

## Features

### Terrain Noise (1.18-)

Terrain noise in `overworld` and `the nether` is similar to `the end`, but sightly changed.

- **(1.16.x)** Overworld sea level has changed to 0 for better vegetation on overworld islands, also avoiding sea ravine from generating in the void

- **(1.17.x)** Overworld sea level has changed to 32 for better vegetation on overworld islands

### Terrain Noise (1.18+)

Overworld terrain noise has completely rewrote to match 1.18 world height. 

Terrain noise in `the nether` is similar to `the end`, but sightly changed.

  - Nether terrain surface is sightly rougher than `the end`

### Minecraft 26.2

The experimental 26.2 build uses pack format `107.1` and updates the
world-generation registries for the new version.

- The overworld keeps a continuous main island, a protected void ring, and
  smaller End-style outer islands.
- Frozen and deep-frozen ocean replacements retain 26.2 biome content without
  generating oversized floating icebergs.
- The replacement frozen-ocean biomes are excluded from structure eligibility
  tags that could place large structures directly in the protected void.
- Terrain adaptation is disabled for structures that would otherwise create
  artificial terrain islands in the protected void.
- Return gateways are registered through structure sets and target
  `(0, 90, 0)` in their current dimension.

Use this build only when creating a new world. Back up long-running worlds and
avoid other world-generation datapacks during initial testing.

### End Gateways

End gateways are distributed randomly in `overworld` and `the nether`.
Legacy builds target (0,0); the 26.2 build targets `(0, 90, 0)` in the current
dimension.

Below are the biomes that end gateways may generate:
  - deep_ocean
  - desert
  - forest
  - windswept_hills (1.18+) or minecraft:mountains (1.18-)
  - ocean
  - plains
  - savanna
  - swamp
  - taiga
  - basalt_deltas
  - nether_wastes
  - soul_sand_valley
  - **warped_forest** (*highest density*)
  - end_highlands (*vanilla datapack*)

## Usage

Load it with correct version of Minecraft(Java Edition) before world generation, and enjoy the game `:)`
