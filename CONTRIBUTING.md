# Contributing

Contributions are welcome! The build system is a small Python program with a single third-party dependency (`chardet`), so any Python 3 runtime can run it. Run the scripts from the project root:

```
python build.py     # build and pack every version
python clean.py     # remove __pycache__ folders
```

Only patcher files and the vanilla sources they need are tracked. Those sources are the minimal set of original files picked from vanilla data to satisfy the pack build, and they all live in `common/`; the full extracted vanilla data stays in the git-ignored `ref/`, generated packs in the git-ignored `build/`.

## How to update this datapack

1. extract new and old version worldgen data into `ref/`.
2. compare worldgen data between versions with any diff tools, understand changes, especially biome data, noise_settings and density functions. `json_diff.py` is a minimal helper that only reports differing paths, so keep using your usual diff tools alongside it.
3. If there are minor changes, create `x_patch/` in `common/` and add changed vanilla data files, then write patcher files.
4. If there are major changes, create `x_y_z/` in `common/` and add a group of changed vanilla data files (e.g. biomes, noise settings), then write patcher files.
5. Currently new versions use sub-pack override, no matter how much the new version changes. This is a requirement of the datapack overlay format, the `common/` files above are just the vanilla sources read by the patchers.
6. Must test before release. `python build.py` only produces the builds, it does not test them; build the test environment yourself, e.g. a server and a client of the target MC version.

## Patcher files

A patcher is a Python module placed anywhere in a version directory. `TYPE`, `reference_file` and `process_single` / `process_multi` form its interface, documented in `script_modules/template/json_patcher.py`.

- the file name is the target file name, with `.` written as `___`, e.g. `pack___mcmeta.py` generates `pack.mcmeta`.
- a reference may only read the build output of an older version (`MC_*` constants in   `build_settings.py`), static files of the current version (`MC_0`) or `common/` (`COMMON`). Versions are built in the order they are declared in `build_settings.py`.
