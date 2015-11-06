# -*- coding: utf-8 -*-
from __future__ import absolute_import

import constants
from errors import (LanguageNotSupported,
                    QuotationNotFound)
from utils import QUOTATION_MAP


class Quotation(object):

    def __init__(self, lc, position):
        if lc not in QUOTATION_MAP:
            raise LanguageNotSupported(u"[{}] language code is not supported".format(lc))

        self._lc = lc  # language code
        self._position = position  # index position of quotation in QUOTATION MAP
        self._closing = position % 2 == 1  # opening or closing quotation based on position

    @classmethod
    def create(cls, lc, char, force_close=False):
        if lc not in QUOTATION_MAP:
            raise LanguageNotSupported(u"[{}] language code is not supported".format(lc))

        try:
            position = QUOTATION_MAP[lc].index(char)
            is_closed = position % 2 == 1
            if not is_closed and force_close:
                # currently recognized as open quotation; we want to force this to be closed
                position += 1  # from open to close
        except ValueError:
            raise QuotationNotFound(u"cannot find \"{}\" quotation for language code [{}]".format(char, lc))
        else:
            return Quotation(lc, position)

    def mirror(self):
        """ Returns the complement of itself

        assert complement ^ self is True

        """
        offset = -1 if self._closing else 1
        return Quotation(self._lc, self._position + offset)

    def __eq__(self, other):
        return self._closing == other._closing

    def __ne__(self, other):
        return not self.__eq__(other)

    def __xor__(self, other):
        return self._lc == other._lc and \
               self._closing is not other._closing and \
               abs(self._position - other._position) == 1

    def __str__(self):
        return QUOTATION_MAP[self._lc][self._position].encode('utf-8')

    def __repr__(self):
        return str(self)
