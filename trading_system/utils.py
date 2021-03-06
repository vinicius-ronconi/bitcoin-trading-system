from math import floor


def get_floor_in_satoshi_precision(value):
    return floor(value * 100000000) / 100000000


def get_rounded_decimal_value(value):
    return floor(value * 100) / 100
