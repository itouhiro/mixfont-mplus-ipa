# -*- coding: utf-8 -*-
import sys
import os.path
import time
from datetime import date
import fontforge
import config

fontforge.setPrefs('CoverageFormatsAllowed', 1)

family = 'Migu ' + sys.argv[1]
weight_lower = sys.argv[2]
print('family='+family)
print('weight(lowercase)='+weight_lower)

fonttype = '1p'
if 'VS' in family or 'BT' in family:
  fonttype = '1c'
elif 'DS' in family:
  fonttype = '2p'
else:
  fonttype = sys.argv[1].lower()

today = date.today()
versionToday = '{0:04d}.{1:02d}{2:02d}'.format(today.year, today.month, today.day)
print('versionToday:Version '+versionToday)
#mplus_year = str(today.year)
mplus_year = '2019'
copyright_mixer = 'mix: Copyright(c) ' + str(today.year) + ' itouhiro'
copyright_ipagothic = 'IPA Gothic Ver.003.03: Copyright(c) Information-technology Promotion Agency, Japan (IPA), 2003-2011. You must accept "http://ipafont.ipa.go.jp/ipa_font_license_v1.html" to use this product.\n'
license_ipagothic = 'IPA Font License Agreement v1.0'
license_url_ipagothic = 'http://ipafont.ipa.go.jp/ipa_font_license_v1.html'
copyright_droid = 'Droid Sans Version 1.00 build 114: Digitized data copyright © 2007, Google Corporation. Licensed under the Apache License, Version 2.0\n'
copyright_droid_bold = 'Droid Sans Version 1.00 build 113: Digitized data copyright © 2007, Google Corporation. Licensed under the Apache License, Version 2.0\n'
copyright_dejavu_sans = 'DejaVu Sans Condensed Version 2.33: Copyright (c) 2003 by Bitstream, Inc. All Rights Reserved. Copyright (c) 2006 by Tavmjong Bah. All Rights Reserved.\n'
copyright_bitter = 'Bitter Version 1.001: Copyright (c) 2011, Sol Matas (www.huertatipografica.com.ar), with Reserved Font Name "Bitter".  Licensed under the SIL Open Font License, Version 1.1\n'

fontfile_base = 'circle-mplus-' + fonttype + '-' + weight_lower + '.ttf'
path_basefont = fontfile_base
if not os.path.exists(path_basefont):
    path_basefont = 'work.d/' + fontfile_base
print('fontBase open:'+path_basefont)
fontBase = fontforge.open(path_basefont)
fontBase.encoding = 'unicode4'

def pickSfntName(sfntNames, search):
  for j in range(0,len(sfntNames)):
    if sfntNames[j][0] == 'English (US)' and sfntNames[j][1] == search:
      break
  return sfntNames[j][2]

## get M+ version
sfntNames = fontBase.sfnt_names
ttf_version = pickSfntName(sfntNames, 'Version')
mplus_version = "TESTFLIGHT " + ttf_version[10:]
copyright_mplus = 'M+ ' + mplus_version + ': Copyright(c) ' + mplus_year + ' M+ FONTS PROJECT\n'

## delete some CJK ambiguous characters for merging
ipagothic_del_glyph = []
if 'm-' in fontfile_base or 'mn-' in fontfile_base:
  # ´¨‖‘’“”
  # °′″
  # ΑΒΓΔΕΖΗΘ
  # ΙΚΛΜΝΞΟΠ
  # ΡΣΤΥΦΧΨΩ
  # αβγδεζηθ
  # ικλμνξοπ
  # ρστυφχψω
  # АБВГДЕЁЖ
  # ЗИЙКЛМНО
  # ПРСТУФХЦ
  # ЧШЩЪЫЬЭЮ
  # Я
  # абвгдеёж
  # зийклмно
  # прстуфхц
  # чшщъыьэю
  # я
  # ±×÷§√‰†‡
  # ¶№
  ipagothic_del_glyph = [ \
    0x00b4, 0x00a8, 0x2016, 0x2018, 0x2019, 0x201c, 0x201d, \
    0x00b0, 0x2032, 0x2033, \
    0x0391, 0x0392, 0x0393, 0x0394, 0x0395, 0x0396, 0x0397, 0x0398, \
    0x0399, 0x039a, 0x039b, 0x039c, 0x039d, 0x039e, 0x039f, 0x03a0, \
    0x03a1, 0x03a3, 0x03a4, 0x03a5, 0x03a6, 0x03a7, 0x03a8, 0x03a9, \
    0x03b1, 0x03b2, 0x03b3, 0x03b4, 0x03b5, 0x03b6, 0x03b7, 0x03b8, \
    0x03b9, 0x03ba, 0x03bb, 0x03bc, 0x03bd, 0x03be, 0x03bf, 0x03c0, \
    0x03c1, 0x03c3, 0x03c4, 0x03c5, 0x03c6, 0x03c7, 0x03c8, 0x03c9, \
    0x0410, 0x0411, 0x0412, 0x0413, 0x0414, 0x0415, 0x0401, 0x0416, \
    0x0417, 0x0418, 0x0419, 0x041a, 0x041b, 0x041c, 0x041d, 0x041e, \
    0x041f, 0x0420, 0x0421, 0x0422, 0x0423, 0x0424, 0x0425, 0x0426, \
    0x0427, 0x0428, 0x0429, 0x042a, 0x042b, 0x042c, 0x042d, 0x042e, \
    0x042f, \
    0x0430, 0x0431, 0x0432, 0x0433, 0x0434, 0x0435, 0x0451, 0x0436, \
    0x0437, 0x0438, 0x0439, 0x043a, 0x043b, 0x043c, 0x043d, 0x043e, \
    0x043f, 0x0440, 0x0441, 0x0442, 0x0443, 0x0444, 0x0445, 0x0446, \
    0x0447, 0x0448, 0x0449, 0x044a, 0x044b, 0x044c, 0x044d, 0x044e, \
    0x044f, \
    0x00b1, 0x00d7, 0x00f7, 0x00a7, 0x221a, 0x2030, 0x2020, 0x2021, \
    0x00b6, 0x2116]


def merge(fontfile_add, del_glyph):
  # file open
  path_addfont = fontfile_add
  if not os.path.exists(path_addfont):
    path_addfont = 'mig.d/sfd.d/' + fontfile_add
  print('fontAdd open:'+path_addfont)
  fontAdd = fontforge.open(path_addfont)
  fontAdd.encoding = 'unicode4'

  # delete some glyph
  print('delete glyphs')
  count = 0
  for u in del_glyph:
    #print('delete glyph:U+{0:04X}'.format(u))
    count += 1
    fontBase.selection.select(u)
    fontBase.clear()
  print('deleted glyph number:{0:d}'.format(count))

  ## merge
  unib = [] #unicode index
  unia = []
  ## get unicode numbers
  print('get unicode numbers')
  for g in fontBase.glyphs():
    if (0x20 <= g.unicode and g.unicode <= 0xEFFFF and not(g.unicode in unib)):
      unib.append(g.unicode)
  for g in fontAdd.glyphs():
    if (0x20 <= g.unicode and g.unicode <= 0xEFFFF and not(g.unicode in unia)):
      unia.append(g.unicode)
  ## merge: fontAdd -> fontBase
  print('copy glyphs')
  count = 0
  for u in unia:
    if (u in unib):
      pass
    else:
      #print('copy glyph:U+{0:04X}'.format(u))
      count += 1
      fontAdd.selection.select(u)
      fontAdd.copy()
      fontBase.selection.select(u)
      fontBase.paste()
  print('copied glyph number:{0:d}'.format(count))
  fontAdd.close()


# merge kanji
fontfile_add = ''
if 'ld' in weight_lower:
  fontfile_add = 'IPAGothic-bold.sfd'
else:
  fontfile_add = 'IPAGothic-regular.sfd'
merge(fontfile_add, ipagothic_del_glyph)


## merge latin1
if 'VS' in family:
  if 'ld' in weight_lower:
    fontfile_add = 'DejaVuSansCondensed-bold.sfd'
  else:
    fontfile_add = 'DejaVuSansCondensed-regular.sfd'
  import merge_dejavu_sans
  merge(fontfile_add, merge_dejavu_sans.del_glyph)
elif 'BT' in family:
  if 'ld' in weight_lower:
    fontfile_add = 'Bitr-bold.sfd'
  else:
    fontfile_add = 'Bitr-regular.sfd'
  import merge_bitter
  merge(fontfile_add, merge_bitter.del_glyph)
elif 'DS' in family:
  if 'ld' in weight_lower:
    fontfile_add = 'DroidSans-bold.sfd'
  else:
    fontfile_add = 'DroidSans-regular.sfd'
  import merge_droid_sans
  merge(fontfile_add, merge_droid_sans.del_glyph)


## delete 'notdef' character
fontBase.removeGlyph(-1,'.notdef')

## tidy up data
print('tidy up')
for g in fontBase.glyphs():
  g.removeOverlap()
  g.round()
if 'VS' in family or 'BT' in family:
  fontBase.os2_winascent = 1075
  fontBase.os2_windescent = 320
  fontBase.os2_typolinegap = 90
  fontBase.hhea_ascent = 1075
  fontBase.hhea_descent = -320
  fontBase.hhea_linegap = 90

## set font name
#weight = pickSfntName(sfntNames, 'SubFamily')
weight = weight_lower.capitalize()
fullName = family + ' ' + weight
postScriptName = (family.replace(' ','-') + '-' + weight).lower()
unique_id = 'FontForge : '+family+' '+weight+' : '+versionToday
print('weight='+weight)
print('fullName='+fullName)
print('postScriptName='+postScriptName)
print('unique_id='+unique_id)

if 'DS' in family:
  if 'ld' in weight:
     copyright = copyright_droid_bold + copyright_mplus + copyright_ipagothic
  else:
     copyright = copyright_droid + copyright_mplus + copyright_ipagothic
elif 'VS' in family:
  copyright = copyright_dejavu_sans + copyright_mplus + copyright_ipagothic
elif 'BT' in family:
  copyright = copyright_bitter + copyright_mplus + copyright_ipagothic
else:
  copyright = copyright_mplus + copyright_ipagothic
copyright += copyright_mixer

fontBase.fontname = postScriptName
fontBase.familyname = family
fontBase.fullname = fullName
fontBase.weight = weight
fontBase.copyright = copyright
fontBase.version = versionToday
fontBase.os2_vendor = 'Mig '
fontBase.sfnt_names = (
    ('English (US)', 'Copyright', copyright),
    ('English (US)', 'Family', family),
    ('English (US)', 'SubFamily', weight),
    ('English (US)', 'Fullname', fullName),
    ('English (US)', 'Version', 'Version {0:s}'.format(versionToday)),
    ('English (US)', 'PostScriptName', postScriptName),
    ('English (US)', 'License', license_ipagothic),
    ('English (US)', 'License URL', license_url_ipagothic),
    ('English (US)', 'Vendor URL', config.url),
    ('Japanese', 'Copyright', copyright),
    ('Japanese', 'Family', family),
    ('Japanese', 'SubFamily', weight),
    ('Japanese', 'Fullname', fullName),
    ('Japanese', 'Version', 'Version {0:s}'.format(versionToday)),
    ('Japanese', 'Vendor URL', config.url),
)

## save font
ttfname = postScriptName + '.ttf'
fontBase.generate(ttfname, '', ('short-post', 'opentype', 'PfEd-lookups', 'no-hints'))
print('Generate:' + ttfname)

fontBase.close()
## End
