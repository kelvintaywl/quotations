# -*- coding: utf-8 -*-
from __future__ import absolute_import


class QuotationValidationError(Exception):
    """ Base Exception for quotation validation """
    pass

class LanguageNotSupported(QuotationValidationError):
    """ Exception when a certain language is not supported """
    pass


class QuotationNotFound(QuotationValidationError):
    """ Exception when a specific quotation cannot be found or understood """
    pass


class QuotationMissingPair(QuotationValidationError):
    """ Exception when a quotation is found to be orphaned or missing its complement """
    pass


class TranslatedQuotationAmountDifference(QuotationValidationError):
    """ Exception when total quotations in translation is different from that of source """
    pass


class TranslatedQuotationWrongOrder(QuotationValidationError):
    """ Exception when a translated quotation is not in right order of text """
    pass

