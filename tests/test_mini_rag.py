"""Test the offline educational retrieve/augment example using the standard library."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from mini_rag import build_prompt, char_bigrams, retrieve


class MiniRagTests(unittest.TestCase):
    def test_2026_policy_ranked_before_unrelated_account(self):
        hits = retrieve("2026 版退款多久？", version="2026", k=2)
        self.assertEqual(hits[0]["id"], "S1")
        self.assertTrue(all(d["version"] == "2026" for d in hits))

    def test_version_filter_excludes_old_policy(self):
        self.assertEqual(retrieve("2026 版退款多久？", "2025")[0]["id"], "S2")

    def test_zero_k_and_nonnegative_contract(self):
        self.assertEqual(retrieve("退款", "2026", k=0), [])
        with self.assertRaises(ValueError):
            retrieve("退款", "2026", k=-1)

    def test_prompt_has_explicit_source_ids_and_no_fake_answer(self):
        prompt = build_prompt("2026 版退款多久？", retrieve("2026 版退款多久？", "2026"))
        self.assertIn("[S1]", prompt)
        self.assertIn("QUESTION:", prompt)
        self.assertNotIn("ANSWER: 7", prompt)

    def test_bigrams_deterministic(self):
        self.assertEqual(char_bigrams("付款 后"), {"付款", "款后"})


if __name__ == "__main__":
    unittest.main()
