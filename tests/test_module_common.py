#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase

from modules import is_without_special_chars


class TestModuleCommonIsWithoutSpecialChars(TestCase):

    # success cases

    def test_module_common_is_without_special_chars__pure_text(self):
        self.assertTrue(is_without_special_chars("text"))

    def test_module_common_is_without_special_chars__with_underscore(self):
        self.assertTrue(is_without_special_chars("underscore_in_the_center"))
        self.assertTrue(is_without_special_chars("underscore_in_the_end_"))
        self.assertTrue(is_without_special_chars("_underscore_at_the_beginning"))

    # def test_module_common_is_without_special_chars__text_with_number(self):
    #     self.assertTrue(is_without_special_chars("text1"))

    # error cases

    def test_module_common_is_without_special_chars__special_character(self):
        self.assertFalse(is_without_special_chars("special_character_in_the_end_("))
        self.assertFalse(is_without_special_chars(")_special_character_at_the_beginning"))
        self.assertFalse(is_without_special_chars("special_character_*_in_the_center"))

        self.assertFalse(is_without_special_chars("special_character_&"))
        self.assertFalse(is_without_special_chars("special_character_¨"))
        self.assertFalse(is_without_special_chars("special_character_%"))
        self.assertFalse(is_without_special_chars("special_character_$"))
        self.assertFalse(is_without_special_chars("special_character_#"))
        self.assertFalse(is_without_special_chars("special_character_@"))
        self.assertFalse(is_without_special_chars("special_character_!"))
        self.assertFalse(is_without_special_chars("special_character_'"))
        self.assertFalse(is_without_special_chars("special_character_\""))
        self.assertFalse(is_without_special_chars("special_character_|"))
        self.assertFalse(is_without_special_chars("special_character_\\"))

        self.assertFalse(is_without_special_chars("special_character_-"))
        self.assertFalse(is_without_special_chars("special_character_+"))
        self.assertFalse(is_without_special_chars("special_character_="))
        self.assertFalse(is_without_special_chars("special_character_§"))
        self.assertFalse(is_without_special_chars("special_character_`"))
        self.assertFalse(is_without_special_chars("special_character_´"))
        self.assertFalse(is_without_special_chars("special_character_^"))
        self.assertFalse(is_without_special_chars("special_character_~"))
        self.assertFalse(is_without_special_chars("special_character_{"))
        self.assertFalse(is_without_special_chars("special_character_}"))

        self.assertFalse(is_without_special_chars("special_character_["))
        self.assertFalse(is_without_special_chars("special_character_]"))
        self.assertFalse(is_without_special_chars("special_character_ª"))
        self.assertFalse(is_without_special_chars("special_character_º"))
        self.assertFalse(is_without_special_chars("special_character_<"))
        self.assertFalse(is_without_special_chars("special_character_>"))
        self.assertFalse(is_without_special_chars("special_character_,"))
        self.assertFalse(is_without_special_chars("special_character_."))

        self.assertFalse(is_without_special_chars("special_character_:"))
        self.assertFalse(is_without_special_chars("special_character_;"))
        self.assertFalse(is_without_special_chars("special_character_/"))
        self.assertFalse(is_without_special_chars("special_character_?"))
        self.assertFalse(is_without_special_chars("special_character_°"))

    def test_module_common_is_without_special_chars__accent(self):
        self.assertFalse(is_without_special_chars("character_with_accent_à"))
        self.assertFalse(is_without_special_chars("character_with_accent_è"))
        self.assertFalse(is_without_special_chars("character_with_accent_ì"))
        self.assertFalse(is_without_special_chars("character_with_accent_ò"))
        self.assertFalse(is_without_special_chars("character_with_accent_ù"))

        self.assertFalse(is_without_special_chars("character_with_accent_á"))
        self.assertFalse(is_without_special_chars("character_with_accent_é"))
        self.assertFalse(is_without_special_chars("character_with_accent_í"))
        self.assertFalse(is_without_special_chars("character_with_accent_ó"))
        self.assertFalse(is_without_special_chars("character_with_accent_ú"))

        self.assertFalse(is_without_special_chars("character_with_accent_â"))
        self.assertFalse(is_without_special_chars("character_with_accent_ê"))
        self.assertFalse(is_without_special_chars("character_with_accent_î"))
        self.assertFalse(is_without_special_chars("character_with_accent_ô"))
        self.assertFalse(is_without_special_chars("character_with_accent_û"))

        self.assertFalse(is_without_special_chars("character_with_accent_ã"))
        self.assertFalse(is_without_special_chars("character_with_accent_ẽ"))
        self.assertFalse(is_without_special_chars("character_with_accent_ĩ"))
        self.assertFalse(is_without_special_chars("character_with_accent_õ"))
        self.assertFalse(is_without_special_chars("character_with_accent_ũ"))

        self.assertFalse(is_without_special_chars("character_with_accent_ç"))


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
