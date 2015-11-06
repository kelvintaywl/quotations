# -*- coding: utf-8 -*-
from __future__ import absolute_import

import constants

NEUTRAL_QUOTATIONS = u"\'\'\"\"``"
NEUTRAL_EXCLUDE = {
    constants.LC_ENGLISH
}

# the lone rangers where these quotations do not need a pairing based on some logic
# long rangers typically appear right after an alphabet
LONE_RANGERS = u'\'\"’'

QUOTATION_MAP = {
    constants.LC_ENGLISH: NEUTRAL_QUOTATIONS,
    constants.LC_SPANISH: u"«»“”",
    constants.LC_SPANISH_LATIN: u"«»“”",
    constants.LC_FRENCH: u"«»“”",
    constants.LC_GERMAN: u"„“‚‘",
    constants.LC_JAPANESE: u"「」『』",
    constants.LC_THAI: u"“”‘’",
    constants.LC_CHINESE: u"「」『』",
    constants.LC_CHINESE_TRADITIONAL: u"「」『』"
}

for lc in QUOTATION_MAP:
    if lc not in NEUTRAL_EXCLUDE:
        # append NEUTRAL_QUOTATIONS to some languges
        # because neutral quotations seem to be used in other languages besides english
        QUOTATION_MAP[lc] += NEUTRAL_QUOTATIONS
