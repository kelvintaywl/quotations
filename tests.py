# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest

import constants
from quotations import QuotationValidator


class TestQuotationMap(unittest.TestCase):

    def test_pairing(self):
        """ Test to check that there is a closing quotation for every opening quotation """
        from utils import QUOTATION_MAP

        for quotations in QUOTATION_MAP.values():
            self.assertTrue(len(quotations) and len(quotations) % 2 == 0)


class TestQuotation(unittest.TestCase):

    def test_init_not_found(self):
        """ Test that a QuotationNotFound is raised when unsupported languages or quotations requested """
        from models import Quotation
        from errors import LanguageNotSupported, QuotationNotFound

        # klingon should not be supported, maybe in the future?
        self.assertRaises(LanguageNotSupported, Quotation.__call__, "klingon", 10)

        # french should not include japanese quotation
        self.assertRaises(QuotationNotFound, Quotation.create, constants.LC_FRENCH, u"「")

    def test_create(self):
        """ Test that a Quotation.create works when supported language and quotation character """
        from models import Quotation

        tests = [
            {"lc": constants.LC_FRENCH, "char": u"«"},
            {"lc": constants.LC_ENGLISH, "char": u"\"", "close": True},
            {"lc": constants.LC_JAPANESE, "char": u"「"}
        ]

        for test in tests:
            q = Quotation.create(test["lc"], test["char"], force_close=("close" in test))
            self.assertTrue(q)
            self.assertEqual(str(q), test["char"].encode('utf-8'))


class TestQuotationValid(unittest.TestCase):

    def test_validate_success(self):
        """ Test to check that translation's quotations open and close correctly."""
        tests = [
            {
                "source": u"'Hello world,' she said.",
                "translation": u"«Bonjour tout le monde», dit-elle.",
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_FRENCH)
            },
            {
                "source": u"'Hello world,' she said.",
                "translation": u"「世界こんにちは」と彼女は言いました。",
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_JAPANESE)
            },
            {
                "source": u"this is a markdown text where we have a [link (please click)](https://www.google.com)",
                "translation": u"Ceci est un texte de démarque où nous avons un  [lien(s'il vous plaît cliquer sur)](https://www.google.com)",
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_FRENCH),
                "remarks": "this is to test that lone rangers should be ignored (e.g., \"Maccabees' place \""
            },
            {
                "source": u"「これは最高なものです！」と、彼女は叫びました",
                "translation": u"'This is dog's bollocks!', she exclaimed",
                "language_pair": "{}_{}".format(constants.LC_JAPANESE, constants.LC_ENGLISH),
                "remarks": "this is a more complicated test that lone rangers should be ignored (e.g., \"Maccabees' place \""
            },
        ]

        for test in tests:
            ok = QuotationValidator.validate(test["source"], test["translation"], test["language_pair"])
            self.assertTrue(ok)

    def test_validate_strict_success(self):
        """ Test to check that source and translation have equal amount and order of quotations """

        tests = [
            {
                "source": u"'Hello world,' she said.",
                "translation": u"«Bonjour tout le monde», dit-elle.",
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_FRENCH)
            },
            {
                "source": u"'Hello world,' she said.",
                "translation": u"「世界こんにちは」と彼女は言いました。",
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_JAPANESE)
            },
            {
                "source": u"this is a markdown text where we have a [link (please click)](https://www.google.com)",
                "translation": u"Ceci est un texte de démarque où nous avons un  [lien(s'il vous plaît cliquer sur)](https://www.google.com)",
                "language_pair": "{}_{}".format(constants.LC_ENGLISH, constants.LC_FRENCH)
            },
            {
                "source": u"「これは最高なものです！」と、彼女は叫びました",
                "translation": u"'This is dog's bollocks!', she exclaimed",
                "language_pair": "{}_{}".format(constants.LC_JAPANESE, constants.LC_ENGLISH),
                "remarks": "this is a more complicated test that lone rangers should be ignored (e.g., \"Maccabees' place \""
            },
        ]

        for i, test in enumerate(tests):
            ok, e = QuotationValidator.validate(test["source"], test["translation"], test["language_pair"], strict=True, verbose=True)
            self.assertEqual(ok, True, msg=str(e))

    def test_validate_strict_failure(self):
        """ Test to check that source and translation have equal amount and order of quotations """
        pass

if __name__ == "__main__":
    unittest.main()
