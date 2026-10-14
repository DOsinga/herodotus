from copy import deepcopy
import unittest

from database import load_polities, validate_polities


class DescriptionTests(unittest.TestCase):
    def test_all_records_have_120_word_descriptions(self):
        for polity in load_polities():
            with self.subTest(polity=polity["id"]):
                self.assertEqual(len(polity["description"].split()), 120)

    def test_rejects_invalid_descriptions(self):
        polities = load_polities()
        for invalid in (None, 120, [], {}, "", "   ", "word " * 119, "word " * 121):
            with self.subTest(description=invalid):
                modified = deepcopy(polities)
                modified[0]["description"] = invalid
                with self.assertRaises(AssertionError):
                    validate_polities(modified)

    def test_rejects_missing_description(self):
        polities = load_polities()
        del polities[0]["description"]
        with self.assertRaises(AssertionError):
            validate_polities(polities)


if __name__ == "__main__":
    unittest.main()
