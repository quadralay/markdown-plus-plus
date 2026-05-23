"""Tests for add-aliases.py.

Run with: python -m unittest test_add_aliases
(must be invoked from this scripts/ directory)
"""

import importlib.util
import os
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_SPEC = importlib.util.spec_from_file_location(
    "add_aliases", os.path.join(_HERE, "add-aliases.py")
)
add_aliases = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(add_aliases)


class GetExistingAliasesTests(unittest.TestCase):
    def test_compact_form_does_not_over_capture(self):
        # Regression: ALIAS_PATTERN body class includes '-' without a
        # terminating lookahead would greedily match '-->' as 'name--'.
        self.assertEqual(
            add_aliases.get_existing_aliases("<!--#intro-->"),
            {"intro"},
        )

    def test_compact_form_hyphenated_name(self):
        self.assertEqual(
            add_aliases.get_existing_aliases("<!--#sh-ug-installation-->"),
            {"sh-ug-installation"},
        )

    def test_compact_form_digit_first(self):
        self.assertEqual(
            add_aliases.get_existing_aliases("<!--#04499224-->"),
            {"04499224"},
        )

    def test_spaced_form(self):
        self.assertEqual(
            add_aliases.get_existing_aliases("<!-- #intro -->"),
            {"intro"},
        )

    def test_unicode_letter_alias_compact(self):
        self.assertEqual(
            add_aliases.get_existing_aliases("<!--#Café-->"),
            {"Café"},
        )

    def test_combined_command_alias_is_not_extracted(self):
        # ALIAS_PATTERN starts with '<!--\\s*#' and so only matches
        # standalone alias comments where '#' immediately follows the
        # opening '<!--'. Aliases inside combined-command comments
        # (e.g., '<!--style:Foo ; #intro-->') are intentionally not
        # extracted here -- pre-existing scope of this script.
        self.assertEqual(
            add_aliases.get_existing_aliases("<!--style:Foo ; #intro-->"),
            set(),
        )

    def test_multiple_aliases_in_document(self):
        content = (
            "# Heading One\n"
            "<!--#one-->\n"
            "# Heading Two\n"
            "<!-- #two -->\n"
            "# Heading Three\n"
            "<!--#three-with-hyphens-->\n"
        )
        self.assertEqual(
            add_aliases.get_existing_aliases(content),
            {"one", "two", "three-with-hyphens"},
        )


if __name__ == "__main__":
    unittest.main()
