"""Deterministic indexing foundations, no network nor model downloads."""
import unittest
from examples.structured_ingest import EXAMPLE_HTML, ingest_html
from examples.chunking_lab import (
    fixed_windows, expected_windows, section_spans, parent_child_records, EXAMPLE
)
from examples.embedding_lab import (
    DOCUMENTS, dot, cosine, rank, infonce_loss, maxsim
)


class DocumentParserTests(unittest.TestCase):
    def test_table_has_column_qualified_values(self):
        records = ingest_html(EXAMPLE_HTML, "policy", "v2026", "support")
        rows = [r for r in records if r["kind"] == "table_row"]
        self.assertEqual(len(rows), 2)
        self.assertIn("地区：中国大陆；退款时限：7天", rows[0]["text"])

    def test_lineage_metadata_and_determinism(self):
        a = ingest_html(EXAMPLE_HTML, "policy", "v2026", "support")
        b = ingest_html(EXAMPLE_HTML, "policy", "v2026", "support")
        self.assertEqual(a, b)
        self.assertTrue(all(r["source_sha256"] and r["chunk_id"] for r in a))
        changed = ingest_html(EXAMPLE_HTML, "policy", "v2027", "support")
        self.assertNotEqual(a[0]["chunk_id"], changed[0]["chunk_id"])
        self.assertEqual(a[0]["access_group"], "support")


class ChunkTests(unittest.TestCase):
    def test_no_empty_and_exact_last_window(self):
        self.assertEqual(fixed_windows("", 5, 2), [])
        a = fixed_windows("abcdefghijk", size=5, overlap=2)
        self.assertEqual([(x["start"], x["end"]) for x in a],
                         [(0, 5), (3, 8), (6, 11)])
        self.assertEqual(a[-1]["text"], "ghijk")
        self.assertEqual(len(a), expected_windows(11, 5, 2))

    def test_reject_invalid_overlap(self):
        for cfg in ((0, 0), (5, -1), (5, 5), (5, 9)):
            with self.subTest(cfg=cfg), self.assertRaises(ValueError):
                fixed_windows("any", *cfg)

    def test_sections_preserve_source_text(self):
        ps = section_spans(EXAMPLE)
        self.assertEqual("".join(p["text"] for p in ps), EXAMPLE)
        self.assertEqual([p["title"] for p in ps],
                         ["退款规则", "账户安全"])

    def test_child_offsets_and_parent_id(self):
        parents, children = parent_child_records(EXAMPLE, 12, 3)
        self.assertTrue(parents and children)
        for c in children:
            self.assertEqual(EXAMPLE[c["start"]:c["end"]], c["text"])
            self.assertRegex(c["parent_id"], r"^P[0-9]+$")


class GeometryTests(unittest.TestCase):
    def test_raw_dot_vs_cosine_order(self):
        self.assertEqual(rank((1.0, 0.0), DOCUMENTS)[0][0], "D1")
        self.assertEqual(rank((1.0, 0.0), DOCUMENTS, "dot")[0][0], "D2")

    def test_nonzero_cosine_and_validation(self):
        self.assertAlmostEqual(cosine((1, 0), (0, 1)), 0.0)
        with self.assertRaises(ValueError):
            cosine((0, 0), (1, 0))
        with self.assertRaises(ValueError):
            dot([1], [1, 2])

    def test_contrastive_loss_direction(self):
        q = (1.0, 0.0)
        self.assertLess(infonce_loss(q, (1, 0), [(0, 1)], .5),
                        infonce_loss(q, (0, 1), [(1, 0)], .5))

    def test_token_maxsim(self):
        self.assertEqual(maxsim([(1, 0), (0, 1)], [(0, 1), (1, 0)]), 2.0)
        with self.assertRaises(ValueError):
            maxsim([], [(1, 0)])


if __name__ == "__main__":
    unittest.main()
