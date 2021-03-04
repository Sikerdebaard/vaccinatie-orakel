from babel.numbers import format_decimal
import math


def human_format(num, decimals=1):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    num = round(num, decimals)
    
    # remove x.0 from rounded float
    if int(num) == num:
        num = int(num)
    
    indicators = ['', 'K', 'M', 'B', 'T']
    return f'{fnum(num)}{indicators[magnitude]}'


def progressbar(pct, l=15, style='🟩⬜️', decimals=2):
    out = ''
    for i in range(0, l):
        if pct >= (100 / l * (i+1)):
            out += style[0]
        else:
            out += style[1]
    return f'{out} {fnum(pct, decimals)}%'


def fnum(x, decimals=None):
        if math.isinf(x):
            return '∞'

        if decimals is None:
            return format_decimal(x, locale="nl_NL")
        else:
            return format_decimal(round(x, decimals), locale="nl_NL", decimal_quantization=False)

