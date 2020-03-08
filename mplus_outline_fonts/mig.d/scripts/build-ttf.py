# -*- coding: utf-8 -*-
import math
import sys
import os
import re
import psMat
import fontforge
import config

fontforge.setPrefs('CoverageFormatsAllowed', 1)

ttfname = sys.argv[1]
middlefamily, weight = os.path.splitext(ttfname)[0].split('-')[1:]
modules = sys.argv[2:]

is_monospace = middlefamily[1] == 'm'

ascent = 860
descent = 140
em = ascent + descent

kanji_scale = 0.98
kanji_matrix = psMat.compose(
    psMat.translate(-em / 2, -ascent + em / 2), psMat.compose(
    psMat.scale(kanji_scale),
    psMat.translate(em / 2, ascent - em / 2)))

svg_uni_name = re.compile('^u[0-9A-F]{4,5}$', re.IGNORECASE)
feature_name = re.compile('^([- 0-9a-zA-Z]{4})_(uni[0-9A-F]{4,5})$')

alt_glyphs = {}
def svgname_to_glyphname(name):
    if svg_uni_name.match(name):
        return (int(name[1:], 16),)
    m = feature_name.match(name)
    if m:
        tag = m.group(1)
        if tag == 'jp04':
            tag = 'jp90'
        name = m.group(2)
        tagged_name = "%s.%s" % (name, tag)
        if not (tag in alt_glyphs):
            alt_glyphs[tag] = []
        alt_glyphs[tag].append((name, tagged_name))
        return (-1, tagged_name)
    return (-1, name)

def import_svg(svgpath, svgfile):
    name, ext = os.path.splitext(os.path.basename(svgfile))
    if ext != '.svg':
        raise Exception('%s is not SVG file' % os.path.join(svgpath, svgfile))
    glyphname = svgname_to_glyphname(name)
    c = f.createChar(*glyphname)
    c.width = em
    c.vwidth = em
    c.clear()
    c.importOutlines(os.path.join(svgpath, svgfile),
        ('removeoverlap', 'correctdir'))
    f.selection.select(('more',), c)

def import_svgs(svgdir):
    for svgfile in os.listdir(svgdir):
        try:
            import_svg(svgdir, svgfile)
        except Exception as message:
            #print(message)
            pass

def import_kanji(moddir):
    for svgdir in os.listdir(moddir):
        import_svgs(os.path.join(moddir, svgdir))

glyph_name = re.compile(r'^(u|uni)?([0-9A-F]{4,5})$')
def get_glyph_by_name(name):
    if len(name) == 1 and ord(name) in f:
        return f[ord(name)]
    elif name == 'space':
        if ord(' ') in f:
            c = f[ord(' ')]
        else:
            c = f.createChar(ord(' '))
            c.width = em
            c.vwidth = em
        return c
    m = glyph_name.match(name)
    if m:
        ucode = int(m.group(2), 16)
        if ucode in f:
            c = f[ucode]
        else:
            c = f.createChar(ucode)
    else:
        if name in f:
            c = f[name]
        else:
            c = f.createChar(-1, name)
            c.width = em
            c.vwidth = em
    return c

charspaces_comment = re.compile(r'^#')
bearings_comment = re.compile(r'^###')
bearings_space = re.compile(r'^\s*$')
bearings_format = re.compile(r'(\+|w)?([-0-9]+)')
weights_position = {'black': 0, 'heavy': 1, 'bold': 2,
                    'medium': 3, 'regular': 4, 'light': 5, 'thin': 6}

def set_bearings_line(line, charspaces):
    splitted = line.split()
    position = weights_position[weight] * 2
    for s in splitted[1:]:
        if not bearings_format.match(s):
            raise Exception('format error: %s' % s)
    bearings = splitted[position + 1:position + 3]
    l, r = charspaces
    c = get_glyph_by_name(splitted[0])
    m = bearings_format.match(bearings[0])
    bearing = int(m.group(2))
    if m.group(1) == '+':
        c.left_side_bearing = c.left_side_bearing + bearing
    else:
        c.left_side_bearing = bearing + l
    m = bearings_format.match(bearings[1])
    bearing = int(m.group(2))
    if m.group(1) == '+':
        c.right_side_bearing = c.right_side_bearing + bearing
    elif m.group(1) == 'w':
        c.width = bearing
    else:
        c.right_side_bearing = bearing + r

def set_bearings(mod):
    charspaces_path = "../../../../svg.d/%s/charspaces" % mod
    bearings_path = "../../../../svg.d/%s/bearings" % mod
    if os.path.exists(charspaces_path):
        fp = open(charspaces_path, 'r')
        for line in fp:
            if charspaces_comment.match(line):
                continue
            if bearings_space.match(line):
                continue
            position = weights_position[weight] * 2
            splitted = line.split()
            charspaces = map(int, splitted[position:position + 2])
            break
        fp.close()
    else:
        charspaces = [0, 0]
    if os.path.exists(bearings_path):
        fp = open(bearings_path, 'r')
        line_count = 0
        for line in fp:
            line_count = line_count + 1
            if bearings_comment.match(line):
                continue
            if bearings_space.match(line):
                continue
            try:
                set_bearings_line(line, charspaces)
            except Exception as message:
                print(bearings_path, "line:", line_count)
                print(message)
        fp.close()

def set_vbearings_line(line):
    splitted = line.split()
    ch, method = splitted[0:2]
    h2v_shift = splitted[2:]
    c = get_glyph_by_name(ch)
    f.selection.select(c)
    f.copy()
    tag = 'vert'
    name = c.glyphname
    tagged_name = "%s.%s" % (name, tag)
    n = get_glyph_by_name(tagged_name)
    f.selection.select(n)
    alt_path = "../../../splitted/%s/%s/vert/u%04X.svg" % (
        weight, mod, c.unicode)
    if os.path.exists(alt_path):
        n.clear()
        n.importOutlines(alt_path, ('removeoverlap', 'correctdir'))
    else:
        f.paste()
        if method.find('R') >= 0:
            rot = psMat.compose(
                psMat.translate(-em / 2, -ascent + em / 2),
                psMat.compose(psMat.rotate(-math.pi / 2),
                psMat.translate(em / 2, ascent - em / 2)))
            n.transform(rot)
            if method.find('F') >= 0:
                flip = psMat.compose(
                    psMat.translate(-em / 2, -ascent + em / 2),
                    psMat.compose(psMat.scale(-1, 1),
                    psMat.translate(em / 2, ascent - em / 2)))
                n.transform(flip)
        elif method == 'S':
            position = weights_position[weight] * 2
            x, y = h2v_shift[position:position + 2]
            sht = psMat.translate(int(x), int(y))
            n.transform(sht)
    n.width = em
    n.vwidth = em
    if not (tag in alt_glyphs):
        alt_glyphs[tag] = []
    alt_glyphs[tag].append((name, tagged_name))

def set_vert_chars(mod):
    vbearings_path = "../../../../svg.d/%s/vbearings" % mod
    if os.path.exists(vbearings_path):
        fp = open(vbearings_path, 'r')
        line_count = 0
        for line in fp:
            line_count = line_count + 1
            if bearings_comment.match(line):
                continue
            if bearings_space.match(line):
                continue
            try:
                set_vbearings_line(line)
            except Exception as message:
                print(vbearings_path, "line:", line_count)
                print(message)
        fp.close()

def set_kernings_line(line):
    splitted = line.split()
    first, second = splitted[0][1:-1].split('][', 1)
    first = first.replace(
        '\\[', '[').replace('\\]', ']').replace('\\\\', '\\')
    second = second.replace(
        '\\[', '[').replace('\\]', ']').replace('\\\\', '\\')
    kerns = int(splitted[1:][weights_position[weight]])
    for l in first:
        cl = get_glyph_by_name(l)
        for r in second:
            cr = get_glyph_by_name(r)
            cl.addPosSub('kp', cr.glyphname, kerns)

def set_kernings(mod):
    kernings_path = "../../../../svg.d/%s/kernings" % mod
    if os.path.exists(kernings_path):
        fp = open(kernings_path, 'r')
        line_count = 0
        for line in fp:
            line_count = line_count + 1
            if bearings_comment.match(line):
                continue
            if bearings_space.match(line):
                continue
            try:
                set_kernings_line(line)
            except Exception as message:
                print(kernings_path, "line:", line_count)
                print(message)
        fp.close()

def set_fontnames():
    family = 'Circle M+ %s' % (middlefamily)
    subfamily = 'Regular'
    try:
        f.os2_stylemap = int('0001000000', 2) # regular
    except Exception as message:
        print(message)
    postscript = '%s-%s-%s' % (config.postscript, middlefamily, weight)
    styling_group = ("%s %s" % (family, weight))
    fullname = ("%s %s" % (family, weight))
    copyright = "Copyright(c) %s %s" % (config.year, config.author)
    f.fontname = postscript
    f.familyname = styling_group
    f.fullname = fullname
    f.weight = subfamily
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
        ('Japanese', 'Preferred Family', family),
        ('English (US)', 'Preferred Family', family),
        ('Japanese', 'Preferred Styles', weight),
        ('English (US)', 'Preferred Styles', weight),
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
    }[weight]
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
    }[weight]
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

def merge_features():
    if not is_monospace:
        f.mergeFeature('ligature01.fea')
        f.mergeFeature('mark01.fea')
    f.mergeFeature('ccmp01.fea')
    f.mergeFeature('ccmp02.fea')

def set_ccmp():
    table = [
        (0xE055, "uni304B_uni309A"),
        (0xE056, "uni304D_uni309A"),
        (0xE057, "uni304F_uni309A"),
        (0xE058, "uni3051_uni309A"),
        (0xE059, "uni3053_uni309A"),
        (0xE205, "uni30AB_uni309A"),
        (0xE206, "uni30AD_uni309A"),
        (0xE207, "uni30AF_uni309A"),
        (0xE208, "uni30B1_uni309A"),
        (0xE209, "uni30B3_uni309A"),
        (0xE20D, "uni30BB_uni309A"),
        (0xE211, "uni30C4_uni309A"),
        (0xE213, "uni30C8_uni309A"),
        (0xE29B, "uni31F7_uni309A")]
    for t in table:
        try:
            c = f[t[0]]
            c.unicode = -1
            c.glyphname = t[1]
            c.addPosSub('kana semi-voiced table', tuple(t[1].split('_')))
        except Exception as message:
            print(t)
            print(message)

def set_alt_tables():
    # swap glyphs jp90 <-> jp04
    if 'jp90' in alt_glyphs:
        for gs in alt_glyphs['jp90']:
            f.selection.select(gs[0]) #copy jp90
            f.copy()
            f.selection.select(0x0000) #paste jp90 to tmp
            f.paste()
            f.selection.select(gs[1]) #copy jp04
            f.copy()
            f.selection.select(gs[0]) #paste jp04 to jp90position
            f.paste()
            f.selection.select(0x0000) #copy tmp
            f.copy()
            f.selection.select(gs[1]) #paste tmp to jp04position
            f.paste()
        f[0x0000].clear()

    tag_table = {
        'jp90': 'jp90table',
        'vert': 'j-vert'
    }
    for tag in tag_table:
        if not tag in alt_glyphs:
            continue
        for names in alt_glyphs[tag]:
            name, tagged_name = names
            c = get_glyph_by_name(name)
            c.addPosSub(tag_table[tag], tagged_name)

def set_kanji_aliases():
    kangxi_ucs = [
        0x4E00, 0x4E28, 0x4E36, 0x4E3F, 0x4E59, 0x4E85, 0x4E8C, 0x4EA0,
        0x4EBA, 0x513F, 0x5165, 0x516B, 0x5182, 0x5196, 0x51AB, 0x51E0,
        0x51F5, 0x5200, 0x529B, 0x52F9, 0x5315, 0x531A, 0x5338, 0x5341,
        0x535C, 0x5369, 0x5382, 0x53B6, 0x53C8, 0x53E3, 0x56D7, 0x571F,
        0x58EB, 0x5902, 0x590A, 0x5915, 0x5927, 0x5973, 0x5B50, 0x5B80,
        0x5BF8, 0x5C0F, 0x5C22, 0x5C38, 0x5C6E, 0x5C71, 0x5DDB, 0x5DE5,
        0x5DF1, 0x5DFE, 0x5E72, 0x5E7A, 0x5E7F, 0x5EF4, 0x5EFE, 0x5F0B,
        0x5F13, 0x5F50, 0x5F61, 0x5F73, 0x5FC3, 0x6208, 0x6236, 0x624B,
        0x652F, 0x6534, 0x6587, 0x6597, 0x65A4, 0x65B9, 0x65E0, 0x65E5,
        0x66F0, 0x6708, 0x6728, 0x6B20, 0x6B62, 0x6B79, 0x6BB3, 0x6BCB,
        0x6BD4, 0x6BDB, 0x6C0F, 0x6C14, 0x6C34, 0x706B, 0x722A, 0x7236,
        0x723B, 0x723F, 0x7247, 0x7259, 0x725B, 0x72AC, 0x7384, 0x7389,
        0x74DC, 0x74E6, 0x7518, 0x751F, 0x7528, 0x7530, 0x758B, 0x7592,
        0x7676, 0x767D, 0x76AE, 0x76BF, 0x76EE, 0x77DB, 0x77E2, 0x77F3,
        0x793A, 0x79B8, 0x79BE, 0x7A74, 0x7ACB, 0x7AF9, 0x7C73, 0x7CF8,
        0x7F36, 0x7F51, 0x7F8A, 0x7FBD, 0x8001, 0x800C, 0x8012, 0x8033,
        0x807F, 0x8089, 0x81E3, 0x81EA, 0x81F3, 0x81FC, 0x820C, 0x821B,
        0x821F, 0x826E, 0x8272, 0x8278, 0x864D, 0x866B, 0x8840, 0x884C,
        0x8863, 0x897E, 0x898B, 0x89D2, 0x8A00, 0x8C37, 0x8C46, 0x8C55,
        0x8C78, 0x8C9D, 0x8D64, 0x8D70, 0x8DB3, 0x8EAB, 0x8ECA, 0x8F9B,
        0x8FB0, 0x8FB5, 0x9091, 0x9149, 0x91C6, 0x91CC, 0x91D1, 0x9577,
        0x9580, 0x961C, 0x96B6, 0x96B9, 0x96E8, 0x9751, 0x975E, 0x9762,
        0x9769, 0x97CB, 0x97ED, 0x97F3, 0x9801, 0x98A8, 0x98DB, 0x98DF,
        0x9996, 0x9999, 0x99AC, 0x9AA8, 0x9AD8, 0x9ADF, 0x9B25, 0x9B2F,
        0x9B32, 0x9B3C, 0x9B5A, 0x9CE5, 0x9E75, 0x9E7F, 0x9EA5, 0x9EBB,
        0x9EC3, 0x9ECD, 0x9ED1, 0x9EF9, 0x9EFD, 0x9F0E, 0x9F13, 0x9F20,
        0x9F3B, 0x9F4A, 0x9F52, 0x9F8D, 0x9F9C, 0x9FA0,
    ]
    for i in range(0, len(kangxi_ucs)):
        kangxi_code = i + 0x2F00
        if kangxi_code in f:
            continue
        if kangxi_ucs[i] in f:
            f.selection.select(kangxi_ucs[i])
            f.copyReference()
            n = get_glyph_by_name('uni%04X' % kangxi_code)
            f.selection.select(n)
            f.paste()
    cjk_radicals = [
        (0x2E81, 0x20086),
        (0x2E83, 0x4E5A),
        (0x2E85, 0x4EBB),
        (0x2E89, 0x5202),
        (0x2E8B, 0x353E),
        (0x2E8E, 0x5140),
        (0x2E8F, 0x5C23),
        (0x2E90, 0x5C22),
        (0x2E92, 0x5DF3),
        (0x2E93, 0x5E7A),
        (0x2E94, 0x5F51),
        (0x2E96, 0x5FC4),
        (0x2E97, 0x38FA),
        (0x2E98, 0x624C),
        (0x2E99, 0x6535),
        (0x2E9B, 0x65E1),
        (0x2E9E, 0x6B7A),
        (0x2E9F, 0x6BCD),
        (0x2EA0, 0x6C11),
        (0x2EA1, 0x6C35),
        (0x2EA2, 0x6C3A),
        (0x2EA3, 0x706C),
        (0x2EA5, 0x722B),
        (0x2EA6, 0x4E2C),
        (0x2EA8, 0x72AD),
        (0x2EAB, 0x7F52),
        (0x2EAD, 0x793B),
        (0x2EB2, 0x7F52),
        (0x2EB3, 0x34C1),
        (0x2EB9, 0x8002),
        (0x2EBD, 0x26951),
        (0x2EBE, 0x8279),
        (0x2EBF, 0xFA5E),
        (0x2EC0, 0xFA5D),
        (0x2EC2, 0x8864),
        (0x2EC3, 0x8980),
        (0x2EC4, 0x897F),
        (0x2ECA, 0x27FB7),
        (0x2ECC, 0xFA66),
        (0x2ECD, 0x8FB6),
        (0x2ED1, 0x9577),
        (0x2ED2, 0x9578),
        (0x2ED8, 0x9752),
        (0x2EDE, 0x2967F),
        (0x2EDF, 0x98E0),
        (0x2EE8, 0x9EA6),
        (0x2EE9, 0x9EC4),
        (0x2EEB, 0x6589),
        (0x2EED, 0x6B6F),
        (0x2EEF, 0x7ADC),
        (0x2EF2, 0x4E80),
    ]
    for i in cjk_radicals:
        if i[0] in f:
            continue
        if i[1] in f:
            f.selection.select(i[1])
            f.copyReference()
            n = get_glyph_by_name('uni%04X' % i[0])
            f.selection.select(n)
            f.paste()

def set_kanji_altuni():
    kanjidir = '../../../../svg.d/kanji'
    for subdir in os.listdir(kanjidir):
        if subdir.upper().find('CVS') >= 0:
            continue
        altuni_path = os.path.join(kanjidir, subdir, 'altuni')
        if os.path.exists(altuni_path):
            fp = open(altuni_path, 'r')
            line_count = 0
            for line in fp:
                line_count += 1
                l = line.strip()
                if len(l) == 0 or l[0] == '#':
                    continue
                splitted = line.split(None, 1)
                name = splitted[0]
                def hex2int(s):
                    return int(s, 16)
                alts = [tuple(map(hex2int, x.split()))
                        for x in splitted[1].split(',')]
                if name in f:
                    try:
                        f[name].altuni = tuple(alts)
                    except Exception as message:
                        print(altuni_path, line_count)
                        print(message)
                        print(alts)
            fp.close()

def fix_width():
    # ←↑→↓ as full width
    for c in (0x2190, 0x2191, 0x2192, 0x2193):
        full_width = 1000
        # put the glyph in the horizontal center of em
        xmin,ymin,xmax,ymax = f[c].boundingBox()
        bearing = (full_width - (xmax-xmin)) / 2
        f[c].left_side_bearing = bearing
        f[c].right_side_bearing = bearing
        f[c].width = full_width

    # add zero-width character
    #   U+200B ZERO WIDTH SPACE
    #   U+2060 WORD JOINER (zero width non-breaking space)
    #   U+FEFF ZERO WIDTH NO-BREAK SPACE (Byte Order Mark)
    for c in (0x200B, 0x2060, 0xFEFF):
        g = f.createChar(c)
        g.width = 0

    # ￣ ‾upper line
    if middlefamily[1] == 'm':
        f.selection.select(0xffe3)
        f.transform(psMat.translate(0, -80))
        f.selection.select(0x203e)
        f.transform(psMat.translate(0, -80))

    # WAVE DASH differ
    if middlefamily == '2m':
        f.selection.select(0x301C)
        f.copy()
        f.selection.select(0xFF5E)
        f.paste()


def set_japanese_proportional():
    scale = 1
    if middlefamily == '2p':
        scale = 0.8

    # small kana, dakuten, onbiki
    #   ぁぃぅぇ ぉっゃゅ
    #   ょゎゕゖ ゛゜ァィ
    #   ゥェォャ ュョヮヵ
    #   ヶー(ッ 0x30c3)
    japanese_chars_small = (
        0x3041,0x3043,0x3045,0x3047, 0x3049,0x3063,0x3083,0x3085,
        0x3087,0x308e,0x3095,0x3096, 0x309b,0x309c,0x30a1,0x30a3,
        0x30a5,0x30a7,0x30a9,0x30e3, 0x30e5,0x30e7,0x30ee,0x30f5,
        0x30f6,0x30fc
    )

    # wall left (Left edges of these glyphs are drawn as lines like walls.)
    # けげしじ はばぱ
    # ほぼぽゆ り
    # トドヒビ ピレロ
    # (ハバパ)
    japanese_chars_wall_L = (
        0x3051,0x3052,0x3057,0x3058, 0x306f,0x3070,0x3071,
        0x307b,0x307c,0x307d,0x3086, 0x308a,
        0x30c8,0x30c9,0x30d2,0x30d3, 0x30d4,0x30ec,0x30ed
    )
    # ぬねの りわ
    # カガコゴ ヨリロ
    japanese_chars_wall_R = (
        0x306c,0x306d,0x306e, 0x308a,0x308f,
        0x30ab,0x30ac,0x30b3,0x30b4, 0x30e8,0x30ea,0x30ed
    )
    # needle left (Left edges of these glyphs are drawn as points like needles)
    # くへべぺ やん
    # イノヘベ ペ
    japanese_chars_needle_L = (
        0x304f,0x3078,0x3079,0x307a, 0x3084, 0x3093,
        0x30a4,0x30ce,0x30d8,0x30d9, 0x30da
    )
    # しへ
    # ピプへ
    japanese_chars_needle_R = (
        0x3057,0x3078,
        0x30d4,0x30d7,0x30d8
    )

    # parenthesis fullwitdh
    # 〈《「『  【〔（［ ｛
    #brackets_start = (0x3008,0x300a,0x300c,0x300e, 0x3010,0x3014,0xff08,0xff3b, 0xff5b)
    #brackets_end = [0x3009,0x300b,0x300d,0x300f, 0x3011,0x3015,0xff09,0xff3d, 0xff5d]
    # 「『【
    brackets_start = (0x300c,0x300e,0x3010)
    brackets_end = (0x300d,0x300f,0x3011)

    # hiragana, katakana
    for kana in range(0x3041, 0x30ff+1):
        # blank, blank, combining゛. combining゜, ・
        if kana == 0x3097 or kana == 0x3098 or kana == 0x3099 or kana == 0x309a or kana == 0x30fb:
            continue

        maxL = 75
        maxR = 75
        for c in japanese_chars_small:
            if kana == c:
                maxL = 50
                maxR = 50
                break
        for c in japanese_chars_wall_L:
            if kana == c:
                maxL = 125
                break
        for c in japanese_chars_wall_R:
            if kana == c:
                maxR = 125
                break
        for c in japanese_chars_needle_L:
            if kana == c:
                maxL = 50
                break
        for c in japanese_chars_needle_R:
            if kana == c:
                maxR = 50
                break
        maxL = int(maxL * scale)
        maxR = int(maxR * scale)

        bearing_L = f[kana].left_side_bearing
        bearing_R = f[kana].right_side_bearing
        if bearing_L > maxL:
            f[kana].left_side_bearing = maxL
        if bearing_R > maxR:
            f[kana].right_side_bearing = maxR
        else:
            f[kana].right_side_bearing = bearing_R
    # ン
    f[0x30f3].right_side_bearing = int(65 * scale)
    # nakaguro ・
    f[0x30fb].left_side_bearing = 250
    f[0x30fb].right_side_bearing = 250

    # brackets
    max = 250
    min = 50
    for c in brackets_start:
        bearing_L = f[c].left_side_bearing
        bearing_R = f[c].right_side_bearing
        if bearing_L > max:
            f[c].left_side_bearing = max
        if bearing_R > min:
            f[c].right_side_bearing = min
        else:
            f[c].right_side_bearing = bearing_R
    for c in brackets_end:
        bearing_R = f[c].right_side_bearing
        if bearing_R > max:
            f[c].right_side_bearing = max

# create font
f = fontforge.open('mplus.sfd')
f.encoding = 'unicode4'
f.hasvmetrics = True
f.ascent = ascent
f.descent = descent

kanji_flag = False
if 'kanji' in modules:
    kfontname = 'mplus-' + middlefamily[0]
    if modules[0] == 'kanji':
        kanji_flag = True
        moddir = '../../../splitted/%s/%s' % (weight, 'kanji')
        glyphs = import_kanji(moddir)
        if kfontname == 'mplus-2':
            f.transform(kanji_matrix)
        for code in f.selection:
            c = f[code]
            c.width = em
            c.vwidth = em
    else:
        f.close()
        f = fontforge.open('../../%sk/%s/%sk-%s.sfd'
            % (kfontname, weight, kfontname, weight))
    modules.remove('kanji')

# add lookups
if kanji_flag:
    f.addLookup('jis1990', 'gsub_single', (), (
        ("jp90", (("latn", ("dflt",)), ("grek", ("dflt",)),
                  ("cyrl", ("dflt",)), ("kana", ("dflt", "JAN ")),
                  ("hani", ("dflt",))),),))
    f.addLookupSubtable('jis1990', 'jp90table')
    set_kanji_aliases()
    set_kanji_altuni()
else:
    f.addLookup('gsubvert', 'gsub_single', (), (
        ("vert", (("DFLT", ("dflt",)), ("latn", ("dflt",)), ("grek", ("dflt",)),
                  ("cyrl", ("dflt",)), ("kana", ("dflt", "JAN ")),
                  ("hani", ("dflt",))),),))
    f.addLookupSubtable('gsubvert', 'j-vert')
    f.addLookup('kerning pairs', 'gpos_pair', (), (
        ("kern", (("DFLT", ("dflt",)), ("latn", ("dflt",)),)),))
    f.addLookupSubtable('kerning pairs', 'kp')
    f.addLookup('kana semi-voiced lookup', 'gsub_ligature', (), (
        ("ccmp", (("DFLT", ("dflt",)), ("kana", ("JAN ", "dflt")),)),
        ("liga", (("DFLT", ("dflt",)), ("kana", ("JAN ", "dflt")),))))
    f.addLookupSubtable('kana semi-voiced lookup', 'kana semi-voiced table')
    for mod in modules:
        moddir = '../../../splitted/%s/%s' % (weight, mod)
        import_svgs(moddir)
        set_bearings(mod)
        set_kernings(mod)
        set_vert_chars(mod)
    merge_features()
    set_ccmp()
    f.autoInstr()
    f.hasvmetrics = True

set_alt_tables()
set_fontnames()
if middlefamily in ('1c', '2p'):
    set_japanese_proportional()
if not kanji_flag:
    fix_width()

f.selection.all()
f.removeOverlap()
f.round()

if kanji_flag:
    f.save('%sk-%s.sfd' % (kfontname, weight))
    open(ttfname, 'w').close()
else:
    f.generate(ttfname, '', ('short-post', 'opentype', 'PfEd-lookups', 'no-hints'))
