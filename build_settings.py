COMMON_PATH = 'common/'
BUILD_PATH = 'build/'
SAME_VERSION = 'MC_0'

EXTRA_FILE = ['README.md', 'LICENSE'] 
# relative to project root

EXCLUDE_FILE = ['spyglass.json'] 
# relative to version source root

# The namings: use the first supported MC version as version name, to easily maintaining version compatibility
# i.e. when a new MC version is released and be compatible with the previous pack version, the source code does not need to be renamed.

MC_1_16_X = {'path': '1_16_x/', 'name': 'FloatingIslands-Datapack_v{version}_1.16.x', 'version': '1.2.0'}
MC_1_17_X = {'path': '1_17_x/', 'name': 'FloatingIslands-Datapack_v{version}_1.17.x', 'version': '1.1.0'}
MC_1_18 = {'path': '1_18/', 'name': 'FloatingIslands-Datapack_v{version}_1.18', 'version': '2.0.2'}
MC_1_18_2 = {'path': '1_18_2/', 'name': 'FloatingIslands-Datapack_v{version}_1.18.2', 'version': '2.1.1'}
MC_1_19 = {'path': '1_19/', 'name': 'FloatingIslands-Datapack_v{version}_1.19', 'version': '3.0.2'}
MC_1_19_4 = {'path': '1_19_4/', 'name': 'FloatingIslands-Datapack_v{version}_1.19.4', 'version': '3.1.2'}
MC_1_20 = {'path': '1_20/', 'name': 'FloatingIslands-Datapack_v{version}_1.20', 'version': '3.2.1'}
MC_1_20_2 = {'path': '1_20_2/', 'name': 'FloatingIslands-Datapack_v{version}_1.20.2', 'version': '3.3.0'}
# MC_1_20_5- = {'path': '1_20_5/', 'name': 'FloatingIslands-Datapack_v{version}_1.20.5', 'version': '3.4.0'}
MC_1_21 = {'path': '1_21/', 'name': 'FloatingIslands-Datapack_v{version}_1.21', 'version': '3.5.0'}
MC_1_21_9 = {'path': '1_21_9/', 'name': 'FloatingIslands-Datapack_v{version}_1.21.9', 'version': '3.6.0'}
MC_26_1 = {'path': '26_1/', 'name': 'FloatingIslands-Datapack_v{version}_26.1', 'version': '3.6.0'}


def __collect_constant() -> dict:
    ret = {}
    global_temp = globals().copy()
    for key in global_temp:
        if key.startswith('MC_'):
            ret[key] = global_temp[key]
    # ret.pop(*['COMMON_PATH', 'BUILD_PATH', 'SAME_VERSION', 'EXTRA_FILE', 'EXCLUDE_FILE'])
    return ret

__VERSION_CONFIG = __collect_constant()
