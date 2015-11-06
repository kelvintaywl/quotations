# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re

import constants
from models import Quotation
from utils import QUOTATION_MAP, LONE_RANGERS


ALPHABETS = re.compile('\w')

class QuotationExtractor(object):

    def __init__(self, text, lc=constants.LC_ENGLISH):
        self.text = text
        self.lc = lc

    def extract(self):
        """ Yields Quotation instance extractable from text """
        closed = True
        for index, char in enumerate(self.text):
            if char in QUOTATION_MAP.get(self.lc, []):
                if char in LONE_RANGERS and index > 0:
                    prev_char = self.text[index-1]
                    if ALPHABETS.match(prev_char):
                        # prev char is a alphabet; highly likely to be a lone ranger, not a true quotation
                        # ignore lone ranger
                        continue

                closed = not closed  # toggle to open from start
                yield Quotation.create(self.lc, char, force_close=closed)

    def __len__(self):
        return len(list(self.extract()))

