# -*- coding: utf-8 -*-
import sys
import time
from datetime import date
import fontforge

fontforge.setPrefs('CoverageFormatsAllowed', 1)

dir_mplus = sys.argv[1]
dir_ipa = sys.argv[2]
# print('dir_mplus='+dir_mplus+', dir_ipa='+dir_ipa)

fontfile_ipa = ['IPAGothic-regular.sfd', 'IPAGothic-bold.sfd']
fontfile_mplus = ['mplus-1p-regular.ttf', 'mplus-1p-bold.ttf', 'mplus-1m-regular.ttf', 'mplus-1m-bold.ttf', 'mplus-2p-regular.ttf', 'mplus-2p-bold.ttf', 'mplus-2m-regular.ttf', 'mplus-2m-bold.ttf']

copyright_ipagothic = 'IPA Gothic Ver.003.03: Copyright(c) Information-technology Promotion Agency, Japan (IPA), 2003-2011. You must accept "http://ipafont.ipa.go.jp/ipa_font_license_v1.html" to use this product.'
license_ipagothic = 'IPA Font License Agreement v1.0'
license_url_ipagothic = 'http://ipafont.ipa.go.jp/ipa_font_license_v1.html'
today = date.today()
versionToday = '{0:04d}.{1:02d}{2:02d}'.format(today.year, today.month, today.day)
print('versionToday:Version '+versionToday)
# mplus_year = str(today.year)
mplus_year = '2019'

fontAdd = []
for i in [0,1]:
  print('fontAdd['+str(i)+'] open:'+dir_ipa + '/' + fontfile_ipa[i])
  fontAdd.append(fontforge.open(dir_ipa + '/' + fontfile_ipa[i]))
  fontAdd[i].encoding = 'unicode4'

def pickSfntName(sfntNames, search):
  for j in range(0,len(sfntNames)):
    if sfntNames[j][0] == 'English (US)' and sfntNames[j][1] == search:
      break
  return sfntNames[j][2]

for i in range(0,len(fontfile_mplus)):

  # open mplus font
  fileBase = dir_mplus + '/' + fontfile_mplus[i]
  print('fontBase open:' + fileBase)
  fontBase = fontforge.open(fileBase)
  fontBase.encoding = 'unicode4'

  # get M+ version
  sfntNames = fontBase.sfnt_names
  ttf_version = pickSfntName(sfntNames, 'Version')
  mplus_version = "TESTFLIGHT " + ttf_version[10:]
  copyright_mplus = 'M+ ' + mplus_version + ': Copyright(c) ' + mplus_year + ' M+ FONTS PROJECT\n'
  copyright = copyright_mplus + copyright_ipagothic
  # print('copyright='+copyright)

  ## merge kanji
  unib = [] #unicode index
  unia = []
  ## get unicode numbers
  print('get unicode numbers')
  for g in fontBase.glyphs():
    if (0x20 <= g.unicode and g.unicode <= 0xEFFFF and not(g.unicode in unib)):
      unib.append(g.unicode)
  for g in fontAdd[i%2].glyphs():
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
      fontAdd[i%2].selection.select(u)
      fontAdd[i%2].copy()
      fontBase.selection.select(u)
      fontBase.paste()
  print('copied glyph number:{0:d}'.format(count))

  ## add zero-width character
  #   U+200B ZERO WIDTH SPACE
  #   U+2060 WORD JOINER (zero width non-breaking space)
  #   U+FEFF ZERO WIDTH NO-BREAK SPACE (Byte Order Mark)
  for u in (0x200B, 0x2060, 0xFEFF):
    g = fontBase.createChar(u)
    g.width = 0

  ## delete 'notdef' character
  fontBase.removeGlyph(-1,'.notdef')

  ## tidy up data
  print('tidy up')
  for g in fontBase.glyphs():
    g.removeOverlap()
    g.round()

  ## set font name
  weight = pickSfntName(sfntNames, 'SubFamily')
  w = fontfile_mplus[i].split('-')
  family = 'MigMix ' + w[1].upper()
  fullName = family + ' ' + weight
  postScriptName = (family.replace(' ','-') + '-' + weight).lower()
  unique_id = 'FontForge : '+family+' '+weight+' : '+versionToday
  print('family='+family)
  print('weight='+weight)
  print('fullName='+fullName)
  print('postScriptName='+postScriptName)
  print('unique_id='+unique_id)

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
      ('English (US)', 'Vendor URL', 'http://mix-mplus-ipa.osdn.jp/'),
      ('Japanese', 'Copyright', copyright),
      ('Japanese', 'Family', family),
      ('Japanese', 'SubFamily', weight),
      ('Japanese', 'Fullname', fullName),
      ('Japanese', 'Version', 'Version {0:s}'.format(versionToday)),
      ('Japanese', 'Vendor URL', 'http://mix-mplus-ipa.osdn.jp/'),
  )

  ## save font
  ttfname = postScriptName + '.ttf'
  fontBase.generate(ttfname, '', ('short-post', 'opentype', 'PfEd-lookups', 'no-hints'))
  print('Generate:' + ttfname)

  fontBase.close()
## End
