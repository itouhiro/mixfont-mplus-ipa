# -*- coding: utf-8 -*-
# <usage: fontforge -script clamp.py 1p regular w3 regular
import sys
import fontforge
import config

fontforge.setPrefs('CoverageFormatsAllowed', 1)

middlefamily = sys.argv[1].lower()
weight = sys.argv[2].lower()
familyPostfix = sys.argv[3].lower()
subfamily = sys.argv[4].lower()
is_monospace = middlefamily[1] == 'm'

# create font
src_ttf_file = 'work.d/circle-mplus-%s-%s.ttf' % (middlefamily, weight)
f = fontforge.open(src_ttf_file)
print('input:'+src_ttf_file)
f.encoding = 'unicode4'
f.hasvmetrics = True

if subfamily == 'bold':
    try:
        f.os2_stylemap = int('0000100000', 2) # bold
    except Exception as message:
        print(message)
else:
    # subfamily = 'Regular'
    try:
        f.os2_stylemap = int('0001000000', 2) # regular
    except Exception as message:
        print(message)
family = 'Clamp %s %s' % (middlefamily, familyPostfix.upper())
postscript = 'clamp-%s-%s-%s' % (middlefamily, familyPostfix, subfamily)
styling_group = family
if subfamily == 'regular':
    fullname = family
else:
    fullname = ("%s %s" % (family, subfamily.capitalize()))
copyright = "Copyright(c) %s %s" % (config.year, config.author)
f.fontname = postscript
f.familyname = styling_group
f.fullname = fullname
f.weight = subfamily.capitalize()
f.copyright = copyright
f.version = config.version
sfnt_names = [
    ('English (US)', 'Copyright', copyright),
    ('English (US)', 'Family', styling_group),
    ('English (US)', 'SubFamily', subfamily),
    ('English (US)', 'Fullname', fullname),
    ('English (US)', 'Version', 'Version %s' % config.version),
    ('English (US)', 'PostScriptName', postscript),
    ('English (US)', 'Vendor URL', config.url),
    ('Japanese', 'Copyright', copyright),
    ('Japanese', 'Family', styling_group),
    ('Japanese', 'SubFamily', subfamily),
    ('Japanese', 'Fullname', fullname),
    ('Japanese', 'Version', 'Version %s' % config.version),
    ('Japanese', 'Vendor URL', config.url),
]
for k, v in config.license.items():
    sfnt_names.append((k, 'License', v))
f.sfnt_names = tuple(sfnt_names)
panose = [
    2, # 0-Family Kind: 2-Latin Text
    11, # 1-Serif Style: 11-Normal Sans
    0, # 2-Weight
    3, # 3-Proportion: 3-Modern
    2, # 4-Contrast: 2-None
    2, # 5-Stroke Variation: 2-No Variation
    3, # 6-Arm Style: 3-Straight Arms/Wedge
    2, # 7-Letterform: 2-Normal/Contact
    2, # 8-Midline: 2-Standard
    4, # 9-X-height: 4-Constant/Large
]
panose[2] = {
    "black": 8,
    "heavy": 8,
    "bold": 7,
    "medium": 6,
    "regular": 5,
    "light": 4,
    "thin": 2,
}[subfamily]
if middlefamily[1:] == 'p':
    if weight in ('light', 'thin'):
        panose[3] = 2 # 3-Proportion: 2-Old Style
else:
    panose[6] = 4 # 6-Arm Style: 4-Straight Arms/Vertical
if is_monospace:
    panose[3] = 9 # 3-Proportion: 9-Monospace
    f.os2_family_class = 8 * 256 + 9
else:
    f.os2_family_class = 8 * 256 + 6
f.os2_weight = {
    "black": 900,
    "heavy": 800,
    "bold": 700,
    "medium": 500,
    "regular": 400,
    "light": 300,
    "thin": 100,
}[subfamily]
f.os2_panose = tuple(panose)
f.os2_vendor = config.os2_vendor
f.os2_winascent_add = 0
f.os2_windescent_add = 0
f.hhea_ascent_add = 0
f.hhea_descent_add = 0
f.os2_winascent = 1075
f.os2_windescent = 320
f.hhea_ascent = 1075
f.hhea_descent = -320
f.hhea_linegap = 90
if is_monospace:
    f.os2_winascent = 880
    f.os2_windescent = 230
    f.hhea_ascent = 880
    f.hhea_descent = -230
    f.hhea_linegap = 0
else:
    f.os2_winascent = 1075
    f.os2_windescent = 320
    f.hhea_ascent = 1075
    f.hhea_descent = -320
    f.hhea_linegap = 90

dst_ttf_file = 'work.d/' + postscript + '.ttf'
# dst_ttf_file = 'work.d/' + postscript + '(' + weight + ').ttf'
f.generate(dst_ttf_file, '', ('short-post', 'opentype', 'PfEd-lookups', 'no-hints'))
print('output:'+dst_ttf_file)
