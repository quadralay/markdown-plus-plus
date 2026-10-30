"""Tests for validate-mdpp.py command splitting, fences, and container tags.

Run with: python -m unittest test_validate_mdpp
(must be invoked from this scripts/ directory)
"""

import importlib.util
import os
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_SPEC = importlib.util.spec_from_file_location(
    "validate_mdpp", os.path.join(_HERE, "validate-mdpp.py")
)
validate_mdpp = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(validate_mdpp)

BS = chr(92)  # backslash, spelled out so JSON escapes survive transit


def segments(content):
    parts, unterminated = validate_mdpp.split_commands(content)
    return [p.strip() for p in parts], unterminated


class SplitCommandsTests(unittest.TestCase):
    def test_plain_combined_tag(self):
        self.assertEqual(
            segments(' style:Note ; #a1 '),
            (['style:Note', '#a1'], False),
        )

    def test_semicolon_inside_quoted_marker_value(self):
        self.assertEqual(
            segments(' marker:Note="a; b" ; #n1 '),
            (['marker:Note="a; b"', '#n1'], False),
        )

    def test_equals_and_empty_values(self):
        self.assertEqual(
            segments('marker:Hyperlink="https://x.test/p?id=42";marker:DropDownEnd=""'),
            (['marker:Hyperlink="https://x.test/p?id=42"', 'marker:DropDownEnd=""'], False),
        )

    def test_semicolon_inside_json_string(self):
        self.assertEqual(
            segments(' markers:{"Key": "val;ue"} ; #alias '),
            (['markers:{"Key": "val;ue"}', '#alias'], False),
        )

    def test_escaped_quote_inside_json_string(self):
        content = 'markers:{"D": "say ' + BS + '"hi; there' + BS + '""} ; #p1'
        parts, unterminated = segments(content)
        self.assertEqual(len(parts), 2)
        self.assertEqual(parts[1], '#p1')
        self.assertFalse(unterminated)

    def test_nested_json_braces(self):
        self.assertEqual(
            segments('markers:{"A": {"b": "c;d"}} ; style:X'),
            (['markers:{"A": {"b": "c;d"}}', 'style:X'], False),
        )

    def test_unterminated_simple_value(self):
        # A --> inside the value ended the comment early.
        self.assertEqual(segments(' marker:Note="a'), (['marker:Note="a'], True))

    def test_unterminated_json(self):
        self.assertEqual(segments('markers:{"a": "b'), (['markers:{"a": "b'], True))


class SkipMaskTests(unittest.TestCase):
    def test_top_level_fence(self):
        lines = ['text', '```', 'code', '```', 'after']
        self.assertEqual(validate_mdpp._skip_mask(lines), [False, True, True, True, False])

    def test_fence_indented_four_spaces_under_ordered_item(self):
        lines = ['1. Step:', '', '    ```', '    $1bad;', '    ```', 'after']
        self.assertEqual(
            validate_mdpp._skip_mask(lines),
            [False, False, True, True, True, False],
        )

    def test_indented_code_is_not_a_fence(self):
        lines = ['Paragraph.', '', '    ```', '    not a fence', 'after']
        self.assertEqual(validate_mdpp._skip_mask(lines), [False] * 5)

    def test_closing_fence_cannot_have_an_info_string(self):
        lines = ['```markdown', '```python', 'x', '```', 'after']
        self.assertEqual(
            validate_mdpp._skip_mask(lines),
            [True, True, True, True, False],
        )

    def test_fence_inside_blockquote(self):
        lines = ['> ```', '> <!-- style:123Bad -->', '> ```', '> after']
        self.assertEqual(validate_mdpp._skip_mask(lines), [True, True, True, False])

    def test_front_matter_is_skipped(self):
        lines = ['---', 'description: <!--style:--> mention', '---', 'Body']
        self.assertEqual(validate_mdpp._skip_mask(lines), [True, True, True, False])

    def test_inline_backticks_are_not_a_fence(self):
        lines = ['```inline``` code', 'after']
        self.assertEqual(validate_mdpp._skip_mask(lines), [False, False])


class ContainerTagTests(unittest.TestCase):
    def test_tag_in_blockquote(self):
        self.assertTrue(validate_mdpp._is_mdpp_tag_line('> <!-- style:Note ; #n1 -->'))

    def test_tag_on_list_marker_line(self):
        self.assertTrue(validate_mdpp._is_mdpp_tag_line('2. <!-- style:BQ_Note ; #q -->'))

    def test_regular_comment_is_not_a_tag(self):
        self.assertFalse(validate_mdpp._is_mdpp_tag_line('<!-- # TODO -->'))
        self.assertFalse(validate_mdpp._is_mdpp_tag_line('> <!-- just a note -->'))

    def test_blank_quote_line_is_not_content(self):
        self.assertFalse(validate_mdpp._is_content_line('>'))
        self.assertTrue(validate_mdpp._is_content_line('> text'))

    def test_list_item_opening_with_a_tag_is_content(self):
        # A list style above a list item whose first block is its own tag.
        self.assertTrue(validate_mdpp._is_content_line(
            '- <!--style:CustomParagraph-->', tag_line='<!--style:CustomUList-->'))

    def test_deeper_blockquote_opening_with_a_tag_is_content(self):
        self.assertTrue(validate_mdpp._is_content_line(
            '> > <!-- style:Inner -->', tag_line='> <!-- style:Outer -->'))

    def test_stacked_tags_at_the_same_depth_are_not_content(self):
        self.assertFalse(validate_mdpp._is_content_line(
            '> <!-- style:B -->', tag_line='> <!-- style:A -->'))


def codes(line):
    """Issue codes _check_comment_commands reports for one line."""
    issues = validate_mdpp._check_comment_commands(line, 1, 'test.md', {}, {}, False)
    return [i.code for i in issues]


class DuplicateMarkerKeyTests(unittest.TestCase):
    """MDPP022: a marker key used more than once in one comment tag."""

    def test_repeated_key_in_json(self):
        self.assertEqual(codes('<!-- markers:{"TopicAlias":"a", "TopicAlias":"b"} -->'), ['MDPP022'])

    def test_repeated_simple_commands(self):
        self.assertEqual(codes('<!-- marker:TopicAlias="a" ; marker:TopicAlias="b" -->'), ['MDPP022'])

    def test_repeated_across_simple_and_json_forms(self):
        self.assertEqual(
            codes('<!-- marker:Keywords="x" ; markers:{"Keywords":"y", "Description":"d"} -->'),
            ['MDPP022'])

    def test_identical_repeated_values_warn_once(self):
        self.assertEqual(codes('<!-- markers:{"P":"same", "P":"same", "P":"same"} -->'), ['MDPP022'])

    def test_inline_tag(self):
        self.assertEqual(codes('Run <!--marker:Keywords="a" ; marker:Keywords="b"-->**this**.'), ['MDPP022'])

    def test_distinct_keys_do_not_warn(self):
        self.assertEqual(codes('<!-- marker:Keywords="x" ; markers:{"A":"1", "B":"2"} ; #k1 -->'), [])

    def test_keys_are_case_sensitive(self):
        self.assertEqual(codes('<!-- marker:Keywords="x" ; marker:keywords="y" -->'), [])

    def test_same_key_in_separate_tags_does_not_warn(self):
        self.assertEqual(codes('<!-- marker:TopicAlias="a" --> <!-- marker:TopicAlias="b" -->'), [])

    def test_malformed_json_reports_mdpp003_only(self):
        self.assertEqual(codes('<!-- markers:{"A":"1", "A": } -->'), ['MDPP003'])


if __name__ == '__main__':
    unittest.main()
