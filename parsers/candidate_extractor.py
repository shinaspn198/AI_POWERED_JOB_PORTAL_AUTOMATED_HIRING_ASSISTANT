import re


class CandidateExtractor:
    """
    Extracts candidate information from parsed resume sections.
    """

    EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    PHONE_PATTERN = r"(?:\+91[- ]?)?[6-9]\d{4}[- ]?\d{5}"

    @staticmethod
    def extract(sections):

        candidate = {
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
            "summary": "",
            "skills": [],
            "experience": [],
            "education": [],
            "projects": [],
            "certifications": [],
            "languages": []
        }

        # ---------- General Section ----------

        general = sections.get("general", [])

        if general:
            candidate["name"] = general[0]

        general_text = "\n".join(general)

        # ---------- Email ----------

        email = re.search(
            CandidateExtractor.EMAIL_PATTERN,
            general_text
        )

        if email:
            candidate["email"] = email.group()

        # ---------- Phone ----------

        phone = re.search(
            CandidateExtractor.PHONE_PATTERN,
            general_text
        )

        if phone:
            candidate["phone"] = phone.group()

        # ---------- Location ----------

        location_patterns = [
    r"Location\s*:\s*(.+)",
    r"Location\s*-\s*(.+)",
    r"Location\s*\|\s*(.+)",
    r"Address\s*:\s*(.+)",
    r"Address\s*-\s*(.+)",
    r"City\s*:\s*(.+)",
    r"\|\s*([^|]+,\s*[^|]+)$"
]

        for pattern in location_patterns:

            location = re.search(
                pattern,
                general_text,
                re.IGNORECASE
            )

            if location:
                candidate["location"] = location.group(1).strip()
                break

        # ---------- Summary ----------

        explicit_summary = sections.get("summary", [])

        if explicit_summary:

            candidate["summary"] = "\n".join(
                explicit_summary
            )

        else:

            # Some resumes do not have a Summary heading.
            # In those resumes, the general section may contain:
            #
            # Name
            # Contact information
            # Professional title
            # Summary paragraph

            if len(general) > 3:

                possible_summary = general[3:]

                candidate["summary"] = " ".join(
                    possible_summary
                ).strip()

        # ---------- Other Sections ----------

        candidate["skills"] = sections.get(
            "skills", []
        )

        candidate["experience"] = sections.get(
            "experience", []
        )

        candidate["education"] = sections.get(
            "education", []
        )

        candidate["projects"] = sections.get(
            "projects", []
        )

        candidate["certifications"] = sections.get(
            "certifications", []
        )

        candidate["languages"] = sections.get(
            "languages", []
        )

        return candidate