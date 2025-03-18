import re


class DocumentParser:
    def __init__(self, text: str, clean: bool = True):
        self.original_text = text
        # Optionally clean the text on initialization.
        self.text = self.clean_text(text) if clean else text

    def clean_text(self, text: str) -> str:
        """
        Normalize text by replacing newlines with spaces and removing extra whitespace.
        """
        cleaned = text.replace("\n", " ")
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned.strip()

    def return_sections(self, custom_sections: set = None) -> dict:
        """
        Split the original text into sections.

        For resumes, common sections might be "OBJECTIVE", "SUMMARY", "EXPERIENCE",
        "EDUCATION", "SKILLS", "PROJECTS", etc. A line is assumed to be a section header if
        it is entirely uppercase (and short) or matches one of the common resume section names.
        Alternatively, the user may provide a set of custom section headers to look for.

        Parameters:
            custom_sections (set, optional): A set of custom section header strings to use for
                section detection. If provided, these headers will be used instead of the default ones.

        Returns:
            dict: A dictionary where the keys are section headers and the values are the corresponding text.
        """
        sections = {}
        # Split based on original lines to preserve potential section headers.
        lines = self.original_text.splitlines()
        # Default section when no header is encountered.
        current_section = "GENERAL"
        sections[current_section] = []

        # Use provided custom sections or default common resume sections.
        default_sections = {
            "OBJECTIVE",
            "SUMMARY",
            "EXPERIENCE",
            "EDUCATION",
            "SKILLS",
            "PROJECTS",
            "CERTIFICATIONS",
            "AWARDS",
            "EXTRACURRICULAR",
        }
        resume_sections = (
            custom_sections if custom_sections is not None else default_sections
        )

        for line in lines:
            stripped = line.strip()
            # Check if the line qualifies as a section header.
            if stripped.upper() in resume_sections or (
                stripped.isupper() and len(stripped.split()) <= 4
            ):
                current_section = stripped.upper()
                sections[current_section] = []
            elif stripped:
                sections[current_section].append(stripped)

        # Join the lines in each section to form one block of text.
        for section in sections:
            sections[section] = " ".join(sections[section])
        return sections

    def search(self, keyword: str) -> list:
        """
        Search the cleaned text for occurrences of the keyword.
        Returns a list of context snippets (5 words before and after each match).
        """
        matches = []
        words = self.text.split()
        for i, word in enumerate(words):
            if keyword.lower() in word.lower():
                start = max(i - 5, 0)
                end = min(i + 6, len(words))
                context = " ".join(words[start:end])
                matches.append(context)
        return matches

    def extract_emails(self) -> list:
        """
        Extract email addresses from the cleaned text.
        """
        REGEX_PATTERN = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        return re.findall(REGEX_PATTERN, self.text)

    def extract_phone_numbers(self) -> list:
        """
        Extract phone numbers from the cleaned text.
        """
        import re

        phones = []

        # Pattern for formatted international numbers (preserves original format)
        formatted_pattern = r"(\+\d+\s*\(\d+\)\s*\d+[-\s]\d+)"

        # Pattern for other international numbers
        int_pattern = r"(\+\d+[\s\-.]?\d+[\s\-.]?\d+[\s\-.]?\d+)"

        # Pattern for local 10-digit numbers
        local_pattern = r"\b(\d{10})\b"

        # Find and add formatted international numbers (keeping original format)
        formatted_matches = re.findall(formatted_pattern, self.text)
        phones.extend(formatted_matches)

        # Find and normalize other international numbers
        int_matches = re.findall(int_pattern, self.text)
        for phone in int_matches:
            # Skip already added formatted numbers
            if phone not in formatted_matches:
                normalized = "+" + re.sub(r"[^0-9]", "", phone[1:])
                # Avoid duplicates
                if normalized not in phones:
                    phones.append(normalized)

        # Find local numbers
        local_matches = re.findall(local_pattern, self.text)
        for match in local_matches:
            if match not in phones:
                phones.append(match)

        return phones

    def extract_name(self) -> list:
        """
        Extract all matching name candidates from the original text using regex.
        Returns:
            List[str]: All matches from the regex pattern.
        """
        #! TODO : NEED TO FIND WAY TO REMOVE ALL THE NON NAMES returned in this list
        # Regex pattern to match names (supports title-case and all uppercase, with hyphens/apostrophes)
        regex_pattern = r"\b(?:[A-Z][a-z]+|[A-Z]+)(?:[-' ](?:[A-Z][a-z]+|[A-Z]+))*\b"
        # Return all matches found in the original text.
        return re.findall(regex_pattern, self.original_text)

    def extract_skills(self) -> list:
        """
        Attempt to extract skills from a section labeled "SKILLS".
        Assumes that skills are comma-separated in that section.
        """
        sections = self.return_sections()
        skills_text = sections.get("SKILLS", "")
        if skills_text:
            skills = [
                skill.strip() for skill in skills_text.split(",") if skill.strip()
            ]
            return skills
        return []
