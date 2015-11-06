# -*- coding: utf-8 -*-
from __future__ import absolute_import

from errors import (LanguageNotSupported,
                    QuotationMissingPair,
                    QuotationValidationError,
                    TranslatedQuotationAmountDifference,
                    TranslatedQuotationWrongOrder)
from libs import QuotationExtractor
from utils import QUOTATION_MAP


class QuotationValidator(object):

    def __init__(self):
        pass

    @staticmethod
    def validate_open_close(text, lc):
        """
        Raises:
            QuotationMissingPair if orphaned quotations found
            LanguageNotSupported if lc is not supported
        """
        if lc not in QUOTATION_MAP:
            raise LanguageNotSupported

        stack = []
        for index, quotation in enumerate(QuotationExtractor(text, lc).extract()):
            if len(stack) and stack[-1] ^ quotation:
                # found complement
                stack.pop()
            else:
                stack.append(quotation)

        if stack:
            # not empty; extra quotations not closed
            raise QuotationMissingPair(u"there are orphaned quotations: {}".format(stack))

    @staticmethod
    def validate_translated_quotations(source, translation, source_lc, translation_lc):
        source_extractor = QuotationExtractor(source, source_lc)
        translation_extractor = QuotationExtractor(translation, translation_lc)

        # raise issue when amount of quotations differs between source and translation
        if len(source_extractor) != len(translation_extractor):
            raise TranslatedQuotationAmountDifference(
                u"total quotations of source ({}) and translation ({}) is different.".format(
                    list(source_extractor.extract()), list(translation_extractor.extract())
                )
            )

        # raise issue if order of quotations between source and translation do not tally
        source_quotations = list(source_extractor.extract())
        translation_quotations = list(translation_extractor.extract())

        for index in xrange(len(source_quotations)):
            if source_quotations[index] == translation_quotations[index]:
                continue
            else:
                raise TranslatedQuotationWrongOrder(
                    "differing order in quotation: source ({}), target ({})".format(
                        source_quotations[index],
                        translation_quotations[index]
                    )
                )

    @staticmethod
    def validate(source, translation, language_pair, verbose=False, strict=False):
        """ Returns true if validations passed, else False

        If verbose is True, returns a tuple of (bool, validation_error)
        If strict is True, validation is done across source and translation
        """
        try:
            source_lc, translation_lc = language_pair.split("_", 2)
            if source_lc not in QUOTATION_MAP or translation_lc not in QUOTATION_MAP:
                raise LanguageNotSupported
            # validate opening and closing quotations only for translation
            QuotationValidator.validate_open_close(translation, translation_lc)
        except QuotationValidationError as e:
            if verbose:
                return False, e
            else:
                return False

        else:
            if strict:
                try:
                    QuotationValidator.validate_translated_quotations(source, translation, source_lc, translation_lc)

                except QuotationValidationError as e:
                    if verbose:
                        return False, e
                    else:
                        return False

        return True if not verbose else (True, "")
