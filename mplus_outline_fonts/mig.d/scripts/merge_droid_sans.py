# -*- coding: utf-8 -*-
del_glyph = [ \
0x0020, 0x0021, 0x0022, 0x0023, 0x0024, 0x0025, 0x0026, 0x0027, \
0x0028, 0x0029, 0x002A, 0x002B, 0x002C, 0x002D, 0x002E, 0x002F, \
0x0030, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037, \
0x0038, 0x0039, 0x003A, 0x003B, 0x003C, 0x003D, 0x003E, 0x003F, \
0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 0x0047, \
0x0048, 0x0049, 0x004A, 0x004B, 0x004C, 0x004D, 0x004E, 0x004F, \
0x0050, 0x0051, 0x0052, 0x0053, 0x0054, 0x0055, 0x0056, 0x0057, \
0x0058, 0x0059, 0x005A, 0x005B, 0x005C, 0x005D, 0x005E, 0x005F, \
0x0060, 0x0061, 0x0062, 0x0063, 0x0064, 0x0065, 0x0066, 0x0067, \
0x0068, 0x0069, 0x006A, 0x006B, 0x006C, 0x006D, 0x006E, 0x006F, \
0x0070, 0x0071, 0x0072, 0x0073, 0x0074, 0x0075, 0x0076, 0x0077, \
0x0078, 0x0079, 0x007A, 0x007B, 0x007C, 0x007D, 0x007E, 0x00A0, \
0x00A1, 0x00A2, 0x00A3, 0x00A4, 0x00A5, 0x00A6, 0x00A7, 0x00A8, \
0x00A9, 0x00AA, 0x00AB, 0x00AC, 0x00AD, 0x00AE, 0x00AF, 0x00B0, \
0x00B1, 0x00B2, 0x00B3, 0x00B4, 0x00B5, 0x00B6, 0x00B7, 0x00B8, \
0x00B9, 0x00BA, 0x00BB, 0x00BC, 0x00BD, 0x00BE, 0x00BF, 0x00C0, \
0x00C1, 0x00C2, 0x00C3, 0x00C4, 0x00C5, 0x00C6, 0x00C7, 0x00C8, \
0x00C9, 0x00CA, 0x00CB, 0x00CC, 0x00CD, 0x00CE, 0x00CF, 0x00D0, \
0x00D1, 0x00D2, 0x00D3, 0x00D4, 0x00D5, 0x00D6, 0x00D7, 0x00D8, \
0x00D9, 0x00DA, 0x00DB, 0x00DC, 0x00DD, 0x00DE, 0x00DF, 0x00E0, \
0x00E1, 0x00E2, 0x00E3, 0x00E4, 0x00E5, 0x00E6, 0x00E7, 0x00E8, \
0x00E9, 0x00EA, 0x00EB, 0x00EC, 0x00ED, 0x00EE, 0x00EF, 0x00F0, \
0x00F1, 0x00F2, 0x00F3, 0x00F4, 0x00F5, 0x00F6, 0x00F7, 0x00F8, \
0x00F9, 0x00FA, 0x00FB, 0x00FC, 0x00FD, 0x00FE, 0x00FF, 0x0100, \
0x0101, 0x0102, 0x0103, 0x0104, 0x0105, 0x0106, 0x0107, 0x0108, \
0x0109, 0x010A, 0x010B, 0x010C, 0x010D, 0x010E, 0x010F, 0x0110, \
0x0111, 0x0112, 0x0113, 0x0114, 0x0115, 0x0116, 0x0117, 0x0118, \
0x0119, 0x011A, 0x011B, 0x011C, 0x011D, 0x011E, 0x011F, 0x0120, \
0x0121, 0x0122, 0x0123, 0x0124, 0x0125, 0x0126, 0x0127, 0x0128, \
0x0129, 0x012A, 0x012B, 0x012C, 0x012D, 0x012E, 0x012F, 0x0130, \
0x0131, 0x0132, 0x0133, 0x0134, 0x0135, 0x0136, 0x0137, 0x0138, \
0x0139, 0x013A, 0x013B, 0x013C, 0x013D, 0x013E, 0x013F, 0x0140, \
0x0141, 0x0142, 0x0143, 0x0144, 0x0145, 0x0146, 0x0147, 0x0148, \
0x0149, 0x014A, 0x014B, 0x014C, 0x014D, 0x014E, 0x014F, 0x0150, \
0x0151, 0x0152, 0x0153, 0x0154, 0x0155, 0x0156, 0x0157, 0x0158, \
0x0159, 0x015A, 0x015B, 0x015C, 0x015D, 0x015E, 0x015F, 0x0160, \
0x0161, 0x0162, 0x0163, 0x0164, 0x0165, 0x0166, 0x0167, 0x0168, \
0x0169, 0x016A, 0x016B, 0x016C, 0x016D, 0x016E, 0x016F, 0x0170, \
0x0171, 0x0172, 0x0173, 0x0174, 0x0175, 0x0176, 0x0177, 0x0178, \
0x0179, 0x017A, 0x017B, 0x017C, 0x017D, 0x017E, 0x017F, 0x0192, \
0x01A0, 0x01A1, 0x01AF, 0x01B0, 0x01F0, 0x01FA, 0x01FB, 0x01FC, \
0x01FD, 0x01FE, 0x01FF, 0x0218, 0x0219, 0x021A, 0x021B, 0x02BC, \
0x02C6, 0x02C7, 0x02C9, 0x02D8, 0x02D9, 0x02DA, 0x02DB, 0x02DC, \
0x02DD, 0x02F3, 0x0300, 0x0301, 0x0303, 0x0309, 0x030F, 0x0323, \
0x0384, 0x0385, 0x0386, 0x0387, 0x0388, 0x0389, 0x038A, 0x038C, \
0x038E, 0x038F, 0x0390, 0x0391, 0x0392, 0x0393, 0x0394, 0x0395, \
0x0396, 0x0397, 0x0398, 0x0399, 0x039A, 0x039B, 0x039C, 0x039D, \
0x039E, 0x039F, 0x03A0, 0x03A1, 0x03A3, 0x03A4, 0x03A5, 0x03A6, \
0x03A7, 0x03A8, 0x03A9, 0x03AA, 0x03AB, 0x03AC, 0x03AD, 0x03AE, \
0x03AF, 0x03B0, 0x03B1, 0x03B2, 0x03B3, 0x03B4, 0x03B5, 0x03B6, \
0x03B7, 0x03B8, 0x03B9, 0x03BA, 0x03BB, 0x03BC, 0x03BD, 0x03BE, \
0x03BF, 0x03C0, 0x03C1, 0x03C2, 0x03C3, 0x03C4, 0x03C5, 0x03C6, \
0x03C7, 0x03C8, 0x03C9, 0x03CA, 0x03CB, 0x03CC, 0x03CD, 0x03CE, \
0x03D1, 0x03D2, 0x03D6, 0x0400, 0x0401, 0x0402, 0x0403, 0x0404, \
0x0405, 0x0406, 0x0407, 0x0408, 0x0409, 0x040A, 0x040B, 0x040C, \
0x040D, 0x040E, 0x040F, 0x0410, 0x0411, 0x0412, 0x0413, 0x0414, \
0x0415, 0x0416, 0x0417, 0x0418, 0x0419, 0x041A, 0x041B, 0x041C, \
0x041D, 0x041E, 0x041F, 0x0420, 0x0421, 0x0422, 0x0423, 0x0424, \
0x0425, 0x0426, 0x0427, 0x0428, 0x0429, 0x042A, 0x042B, 0x042C, \
0x042D, 0x042E, 0x042F, 0x0430, 0x0431, 0x0432, 0x0433, 0x0434, \
0x0435, 0x0436, 0x0437, 0x0438, 0x0439, 0x043A, 0x043B, 0x043C, \
0x043D, 0x043E, 0x043F, 0x0440, 0x0441, 0x0442, 0x0443, 0x0444, \
0x0445, 0x0446, 0x0447, 0x0448, 0x0449, 0x044A, 0x044B, 0x044C, \
0x044D, 0x044E, 0x044F, 0x0450, 0x0451, 0x0452, 0x0453, 0x0454, \
0x0455, 0x0456, 0x0457, 0x0458, 0x0459, 0x045A, 0x045B, 0x045C, \
0x045D, 0x045E, 0x045F, 0x0460, 0x0461, 0x0462, 0x0463, 0x0464, \
0x0465, 0x0466, 0x0467, 0x0468, 0x0469, 0x046A, 0x046B, 0x046C, \
0x046D, 0x046E, 0x046F, 0x0470, 0x0471, 0x0472, 0x0473, 0x0474, \
0x0475, 0x0476, 0x0477, 0x0478, 0x0479, 0x047A, 0x047B, 0x047C, \
0x047D, 0x047E, 0x047F, 0x0480, 0x0481, 0x0482, 0x0483, 0x0484, \
0x0485, 0x0486, 0x0488, 0x0489, 0x048A, 0x048B, 0x048C, 0x048D, \
0x048E, 0x048F, 0x0490, 0x0491, 0x0492, 0x0493, 0x0494, 0x0495, \
0x0496, 0x0497, 0x0498, 0x0499, 0x049A, 0x049B, 0x049C, 0x049D, \
0x049E, 0x049F, 0x04A0, 0x04A1, 0x04A2, 0x04A3, 0x04A4, 0x04A5, \
0x04A6, 0x04A7, 0x04A8, 0x04A9, 0x04AA, 0x04AB, 0x04AC, 0x04AD, \
0x04AE, 0x04AF, 0x04B0, 0x04B1, 0x04B2, 0x04B3, 0x04B4, 0x04B5, \
0x04B6, 0x04B7, 0x04B8, 0x04B9, 0x04BA, 0x04BB, 0x04BC, 0x04BD, \
0x04BE, 0x04BF, 0x04C0, 0x04C1, 0x04C2, 0x04C3, 0x04C4, 0x04C5, \
0x04C6, 0x04C7, 0x04C8, 0x04C9, 0x04CA, 0x04CB, 0x04CC, 0x04CD, \
0x04CE, 0x04CF, 0x04D0, 0x04D1, 0x04D2, 0x04D3, 0x04D4, 0x04D5, \
0x04D6, 0x04D7, 0x04D8, 0x04D9, 0x04DA, 0x04DB, 0x04DC, 0x04DD, \
0x04DE, 0x04DF, 0x04E0, 0x04E1, 0x04E2, 0x04E3, 0x04E4, 0x04E5, \
0x04E6, 0x04E7, 0x04E8, 0x04E9, 0x04EA, 0x04EB, 0x04EC, 0x04ED, \
0x04EE, 0x04EF, 0x04F0, 0x04F1, 0x04F2, 0x04F3, 0x04F4, 0x04F5, \
0x04F6, 0x04F7, 0x04F8, 0x04F9, 0x04FA, 0x04FB, 0x04FC, 0x04FD, \
0x04FE, 0x04FF, 0x0500, 0x0501, 0x0502, 0x0503, 0x0504, 0x0505, \
0x0506, 0x0507, 0x0508, 0x0509, 0x050A, 0x050B, 0x050C, 0x050D, \
0x050E, 0x050F, 0x0510, 0x0511, 0x0512, 0x0513, 0x1E00, 0x1E01, \
0x1E3E, 0x1E3F, 0x1E80, 0x1E81, 0x1E82, 0x1E83, 0x1E84, 0x1E85, \
0x1EA0, 0x1EA1, 0x1EA2, 0x1EA3, 0x1EA4, 0x1EA5, 0x1EA6, 0x1EA7, \
0x1EA8, 0x1EA9, 0x1EAA, 0x1EAB, 0x1EAC, 0x1EAD, 0x1EAE, 0x1EAF, \
0x1EB0, 0x1EB1, 0x1EB2, 0x1EB3, 0x1EB4, 0x1EB5, 0x1EB6, 0x1EB7, \
0x1EB8, 0x1EB9, 0x1EBA, 0x1EBB, 0x1EBC, 0x1EBD, 0x1EBE, 0x1EBF, \
0x1EC0, 0x1EC1, 0x1EC2, 0x1EC3, 0x1EC4, 0x1EC5, 0x1EC6, 0x1EC7, \
0x1EC8, 0x1EC9, 0x1ECA, 0x1ECB, 0x1ECC, 0x1ECD, 0x1ECE, 0x1ECF, \
0x1ED0, 0x1ED1, 0x1ED2, 0x1ED3, 0x1ED4, 0x1ED5, 0x1ED6, 0x1ED7, \
0x1ED8, 0x1ED9, 0x1EDA, 0x1EDB, 0x1EDC, 0x1EDD, 0x1EDE, 0x1EDF, \
0x1EE0, 0x1EE1, 0x1EE2, 0x1EE3, 0x1EE4, 0x1EE5, 0x1EE6, 0x1EE7, \
0x1EE8, 0x1EE9, 0x1EEA, 0x1EEB, 0x1EEC, 0x1EED, 0x1EEE, 0x1EEF, \
0x1EF0, 0x1EF1, 0x1EF2, 0x1EF3, 0x1EF4, 0x1EF5, 0x1EF6, 0x1EF7, \
0x1EF8, 0x1EF9, 0x1F4D, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004, \
0x2005, 0x2006, 0x2007, 0x2008, 0x2009, 0x200A, 0x200B, 0x2013, \
0x2014, 0x2015, 0x2017, 0x2018, 0x2019, 0x201A, 0x201B, 0x201C, \
0x201D, 0x201E, 0x2020, 0x2021, 0x2022, 0x2026, 0x2030, 0x2032, \
0x2033, 0x2039, 0x203A, 0x203C, 0x2044, 0x207F, 0x20A3, 0x20A4, \
0x20A7, 0x20AB, 0x20AC, 0x2105, 0x2113, 0x2116, 0x2122, 0x2126, \
0x212E, 0x215B, 0x215C, 0x215D, 0x215E, 0x2202, 0x2206, 0x220F, \
0x2211, 0x2212, 0x221A, 0x221E, 0x222B, 0x2248, 0x2260, 0x2264, \
0x2265, 0x25CA, 0xFB01, 0xFB02, 0xFB03, 0xFB04, 0xFEFF, 0xFFFC, \
0xFFFD]
## End