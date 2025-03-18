import unittest
from doc_parser.parser import DocumentParser


class TestDocumentParser(unittest.TestCase):

    def setUp(self):
        # Example text simulating a resume with various sections.
        self.resume_text = (
            "John Doe\n"
            "john.doe@example.com\n"
            "+1 (555) 123-4567\n"
            "\n"
            "OBJECTIVE\n"
            "To obtain a challenging position in a reputable organization.\n"
            "\n"
            "EXPERIENCE\n"
            "Software Engineer at ABC Corp\n"
            "Developed innovative solutions.\n"
            "\n"
            "EDUCATION\n"
            "Bachelor of Science in Computer Science\n"
            "XYZ University\n"
            "\n"
            "SKILLS\n"
            "Python, Java, C++, SQL, JavaScript\n"
        )
        self.parser = DocumentParser(self.resume_text)

    def test_clean_text(self):
        messy_text = "Hello,\n\n   world!  This is   a test.\nNew line here."
        parser = DocumentParser(messy_text)
        self.assertNotIn("\n", parser.text)
        self.assertNotIn("  ", parser.text)

    def test_return_sections_default(self):
        sections = self.parser.return_sections()
        self.assertIn("OBJECTIVE", sections)
        self.assertIn("EXPERIENCE", sections)
        self.assertIn("EDUCATION", sections)
        self.assertIn("SKILLS", sections)
        self.assertIn("GENERAL", sections)
        self.assertIn("To obtain a challenging position", sections["OBJECTIVE"])

    def test_return_sections_custom(self):
        custom = {"INTRODUCTION", "BODY", "CONCLUSION"}
        text = (
            "INTRODUCTION\n"
            "This is an intro.\n"
            "BODY\n"
            "The main part of the document.\n"
            "CONCLUSION\n"
            "The end."
        )
        parser = DocumentParser(text, clean=False)
        sections = parser.return_sections(custom_sections=custom)
        self.assertIn("INTRODUCTION", sections)
        self.assertIn("BODY", sections)
        self.assertIn("CONCLUSION", sections)
        self.assertEqual(sections["INTRODUCTION"], "This is an intro.")
        self.assertEqual(sections["BODY"], "The main part of the document.")
        self.assertEqual(sections["CONCLUSION"], "The end.")

    def test_search(self):
        results = self.parser.search("Software")
        self.assertGreater(len(results), 0)
        self.assertTrue(any("Software" in snippet for snippet in results))

    def test_extract_emails(self):
        emails = self.parser.extract_emails()
        self.assertIn("john.doe@example.com", emails)

    def test_extract_phone_numbers(self):
        # Test using resume text.
        phones = self.parser.extract_phone_numbers()
        self.assertIn("+1 (555) 123-4567", phones)

        # Test for a local phone number without international code.
        text_local = "Please call 5551234567 for more info."
        parser_local = DocumentParser(text_local)
        phones_local = parser_local.extract_phone_numbers()
        self.assertIn("5551234567", phones_local)

        # Test for an international phone number without spaces.
        text_international_no_space = "Please call +971568098085 for more info."
        parser_international_no_space = DocumentParser(text_international_no_space)
        phones_international_no_space = (
            parser_international_no_space.extract_phone_numbers()
        )
        self.assertIn("+971568098085", phones_international_no_space)

        # Test for an international phone number with spaces and irregular delimiters.
        text_international_with_space_type_1 = (
            "Please call +971 56 809 8085 for more info."
        )
        text_international_with_space_type_2 = (
            "Please call +971 568098085 for more info."
        )
        parser_international_with_space_type_2 = DocumentParser(
            text_international_with_space_type_1
        )

        parser_international_with_space_type_1 = DocumentParser(
            text_international_with_space_type_1
        )
        parser_international_with_space_type_2 = DocumentParser(
            text_international_with_space_type_2
        )

        phones_international_with_space_type_1 = (
            parser_international_with_space_type_1.extract_phone_numbers()
        )
        phones_international_with_space_type_2 = (
            parser_international_with_space_type_2.extract_phone_numbers()
        )

        # The normalized number should have no spaces/dashes.
        self.assertIn("+971568098085", phones_international_with_space_type_1)
        self.assertIn("+971568098085", phones_international_with_space_type_2)

    def test_extract_name(self):
        names = self.parser.extract_name()
        self.assertIn("John Doe", names)

        name_test = """
        Name : JOEL STEPHEN
        """
        name_test_parser = DocumentParser(name_test)
        names_test = name_test_parser.extract_name()
        self.assertIn("JOEL STEPHEN", names_test)

        candidates_text = """
            JOEL STEPHEN
            MARY ANN LOUISE
            John Smith
            John-Paul Smith
            O'Connor
            Alice
            Jean-Luc Picard
            Anne Marie
            JANE
            John O'Neil
            12345
            hello world
            john smith
        """
        candidate_parser = DocumentParser(candidates_text)
        names_list = candidate_parser.extract_name()
        expected_names = [
            "JOEL STEPHEN",
            "MARY ANN LOUISE",
            "John Smith",
            "John-Paul Smith",
            "O'Connor",
            "Alice",
            "Jean-Luc Picard",
            "Anne Marie",
            "JANE",
            "John O'Neil",
        ]
        for expected in expected_names:
            self.assertIn(expected, names_list)

        self.assertNotIn("12345", names_list)
        self.assertNotIn("hello world", names_list)
        self.assertNotIn("john smith", names_list)

    def test_extract_skills(self):
        skills = self.parser.extract_skills()
        self.assertIn("Python", skills)
        self.assertIn("JavaScript", skills)
        self.assertEqual(len(skills), 5)


if __name__ == "__main__":
    unittest.main()
