# Configuration file for the optimisation. Only static global variables.
#
# For testing whether the config is sane, please add tests to `test_config.py`


def StripFreeParams(point):
    fixed_params = []
    for low, high in FIXED_RANGES:
        fixed_params += point[low:high]
    return fixed_params


DEFAULT_POINT = [
    70.0,
    170.0,
    205.,
    205.,
    280.,
    245.,
    305.,
    240.,
    40.0,
    40.0,
    150.0,
    150.0,
    2.0,
    2.0,
    80.0,
    80.0,
    150.0,
    150.0,
    2.0,
    2.0,
    87.,
    65.,
    35.,
    121,
    11.,
    2.,
    65.,
    43.,
    121.,
    207.,
    11.,
    2.,
    6.,
    33.,
    32.,
    13.,
    70.,
    11.,
    5.,
    16.,
    112.,
    5.,
    4.,
    2.,
    15.,
    34.,
    235.,
    32.,
    5.,
    8.,
    31.,
    90.,
    186.,
    310.,
    2.,
    55.,
]
FIXED_RANGES = [(0, 2), (8, 20)]
FIXED_PARAMS = StripFreeParams(DEFAULT_POINT)


RUN = 'discrete4'
POINTS_IN_BATCH = 10
RANDOM_STARTS = 10

MIN = [
    70.0, 170.0, 208, 207, 281, 248, 305, 242, 40.0, 40.0, 150.0, 150.0, 2.0,
    2.0, 80.0, 80.0, 150.0, 150.0, 2.0, 2.0, 72, 51, 29, 46, 10, 7, 54, 38, 46,
    192, 14, 9, 10, 31, 35, 31, 51, 11, 3, 32, 54, 24, 8, 8, 22, 32, 209, 35,
    8, 13, 33, 77, 85, 241, 9, 26
]

METADATA_TEMPLATE = {
    'user': {
        'tag': '',
        'params': []
    },
    'k8s': {}
}

