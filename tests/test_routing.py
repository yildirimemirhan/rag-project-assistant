"""Gate tests: project routing and document set. Deterministic, no models, no network."""
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from routing import KNOWN_PROJECTS, detect_project, extract_project  # noqa: E402

DOCS = os.path.join(ROOT, "documents")
KNOWLEDGE = os.path.join(ROOT, "knowledge")

ROUTES = [
    ("How did the WBC Analyzer raise OOD accuracy?", "wbc-analyzer"),
    ("What does the kinematic pipeline use for drift detection?", "kinematic"),
    ("How does Listing Pilot handle Dolap?", "listing-pilot"),
    ("Which similarity search does Popcorn Wagon use?", "popcorn-wagon"),
    ("How did you test the portal cleaner?", "portal-cleaner-ultimate"),
    ("What did you build at Esbi?", "crm-aspnetcore"),
    ("Tell me about the CRM application", "crm-aspnetcore"),
    ("How does this assistant avoid hallucination?", "rag-project-assistant"),
    ("What is your M.Sc. thesis about?", "research"),
    ("What do you do with blood smear microscopy and stain normalization?", "research"),
    ("Where did you study?", None),  # no keyword; falls back to full corpus
    ("What is your education?", "profile"),
    ("Are you available for part-time work?", "profile"),
    ("What is your email?", "profile"),
    ("What did you do at zidorun?", "profile"),
    ("Which certifications do you have?", "profile"),
    ("Özgeçmişin nedir?", "profile"),
    ("What is the capital of France?", None),
]

# Claims the vetted resume/LinkedIn no longer support.
BANNED = [
    r"1st (place|on)",
    r"700\+ (processed |live )?transactions",
    r"Applied ML Engineer",
    r"final-year",
    r"~1,000 active listings",
]


class TestRouting(unittest.TestCase):
    def test_routes(self):
        for query, expected in ROUTES:
            with self.subTest(query=query):
                self.assertEqual(detect_project(query), expected)

    def test_extract_project_prefix(self):
        self.assertEqual(extract_project("crm-aspnetcore_highlights.txt"), "crm-aspnetcore")
        self.assertEqual(extract_project("kinematic_README.md"), "kinematic")
        self.assertEqual(extract_project("profile_README.md"), "profile")
        self.assertEqual(extract_project("mystery.txt"), "unknown")


class TestDocuments(unittest.TestCase):
    def setUp(self):
        self.files = [f for f in os.listdir(DOCS) if f.endswith((".txt", ".md"))]

    def test_every_project_has_a_document(self):
        for project in KNOWN_PROJECTS:
            with self.subTest(project=project):
                self.assertTrue(any(extract_project(f) == project for f in self.files))

    def test_no_unrouted_documents(self):
        unknown = [f for f in self.files if extract_project(f) == "unknown"]
        self.assertEqual(unknown, [])

    def test_knowledge_docs_are_in_documents(self):
        for name in os.listdir(KNOWLEDGE):
            with self.subTest(name=name):
                with open(os.path.join(KNOWLEDGE, name), "rb") as a, open(os.path.join(DOCS, name), "rb") as b:
                    self.assertEqual(a.read(), b.read(), "run prepare_docs.copy_knowledge()")

    def test_no_stale_claims(self):
        for f in self.files:
            with open(os.path.join(DOCS, f), encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
            for pattern in BANNED:
                with self.subTest(file=f, pattern=pattern):
                    self.assertIsNone(re.search(pattern, text, re.I))


if __name__ == "__main__":
    unittest.main()
